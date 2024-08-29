"""from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

router = APIRouter()

# Cargar el modelo
model = tf.keras.models.load_model('/home/diego/Escritorio/IAs/IA-reconocimiento/IA_ambiente/modelos/modelo_seguridad.h5')

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

@router.post("/predict/ambiente")
async def predict_image(file: UploadFile = File(...)):
    try:
        # Guardar archivo temporalmente
        with open("temp_image.jpg", "wb") as buffer:
            buffer.write(file.file.read())
        
        # Preprocesar la imagen
        img_array = preprocess_image("temp_image.jpg")

        # Realizar la predicción
        predictions = model.predict(img_array)
        prediction = (predictions[0][0] > 0.5).astype(int)

        # Resultado
        result = "Zona Segura" if prediction == 1 else "Falla de seguridad"

        return JSONResponse(content={"message": result})

    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)"""