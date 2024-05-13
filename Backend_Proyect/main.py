from fastapi import FastAPI
from routers.router import router
from routers.user_router import user_rutes

# Para correr el servidor se debe ejecutar el siguiente comando en la terminal
# uvicorn main:app --reload

app = FastAPI()





app.include_router(user_rutes)
app.include_router(router)

