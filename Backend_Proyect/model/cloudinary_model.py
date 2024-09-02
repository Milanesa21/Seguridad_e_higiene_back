from sqlalchemy import Column, Integer, String, DateTime
from dataBase.db import Base
from datetime import datetime

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String, index=True)
    url = Column(String, index=True)
    uploaded_at = Column(DateTime, default=datetime.now)