from pydantic import BaseModel, EmailStr
from sqlalchemy import DateTime

class TokenRequest(BaseModel):
    email: str = EmailStr

