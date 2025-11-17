"""
Logging filters for the Todo API.
Adds contextual information to log records.
"""

import logging
import uuid
from contextvars import ContextVar
from typing import Optional

# Context variable to store request ID
_request_id: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


def set_request_id(request_id: str) -> None:
    """Set the request ID for the current context."""
    _request_id.set(request_id)


def get_request_id() -> Optional[str]:
    """Get the current request ID."""
    return _request_id.get()


def generate_request_id() -> str:
    """Generate a unique request ID."""
    return str(uuid.uuid4())


class ContextFilter(logging.Filter):
    """
    Filter that adds contextual information to log records.
    Includes request ID and other relevant context.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Add context to log record.
 
        Args:
            record (logging.LogRecord): The log record to filter.
 
        Returns:
            bool: True to allow the record to be logged.
        """
        request_id = get_request_id()
        if request_id:
            record.request_id = request_id
        else:
            record.request_id = "N/A"

        return True
    