from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import subprocess
import time
from typing import List

class Query(BaseModel):
    input_text: str
    conversation_history: List[str] = []

app = FastAPI()

# Definimos la cadena inicial del prompt
initial_prompt = (
    "Eres un asistente amigable y servicial llamado Jorgito el ingeniero, "
    "se supone que tu comportamiento se debe basar en un asistente de mentorías para el ámbito industrial. "
    "Por favor, proporciona respuestas útiles y detalladas, procura que sean lo más técnicas y entendibles posibles. "
    "trata de no ser redundante y de ser lo más claro posible."
)

# Función para ejecutar el modelo
def run_model(full_prompt):
    process = subprocess.Popen('ollama run llama3', 
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               shell=True,
                               bufsize=1,
                               universal_newlines=True)
    
    stdout, stderr = process.communicate(input=full_prompt.encode())

    if process.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Error: {stderr.decode()}")

    return stdout

# Generador para transmitir respuestas parciales
def model_output_generator(full_prompt):
    process = subprocess.Popen('ollama run llama3', 
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               shell=True,
                               bufsize=1,
                               universal_newlines=True)
    
    process.stdin.write(full_prompt)
    process.stdin.close()

    # Leer la salida línea por línea y transmitirla
    for line in process.stdout:
        yield line

    # Esperar a que el proceso termine
    process.stdout.close()
    process.wait()

    if process.returncode != 0:
        stderr = process.stderr.read()
        process.stderr.close()
        raise HTTPException(status_code=500, detail=f"Error: {stderr}")

# Ruta para manejar las solicitudes POST con transmisión
@app.post("/query/")
async def get_response(query: Query):
    full_prompt = initial_prompt + query.input_text

    # Verificar si se ha proporcionado historial de conversación
    if query.conversation_history:
        for utterance in query.conversation_history:
            full_prompt += "\n" + utterance

    return StreamingResponse(model_output_generator(full_prompt), media_type="text/plain")
