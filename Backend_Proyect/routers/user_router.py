from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import random
from controllers.auth_users import (
    create_user, authenticate_user, get_all_user_by_name, delete_user,
    change_password, change_job_position, get_user_by_id, get_user_email,
    change_name, get_user_by_name, change_email,get_all_users
)
from services.jwt import write_token
from services.email_service import send_email
from dataBase.db import get_db
from model.schemas.user_schemas import UserCreate, CreateUsersRequest, LoginRequest, UpdateUserRequest
from model.alert_message import AlertMessage
from model.schemas.alert_message_schemas import AlertMessageRequest

# Crear un router para las rutas de usuario
user_routes = APIRouter(prefix='/Usuarios', tags=['Crud de Usuarios'])

# Ruta para crear usuarios
@user_routes.post('/createUsers')
async def create_users(request: CreateUsersRequest, db: Session = Depends(get_db)):
    users = []
    for i in range(request.num_usuarios):
        password = "123456"  # Contraseña predeterminada
        email = f"email{random.randint(1, 100000)}@predeterminado.com"  # Generar email único
        user_data = {
            "full_name": f"Usuario N{i+1}",
            "email": email,
            "password": password,
            "puesto_trabajo": request.puesto_trabajo,
            'id_role': 4,
            'id_empresa': request.id_empresa
        }
        if user_data['puesto_trabajo'] == 'Area de seguridad':
            user_data['id_role'] = 3
        elif user_data["puesto_trabajo"] == 'Admin':
            user_data['id_role'] = 2
        try:
            db_user = create_user(UserCreate(**user_data), db)
            users.append(db_user)
            print(f"Usuario creado: {db_user.full_name} con email {db_user.email}")
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            raise HTTPException(status_code=500, detail=f"Error al crear usuario: {e}")
            
    return {"status": "success", "users": users}

# Ruta para iniciar sesión
@user_routes.post('/login')
async def login_user(login_request: LoginRequest, db: Session = Depends(get_db)):
    full_name = login_request.full_name
    puesto_trabajo = login_request.puesto_trabajo
    password = login_request.password
    id_empresa = login_request.id_empresa
    user = authenticate_user(id_empresa,full_name,puesto_trabajo, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    user_data = {
        "id": user.id,
        'id_empresa': user.id_empresa,
    }

    # Generar un token JWT y devolverlo en la respuesta
    token = write_token(user_data)
    return token

@user_routes.get('/user/all')
async def get_all_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users

# Ruta para actualizar los datos del usuario (nombre, email, contraseña)
@user_routes.patch('/user/updateData')
async def update_user_data(request: UpdateUserRequest, db: Session = Depends(get_db)):
    user_id = request.id
    # Obtener el usuario por ID
    user = get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Cambiar el nombre del usuario
    if request.new_name:
        if not change_name(user_id, request.new_name, db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to change name")

    # Cambiar el email del usuario
    if request.new_email:
        if not change_email(user_id, user["email"], request.new_email, db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to change email")

    # Cambiar la contraseña del usuario
    if request.new_password:
        if not change_password(user_id, request.new_password, db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to change password")

    return {"message": "User data updated successfully"}

# Ruta para obtener un usuario por su ID
@user_routes.get('/user/id/{id}')
async def get_user_id(id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message":"Usuario encontrado","Usuario":user}

# Ruta para obtener un usuario por su nombre
@user_routes.get('/user/name/{full_name}')
async def get_user_by_full_name(full_name: str, db: Session = Depends(get_db)):
    user = get_user_by_name(full_name, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message":"Usuario encontrado","Usuario":user}

# Ruta para obtener todos los usuarios por su nombre
@user_routes.get('/user/all/{full_name}')
async def get_all_user_by_full_name(full_name: str, db: Session = Depends(get_db)):
    users = get_all_user_by_name(full_name, db)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return {"message":"Usuarios encontrados","Usuarios":users}

# Ruta para obtener un usuario por su email
@user_routes.get('/user/email/{email}')
async def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = get_user_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message":"Usuario encontrado","Usuario":user}

# Ruta para eliminar un usuario
@user_routes.delete('/user/delete/{full_name}')
async def delete_user_route(full_name: str, email: str, puesto_trabajo: str, db: Session = Depends(get_db)):
    if not delete_user(full_name, email, puesto_trabajo, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Usuario eliminado exitosamente"}

# Ruta para enviar un correo para cambiar contraseña
@user_routes.post('/user/sendEmail/{full_name}')
async def send_email_route(full_name: str, db: Session = Depends(get_db)):
    user = get_user_by_name(full_name, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    send_email(full_name, user.email)

# Ruta para cambiar la contraseña de un usuario
@user_routes.patch('/user/changePassword/{id}')
async def change_password_route(id: int, new_password: str, db: Session = Depends(get_db)):
    if not change_password(id, new_password, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to change password")
    return {"message": "Contraseña cambiada exitosamente"}

# Ruta para cambiar el puesto de trabajo de un usuario
@user_routes.patch('/user/changeJobPosition/{id}')
async def change_job_position_route(id: int, new_position: str, db: Session = Depends(get_db)):
    if not change_job_position(id, new_position, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to change job position")
    return {"message": "Puesto de trabajo cambiado exitosamente"}

# Ruta para cambiar el nombre de un usuario
@user_routes.patch('/user/changeName/{id}')
async def change_name_route(id: int, new_name: str, db: Session = Depends(get_db)):
    if not change_name(id, new_name, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Failed to change name")
    return {"message": "El nombre de usuario fue correctamente cambiado"}

# Ruta para enviar un mensaje de alerta
@user_routes.post('/SendAlertMessage')
async def send_message(alert_message: AlertMessageRequest, db: Session = Depends(get_db)):
    full_name = alert_message.full_name
    user_id = alert_message.user_id
    puesto_trabajo = alert_message.puesto_trabajo
    message = alert_message.message
    print (full_name, user_id, puesto_trabajo, message)

    if not message:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message is required")

    # Lógica para enviar mensaje de alerta
    alert = AlertMessage(full_name=full_name, user_id=user_id, puesto_trabajo=puesto_trabajo, message=message)
    db.add(alert)
    db.commit()
    
    return {"message": "Alert message sent successfully"}

# Ruta para obtener todos los mensajes
@user_routes.get('/alert/messages')
async def get_messages(db: Session = Depends(get_db)):
    # Obtener todos los mensajes de la base de datos y ordenarlos por id_message
    messages = db.query(AlertMessage).order_by(AlertMessage.id_message).all()

    if not messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay mensajes")

    # Formatear los mensajes para la respuesta
    response = [{"user_id": message.user_id, "full_name": message.full_name, "puesto_trabajo": message.puesto_trabajo, "message": message.message} for message in messages]

    return response
