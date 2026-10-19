"""Herramientas del agente construido con Microsoft Agent Framework."""

from typing import Annotated
from agent_framework import tool


@tool(approval_mode="never_require")
def calculate(
    expression: Annotated[str, "Expresión matemática básica, por ejemplo 25 * 18"],
) -> str:
    """Calcula una expresión matemática básica usando números y operadores aritméticos."""
    allowed = set("0123456789+-*/(). %")
    if not expression or any(char not in allowed for char in expression):
        return "Expresión no válida."
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except (ArithmeticError, SyntaxError, TypeError, ValueError):
        return "No se pudo calcular la expresión."
