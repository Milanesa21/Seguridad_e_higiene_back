from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    full_name: str = Field(min_length=4,max_length=30)
    email: EmailStr
    puesto_trabajo: str = Field(min_length=3,max_length=100)

class CreateUsersRequest(BaseModel):
    puesto_trabajo: str = Field(min_length=3,max_length=100)
    num_usuarios: int = Field(ge=1)


class LoginRequest(BaseModel):
    full_name: str = Field(min_length=4,max_length=30)
    password: str 

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class DBUser(User):
    password: str
