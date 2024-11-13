from sqlalchemy import Column, Integer, String, ForeignKey
from model.Construccion_model import Construccion
from model.Electriciad_model import Electricidad
from model.Quimica_model import Quimica
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
    id_role = Column(Integer, ForeignKey("roles.id"))

    # Relación uno a muchos con la tabla de usuarios
    users = relationship("Users", back_populates="company")

    # Relación uno a muchos con la tabla de archivos
    files = relationship("File", back_populates="company")

    # Relación uno a muchos con la tabla de agropecuario
    inspecciones_agropecuario: Mapped[List[Agropecuario]] = relationship("Agropecuario", back_populates="company")
    inspecciones_quimica: Mapped[List[Quimica]] = relationship("Quimica", back_populates="company")
    inspecciones_electricidad: Mapped[List[Electricidad]] = relationship("Electricidad", back_populates="company")
    inspecciones_construccion: Mapped[List[Construccion]] = relationship("Construccion", back_populates="company")

    rol = relationship("Rol", back_populates="companies")
