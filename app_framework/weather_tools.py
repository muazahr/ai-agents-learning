"""Herramienta meteorológica basada en la API pública de Open-Meteo."""

import json
from typing import Annotated
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from agent_framework import tool

WEATHER_CODES = {
    0: "despejado",
    1: "mayormente despejado",
    2: "parcialmente nuboso",
    3: "cubierto",
    45: "niebla",
    48: "niebla con escarcha",
    51: "llovizna ligera",
    53: "llovizna moderada",
    55: "llovizna intensa",
    61: "lluvia ligera",
    63: "lluvia moderada",
    65: "lluvia intensa",
    71: "nieve ligera",
    73: "nieve moderada",
    75: "nieve intensa",
    80: "chubascos ligeros",
    81: "chubascos moderados",
    82: "chubascos intensos",
    95: "tormenta",
    96: "tormenta con granizo ligero",
    99: "tormenta con granizo intenso",
}


def _fetch_json(url: str) -> dict:
    """Obtiene JSON de una URL pública con timeout y User-Agent."""
    request = Request(url, headers={"User-Agent": "ai-agents-learning/1.0"})
    with urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


@tool(approval_mode="never_require")
def get_weather(
    city: Annotated[str, "Nombre de la ciudad para la que se consulta el tiempo"],
) -> str:
    """Consulta el tiempo actual y la previsión diaria usando Open-Meteo, sin API key."""
    city = city.strip()
    if not city or len(city) > 120:
        return "Indica una ciudad válida (máximo 120 caracteres)."

    try:
        geo_query = urlencode({"name": city, "count": 1, "language": "es", "format": "json"})
        geocoding = _fetch_json("https://geocoding-api.open-meteo.com/v1/search?" + geo_query)
        locations = geocoding.get("results") or []
        if not locations:
            return "No encontré esa ciudad. Prueba con otro nombre o añade el país."

        location = locations[0]
        latitude = location.get("latitude")
        longitude = location.get("longitude")
        if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
            return "La API no devolvió coordenadas válidas para esa ciudad."

        forecast_query = urlencode({
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "forecast_days": 1,
            "timezone": "auto",
        })
        forecast = _fetch_json("https://api.open-meteo.com/v1/forecast?" + forecast_query)
        current = forecast.get("current") or {}
        daily = forecast.get("daily") or {}
        code = current.get("weather_code")
        condition = WEATHER_CODES.get(code, "estado del cielo no disponible")
        name = location.get("name", city)
        country = location.get("country", "")
        place = "{}, {}".format(name, country) if country else name

        temperature = current.get("temperature_2m")
        feels_like = current.get("apparent_temperature")
        humidity = current.get("relative_humidity_2m")
        wind = current.get("wind_speed_10m")
        date = (daily.get("time") or ["fecha no disponible"])[0]
        maximum = (daily.get("temperature_2m_max") or [None])[0]
        minimum = (daily.get("temperature_2m_min") or [None])[0]
        rain_chance = (daily.get("precipitation_probability_max") or [None])[0]

        lines = ["Tiempo en {} ({}): {}".format(place, date, condition)]
        if temperature is not None:
            lines.append("Temperatura actual: {} °C".format(temperature))
        if feels_like is not None:
            lines.append("Sensación térmica: {} °C".format(feels_like))
        if minimum is not None and maximum is not None:
            lines.append("Mínima/máxima prevista: {} / {} °C".format(minimum, maximum))
        if humidity is not None:
            lines.append("Humedad relativa: {} %".format(humidity))
        if wind is not None:
            lines.append("Viento: {} km/h".format(wind))
        if rain_chance is not None:
            lines.append("Probabilidad máxima de precipitación hoy: {} %".format(rain_chance))
        lines.append("Fuente: Open-Meteo. Consulta orientativa; las condiciones pueden cambiar.")
        return "\n".join(lines)
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, TypeError) as exc:
        return "No se pudo consultar el tiempo ahora mismo ({}). Inténtalo de nuevo más tarde.".format(
            type(exc).__name__
        )
