from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date, timezone
from cuid import cuid
from typing import Optional


class Book(SQLModel, table=True):
    __tablename__ = "book"

    id: str = Field(
        default_factory=cuid,
        sa_column=Column(
            pg.VARCHAR,
            nullable=False,
            primary_key=True,
        ),
    )
    title: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    author: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    publisher: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    published_date: date = Field(sa_column=Column(pg.DATE, nullable=False))
    page_count: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    language: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    user_id: Optional[str] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=lambda: datetime.now(timezone.utc),
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
        ),
    )

    def __repr__(self) -> str:
        return f"<Book {self.title}>"
