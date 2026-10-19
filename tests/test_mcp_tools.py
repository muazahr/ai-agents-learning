from app_framework.mcp_server import _calculate, current_datetime, text_statistics


def test_mcp_calculator_handles_arithmetic():
    assert _calculate("25 * 18") == 450
    assert _calculate("(8 + 2) / 5") == 2


def test_mcp_calculator_rejects_python_expressions():
    try:
        _calculate("__import__('os').system('echo unsafe')")
    except ValueError:
        pass
    else:
        raise AssertionError("La expresión no permitida debería rechazarse")


def test_mcp_datetime_returns_text():
    assert isinstance(current_datetime(), str)
    assert current_datetime()


def test_text_statistics():
    result = text_statistics("hola mundo\nsegunda línea")
    assert "Palabras: 4" in result
    assert "Líneas: 2" in result
