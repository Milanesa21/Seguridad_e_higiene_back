from pydantic import BaseModel

class PermisoBase(BaseModel):
    nombre_permiso: str
    descripcion: str



class Permiso(PermisoBase):
    id: int
    class Config:
        orm_mode = True
        from_attributes = True
        arbitrary_types_allowed = True