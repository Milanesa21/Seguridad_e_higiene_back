from sqlalchemy import Column, String, DateTime
from dataBase.db import Base
from datetime import datetime

class File(Base):
    __tablename__ = 'files'

    public_id = Column(String, primary_key=True, index=True)
    url = Column(String, index=True)
    uploaded_at = Column(DateTime, default=datetime.now)