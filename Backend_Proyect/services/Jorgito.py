from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain_ollama import OllamaLLM
from transformers import AutoTokenizer, AutoModel
import torch
import os
import glob
import numpy as np

class Query(BaseModel):
    input_text: str

class CustomHuggingFaceEmbeddings(Embeddings):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Genera embeddings para una lista de textos."""
        embeddings = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, 
                                    padding=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs)
                embedding = outputs.last_hidden_state.mean(dim=1).numpy()
                embeddings.append(embedding[0].tolist())
        return embeddings
    
    def embed_query(self, text: str) -> list[float]:
        """Genera embedding para un solo texto de consulta."""
        return self.embed_documents([text])[0]

app = FastAPI()

# Configuración de LangChain
llm = OllamaLLM(model="llama3.2:1b", max_tokens=100)
prompt_template = PromptTemplate(
    input_variables=["context", "question"], 
    template="{context}\nPregunta: {question}"
)

# Crear el chain usando el nuevo método recomendado
chain = prompt_template | llm

# Variables globales para almacenar el vectorstore
vectorstore = None

# Directorio donde se almacenan los archivos PDF
pdf_directory = "/home/diego/Escritorio/Seguridad_e_higiene_back/Backend_Proyect/services/context/"

# Verificación y carga de todos los archivos PDF en el directorio
pdf_files = glob.glob(os.path.join(pdf_directory, "*.pdf"))

if pdf_files:
    print("Contexto añadido correctamente. Archivos encontrados:", pdf_files)
    
    documents = []
    for pdf_file in pdf_files:
        pdf_loader = PyPDFLoader(pdf_file)
        documents.extend(pdf_loader.load())
    
    # Crear el vectorstore con todos los documentos cargados
    embedding_model = CustomHuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(documents, embedding_model)
else:
    print("No se encontraron archivos PDF en el directorio especificado.")

async def model_output_generator(full_prompt):
    try:
        if vectorstore:
            # Realizar la búsqueda de documentos similares
            similar_docs = vectorstore.similarity_search(full_prompt, k=2)
            # Extraer el contenido de los documentos
            context_text = "\n".join([doc.page_content for doc in similar_docs])
        else:
            context_text = "No se encontró el contexto."
            
        # Usar el chain para generar la respuesta
        response = await chain.ainvoke({
            "context": context_text,
            "question": full_prompt
        })
        
        # Convertir la respuesta en un generador de tokens
        for token in response.split():
            yield token.encode('utf-8') + b' '
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/query/")
async def get_response(query: Query):
    full_prompt = query.input_text
    return StreamingResponse(model_output_generator(full_prompt), media_type="text/plain")
