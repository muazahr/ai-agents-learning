# Explicación de los agentes 🤖

Este archivo explica, de forma sencilla y con ejemplos, cada agente que vayamos construyendo en este repositorio.

> **Objetivo:** no solo escribir código, sino entender qué hace cada parte y poder explicarlo en una entrevista técnica.

---

# Agente 01 — Primer agente con herramienta de cálculo

## 1. ¿Qué es este agente?

Nuestro primer agente es un programa en Python que utiliza un modelo de lenguaje (LLM) y tiene acceso a una herramienta externa: una calculadora.

La diferencia entre un chatbot básico y nuestro agente es que el agente puede **decidir utilizar una herramienta** cuando la necesita.

Flujo general:

```text
Usuario
   ↓
Agente
   ↓
LLM
   ↓
¿Necesito una herramienta?
   ↓ Sí
Calculadora
   ↓
Resultado
   ↓
LLM
   ↓
Respuesta al usuario
```

---

## 2. Ejemplo sencillo

El usuario escribe:

```text
¿Cuánto es 25 * 18?
```

El agente recibe la pregunta y se la envía al modelo.

El modelo entiende que para responder correctamente puede utilizar la herramienta `calculate`.

Entonces solicita algo equivalente a:

```json
{
  "expression": "25 * 18"
}
```

Nuestra aplicación ejecuta:

```text
calculate("25 * 18")
```

Resultado:

```text
450
```

El resultado vuelve al modelo y finalmente el agente responde:

```text
El resultado es 450.
```

---

## 3. ¿Por qué esto es un agente?

Porque el modelo no se limita a generar texto.

Tiene acceso a una capacidad externa y puede decidir cuándo utilizarla.

Podemos resumirlo así:

```text
LLM + herramientas + capacidad de decidir cuándo utilizarlas = agente
```

Esto será especialmente importante cuando añadamos herramientas más útiles, como APIs, búsqueda web, bases de datos o sistemas externos.

---

## 4. ¿Qué hace `main.py`?

`main.py` es el punto de entrada de nuestra aplicación.

Cuando ejecutamos:

```bash
python -m app.main
```

se inicia una pequeña interfaz de consola.

Ejemplo:

```text
🤖 AI Agent — Proyecto 01
Escribe 'salir' para terminar.

Tú: ¿Cuánto es 100 / 4?
Agente: El resultado es 25.
```

`main.py` recibe el mensaje del usuario y llama a:

```python
run_agent(user_message)
```

La lógica del agente está separada de la interfaz para mantener el proyecto organizado.

---

## 5. ¿Qué hace `agent.py`?

Este es el cerebro de nuestra aplicación.

Aquí hacemos principalmente cinco cosas:

### 5.1 Cargar la API key

```python
load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
```

La clave se guarda en `.env` y **nunca debe subirse a GitHub**.

Por eso `.env` aparece en `.gitignore`.

---

### 5.2 Definir la herramienta

Le explicamos al modelo que existe una herramienta llamada `calculate`.

La definición contiene:

- nombre de la herramienta;
- descripción;
- parámetros que necesita.

Por ejemplo:

```text
Nombre: calculate
Descripción: Calcula una expresión matemática básica
Parámetro: expression
```

Esto permite que el modelo sepa cómo utilizarla.

---

### 5.3 Recibir la pregunta

La función principal es:

```python
run_agent(user_message)
```

Por ejemplo:

```python
run_agent("¿Cuánto es 50 * 20?")
```

---

### 5.4 El modelo decide si utiliza la herramienta

Tenemos configurado:

```python
tool_choice="auto"
```

Esto significa que el modelo puede decidir si necesita llamar a una herramienta.

Por ejemplo:

```text
Usuario: ¿Cuánto es 50 * 20?
→ utiliza calculate
```

Pero si preguntamos:

```text
Usuario: ¿Qué es Python?
→ no necesita calculate
```

En este segundo caso puede responder directamente.

---

### 5.5 Devolver el resultado al modelo

Cuando la herramienta termina, el resultado se incorpora de nuevo a la conversación.

