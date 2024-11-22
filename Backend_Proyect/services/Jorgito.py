from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import subprocess

class Query(BaseModel):
    input_text: str

app = FastAPI()

# Prompt inicial para el asistente de seguridad e higiene industrial
initial_prompt = (
    "Eres un asistente de seguridad e higiene industrial. "
    "Tu objetivo es proporcionar información y orientación sobre prácticas de seguridad e higiene que se deben seguir en el lugar de trabajo para proteger la salud y seguridad de los empleados. "
    "Responde de manera clara y concisa, siempre enfocándote en las normativas de seguridad e higiene industrial aplicables. "
    "Si la normativa o regla que se te esta preguntando es una que se tiene en varios paises, responde con las de Argentina"
    "Ademas debes de ayudar con toda la informacion posible en caso de que se pregunte de como utilizar herramientas laborales, como se deben de utilizar, que medidas de seguridad se deben de tomar, etc. "
    "Si se te solicita una guia, haz un paso a paso de como realizar la tarea solicitada o el como utilizar la herramienta solicitada. "
)

# Generador para transmitir respuestas parciales letra por letra
def model_output_generator(full_prompt):
    with subprocess.Popen(
        'ollama run llama3.2:1b',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        bufsize=1,
        universal_newlines=True
    ) as process:
        try:
            # Enviar el prompt inicial y la consulta del usuario al proceso antes de empezar a leer la salida
            process.stdin.write(initial_prompt + full_prompt)
            process.stdin.close()

            # Esperar a que el proceso comience a generar una respuesta
            process.stdout.flush()

            # Leer la salida del proceso carácter por carácter
            while True:
                char = process.stdout.read(1)  # Leer un carácter a la vez
                if not char:
                    break
                yield char  # Enviar el carácter como respuesta

            process.stdout.close()
            process.wait(timeout=30)  # Añadir un tiempo de espera para evitar bloqueos indefinidos

            if process.returncode != 0:
                stderr = process.stderr.read()
                process.stderr.close()
                raise HTTPException(status_code=500, detail=f"Error: {stderr}")

        except subprocess.TimeoutExpired:
            process.kill()
            raise HTTPException(status_code=500, detail="Error: El proceso se bloqueó y fue terminado.")

# Ruta para manejar las solicitudes POST con transmisión
@app.post("/query/")
async def get_response(query: Query):
    full_prompt = query.input_text
    return StreamingResponse(model_output_generator(full_prompt), media_type="text/plain")