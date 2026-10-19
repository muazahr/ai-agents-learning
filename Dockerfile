FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements-framework.txt requirements-framework.txt
COPY requirements-production.txt requirements-production.txt
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements-production.txt

COPY app_framework app_framework
COPY app app
COPY tests tests
COPY README.md README.md
COPY "explicacion agentes.md" "explicacion agentes.md"

RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && mkdir -p /app/data \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app_framework.api:app", "--host", "0.0.0.0", "--port", "8000"]
