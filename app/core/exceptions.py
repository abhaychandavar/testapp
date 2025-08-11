from fastapi import HTTPException, status

class BaseAPIException(HTTPException):
    """Base API Exception that can be used to raise HTTP exceptions."""
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: dict = None
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class NotFoundException(BaseAPIException):
    """Exception raised when a resource is not found."""
    def __init__(self, detail: str = "Resource not found") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UnauthorizedException(BaseAPIException):
    """Exception raised when authentication fails."""
    def __init__(self, detail: str = "Not authenticated") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class ForbiddenException(BaseAPIException):
    """Exception raised when user doesn't have permission."""
    def __init__(self, detail: str = "Not enough permissions") -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class ValidationException(BaseAPIException):
    """Exception raised when validation fails."""
    def __init__(self, detail: str = "Validation error") -> None:
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)
