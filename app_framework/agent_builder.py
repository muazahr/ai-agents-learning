"""Agent Builder: generador local de esqueletos de agentes Python seguros por plantilla."""

import re
import shutil
import unicodedata
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

GENERATED_DIR = Path(__file__).resolve().parents[1] / "generated_agents"
MAX_NAME_LENGTH = 80
MAX_PURPOSE_LENGTH = 500
MAX_INSTRUCTIONS_LENGTH = 2000


def slugify(name: str) -> str:
    """Convierte un nombre en un identificador de carpeta sin rutas ni caracteres especiales."""
    if not isinstance(name, str):
        raise ValueError("El nombre debe ser texto.")
    normalized = unicodedata.normalize("NFKD", name)
    ascii_name = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name).strip("-")
    slug = slug[:60].strip("-")
    if not slug:
        raise ValueError("El nombre debe incluir letras o números.")
    return slug


def _render_agent(name: str, purpose: str, instructions: str) -> str:
    """Genera código a partir de valores de texto, usando repr para escapar literales."""
    return '''"""Agente generado por Agent Builder."""

import asyncio
import os

from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

load_dotenv()

AGENT_NAME = {agent_name}
AGENT_PURPOSE = {purpose}
AGENT_INSTRUCTIONS = {instructions}


def build_agent() -> Agent:
    """Construye el agente generado."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY. Configúrala en tu archivo .env.")

    model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")
    client = OpenAIChatClient(model=model, api_key=api_key)
    return Agent(
        client=client,
        name=AGENT_NAME,
        instructions=AGENT_INSTRUCTIONS,
        tools=[],
    )


async def run_agent(user_message: str) -> str:
    """Ejecuta una petición y devuelve la respuesta."""
    response = await build_agent().run(user_message)
    return response.text


async def main() -> None:
    print("Agente generado: " + AGENT_NAME)
    print("Objetivo: " + AGENT_PURPOSE)
    print("Escribe 'salir' para terminar.\\n")
    while True:
        message = input("Tú: ").strip()
        if message.lower() in {{"salir", "exit", "quit"}}:
            print("Agente: ¡Hasta luego!")
            return
        if not message:
            continue
        try:
            print("Agente: {{}}\\n".format(await run_agent(message)))
        except Exception as exc:
            print("Error: {{}}\\n".format(exc))


if __name__ == "__main__":
    asyncio.run(main())
'''.format(
        agent_name=repr(name),
        purpose=repr(purpose),
        instructions=repr(instructions),
    )


def create_agent_project(name: str, purpose: str, instructions: str = "") -> Path:
    """Crea un nuevo proyecto sin sobrescribir nada que ya exista."""
    name = name.strip()
    purpose = purpose.strip()
    instructions = instructions.strip() or (
        "Eres un asistente especializado en: {}. Responde en español, "
        "sé claro y reconoce cuando no sabes algo.".format(purpose)
    )

    if not name or len(name) > MAX_NAME_LENGTH:
        raise ValueError("El nombre es obligatorio y admite hasta 80 caracteres.")
    if not purpose or len(purpose) > MAX_PURPOSE_LENGTH:
        raise ValueError("El objetivo es obligatorio y admite hasta 500 caracteres.")
    if len(instructions) > MAX_INSTRUCTIONS_LENGTH:
        raise ValueError("Las instrucciones admiten hasta 2000 caracteres.")

    slug = slugify(name)
    base = GENERATED_DIR.resolve()
    target = (base / slug).resolve()
    if not target.is_relative_to(base):
        raise ValueError("La ruta generada no es válida.")
    if target.exists():
        raise FileExistsError("Ya existe un proyecto con ese nombre: {}".format(target))

    agent_source = _render_agent(name, purpose, instructions)
    compile(agent_source, str(target / "agent.py"), "exec")

    target.mkdir(parents=True, exist_ok=False)
    try:
        (target / "__init__.py").write_text('"""Agente generado."""\n', encoding="utf-8")
        (target / "agent.py").write_text(agent_source, encoding="utf-8")
        (target / "README.md").write_text(
            "# {}\n\n".format(name)
            + "Objetivo: {}\n\n".format(purpose)
            + "## Ejecutar\n\n"
            + "Desde la raíz del repositorio, con el entorno virtual activado:\n\n"
            + "```powershell\n"
            + "python -m generated_agents.{}.agent\n".format(slug)
            + "```\n\n"
            + "Este esqueleto no incluye herramientas personalizadas. "
            + "Amplía `tools=[]` en `agent.py` cuando añadas herramientas. "
            + "Configura `OPENAI_API_KEY` en el archivo `.env` local y no la subas a GitHub.\n",
            encoding="utf-8",
        )
    except OSError:
        shutil.rmtree(target, ignore_errors=True)
        raise
    return target


def main() -> None:
    print("🧰 Agent Builder — generador de esqueletos de agentes")
    name = input("Nombre del nuevo agente: ").strip()
    purpose = input("¿Qué problema resolverá?: ").strip()
    instructions = input("Instrucciones (opcional; pulsa Enter para usar las predeterminadas): ").strip()
    try:
        path = create_agent_project(name, purpose, instructions)
        slug = path.name
        print("\nProyecto creado en: {}".format(path))
        print("Ejecútalo con: python -m generated_agents.{}.agent".format(slug))
        print("No se han sobrescrito archivos existentes.")
    except (ValueError, FileExistsError, OSError) as exc:
        print("No se pudo crear el proyecto: {}".format(exc))


if __name__ == "__main__":
    main()
