from controllers.auth_user import login, read_users
from fastapi import APIRouter

user_rutes = APIRouter(prefix='/user')

@user_rutes.post('/login')
async def login_user():
    return await login()

@user_rutes.get('/users')
async def get_users():
    return await read_users()

