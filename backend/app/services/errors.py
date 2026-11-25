class AppError(Exception):
    """Base domain error for service layer."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class NotFoundError(AppError):
    """Raised when a requested resource is not found."""


class ForbiddenError(AppError):
    """Raised when the user lacks permission for an action."""


class BadRequestError(AppError):
    """Raised when a business rule is violated."""


class ConflictError(AppError):
    """Raised when a resource conflicts with existing state."""


class AuthError(AppError):
    """Raised when authentication fails or credentials are invalid."""
