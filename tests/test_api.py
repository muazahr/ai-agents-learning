from fastapi.testclient import TestClient

from app_framework import api


client = TestClient(api.app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_rejects_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = client.post("/v1/chat", json={"message": "Hola"})
    assert response.status_code == 503


def test_chat_rejects_empty_message():
    response = client.post("/v1/chat", json={"message": ""})
    assert response.status_code == 422
