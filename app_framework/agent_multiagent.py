"""Agente 07: sistema multiagente con router, especialistas y coordinador."""

import asyncio
import os
import re

from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

from app_framework.tools import calculate
from app_framework.tools_multi import current_datetime
from app_framework.weather_tools import get_weather
from app_framework.web_search_tools import search_wikipedia

load_dotenv()

WEATHER_TERMS = (
    "tiempo", "clima", "temperatura", "lluvia", "llueve",
    "previsión", "pronóstico", "meteorología", "weather",
)
RESEARCH_TERMS = (
    "investiga", "busca", "historia", "quién", "quien", "qué es",
    "que es", "información", "informacion", "wikipedia", "artículos",
    "articulos", "explica", "resumen",
)
DATE_TERMS = ("fecha", "hora actual", "qué hora", "que hora", "qué día", "que dia", "hoy")
MATH_TERMS = ("calcula", "calcular", "cuánto es", "cuanto es", "resuelve", "multiplica", "divide")


def route_request(message: str) -> list[str]:
    """Selecciona especialistas con reglas simples y previsibles."""
    normalized = message.casefold()
    selected: list[str] = []

    if any(term in normalized for term in WEATHER_TERMS):
        selected.append("weather")

    if any(term in normalized for term in DATE_TERMS):
        selected.append("datetime")

    has_math_symbol = bool(re.search(r"\d\s*[+*/%-]\s*\d", normalized))
    if has_math_symbol or any(term in normalized for term in MATH_TERMS):
        selected.append("math")

    if any(term in normalized for term in RESEARCH_TERMS):
        selected.append("research")

    if not selected:
        selected.append("research")
    return selected


def _create_agent(
    client: OpenAIChatClient,
    name: str,
    instructions: str,
    tools: list | None = None,
) -> Agent:
    return Agent(
        client=client,
        name=name,
        instructions=instructions,
        tools=tools or [],
    )


def _get_client() -> OpenAIChatClient:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY. Configúrala en tu archivo .env.")
    model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
    return OpenAIChatClient(model=model, api_key=api_key)


async def _run_specialist(kind: str, user_message: str, client: OpenAIChatClient) -> str:
    """Ejecuta un especialista concreto y devuelve su resultado."""
    if kind == "weather":
        agent = _create_agent(
            client,
            "EspecialistaMeteorologia",
            "Responde en español. Identifica la ciudad de la petición y utiliza "
            "get_weather. Si no hay ciudad, pide que la indiquen. No inventes datos.",
            [get_weather],
        )
    elif kind == "datetime":
        agent = _create_agent(
            client,
            "EspecialistaFechaHora",
            "Responde en español. Para fecha u hora actual utiliza current_datetime. "
            "No inventes la hora local.",
            [current_datetime],
        )
    elif kind == "math":
        agent = _create_agent(
            client,
            "EspecialistaMatematico",
            "Responde en español y utiliza calculate para resolver la operación. "
            "Explica brevemente el resultado.",
            [calculate],
        )
    else:
        agent = _create_agent(
            client,
            "EspecialistaInvestigacion",
            "Responde en español. Busca artículos con search_wikipedia cuando sea útil. "
            "Aclara que la búsqueda está limitada a Wikipedia en español e incluye enlaces. "
            "No inventes fuentes.",
            [search_wikipedia],
        )

    response = await agent.run(user_message)
    return response.text


async def run_agent(user_message: str) -> str:
    """Coordina especialistas en paralelo y sintetiza sus resultados."""
    client = _get_client()
    route = route_request(user_message)
    results = await asyncio.gather(
        *[_run_specialist(kind, user_message, client) for kind in route],
        return_exceptions=True,
    )

    sections = []
    for kind, result in zip(route, results):
        if isinstance(result, Exception):
            sections.append("{}: el especialista no pudo completar su consulta ({}).".format(
                kind, type(result).__name__
            ))
        else:
            sections.append("{}:\n{}".format(kind, result))

    coordinator = _create_agent(
        client,
        "CoordinadorMultiagente",
        "Eres el coordinador de un sistema multiagente. Responde en español. "
        "Sintetiza las salidas de los especialistas para contestar la petición original. "
        "No inventes datos ni afirmes que un especialista tuvo éxito si su salida indica "
        "un error. Si faltan datos, dilo claramente. Organiza una respuesta breve y útil.",
    )
    prompt = (
        "Petición original del usuario:\n"
        + user_message
        + "\n\nResultados de los especialistas:\n"
        + "\n\n".join(sections)
    )
    response = await coordinator.run(prompt)
    return response.text


async def main() -> None:
    print("🤝 Agente 07 — Sistema multiagente")
    print("Router + especialistas en matemáticas, fecha/hora, meteorología e investigación.")
    print("Los especialistas independientes se ejecutan en paralelo.")
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
