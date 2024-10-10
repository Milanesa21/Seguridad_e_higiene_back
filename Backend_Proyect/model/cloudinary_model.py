from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from dataBase.db import Base
from datetime import datetime

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String, index=True)
    url = Column(String, index=True)
    uploaded_at = Column(DateTime, default=datetime.now)
    
    # Columna para almacenar el ID de la compañía
    id_empresa = Column(Integer, ForeignKey('companies.id_empresa'))
    
    # Relación con el modelo Company
    company = relationship("Company", back_populates="files")
