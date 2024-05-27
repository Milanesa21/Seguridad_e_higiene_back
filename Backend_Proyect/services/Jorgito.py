from urllib import response
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import subprocess
import time

app = FastAPI()

class Query(BaseModel):
    input_text: str

# Definimos la cadena inicial del prompt
initial_prompt = (
    "Eres un asistente amigable y servicial llamado Jorgito el ingeniero, "
    "se supone que tu comportamiento se debe basar en un asistente de mentorías para el ámbito industrial. "
    "Por favor, proporciona respuestas útiles y detalladas a las preguntas, procura que sean lo más técnicas y entendibles posibles. "
    "trata de no ser redundante y de ser lo más claro posible. "
)

# Función para ejecutar el modelo
def run_model(full_prompt):
    process = subprocess.Popen('ollama run llama3', 
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               shell=True)
    stdout, stderr = process.communicate(input=full_prompt.encode())

    if process.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Error: {stderr.decode()}")

    return stdout.decode()

# Ruta para manejar las solicitudes POST
@app.post("/query/")
async def get_response(query: Query):
    full_prompt = initial_prompt + query.input_text
    response_content = run_model(full_prompt)
    print(response_content)
    return Response(content=response_content, media_type="text/plain")




