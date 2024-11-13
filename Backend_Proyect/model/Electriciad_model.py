# Electricidad_model.py
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from dataBase.db import Base
from pydantic import BaseModel
from datetime import datetime

class Electricidad(Base):
    __tablename__ = "inspecciones Electricidad"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime)
    inspeccionEquipos = Column(Boolean)
    equiposDañados = Column(Boolean)
    etiquetadoCorrecto = Column(Boolean)
    cablesAisladosCorrectamente = Column(Boolean)
    conexionesFirmes = Column(Boolean)
    cablesDañados = Column(Boolean)
    interruptoresFuncionando = Column(Boolean)
    panelesEtiquetados = Column(Boolean)
    accesoDespejadoPaneles = Column(Boolean)
    usoEquiposProteccion = Column(Boolean)
    guantesAislantes = Column(Boolean)
    gafasProteccion = Column(Boolean)
    bloqueoEtiquetado = Column(Boolean)
    procedimientosTrabajoSeguro = Column(Boolean)
    formacionAdecuada = Column(Boolean)
    herramientasAisladas = Column(Boolean)
    herramientasEnBuenEstado = Column(Boolean)
    equipoPruebasCalibrado = Column(Boolean)

    id_empresa = Column(Integer, ForeignKey("companies.id_empresa"))
    company = relationship("Company", back_populates="inspecciones_electricidad")

class ElectricidadCreate(BaseModel):
    inspeccionEquipos: bool
    equiposDañados: bool
    etiquetadoCorrecto: bool
    cablesAisladosCorrectamente: bool
    conexionesFirmes: bool
    cablesDañados: bool
    interruptoresFuncionando: bool
    panelesEtiquetados: bool
    accesoDespejadoPaneles: bool
    usoEquiposProteccion: bool
    guantesAislantes: bool
    gafasProteccion: bool
    bloqueoEtiquetado: bool
    procedimientosTrabajoSeguro: bool
    formacionAdecuada: bool
    herramientasAisladas: bool
    herramientasEnBuenEstado: bool
    equipoPruebasCalibrado: bool

class ElectricidadResponse(ElectricidadCreate):
    id: int
    fecha: datetime
    id_empresa: int

    class Config:
        orm_mode = True
