"""Agente 05: búsqueda de información con la API de Wikipedia."""

import asyncio
import os

from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

from app_framework.web_search_tools import search_wikipedia

load_dotenv()


def build_agent() -> Agent:
    """Construye un agente que puede buscar artículos de Wikipedia."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY. Configúrala en tu archivo .env.")

    model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
    client = OpenAIChatClient(model=model, api_key=api_key)
    return Agent(
        client=client,
        name="AsistenteInvestigador",
        instructions=(
            "Eres un asistente investigador educativo y respondes en español. "
            "Cuando la pregunta necesite información sobre un tema, utiliza "
            "search_wikipedia para buscar fuentes y enlaces. Basa el resumen en los "
            "resultados devueltos y distingue los datos de tus explicaciones. "
            "No digas que has buscado en toda Internet: esta herramienta solo consulta "
            "Wikipedia en español. Si no hay resultados o falla la API, dilo claramente. "
            "Incluye los enlaces de los artículos usados y no inventes citas."
        ),
        tools=[search_wikipedia],
    )


async def run_agent(user_message: str) -> str:
    """Ejecuta una petición y devuelve la respuesta del agente."""
    agent = build_agent()
    response = await agent.run(user_message)
    return response.text


async def main() -> None:
    print("🔎 Agente 05 — Búsqueda en Wikipedia")
    print("Esta herramienta consulta Wikipedia en español, no toda Internet.")
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
