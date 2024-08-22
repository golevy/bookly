from fastapi import FastAPI, status
from src.books.routes import book_router
from src.demo.routes import demo_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.errors import (
    create_exception_handler,
    InvalidCredentials,
    BookNotFound,
    UserAlreadyExists,
    UserNotFound,
    InsufficientPermissions,
    AccessTokenRequired,
    InvalidToken,
    RefreshTokenRequired,
    RevokedToken,
)


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"========================")
    print(f"🚀 Server is starting...")
    await init_db()
    print(f"========================")
    yield
    print(f"========================")
    print(f"🚀 Server has been stopped")
    print(f"========================")


version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version=version,
)

app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "User with the given email already exists.",
            "error_code": "user_already_exists",
        },
    ),
)

app.add_exception_handler(
    UserNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "User not found.",
            "error_code": "user_not_found",
        },
    ),
)

app.add_exception_handler(
    BookNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Book not found.",
            "error_code": "book_not_found",
        },
    ),
)

app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        initial_detail={
            "message": "Invalid email or password.",
            "error_code": "invalid_email_or_password",
        },
    ),
)

app.add_exception_handler(
    InvalidToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Token is invalid or expired.",
            "error_code": "invalid_token",
        },
    ),
)

app.add_exception_handler(
    RevokedToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Token has been revoked.",
            "error_code": "revoked_token",
        },
    ),
)

app.add_exception_handler(
    AccessTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Access token is required.",
            "error_code": "access_token_required",
        },
    ),
)

app.add_exception_handler(
    RefreshTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Refresh token is required.",
            "error_code": "refresh_token_required",
        },
    ),
)

app.add_exception_handler(
    InsufficientPermissions,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "User does not have the required permissions to perform the action.",
            "error_code": "insufficient_permissions",
        },
    ),
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(demo_router, prefix=f"/api/{version}/demo", tags=["demo"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
