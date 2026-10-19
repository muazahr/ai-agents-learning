from app_framework.tools import calculate


def test_framework_calculator_addition():
    assert calculate("2 + 3") == "5"


def test_framework_calculator_multiplication():
    assert calculate("10 * 4") == "40"


def test_framework_calculator_rejects_invalid_input():
    assert calculate("import os") == "Expresión no válida."
