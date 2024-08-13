from fastapi import FastAPI
from routers.user_router import user_rutes
from routers.company_router import company_rutes
from routers.auth_router import auth_router
from fastapi.middleware.cors import CORSMiddleware
import init_db
from services.Jorgito import app as jorgito_app
from controllers.socket_controllers import router as socket_router  # Importa el router de WebSocket
from services.roles_permisos_asignacion import Db_insert_RP
from routers.permiso_router import permiso_router

#Para iniciar el proyecto: uvicorn main:app --reload
app = FastAPI()

origins = [
    "http://127.0.0.1:3000",  # Cambiado al puerto por defecto de React
    "http://127.0.0.1:8000",  # Asegúrate de que el puerto es el correcto
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_rutes)
app.include_router(auth_router)
app.include_router(company_rutes)
app.mount("/jorgito", jorgito_app)
app.include_router(socket_router)  # Incluye el router de WebSocket
app.include_router(permiso_router)

Db_insert_RP()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
