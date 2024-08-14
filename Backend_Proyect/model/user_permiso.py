from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from dataBase.db import Base

class User_Permiso(Base):
    __tablename__ = "users_permisos"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    id_permiso = Column(Integer, ForeignKey("permisos.id"))

    user = relationship("Users", back_populates="user_permisos")
    permiso = relationship("Permisos", back_populates="user_permisos")
