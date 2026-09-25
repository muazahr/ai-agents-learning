"""Herramientas disponibles para el agente."""


def calculate(expression: str) -> str:
    allowed = set("0123456789+-*/(). %")
    if not expression or any(char not in allowed for char in expression):
        return "Expresión no válida."
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except (ArithmeticError, SyntaxError, TypeError, ZeroDivisionError):
        return "No se pudo calcular la expresión."
