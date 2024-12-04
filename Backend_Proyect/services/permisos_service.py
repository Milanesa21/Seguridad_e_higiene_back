from sqlalchemy.orm import Session
from model.user import Users
from model.roles_permisos import Rol_permiso
from model.permisos import Permisos


def user_has_permission(user_id:int, permission_name: str, db: Session):
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        return {'message': 'User not found'}
    
    permission = (
        db.query(Permisos)
        .join(Rol_permiso, Rol_permiso.id_permiso == Permisos.id)
        .filter(Rol_permiso.id_rol == user.id_role, Permisos.nombre_permiso == permission_name)
    )

    return permission is not None