from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from dataBase.db import Base
from datetime import date

class Task(Base):
    __tablename__ = "Tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    color = Column(String, nullable=False, default="Ninguna")
    completed = Column(Boolean, default=False)
    date = Column(Date, nullable=False, default=date.today())
    company_id = Column(Integer, ForeignKey("companies.id_empresa"), nullable=False)  # Relación con la empresa

    # Relación con la empresa
    company = relationship("Company", back_populates="tasks")

