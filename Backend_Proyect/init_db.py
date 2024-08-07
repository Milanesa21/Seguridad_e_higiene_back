from dataBase.db import engine, Base
from model.user import Users
from model.empresa import Company
from model.alert_message import AlertMessage
from model.permisos import Permisos
from model.roles import Rol
from model.roles_permisos import Rol_permiso

Base.metadata.create_all(engine)
