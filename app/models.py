from app.database import Base
from sqlalchemy import Column, Integer, String, Float

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float)