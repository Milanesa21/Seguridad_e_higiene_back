from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from controllers.company_controllers import create_company, get_company_by_id, update_company, delete_company, authenticate_company, get_companies
from controllers.auth_users import get_user_by_id
from model.schemas.company_schemas import CompanyBase, CompanyCreate, CompanyRequest, CompanyUpdate, CompanyResponse
from dataBase.db import get_db
from services.jwt import write_token

# Definición del APIRouter con prefijo y etiquetas
company_rutes = APIRouter(prefix='/empresas', tags=['CRUD de Empresas'])

@company_rutes.post("/registrar_empresa", response_model=CompanyResponse)
def registrar_empresa(company_data: CompanyCreate, db: Session = Depends(get_db)):
    print("Datos recibidos:", company_data.model_dump())  # Agregar para depuración
    if company_data.id_superuser is None:
        raise HTTPException(status_code=400, detail="Permisos es requerido.")
    if company_data.id_superuser:
        user = get_user_by_id(company_data.id_superuser, db)
        if user is None:
            raise HTTPException(status_code=400, detail="Usuario no encontrado.")
        if user['rol']['nombre'] != "super_admin":
            raise HTTPException(status_code=400, detail="El usuario no tiene autorizacion para registrar")
        if user['rol']['permisos'][0] != "crear_empresa":
            raise HTTPException(status_code=400, detail="El usuario no tiene permisos para registrar")
    try:
        return create_company(company_data.model_dump(), db)
    except HTTPException as e:
        print("Error al registrar empresa:", str(e))  # Agregar para depuración
        raise


@company_rutes.get("/empresa/{id}", response_model=CompanyResponse)
def obtener_empresa(id_empresa: int, db: Session = Depends(get_db)):
    company = get_company_by_id(id_empresa, db)
    if not company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada.")
    return company

@company_rutes.put("/actualizar_empresa/{id}", response_model=CompanyResponse)
def actualizar_empresa(id_empresa: int, company_data: CompanyUpdate, db: Session = Depends(get_db)):
    company = update_company(id_empresa, company_data, db)
    if not company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada.")
    return company

@company_rutes.delete("/eliminar_empresa/{id}", response_model=CompanyResponse)
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


@company_rutes.post('/login')
async def login_company(login_request: CompanyRequest, db: Session = Depends(get_db)):
    nombre_empresa = login_request.nombre_empresa
    password = login_request.password
    company = authenticate_company(nombre_empresa, password, db)
    print(company)

    if not company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    company_data = {
        "id": company.id_empresa,
    }

    # Generar un token JWT y devolverlo en la respuesta
    token = write_token(company_data)
    return token

@company_rutes.get('/all')
def get_companies_rutes(db: Session = Depends(get_db)):
    return get_companies(db)