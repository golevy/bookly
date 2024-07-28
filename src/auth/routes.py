from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from src.db.main import get_session
from .schemas import UserCreateModel, UserLoginModel
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from fastapi.exceptions import HTTPException
from .schemas import UserModel
from .utils import create_access_token, verify_password
from datetime import timedelta

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 30


@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )
    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.post("/login", response_model=UserModel)
async def login_user(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password
    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "id": user.id,
                    "email": user.email,
                }
            )
            refresh_token = create_access_token(
                user_data={
                    "id": user.id,
                    "email": user.email,
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                    },
                }
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid email or password",
    )
