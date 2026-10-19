from pathlib import Path

import pytest

from app_framework import agent_builder


def test_slugify_normalizes_name():
    assert agent_builder.slugify("Mi Agente: Prueba") == "mi-agente-prueba"


def test_create_agent_project_writes_valid_files(tmp_path, monkeypatch):
    monkeypatch.setattr(agent_builder, "GENERATED_DIR", tmp_path)
    target = agent_builder.create_agent_project(
        "Agente de prueba",
        "Ayudar con pruebas",
        "Responde con claridad en español.",
    )

    assert target == tmp_path / "agente-de-prueba"
    assert (target / "agent.py").exists()
    assert (target / "README.md").exists()
    source = (target / "agent.py").read_text(encoding="utf-8")
    compile(source, str(target / "agent.py"), "exec")
    assert "Ayudar con pruebas" in (target / "README.md").read_text(encoding="utf-8")


def test_builder_does_not_overwrite_existing_project(tmp_path, monkeypatch):
    monkeypatch.setattr(agent_builder, "GENERATED_DIR", tmp_path)
    target = agent_builder.create_agent_project("Mi agente", "Primer objetivo")
    marker = target / "marker.txt"
    marker.write_text("no modificar", encoding="utf-8")

    with pytest.raises(FileExistsError):
        agent_builder.create_agent_project("Mi agente", "Otro objetivo")

    assert marker.read_text(encoding="utf-8") == "no modificar"


def test_builder_rejects_invalid_name(tmp_path, monkeypatch):
    monkeypatch.setattr(agent_builder, "GENERATED_DIR", tmp_path)
    with pytest.raises(ValueError):
        agent_builder.create_agent_project("../", "Objetivo")
