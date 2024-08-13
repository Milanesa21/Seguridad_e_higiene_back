from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from dataBase.db import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    puesto_trabajo = Column(String)
    password = Column(String)

    # Relación uno a muchos con la tabla de roles
    id_role = Column(Integer, ForeignKey("roles.id"))
    rol = relationship("Rol", back_populates="users")
    # Relación uno a muchos con la tabla de mensajes de alerta
    alert_messages = relationship("AlertMessage", back_populates="user")

    # Relación muchos a muchos con la tabla de permisos
    user_permisos = relationship("User_Permiso", back_populates="user")

    def change_password(self, new_password: str):
        self.password = new_password
