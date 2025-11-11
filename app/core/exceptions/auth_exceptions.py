from fastapi import status
from app.core.exceptions.base_exceptions import BaseAPIException


class InvalidTokenHeaderException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_INVALID_TOKEN_HEADER",
            message="Invalid token header",
        )


class TokenKeyNotFoundException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_TOKEN_KEY_NOT_FOUND",
            message="Token key not found",
        )


class TokenException(BaseAPIException):
    def __init__(self, exc: Exception):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_TOKEN_EXCEPTION",
            message=str(exc),
        )


class MissingAuthorizationHeaderException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_MISSING_HEADER",
            message="Missing Authorization header",
        )


class InvalidAuthorizationHeaderException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_INVALID_HEADER",
            message="Invalid Authorization header",
        )
