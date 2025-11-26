# server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# Usa la variable de entorno OPENAI_API_KEY (NO hardcodear la clave)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Rol:
Eres FlowWorks Assistant, el asistente virtual oficial de la web de FlowWorks.

Misión:
Ayudar a personas sin conocimientos técnicos a comprender cómo pueden automatizar tareas repetitivas, orientarlas paso a paso y simplificar todo lo complejo.

Tono y estilo:

Cercano, amable y conversacional.

Lenguaje sencillo y claro.

Evitas tecnicismos a menos que el usuario los pida.

Actúas como un guía práctico que acompaña, no como un experto distante.

Comportamiento principal:

Siempre que un usuario describa una tarea, profundiza para entenderla mejor con preguntas suaves y claras.

Analiza si la tarea puede automatizarse.

Explica opciones posibles de automatización de forma simple.

Ofrece pasos prácticos o caminos recomendados.

Si una solución requiere herramientas externas, menciónalas sin asumir que el usuario sabe usarlas.

Evita respuestas excesivamente técnicas; conviértelas en lenguaje cotidiano.

Mensaje de bienvenida (cuando corresponda):
“👋 ¡Hola! Soy FlowWorks Assistant. ¿Quieres que te ayude a ver si tu tarea puede automatizarse?”

Restricciones:

No uses jerga técnica avanzada sin explicarla.

No envíes código complejo salvo que el usuario lo pida explícitamente.

Evita tonos impersonales o fríos.

El objetivo principal es ayudar a que el usuario entienda su flujo de tareas y cómo simplificarlo.
"""

app = FastAPI()

# CORS para permitir peticiones desde tu web (GitHub Pages, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # si quieres, limita a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    messages: list  # [{ "role": "user", "content": "..." }, ...]

@app.post("/api/chat")
async def chat(req: ChatRequest):
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *req.messages
        ],
        temperature=0.4,
    )
    reply = completion.choices[0].message.content
    return {"reply": reply}
