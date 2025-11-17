"""
Base API Exception

This module defines the `BaseAPIException`, a custom exception class that extends FastAPI's
`HTTPException` to provide structured error responses for the API.

The exception uses `ErrorResponse` to format the error with a consistent structure including:
- `code`: A unique error code for programmatic handling
- `message`: A human-readable error message
- `details`: Optional additional information about the error
"""

from fastapi import HTTPException
from app.core.exceptions.error_response import ErrorResponse


class BaseAPIException(HTTPException):
    """
    Base class for API exceptions with structured error response.

    Args:
        status_code (int): HTTP status code to return.
        code (str): Unique error code for the exception.
        message (str): Human-readable error message.
        details (str | None): Optional additional details about the error.

    Usage:
        raise BaseAPIException(
            status_code=400,
            code="INVALID_INPUT",
            message="The provided input is invalid",
            details="Username cannot be empty"
        )
    """
    def __init__(self, status_code: int, code: str, message: str, details: str | None = None):
        error = ErrorResponse(code=code, message=message, details=details)
        super().__init__(status_code=status_code, detail=error.model_dump())
