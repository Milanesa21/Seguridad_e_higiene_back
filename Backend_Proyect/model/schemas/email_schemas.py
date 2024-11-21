from pydantic import BaseModel



class CreateNewCompany(BaseModel):
    empresa: str
    dueno: str
    email: str
    telefono: str