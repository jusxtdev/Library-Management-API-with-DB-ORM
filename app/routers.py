from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.schemas import BookCreate, BookUpdate, BookResponse
from app.database import get_db
from app.models import Book

router = APIRouter(prefix='/books', tags=['Book'])

@router.get('/', response_model=list[BookResponse], status_code=status.HTTP_200_OK)
def get_books(db : Session = Depends(get_db)):
    all_books = db.query(Book).all()
    return all_books


@router.get('/{book_id}', response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_book_by_id(book_id : int, db : Session = Depends(get_db)):
    requested_book = db.query(Book).where(Book.book_id == book_id).first()
    
    if not requested_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book with id as {book_id} not found')

    return requested_book

@router.post('/', response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def add_book(new_book_data : BookCreate, db : Session = Depends(get_db)):
    new_book = Book(title=new_book_data.title, price = new_book_data.price)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put('/{book_id}', response_model = BookResponse, status_code=status.HTTP_202_ACCEPTED)
def update_book(book_id : int, book_data : BookUpdate, db : Session = Depends(get_db)):
    existing_book = db.query(Book).where(Book.book_id == book_id).first()
    if not existing_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book with id as {book_id} not found')

    update_data = book_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing_book, key, value)
    
    db.commit()
    db.refresh(existing_book)
    return existing_book


@router.delete('/{book_id}', response_model = BookResponse, status_code=status.HTTP_202_ACCEPTED)
def delete_book(book_id : int, db : Session = Depends(get_db)):
    existing_book = db.query(Book).where(Book.book_id == book_id).first()
    if not existing_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book with id as {book_id} not found')
    
    db.delete(existing_book)
    db.commit()
    return existing_book
    
