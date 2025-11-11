from fastapi import HTTPException
from app.core.exceptions.error_response import ErrorResponse


class BaseAPIException(HTTPException):
    def __init__(self, status_code: int, code: str, message: str, details: str | None = None):
        error = ErrorResponse(code=code, message=message, details=details)
        super().__init__(status_code=status_code, detail=error.model_dump())
