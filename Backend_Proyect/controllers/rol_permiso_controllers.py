from model.roles_permisos import Rol_permiso
from model.permisos import Permisos
from model.roles import Rol
from sqlalchemy.orm import Session
from model.user import Users

def agregar_permiso_a_rol(db: Session):
    def admin_RP(db: Session):
        permisos_admin = db.query(Permisos).filter(Permisos.id < 3).all()
        rol_admin = db.query(Rol).filter(Rol.id == 2).first()

        try:
            rol_permiso = [
                Rol_permiso(id_rol=rol_admin.id, id_permiso=permiso.id)
                for permiso in permisos_admin
            ]
            db.add_all(rol_permiso)
            db.commit()
        except:
            db.rollback()
            raise ValueError("Error al asignar permisos al rol admin")

    def segurity_RP(db: Session):
        permisos_segurity = db.query(Permisos).filter(Permisos.id >= 8).all()
        rol_segurity = db.query(Rol).filter(Rol.id == 3).first()

        try:
            rol_permiso = [
                Rol_permiso(id_rol=rol_segurity.id, id_permiso=permiso.id)
                for permiso in permisos_segurity
            ]
            db.add_all(rol_permiso)
            db.commit()
        except:
            db.rollback()
            raise ValueError("Error al asignar permisos al rol security")

    def super_admin_RP(db: Session):
        permisos_super_admin = db.query(Permisos).all()
        rol_super_admin = db.query(Rol).filter(Rol.id == 1).first()

        try:
            rol_permiso = [
                Rol_permiso(id_rol=rol_super_admin.id, id_permiso=permiso.id)
                for permiso in permisos_super_admin
            ]
            db.add_all(rol_permiso)
            db.commit()
        except:
            db.rollback()
            raise ValueError("Error al asignar permisos al rol super_admin")
        
    def user_RP(db: Session):
        permisos_user = db.query(Permisos).filter(Permisos.id == 12).all()
        rol_user = db.query(Rol).filter(Rol.id == 4).first()

        try:
            rol_permiso = [
                Rol_permiso(id_rol=rol_user.id, id_permiso=permiso.id)
                for permiso in permisos_user
            ]
            db.add_all(rol_permiso)
            db.commit()
        except:
            db.rollback()
            raise ValueError("Error al asignar permisos al rol user")

    admin_RP(db)
    segurity_RP(db)
    super_admin_RP(db)
    user_RP(db)



def agregar_permiso_al_rol(id_user: int, id_permisos: int, db: Session):
    user = db.query(Users).filter(Users.id == id_user).first()
    
    try:
        if not user or not user.rol:
            return {"detail": "User not found or user does not have a role"}
        rol = user.rol
        Permiso = db.query(Permisos).filter(Permisos.id == id_permisos).first()
        if not Permiso:
            return {"detail": "Permission not found"}
        rol.permisos.append(Permiso)
        db.commit()
        return {"message": "Permission added to role successfully"}
    except:
        return {'message': 'Invalid user or invalid rol', 'status_code': 401}
    

def quitar_permiso_al_rol(id_user: int, id_permisos: int, db: Session):
    user = db.query(Users).filter(Users.id == id_user).first()
    
    try:
        if not user or not user.rol:
            return {"detail": "User not found or user does not have a role"}
        rol = user.rol
        Permiso = db.query(Permisos).filter(Permisos.id == id_permisos).first()
        if not Permiso:
            return {"detail": "Permission not found"}
        rol.permisos.remove(Permiso)
        db.commit()
        return {"message": "Permission removed from role successfully"}
    except:
        return {'message': 'Invalid user or invalid rol', 'status_code': 401}