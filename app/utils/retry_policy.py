import asyncio
import random
from typing import Callable


async def retry_async(
    func: Callable,
    exceptions: tuple = (Exception,),
    max_attempts: int = 4,
    base_delay: float = 0.5,
    max_delay: float = 8.0,
    *args,
    **kwargs,
):
    """
    Generic retry with exponential backoff + jitter for async callables.
    Retries only when one of `exceptions` is raised.
    """
    attempt = 0
    while True:
        try:
            return await func(*args, **kwargs)
        except exceptions as exc:
            attempt += 1
            if attempt >= max_attempts:
                raise
            delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
            jitter = random.uniform(0, delay * 0.1)
            await asyncio.sleep(delay + jitter)
