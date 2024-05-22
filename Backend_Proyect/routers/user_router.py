from controllers.auth_users import create_user, authenticate_user, get_user_by_name, delete_user, change_password, change_job_position, get_user_email, change_name
from sqlalchemy.orm import Session
from dataBase.db import get_db
from model.user import UserCreate, AlertMessage
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel


class LoginRequest(BaseModel):
    full_name: str
    password: str




user_rutes = APIRouter(prefix='/Usuarios', tags=['Crud de Usuarios'])

# Funcion que crea un usuario
@user_rutes.post('/createUser')
async def create_users(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(user,db)
    return db_user

# Funcion para iniciar sesion de un usuario
@user_rutes.post('/login')
async def login_user(login_request: LoginRequest, db: Session = Depends(get_db)):
    full_name = login_request.full_name
    password = login_request.password
    user = authenticate_user(full_name, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    return {"message": "Inicio de sesión exitoso", "Usuario": user}
    

@user_rutes.get('/{full_name}')
async def get_user_by_full_name(full_name: str, db: Session = Depends(get_db)):
    user = get_user_by_name(full_name, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message":"Usuario encontrado","Usuario":user}


@user_rutes.get('/email/{email}')
async def get_user__by_email(email: str, db: Session = Depends(get_db)):
    emaill = get_user_email(email, db)
    if not emaill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message":"Usuario encontrado","Usuario":emaill}

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

# Ruta para cambiar el nombre de un usuario
@user_rutes.patch('/changeName/{full_name}')
async def change_name_route(full_name: str, new_name: str, db: Session = Depends(get_db)):
    changed = change_name(full_name, new_name, db)
    if not changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "El nombre de usuario fue correctamente cambiado"}

@user_rutes.post('/sendEmergencyMessage/{full_name}')
async def send_emergency_message(full_name: str, puesto_trabajo: str, message: str = None, db: Session = Depends(get_db)):
    user = get_user_by_name(full_name, db)  
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if message is None:
        message = "¡Emergencia! Necesito asistencia."
    
    # Crear una instancia de AlertMessage y guardarla en la base de datos
    alert_message = AlertMessage(user_id = user.id, full_name = user.full_name, puesto_trabajo = user.puesto_trabajo , message = message)
    db.add(alert_message)
    db.commit()
    # Aquí puedes implementar la lógica para enviar el mensaje de emergencia
    # Por ejemplo, enviar un mensaje a través de un sistema de notificación o correo electrónico
    
    # En este ejemplo, simplemente devolvemos un mensaje de confirmación
    return {"message": f"¡Emergencia! {full_name} en el puesto de trabajo {puesto_trabajo} necesita asistencia: {message}"}
