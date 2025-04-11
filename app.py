from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from model.metta_queries import MettaKnowledgeBase
from model.gemini_model import GeminiChain

from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()  # Load environment variables

app = FastAPI(title="Cybersecurity Knowledge Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the knowledge base and chat chain
try:
    knowledge_base = MettaKnowledgeBase()
    chat_chain = GeminiChain(knowledge_base)
except Exception as e:
    raise RuntimeError(f"Initialization failed: {str(e)}")

# Define request model
class ChatRequest(BaseModel):
    message: str

# Define response model
class ChatResponse(BaseModel):
    response: str

@app.get("/chat")
def root():
    return {"message": "Hello"}

@app.post("/chat", response_model=ChatResponse)
async def chat_handler(request: ChatRequest):
    try:
        user_input = request.message
        if not user_input.strip():
            raise HTTPException(status_code=400, detail="Empty message")
        
        response = chat_chain.generate_response(user_input)
        return ChatResponse(response=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=8006, 
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )