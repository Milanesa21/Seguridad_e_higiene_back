from fastapi import APIRouter, Depends
from controllers.rol_permiso_controllers import agregar_permiso_al_rol, quitar_permiso_al_rol, get_all_permisos
from dataBase.db import get_db
from sqlalchemy.orm import Session
from model.schemas.permisos_schemas import PermisoRequest

permiso_router = APIRouter(prefix='/permiso', tags=['Permisos'])

@permiso_router.post('/role/addPermission')
async def add_permissions_to_role(request: PermisoRequest, db: Session = Depends(get_db)):
    id_user = request.id_user
    id_permiso = request.id_permiso
    return agregar_permiso_al_rol(id_user, id_permiso, db)

@permiso_router.patch('/role/removePermission')
async def remove_permission_from_role(request: PermisoRequest, db: Session = Depends(get_db)):
    id_user = request.id_user
    id_permiso = request.id_permiso
    return quitar_permiso_al_rol(id_user, id_permiso, db)


@permiso_router.get('/role/getPermissions')
async def get_all_permissions(db: Session = Depends(get_db)):
    return get_all_permisos(db)
