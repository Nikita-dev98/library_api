import pytest
from fastapi.testclient import TestClient
from fast_api import app

client = TestClient(app)

# create a book
def test_create_book():
    response = client.post(
        "/books/",
        json={
            "title": "Unit Test Book",
            "author": "Author UT",
            "isbn": "999-ut-001",
            "published_date": "2025-08-20",
            "status": "available"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Unit Test Book"
    assert data["status"] == "available"


# read all books
def test_read_books():
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


# read a single book
def test_read_single_book():
    create_resp = client.post( "/books/",
        json={
            "title": "Single Book",
            "author": "Author X",
            "isbn": "999-ut-002",
            "published_date": "2025-08-20"
        }
    )
    book_id = create_resp.json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id


# update a book
def test_update_book():
    create_resp = client.post(
        "/books/",
        json={
            "title": "Update Test",
            "author": "Author UT",
            "isbn": "999-ut-003",
            "published_date": "2025-08-20"
        }
    )
    book_id = create_resp.json()["id"]

    response = client.put(f"/books/{book_id}",
        json={"status": "borrowed"})
    assert response.status_code == 200
    assert response.json()["status"] == "borrowed"


# borrow a book
def test_borrow_book():
    create_resp = client.post(
        "/books/",
        json={
            "title": "Borrow Test",
            "author": "Author UT",
            "isbn": "999-ut-004",
            "published_date": "2025-08-20"
        }
    )
    book_id = create_resp.json()["id"]

    # borrow first time
    response = client.post(f"/books/{book_id}/borrow/")
    assert response.status_code == 200
    assert response.json()["status"] == "borrowed"

    # borrow again should fail
    response2 = client.post(f"/books/{book_id}/borrow/")
    assert response2.status_code == 400


# search books
def test_search_books():
    response = client.get("/books/search/?title=Unit Test Book")
    assert response.status_code == 200
    data = response.json()
    assert any("Unit Test Book" in book["title"] for book in data)


# delete a book
def test_delete_book():
    create_resp = client.post(
            "/books/",
            json={
                "title": "Delete Test",
                "author": "Author UT",
                "isbn": "999-ut-005",
                "published_date": "2025-08-20"
            }
        )
    book_id = create_resp.json()["id"]

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id

    response2 = client.get(f"/books/{book_id}")
    assert response2.status_code == 404


# series availability
def test_series_availability():
    b1 = client.post("/books/", json={"title": "Series1", "author": "A", "isbn": "999-ut-006", "published_date": "2025-08-20"}).json()["id"]
    b2 = client.post("/books/", json={"title": "Series2", "author": "A", "isbn": "999-ut-007", "published_date": "2025-08-20"}).json()["id"]

    response = client.post("/books/series_availability/", json={
        "book_ids": [b1, b2],
        "check_date": "2025-08-21"
    })
    assert response.status_code == 200
    assert "available" in response.json()