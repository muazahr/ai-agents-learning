from app_framework.agent_multiagent import route_request


def test_route_selects_weather_and_research():
    route = route_request("Investiga la historia de Granada y dime qué tiempo hace")
    assert "weather" in route
    assert "research" in route


def test_route_selects_math_and_datetime():
    route = route_request("¿Cuánto es 25 * 18 y qué hora es ahora?")
    assert "math" in route
    assert "datetime" in route


def test_route_defaults_to_research():
    assert route_request("Háblame de un tema") == ["research"]
