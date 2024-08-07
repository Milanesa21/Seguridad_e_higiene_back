from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from dataBase.db import Base

class Company(Base):
    __tablename__ = "companies"

    id_empresa = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_empresa = Column(String, index=True, nullable=False)
    nombre_jefe = Column(String, nullable=False)
    correo_jefe = Column(String, unique=True, index=True, nullable=False)
    numero_jefe = Column(String, nullable=False)
    password = Column(String, nullable=False)

    employees = relationship("Users", back_populates="company", cascade="all, delete-orphan")
