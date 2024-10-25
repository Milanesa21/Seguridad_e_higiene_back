from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from dataBase.db import Base
from pydantic import BaseModel
from datetime import datetime

class Agropecuario(Base):
    __tablename__ = "inspecciones Agropecuario"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime)
    riegoAdecuado = Column(Boolean)
    controlPlagas = Column(Boolean)
    fertilizacionAdecuada = Column(Boolean)
    herramientasLimpias = Column(Boolean)
    saludAnimal = Column(Boolean)
    alimentacionAdecuada = Column(Boolean)
    aguaSuficiente = Column(Boolean)
    instalacionesLimpias = Column(Boolean)
    usoEquipoProteccion = Column(Boolean)
    maquinariaEnBuenEstado = Column(Boolean)
    procedimientosEmergencia = Column(Boolean)
    productosQuimicosAlmacenados = Column(Boolean)
    maquinariaMantenida = Column(Boolean)
    equiposCalibrados = Column(Boolean)
    herramientasAdecuadas = Column(Boolean)
    equipoSeguridadDisponible = Column(Boolean)
    gestionResiduos = Column(Boolean)
    practicasSostenibles = Column(Boolean)
    usoAdecuadoAgua = Column(Boolean)
    energiaRenovable = Column(Boolean)

    # Clave foránea para la relación con la tabla de empresas
    id_empresa = Column(Integer, ForeignKey("companies.id_empresa"))


# Relación uno a muchos con la tabla de empresas
    company = relationship("Company", back_populates="inspecciones")

class InspeccionCreate(BaseModel):
    riegoAdecuado: bool
    controlPlagas: bool
    fertilizacionAdecuada: bool
    herramientasLimpias: bool
    saludAnimal: bool
    alimentacionAdecuada: bool
    aguaSuficiente: bool
    instalacionesLimpias: bool
    usoEquipoProteccion: bool
    maquinariaEnBuenEstado: bool
    procedimientosEmergencia: bool
    productosQuimicosAlmacenados: bool
    maquinariaMantenida: bool
    equiposCalibrados: bool
    herramientasAdecuadas: bool
    equipoSeguridadDisponible: bool
    gestionResiduos: bool
    practicasSostenibles: bool
    usoAdecuadoAgua: bool
    energiaRenovable: bool

class InspeccionResponse(InspeccionCreate):
    id: int
    fecha: datetime
    id_empresa: int

    class Config:
        orm_mode = True
