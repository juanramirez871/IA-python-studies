from fastapi import APIRouter
from ..services.genre_services import get_genres, remove_genre, add_genre, get_genre, update_genre

router = APIRouter()

@router.get("/genres")
def message():
    return get_genres()

@router.delete("/genres/{id}")
def delete_genre(id: int):
    return remove_genre(id)

@router.post("/genres")
def add_a_genre(genre):
    return add_genre(genre)

@router.get("/genres/{id}")
def get_a_genre(id: int):
    return get_genre(id)

@router.put("/genres/{id}")
def update_a_genre(id: int, genre):
    return update_genre(id, genre)