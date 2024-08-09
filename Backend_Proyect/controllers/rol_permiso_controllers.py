from model.schemas.roles_schemas import RolBase
from model.schemas.permisos_schemas import PermisoBase
from model.roles_permisos import Rol_permiso
from model.permisos import Permisos
from model.roles import Rol
from sqlalchemy.orm import Session
from dataBase.db import get_db

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
        permisos_segurity = db.query(Permisos).filter(Permisos.id < 7).all()
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

    admin_RP(db)
    segurity_RP(db)
    super_admin_RP(db)
