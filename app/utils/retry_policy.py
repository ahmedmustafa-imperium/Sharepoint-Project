"""
Retry policy utility for handling transient failures in HTTP requests.

Provides exponential backoff retry logic for Microsoft Graph API calls.
"""
import asyncio
import logging
from typing import Callable, TypeVar, Optional

logger = logging.getLogger(__name__)

T = TypeVar('T')


class RetryPolicy:
    """
    Retry policy configuration for HTTP requests.
    """
    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        retryable_status_codes: Optional[list[int]] = None
    ):
        """
        Initialize retry policy.
        
        Args:
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay in seconds before first retry
            max_delay: Maximum delay in seconds between retries
            exponential_base: Base for exponential backoff calculation
            retryable_status_codes: HTTP status codes that should trigger retry
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.retryable_status_codes = retryable_status_codes or [429, 500, 502, 503, 504]

    def should_retry(self, status_code: int, attempt: int) -> bool:
        """
        Determine if a request should be retried based on status code and attempt number.
        
        Args:
            status_code: HTTP status code from the response
            attempt: Current attempt number (0-indexed)
            
        Returns:
            True if request should be retried, False otherwise
        """
        if attempt >= self.max_retries:
            return False
        return status_code in self.retryable_status_codes

    def get_delay(self, attempt: int) -> float:
        """
        Calculate delay before next retry attempt using exponential backoff.
        
        Args:
            attempt: Current attempt number (0-indexed)
            
        Returns:
            Delay in seconds
        """
        delay = self.initial_delay * (self.exponential_base ** attempt)
        return min(delay, self.max_delay)


async def retry_with_policy(
    func: Callable[..., T],
    retry_policy: Optional[RetryPolicy] = None,
    *args,
    **kwargs
) -> T:
    """
    Execute an async function with retry policy.
    
    Args:
        func: Async function to execute
        retry_policy: Retry policy to use (defaults to standard policy)
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func
        
    Returns:
        Result of func execution
        
    Raises:
        Exception: Last exception raised if all retries are exhausted
    """
    if retry_policy is None:
        retry_policy = RetryPolicy()
    
    last_exception = None
    
    for attempt in range(retry_policy.max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            status_code = getattr(e, 'status_code', None)
            
            if status_code and retry_policy.should_retry(status_code, attempt):
                delay = retry_policy.get_delay(attempt)
                logger.warning(
                    f"Request failed with status {status_code}, "
                    f"retrying in {delay}s (attempt {attempt + 1}/{retry_policy.max_retries + 1})"
                )
                await asyncio.sleep(delay)
                continue
            else:
                # Non-retryable error or max retries exceeded
                raise
    
    # Should never reach here, but just in case
    if last_exception:
        raise last_exception
