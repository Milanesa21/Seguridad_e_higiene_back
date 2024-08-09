from sqlalchemy import Column, Integer, String, ForeignKey, table
from sqlalchemy.orm import relationship
from dataBase.db import Base


class Rol(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String, unique=True)
    descripcion = Column(String)