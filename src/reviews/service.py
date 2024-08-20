from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status
from .schemas import ReviewCreateModel
import logging

user_service = UserService()
book_service = BookService()


class ReviewService:
    async def add_review_to_book(
        self,
        session: AsyncSession,
        user_email: str,
        book_id: int,
        review_data: ReviewCreateModel,
    ):
        try:
            book = await book_service.get_book_by_id(session, book_id)
            user = await user_service.get_user_by_email(session, user_email)
            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)

            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found!",
                )

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found!",
                )

            new_review.user = user
            new_review.book = book
            session.add(new_review)
            await session.commit()

            return new_review
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oops, something went wrong!",
            )
