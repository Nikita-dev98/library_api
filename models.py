from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import relationship
from datetime import date
import enum

from database import Base

# Book status options
class BookStatus(str, enum.Enum):
    available = "available"
    borrowed = "borrowed"
    reserved = "reserved"

# Book model = book table on db
class Book(Base):
    __tablename__ = "books"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, nullable=False, index=True)
    published_date = Column(Date, nullable=False)

    status = Column(Enum(BookStatus), default=BookStatus.available)

    borrowed_until = Column(Date, nullable=True)
    reserved_until = Column(Date, nullable=True)

    # debugging purpose
    def __repr__(self):
        return f"<Book(title={self.title}, author={self.author}, isbn={self.isbn}, status={self.status})>"

