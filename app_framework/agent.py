"""Versión del agente que utiliza Microsoft Agent Framework."""

import asyncio
import os

from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

from app_framework.tools import calculate

load_dotenv()


def build_agent() -> Agent:
    """Construye y devuelve el agente con la herramienta de cálculo."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY. Configúrala en tu archivo .env.")

    model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
    client = OpenAIChatClient(model=model, api_key=api_key)
    return Agent(
        client=client,
        name="CalculadoraAgent",
        instructions=(
            "Eres un agente educativo y respondes en español. "
            "Cuando la pregunta requiera un cálculo, utiliza la herramienta calculate. "
            "Explica brevemente el resultado al usuario."
        ),
        tools=[calculate],
    )


async def run_agent(user_message: str) -> str:
    """Ejecuta una petición y devuelve el texto de respuesta."""
    agent = build_agent()
    response = await agent.run(user_message)
    return response.text


async def main() -> None:
    print("🤖 AI Agent — Microsoft Agent Framework")
    print("Escribe 'salir' para terminar.\n")
    while True:
        message = input("Tú: ").strip()
        if message.lower() in {"salir", "exit", "quit"}:
            print("Agente: ¡Hasta luego!")
            return
        if not message:
            continue
        try:
            print(f"Agente: {await run_agent(message)}\n")
        except Exception as exc:
            print(f"Error: {exc}\n")


if __name__ == "__main__":
    asyncio.run(main())
