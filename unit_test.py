from sqlalchemy.orm import Session
from database import get_db
import crud, schemas, models
from datetime import datetime, timedelta

# Create a DB session
db: Session = next(get_db())


# Delete any old "New Test Book" from Author X to prevent duplicates
#old_books = crud.search_books(db, title="New Test Book", author="Author X")
#for book in old_books:
#    crud.delete_book(db, book.id)
print("Cleaning up all existing books before running tests...")
db.query(models.Book).delete()
db.commit()


# --- TEST CREATE ---
print("=== CREATE BOOK ===")
try:
    # Use a unique ISBN to avoid conflicts
    new_book = schemas.BookCreate(
        title="New Test Book",
        author="Author X",
        isbn=f"999-test-{datetime.now().timestamp()}",  # unique
        published_date="2025-08-01"
    )
    created_book = crud.create_book(db, new_book)
    if not created_book:
        raise Exception("Book creation failed - maybe it already exists")
    print("Created book:", created_book)
except Exception as e:
    print("Error creating book:", e)


# --- TEST READ ---
print("\n=== READ BOOKS ===")
books = crud.get_books(db)
for book in books[:5]:
    print(book)


# --- TEST BORROW BOOK ---
if created_book:
    print("\n=== BORROW BOOK ===")
    try:
        borrowed_book = crud.borrow_book(db, created_book.id)
        if borrowed_book:
            print("Borrowed book:", borrowed_book)
        else:
            print("Book cannot be borrowed (maybe already borrowed)")
    except Exception as e:
        print("Error borrowing book:", e)
else:
    print("\nSkipping BORROW - book was not created")


# --- TEST UPDATE ---
if created_book:
    print("\n=== UPDATE BOOK ===")
    try:
        update_data = schemas.BookUpdate(
            status="borrowed",
            borrowed_until=(datetime.today() + timedelta(days=7)).date()
        )
        updated_book = crud.update_book(db, created_book.id, update_data)
        print("Updated book:", updated_book)
    except Exception as e:
        print("Error updating book:", e)
else:
    print("\nSkipping UPDATE - book was not created")


# --- TEST SEARCH BY AUTHOR / TITLE ---
print("\n=== SEARCH BOOKS ===")
try:
    author_search = crud.search_books(db, author="Author X")
    print(f"Books by 'Author X': {author_search}")

    title_search = crud.search_books(db, title="New Test Book")
    print(f"Books titled 'New Test Book': {title_search}")
except Exception as e:
    print("Error searching books:", e)


# --- TEST SERIES AVAILABILITY ---
print("\n=== SERIES AVAILABILITY ===")
# Use IDs of 3 existing books from your 15 inserted books
try:
    # Use IDs of 3 existing books (from your inserted test data)
    series_ids = [1, 2, 3]
    check_date = (datetime.today() + timedelta(days=1)).date()
    available = crud.check_series_availability(db, series_ids, check_date)
    print(f"Series {series_ids} available on {check_date}: {available}")
except Exception as e:
    print("Error checking series availability:", e)


# --- TEST DELETE ---
if created_book:
    print("\n=== DELETE BOOK ===")
    try:
        deleted_book = crud.delete_book(db, created_book.id)
        if not deleted_book:
            print("Book deletion failed")
        else:
            print("Deleted book:", deleted_book)
    except Exception as e:
        print("Error deleting book:", e)
else:
    print("\nSkipping DELETE - book was not created")


# Close the DB session
db.close()
