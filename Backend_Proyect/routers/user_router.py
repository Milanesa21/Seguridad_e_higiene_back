from controllers.auth_users import create_user, authenticate_user, get_all_user_by_name, delete_user, change_password, change_job_position, get_user_email, change_name, get_user_by_name
from services.jwt import write_token
from services.email_service import send_email
from sqlalchemy.orm import Session
from dataBase.db import get_db
from model.schemas.user_schemas import UserCreate, CreateUsersRequest, LoginRequest
from model.alert_message import AlertMessage
from model.schemas.alert_message_schemas import AlertMessageRequest
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
import random
from services.Jorgito import app as jorgito_app  # Importa la aplicación de Jorgito
from services.middleware_verification import get_user_info_by_id
from controllers.rol_permiso_controllers import agregar_permiso_al_rol, quitar_permiso_al_rol
from controllers.socket_controllers import manager


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
            "puesto_trabajo": request.puesto_trabajo,
            'id_role': 4
        }
        if user_data['puesto_trabajo'] == 'Area de seguridad':
            user_data['id_role'] = 3
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
        "id": user.id,
    }

    # Generar un token JWT y devolverlo en la respuesta
    token = write_token(user_data)
    return token


# Ruta para obtener un usuario por su id
@user_rutes.get('/user/id/{id}')
async def get_user_id(id: int, db: Session = Depends(get_db)):
    """ trae un usuario por su id """
    user = get_user_info_by_id(id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message":"Usuario encontrado","Usuario":user}


# Ruta para obtener un usuario por su nombre
@user_rutes.get('/user/name/{full_name}')
async def get_user_by_full_name(full_name: str, db: Session = Depends(get_db)):
    user = get_user_by_name(full_name, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message":"Usuario encontrado","Usuario":user}

# Ruta para obtener todos los usuarios por su nombre
@user_rutes.get('/user/all/{full_name}')
async def get_all_user_by_full_name(full_name: str, db: Session = Depends(get_db)):
    users = get_all_user_by_name(full_name, db)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return {"message":"Usuarios encontrados","Usuarios":users}


#Ruta para obtener un usuario por su email
@user_rutes.get('/user/email/{email}')
async def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = get_user_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message":"Usuario encontrado","Usuario":user}

# Ruta para eliminar un usuario
@user_rutes.delete('/user/delete/{full_name}')
async def delete_user_route(full_name: str, email: str, puesto_trabajo: str, db: Session = Depends(get_db)):
    deleted = delete_user(full_name, email, puesto_trabajo, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Usuario eliminado exitosamente"}

#eviar correo para cambiar contraseña
@user_rutes.post('/user/sendEmail/{full_name}')
async def send_email_route(full_name: str, db: Session = Depends(get_db)):
    user = get_user_by_name(full_name, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    send_email(full_name, user.email)

# Ruta para cambiar la contraseña de un usuario
@user_rutes.patch('/user/changePassword/{full_name}')
async def change_password_route(full_name: str, email: str, new_password: str, db: Session = Depends(get_db)):
    changed = change_password(full_name, email, new_password, db)
    if not changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Contraseña cambiada exitosamente"}
    

# Ruta para cambiar el puesto de trabajo de un usuario
@user_rutes.patch('/user/changeJobPosition/{full_name}')
async def change_job_position_route(full_name: str, email: str, new_position: str, db: Session = Depends(get_db)):
    changed = change_job_position(full_name, email, new_position, db)
    if not changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Puesto de trabajo cambiado exitosamente"}

# Ruta para cambiar el nombre de un usuario
@user_rutes.patch('/user/changeName/{full_name}')
async def change_name_route(full_name: str, new_name: str, db: Session = Depends(get_db)):
    changed = change_name(full_name, new_name, db)
    if not changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "El nombre de usuario fue correctamente cambiado"}


# Ruta para enviar un mensaje
@user_rutes.post('/alert/sendMessage')
async def send_message(alert_message: AlertMessageRequest, db: Session = Depends(get_db)):
    full_name = alert_message.full_name
    user_id = alert_message.user_id
    puesto_trabajo = alert_message.puesto_trabajo
    message = alert_message.message

    # Verificar si el mensaje está vacío o es None y asignar el mensaje predeterminado si es necesario
    if not message:
        message = "¡Emergencia! Necesito asistencia."
    
    print(full_name, user_id, puesto_trabajo, message)
    
    # Crear una instancia de AlertMessage y guardarla en la base de datos
    alert_message_instance = AlertMessage(user_id=user_id, full_name=full_name, puesto_trabajo=puesto_trabajo, message=message)
    db.add(alert_message_instance)
    db.commit()

    # Enviar mensaje a todos los clientes conectados a través del WebSocket
    message_data = {"user_id": user_id, "full_name": full_name, "puesto_trabajo": puesto_trabajo, "message": message}
    await manager.broadcast(message_data)

    return {"message": f"Mensaje enviado de {full_name} en el puesto de trabajo {puesto_trabajo}: {message}"}



# Ruta para obtener todos los mensajes
@user_rutes.get('/alert/messages')
async def get_messages(db: Session = Depends(get_db)):
    # Obtener todos los mensajes de la base de datos y ordenarlos por id_message
    messages = db.query(AlertMessage).order_by(AlertMessage.id_message).all()

    if not messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay mensajes")

    # Formatear los mensajes para la respuesta
    response = [{"user_id": message.user_id, "full_name": message.full_name, "puesto_trabajo": message.puesto_trabajo, "message": message.message} for message in messages]
    
    return response

@user_rutes.post('/role/addPermission')
async def add_permissions_to_role(id_user: int, id_permiso: int, db: Session = Depends(get_db)):
    return agregar_permiso_al_rol(id_user, id_permiso, db)

@user_rutes.delete('/role/removePermission')
async def remove_permission_from_role(id_user: int, id_permiso: int, db: Session = Depends(get_db)):
    return quitar_permiso_al_rol(id_user, id_permiso, db)



# Incluir las rutas de Jorgito en el router principal
main_app = FastAPI()
main_app.include_router(user_rutes)  # Incluir las rutas de usuario
main_app.mount("/Jorgito", jorgito_app)  # Montar la aplicación de Jorgito
