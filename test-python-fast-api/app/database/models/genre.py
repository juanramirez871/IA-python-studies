from sqlalchemy import Column, Integer, String
from ..config import Base
from sqlalchemy.orm import relationship
from .relationships import book_genre_association

book_genre_relationships = book_genre_association(Base)

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    books = relationship("Book", secondary=book_genre_relationships, back_populates="genres")