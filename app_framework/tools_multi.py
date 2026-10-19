"""Herramientas adicionales para el Agente 02 con Microsoft Agent Framework."""

import json
from datetime import datetime
from pathlib import Path
from typing import Annotated

from agent_framework import tool

NOTES_FILE = Path("data") / "notes.json"


@tool(approval_mode="never_require")
def current_datetime() -> str:
    """Devuelve la fecha, hora y zona horaria local del equipo."""
    now = datetime.now().astimezone()
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")


def _read_notes() -> list[dict[str, str]]:
    """Lee las notas guardadas; devuelve una lista vacía si aún no existe el archivo."""
    if not NOTES_FILE.exists():
        return []
    try:
        with NOTES_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if isinstance(data, list):
            return [
                note for note in data
                if isinstance(note, dict)
                and isinstance(note.get("title"), str)
                and isinstance(note.get("content"), str)
            ]
    except (OSError, json.JSONDecodeError):
        return []
    return []


@tool(approval_mode="never_require")
def save_note(
    title: Annotated[str, "Título breve de la nota"],
    content: Annotated[str, "Contenido que se desea guardar"],
) -> str:
    """Guarda una nota de texto en un archivo local del proyecto."""
    title = title.strip()
    content = content.strip()
    if not title or not content:
        return "No se ha guardado la nota: el título y el contenido son obligatorios."
    if len(title) > 120 or len(content) > 5000:
        return "No se ha guardado la nota: el título admite 120 caracteres y el contenido 5000."

    notes = _read_notes()
    notes.append({
        "title": title,
        "content": content,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    })
    try:
        NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with NOTES_FILE.open("w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False, indent=2)
    except OSError:
        return "No se pudo guardar la nota en el archivo local."
    return "Nota guardada correctamente: " + title


@tool(approval_mode="never_require")
def list_notes() -> str:
    """Devuelve los títulos de todas las notas guardadas localmente."""
    notes = _read_notes()
    if not notes:
        return "Todavía no hay notas guardadas."
    return "\n".join(
        "{}. {}".format(index, note["title"])
        for index, note in enumerate(notes, start=1)
    )


@tool(approval_mode="never_require")
def get_note(
    title: Annotated[str, "Título de la nota que se quiere recuperar"],
) -> str:
    """Busca una nota por su título y devuelve su contenido."""
    wanted = title.strip().casefold()
    for note in _read_notes():
        if note["title"].casefold() == wanted:
            return "Título: {}\nContenido: {}".format(
                note["title"], note["content"]
            )
    return "No se encontró una nota con ese título."
