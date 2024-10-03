from model.user import Users
from model.permisos import Permisos
from model.user_permiso import User_Permiso
from model.schemas.user_schemas import UserCreate
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
    db_user = Users(
        full_name=user.full_name, 
        email=user.email, 
        puesto_trabajo=user.puesto_trabajo, 
        password=hashed_password, 
        id_role=user.id_role,
        id_empresa=user.id_empresa  
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Asignar permisos del rol al usuario
    if db_user.rol:
        for permiso in db_user.rol.permisos:
            user_permiso = User_Permiso(id_user=db_user.id, id_permiso=permiso.id)
            db.add(user_permiso)
        db.commit()

    return db_user


def get_user_by_id(id: int, db: Session):
    """ Trae un usuario por su id """
    try:
        user = db.query(Users).filter(Users.id == id).first()
        if not user:
            return {"detail": "User not found"}
        
        # Obtener permisos específicos asignados al usuario
        user_permisos = db.query(Permisos).join(User_Permiso).filter(User_Permiso.id_user == id).all()
        user_permisos = [permiso.nombre_permiso for permiso in user_permisos]
        
        return {
            "id": user.id,
            "full_name": user.full_name,
            "puesto_trabajo": user.puesto_trabajo,
            "email": user.email,
            "rol": {
                "id": user.rol.id if user.rol else None,
                "nombre": user.rol.nombre_rol if user.rol else None,
                "permisos": user_permisos
            },
            "id_empresa": user.id_empresa 
        }
    except Exception as e:
        return {"detail": f"Error: {e}"}


def get_all_user_by_name(full_name: str, db: Session):
    return db.query(Users).filter(Users.full_name == full_name).all()

def get_user_by_name(full_name: str, db: Session):
    return db.query(Users).filter(Users.full_name == full_name).first()

def get_user_email(email: str, db: Session):
    return db.query(Users).filter(Users.email == email).first()

def delete_user(full_name:str, email: str, puesto_trabajo: str, db: Session):
    user = db.query(Users).filter(Users.full_name == full_name, Users.email == email, Users.puesto_trabajo == puesto_trabajo).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def change_password(id: int, new_password: str, db: Session):
    user = db.query(Users).filter(Users.id == id).first()
    if user:
        user.password = hash_password(new_password)
        db.commit()
        db.refresh(user)
        return True
    return False


def change_email(id: int, email:str, new_email: str, db: Session):
    user = db.query(Users).filter(Users.id == id, Users.email == email).first()
    if user:
        user.email = new_email
        db.commit()
        db.refresh(user)
        return True
    return False


def change_job_position(full_name:str, email:str, new_position: str, db: Session):
    user = db.query(Users).filter(Users.full_name == full_name, Users.email == email).first()
    if user:
        user.puesto_trabajo = new_position
        db.commit()
        db.refresh(user)
        return True
    return False

def change_name(id: int, new_name: str, db: Session):
    user = db.query(Users).filter(Users.id == id).first()
    if user:
        user.full_name = new_name
        db.commit()
        db.refresh(user)
        return True
    return False

def get_all_users(db: Session):
    try:
        users = db.query(Users).all()
        result = []

        if not users:
            return {"message": "No users found"}
        
        for user in users:
            user_permisos = db.query(Permisos).join(User_Permiso).filter(User_Permiso.id_user == user.id).all()
            user_permisos = [permiso.nombre_permiso for permiso in user_permisos]

            result.append({
                "id": user.id,
                "full_name": user.full_name,
                "puesto_trabajo": user.puesto_trabajo,
                "email": user.email,
                "rol": {
                    "id": user.rol.id if user.rol else None,
                    "nombre": user.rol.nombre_rol if user.rol else None,
                    "permisos": user_permisos
                }
            })

        return result
    except Exception as e:
        return {"message": f"Error: {e}"}

