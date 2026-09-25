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
