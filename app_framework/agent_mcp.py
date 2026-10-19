"""Agente 08: cliente MCP que descubre y ejecuta herramientas de un servidor local."""

import asyncio
import json
import os
import sys
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

SYSTEM_PROMPT = (
    "Eres un asistente educativo y respondes en español. Puedes utilizar herramientas "
    "publicadas por un servidor MCP. Usa las herramientas cuando aporten datos útiles. "
    "No inventes resultados: basa tus respuestas en la salida real de las herramientas."
)


def _openai_tool_schema(tool: Any) -> dict[str, Any]:
    """Convierte la definición MCP de una herramienta al formato function calling."""
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "Herramienta proporcionada por MCP.",
            "parameters": tool.inputSchema or {"type": "object", "properties": {}},
        },
    }


def _tool_result_text(result: Any) -> str:
    """Extrae texto del resultado MCP sin asumir que siempre exista contenido."""
    parts = []
    for item in getattr(result, "content", []) or []:
        text = getattr(item, "text", None)
        if text:
            parts.append(text)
    if getattr(result, "isError", False):
        return "La herramienta MCP informó de un error: " + (" ".join(parts) or "sin detalle")
    return "\n".join(parts) or "La herramienta no devolvió texto."


async def run_agent(user_message: str) -> str:
    """Conecta al servidor MCP, descubre herramientas y responde a una petición."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY. Configúrala en el archivo .env.")
    if not user_message.strip():
        raise ValueError("Escribe una pregunta.")
    if len(user_message) > 10000:
        raise ValueError("El mensaje supera el límite de 10000 caracteres.")

    model = os.getenv("OPENAI_MODEL", os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini"))
    client = OpenAI(api_key=api_key)
    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app_framework.mcp_server"],
    )

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            mcp_tools = (await session.list_tools()).tools
            schemas = [_openai_tool_schema(item) for item in mcp_tools]
            messages: list[dict[str, Any]] = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ]

            for _ in range(6):
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=schemas or None,
                    tool_choice="auto" if schemas else "none",
                )
                assistant = response.choices[0].message
                if not assistant.tool_calls:
                    return assistant.content or "El modelo no devolvió texto."
                messages.append({
                    "role": "assistant",
                    "content": assistant.content,
                    "tool_calls": [
                        {
                            "id": call.id,
                            "type": "function",
                            "function": {
                                "name": call.function.name,
                                "arguments": call.function.arguments,
                            },
                        }
                        for call in assistant.tool_calls
                    ],
                })

                for call in assistant.tool_calls:
                    name = call.function.name
                    available_names = {item.name for item in mcp_tools}
                    if name not in available_names:
                        result_text = "Herramienta no disponible en el servidor MCP."
                    else:
                        try:
                            arguments = json.loads(call.function.arguments or "{}")
                            result = await session.call_tool(name, arguments=arguments)
                            result_text = _tool_result_text(result)
                        except (json.JSONDecodeError, ValueError, TypeError) as exc:
                            result_text = "No se pudo procesar la llamada a la herramienta: {}".format(type(exc).__name__)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": result_text,
                    })

            return "He alcanzado el límite de llamadas a herramientas para esta petición."


async def main() -> None:
    print("🔌 Agente 08 — Agente conectado a herramientas MCP")
    print("Herramientas MCP: calculadora segura, fecha/hora y estadísticas de texto.")
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
