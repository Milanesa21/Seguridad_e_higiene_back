from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.params import Query
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
async def upload_file(file: UploadFile = File(...),
                    id_empresa: int= Query(..., description="Id de la empresa"),
                    db: Session = Depends(get_db)):
    try:
        # Subir archivo a Cloudinary
        result = cloudinary.uploader.upload(file.file, resource_type='auto')
        public_id = result['public_id']
        url = result['secure_url']
        uploaded_at = datetime.now()
        id_empresa = id_empresa
        
        # Guardar la información en la base de datos
        db_file = CloudinaryModel(public_id=public_id, url=url, uploaded_at=uploaded_at, id_empresa=id_empresa)
        db.add(db_file)
        db.commit()
        
        return {"public_id": public_id, "url": url, "uploaded_at": uploaded_at,"id_empresa":id_empresa}
    except cloudinary.exceptions.Error as e:
        raise HTTPException(status_code=500, detail="Error uploading file")

# Ruta para listar todos los archivos
@file_router.get("/images/{id}")
async def list_images(
    id_empresa: int = Query(..., description="ID de la empresa"),
    db: Session = Depends(get_db)
):
    try:
        # Consultar y ordenar los archivos por fecha de subida (más reciente primero)
        files = db.query(CloudinaryModel).filter(CloudinaryModel.id_empresa == id_empresa).order_by(CloudinaryModel.uploaded_at.desc()).all()

        # Extraer los detalles necesarios y convertir `uploaded_at` a cadena
        image_list = [
            {
                "public_id": file.public_id,
                "url": file.url,
                "uploaded_at": file.uploaded_at.isoformat(),  # Convertir datetime a string
                "id_empresa": file.id_empresa  
            }
            for file in files
        ]

        if not image_list:
            raise HTTPException(status_code=404, detail="No se han encontrado imagenes")
        
        return JSONResponse(content={"images": image_list})
    except Exception as e:
        print(f"Error retrieving images: {e}")
        raise HTTPException(status_code=500, detail="Fallo al traer las imagenes")



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
            return {"message": "Archivo borrado correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
    except cloudinary.exceptions.Error as e:
        raise HTTPException(status_code=404, detail="archivo no encontrado o no borrado correctamente")
    except Exception as e:
        # Imprimir el error para depuración
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
