from fastapi import APIRouter, status, Depends
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import (
    BookModel,
    BookCreateModel,
    BookUpdateModel,
    BookDetailModel,
)
from src.books.service import BookService
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.errors import BookNotFound


book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin"]))


@book_router.get(
    "/",
    response_model=List[BookModel],
    status_code=status.HTTP_200_OK,
    dependencies=[role_checker],
)
async def find_all(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    books = await book_service.find_all(session)

    return books


@book_router.get(
    "/user/{user_id}",
    response_model=List[BookModel],
    status_code=status.HTTP_200_OK,
    dependencies=[role_checker],
)
async def get_user_book_submissions(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    books = await book_service.get_user_books(session, user_id)

    return books


@book_router.post(
    "/",
    response_model=BookModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[role_checker],
)
async def create(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    user_id = token_details.get("user")["id"]
    new_book = await book_service.create(session, book_data, user_id)
    return new_book


@book_router.get(
    "/{book_id}",
    response_model=BookDetailModel,
    status_code=status.HTTP_200_OK,
    dependencies=[role_checker],
)
async def find_one(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    book = await book_service.get_book_by_id(session, book_id)
    if book is None:
        raise BookNotFound()
    return book


@book_router.patch(
    "/{book_id}",
    response_model=BookModel,
    status_code=status.HTTP_200_OK,
    dependencies=[role_checker],
)
async def update(
    book_id: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    updated_book = await book_service.update(session, book_id, book_update_data)
    if updated_book is None:
        raise BookNotFound()
    return updated_book


@book_router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[role_checker],
)
async def delete(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    book_to_delete = await book_service.delete(session, book_id)

    if book_to_delete is None:
        raise BookNotFound()

    return {}
