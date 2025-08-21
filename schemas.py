from pydantic import BaseModel, Field, constr
from datetime import datetime, date
from typing import Optional, List

class SeriesAvailabilityRequest(BaseModel):
    book_ids: List[int]
    check_date: str

# schema for book creation
class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    published_date: date
    status: Optional[str] = "available"

# schmea for book updation
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    published_date: Optional[date] = None
    status: Optional[str] = None
    borrowed_until: Optional[date] = None

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    published_date: date
    status: str
    borrowed_until: Optional[date]

    class Config:
        orm_mode = True
