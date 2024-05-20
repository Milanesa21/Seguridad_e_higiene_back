from model.user import Users, UserCreate
from sqlalchemy.orm import Session
from controllers.password_hasheado import hash_password, verify_password

def authenticate_user(full_name: str, password: str, db: Session):
    user = db.query(Users).filter(Users.full_name == full_name).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_user(user: UserCreate, db: Session):
    hashed_password = hash_password(user.password)
    db_user = Users(full_name=user.full_name, email=user.email,puesto_trabajo=user.puesto_trabajo ,password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_name(full_name: str, db: Session):
    return db.query(Users).filter(Users.full_name == full_name).first()

def get_user_email(email: str, db: Session):
    return db.query(Users).filter(Users.email == email).first()

def delete_user(full_name: str, db: Session):
    user = db.query(Users).filter(Users.full_name == full_name).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def change_password(full_name: str, new_password: str, db: Session):
    user = db.query(Users).filter(Users.full_name == full_name).first()
    if user:
        user.password = hash_password(new_password)
        db.commit()
        db.refresh(user)
        return True
    return False


def change_job_position(full_name: str, new_position: str, db: Session):
    user = db.query(Users).filter(Users.full_name == full_name).first()
    if user:
        user.puesto_trabajo = new_position
        db.commit()
        db.refresh(user)
        return True
    return False

def change_name(full_name: str, new_name: str, db: Session):
    user = db.query(Users).filter(Users.full_name == full_name).first()
    if user:
        user.full_name = new_name
        db.commit()
        db.refresh(user)
        return True
    return False

