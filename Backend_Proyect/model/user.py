from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from dataBase.db import Base
from dataBase.db import engine

class UserBase(BaseModel):
    full_name: str = Field(min_length=4,max_length=30)
    email: EmailStr
    puesto_trabajo: str = Field(min_length=3,max_length=100)

class CreateUsersRequest(BaseModel):
    puesto_trabajo: str = Field(min_length=3,max_length=100)
    num_usuarios: int = Field(ge=1)


class LoginRequest(BaseModel):
    full_name: str = Field(min_length=4,max_length=30)
    password: str 

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

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
