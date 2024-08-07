from dataBase.db import engine, Base
from model.user import Users
from model.empresa import Company
from model.alert_message import AlertMessage

try:
    Base.metadata.create_all(engine, checkfirst=True)
    print("Tablas creadas con éxito")
except Exception as e:
    print(f"Error al crear tablas: {e}")