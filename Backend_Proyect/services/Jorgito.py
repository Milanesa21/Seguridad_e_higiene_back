"""from sentence_transformers import SentenceTransformer
from langchain.prompts import PromptTemplate
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel
import os
import shutil
import glob
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time

app = FastAPI()

# Inicializar el modelo de embeddings de sentence-transformers
embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Prompt template para la IA
custom_prompt_template = """ 
#Usa el contexto más relevante para responder la pregunta.
#Contexto: {context}
#Pregunta: {question}

#Tus respuestas deben ser breves, pero explicativas para lo que se te esta preguntando

#Respuesta en español:
"""
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=custom_prompt_template
)

# Memoria local para almacenar los contextos
memory_context = []

# Clase para la consulta del usuario
class Query(BaseModel):
    input_text: str

# Función para agregar documentos al contexto
def update_memory_context(documents):
    global memory_context
    memory_context.extend(documents)

# Función optimizada para cargar y actualizar el contexto desde archivos PDF
def load_context_from_pdfs():
    global memory_context
    memory_context = []  # Reiniciar el contexto al cargar

    # Cargar todos los archivos PDF desde el directorio temporal
    pdf_files = glob.glob("/tmp/*.pdf")
    for pdf_file in pdf_files:
        try:
            loader = PyMuPDFLoader(pdf_file)
            documents = loader.load()

            # Fragmentar documentos en chunks más pequeños
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
            chunks = text_splitter.split_documents(documents)

            # Agregar los chunks al contexto
            update_memory_context(chunks)

        except Exception as e:
            print(f"Error al procesar {pdf_file}: {str(e)}")

# Función para generar embeddings de documentos
def embed_documents(texts):
    return embed_model.encode(texts, convert_to_tensor=True)

# Función para obtener contexto relevante usando embeddings
def get_relevant_context(query):
    if not memory_context:
        return "No tengo contexto disponible aún."

    # Extraer contenido del contexto
    texts = [doc.page_content for doc in memory_context]
    embeddings = embed_documents(texts)

    # Generar embedding para la consulta del usuario
    query_embedding = embed_model.encode(query, convert_to_tensor=True)

    # Calcular similitud coseno
    similarities = cosine_similarity(query_embedding.cpu().numpy().reshape(1, -1), embeddings.cpu().numpy())[0]

    # Encontrar los textos más relevantes (top 2 en vez de 3)
    top_indices = np.argsort(similarities)[::-1][:2]  # Top 2 documentos más relevantes
    relevant_texts = [texts[i] for i in top_indices]

    return " ".join(relevant_texts)  # Concatenar los fragmentos más relevantes

# Ruta para manejar la subida de archivos PDF y actualizar el contexto
@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
    
    try:
        # Guardar el archivo temporalmente
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Recargar el contexto desde todos los archivos PDF y reiniciar la IA
        start_time = time.time()
        load_context_from_pdfs()
        end_time = time.time()

        processing_time = end_time - start_time
        return JSONResponse(status_code=200, content={
            "message": "PDF cargado y contexto actualizado.",
            "processing_time": processing_time  # Devolver el tiempo de procesamiento
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ruta para eliminar un archivo PDF específico y su contexto asociado
@app.post("/delete/")
async def delete_pdf(doc_name: str):
    try:
        file_path = f"/tmp/{doc_name}"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Archivo no encontrado")

        os.remove(file_path)

        # Recargar el contexto después de eliminar el archivo
        load_context_from_pdfs()

        return JSONResponse(status_code=200, content={"message": "Archivo y contexto eliminados."})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ruta para manejar las preguntas del usuario
@app.post("/query/")
async def get_response(query: Query):
    full_prompt = query.input_text

    # Obtener el contexto relevante
    try:
        start_time = time.time()
        context_text = get_relevant_context(full_prompt)
        end_time = time.time()

        response_time = end_time - start_time
        return JSONResponse(content=context_text.strip(), status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Cargar el contexto y reiniciar la IA cuando se inicia el servidor
@app.on_event("startup")
async def on_startup():
    print("Cargando contexto desde archivos PDF...")
    load_context_from_pdfs()
"""