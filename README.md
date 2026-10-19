# AI Agents Learning

Un repositorio para aprender a construir agentes de inteligencia artificial con Python, desde una primera llamada a un modelo hasta una API que se puede ejecutar en un contenedor.

La idea de este proyecto es aprender haciendo. Cada ejemplo añade una pieza concreta y reutiliza lo que ya funciona: primero una herramienta sencilla, después varias herramientas, memoria, servicios externos, coordinación entre agentes y, por último, una interfaz HTTP para poder integrar el agente en otra aplicación.

No hace falta dominar todos los conceptos antes de empezar. Lo recomendable es ejecutar los ejemplos en orden, cambiar las instrucciones, probar preguntas distintas y leer el código para entender qué ocurre.

## Índice

- [Qué vas a construir](#qué-vas-a-construir)
- [Requisitos](#requisitos)
- [Preparar el proyecto en Windows](#preparar-el-proyecto-en-windows)
- [Configurar la API de OpenAI](#configurar-la-api-de-openai)
- [Proyectos, en orden](#proyectos-en-orden)
- [Ejecutar las pruebas](#ejecutar-las-pruebas)
- [Levantar la API con Docker](#levantar-la-api-con-docker)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Costes, privacidad y seguridad](#costes-privacidad-y-seguridad)
- [Cómo seguir aprendiendo](#cómo-seguir-aprendiendo)

## Qué vas a construir

Al terminar el recorrido tendrás ejemplos independientes que muestran distintas formas de diseñar un agente:

- un agente que decide cuándo llamar a una calculadora;
- un ejemplo equivalente con Microsoft Agent Framework;
- un asistente que combina varias herramientas;
- memoria local que se puede consultar y borrar;
- consultas a una API meteorológica y búsqueda en Wikipedia;
- planificación de tareas y coordinación de especialistas;
- un generador de esqueletos de agentes;
- un servidor y un cliente que se comunican mediante MCP;
- una evaluación reproducible para comprobar parte del comportamiento;
- una API HTTP empaquetada con Docker.

Los proyectos son didácticos. Que el código exista no significa que cada ejemplo haya sido ejecutado en todos los sistemas operativos o con todas las versiones de sus dependencias. La integración continua ejecuta las pruebas automáticas cuando se suben cambios; las llamadas reales a modelos y servicios externos requieren configuración y conectividad.

## Requisitos

- Python 3.11 o posterior.
- GitHub y Git (opcionales si descargas el repositorio como ZIP).
- Visual Studio Code u otro editor.
- Una clave de API de OpenAI para ejecutar los agentes que llaman a un modelo.
- Docker Desktop solo para el último proyecto.

El modelo predeterminado es `gpt-4.1-mini`. Puedes cambiarlo con una variable de entorno si tu cuenta tiene acceso a otro modelo compatible.

## Preparar el proyecto en Windows

### 1. Descargar el repositorio

Descarga el ZIP desde GitHub y extrae su contenido. Abre en VS Code la carpeta que contiene directamente `README.md`, `requirements.txt` y las carpetas `app`, `app_framework` y `tests`.

Si al ejecutar `dir` solo ves otra carpeta llamada `ai-agents-learning-main`, entra en ella:

```powershell
cd .\ai-agents-learning-main
dir
```

### 2. Crear y activar un entorno virtual

Desde la raíz del repositorio:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Cuando el entorno esté activo, normalmente verás `(.venv)` al principio de la línea de PowerShell. Si Windows bloquea la ejecución del script de activación, revisa el mensaje de error antes de cambiar la política del sistema; también puedes activar el entorno desde una terminal compatible.

### 3. Instalar las dependencias

Para los primeros ejemplos:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-framework.txt
```

Para instalar también las dependencias de la API web y del despliegue:

```powershell
python -m pip install -r requirements-production.txt
```

## Configurar la API de OpenAI

Crea un archivo local llamado `.env` en la raíz del proyecto. Puedes copiar la plantilla si está disponible:

```powershell
Copy-Item .env.framework.example .env
```

Abre `.env` y configura las variables necesarias:

```dotenv
OPENAI_API_KEY=tu_clave_api_real
OPENAI_CHAT_MODEL=gpt-4.1-mini
OPENAI_MODEL=gpt-4.1-mini
```

No pongas comillas alrededor de la clave. Si solo usas la implementación manual del Proyecto 01, también puedes revisar las variables de `.env.example`.

**La clave API es un secreto.** No la pegues en una incidencia, captura de pantalla, commit, README ni mensaje público. El archivo `.env` está excluido de Git mediante `.gitignore`. La suscripción de ChatGPT y el uso de la API se gestionan por separado; las llamadas a la API pueden generar cargos según tu cuenta y el modelo elegido.

## Proyectos, en orden

Los comandos se ejecutan desde la raíz del repositorio, con el entorno virtual activado. Los agentes de consola terminan cuando escribes `salir`.

### Proyecto 01 — Primer agente y calculadora

**Qué aprende:** el ciclo básico de una llamada a un modelo y una herramienta.

```powershell
python -m app.main
```

Prueba: `¿Cuánto es 25 * 18?`

La aplicación declara una herramienta, permite que el modelo solicite su ejecución, ejecuta el cálculo en Python y devuelve el resultado al modelo para que redacte la respuesta final. Es una implementación manual para que el flujo sea visible.

### Proyecto 01B — El mismo agente con Microsoft Agent Framework

```powershell
python -m app_framework.agent
```

Prueba la misma operación. Compara `app/agent.py` con `app_framework/agent.py`: el framework aporta abstracciones para declarar el agente y registrar herramientas, de modo que hay menos código dedicado a coordinar cada llamada.

### Proyecto 02 — Varias herramientas

```powershell
python -m app_framework.agent_multi
```

Incluye calculadora, fecha y hora local, y notas guardadas en `data/notes.json`. Prueba a guardar una nota, listar sus títulos y recuperar su contenido. El archivo se queda en tu equipo.

### Proyecto 03 — Memoria local persistente

```powershell
python -m app_framework.agent_memory
```

La memoria no aparece mágicamente: el agente tiene herramientas para guardar, buscar, listar y borrar recuerdos en `data/memory.json`. Pídele explícitamente que recuerde un dato de prueba y luego pregúntale por él. Evita guardar contraseñas, claves o información personal sensible.

### Proyecto 04 — Consulta meteorológica

```powershell
python -m app_framework.agent_weather
```

La herramienta consulta Open-Meteo para obtener la ubicación y el tiempo. Ejemplo: `¿Qué tiempo hace en Granada, España?` No requiere una clave de Open-Meteo, pero sí requiere Internet y la clave de OpenAI para la respuesta del agente. La previsión puede cambiar y no debe tratarse como una fuente de emergencia.

### Proyecto 05 — Búsqueda en Wikipedia

```powershell
python -m app_framework.agent_web_search
```

Busca páginas de Wikipedia en español y devuelve títulos, extractos y enlaces. Es una búsqueda limitada a esa fuente, no un buscador de toda Internet. Prueba: `Investiga qué es la inteligencia artificial.`

### Proyecto 06 — Planificación y coordinación de herramientas

```powershell
python -m app_framework.agent_planner
```

El agente puede combinar cálculos, fecha/hora, meteorología y búsqueda para responder a peticiones que necesitan varios pasos. Prueba: `Prepara un resumen con la fecha actual, el tiempo en Granada y dos datos sobre la historia de Granada.`

La planificación se guía mediante instrucciones al modelo; no es un planificador formal y no garantiza que cada plan sea perfecto. En esta versión las herramientas se limitan a consultas y cálculos.

### Proyecto 07 — Sistema multiagente

```powershell
python -m app_framework.agent_multiagent
```

Un router selecciona especialistas para matemáticas, fecha/hora, meteorología e investigación. Cuando se seleccionan varios, se ejecutan en paralelo y un coordinador reúne sus resultados.

Prueba: `Investiga la historia de Granada, dime qué tiempo hace y calcula 125 * 8.`

El router usa reglas y palabras clave para que sea fácil de inspeccionar. Puede fallar con frases inesperadas; precisamente por eso se incluye una evaluación básica en un proyecto posterior.

### Herramienta adicional — Agent Builder

```powershell
python -m app_framework.agent_builder
```

Responde a las preguntas sobre el nombre, el objetivo y las instrucciones de un agente. El generador crea una carpeta en `generated_agents/` con el código inicial y un README propio. Es un generador por plantillas: no ejecuta automáticamente el código nuevo ni lo publica en Internet. Tampoco sobrescribe una carpeta existente.

### Proyecto 08 — Herramientas con MCP

Primero puedes inspeccionar el servidor:

```powershell
python -m app_framework.mcp_server
```

El servidor MCP usa el transporte `stdio`; es un proceso que espera mensajes del cliente, así que puede parecer que la terminal no muestra nada. Detén esa ejecución con Ctrl+C y después lanza el agente cliente:

```powershell
python -m app_framework.agent_mcp
```

El cliente descubre las herramientas que publica el servidor y las adapta al formato de llamadas a funciones del modelo. El servidor ofrece una calculadora limitada, fecha/hora y estadísticas de texto. MCP permite separar el agente de las herramientas y facilita que otros clientes compatibles puedan reutilizarlas.

### Proyecto 09 — Evaluación básica

```powershell
python -m app_framework.evaluation
```

Este comando ejecuta casos conocidos contra el router multiagente y muestra cuántos pasan. No necesita una llamada al modelo, por lo que el resultado es rápido y reproducible. Es una primera evaluación de una pieza concreta del sistema, no una medida completa de la calidad de las respuestas generadas por un LLM.

### Proyecto final — API HTTP y Docker

Instala las dependencias de producción:

```powershell
python -m pip install -r requirements-production.txt
```

Inicia la API directamente:

```powershell
uvicorn app_framework.api:app --host 127.0.0.1 --port 8000
```

Abre [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) para comprobar que el servicio está activo y [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para explorar la documentación interactiva. Envía un POST a `/v1/chat` con un cuerpo JSON como:

```json
{
  "message": "Calcula 125 * 8 y explica el resultado."
}
```

Si tienes Docker Desktop instalado y el archivo `.env` configurado, también puedes construir y levantar el contenedor:

```powershell
docker compose up --build
```

La API escucha en el puerto 8000. Este contenedor es una base de despliegue para aprendizaje, no una solución lista para exponer públicamente sin más trabajo. Antes de publicarlo, añade autenticación, límites de uso, control de costes, monitorización, gestión de secretos y políticas de acceso adecuadas.

## Ejecutar las pruebas

Para ejecutar todas las pruebas locales:

```powershell
python -m pytest -q
```

Para evaluar específicamente el router:

```powershell
python -m app_framework.evaluation
```

Las pruebas unitarias deben poder comprobar la lógica sin gastar dinero en llamadas al modelo. Las pruebas de integración con proveedores externos pueden depender de la red, credenciales y límites de servicio; no se deben confundir con una evaluación de calidad real del agente.

GitHub Actions ejecuta las pruebas al subir cambios o abrir una solicitud de cambios. Puedes consultar el resultado en la pestaña **Actions** del repositorio.

## Estructura del repositorio

```text
app/
  agent.py                 # Tool calling manual
  main.py                  # Consola del primer agente
  tools/calculator.py      # Calculadora del agente manual
app_framework/
  agent.py                 # Proyecto 01B
  agent_multi.py           # Proyecto 02
  agent_memory.py          # Proyecto 03
  agent_weather.py         # Proyecto 04
  agent_web_search.py      # Proyecto 05
  agent_planner.py         # Proyecto 06
  agent_multiagent.py      # Proyecto 07
  agent_builder.py         # Generador de proyectos
  mcp_server.py            # Servidor MCP del Proyecto 08
  agent_mcp.py             # Cliente MCP del Proyecto 08
  evaluation.py            # Evaluación reproducible del Proyecto 09
  api.py                   # API HTTP del proyecto final
tests/                     # Pruebas automáticas
data/                      # Datos locales ignorados por Git
generated_agents/          # Proyectos creados por Agent Builder
Dockerfile                 # Imagen del servicio HTTP
docker-compose.yml         # Ejecución local con Docker
requirements*.txt          # Dependencias separadas por uso
explicacion agentes.md     # Guía conceptual en español
```

## Costes, privacidad y seguridad

- Las llamadas al modelo pueden tener coste. Empieza con pruebas pequeñas y revisa el uso en tu cuenta de API.
- Nunca subas `.env`, claves, tokens o archivos con datos privados.
- Los archivos locales de memoria y notas están excluidos de Git, pero siguen existiendo en tu ordenador.
- El agente debe usar herramientas solo cuando sea necesario y explicar cuando una consulta falla.
- Las herramientas de ejemplo son deliberadamente limitadas. Antes de permitir que un agente envíe correos, haga compras, borre datos o modifique sistemas, añade autorización, validación y confirmación humana.
- No ejecutes código generado por un agente sin revisarlo.
- No expongas la API de ejemplo a Internet sin autenticación, límites de peticiones y una estrategia para gestionar secretos.

## Cómo seguir aprendiendo

Una buena forma de trabajar con este repositorio es elegir un proyecto, ejecutarlo, leer su código y modificar una sola cosa cada vez. Después añade una prueba para demostrar que el cambio funciona. Por ejemplo, puedes añadir una herramienta nueva al Agente 02, crear un caso de evaluación para el router o escribir un servidor MCP con una herramienta propia.

La guía [`explicacion agentes.md`](explicacion%20agentes.md) explica los conceptos con más detalle y está pensada para acompañar el código, no para sustituirlo.

Si encuentras un error, guarda el mensaje completo de la terminal y el comando que ejecutaste. Esa información suele ser suficiente para localizar el problema sin rehacer el entorno.
