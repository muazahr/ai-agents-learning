from app_framework import memory_tools


def test_remember_list_search_and_forget(tmp_path, monkeypatch):
    monkeypatch.setattr(memory_tools, "MEMORY_FILE", tmp_path / "memory.json")

    saved = memory_tools.remember_fact("proyecto", "Estoy aprendiendo agentes de IA")
    assert "ID" in saved

    listed = memory_tools.list_memories()
    assert "Estoy aprendiendo agentes de IA" in listed

    found = memory_tools.search_memory("agentes de IA")
    assert "proyecto" in found

    memory_id = listed.split("]", 1)[0].removeprefix("[")
    deleted = memory_tools.forget_memory(memory_id)
    assert "eliminado" in deleted
    assert memory_tools.list_memories() == "La memoria está vacía."


def test_memory_requires_category_and_fact(tmp_path, monkeypatch):
    monkeypatch.setattr(memory_tools, "MEMORY_FILE", tmp_path / "memory.json")
    result = memory_tools.remember_fact("", "dato")
    assert "obligatorios" in result


def test_search_memory_returns_empty_message(tmp_path, monkeypatch):
    monkeypatch.setattr(memory_tools, "MEMORY_FILE", tmp_path / "memory.json")
    assert "No encontré" in memory_tools.search_memory("inexistente")
