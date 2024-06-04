from fastapi import FastAPI, Header, status
from fastapi.exceptions import HTTPException
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

HEADER_ACCEPT = "Accept"
HEADER_CONTENT_TYPE = "Content-Type"
HEADER_USER_AGENT = "User-Agent"
HEADER_HOST = "Host"


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: str
    language: str


class BookUpdateRequest(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: str
    language: str


# Mock data
books = [
    {
        "id": 1,
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "publisher": "Little, Brown and Company",
        "published_date": "July 16, 1951",
        "page_count": "277",
        "language": "English",
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publisher": "J. B. Lippincott & Co.",
        "published_date": "July 16, 1960",
        "page_count": "304",
        "language": "English",
    },
]


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/greet")
async def greet_name(name: Optional[str] = "User", age: int = 0) -> dict:
    return {"message": f"Hello {name}", "age": age}


@app.get("/get_headers", status_code=status.HTTP_200_OK)
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None),
):
    request_headers = {}
    request_headers[HEADER_ACCEPT] = accept
    request_headers[HEADER_CONTENT_TYPE] = content_type
    request_headers[HEADER_USER_AGENT] = user_agent
    request_headers[HEADER_HOST] = host

    return request_headers


@app.get("/books", response_model=List[Book], status_code=status.HTTP_200_OK)
async def find_all():
    return books


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create(book_data: Book) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)

    return new_book


@app.get("/book/{book_id}")
async def find_by_id(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.patch("/book/{book_id}")
async def update_by_id(book_id: int, book_update_data: BookUpdateRequest) -> dict:
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update_data.title
            book["author"] = book_update_data.author
            book["publisher"] = book_update_data.publisher
            book["page_count"] = book_update_data.page_count
            book["language"] = book_update_data.language

            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/book/{book_id}")
async def delete_by_id(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

            return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
