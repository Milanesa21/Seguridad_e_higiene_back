from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PDFFileCreate(BaseModel):
    filename: str


class PDFFileOut(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime
    user_id: int

    class Config:
        orm_mode = True
