from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from model.company import Company
from controllers.password_hasheado import hash_password, verify_password
from model.schemas.company_schemas import CompanyUpdate, CompanyResponse
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

def create_company(company_data: dict, db: Session):
    try:
        hashed_password = hash_password(company_data.get('password', ''))

        existing_company = db.query(Company).filter(Company.correo_jefe == company_data['correo_jefe']).first()

        if existing_company:
            raise HTTPException(status_code=400, detail="La empresa ya está registrada")

        new_company = Company(
            nombre_empresa=company_data['nombre_empresa'],
            nombre_jefe=company_data['nombre_jefe'],
            correo_jefe=company_data['correo_jefe'],
            numero_jefe=company_data['numero_jefe'],
            password=hashed_password
        )
        
        if 'id_empresa' in company_data and company_data['id_empresa'] is not None:
            new_company.id_empresa = company_data['id_empresa']

        db.add(new_company)
        db.commit()
        db.refresh(new_company)
        return new_company

    except IntegrityError:
        db.rollback()  # Rollback the transaction in case of error
        raise HTTPException(status_code=400, detail="Error de integridad al registrar la empresa.")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al registrar la empresa.")


def crear_empresa_inicial(db: Session):
    db_company = db.query(Company).filter(Company.id_empresa == 0).first()
    if db_company:
        return None
    try:
        company_data = {
            'id_empresa': 0,
            'nombre_empresa': 'CJ_LibertyCity',
            'nombre_jefe': 'Carl Johnson',
            'correo_jefe': 'CJ_GroveStreet@gmail.com',
            'numero_jefe': '555-1234',
            'password': 'GTA_SanAndreas'
        }
        create_company(company_data, db)
    except Exception as e:
        print(f"Error al crear empresa inicial: {e}")
        return None

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


def delete_company(id_empresa: int, db: Session) -> CompanyResponse:
    db_company = db.query(Company).filter(Company.id_empresa == id_empresa).first()
    if not db_company:
        return None
    db.delete(db_company)
    db.commit()
    return CompanyResponse.from_orm(db_company)


def authenticate_company(nombre_empresa: str, password: str, db: Session) -> CompanyResponse:
    db_company = db.query(Company).filter(Company.nombre_empresa == nombre_empresa).first()
    print(db_company)
    if db_company and verify_password(password, db_company.password):
        return CompanyResponse.from_orm(db_company)
    return None

def get_companies(db: Session):
    return db.query(Company).all()