import pandas as pd
from fastapi import APIRouter
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'services'))
import book_services
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'database'))
from schemas.book_schema import Book_schema


router = APIRouter()

@router.get("/books")
async def books():
    response = await book_services.get_books()
    return response

@router.delete("/books/{id}")
async def delete_book(id: int):
    response = await book_services.remove_book(id)
    return response

@router.post("/books")
async def add_a_book(book: Book_schema):
    response = await book_services.add_book(book)
    return response

@router.get("/books/{id}")
async def get_a_book(id: int):
    response = await book_services.get_book(id)
    return response

@router.get("/books/statistics")
async def books_statistics():
    books = await book_services.get_books()
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