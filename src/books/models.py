from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4()
        )
    )
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: str
    language: str
    created_at: datetime = Field(
        Column(pg.TIMESTAMP, nullable=False, default=datetime.now())
    )
    updated_at: datetime = Field(
        Column(pg.TIMESTAMP, nullable=False, default=datetime.now())
    )

    def __repr__(self) -> str:
        return f"<Book {self.title}>"
