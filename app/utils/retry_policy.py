import asyncio
import functools
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)

def retry(max_attempts: int = 3, base_delay: float = 10.0, exceptions: tuple = (Exception,)):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.warning("Attempt %s failed for %s: %s. Retrying after %.2fs", attempt, func.__name__, exc, delay)
                    await asyncio.sleep(delay)
            logger.error("All %d attempts failed for %s", max_attempts, func.__name__)
            raise last_exc
        return wrapper
    return decorator
