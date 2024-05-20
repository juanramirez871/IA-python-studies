from fastapi import APIRouter
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'services'))
import genre_services

router = APIRouter()

@router.get("/genres")
async def message():
    response = await genre_services.get_genres()
    return response

@router.delete("/genres/{id}")
async def delete_genre(id: int):
    response = await genre_services.remove_genre(id)
    return response

@router.post("/genres")
async def add_a_genre(genre):
    response = await genre_services.add_genre(genre)
    return response

@router.get("/genres/{id}")
async def get_a_genre(id: int):
    response = await genre_services.get_genre(id)
    return response