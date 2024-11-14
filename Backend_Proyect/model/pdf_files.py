from sqlalchemy import Column, Integer, String, LargeBinary, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from dataBase.db import Base

class PDFFile(Base):
    __tablename__ = "pdf_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content = Column(LargeBinary, nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())

    # Relación con la tabla de usuarios (Users)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="pdf_files")

# Importar al final para evitar importaciones circulares
from model.user import Users
