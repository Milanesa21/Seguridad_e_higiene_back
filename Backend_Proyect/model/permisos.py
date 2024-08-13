from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from dataBase.db import Base

class Permisos(Base):
    __tablename__ = "permisos"

    id = Column(Integer, primary_key=True, index=True)
    nombre_permiso = Column(String, unique=True)
    descripcion = Column(String)

    roles = relationship("Rol", secondary="roles_permisos", back_populates="permisos")
    users = relationship("User_Permiso", back_populates="permiso")
