# Construccion_model.py
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from dataBase.db import Base
from pydantic import BaseModel
from datetime import datetime

class Construccion(Base):
    __tablename__ = "inspeccionesConstruccion"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime)
    accesoControlado = Column(Boolean)
    senalizacionAdecuada = Column(Boolean)
    pasillosDespejados = Column(Boolean)
    equiposEmergenciaDisponibles = Column(Boolean)
    cascoSeguridad = Column(Boolean)
    gafasProtectoras = Column(Boolean)
    chalecoReflectante = Column(Boolean)
    calzadoSeguridad = Column(Boolean)
    guantesTrabajo = Column(Boolean)
    maquinariaInspeccionada = Column(Boolean)
    herramientasAdecuadas = Column(Boolean)
    equiposCalibrados = Column(Boolean)
    mantenimientoRealizado = Column(Boolean)
    lineasVidaInstaladas = Column(Boolean)
    arnesesVerificados = Column(Boolean)
    barandasProteccion = Column(Boolean)
    sistemasPrevencionCaidas = Column(Boolean)
    almacenamientoAdecuado = Column(Boolean)
    etiquetasCorrectas = Column(Boolean)
    equipoManipulacionDisponible = Column(Boolean)
    ventilacionAdecuada = Column(Boolean)

    id_empresa = Column(Integer, ForeignKey("companies.id_empresa"))
    company = relationship("Company", back_populates="inspeccionesConstruccion")

class ConstruccionCreate(BaseModel):
    # Campos para crear registros
    accesoControlado: bool
    senalizacionAdecuada: bool
    pasillosDespejados: bool
    equiposEmergenciaDisponibles: bool
    cascoSeguridad: bool
    gafasProtectoras: bool
    chalecoReflectante: bool
    calzadoSeguridad: bool
    guantesTrabajo: bool
    maquinariaInspeccionada: bool
    herramientasAdecuadas: bool
    equiposCalibrados: bool
    mantenimientoRealizado: bool
    lineasVidaInstaladas: bool
    arnesesVerificados: bool
    barandasProteccion: bool
    sistemasPrevencionCaidas: bool
    almacenamientoAdecuado: bool
    etiquetasCorrectas: bool
    equipoManipulacionDisponible: bool
    ventilacionAdecuada: bool

class ConstruccionResponse(ConstruccionCreate):
    id: int
    fecha: datetime
    id_empresa: int

    class Config:
        orm_mode = True
