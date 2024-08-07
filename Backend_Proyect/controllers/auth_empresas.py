from model.empresa import CompanyCreate, Company, CompanyBase
from sqlalchemy.orm import Session
from controllers.password_hasheado import hash_password, verify_password

def authenticate_company(nombre_empresa: str, password: str, db: Session):
    company = db.query(Company).filter(Company.nombre_empresa == nombre_empresa).first()
    if not company:
        return False
    if not verify_password(password, company.password):
        return False
    return company