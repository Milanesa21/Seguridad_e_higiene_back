from fastapi import FastAPI
from routers.user_router import user_rutes
from fastapi.middleware.cors import CORSMiddleware

# Para correr el servidor se debe ejecutar el siguiente comando en la terminal
# uvicorn main:app --reload

app = FastAPI()

<<<<<<< HEAD
=======
origins = [
    "http://localhost:5173",  # Reemplaza con la URL de tu aplicación React sin la barra al final
    "http://127.0.0.1:8000",  # Asegúrate de que el puerto es el correcto
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["POST"],  # Permitir solo el método POST
    allow_headers=["*"],
)
>>>>>>> e306f23f817b4c7d2fdaa1d03982fb48c854df03
app.include_router(user_rutes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
