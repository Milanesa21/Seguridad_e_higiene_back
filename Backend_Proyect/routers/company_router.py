from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dataBase.db import get_db
from model.company import Company
from controllers.company_controllers import (
    create_company, 
    get_company_by_id, 
    update_company, 
    authenticate_company
)
from model.schemas.company_schemas import CompanyCreate, CompanyUpdate, CompanyResponse

company_rutes = APIRouter(prefix='/empresas', tags=['CRUD de Empresas'])

@company_rutes.post("/", response_model=CompanyResponse)
def create_new_company(company: CompanyCreate, db: Session = Depends(get_db)):
    try:
        return create_company(company, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@company_rutes.get("/{id_empresa}", response_model=CompanyResponse)
def read_company(id_empresa: int, db: Session = Depends(get_db)):
    company = get_company_by_id(id_empresa, db)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@company_rutes.put("/{id_empresa}", response_model=CompanyResponse)
def update_existing_company(id_empresa: int, company: CompanyUpdate, db: Session = Depends(get_db)):
    company = update_company(id_empresa, company, db)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found or update failed")
    return company


@company_rutes.post("/authenticate", response_model=CompanyResponse)
def authenticate_existing_company(correo_jefe: str, password: str, db: Session = Depends(get_db)):
    company = authenticate_company(correo_jefe, password, db)
    if not company:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return company
