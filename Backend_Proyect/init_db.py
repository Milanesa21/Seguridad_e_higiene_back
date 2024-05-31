# init_db.py
from dataBase.db import engine, Base
from model.user import Users
from model.empresa import Company
from model.alert_message import AlertMessage

Base.metadata.create_all(engine)
