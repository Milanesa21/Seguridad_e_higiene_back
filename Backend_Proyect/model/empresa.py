from sqlalchemy import Column, Integer, String
from dataBase.db import Base
from sqlalchemy.orm import relationship
from dataBase.db import engine
from pydantic import BaseModel

class CompanyBase(BaseModel):
    nombre_empresa: str
    nombre_representante: str
    correo_representante: str
    numero_representante: str

class CompanyCreate(CompanyBase):
    password: str

class Company(CompanyBase):
    id_empresa: int

    class Config:
        orm_mode = True

class Company(Base):
    __tablename__ = "companies"

    id_empresa = Column(Integer, primary_key=True, index=True)
    nombre_empresa = Column(String, index=True)
    nombre_representante = Column(String)
    correo_representante = Column(String, unique=True, index=True)
    numero_representante = Column(String)
    password = Column(String)

    # Relación uno a muchos con usuarios (empleados)
    employees = relationship("Users", back_populates="company")


