from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String
from dataBase.db import Base
from dataBase.db import engine


class UserBase(BaseModel):
    username: str   
    email: str
    disables: bool


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class DBUser(User):
    password: str

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    disabled = Column(Boolean)
    password = Column(String)

    def change_password(self, new_password: str):
        self.password = new_password


Base.metadata.create_all(engine)


