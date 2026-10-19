"""Agente 03: asistente con memoria local persistente."""

import asyncio
import os

from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

from app_framework.memory_tools import (
    forget_memory,
    list_memories,
    remember_fact,
    search_memory,
)

load_dotenv()


def build_agent() -> Agent:
    """Construye el agente con herramientas explícitas de memoria local."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY. Configúrala en tu archivo .env.")

    model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
    client = OpenAIChatClient(model=model, api_key=api_key)
    return Agent(
        client=client,
        name="AsistenteConMemoria",
        instructions=(
            "Eres un asistente educativo que responde en español. "
            "Tu memoria persistente está en un archivo local y solo puedes acceder "
            "a ella mediante las herramientas disponibles. "
            "Guarda información únicamente cuando el usuario lo pida de forma explícita "
            "con expresiones como 'recuerda' o 'guarda en memoria'. "
            "No guardes contraseñas, claves API, datos financieros, datos de salud "
            "ni otra información personal sensible. Si el usuario solicita guardar "
            "algo sensible, explica que este ejemplo no debe utilizarse para ello. "
            "Antes de afirmar que recuerdas algo de una conversación anterior, busca "
            "la información con search_memory o list_memories. "
            "Para borrar un recuerdo, identifica su ID y usa forget_memory; no afirmes "
            "que se ha borrado si la herramienta no lo confirma. "
            "No inventes recuerdos ni afirmes tener acceso a conversaciones que no estén "
            "guardadas en esta memoria local."
        ),
        tools=[remember_fact, search_memory, list_memories, forget_memory],
    )


async def run_agent(user_message: str) -> str:
    """Ejecuta una petición y devuelve la respuesta textual del agente."""
    agent = build_agent()
    response = await agent.run(user_message)
    return response.text


async def main() -> None:
    print("🤖 Agente 03 — Asistente con memoria local")
    print("La memoria persiste en data/memory.json entre ejecuciones.")
    print("No guardes contraseñas ni datos sensibles. Escribe 'salir' para terminar.\n")
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
