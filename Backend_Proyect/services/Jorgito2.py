from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, JSONResponse
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.chains import RetrievalQA
import os
import shutil
import glob

class Query(BaseModel):
    input_text: str

app = FastAPI()

# Configuración del modelo LLM
llm = OllamaLLM(model="llama3.2:1b") 

# Definir un prompt detallado
custom_prompt_template = """
Usa la siguiente información para responder a la pregunta del usuario.
Si no puedes encontrar la respuesta, indica que no sabes la respuesta.
Para indicar que no sabes la respuesta, escribe "No sé la respuesta a esa pregunta, puedes brindarme un pdf para que te pueda responder a eso".

Solo contesta en español, y trata de ser lo más preciso posible.

Si el contexto es muy largo, puedes resumirlo.

Si el contexto esta en un idioma que no sea español, tradúcelo antes de contestar.

Contexto: {context}
Pregunta: {question}
"""
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=custom_prompt_template
)

# Variables globales para almacenar el vectorstore
pdf_directory = "/home/diego/Escritorio/Seguridad_e_higiene_back/Backend_Proyect/services/context/"
persist_db = "/home/diego/chroma_db_dir"
collection_name = "chroma_collection"
embed_model = FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = None
retriever = None
qa_chain = None

# Función para inicializar o actualizar ChromaDB
def initialize_chroma_db():
    global vectorstore, retriever, qa_chain  # Declarar antes de usar

    # Cargar la base de datos persistente si existe
    if os.path.exists(persist_db):
        print("Cargando ChromaDB existente...")
        vectorstore = Chroma(
            embedding_function=embed_model,
            persist_directory=persist_db,
            collection_name=collection_name
        )
    else:
        print("No se encontró una base de datos persistente. Creando una nueva...")
        pdf_files = glob.glob(os.path.join(pdf_directory, "*.pdf"))

        if pdf_files:
            documents = []
            for pdf_file in pdf_files:
                loader = PyMuPDFLoader(pdf_file)
                documents.extend(loader.load())

            # Fragmentar documentos en chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
            chunks = text_splitter.split_documents(documents)

            # Crear una nueva base de datos con los chunks
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embed_model,
                persist_directory=persist_db,
                collection_name=collection_name
            )
        else:
            vectorstore = None

    # Actualizar el retriever y la cadena QA si hay un vectorstore disponible
    if vectorstore:
        retriever = vectorstore.as_retriever(search_kwargs={'k': 5})
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=False,
            chain_type_kwargs={'prompt': prompt_template}
        )

# Endpoint para subir archivos PDF
@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    global vectorstore, retriever, qa_chain  # Declarar aquí también

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF.")

    file_path = os.path.join(pdf_directory, file.filename)
    with open(file_path, "wb") as pdf_file:
        shutil.copyfileobj(file.file, pdf_file)

    # Procesar el nuevo archivo PDF y actualizar ChromaDB
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
    chunks = text_splitter.split_documents(documents)

    if vectorstore:
        # Agregar nuevos documentos al vectorstore existente
        vectorstore.add_documents(chunks)
    else:
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embed_model,
            persist_directory=persist_db,
            collection_name=collection_name
        )

    # Actualizar el retriever y la cadena QA
    initialize_chroma_db()

    return JSONResponse(content={"message": "Archivo subido y procesado exitosamente."})

# Endpoint para borrar archivos PDF y su contexto en ChromaDB
@app.post("/delete/")
async def delete_pdf(doc_name: str):
    global vectorstore, retriever, qa_chain  # Declarar aquí también

    # Ruta completa del archivo PDF
    file_path = os.path.join(pdf_directory, doc_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado.")

    # Eliminar el archivo físico
    os.remove(file_path)
    print(f"Archivo {doc_name} eliminado del sistema de archivos.")

    # Reconstruir ChromaDB sin el archivo eliminado
    pdf_files = glob.glob(os.path.join(pdf_directory, "*.pdf"))

    if pdf_files:
        documents = []
        for pdf_file in pdf_files:
            loader = PyMuPDFLoader(pdf_file)
            documents.extend(loader.load())
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
        chunks = text_splitter.split_documents(documents)

        # Actualizar el vectorstore
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embed_model,
            persist_directory=persist_db,
            collection_name=collection_name
        )
    else:
        # Si no quedan archivos, limpiar el vectorstore
        vectorstore = None

    # Actualizar el retriever y la cadena QA
    initialize_chroma_db()

    return JSONResponse(content={"message": f"Archivo {doc_name} eliminado y ChromaDB actualizado exitosamente."})


# Inicializar ChromaDB al arrancar el servidor
initialize_chroma_db()

# Generador para respuestas en streaming
async def model_output_generator(full_prompt):
    try:
        if qa_chain:
            response = await qa_chain.ainvoke({"query": full_prompt})
            for token in response['result'].split():
                yield token.encode('utf-8') + b' '
        else:
            yield b"No hay un contexto disponible para responder la pregunta."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Endpoint para realizar consultas al modelo
@app.post("/query/")
async def get_response(query: Query):
    full_prompt = query.input_text
    return StreamingResponse(model_output_generator(full_prompt), media_type="text/plain")

