import pandas as pd
from fastapi import APIRouter
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'services'))
import book_services

router = APIRouter()

@router.get("/books")
def books():
    return book_services.get_books()

@router.delete("/books/{id}")
def delete_book(id: int):
    return book_services.remove_book(id)

@router.post("/books")
def add_a_book(book):
    return book_services.add_book(book)

@router.get("/books/{id}")
def get_a_book(id: int):
    return book_services.get_book(id)

@router.put("/books/{id}")
def update_a_book(id: int, book):
    return book_services.update_book(id, book)

@router.get("/books/statistics")
def books_statistics():
    books = book_services.get_books()
    genres = {}
    for book in books:
        for genre in book.genres:
            if genre.name in genres:
                genres[genre.name] += 1
            else:
                genres[genre.name] = 1
    df = pd.DataFrame(genres.items(), columns=['Genre', 'Amount'])
    save_path = os.path.join(os.pardir, os.pardir, 'public', 'books_statistics.csv')
    df.to_csv(save_path, index=False)
    return 'file created: books_statistics.csv'