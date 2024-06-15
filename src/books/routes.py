from fastapi import APIRouter, status, Depends
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import BookModel, BookCreateModel, BookUpdateModel
from src.books.service import BookService
from src.db.main import get_session
from fastapi.exceptions import HTTPException

book_router = APIRouter()
book_service = BookService()


@book_router.get("/", response_model=List[BookModel], status_code=status.HTTP_200_OK)
async def find_all(session: AsyncSession = Depends(get_session)):
    books = await book_service.find_all(session)
    return books


@book_router.post("/", response_model=BookModel, status_code=status.HTTP_201_CREATED)
async def create(
    book_data: BookCreateModel, session: AsyncSession = Depends(get_session)
) -> dict:
    new_book = await book_service.create(session, book_data)

    return new_book


@book_router.get("/{book_id}", response_model=BookModel, status_code=status.HTTP_200_OK)
async def find_one(book_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.find_one(session, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    else:
        return book


@book_router.patch(
    "/{book_id}", response_model=BookModel, status_code=status.HTTP_200_OK
)
async def update(
    book_id: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    update_book = await book_service.update(session, book_id, book_update_data)

    if update_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    else:
        return update_book


@book_router.delete("/{book_id}")
async def delete(book_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    book_to_delete = await book_service.delete(session, book_id)

    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    else:
        return {}
