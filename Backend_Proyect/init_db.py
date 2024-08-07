from dataBase.db import engine, Base
from model.user import Users
from model.company import Company
from model.alert_message import AlertMessage
from model.permisos import Permisos
from model.roles import Rol
from model.roles_permisos import Rol_permiso

try:
    Base.metadata.create_all(engine, checkfirst=True)
    print("Tablas creadas con éxito")
except Exception as e:
    print(f"Error al crear tablas: {e}")