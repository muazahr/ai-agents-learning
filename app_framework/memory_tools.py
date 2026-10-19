"""Herramientas de memoria local para el Agente 03.

La memoria se guarda en JSON en el equipo del usuario. No almacenes secretos
ni datos personales sensibles en este ejemplo educativo.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Annotated
from uuid import uuid4

from agent_framework import tool

MEMORY_FILE = Path("data") / "memory.json"


def _read_memories() -> list[dict[str, str]]:
    """Lee registros válidos de memoria; un archivo inexistente equivale a vacío."""
    if not MEMORY_FILE.exists():
        return []
    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []

    memories: list[dict[str, str]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        if all(isinstance(item.get(key), str) for key in ("id", "category", "fact", "created_at")):
            memories.append(item)
    return memories


def _write_memories(memories: list[dict[str, str]]) -> bool:
    """Escribe la memoria de forma controlada y comunica si hubo un error."""
    try:
        MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        temporary_file = MEMORY_FILE.with_suffix(".tmp")
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(memories, file, ensure_ascii=False, indent=2)
        temporary_file.replace(MEMORY_FILE)
    except OSError:
        return False
    return True


@tool(approval_mode="never_require")
def remember_fact(
    category: Annotated[str, "Categoría corta, por ejemplo preferencias o proyecto"],
    fact: Annotated[str, "Dato no sensible que el usuario ha pedido guardar explícitamente"],
) -> str:
    """Guarda un dato no sensible solo cuando el usuario pide explícitamente recordarlo."""
    category = category.strip()
    fact = fact.strip()
    if not category or not fact:
        return "No se guardó: la categoría y el dato son obligatorios."
    if len(category) > 80 or len(fact) > 1000:
        return "No se guardó: la categoría admite 80 caracteres y el dato 1000."
    memories = _read_memories()
    memory_id = uuid4().hex[:8]
    memories.append({
        "id": memory_id,
        "category": category,
        "fact": fact,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    })
    if not _write_memories(memories):
        return "No se pudo guardar la memoria en el archivo local."
    return "Dato guardado en memoria local con ID {}.".format(memory_id)


@tool(approval_mode="never_require")
def search_memory(
    query: Annotated[str, "Palabra o frase que buscar en la categoría o el dato guardado"],
) -> str:
    """Busca recuerdos locales por texto en su categoría o contenido."""
    query = query.strip().casefold()
    if not query:
        return "Escribe un término para buscar en la memoria."
    matches = [
        item for item in _read_memories()
        if query in item["category"].casefold() or query in item["fact"].casefold()
    ]
    if not matches:
        return "No encontré recuerdos que coincidan con esa búsqueda."
    return "\n".join(
        "[{}] {}: {}".format(item["id"], item["category"], item["fact"])
        for item in matches
    )


@tool(approval_mode="never_require")
def list_memories() -> str:
    """Lista los recuerdos guardados, con su identificador y categoría."""
    memories = _read_memories()
    if not memories:
        return "La memoria está vacía."
    return "\n".join(
        "[{}] {}: {}".format(item["id"], item["category"], item["fact"])
        for item in memories
    )


@tool(approval_mode="never_require")
def forget_memory(
    memory_id: Annotated[str, "ID exacto del recuerdo que se desea borrar"],
) -> str:
    """Borra un recuerdo por su ID exacto; no borra toda la memoria."""
    memory_id = memory_id.strip()
    if not memory_id:
        return "Indica el ID exacto del recuerdo que quieres borrar."
    memories = _read_memories()
    remaining = [item for item in memories if item["id"] != memory_id]
    if len(remaining) == len(memories):
        return "No se encontró ningún recuerdo con ese ID."
    if not _write_memories(remaining):
        return "No se pudo borrar el recuerdo del archivo local."
    return "Recuerdo {} eliminado de la memoria local.".format(memory_id)
