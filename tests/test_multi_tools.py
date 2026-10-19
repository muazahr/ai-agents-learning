from app_framework import tools_multi


def test_save_list_and_retrieve_note(tmp_path, monkeypatch):
    monkeypatch.setattr(tools_multi, "NOTES_FILE", tmp_path / "notes.json")

    saved = tools_multi.save_note("Plan", "Estudiar agentes")
    assert "guardada correctamente" in saved

    listed = tools_multi.list_notes()
    assert "Plan" in listed

    retrieved = tools_multi.get_note("Plan")
    assert "Estudiar agentes" in retrieved


def test_list_notes_when_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(tools_multi, "NOTES_FILE", tmp_path / "notes.json")
    assert tools_multi.list_notes() == "Todavía no hay notas guardadas."


def test_save_note_requires_title_and_content(tmp_path, monkeypatch):
    monkeypatch.setattr(tools_multi, "NOTES_FILE", tmp_path / "notes.json")
    result = tools_multi.save_note("", "Contenido")
    assert "obligatorios" in result
