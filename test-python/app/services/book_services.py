from database.models.book import Book
from sqlalchemy import select
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'database'))
from config import get_db


async def get_books():
    db = next(get_db())
    query = select(Book)
    result = await db.execute(query)
    books = [{"id": book.id, "title": book.title, "description": book.description} for book in result.scalars()]
    return { "message": "Genres all", "data": books}


async def remove_book(book_id):
        db = next(get_db())
        book = await db.get(Book, book_id)
        if book:
            await db.delete(book)
            await db.commit()
            return {'message': f'Book with ID {book_id} deleted'}
        else:
            return {'error': 'Book not found'}


async def add_book(book_schema):
    db = next(get_db())
    book = Book(title=book_schema.title, description=book_schema.description)
    db.add(book)
    await db.commit()
    return {'message': 'Book added'}


async def get_book(id):
    db = next(get_db())
    query = select(Book).where(Book.id.in_([id]))
    result = await db.execute(query)
    book = [{"id": book.id, "name": book.title, "description": book.description} for book in result.scalars()]
    return { "message": "Book", "data": book}