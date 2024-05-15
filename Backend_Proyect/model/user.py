from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from dataBase.db import Base
from dataBase.db import engine


class UserBase(BaseModel):
    full_name: str   
    email: str
    puesto_trabajo: str


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class DBUser(User):
    password: str

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    puesto_trabajo = Column(String)
    password = Column(String)
    
    # Relación uno a muchos con la tabla de mensajes de alerta
    alert_messages = relationship("AlertMessage", back_populates="user")


    def change_password(self, new_password: str):
        self.password = new_password

class AlertMessage(Base):
    __tablename__ = "alert_messages"

    id_message = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    full_name= Column(String) 
    puesto_trabajo= Column(String)
    message = Column(String)
    
    # Relación con la tabla de usuarios
    user = relationship("Users", back_populates="alert_messages")


Base.metadata.create_all(engine)


