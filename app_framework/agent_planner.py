"""Agente 06: planifica una petición y coordina herramientas de solo lectura."""

import asyncio
import os

from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

from app_framework.tools import calculate
from app_framework.tools_multi import current_datetime
from app_framework.weather_tools import get_weather
from app_framework.web_search_tools import search_wikipedia

load_dotenv()


def build_agent() -> Agent:
    """Construye un agente que descompone objetivos y usa varias herramientas."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY. Configúrala en tu archivo .env.")

    model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
    client = OpenAIChatClient(model=model, api_key=api_key)
    return Agent(
        client=client,
        name="PlanificadorDeTareas",
        instructions=(
            "Eres un agente planificador educativo y respondes en español. "
            "Para una petición compleja, identifica el objetivo y divídelo en pasos "
            "pequeños y ordenados. Decide qué herramientas necesitas y úsalas cuando "
            "aportan datos reales: calculate para matemáticas, current_datetime para "
            "fecha y hora local, get_weather para meteorología y search_wikipedia para "
            "buscar artículos en Wikipedia en español. Ejecuta los pasos en un orden "
            "lógico, evita llamadas innecesarias y presenta el resultado con un resumen "
            "y una lista breve de pasos completados. Si falta información esencial, "
            "haz una pregunta concreta. No inventes resultados ni digas que has usado "
            "una herramienta si no se ha ejecutado. Esta versión solo dispone de "
            "herramientas de consulta y cálculo: no puede realizar compras, enviar "
            "mensajes ni modificar sistemas externos. Si una herramienta falla, explica "
            "la limitación y separa los hechos confirmados de las inferencias."
        ),
        tools=[calculate, current_datetime, get_weather, search_wikipedia],
    )


async def run_agent(user_message: str) -> str:
    """Ejecuta el objetivo del usuario y devuelve la respuesta del planificador."""
    agent = build_agent()
    response = await agent.run(user_message)
    return response.text


async def main() -> None:
    print("🧭 Agente 06 — Planificación y coordinación de herramientas")
    print("Puede calcular, consultar fecha/hora, meteorología y Wikipedia.")
    print("Solo usa herramientas de lectura y cálculo; no ejecuta acciones externas.")
    print("Escribe 'salir' para terminar.\n")
    while True:
        message = input("Tú: ").strip()
        if message.lower() in {"salir", "exit", "quit"}:
            print("Agente: ¡Hasta luego!")
            return
        if not message:
            continue
        try:
            print("Agente: {}\n".format(await run_agent(message)))
        except Exception as exc:
            print("Error: {}\n".format(exc))


if __name__ == "__main__":
    asyncio.run(main())
