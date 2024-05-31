from sqlalchemy import Column, Integer, String
from dataBase.db import Base
from sqlalchemy.orm import relationship
from dataBase.db import engine
from .user import Users


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


