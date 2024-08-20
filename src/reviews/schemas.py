from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReviewModel(BaseModel):
    id: str
    rating: int = Field(lt=5)
    review_text: str
    user_id: Optional[str]
    book_id: Optional[str]
    created_at: datetime
    updated_at: datetime


class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=5)
    review_text: str
