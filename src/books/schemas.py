from pydantic import BaseModel
from datetime import datetime
import uuid


class BookModel(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: str
    language: str
    created_at: datetime
    updated_at: datetime


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: str
    language: str
