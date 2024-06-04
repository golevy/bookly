from fastapi import FastAPI, Header
from typing import Optional, List
from pydantic import BaseModel
from starlette.status import HTTP_200_OK

app = FastAPI()

HEADER_ACCEPT = "Accept"
HEADER_CONTENT_TYPE = "Content-Type"
HEADER_USER_AGENT = "User-Agent"
HEADER_HOST = "Host"


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/greet")
async def greet_name(name: Optional[str] = "User", age: int = 0) -> dict:
    return {"message": f"Hello {name}", "age": age}


class BookCreateModel(BaseModel):
    title: str
    author: str


@app.post("/create_book")
async def create_book(book_data: BookCreateModel):
    return {"title": book_data.title, "author": book_data.author}


@app.get("/get_headers", status_code=HTTP_200_OK)
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


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: str
    language: str


@app.get("/books", response_model=List[Book])
async def get_all_books():
    pass


@app.post("/books")
async def create_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()
    pass


@app.get("/books/{book_id}")
async def get_book(book_id: int) -> dict:
    pass
