from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from model.pdf_files import PDFFile
from model.user import Users
from dataBase.db import get_db
from model.schemas.pdf_file import PDFFileOut
from typing import List


router = APIRouter()


@router.post("/upload-pdf/", response_model=PDFFileOut)
async def upload_pdf(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validar que el archivo sea un PDF
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    # Verificar si el usuario existe
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Leer el contenido del archivo
    content = await file.read()

    # Crear el registro en la base de datos
    pdf_record = PDFFile(filename=file.filename, content=content, user_id=user.id)
    db.add(pdf_record)
    db.commit()
    db.refresh(pdf_record)

    return pdf_record


@router.get("/pdfs/", response_model=List[PDFFileOut])
def get_all_pdfs(db: Session = Depends(get_db)):
    pdfs = db.query(PDFFile).all()
    return pdfs


@router.get("/pdfs/{pdf_id}", response_model=PDFFileOut)
def get_pdf(pdf_id: int, db: Session = Depends(get_db)):
    pdf = db.query(PDFFile).filter(PDFFile.id == pdf_id).first()
    if not pdf:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return pdf