Por ejemplo:

```text
Usuario
  ↓
"¿Cuánto es 50 * 20?"
  ↓
LLM
  ↓
calculate("50 * 20")
  ↓
1000
  ↓
LLM
  ↓
"El resultado es 1000."
```

Este ciclo es uno de los conceptos fundamentales que estamos aprendiendo.

---

# 6. ¿Qué hace `calculator.py`?

Aquí está implementada nuestra herramienta.

La función principal es:

```python
calculate(expression)
```

Ejemplos:

```text
calculate("2 + 3")
→ 5
```

```text
calculate("10 * 4")
→ 40
```

```text
calculate("100 / 5")
→ 20.0
```

La herramienta recibe una expresión, la procesa y devuelve el resultado al agente.

---

# 7. Ejemplo completo de ejecución

Imaginemos que escribimos:

```text
Tú: ¿Cuánto es 125 * 8 + 20?
```

### Paso 1 — El usuario pregunta

```text
125 * 8 + 20
```

### Paso 2 — El LLM analiza la petición

Detecta que necesita hacer una operación matemática.

### Paso 3 — El LLM solicita la herramienta

```json
{
  "expression": "125 * 8 + 20"
}
```

### Paso 4 — Python ejecuta la herramienta

```text
calculate("125 * 8 + 20")
```

Resultado:

```text
1020
```

### Paso 5 — El resultado vuelve al LLM

El modelo recibe `1020` como resultado de la herramienta.

### Paso 6 — El agente responde

```text
El resultado es 1020.
```

---

# 8. ¿Qué hemos aprendido con el Agente 01?

Con este proyecto hemos aprendido los fundamentos de los agentes:

- qué es un LLM;
- qué es una herramienta;
- qué es el tool calling;
- cómo un LLM puede decidir utilizar una herramienta;
- cómo devolver el resultado de una herramienta al modelo;
- cómo separar la lógica del agente de sus herramientas;
- cómo proteger una API key mediante variables de entorno.

---

# Próximos agentes

Esta sección irá creciendo conforme construyamos los siguientes proyectos.

## Agente 02 — Varias herramientas

Añadiremos varias herramientas y el agente tendrá que decidir cuál utilizar.

Ejemplo:

```text
Usuario: ¿Qué tiempo hace y qué temperatura hay?
                 ↓
              Agente
             ↙       ↘
     weather_tool   temperature_tool
```

## Agente 03 — Memoria

El agente podrá mantener información relevante de conversaciones anteriores.

Ejemplo:

```text
Usuario: Me llamo Muaz.

Agente: Encantado, Muaz.

--- nueva interacción ---

Usuario: ¿Cómo me llamo?

Agente: Te llamas Muaz.
```

## Agente 04 — APIs externas

El agente podrá utilizar servicios externos.

Ejemplo:

```text
Usuario: Busca el precio de una moneda.
          ↓
        Agente
          ↓
     API externa
          ↓
       Resultado
```

## Agente 05 — Búsqueda web

El agente podrá buscar información actualizada en Internet cuando sea necesario.

## Agente 06 — Agente autónomo

El agente podrá dividir un objetivo en varios pasos y utilizar diferentes herramientas para conseguirlo.

## Agente 07 — Multi-agent

Crearemos varios agentes especializados que colaboren entre ellos.

Ejemplo:

```text
                 Agente principal
                 /       |       \
                /        |        \
        Investigador   Analista   Redactor
                \        |        /
                 \       |       /
                  Resultado final
```

---

# Regla de aprendizaje

Cada nuevo agente que construyamos debe responder a estas preguntas:

1. ¿Qué problema resuelve?
2. ¿Qué puede hacer?
3. ¿Qué herramientas utiliza?
4. ¿Cómo decide qué herramienta utilizar?
5. ¿Qué información recibe?
6. ¿Qué información devuelve?
7. ¿Qué ocurre paso a paso cuando recibe una petición?
8. ¿Qué ejemplo práctico podemos ejecutar?
9. ¿Cómo podríamos mejorarlo?
10. ¿Cómo lo explicaríamos en una entrevista técnica?

