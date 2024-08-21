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
