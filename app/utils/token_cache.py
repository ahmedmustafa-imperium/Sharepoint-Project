"""
Token cache for storing access tokens.

Right now only use in-memory storage.
This means: as long as the FastAPI process is running, the token is stored.
When server restarts → the token is lost.
"""

import asyncio
from typing import Optional
from app.core.logging import get_logger
from app.data.auth_models import TokenResponse

logger = get_logger(__name__)

class TokenCache:
    """
    Simple in-memory token cache.
    don't want to fetch a new SharePoint token for every request.
    We fetch once, store it here, and reuse until it expires.
    Only one token is stored at a time for the entire backend process.
    """

    def __init__(self):
        # holds TokenResponse or None
        self._in_memory: Optional[TokenResponse] = None

        # lock to make sure async operations do not overlap
        self._lock = asyncio.Lock()

    async def get_token_response(self) -> Optional[TokenResponse]:
        """
        Return the cached token if it exists.
        If no cached token exists, return None.
        """
        async with self._lock:
            return self._in_memory

    async def set_token_response(self, token: TokenResponse):
        """
        Set the token in the in-memory cache.
        """
        async with self._lock:
            logger.info("Token cached in-memory with expiration = %s seconds", token.expires_in)
            self._in_memory = token
