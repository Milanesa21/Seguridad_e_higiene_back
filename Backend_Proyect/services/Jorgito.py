from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import os
import glob

class Query(BaseModel):
    input_text: str

app = FastAPI()

# Configuración de LangChain
llm = OllamaLLM(model="llama3.2:1b")

# Definir un prompt detallado
custom_prompt_template = """
Usa la siguiente información para responder a la pregunta del usuario.
Si no puedes encontrar la respuesta, indica que no sabes la respuesta.

Contexto: {context}
Pregunta: {question}

Respuesta en español:
"""
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=custom_prompt_template
)
chain = prompt_template | llm

# Variables globales para almacenar el vectorstore
vectorstore = None

# Directorio donde se almacenan los archivos PDF
pdf_directory = "/home/diego/Escritorio/Seguridad_e_higiene_back/Backend_Proyect/services/context/"
pdf_files = glob.glob(os.path.join(pdf_directory, "*.pdf"))

# Verificación y carga de archivos PDF
if pdf_files:
    print("Contexto encontrado.")
    documents = []
    for pdf_file in pdf_files:
        loader = PyMuPDFLoader(pdf_file)
        documents.extend(loader.load())

    # Fragmentar documentos en chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
    chunks = text_splitter.split_documents(documents)
    
    # Crear vectorstore persistente usando Chroma
    embed_model = FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    persist_db = "/home/diego/chroma_db_dir"
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embed_model,
        persist_directory=persist_db,
        collection_name="chroma_collection"
    )
else:
    print("No se encontraron archivos PDF en el directorio especificado.")

async def model_output_generator(full_prompt):
    try:
        if vectorstore:
            # Realizar la búsqueda de documentos similares
            similar_docs = vectorstore.as_retriever(search_kwargs={'k': 3}).get_relevant_documents(full_prompt)
            context_text = "\n".join([doc.page_content for doc in similar_docs])
        else:
            context_text = "No se encontró el contexto."
            
        response = await chain.ainvoke({
            "context": context_text,
            "question": full_prompt
        })
        
        for token in response.split():
            yield token.encode('utf-8') + b' '
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/query/")
async def get_response(query: Query):
    full_prompt = query.input_text
    return StreamingResponse(model_output_generator(full_prompt), media_type="text/plain")
