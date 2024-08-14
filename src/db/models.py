from typing import List, Optional
from sqlmodel import SQLModel, Field, Column, Relationship
from cuid import cuid
from datetime import date, datetime, timezone
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: str = Field(
        default_factory=cuid,
        sa_column=Column(
            pg.VARCHAR,
            nullable=False,
            primary_key=True,
        ),
    )
    username: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    email: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    first_name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    last_name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(
        default=False, sa_column=Column(pg.BOOLEAN, nullable=False)
    )
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )
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
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"


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
    user: Optional["User"] = Relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"<Book {self.title}>"
