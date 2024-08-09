from pydantic import BaseModel, Field

class PermisoBase(BaseModel):
    nombre_permiso: str = Field(min_length=3,max_length=30)
    descripcion: str = Field(min_length=3,max_length=100)



class Permiso(PermisoBase):
    id: int
    class Config:
        orm_mode = True
        from_attributes = True
        arbitrary_types_allowed = True