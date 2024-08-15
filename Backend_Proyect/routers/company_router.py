from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers.company_controllers import create_company, get_company_by_id, update_company, delete_company, authenticate_company
from model.schemas.company_schemas import CompanyCreate, CompanyUpdate, CompanyResponse
from dataBase.db import get_db

# Definición del APIRouter con prefijo y etiquetas
company_rutes = APIRouter(prefix='/empresas', tags=['CRUD de Empresas'])

@company_rutes.post("/registrar_empresa", response_model=CompanyResponse)
def registrar_empresa(company_data: CompanyCreate, db: Session = Depends(get_db)):
    print("Datos recibidos:", company_data.model_dump())  # Agregar para depuración
    try:
        return create_company(company_data.model_dump(), db)
    except HTTPException as e:
        print("Error al registrar empresa:", str(e))  # Agregar para depuración
        raise


@company_rutes.get("/empresa/{id_empresa}", response_model=CompanyResponse)
def obtener_empresa(id_empresa: int, db: Session = Depends(get_db)):
    company = get_company_by_id(id_empresa, db)
    if not company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada.")
    return company

@company_rutes.put("/actualizar_empresa/{id_empresa}", response_model=CompanyResponse)
def actualizar_empresa(id_empresa: int, company_data: CompanyUpdate, db: Session = Depends(get_db)):
    company = update_company(id_empresa, company_data, db)
    if not company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada.")
    return company

@company_rutes.delete("/eliminar_empresa/{id_empresa}", response_model=CompanyResponse)
def eliminar_empresa(id_empresa: int, db: Session = Depends(get_db)):
    company = delete_company(id_empresa, db)
    if not company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada.")
    return company

@company_rutes.post("/autenticar_empresa", response_model=CompanyResponse)
def autenticar_empresa(correo_jefe: str, password: str, db: Session = Depends(get_db)):
    company = authenticate_company(correo_jefe, password, db)
    if not company:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas.")
    return company
