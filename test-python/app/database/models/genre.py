from sqlalchemy import Column, Integer, String
from ..config import Base

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    book_id = Column(Integer, index=True)