from ..database.config import get_db
import database.models.genre as Genre

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