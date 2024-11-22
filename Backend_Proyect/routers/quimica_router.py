from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dataBase.db import get_db
from model.Quimica_model import Quimica, QuimicaCreate
from datetime import datetime
from sqlalchemy import func, cast, Integer

quimica_router = APIRouter(prefix='/Quimica', tags=['Quimica'])



@quimica_router.post('/guardar_checklist')
async def guardar_checklist(
    data: QuimicaCreate,
    id_empresa: int,
    db: Session = Depends(get_db)
):
    try:
        nuevo_registro = Quimica(**data.dict(), fecha=datetime.now(), id_empresa=id_empresa)
        db.add(nuevo_registro)
        db.commit()
        db.refresh(nuevo_registro)
        return {"mensaje": "Checklist guardado exitosamente", "data": nuevo_registro}
    except Exception as e:
        print(f"Error al guardar el checklist: {e}")
        raise HTTPException(status_code=500, detail="Error al guardar el checklist")


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
            result = db.query(func.avg(cast(getattr(Quimica, campo), Integer))) \
                .filter(Quimica.id_empresa == id_empresa).scalar()
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
            promedios = db.query(*(func.avg(cast(getattr(Quimica, campo),Integer)).label(campo) for campo in campos)) \
                            .filter(Quimica.id_empresa == id_empresa) \
                            .first()
            resultados[seccion] = {campo: float(getattr(promedios, campo) or 0) for campo in campos}
        
        return resultados
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las estadísticas por sección")