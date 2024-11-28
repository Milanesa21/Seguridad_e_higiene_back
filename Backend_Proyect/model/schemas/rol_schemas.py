from pydantic import BaseModel

class RolBase(BaseModel):
    nombre_rol: str
    descripcion: str

class Rol(RolBase):
    id: int
    class Config:
        orm_mode = True
        from_attributes = True
        arbitrary_types_allowed = True

class RolRequest(BaseModel):
    id_user: int
    id_rol: int