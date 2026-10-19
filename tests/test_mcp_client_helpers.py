from types import SimpleNamespace

from app_framework.agent_mcp import _openai_tool_schema, _tool_result_text


def test_mcp_schema_is_converted_to_openai_function():
    tool = SimpleNamespace(
        name="calculate",
        description="Calcula",
        inputSchema={"type": "object", "properties": {"expression": {"type": "string"}}},
    )
    schema = _openai_tool_schema(tool)
    assert schema["function"]["name"] == "calculate"
    assert schema["function"]["parameters"]["properties"]["expression"]["type"] == "string"


def test_mcp_result_extracts_text():
    result = SimpleNamespace(
        content=[SimpleNamespace(text="450"), SimpleNamespace(text="hecho")],
        isError=False,
    )
    assert _tool_result_text(result) == "450\nhecho"
