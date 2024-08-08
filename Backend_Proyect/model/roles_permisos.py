from sqlalchemy import Column, Integer, ForeignKey
from dataBase.db import Base


class Rol_permiso(Base):
    __tablename__ = "roles_permisos"
    id = Column(Integer, primary_key=True, index=True)
    id_rol = Column(Integer, ForeignKey("roles.id"))
    id_permiso = Column(Integer, ForeignKey("permisos.id"))