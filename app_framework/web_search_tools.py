"""Herramienta de búsqueda en Wikipedia en español mediante su API REST."""

import json
import re
from html import unescape
from typing import Annotated
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from agent_framework import tool


def _fetch_json(url: str) -> dict:
    request = Request(
        url,
        headers={
            "User-Agent": "ai-agents-learning/1.0 (educational project)",
            "Accept": "application/json",
        },
    )
    with urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def _clean_html(text: str) -> str:
    """Elimina etiquetas sencillas de los extractos devueltos por la API."""
    return unescape(re.sub(r"<[^>]+>", " ", text)).strip()


@tool(approval_mode="never_require")
def search_wikipedia(
    query: Annotated[str, "Tema o pregunta que buscar en Wikipedia en español"],
) -> str:
    """Busca artículos en Wikipedia en español; no equivale a buscar en toda Internet."""
    query = query.strip()
    if not query or len(query) > 200:
        return "Escribe una búsqueda de entre 1 y 200 caracteres."

    try:
        params = urlencode({"q": query, "limit": 5})
        data = _fetch_json("https://es.wikipedia.org/w/rest.php/v1/search/page?" + params)
        pages = data.get("pages") or []
        if not pages:
            return "Wikipedia no devolvió resultados para esa búsqueda."

        results = []
        for page in pages[:5]:
            title = page.get("title", "Título no disponible")
            description = page.get("description", "")
            excerpt = _clean_html(page.get("excerpt", ""))
            lines = ["- " + title]
            if description:
                lines.append("  Descripción: " + description)
            if excerpt:
                lines.append("  Extracto: " + excerpt)
            lines.append(
                "  Enlace: https://es.wikipedia.org/wiki/"
                + str(page.get("key", title.replace(" ", "_"))).replace(" ", "_")
            )
            results.append("\n".join(lines))
        return "Resultados de Wikipedia en español para '{}':\n{}".format(
            query, "\n".join(results)
        )
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, TypeError, AttributeError) as exc:
        return "No se pudo consultar Wikipedia ahora mismo ({}). Inténtalo más tarde.".format(
            type(exc).__name__
        )
