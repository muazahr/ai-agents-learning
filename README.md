# AI Agents Learning 🤖

Repositorio práctico para aprender a construir agentes de IA desde cero.

## Proyecto 01 — Primer agente con herramientas

Primer proyecto del itinerario: un agente en Python que puede decidir cuándo utilizar una herramienta de cálculo y usar el resultado para responder al usuario.

### Conceptos

- LLM
- Prompt
- Herramientas
- Tool calling
- Contexto
- Ejecución de acciones

### Roadmap

- [x] Proyecto 01 — Primer agente + calculadora
- [x] Comparativa — agente manual frente a Microsoft Agent Framework
- [ ] Proyecto 02 — Agente con varias herramientas
- [ ] Proyecto 03 — Memoria
- [ ] Proyecto 04 — APIs externas
- [ ] Proyecto 05 — Búsqueda web
- [ ] Proyecto 06 — Agente multi-herramienta

## Proyecto 01B — El mismo agente con un framework

Hemos añadido una segunda implementación usando **Microsoft Agent Framework** para comparar el control manual del primer agente con las abstracciones de un framework.

- Código: [`app_framework/`](app_framework/)
- Dependencias: [`requirements-framework.txt`](requirements-framework.txt)
- Guía detallada: [`explicacion agentes.md`](explicacion%20agentes.md)

### Preparación

1. Crea/activa tu entorno virtual.
2. Instala `pip install -r requirements-framework.txt`.
3. Copia `.env.framework.example` a `.env` y configura `OPENAI_API_KEY`.
4. Ejecuta `python -m app_framework.agent`.

La API key no debe guardarse ni subirse a GitHub. Esta versión usa una API key de OpenAI; no requiere Azure para este ejemplo.
