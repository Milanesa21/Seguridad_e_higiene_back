from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from model.cloudinary_model import File as CloudinaryModel
from dataBase.db import get_db
import cloudinary.uploader
import cloudinary.api
from datetime import datetime

# Configura Cloudinary con tus credenciales
cloudinary.config(
    cloud_name='dwc8uwkoy',
    api_key='966881539451554',
    api_secret='nI3Mf8-XNlz2r2RClF2nreqyFsM'
)

file_router = APIRouter(prefix='/file', tags=['Files'])

# Ruta para subir un archivo
@file_router.post('/upload/')
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Subir archivo a Cloudinary
        result = cloudinary.uploader.upload(file.file, resource_type='auto')
        public_id = result['public_id']
        url = result['secure_url']
        uploaded_at = datetime.now()
        
        # Guardar la información en la base de datos
        db_file = CloudinaryModel(public_id=public_id, url=url, uploaded_at=uploaded_at)
        db.add(db_file)
        db.commit()
        
        return {"public_id": public_id, "url": url, "uploaded_at": uploaded_at}
    except cloudinary.exceptions.Error as e:
        raise HTTPException(status_code=500, detail="Error uploading file")

# Ruta para listar todos los archivos
@file_router.get("/images/")
async def list_images(db: Session = Depends(get_db)):
    try:
        # Consultar todos los archivos en la base de datos
        files = db.query(CloudinaryModel).all()
        
        # Extraer los detalles necesarios y convertir `uploaded_at` a cadena
        image_list = [
            {
                "public_id": file.public_id,
                "url": file.url,
                "uploaded_at": file.uploaded_at.isoformat()  # Convertir datetime a string
            }
            for file in files
        ]
        
        return JSONResponse(content={"images": image_list})
    except Exception as e:
        # Imprimir el error para depuración
        print(f"Error retrieving images: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve images")


# Ruta para eliminar un archivo
@file_router.delete('/{public_id}')
async def delete_file(public_id: str, db: Session = Depends(get_db)):
    try:
        # Eliminar el archivo desde Cloudinary
        cloudinary.api.delete_resources([public_id])
        
        # Verificar si el archivo está en la base de datos antes de eliminar
        file_to_delete = db.query(CloudinaryModel).filter(CloudinaryModel.public_id == public_id).first()
        if file_to_delete:
            db.delete(file_to_delete)
            db.commit()
            return {"message": "File and database record successfully deleted"}
        else:
            raise HTTPException(status_code=404, detail="File not found in database")
    except cloudinary.exceptions.Error as e:
        raise HTTPException(status_code=404, detail="File not found or could not be deleted")
    except Exception as e:
        # Imprimir el error para depuración
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
