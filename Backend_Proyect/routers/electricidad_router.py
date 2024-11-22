from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dataBase.db import get_db
from model.Electriciad_model import Electricidad, ElectricidadCreate, ElectricidadResponse
from typing import List
from datetime import datetime
from sqlalchemy import func, cast,Integer

electricidad_router = APIRouter(prefix='/Electricidad', tags=['Electricidad'])

@electricidad_router.post('/create/', response_model=ElectricidadResponse)
async def create_inspeccion(
    inspeccion: ElectricidadCreate,
    id_empresa: int,
    db: Session = Depends(get_db)
):
    try:
        db_inspeccion = Electricidad(**inspeccion.dict(), fecha=datetime.now(), id_empresa=id_empresa)
        db.add(db_inspeccion)
        db.commit()
        db.refresh(db_inspeccion)
        return db_inspeccion
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear la inspección")

@electricidad_router.get('/list/', response_model=List[ElectricidadResponse])
async def list_inspecciones(
    id_empresa: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        inspecciones = db.query(Electricidad).filter(Electricidad.id_empresa == id_empresa).offset(skip).limit(limit).all()
        if not inspecciones:
            raise HTTPException(status_code=404, detail="No se han encontrado inspecciones")
        return inspecciones
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las inspecciones")

@electricidad_router.get('/estadisticas/{id_empresa}')
async def get_estadisticas(
    id_empresa: int,
    db: Session = Depends(get_db)
):
    try:
        campos = [
            'inspeccionEquipos', 'equiposDañados', 'etiquetadoCorrecto', 'cablesAisladosCorrectamente',
            'conexionesFirmes', 'cablesDañados', 'interruptoresFuncionando', 'panelesEtiquetados',
            'accesoDespejadoPaneles', 'usoEquiposProteccion', 'guantesAislantes', 'gafasProteccion',
            'bloqueoEtiquetado', 'procedimientosTrabajoSeguro', 'formacionAdecuada', 'herramientasAisladas',
            'herramientasEnBuenEstado', 'equipoPruebasCalibrado'
        ]
        
        estadisticas = {}
        for campo in campos:
            result = db.query(func.avg(cast(getattr(Electricidad, campo),Integer))).filter(Electricidad.id_empresa == id_empresa).scalar()
            estadisticas[campo] = float(result) if result is not None else 0.0
        
        return estadisticas
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las estadísticas")

@electricidad_router.get('/estadisticas_por_seccion/{id_empresa}')
async def get_estadisticas_por_seccion(
    id_empresa: int,
    db: Session = Depends(get_db)
):
    try:
        secciones = {
            "Equipos eléctricos": ['inspeccionEquipos', 'equiposDañados', 'etiquetadoCorrecto'],
            "Cables y conexiones": ['cablesAisladosCorrectamente', 'conexionesFirmes', 'cablesDañados'],
            "Interruptores y paneles": ['interruptoresFuncionando', 'panelesEtiquetados', 'accesoDespejadoPaneles'],
            "Protección personal": ['usoEquiposProteccion', 'guantesAislantes', 'gafasProteccion'],
            "Procedimientos de trabajo": ['bloqueoEtiquetado', 'procedimientosTrabajoSeguro', 'formacionAdecuada'],
            "Herramientas y equipos de prueba": ['herramientasAisladas', 'herramientasEnBuenEstado', 'equipoPruebasCalibrado']
        }
        
        resultados = {}
        for seccion, campos in secciones.items():
            promedios = db.query(*(func.avg(cast(getattr(Electricidad, campo),Integer)).label(campo) for campo in campos)) \
                            .filter(Electricidad.id_empresa == id_empresa) \
                            .first()
            resultados[seccion] = {campo: float(getattr(promedios, campo) or 0) for campo in campos}
        
        return resultados
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las estadísticas por sección")
