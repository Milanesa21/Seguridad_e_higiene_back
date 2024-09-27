from fastapi import FastAPI
from routers.user_router import user_routes
from routers.company_router import company_rutes
from routers.auth_router import auth_router
from fastapi.middleware.cors import CORSMiddleware
import init_db
from services.Jorgito import app as jorgito_app
from controllers.socket_controllers import router as socket_router  # Importa el router de WebSocket
from services.roles_permisos_asignacion import Db_insert_RP
from routers.permiso_router import permiso_router
from routers.cloudinary_routes import file_router as cloudinary_router
#from routers.IA_uniformes_routes import router as IA_uniformes_router
#from routers.IA_ambiente_routes import router as IA_ambiente_router

#Para iniciar el proyecto: uvicorn main:app --reload
app = FastAPI()

origins = [
    "http://127.0.0.1:3000", 
    "http://127.0.0.1:8000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes)
app.include_router(auth_router)
app.mount("/jorgito", jorgito_app)
app.include_router(company_rutes)
app.include_router(socket_router)  
app.include_router(permiso_router)
app.include_router(cloudinary_router)
#app.include_router(IA_uniformes_router)
#app.include_router(IA_ambiente_router)

Db_insert_RP()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
