from controllers.auth_users import create_user, authenticate_user, get_user_by_name, delete_user, change_password, change_job_position, get_user_email, change_name
from services.email_service import send_email
from services.jwt import write_token
from sqlalchemy.orm import Session
from dataBase.db import get_db
from model.user import UserCreate, CreateUsersRequest, LoginRequest
from model.alert_message import AlertMessage
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
import random
from services.Jorgito import app as jorgito_app  # Importa la aplicación de Jorgito



user_rutes = APIRouter(prefix='/Usuarios', tags=['Crud de Usuarios'])

# Ruta para crear usuarios
@user_rutes.post('/createUsers')
async def create_users(request: CreateUsersRequest, db: Session = Depends(get_db)):
    users = []
    for i in range(request.num_usuarios):
        password = "123456"  # Contraseña predeterminada
        email = f"email{random.randint(1, 100000)}@predeterminado.com"  # Generar email único
        user_data = {
            "full_name": f"Usuario N{i+1}",
            "email": email,
            "password": password,
            "puesto_trabajo": request.puesto_trabajo
        }
        try:
            db_user = create_user(UserCreate(**user_data), db)
            users.append(db_user)
            print(f"Usuario creado: {db_user.full_name} con email {db_user.email}")
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            raise HTTPException(status_code=500, detail=f"Error al crear usuario: {e}")
            
    return {"status": "success", "users": users}
    

# Funcion para iniciar sesion de un usuario
@user_rutes.post('/login')
async def login_user(login_request: LoginRequest, db: Session = Depends(get_db)):
    full_name = login_request.full_name
    password = login_request.password
    user = authenticate_user(full_name, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    user_data = {
        "id": user.id
    }

    # Generar un token JWT y devolverlo en la respuesta
    token = write_token(user_data)
    return token


# Ruta para obtener un usuario por su nombre
@user_rutes.get('/{full_name}')
async def get_user_by_full_name(full_name: str, db: Session = Depends(get_db)):
    user = get_user_by_name(full_name, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message":"Usuario encontrado","Usuario":user}

#Ruta para obtener un usuario por su email
@user_rutes.get('/email/{email}')
async def get_user__by_email(email: str, db: Session = Depends(get_db)):
    emaill = get_user_email(email, db)
    if not emaill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message":"Usuario encontrado","Usuario":emaill}

# Ruta para eliminar un usuario
@user_rutes.delete('/deleteUser/{full_name}')
async def delete_user_route(full_name: str,email: str, puesto_trabajo: str, db: Session = Depends(get_db)):
    deleted = delete_user(full_name,email, puesto_trabajo, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Usuario eliminado exitosamente"}

#eviar correo para cambiar contraseña
@user_rutes.post('/sendEmail/{full_name}')
async def send_email_route(full_name: str, db: Session = Depends(get_db)):
    user = get_user_by_name(full_name, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    send_email(full_name, user.email)

# Ruta para cambiar la contraseña de un usuario
@user_rutes.patch('/changePassword/{full_name}')
async def change_password_route(full_name: str,email: str, new_password: str, db: Session = Depends(get_db)):
    changed = change_password(full_name, email, new_password, db)
    if not changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Contraseña cambiada exitosamente"}
    

# Ruta para cambiar el puesto de trabajo de un usuario
@user_rutes.patch('/changeJobPosition/{full_name}')
async def change_job_position_route(full_name: str, email: str, new_position: str, db: Session = Depends(get_db)):
    changed = change_job_position(full_name, email, new_position, db)
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


#Ruta para enviar un mensaje de emergencia
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
    
    # En este ejemplo, simplemente devolvemos un mensaje de confirmación
    return {"message": f"¡Emergencia! {full_name} en el puesto de trabajo {puesto_trabajo} necesita asistencia: {message}"}

# Incluir las rutas de Jorgito en el router principal
main_app = FastAPI()
main_app.include_router(user_rutes)  # Incluir las rutas de usuario
main_app.mount("/Jorgito", jorgito_app)  # Montar la aplicación de Jorgito
