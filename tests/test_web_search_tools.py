from app_framework import web_search_tools


def test_search_wikipedia_requires_query():
    assert "entre 1 y 200" in web_search_tools.search_wikipedia(" ")


def test_search_wikipedia_formats_results(monkeypatch):
    monkeypatch.setattr(
        web_search_tools,
        "_fetch_json",
        lambda url: {
            "pages": [{
                "title": "Inteligencia artificial",
                "description": "Campo de la informática",
                "excerpt": "La <span>inteligencia artificial</span> estudia sistemas.",
                "key": "Inteligencia_artificial",
            }]
        },
    )
    result = web_search_tools.search_wikipedia("inteligencia artificial")
    assert "Inteligencia artificial" in result
    assert "Campo de la informática" in result
    assert "<span>" not in result
    assert "https://es.wikipedia.org/wiki/Inteligencia_artificial" in result


def test_search_wikipedia_handles_no_results(monkeypatch):
    monkeypatch.setattr(web_search_tools, "_fetch_json", lambda url: {"pages": []})
    assert "no devolvió resultados" in web_search_tools.search_wikipedia("tema inexistente")
