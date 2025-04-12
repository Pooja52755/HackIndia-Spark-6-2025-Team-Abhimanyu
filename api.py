from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
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

# Define request and response models
class ChatRequest(BaseModel):
    message: str

class ElementItem(BaseModel):
    description: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    text: Optional[str] = None
    action: Optional[str] = None

class ResponseElements(BaseModel):
    images: Optional[List[ElementItem]] = []
    links: Optional[List[ElementItem]] = []
    accordions: Optional[List[ElementItem]] = []
    buttons: Optional[List[ElementItem]] = []

class ChatResponse(BaseModel):
    response: str
    elements: Optional[ResponseElements] = None

class KnowledgeBaseResponse(BaseModel):
    entities: Dict[str, List[str]]
    relationships: Dict[str, Dict[str, List[str]]]

@app.get("/")
def root():
    return {"message": "Cybersecurity Knowledge Chatbot API", "version": "1.0.0"}

@app.post("/chat", response_model=ChatResponse)
async def chat_handler(request: ChatRequest):
    try:
        user_input = request.message
        if not user_input.strip():
            raise HTTPException(status_code=400, detail="Empty message")
        
        # Get response from chat chain
        response_data = chat_chain.generate_response(user_input)
        
        # Check if response is in the new multi-format structure
        if isinstance(response_data, dict) and "text" in response_data:
            text_response = response_data["text"]
            elements = response_data.get("elements", {})
            return ChatResponse(response=text_response, elements=ResponseElements(**elements))
        else:
            # Handle legacy text-only response
            return ChatResponse(response=response_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge", response_model=KnowledgeBaseResponse)
async def get_knowledge_base():
    """Endpoint to retrieve all entities and relationships from the knowledge base"""
    try:
        print("Knowledge base request received")
        # Get entities
        entities = {
            "ThreatEntity": knowledge_base.getthreatentities(),
            "DefenseTechnology": knowledge_base.getdefensetechnologies(),
            "AttackVector": knowledge_base.getattackvectors(),
            "DataTheft": knowledge_base.getdatatheftthreats(),
            "NetworkSecurity": knowledge_base.getnetworksecuritytools(),
            "EndpointSecurity": knowledge_base.getendpointsecuritytools(),
            "SecurityMonitoring": knowledge_base.getsecuritymonitoringtools()
        }
        
        # Get relationships
        relationships = {
            "MitigatedBy": knowledge_base.kb_data.get("MitigatedBy", {}),
            "DetectedBy": knowledge_base.kb_data.get("DetectedBy", {})
        }
        
        # Log the response for debugging
        response_data = KnowledgeBaseResponse(entities=entities, relationships=relationships)
        print(f"Returning knowledge base with {sum(len(e) for e in entities.values())} entities and {len(relationships)} relationship types")
        
        return response_data
    except Exception as e:
        print(f"Error retrieving knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving knowledge base: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=8006, 
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )