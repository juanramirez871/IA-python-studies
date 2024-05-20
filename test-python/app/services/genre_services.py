import database.models.genre as Genre
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'database'))
from config import get_db

def get_genres(db = get_db()):
    return db.query(Genre).all()

def remove_genre(id, db = get_db()):
    db.query(Genre).filter(Genre.id == id).delete()
    db.commit()
    return 'Genre removed'

def add_genre(genre, db = get_db()):
    db.add(genre)
    db.commit()
    return 'Genre added'

def get_genre(id, db = get_db()):
    return db.query(Genre).filter(Genre.id == id).first()

def update_genre(id, genre, db = get_db()):
    db.query(Genre).filter(Genre.id == id).update(genre)
    db.commit()
    return 'Genre updated'