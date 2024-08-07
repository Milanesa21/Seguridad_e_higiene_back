from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from model.company import Company
from controllers.password_hasheado import hash_password, verify_password
from model.schemas.company_schemas import CompanyCreate, CompanyUpdate, CompanyResponse

def create_company(company_data: CompanyCreate, db: Session) -> CompanyResponse:
    existing_company = db.query(Company).filter(Company.correo_jefe == company_data.correo_jefe).first()
    if existing_company:
        raise ValueError("Ya existe una empresa con el correo electrónico proporcionado.")
    
    hashed_password = hash_password(company_data.password)
    
    db_company = Company(
        nombre_empresa=company_data.nombre_empresa,
        nombre_jefe=company_data.nombre_jefe,
        correo_jefe=company_data.correo_jefe,
        numero_jefe=company_data.numero_jefe,
        password=hashed_password
    )
    
    try:
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        return CompanyResponse.from_orm(db_company)
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Error al crear la empresa en la base de datos.") from e

def get_company_by_id(id_empresa: int, db: Session) -> CompanyResponse:
    db_company = db.query(Company).filter(Company.id_empresa == id_empresa).first()
    if not db_company:
        return None
    return CompanyResponse.from_orm(db_company)

def update_company(id_empresa: int, company_data: CompanyUpdate, db: Session) -> CompanyResponse:
    db_company = db.query(Company).filter(Company.id_empresa == id_empresa).first()
    if not db_company:
        return None
    
    if company_data.nombre_empresa:
        db_company.nombre_empresa = company_data.nombre_empresa
    if company_data.nombre_jefe:
        db_company.nombre_jefe = company_data.nombre_jefe
    if company_data.correo_jefe:
        db_company.correo_jefe = company_data.correo_jefe
    if company_data.numero_jefe:
        db_company.numero_jefe = company_data.numero_jefe
    if company_data.password:
        db_company.password = hash_password(company_data.password)
    
    db.commit()
    db.refresh(db_company)
    return CompanyResponse.from_orm(db_company)



def authenticate_company(correo_jefe: str, password: str, db: Session) -> CompanyResponse:
    db_company = db.query(Company).filter(Company.correo_jefe == correo_jefe).first()
    if db_company and verify_password(password, db_company.password):
        return CompanyResponse.from_orm(db_company)
    return None
