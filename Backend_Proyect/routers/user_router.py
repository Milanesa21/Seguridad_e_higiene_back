from controllers.auth_users import create_user, authenticate_user, get_user, delete_user, change_password, change_job_position
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
async def login_user(full_name: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(full_name, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    return {"message":"Inicio de sesion exitoso","Usuario":user}
    



# Funcion para obtener un usuario por su username
@user_rutes.get('/{full_name}')
async def get_user_by_full_name(full_name: str, db: Session = Depends(get_db)):
    user = get_user(full_name, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message":"Usuario encontrado","Usuario":user}


# Ruta para eliminar un usuario
@user_rutes.delete('/deleteUser/{full_name}')
async def delete_user_route(full_name: str, db: Session = Depends(get_db)):
    deleted = delete_user(full_name, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Usuario eliminado exitosamente"}

# Ruta para cambiar la contraseña de un usuario
@user_rutes.patch('/changePassword/{full_name}')
async def change_password_route(full_name: str, new_password: str, db: Session = Depends(get_db)):
    changed = change_password(full_name, new_password, db)
    if not changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Contraseña cambiada exitosamente"}
    

# Ruta para cambiar el puesto de trabajo de un usuario
@user_rutes.patch('/changeJobPosition/{full_name}')
async def change_job_position_route(full_name: str, new_position: str, db: Session = Depends(get_db)):
    changed = change_job_position(full_name, new_position, db)
    if not changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Puesto de trabajo cambiado exitosamente"}



# @user_rutes.post('/login')
# async def login_user():
#     return await login()

# @user_rutes.get('/users') 
# async def get_users():
#     return await read_users()

