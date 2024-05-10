from controllers.auth_user import login, read_users
from fastapi import APIRouter

user_rutes = APIRouter(prefix='/user', tags=["User"] , responses={404:{"mesege": "No encontrado"} })

@user_rutes.post('/login')
async def login_user():
    return await login()


