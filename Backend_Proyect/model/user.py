from pydantic import BaseModel
from dataBase.db import users_db

class User(BaseModel):
    username: str   
    full_name: str
    email: str
    disables: bool

class UserDB(User):
    password: str



def get_user_by_id(id):
    user = filter(lambda user: user.id == id,)
    try:
        return list(user)[0]
    except:
        return {"Error":"User not found"}

def creatr_user(user: User):
    if user in "users": # users es la base de datos o datos recibido por el servidor
        return {"Error":"User already exist"}

