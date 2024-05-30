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
    id_empresa: int  # Agregamos id_empresa al modelo de usuario
    class Config:
        from_attributes = True

class DBUser(User):
    password: str

class Company(Base):
    __tablename__ = "companies"

    id_empresa = Column(Integer, primary_key=True, index=True)
    nombre_empresa = Column(String, index=True)
    nombre_jefe = Column(String)
    correo_jefe = Column(String, unique=True, index=True)
    numero_jefe = Column(String)
    password = Column(String)

    # Relación uno a muchos con usuarios (empleados)
    employees = relationship("Users", back_populates="company")

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    id_empresa = Column(Integer, ForeignKey('companies.id_empresa'))  # Relación con la tabla de empresas
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    puesto_trabajo = Column(String)
    password = Column(String)
    
    # Relación uno a muchos con la tabla de mensajes de alerta
    alert_messages = relationship("AlertMessage", back_populates="user")

    # Relación con la tabla de empresas
    company = relationship("Company", back_populates="employees")

    def change_password(self, new_password: str):
        self.password = new_password

class AlertMessage(Base):
    __tablename__ = "alert_messages"

    id_message = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    full_name = Column(String) 
    puesto_trabajo = Column(String)
    message = Column(String)
    
    # Relación con la tabla de usuarios
    user = relationship("Users", back_populates="alert_messages")

Base.metadata.create_all(engine)
