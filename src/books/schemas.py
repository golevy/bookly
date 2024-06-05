from pydantic import BaseModel


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
