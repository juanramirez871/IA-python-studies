from ..database.config import get_db
import database.models.book as Book
from sqlalchemy.orm import joinedload

def get_books(db = get_db()):
    return db.query(Book).options(joinedload(Book.genres)).all()

def remove_book(id, db = get_db()):
    db.query(Book).filter(Book.id == id).delete()
    db.commit()
    return 'Book removed'

def add_book(book, db = get_db()):
    db.add(book)
    db.commit()
    return 'Book added'

def get_book(id, db = get_db()):
    return db.query(Book).filter(Book.id == id).options(joinedload(Book.genres)).first()

def update_book(id, book, db = get_db()):
    db.query(Book).filter(Book.id == id).update(book)
    db.commit()
    return 'Book updated'