Este documento se actualizará con cada nuevo agente del repositorio.


---

# Agente 01B — El mismo agente usando Microsoft Agent Framework

## 1. ¿Qué queremos comparar?

En el Agente 01 escribimos manualmente el ciclo de tool calling: describimos la herramienta en un esquema, enviamos la petición al LLM, comprobamos si pidió una herramienta, ejecutamos la función y mandamos el resultado de vuelta al modelo.

En esta versión usamos **Microsoft Agent Framework (MAF)**. El framework permite declarar el agente y sus herramientas en una forma más compacta y gestiona el ciclo de ejecución de herramientas.

Documentación oficial: https://learn.microsoft.com/en-us/agent-framework/get-started/

## 2. Archivos nuevos

- `app_framework/agent.py`: crea y ejecuta el agente con MAF.
- `app_framework/tools.py`: declara la calculadora como herramienta.
- `requirements-framework.txt`: dependencias de esta variante.
- `.env.framework.example`: variables de entorno de ejemplo.
- `tests/test_framework_calculator.py`: pruebas básicas de la función de cálculo.

La implementación original se mantiene intacta para poder comparar ambas versiones.

## 3. Instalación y ejecución

Desde la raíz del repositorio, activa tu entorno virtual y ejecuta:

```bash
pip install -r requirements-framework.txt
```

Copia `.env.framework.example` a `.env` y añade tu clave de API. No compartas la clave ni la subas al repositorio.

Después ejecuta:

```bash
python -m app_framework.agent
```

Ejemplo:

```text
Tú: ¿Cuánto es 25 * 18?
Agente: 25 multiplicado por 18 es 450.
```

El texto exacto puede variar según el modelo.

## 4. ¿Qué hace `app_framework/agent.py`?

### Cliente del modelo

```python
client = OpenAIChatClient(model=model, api_key=api_key)
```

El cliente conecta el framework con el modelo de OpenAI. La clave se lee de una variable de entorno.

### Definición del agente

```python
return Agent(
    client=client,
    name="CalculadoraAgent",
    instructions="...",
    tools=[calculate],
)
```

Aquí declaramos el cliente, el nombre, las instrucciones y las herramientas disponibles. No construimos manualmente el esquema JSON de la función.

### Ejecución

```python
response = await agent.run(user_message)
return response.text
```

El framework coordina la interacción con el modelo y la ejecución de la herramienta. La llamada es asíncrona, por eso usamos `async` y `await`.

## 5. ¿Qué hace `app_framework/tools.py`?

La función `calculate` contiene la lógica matemática. La anotación `@tool` declara que la función puede utilizarse como herramienta del agente. Su descripción y sus parámetros ayudan al framework a exponerla al modelo.

La herramienta sigue siendo código Python normal: el framework no calcula por sí solo; invoca nuestra función cuando el modelo solicita utilizarla.

> En este ejemplo educativo, la herramienta está configurada sin pedir aprobación. Para herramientas que modifican datos, envían mensajes, realizan compras o acceden a información sensible, debemos añadir controles y aprobaciones explícitas.

## 6. Comparación línea por línea

| Aspecto | Agente 01: manual | Agente 01B: con MAF |
|---|---|---|
| Cliente del modelo | `OpenAI(...)` | `OpenAIChatClient(...)` |
| Definir herramienta | Esquema de herramienta escrito a mano | Función decorada con `@tool` |
| Describir herramientas al LLM | Se pasa `TOOLS` en la petición | Se pasa `tools=[calculate]` al agente |
| Ejecutar tool calls | Analizamos `tool_calls` y añadimos mensajes | El framework coordina la invocación |
| Ciclo de conversación | Programado explícitamente | Abstraído por el framework |
| Control y aprendizaje | Más detalles internos visibles | Menos código repetitivo |

## 7. ¿Cuál es mejor?

Ninguno gana siempre.

- **Sin framework:** bueno para aprender el protocolo, depurar y controlar cada paso.
- **Con framework:** útil cuando crecen las herramientas, los flujos, el estado y las integraciones.
- **Coste del framework:** añade una dependencia y hay que aprender sus abstracciones; las APIs pueden cambiar entre versiones.

