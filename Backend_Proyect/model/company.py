from sqlalchemy import Column, Integer, String
from .Agropecuario_model import Agropecuario
from dataBase.db import Base
from sqlalchemy.orm import relationship, Mapped
from typing import List

class Company(Base):
    __tablename__ = "companies"

    id_empresa = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_empresa = Column(String, index=True, nullable=False)
    nombre_jefe = Column(String, nullable=False)
    correo_jefe = Column(String, unique=True, index=True, nullable=False)
    numero_jefe = Column(String, nullable=False)
    password = Column(String, nullable=False)

    # Relación uno a muchos con la tabla de usuarios
    users = relationship("Users", back_populates="company")

    # Relación uno a muchos con la tabla de archivos
    files = relationship("File", back_populates="company")

    # Relación uno a muchos con la tabla de agropecuario
    inspecciones: Mapped[List[Agropecuario]] = relationship("Agropecuario", back_populates="company")
