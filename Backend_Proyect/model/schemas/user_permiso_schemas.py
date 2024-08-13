from pydantic import BaseModel

class UserPermisoBase(BaseModel):
    id_user: int
    id_permiso: int


class UserPermiso(UserPermisoBase):
    id: int
    class Config:
        orm_mode = True
        from_attributes = True
        arbitrary_types_allowed = True