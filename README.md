# AI Agents Learning 🤖

Repositorio práctico para aprender a construir agentes de IA desde cero.

## Roadmap

- [x] Proyecto 01 — Primer agente + calculadora (implementación manual)
- [x] Proyecto 01B — El mismo agente con Microsoft Agent Framework
- [x] Proyecto 02 — Agente con varias herramientas (código añadido; pendiente de prueba local)
- [x] Proyecto 03 — Memoria local persistente (código añadido; pendiente de prueba local)
- [x] Proyecto 04 — API meteorológica Open-Meteo (código añadido; pendiente de prueba local)
- [x] Proyecto 05 — Búsqueda en Wikipedia (código añadido; pendiente de prueba local)
- [x] Proyecto 06 — Planificación y coordinación de herramientas (código añadido; pendiente de prueba local)
- [x] Proyecto 07 — Sistema multiagente con router y coordinador (código añadido; pendiente de prueba local)\n- [x] Herramienta adicional — Agent Builder para crear esqueletos de nuevos agentes (código añadido; pendiente de prueba local)
- [ ] Proyecto 08 — MCP
- [ ] Proyecto 09 — Evaluación de agentes
- [ ] Proyecto final — Despliegue en producción

## Proyecto 01 — Agente manual con calculadora

Primer agente Python con un LLM y una herramienta de cálculo. La implementación manual permite estudiar el ciclo de tool calling paso a paso.

## Proyecto 01B — Microsoft Agent Framework

La segunda implementación permite comparar el control manual con las abstracciones del framework.

- Código: [`app_framework/`](app_framework/)
- Dependencias: [`requirements-framework.txt`](requirements-framework.txt)
- Guía: [`explicacion agentes.md`](explicacion%20agentes.md)
- Ejecutar: `python -m app_framework.agent`

## Proyecto 02 — Agente con varias herramientas

El agente combina estas herramientas:

- `calculate`: realiza operaciones matemáticas.
- `current_datetime`: consulta la fecha y hora local del equipo.
- `save_note`: guarda una nota en `data/notes.json`.
- `list_notes`: muestra los títulos guardados.
- `get_note`: recupera el contenido de una nota por título.

### Ejecutar

Desde la raíz del repositorio, activa el entorno virtual y ejecuta:

```powershell
python -m app_framework.agent_multi
```

Prueba, por ejemplo:

- `¿Cuánto es 125 * 8?`
- `¿Qué fecha y hora son ahora?`
- `Guarda una nota titulada Ideas con el contenido: probar un agente con varias herramientas.`
- `Lista mis notas.`
- `Recupera la nota Ideas.`

Las notas se almacenan en un archivo local dentro de `data/`. No guardes secretos ni información sensible en las notas.

### Pruebas

```powershell
python -m pytest
```

La API key de OpenAI debe estar en el archivo local `.env`, nunca en GitHub. El uso de la API puede tener costes separados de la suscripción de ChatGPT.


## Proyecto 03 — Memoria local persistente

El agente puede guardar, buscar, listar y borrar recuerdos cuando el usuario lo solicita explícitamente. Los datos se guardan localmente en `data/memory.json`; no se suben al repositorio.

### Ejecutar

```powershell
python -m app_framework.agent_memory
```

Pruebas manuales:
- `Recuerda que estoy aprendiendo Python`
- `¿Qué recuerdas sobre Python?`
- `Lista mis recuerdos`
- `Borra el recuerdo con ID <ID>`

La memoria no es una memoria automática de todas las conversaciones: el agente debe usar las herramientas. No guardes contraseñas, claves API ni datos personales sensibles.

## Proyecto 04 — API externa de meteorología

El agente consulta geocodificación y previsión meteorológica mediante Open-Meteo. No hace falta una clave de Open-Meteo, pero sí la clave de OpenAI configurada en `.env`.

### Ejecutar

```powershell
python -m app_framework.agent_weather
```

Ejemplo: `¿Qué tiempo hace en Granada, España?`

La herramienta consulta datos actuales y previsión diaria, establece un timeout y devuelve un mensaje de error si la API no está disponible. Los datos meteorológicos son orientativos y pueden cambiar.

## Pruebas de los proyectos 03 y 04

```powershell
python -m pytest
```


## Proyecto 05 — Búsqueda en Wikipedia

El agente busca artículos en Wikipedia en español mediante su API REST y devuelve títulos, descripciones, extractos y enlaces. Es un ejemplo de búsqueda externa acotada: no consulta toda Internet.

### Ejecutar

```powershell
python -m app_framework.agent_web_search
```

Ejemplos:
- `Investiga qué es la inteligencia artificial.`
- `Busca información sobre la arquitectura de computadores.`
- `Encuentra artículos sobre la historia de Granada.`

La herramienta no necesita una clave de Wikipedia. La aplicación sigue necesitando la clave de OpenAI en `.env`.

### Pruebas

```powershell
python -m pytest
```


## Proyecto 06 — Planificación y coordinación

Este agente recibe objetivos complejos, los divide en pasos y coordina herramientas de cálculo, fecha/hora, meteorología y búsqueda en Wikipedia. En esta versión, las herramientas son de consulta y cálculo: no envía mensajes ni modifica sistemas externos.

### Ejecutar

```powershell
python -m app_framework.agent_planner
```

Prueba:
- `Prepara un resumen con la fecha actual, el tiempo en Granada y dos datos sobre la historia de Granada.`
- `Calcula 125 * 8 y explica brevemente cómo has obtenido el resultado.`

El agente debe consultar las herramientas correspondientes y distinguir los datos confirmados de las explicaciones. La planificación la realiza el modelo mediante instrucciones; este ejemplo no es un motor de planificación formal ni garantiza un plan perfecto.


## Proyecto 07 — Sistema multiagente

La aplicación utiliza un router sencillo para seleccionar especialistas de matemáticas, fecha/hora, meteorología e investigación. Los especialistas seleccionados trabajan en paralelo y un agente coordinador sintetiza sus respuestas.

### Ejecutar

```powershell
python -m app_framework.agent_multiagent
```

Ejemplo:
`Investiga la historia de Granada, dime qué tiempo hace y calcula 125 * 8.`

El router usa reglas explícitas por palabras clave y expresiones matemáticas. Es una demostración didáctica, no un clasificador inteligente universal. Los agentes usan la API de OpenAI, por lo que las peticiones pueden generar costes.

### Pruebas

```powershell
python -m pytest
```


## Herramienta adicional — Agent Builder

Agent Builder crea una nueva carpeta con `agent.py`, `README.md` y `__init__.py` a partir del nombre, objetivo e instrucciones que introduzcas. Valida el nombre de la carpeta, comprueba que el código generado sea sintácticamente válido y no sobrescribe proyectos existentes.

### Ejecutar

```powershell
python -m app_framework.agent_builder
```

El generador crea esqueletos sin herramientas personalizadas; puedes ampliarlos después. Configura la clave de OpenAI en el `.env` local. Los proyectos generados son código fuente y no se ejecutan automáticamente al crearlos.

### Pruebas

```powershell
python -m pytest
```
