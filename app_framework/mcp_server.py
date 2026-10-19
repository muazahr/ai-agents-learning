"""Servidor MCP local con herramientas pequeñas para el proyecto educativo.

Se ejecuta como subproceso del cliente MCP. No imprime mensajes propios a stdout,
porque ese canal se utiliza para el protocolo JSON-RPC de stdio.
"""

from datetime import datetime
import ast
import operator
import math

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ai-agents-learning-tools")

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _calculate(expression: str) -> float | int:
    """Evalúa una expresión aritmética limitada, sin ejecutar código Python arbitrario."""
    if not expression or len(expression) > 120:
        raise ValueError("La expresión debe tener entre 1 y 120 caracteres.")
    tree = ast.parse(expression, mode="eval")

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if abs(node.value) > 1e12:
                raise ValueError("El número es demasiado grande.")
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 8:
                raise ValueError("El exponente debe estar entre -8 y 8.")
            result = _ALLOWED_OPERATORS[type(node.op)](left, right)
            if isinstance(result, (int, float)) and (not math.isfinite(result) or abs(result) > 1e15):
                raise ValueError("El resultado está fuera del límite permitido.")
            return result
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[type(node.op)](visit(node.operand))
        raise ValueError("La expresión contiene una operación no permitida.")

    return visit(tree)


@mcp.tool()
def calculate(expression: str) -> str:
    """Calcula una expresión aritmética sencilla como 25 * 18 o (8 + 2) / 5."""
    try:
        return str(_calculate(expression))
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError) as exc:
        return "No se pudo calcular la expresión: {}".format(str(exc))


@mcp.tool()
def current_datetime() -> str:
    """Devuelve la fecha y hora local del equipo que ejecuta el servidor MCP."""
    return datetime.now().astimezone().isoformat(timespec="seconds")


@mcp.tool()
def text_statistics(text: str) -> str:
    """Cuenta caracteres, palabras y líneas en un texto proporcionado por el usuario."""
    if len(text) > 20000:
        return "El texto supera el límite de 20000 caracteres."
    lines = len(text.splitlines()) if text else 0
    words = len(text.split())
    return "Caracteres: {}\nPalabras: {}\nLíneas: {}".format(len(text), words, lines)


if __name__ == "__main__":
    mcp.run(transport="stdio")
