# quimica_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dataBase.db import get_db
from model.Quimica_model import Quimica, QuimicaCreate, QuimicaResponse
from typing import List
from datetime import datetime
from sqlalchemy import func

quimica_router = APIRouter(prefix='/Quimica', tags=['Quimica'])



@quimica_router.post('/create/', response_model=QuimicaResponse)
async def create_inspeccion(
    checklist_data: dict,
    id_empresa: int,
    db: Session = Depends(get_db)
):
    try:
        db_inspeccion = Quimica(**checklist_data, fecha=datetime.now(), id_empresa=id_empresa)
        db.add(db_inspeccion)
        db.commit()
        db.refresh(db_inspeccion)
        return db_inspeccion
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear la inspección")


@quimica_router.get('/estadisticas/{id_empresa}')
async def get_estadisticas(
    id_empresa: int,
    db: Session = Depends(get_db)
):
    try:
        campos = [
            'usoBataLaboratorio', 'usoGafasProteccion', 'usoGuantesAdecuados', 'usoMascarilla',
            'productosEtiquetados', 'productosSeguros', 'almacenamientoCompatible', 'ventilacionAdecuada',
            'procedimientosSeguidos', 'derramesControlados', 'registroProductos', 'equipoEmergenciaAccesible',
            'campanaFuncionando', 'equipoLimpio', 'vidrioNoDañado', 'equiposCalibrados',
            'residuosEtiquetados', 'residuosAlmacenadosCorrectamente', 'residuosEliminadosFrecuentemente', 'procedimientosEliminacionCorrectos'
        ]
        
        estadisticas = {}
        for campo in campos:
            result = db.query(func.avg(getattr(Quimica, campo))).filter(Quimica.id_empresa == id_empresa).scalar()
            estadisticas[campo] = float(result) if result is not None else 0.0
        
        return estadisticas
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las estadísticas")

@quimica_router.get('/estadisticas_por_seccion/{id_empresa}')
async def get_estadisticas_por_seccion(
    id_empresa: int,
    db: Session = Depends(get_db)
):
    try:
        secciones = {
            "Equipos de protección personal": ['usoBataLaboratorio', 'usoGafasProteccion', 'usoGuantesAdecuados', 'usoMascarilla'],
            "Almacenamiento de productos químicos": ['productosEtiquetados', 'productosSeguros', 'almacenamientoCompatible', 'ventilacionAdecuada'],
            "Procedimientos de manejo de productos químicos": ['procedimientosSeguidos', 'derramesControlados', 'registroProductos', 'equipoEmergenciaAccesible'],
            "Estado del equipo de laboratorio": ['campanaFuncionando', 'equipoLimpio', 'vidrioNoDañado', 'equiposCalibrados'],
            "Eliminación de residuos químicos": ['residuosEtiquetados', 'residuosAlmacenadosCorrectamente', 'residuosEliminadosFrecuentemente', 'procedimientosEliminacionCorrectos']
        }
        
        resultados = {}
        for seccion, campos in secciones.items():
            promedios = db.query(*(func.avg(getattr(Quimica, campo)).label(campo) for campo in campos)) \
                            .filter(Quimica.id_empresa == id_empresa) \
                            .first()
            resultados[seccion] = {campo: float(getattr(promedios, campo) or 0) for campo in campos}
        
        return resultados
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las estadísticas por sección")
