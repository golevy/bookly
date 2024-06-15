from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from src.books.models import Book
from sqlmodel import select, desc


class BookService:
    async def find_all(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)

        return result.all()

    async def find_one(self, session: AsyncSession, book_id: str):
        statement = select(Book).where(Book.id == book_id)
        result = await session.exec(statement)
        book = result.first()

        return book if book is not None else None

    async def create(self, session: AsyncSession, book_data: BookCreateModel):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)

        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)

        return new_book

    async def update(
        self, session: AsyncSession, book_id: str, update_data: BookUpdateModel
    ):
        book_to_update = await self.find_one(session, book_id)

        if book_to_update is not None:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(book_to_update, k, v)
            await session.commit()
            await session.refresh(book_to_update)

            return book_to_update
        else:
            return None

    async def delete(self, session: AsyncSession, book_id: str):
        book_to_delete = await self.find_one(session, book_id)

        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()

            return {}
        else:
            return None
