from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse


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
