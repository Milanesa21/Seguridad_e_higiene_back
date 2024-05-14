from controllers.auth_users import create_user, authenticate_user, get_user, delete_user, change_password
from sqlalchemy.orm import Session
from dataBase.db import get_db
from model.user import UserCreate
from fastapi import APIRouter, Depends, HTTPException, status

user_rutes = APIRouter(prefix='/Usuarios', tags=['Crud de Usuarios'])

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


# Ruta para eliminar un usuario
@user_rutes.delete('/deleteUser/{username}')
async def delete_user_route(username: str, db: Session = Depends(get_db)):
    deleted = delete_user(username, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Usuario eliminado exitosamente"}

# Ruta para cambiar la contraseña de un usuario
@user_rutes.patch('/changePassword/{username}')
async def change_password_route(username: str, new_password: str, db: Session = Depends(get_db)):
    changed = change_password(username, new_password, db)
    if not changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Contraseña cambiada exitosamente"}




# @user_rutes.post('/login')
# async def login_user():
#     return await login()

# @user_rutes.get('/users') 
# async def get_users():
#     return await read_users()

