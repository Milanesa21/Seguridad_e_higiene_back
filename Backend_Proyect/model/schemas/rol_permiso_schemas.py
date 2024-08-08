from pydantic import BaseModel
from typing import List

class RolPermisoBase(BaseModel):
    id_rol: int
    id_permiso: List[int]


class RolPermiso(RolPermisoBase):
    id: int
    class Config:
        orm_mode = True
        from_attributes = True
        arbitrary_types_allowed = True