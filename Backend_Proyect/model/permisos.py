from sqlalchemy import Column, Integer, String, ForeignKey, table
from sqlalchemy.orm import relationship
from dataBase.db import Base

class Permisos(Base):
    __tablename__ = "permisos"

    id = Column(Integer, primary_key=True, index=True)
    nombre_permiso = Column(String, unique=True)
    descripcion = Column(String)
