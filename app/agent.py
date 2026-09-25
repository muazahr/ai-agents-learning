"""Lógica principal del agente."""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.tools.calculator import calculate

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

TOOLS = [{
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Calcula una expresión matemática básica.",
        "parameters": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"]
        }
    }
}]


def run_agent(user_message: str) -> str:
    messages = [
        {"role": "system", "content": "Eres un agente de IA educativo. Responde en español. Cuando necesites hacer un cálculo, utiliza calculate."},
        {"role": "user", "content": user_message}
    ]
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS, tool_choice="auto")
    assistant = response.choices[0].message
    messages.append(assistant)
    if not assistant.tool_calls:
        return assistant.content or ""
    for call in assistant.tool_calls:
        if call.function.name == "calculate":
            args = json.loads(call.function.arguments)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": calculate(args["expression"])})
    final = client.chat.completions.create(model=MODEL, messages=messages)
    return final.choices[0].message.content or ""
