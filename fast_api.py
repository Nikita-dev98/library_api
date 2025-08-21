from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import crud, models, schemas
from database import get_db, engine
from datetime import datetime
from schemas import SeriesAvailabilityRequest

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API")

#-----CRUD Endpoints-----

# book creation
@app.post("/books/", response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    created = crud.create_book(db, book)
    if not created:
        raise HTTPException(status_code=400, detail="Book already exists")
    return created


# read all books
@app.get("/books/", response_model=List[schemas.BookOut])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit)

# read a single book
@app.get("/books/{book_id}", response_model=schemas.BookOut)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# update a book
@app.put("/books/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    updated = crud.update_book(db, book_id, book_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

# delete a book
@app.delete("/books/{book_id}", response_model=schemas.BookOut)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted

# search books by author or title
@app.get("/books/search/", response_model=List[schemas.BookOut])
def search_books(author: Optional[str] = None, title: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.search_books(db, author=author, title=title)

# check series availability
@app.post("/books/series_availability/")
def series_availability(request: SeriesAvailabilityRequest, db: Session = Depends(get_db)):
    date_obj = datetime.strptime(request.check_date, "%Y-%m-%d").date()
    available = crud.check_series_availability(db, request.book_ids, date_obj)
    return {"available": available}

# borrow a book
@app.post("/books/{book_id}/borrow/", response_model=schemas.BookOut)
def borrow_book(book_id: int, db: Session = Depends(get_db)):
    borrowed = crud.borrow_book(db, book_id)
    if not borrowed:
        raise HTTPException(status_code=400, detail="Book cannot be borrowed (maybe already borrowed)")
    return borrowed