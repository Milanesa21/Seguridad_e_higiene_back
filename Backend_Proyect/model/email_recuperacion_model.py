from sqlalchemy import Column, DateTime, Integer, String
from dataBase.db import Base

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    Token = Column(String, unique=True)
    email = Column(String, unique=True)
    expiration_time = Column(DateTime, nullable=False)

