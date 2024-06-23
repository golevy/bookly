from sqlmodel import SQLModel, Field, Column
from cuid import cuid
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, timezone


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
    first_name = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    last_name = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    is_verified: bool = Field(
        default=False, sa_column=Column(pg.BOOLEAN, nullable=False)
    )
    created_at: datetime = Field(
        default_factory=datetime.now(timezone.utc),
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=datetime.now(timezone.utc),
        ),
    )
    updated_at: datetime = Field(
        default_factory=datetime.now(timezone.utc),
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=datetime.now(timezone.utc),
            onupdate=datetime.now(timezone.utc),
        ),
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"
