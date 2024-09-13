from model.roles import Rol
from model.permisos import Permisos
from dataBase.db import get_db
from sqlalchemy.orm import Session
from controllers.rol_permiso_controllers import agregar_permisos_iniciales, crear_super_admin
from controllers.company_controllers import crear_empresa_inicial



def roles_insert(db: Session):

    exite_rol = db.query(Rol).all()
    exite_rol_nombre={rol.nombre_rol for rol in exite_rol}

    roles = [
        Rol(nombre_rol="super_admin", descripcion="Para la creacion de empresas"),
        Rol(nombre_rol="admin", descripcion="Para la creacion de usuarios"),
        Rol(nombre_rol="segurity", descripcion="Para la creacion de alertas"),
        Rol(nombre_rol="user", descripcion="Para la creacion de alertas"),
    ]

    nuevos_roles = [rol for rol in roles if rol.nombre_rol not in exite_rol_nombre]

    if nuevos_roles:
        db.add_all(nuevos_roles)
        db.commit()

def permisos_insert(db: Session):

    exite_permiso = db.query(Permisos).all()
    exite_permiso_nombre={permiso.nombre_permiso for permiso in exite_permiso}

    permisos = [
        Permisos(nombre_permiso="crear_empresa", descripcion="Permite la creacion de empresas"),
        Permisos(nombre_permiso="eliminar_empresa", descripcion="Permite la eliminacion de empresas"),
        Permisos(nombre_permiso="editar_empresa", descripcion="Permite la edicion de empresas"),
        Permisos(nombre_permiso="crear_usuario", descripcion="Permite la creacion de usuarios"),
        Permisos(nombre_permiso="editar_usuario", descripcion="Permite la edicion de usuarios"),
        Permisos(nombre_permiso="lee_usuario", descripcion="Permite la lectura de usuarios"),
        Permisos(nombre_permiso="eliminar_usuario", descripcion="Permite la eliminacion de usuarios"),
        Permisos(nombre_permiso="crear_registros", descripcion="Permite la creacion de registros"),
        Permisos(nombre_permiso="editar_registros", descripcion="Permite la edicion de registros"),
        Permisos(nombre_permiso="eliminar_registros", descripcion="Permite la eliminacion de registros"),
        Permisos(nombre_permiso="lee_registros", descripcion="Permite la lectura de registros"),
        Permisos(nombre_permiso="alertas", descripcion="Permite la creacion de alertas"),
    ]

    nuevos_permisos = [permiso for permiso in permisos if permiso.nombre_permiso not in exite_permiso_nombre]

    if nuevos_permisos:
        db.add_all(nuevos_permisos)
        db.commit()

def Db_insert_RP():
    db: Session = next(get_db())
    try:
        roles_insert(db)
    except:
        db.rollback()
        raise ValueError("Error al insertar roles")
    finally:
        db.close()

    try:
        permisos_insert(db)
    except:
        db.rollback()
        raise ValueError("Error al insertar permisos")
    finally:
        db.close()


    try:
        agregar_permisos_iniciales(db)
    except:
        db.rollback()
        raise ValueError("Error al asignar permisos a roles")
    finally:
        db.close()

    try:
        crear_empresa_inicial(db)
    except:
        db.rollback()
        raise ValueError("Error al crear empresa inicial")
    finally:
        db.close()

    try:
        crear_super_admin(db)
    except:
        db.rollback()
        raise ValueError("Error al crear super admin")
    finally:
        db.close()