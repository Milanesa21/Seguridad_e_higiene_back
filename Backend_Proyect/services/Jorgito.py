from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import subprocess

class Query(BaseModel):
    input_text: str

app = FastAPI()

# Generador para transmitir respuestas parciales letra por letra
def model_output_generator(full_prompt):
    process = subprocess.Popen(
        'ollama run Jorgito2',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        bufsize=1,
        universal_newlines=True
    )
    
    process.stdin.write(full_prompt)
    process.stdin.close()

    while True:
        char = process.stdout.read(1)  # Leer un carácter a la vez
        if not char:
            break
        yield char  # Enviar el carácter como respuesta

    process.stdout.close()
    process.wait()

    if process.returncode != 0:
        stderr = process.stderr.read()
        process.stderr.close()
        raise HTTPException(status_code=500, detail=f"Error: {stderr}")


# Ruta para manejar las solicitudes POST con transmisión
@app.post("/query/")
async def get_response(query: Query):
    full_prompt = query.input_text
    return StreamingResponse(model_output_generator(full_prompt), media_type="text/plain")