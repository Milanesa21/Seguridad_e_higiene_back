from controllers.auth_users import create_user, authenticate_user, get_user
from sqlalchemy.orm import Session
from dataBase.db import engine, get_db
from model.user import UserCreate
from fastapi import APIRouter, Depends, HTTPException, status

user_rutes = APIRouter(prefix='/user')

# Funcion que crea un usuario
@user_rutes.post('/createUser')
def create_users(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(user,db)
    return db_user

# Funcion para iniciar sesion de un usuario

@user_rutes.post('/login')
async def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    return {"message":"Inicio de sesion exitoso","Usuario":user}
    

@user_rutes.get('/{username}')
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = get_user(username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message":"Usuario encontrado","Usuario":user}





# @user_rutes.post('/login')
# async def login_user():
#     return await login()

# @user_rutes.get('/users')
# async def get_users():
#     return await read_users()

