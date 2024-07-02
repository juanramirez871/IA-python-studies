from database.models.genre import Genre
from sqlalchemy import select
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, 'database'))
from config import get_db


async def get_genres():
    db = next(get_db())
    query = select(Genre)
    result = await db.execute(query)
    genres = [{"id": genre.id, "name": genre.name} for genre in result.scalars()]
    return { "message": "Genres all", "data": genres}


async def remove_genre(genre_id):
        db = next(get_db())
        genre = await db.get(Genre, genre_id)
        if genre:
            await db.delete(genre)
            await db.commit()
            return {'message': f'Genre with ID {genre_id} deleted'}
        else:
            return {'error': 'Genre not found'}

async def add_genre(genre):
    
    db = next(get_db())
    genre = Genre(name=genre)
    db.add(genre)
    await db.commit()
    return {'message': 'Genre added'}

async def get_genre(id):
    db = next(get_db())
    query = select(Genre).where(Genre.id.in_([id]))
    result = await db.execute(query)
    genres = [{"id": genre.id, "name": genre.name} for genre in result.scalars()]
    return { "message": "Genre", "data": genres}