from fastapi import APIRouter, Request
from pinecone import Pinecone
from app.services import pinecone_services
import os

router = APIRouter()

@router.get("/conversation/{number_phone}")
async def get_conversation(number_phone, request: Request):
    
    pc = Pinecone()
    index = pc.Index(os.getenv("INDEX_SENTIMENT_NAME"))
    messages = pinecone_services.get_all_vectors_by_number(index, number_phone)
    
    return {
        "messages": messages,
        "number_phone": number_phone,
        "status": "success 🧙‍♂️"
    }