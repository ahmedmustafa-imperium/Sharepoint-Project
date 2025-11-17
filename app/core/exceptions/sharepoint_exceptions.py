"""
SharePoint API Exceptions

This module defines custom exceptions for handling SharePoint Graph API errors.
All exceptions inherit from `BaseAPIException` and provide structured error responses
with specific HTTP status codes, error codes, and messages.

Includes:
- Generic SharePoint API exception
- Resource not found
- Permission denied
- Rate limiting
- Utility function to map raw Graph API errors to the corresponding exception
"""

from fastapi import status
from app.core.exceptions.base_exceptions import BaseAPIException


class SharePointAPIException(BaseAPIException):
    """
    Generic exception for SharePoint Graph API failures.

    Args:
        message (str): Human-readable error message.
        code (str, optional): Unique error code. Defaults to "SHAREPOINT_API_ERROR".
        status_code (int, optional): HTTP status code. Defaults to 502 Bad Gateway.
        details (str | None, optional): Additional details about the error.
    """
    def __init__(
        self,
        *,
        message: str,
        code: str = "SHAREPOINT_API_ERROR",
        status_code: int = status.HTTP_502_BAD_GATEWAY,
        details: str | None = None,
    ):
        super().__init__(status_code=status_code, code=code, message=message, details=details)


class SharePointResourceNotFoundException(SharePointAPIException):
    """
    Raised when a requested SharePoint resource is not found (HTTP 404).

    Args:
        message (str, optional): Human-readable error message. Defaults to
            "SharePoint resource not found".
        details (str | None, optional): Optional additional details about the error.
    """
    def __init__(
        self, *,
        message: str = "SharePoint resource not found", details: str | None = None):
        super().__init__(
            message=message,
            code="SHAREPOINT_RESOURCE_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


class SharePointPermissionDeniedException(SharePointAPIException):
    """
    Raised when access to a SharePoint resource is denied (HTTP 403).

    Args:
        message (str, optional): Human-readable error message. Defaults to
            "Access to SharePoint resource is denied".
        details (str | None, optional): Optional additional details about the error.
    """
    def __init__(
        self, *,
        message: str = "Access to SharePoint resource is denied", details: str | None = None):
        super().__init__(
            message=message,
            code="SHAREPOINT_PERMISSION_DENIED",
            status_code=status.HTTP_403_FORBIDDEN,
            details=details,
        )


class SharePointRateLimitException(SharePointAPIException):
    """
    Raised when SharePoint rate limits are exceeded (HTTP 429).

    Args:
        message (str, optional): Human-readable error message. Defaults to
            "SharePoint rate limit exceeded".
        details (str | None, optional): Optional additional details about the error.
    """
    def __init__(
        self, *,
        message: str = "SharePoint rate limit exceeded", details: str | None = None):
        super().__init__(
            message=message,
            code="SHAREPOINT_RATE_LIMITED",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details=details,
        )


def map_graph_error(
    operation: str, *,
    status_code: int,
    details: str | None = None) -> SharePointAPIException:
    """
    Map a raw Graph API failure to a specific SharePoint API exception.

    Args:
        operation (str): Description of the operation being attempted (for context in the error message).
        status_code (int): HTTP status code returned from Graph API.
        details (str | None): Optional additional details about the failure.

    Returns:
        SharePointAPIException: A specific exception corresponding to the error type.
            - 404 -> SharePointResourceNotFoundException
            - 403 -> SharePointPermissionDeniedException
            - 429 -> SharePointRateLimitException
            - Others -> SharePointAPIException
    """
    if status_code == status.HTTP_404_NOT_FOUND:
        return SharePointResourceNotFoundException(
            message=f"SharePoint resource not found while attempting to {operation}",
            details=details,
        )
    if status_code == status.HTTP_403_FORBIDDEN:
        return SharePointPermissionDeniedException(
            message=f"Permission denied while attempting to {operation}",
            details=details,
        )
    if status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        return SharePointRateLimitException(
            message=f"Rate limit exceeded while attempting to {operation}",
            details=details,
        )

    return SharePointAPIException(
        message=f"SharePoint API request failed while attempting to {operation}",
        status_code=status_code or status.HTTP_502_BAD_GATEWAY,
        details=details,
    )
