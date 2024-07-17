from fastapi import APIRouter
from .schemas import UserCreateModel

auth_router = APIRouter()


@auth_router.post("/signup")
async def create_user_account(user: UserCreateModel):
    pass
