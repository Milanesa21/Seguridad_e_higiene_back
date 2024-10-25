# construccion_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dataBase.db import get_db
from model.Construccion_model import Construccion, ConstruccionCreate, ConstruccionResponse
from typing import List
from datetime import datetime
from sqlalchemy import func

construccion_router = APIRouter(prefix='/Construccion', tags=['Construccion'])

@construccion_router.get('/estadisticas/{id_empresa}')
async def get_estadisticas(
    id_empresa: int,
    db: Session = Depends(get_db)
):
    try:
        campos = [
            'accesoControlado', 'senalizacionAdecuada', 'pasillosDespejados', 'equiposEmergenciaDisponibles',
            'cascoSeguridad', 'gafasProtectoras', 'chalecoReflectante', 'calzadoSeguridad', 'guantesTrabajo',
            'maquinariaInspeccionada', 'herramientasAdecuadas', 'equiposCalibrados', 'mantenimientoRealizado',
            'lineasVidaInstaladas', 'arnesesVerificados', 'barandasProteccion', 'sistemasPrevencionCaidas',
            'almacenamientoAdecuado', 'etiquetasCorrectas', 'equipoManipulacionDisponible', 'ventilacionAdecuada'
        ]
        
        estadisticas = {}
        for campo in campos:
            result = db.query(func.avg(getattr(Construccion, campo))).filter(Construccion.id_empresa == id_empresa).scalar()
            estadisticas[campo] = float(result) if result is not None else 0.0
        
        return estadisticas
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las estadísticas")

@construccion_router.get('/estadisticas_por_seccion/{id_empresa}')
async def get_estadisticas_por_seccion(
    id_empresa: int,
    db: Session = Depends(get_db)
):
    try:
        secciones = {
            "Seguridad en el sitio de construcción": ['accesoControlado', 'senalizacionAdecuada', 'pasillosDespejados', 'equiposEmergenciaDisponibles'],
            "Uso de equipo de protección personal (EPP)": ['cascoSeguridad', 'gafasProtectoras', 'chalecoReflectante', 'calzadoSeguridad', 'guantesTrabajo'],
            "Maquinaria y herramientas": ['maquinariaInspeccionada', 'herramientasAdecuadas', 'equiposCalibrados', 'mantenimientoRealizado'],
            "Procedimientos de trabajo en altura": ['lineasVidaInstaladas', 'arnesesVerificados', 'barandasProteccion', 'sistemasPrevencionCaidas'],
            "Manejo de materiales peligrosos": ['almacenamientoAdecuado', 'etiquetasCorrectas', 'equipoManipulacionDisponible', 'ventilacionAdecuada']
        }
        
        resultados = {}
        for seccion, campos in secciones.items():
            promedios = db.query(*(func.avg(getattr(Construccion, campo)).label(campo) for campo in campos)) \
                            .filter(Construccion.id_empresa == id_empresa) \
                            .first()
            resultados[seccion] = {campo: float(getattr(promedios, campo) or 0) for campo in campos}
        
        return resultados
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener las estadísticas por sección")
