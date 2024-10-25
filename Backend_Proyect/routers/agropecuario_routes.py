# routes/inspeccion_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dataBase.db import get_db
from model.Agropecuario_model import Agropecuario as Inspeccion
from model.Agropecuario_model import InspeccionCreate, InspeccionResponse
from typing import List
from datetime import datetime
from sqlalchemy import func

inspeccion_router = APIRouter(prefix='/Agropecuario', tags=['Agropecuario'])


@inspeccion_router.post('/create/', response_model=InspeccionResponse)
async def create_inspeccion(
    inspeccion: InspeccionCreate,
    id_empresa: int,
    db: Session = Depends(get_db)
):
    try:
        db_inspeccion = Inspeccion(**inspeccion.dict(), fecha=datetime.now(), id_empresa=id_empresa)
        db.add(db_inspeccion)
        db.commit()
        db.refresh(db_inspeccion)
        return db_inspeccion
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear la inspección")

@inspeccion_router.get('/list/', response_model=List[InspeccionResponse])
async def list_inspecciones(
    id_empresa: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        inspecciones = db.query(Inspeccion).filter(Inspeccion.id_empresa == id_empresa).offset(skip).limit(limit).all()
        if not inspecciones:
            raise HTTPException(status_code=404, detail="No se han encontrado inspecciones")
        return inspecciones
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las inspecciones")

@inspeccion_router.get('/{inspeccion_id}', response_model=InspeccionResponse)
async def get_inspeccion(
    inspeccion_id: int,
    db: Session = Depends(get_db)
):
    try:
        inspeccion = db.query(Inspeccion).filter(Inspeccion.id == inspeccion_id).first()
        if not inspeccion:
            raise HTTPException(status_code=404, detail="Inspección no encontrada")
        return inspeccion
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener la inspección")

@inspeccion_router.get('/estadisticas/{id_empresa}')
async def get_estadisticas(
    id_empresa: int,
    db: Session = Depends(get_db)
):
    try:
        campos = [
            'riegoAdecuado', 'controlPlagas', 'fertilizacionAdecuada', 'herramientasLimpias',
            'saludAnimal', 'alimentacionAdecuada', 'aguaSuficiente', 'instalacionesLimpias',
            'usoEquipoProteccion', 'maquinariaEnBuenEstado', 'procedimientosEmergencia',
            'productosQuimicosAlmacenados', 'maquinariaMantenida', 'equiposCalibrados',
            'herramientasAdecuadas', 'equipoSeguridadDisponible', 'gestionResiduos',
            'practicasSostenibles', 'usoAdecuadoAgua', 'energiaRenovable'
        ]
        
        estadisticas = {}
        for campo in campos:
            result = db.query(func.avg(getattr(Inspeccion, campo))).filter(Inspeccion.id_empresa == id_empresa).scalar()
            estadisticas[campo] = float(result) if result is not None else 0.0
        
        return estadisticas
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las estadísticas")

@inspeccion_router.get('/estadisticas_por_seccion/{id_empresa}')
async def get_estadisticas_por_seccion(
    id_empresa: int,
    db: Session = Depends(get_db)
):
    try:
        secciones = {
            "Manejo de cultivos": ['riegoAdecuado', 'controlPlagas', 'fertilizacionAdecuada', 'herramientasLimpias'],
            "Manejo de animales": ['saludAnimal', 'alimentacionAdecuada', 'aguaSuficiente', 'instalacionesLimpias'],
            "Seguridad en la explotación": ['usoEquipoProteccion', 'maquinariaEnBuenEstado', 'procedimientosEmergencia', 'productosQuimicosAlmacenados'],
            "Mantenimiento de maquinaria": ['maquinariaMantenida', 'equiposCalibrados', 'herramientasAdecuadas', 'equipoSeguridadDisponible'],
            "Procedimientos de sostenibilidad": ['gestionResiduos', 'practicasSostenibles', 'usoAdecuadoAgua', 'energiaRenovable']
        }
        
        resultados = {}
        for seccion, campos in secciones.items():
            promedios = db.query(*(func.avg(getattr(Inspeccion, campo)).label(campo) for campo in campos)) \
                            .filter(Inspeccion.id_empresa == id_empresa) \
                            .first()
            resultados[seccion] = {campo: float(getattr(promedios, campo) or 0) for campo in campos}
        
        return resultados
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las estadísticas por sección")