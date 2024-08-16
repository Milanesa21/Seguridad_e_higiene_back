from model.roles_permisos import Rol_permiso
from model.user_permiso import User_Permiso
from model.permisos import Permisos
from model.roles import Rol
from sqlalchemy.orm import Session
from model.user import Users
from model.schemas.user_schemas import UserCreate
from controllers.auth_users import create_user

def agregar_permisos_iniciales(db: Session):
    def asignar_permisos_rol_admin():
        permisos_admin = db.query(Permisos).filter(Permisos.id > 3).all()
        rol_admin = db.query(Rol).filter(Rol.id == 2).first()
        if not rol_admin:
            raise ValueError("Role admin not found")
        rol_permiso = [Rol_permiso(id_rol=rol_admin.id, id_permiso=permiso.id) for permiso in permisos_admin]
        db.add_all(rol_permiso)
        db.commit()

    def asignar_permisos_rol_security():
        permisos_security = db.query(Permisos).filter(Permisos.id >= 8).all()
        rol_security = db.query(Rol).filter(Rol.id == 3).first()
        if not rol_security:
            raise ValueError("Role security not found")
        rol_permiso = [Rol_permiso(id_rol=rol_security.id, id_permiso=permiso.id) for permiso in permisos_security]
        db.add_all(rol_permiso)
        db.commit()

    def asignar_permisos_rol_super_admin():
        permisos_super_admin = db.query(Permisos).all()
        rol_super_admin = db.query(Rol).filter(Rol.id == 1).first()
        if not rol_super_admin:
            raise ValueError("Role super_admin not found")
        rol_permiso = [Rol_permiso(id_rol=rol_super_admin.id, id_permiso=permiso.id) for permiso in permisos_super_admin]
        db.add_all(rol_permiso)
        db.commit()

    def asignar_permisos_rol_user():
        permisos_user = db.query(Permisos).filter(Permisos.id == 12).all()
        rol_user = db.query(Rol).filter(Rol.id == 4).first()
        if not rol_user:
            raise ValueError("Role user not found")
        rol_permiso = [Rol_permiso(id_rol=rol_user.id, id_permiso=permiso.id) for permiso in permisos_user]
        db.add_all(rol_permiso)
        db.commit()

    try:
        asignar_permisos_rol_admin()
        asignar_permisos_rol_security()
        asignar_permisos_rol_super_admin()
        asignar_permisos_rol_user()
    except ValueError as e:
        db.rollback()
        raise ValueError(f"Error al asignar permisos: {e}")

def agregar_permiso_al_rol(id_user: int, id_permisos: int, db: Session):
    try:
        user = db.query(Users).filter(Users.id == id_user).first()

        if not user:
            return {"detail": "User not found"}

        permiso = db.query(Permisos).filter(Permisos.id == id_permisos).first()

        if not permiso:
            return {"detail": "Permission not found"}

        # Verificar si el permiso ya está asignado al usuario
        user_permiso = db.query(User_Permiso).filter(User_Permiso.id_user == id_user, User_Permiso.id_permiso == id_permisos).first()

        if not user_permiso:
            try:
                # Asignar el permiso al usuario
                nuevo_user_permiso = User_Permiso(id_user=id_user, id_permiso=id_permisos)
                db.add(nuevo_user_permiso)
                
                # Sincronizar permisos del rol
                rol_id = user.id_role
                permisos_rol = db.query(Rol_permiso).filter(Rol_permiso.id_rol == rol_id).all()
                for rol_permiso in permisos_rol:
                    if rol_permiso.id_permiso == id_permisos:
                        db.add(nuevo_user_permiso)

                db.commit()
                return {"message": "Permission added to user successfully"}
            except Exception as e:
                db.rollback()
                print(e)
                return {'message': 'Error adding permission to user', 'status_code': 401}
        else:
            return {"message": "Permission already assigned to user"}

    except Exception as e:
        print(e)
        return {'message': 'Error adding permission to user', 'status_code': 401}



def quitar_permiso_al_rol(id_user: int, id_permisos: int, db: Session):
    try:
        # Buscar el usuario por ID
        user = db.query(Users).filter(Users.id == id_user).first()
        if not user:
            return {"detail": "User not found"}

        # Buscar el permiso por ID
        permiso = db.query(Permisos).filter(Permisos.id == id_permisos).first()
        if not permiso:
            return {"detail": "Permission not found"}

        # Buscar la asociación del permiso con el usuario
        user_permiso = db.query(User_Permiso).filter(User_Permiso.id_user == id_user, User_Permiso.id_permiso == id_permisos).first()
        if not user_permiso:
            return {"message": "Permission not assigned to user"}

        try:
            # Eliminar el permiso específico del usuario
            db.delete(user_permiso)

            # Verificar si el permiso es parte de los permisos por defecto del rol
            rol_id = user.id_role
            rol_permisos = db.query(Rol_permiso).filter(Rol_permiso.id_rol == rol_id, Rol_permiso.id_permiso == id_permisos).first()
            
            # Solo eliminar el permiso de los permisos por defecto del rol si no es el único
            if not rol_permisos:
                db.commit()
                return {"message": "Permission removed from user successfully"}
            
            db.commit()
            return {"message": "Permission removed from user successfully"}
        except Exception as e:
            db.rollback()
            print(f"Error removing permission from user: {e}")
            return {'message': 'Error removing permission from user', 'status_code': 401}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {'message': 'Unexpected error occurred', 'status_code': 500}

def get_all_permisos(db: Session):
    return db.query(Permisos).all()

def crear_super_admin(db: Session):
    user = db.query(Users).filter(Users.id_role == 1).first()
    if user:
        return {"message": "Super admin already exists"}
    try:
        user_data = {
            "full_name": 'aaaaaaaaa',
            "email": 'asdasdasda@gmail.com',
            "password": 'saaaas',
            "puesto_trabajo": 'saaaaas',
            'id_role': 1
        }
        create_user(UserCreate(**user_data), db)
    except:
        db.rollback()
        raise ValueError("Error al crear usuario")
    finally:
        db.close()
    return {"status": "success"}

