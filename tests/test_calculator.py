from app.tools.calculator import calculate


def test_addition():
    assert calculate("2 + 3") == "5"


def test_multiplication():
    assert calculate("10 * 4") == "40"


def test_division():
    assert calculate("10 / 2") == "5.0"


def test_invalid_expression():
    assert calculate("import os") == "Expresión no válida."
