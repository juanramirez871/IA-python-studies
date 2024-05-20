from fastapi import APIRouter
from ..services.book_services import get_books, remove_book, add_book, get_book, update_book

router = APIRouter()

@router.get("/books")
def books():
    return get_books()

@router.delete("/books/{id}")
def delete_book(id: int):
    return remove_book(id)

@router.post("/books")
def add_a_book(book):
    return add_book(book)

@router.get("/books/{id}")
def get_a_book(id: int):
    return get_book(id)

@router.put("/books/{id}")
def update_a_book(id: int, book):
    return update_book(id, book)