from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, table
from sqlalchemy.orm import relationship
from dataBase.db import Base

class PermisoBase(BaseModel):
    id: int
    nombre_permiso: str
    descripcion: str


class Permisos(Base):
    __tablename__ = "permisos"

    id_permiso = Column(Integer, primary_key=True, index=True)
    nombre_permiso = Column(String, unique=True)
    descripcion = Column(String)
