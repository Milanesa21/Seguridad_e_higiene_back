from pydantic import BaseModel, Field, EmailStr

class CompanyBase(BaseModel):
    nombre_empresa: str = Field(..., min_length=1, max_length=100)
    nombre_jefe: str = Field(..., min_length=1, max_length=100)
    correo_jefe: EmailStr
    numero_jefe: str = Field(..., min_length=1, max_length=20)

class CompanyCreate(CompanyBase):
    password: str = Field(..., min_length=6, max_length=100)
    id_superuser: int

class CompanyUpdate(CompanyBase):
    password: str = None # Opcional


class CompanyResponse(CompanyBase):
    id_empresa: int

    class Config:
        orm_mode = True
        from_attributes = True

class CompanyRequest(BaseModel):
    nombre_empresa: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)
