from ..database.config import get_db
import database.models.book as Book
from sqlalchemy.orm import joinedload

def get_books(db = get_db()):
    return db.query(Book).options(joinedload(Book.genres)).all()