from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List, Optional
import models, schemas

# ----------CREATE---------
def create_book(db: Session, book: schemas.BookCreate):
    existing = db.query(models.Book).filter(
        models.Book.isbn == book.isbn,
        models.Book.title == book.title,
        models.Book.author == book.author,
        models.Book.published_date == book.published_date
    ).first()

    if existing:
        return None
    
    db_book = models.Book(
        title = book.title,
        author = book.author,
        isbn = book.isbn,
        published_date = book.published_date,
        status = book.status
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# ----------READ----------
def get_book(db: Session, book_id:int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()

def search_books(db: Session, title: Optional[str] = None, author: Optional[str] = None):
    query = db.query(models.Book)
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    return query.all()

#def get_books_by_author(db: Session, author_name: str):
#    return search_books(db, author=author_name)

#def get_books_by_title(db: Session, title_name: str):
#    return search_books(db, title=title_name)

# --------UPDATE---------
def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return None
    
    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book

# -------DELETE---------
def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book

# ------BORROW BOOK-----------
def borrow_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book or db_book.status == "borrowed":
       return None
    print(f"Borrowing book id={book_id}, current status={db_book.status}")

    db_book.status = "borrowed"
    db_book.borrowed_until = date.today() + timedelta(days=7)
    db.commit()
    db.refresh(db_book)
    return db_book

# --------FANCY SEARCH---------
def check_series_availability(db: Session, book_ids: List[int], check_date: date):
    books = db.query(models.Book).filter(models.Book.id.in_(book_ids)).all()
    if len(books) != len(book_ids):
        return False # some books dont exist
    for book in books:
        if book.status == "borrowed" and book.borrowed_until >= check_date:
            return False # not available on that date
    return True