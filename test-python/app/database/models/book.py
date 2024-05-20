from sqlalchemy import Column, Integer, String
from ..config import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, unique=False, index=True)
