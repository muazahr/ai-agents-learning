from app_framework import weather_tools


def test_get_weather_requires_city():
    assert "ciudad válida" in weather_tools.get_weather(" ")


def test_get_weather_uses_geocoding_and_forecast(monkeypatch):
    responses = [
        {"results": [{"name": "Granada", "country": "España", "latitude": 37.18, "longitude": -3.6}]},
        {
            "current": {
                "temperature_2m": 22,
                "apparent_temperature": 23,
                "relative_humidity_2m": 40,
                "wind_speed_10m": 8,
                "weather_code": 0,
            },
            "daily": {
                "time": ["2026-10-19"],
                "temperature_2m_min": [12],
                "temperature_2m_max": [24],
                "precipitation_probability_max": [5],
            },
        },
    ]
    requested_urls = []

    def fake_fetch(url):
        requested_urls.append(url)
        return responses.pop(0)

    monkeypatch.setattr(weather_tools, "_fetch_json", fake_fetch)
    result = weather_tools.get_weather("Granada")

    assert "Granada, España" in result
    assert "22 °C" in result
    assert "despejado" in result
    assert len(requested_urls) == 2


def test_get_weather_handles_unknown_city(monkeypatch):
    monkeypatch.setattr(weather_tools, "_fetch_json", lambda url: {"results": []})
    assert "No encontré esa ciudad" in weather_tools.get_weather("Ciudad inventada")
