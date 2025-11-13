"""
Authentication Exception Classes

This module defines custom exceptions for handling authentication and token-related errors
in the API. All exceptions inherit from `BaseAPIException` and provide specific HTTP status codes,
error codes, and messages for different authentication failure scenarios.
"""

from fastapi import status
from app.core.exceptions.base_exceptions import BaseAPIException


class InvalidTokenHeaderException(BaseAPIException):
    """
    Raised when the token header provided in the request is invalid.
    
    Returns:
        HTTP 401 Unauthorized
        Code: AUTH_INVALID_TOKEN_HEADER
        Message: "Invalid token header"
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_INVALID_TOKEN_HEADER",
            message="Invalid token header",
        )


class TokenKeyNotFoundException(BaseAPIException):
    """
    Raised when the expected token key is not found in the request.
    
    Returns:
        HTTP 401 Unauthorized
        Code: AUTH_TOKEN_KEY_NOT_FOUND
        Message: "Token key not found"
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_TOKEN_KEY_NOT_FOUND",
            message="Token key not found",
        )


class TokenException(BaseAPIException):
    """
    Raised when a general exception occurs while processing the token.
    
    Args:
        exc (Exception): The original exception that was caught.

    Returns:
        HTTP 401 Unauthorized
        Code: AUTH_TOKEN_EXCEPTION
        Message: The string representation of the original exception
    """
    def __init__(self, exc: Exception):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_TOKEN_EXCEPTION",
            message=str(exc),
        )


class MissingAuthorizationHeaderException(BaseAPIException):
    """
    Raised when the Authorization header is missing from the request.
    
    Returns:
        HTTP 401 Unauthorized
        Code: AUTH_MISSING_HEADER
        Message: "Missing Authorization header"
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_MISSING_HEADER",
            message="Missing Authorization header",
        )


class InvalidAuthorizationHeaderException(BaseAPIException):
    """
    Raised when the Authorization header is malformed or invalid.
    
    Returns:
        HTTP 401 Unauthorized
        Code: AUTH_INVALID_HEADER
        Message: "Invalid Authorization header"
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_INVALID_HEADER",
            message="Invalid Authorization header",
        )
