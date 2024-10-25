# Quimica_model.py
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from dataBase.db import Base
from pydantic import BaseModel
from datetime import datetime

class Quimica(Base):
    __tablename__ = "inspeccionesQuimica"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime)
    usoBataLaboratorio = Column(Boolean)
    usoGafasProteccion = Column(Boolean)
    usoGuantesAdecuados = Column(Boolean)
    usoMascarilla = Column(Boolean)
    productosEtiquetados = Column(Boolean)
    productosSeguros = Column(Boolean)
    almacenamientoCompatible = Column(Boolean)
    ventilacionAdecuada = Column(Boolean)
    procedimientosSeguidos = Column(Boolean)
    derramesControlados = Column(Boolean)
    registroProductos = Column(Boolean)
    equipoEmergenciaAccesible = Column(Boolean)
    campanaFuncionando = Column(Boolean)
    equipoLimpio = Column(Boolean)
    vidrioNoDañado = Column(Boolean)
    equiposCalibrados = Column(Boolean)
    residuosEtiquetados = Column(Boolean)
    residuosAlmacenadosCorrectamente = Column(Boolean)
    residuosEliminadosFrecuentemente = Column(Boolean)
    procedimientosEliminacionCorrectos = Column(Boolean)

    id_empresa = Column(Integer, ForeignKey("companies.id_empresa"))
    company = relationship("Company", back_populates="inspeccionesQuimica")

class QuimicaCreate(BaseModel):
    usoBataLaboratorio: bool
    usoGafasProteccion: bool
    usoGuantesAdecuados: bool
    usoMascarilla: bool
    productosEtiquetados: bool
    productosSeguros: bool
    almacenamientoCompatible: bool
    ventilacionAdecuada: bool
    procedimientosSeguidos: bool
    derramesControlados: bool
    registroProductos: bool
    equipoEmergenciaAccesible: bool
    campanaFuncionando: bool
    equipoLimpio: bool
    vidrioNoDañado: bool
    equiposCalibrados: bool
    residuosEtiquetados: bool
    residuosAlmacenadosCorrectamente: bool
    residuosEliminadosFrecuentemente: bool
    procedimientosEliminacionCorrectos: bool

class QuimicaResponse(QuimicaCreate):
    id: int
    fecha: datetime
    id_empresa: int

    class Config:
        orm_mode = True
