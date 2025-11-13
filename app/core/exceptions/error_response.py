"""
Error Response Model

This module defines the `ErrorResponse` Pydantic model used to standardize error responses
across the API. It provides a structured format for returning error information to clients.

Attributes:
    code (str): A unique error code that can be used programmatically to identify the error.
    message (str): A human-readable message describing the error.
    details (Optional[str]): Optional additional information about the error.
"""
from typing import Optional
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    """
    Standardized error response model for API exceptions.

    Attributes:
        code (str): Unique error code for the error.
        message (str): Human-readable error message.
        details (Optional[str]): Optional additional details about the error.
    
    Example:
        {
            "code": "AUTH_INVALID_TOKEN",
            "message": "Invalid authentication token",
            "details": "Token expired or malformed"
        }
    """
    code: str
    message: str
    details: Optional[str] = None
