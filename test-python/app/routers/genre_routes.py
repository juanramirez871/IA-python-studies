from fastapi import APIRouter
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'services'))
import genre_services

router = APIRouter()

@router.get("/genres")
def message():
    return genre_services.get_genres()

@router.delete("/genres/{id}")
def delete_genre(id: int):
    return genre_services.remove_genre(id)

@router.post("/genres")
def add_a_genre(genre):
    return genre_services.add_genre(genre)

@router.get("/genres/{id}")
def get_a_genre(id: int):
    return genre_services.get_genre(id)

@router.put("/genres/{id}")
def update_a_genre(id: int, genre):
    return genre_services.update_genre(id, genre)