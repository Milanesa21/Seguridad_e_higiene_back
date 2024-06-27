from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from dataBase.db import Base
from dataBase.db import engine
from .user import Users
from pydantic import BaseModel

class AlertMessage(Base):
    __tablename__ = "alert_messages"

    id_message = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    full_name = Column(String) 
    puesto_trabajo = Column(String)
    message = Column(String)
    
    # Relación con la tabla de usuarios
    user = relationship("Users", back_populates="alert_messages")

class AlertMessageRequest(BaseModel):
    user_id: int
    full_name: str 
    puesto_trabajo: str
    message: str
