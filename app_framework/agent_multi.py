"""Agente 02: agente con varias herramientas usando Microsoft Agent Framework."""

import asyncio
import os

from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

from app_framework.tools import calculate
from app_framework.tools_multi import current_datetime, get_note, list_notes, save_note

load_dotenv()


def build_agent() -> Agent:
    """Construye el agente con calculadora, fecha/hora y herramientas de notas."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY. Configúrala en tu archivo .env.")

    model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
    client = OpenAIChatClient(model=model, api_key=api_key)
    return Agent(
        client=client,
        name="AsistenteMultiHerramienta",
        instructions=(
            "Eres un asistente educativo que responde en español. "
            "Dispones de herramientas para calcular, consultar la fecha y hora, "
            "guardar notas, listar sus títulos y recuperar una nota por título. "
            "Utiliza las herramientas cuando la petición lo requiera. "
            "No afirmes que has guardado o recuperado una nota si la herramienta "
            "no confirma que la operación se haya realizado. "
            "Antes de guardar una nota, identifica claramente el título y el contenido. "
            "No inventes la fecha ni la hora: consulta la herramienta correspondiente."
        ),
        tools=[calculate, current_datetime, save_note, list_notes, get_note],
    )


async def run_agent(user_message: str) -> str:
    """Ejecuta una petición y devuelve el texto de respuesta."""
    agent = build_agent()
    response = await agent.run(user_message)
    return response.text


async def main() -> None:
    print("🤖 Agente 02 — Asistente con varias herramientas")
    print("Herramientas: calculadora, fecha/hora y notas locales.")
    print("Las notas se guardan en data/notes.json. Escribe 'salir' para terminar.\n")
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
