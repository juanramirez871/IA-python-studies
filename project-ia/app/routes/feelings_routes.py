from fastapi import APIRouter, Request
from pinecone import Pinecone
from app.services import pinecone_services
from transformers import pipeline
import os

router = APIRouter()

@router.get("/feelings/{number_phone}")
async def get_conversation(number_phone, request: Request):
    pc = Pinecone()
    index = pc.Index(os.getenv("INDEX_WHATSAPP_NAME"))
    
    