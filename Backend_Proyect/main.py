from imp import reload
from fastapi import FastAPI
from routers.user_router import user_rutes
from routers.company_router import company_rutes
from routers.auth_router import auth_router
from fastapi.middleware.cors import CORSMiddleware
import init_db  # Importa el módulo para inicializar la base de datos
from services.Jorgito import app as jorgito_app  # Importa la aplicación de Jorgito

# Para correr el servidor se debe ejecutar el siguiente comando en la terminal
# uvicorn main:app --reload
 
app = FastAPI()

origins = [
    "http://localhost:5173",  # Reemplaza con la URL de tu aplicación React sin la barra al final
    "http://127.0.0.1:8000",  # Asegúrate de que el puerto es el correcto
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],
)

# Incluir las rutas de usuario
app.include_router(user_rutes)
app.include_router(auth_router)
app.include_router(company_rutes)

# Montar la aplicación de Jorgito
app.mount("/jorgito", jorgito_app)  # Asegúrate de que la ruta está en minúsculas

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
