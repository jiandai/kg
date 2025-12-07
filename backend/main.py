from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import rag_engine
import os

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    strategy: str = "auto"

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        # Simple fallback for now
        text = content.decode("latin-1")
    
    rag_engine.set_document_context(text)
    return {"filename": file.filename, "message": "File processed successfully", "length": len(text)}

@app.post("/chat")
def chat(request: ChatRequest):
    response = rag_engine.process_query(request.message, request.strategy)
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
