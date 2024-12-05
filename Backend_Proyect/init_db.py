from dataBase.db import engine, Base
from model.user import Users
from model.company import Company
from model.alert_message import AlertMessage
from model.permisos import Permisos
from model.roles import Rol
from model.roles_permisos import Rol_permiso
from model.user_permiso import User_Permiso
from model.cloudinary_model import File
from model.email_recuperacion_model import Token
from model.task import Task

try:
    Base.metadata.create_all(engine, checkfirst=True)
    print("Tablas creadas con éxito")
except Exception as e:
    print(f"Error al crear tablas: {e}")