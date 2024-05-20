from sqlalchemy import Column, Integer, String, Table, ForeignKey

def book_genre_association(Base):
    
    return Table(
        "book_genre_association",
        Base.metadata,
        Column("book_id", Integer, ForeignKey("books.id")),
        Column("genre_id", Integer, ForeignKey("genres.id")),
        extend_existing=True
    )