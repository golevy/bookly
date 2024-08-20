from fastapi import APIRouter, Depends
from src.db.models import User
from src.db.main import get_session
from src.auth.dependencies import get_current_user
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel
from .service import ReviewService

review_router = APIRouter()
review_service = ReviewService()


@review_router.post("/book/{book_id}")
async def add_review_to_books(
    book_id: str,
    review_data: ReviewCreateModel,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    new_review = await review_service.add_review_to_book(
        session=session,
        user_email=current_user.email,
        book_id=book_id,
        review_data=review_data,
    )

    return new_review
