"""API HTTP mínima para exponer el agente planificador en un servicio web."""

import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app_framework.agent_planner import run_agent

load_dotenv()

app = FastAPI(
    title="AI Agents Learning API",
    description="API educativa para probar el agente planificador del repositorio.",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000, description="Mensaje para el agente")


class ChatResponse(BaseModel):
    response: str


@app.get("/health")
async def health() -> dict[str, str]:
    """Comprueba que el proceso HTTP está disponible; no valida proveedores externos."""
    return {"status": "ok"}


@app.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Envía un mensaje al agente planificador y devuelve su respuesta."""
    if not os.environ.get("OPENAI_API_KEY"):
        raise HTTPException(status_code=503, detail="El servicio no tiene OPENAI_API_KEY configurada.")
    try:
        answer = await run_agent(request.message.strip())
        return ChatResponse(response=answer)
    except Exception:
        # No se devuelven detalles internos ni secretos al cliente HTTP.
        raise HTTPException(status_code=502, detail="El agente no pudo completar la petición.")
