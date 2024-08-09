from pydantic import BaseModel, Field


class RolBase(BaseModel):
    nombre_rol: str = Field(min_length=3,max_length=30)
    descripcion: str = Field(min_length=3,max_length=100)

class Rols(RolBase):
    id: int
    class Config:
        orm_mode = True
        from_attributes = True
        arbitrary_types_allowed = True