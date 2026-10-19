"""Agente 04: agente conectado a una API meteorológica externa."""

import asyncio
import os

from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

from app_framework.weather_tools import get_weather

load_dotenv()


def build_agent() -> Agent:
    """Construye el agente con la herramienta de consulta meteorológica."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY. Configúrala en tu archivo .env.")

    model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
    client = OpenAIChatClient(model=model, api_key=api_key)
    return Agent(
        client=client,
        name="AsistenteMeteorologico",
        instructions=(
            "Eres un asistente meteorológico educativo que responde en español. "
            "Cuando el usuario pregunte por el tiempo, pide la ciudad si no la indica "
            "y utiliza get_weather. No inventes condiciones, temperaturas ni previsiones. "
            "Distingue claramente los datos devueltos por la API de cualquier explicación. "
            "Indica que la consulta procede de Open-Meteo y que las previsiones pueden cambiar."
        ),
        tools=[get_weather],
    )


async def run_agent(user_message: str) -> str:
    """Ejecuta una petición y devuelve la respuesta del agente."""
    agent = build_agent()
    response = await agent.run(user_message)
    return response.text


async def main() -> None:
    print("🌦️ Agente 04 — Consulta del tiempo mediante API externa")
    print("Fuente: Open-Meteo (no necesita una clave meteorológica).")
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
