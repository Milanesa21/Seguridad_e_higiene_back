
from model.user import Users, UserCreate
from sqlalchemy.orm import Session

def authenticate_user(full_name: str, password: str, db: Session):
    user = db.query(Users).filter(Users.full_name == full_name).first()
    if not user:
        return False
    if not user.password == password:
        return False
    return user

def create_user(user: UserCreate, db: Session):
    hashed_password = user.password # Aca deberia ir el hash de la contraseña
    db_user = Users(full_name=user.full_name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(full_name: str, db: Session):
    return db.query(Users).filter(Users.full_name == full_name).first()

def delete_user(full_name: str, db:Session):
    user = db.query(Users).filter(Users.full_name == full_name).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    
def change_password(full_name: str, new_password: str, db: Session):
    user = db.query(Users).filter(Users.full_name == full_name).first()
    if user:
        user.password = new_password
        db.commit()
        db.refresh(user)
        return True
    elif user.password == new_password:
        return False
    else:
        
        return False