from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status


class BooklyException(Exception):
    """This is the base class for all Bookly exceptions."""

    pass


class InvalidToken(BooklyException):
    """User has provided an invalid or expired token."""

    pass


class RevokedToken(BooklyException):
    """User has provided a revoked token."""

    pass


class AccessTokenRequired(BooklyException):
    """User has provide a refresh token instead of an access token."""

    pass


class RefreshTokenRequired(BooklyException):
    """User has provide an access token instead of a refresh token."""

    pass


class UserAlreadyExists(BooklyException):
    """User with the given email already exists."""

    pass


class InvalidCredentials(BooklyException):
    """User has provided wrong email or password."""

    pass


class InsufficientPermissions(BooklyException):
    """User does not have the required permissions to perform the action."""

    pass


class BookNotFound(BooklyException):
    """Book not found."""

    pass


class AccountNotVerified(Exception):
    """Account not verified."""

    pass


class TagNotFound(BooklyException):
    """Tag not found."""

    pass


class UserNotFound(BooklyException):
    """User not found."""

    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BooklyException):
        return JSONResponse(status_code=status_code, content=initial_detail)

    return exception_handler


def register_all_errors(app: FastAPI):
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

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account not verified.",
                "error_code": "account_not_verified",
                "resolution": "Please check your email for verification details.",
            },
        ),
    )
