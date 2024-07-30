from fastapi import APIRouter, Request
from pinecone import Pinecone
from app.services import pinecone_services
from transformers import pipeline
import os

router = APIRouter()

@router.get("/feelings/{number_phone}")
async def get_conversation(number_phone, request: Request):
    pc = Pinecone()
    index = pc.Index(os.getenv("INDEX_SENTIMENT_NAME"))
    data = pinecone_services.get_lastest_vectors_by_number(index, number_phone, 20)
    amount_starts = sum([int(message['starts']) for message in data])
    average_starts = amount_starts / len(data)
    
    return {
        "status": "success 🧙‍♂️",
        "number_phone": number_phone,
        "average_starts": average_starts
    }
    
    