La regla es entender primero qué hace el framework por nosotros. No debemos elegirlo solo porque tenga más funcionalidades.

## 8. Preguntas de entrevista

**¿Qué aporta un framework de agentes?**

Reduce código repetitivo y ofrece abstracciones para configurar agentes, registrar herramientas y coordinar su ejecución.

**¿El framework sustituye al LLM?**

No. El LLM sigue interpretando la petición y decidiendo si necesita una herramienta. El framework coordina la aplicación y el ciclo de ejecución.

**¿El framework ejecuta la calculadora por arte de magia?**

No. Nosotros implementamos `calculate`; el framework la registra y se encarga de invocarla cuando corresponde.

**¿Cuándo harías la implementación manual?**

Para un flujo pequeño o cuando necesito control fino y quiero aprender cómo funciona el tool calling.

**¿Cuándo usarías MAF?**

Cuando me conviene su soporte para agentes, herramientas, sesiones, workflows e integraciones dentro de un sistema mayor.

## 9. Resumen mental

```text
Agente manual:
Yo defino herramienta → yo detecto la llamada → yo ejecuto → yo devuelvo resultado

Agente con framework:
Yo defino herramienta y agente → el framework coordina la llamada y el resultado
```

El framework no elimina la necesidad de diseñar buenas herramientas, instrucciones, permisos, pruebas y límites de seguridad.


---

# Agente 02 — Asistente con varias herramientas

## Objetivo

Este agente amplía el Agente 01B. En vez de tener solo una calculadora, dispone de varias herramientas y el modelo decide cuál usar para cada petición.

## Herramientas disponibles

- `calculate(expression)`: calcula una expresión matemática.
- `current_datetime()`: consulta la fecha y hora local del equipo.
- `save_note(title, content)`: guarda una nota en `data/notes.json`.
- `list_notes()`: devuelve los títulos de las notas.
- `get_note(title)`: recupera el contenido de una nota cuyo título coincida.

## Archivos nuevos

- `app_framework/agent_multi.py`: construye el agente y registra todas las herramientas.
- `app_framework/tools_multi.py`: contiene las herramientas de fecha/hora y notas.
- `tests/test_multi_tools.py`: pruebas para guardar, listar y recuperar notas.

La calculadora se reutiliza desde `app_framework/tools.py`. El agente anterior `app_framework.agent` no se modifica, de modo que podemos seguir comparando los proyectos.

## Ejecutar en Windows

Desde la raíz del repositorio y con el entorno virtual activado:

```powershell
python -m app_framework.agent_multi
```

Prueba cada caso por separado:

1. `¿Cuánto es 125 * 8?`
2. `¿Qué fecha y hora son ahora?`
3. `Guarda una nota titulada Ideas con el contenido: probar un agente con varias herramientas.`
4. `Lista mis notas.`
5. `Recupera la nota Ideas.`

Para cerrar, escribe `salir`.

## Cómo se guardan las notas

Las notas se guardan en el archivo local `data/notes.json`. El archivo se crea automáticamente cuando se guarda la primera nota. Si se elimina, se perderán las notas guardadas en él. No guardes contraseñas, claves API ni datos sensibles.

## Ejecutar las pruebas

```powershell
python -m pytest
```

Las pruebas de notas usan un directorio temporal, por lo que no deberían alterar tus notas reales.

## Qué hemos aprendido

1. Un agente puede disponer de varias herramientas a la vez.
2. Las descripciones y los parámetros ayudan al modelo a elegir y llamar a la herramienta correcta.
3. Las herramientas son funciones de Python; el framework coordina su invocación.
4. El almacenamiento local es distinto de la memoria conversacional: guardar una nota no significa que el modelo la recuerde automáticamente, tiene que recuperarla con una herramienta.
5. Hay que verificar el resultado de las herramientas y no afirmar que una operación se completó si falló.

