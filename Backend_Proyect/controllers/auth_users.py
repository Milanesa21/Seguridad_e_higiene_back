
from model.user import Users, UserCreate
from sqlalchemy.orm import Session

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not user.password == password:
        return False
    return user

def create_user(user: UserCreate, db: Session):
    hashed_password = user.password # Aca deberia ir el hash de la contraseña
    db_user = Users(username=user.username, email=user.email, disabled=user.disables, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(username: str, db: Session):
    return db.query(Users).filter(Users.username == username).first()

def delete_user(username: str, db:Session):
    user = db.query(Users).filter(Users.username == username).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    
def change_password(username: str, new_password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if user:
        user.password = new_password
        db.commit()
        db.refresh(user)
        return True
    elif user.password == new_password:
        return False
    else:
        
        return False