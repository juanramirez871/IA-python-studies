from sqlalchemy import Column, Integer, String
from ..config import Base
from sqlalchemy.orm import relationship
from .relationships import book_genre_association

book_genre_relationships = book_genre_association(Base)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, unique=False, index=True)

    genres = relationship("Genre", secondary=book_genre_relationships, back_populates="books")