> Nota de desarrollo: los nuevos archivos se han añadido al repositorio, pero deben ejecutarse en tu equipo para confirmar que la versión instalada de Microsoft Agent Framework es compatible y que todas las pruebas pasan.


---

# Agente 03 — Memoria local persistente

## Objetivo

El Agente 03 introduce una memoria explícita que sobrevive al cierre del programa. A diferencia del historial temporal de un chat, esta memoria se almacena en `data/memory.json` y el agente accede a ella mediante herramientas.

## Herramientas

- `remember_fact(category, fact)`: guarda un dato cuando el usuario lo pide explícitamente.
- `search_memory(query)`: busca por texto en categoría o dato.
- `list_memories()`: muestra los recuerdos guardados con sus IDs.
- `forget_memory(memory_id)`: borra un recuerdo concreto por su ID.

## Flujo

```text
Usuario pide recordar un dato
          ↓
LLM decide llamar remember_fact
          ↓
Python valida y guarda el dato en JSON
          ↓
La herramienta devuelve el ID
          ↓
El agente confirma el resultado
```

Para recordar algo en una ejecución posterior, el agente debe llamar a `search_memory` o `list_memories`. El modelo no obtiene automáticamente el contenido del archivo.

## Ejecutar en Windows

```powershell
python -m app_framework.agent_memory
```

Prueba:
1. `Recuerda que estoy aprendiendo Python.`
2. Cierra el programa con `salir`.
3. Vuelve a ejecutarlo.
4. Pregunta `¿Qué recuerdas sobre Python?`
5. Prueba `Lista mis recuerdos`.
6. Para borrar un dato, identifica su ID y pide que lo elimine.

## Privacidad y límites

- Solo se deben guardar datos no sensibles y cuando el usuario lo solicita expresamente.
- No guardes contraseñas, claves API, información de salud ni otros datos sensibles.
- La memoria es local a la carpeta desde la que se ejecuta el programa.
- El usuario puede inspeccionar o borrar el archivo `data/memory.json` manualmente.
- En una aplicación real convendría añadir cifrado, permisos, control de acceso, auditoría y una política de retención.

## Pruebas

```powershell
python -m pytest
```

Las pruebas usan archivos temporales y no deben modificar los recuerdos reales.

---

# Agente 04 — Integración con una API meteorológica

## Objetivo

Conectar el agente con un servicio externo para obtener datos que el modelo no debería inventar ni confiar en recordar. Usamos Open-Meteo, que ofrece geocodificación y previsiones sin requerir una clave de API meteorológica para este ejemplo.

## Herramienta

`get_weather(city)` realiza dos solicitudes:
1. Busca las coordenadas de la ciudad mediante la API de geocodificación.
2. Consulta el tiempo actual y la previsión diaria para esas coordenadas.

La función utiliza un timeout, valida que existan resultados y maneja errores de red o respuestas no válidas.

## Ejecutar en Windows

```powershell
python -m app_framework.agent_weather
```

Prueba:
- `¿Qué tiempo hace en Granada, España?`
- `Dime la temperatura y la máxima prevista para Madrid.`
- `Consulta el tiempo en una ciudad que no exista.`

La herramienta devuelve el dato recibido de Open-Meteo y una nota indicando que la previsión puede cambiar. La respuesta exacta depende de los datos disponibles en el momento de la consulta.

## Arquitectura

```text
Usuario
  ↓
Agente (LLM)
  ↓ decide usar get_weather
Herramienta Python
  ↓
Geocodificación Open-Meteo
  ↓ coordenadas
API de previsión Open-Meteo
  ↓
Datos meteorológicos
  ↓
Agente explica el resultado
```

## Qué aprendemos

- Cómo una herramienta consulta una API HTTP externa.
- Cómo convertir una ciudad en coordenadas.
- Cómo interpretar JSON y validar campos.
- Cómo gestionar errores de red y timeouts.
- Por qué los datos actuales deben consultarse y no inventarse.

## Pruebas

```powershell
python -m pytest
```

Las pruebas de la herramienta meteorológica usan respuestas simuladas; no dependen de que el servicio externo esté disponible durante la prueba.
