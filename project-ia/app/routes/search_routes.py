from fastapi import APIRouter, Request
from pinecone import Pinecone
from app.services import pinecone_services
import os

router = APIRouter()

@router.get("/search/info/{number_phone}")
async def get_conversation(number_phone, request: Request):
    return