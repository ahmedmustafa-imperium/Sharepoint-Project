"""
This module provides the SharePointAuthManager class which acts as
an orchestrator between FastAPI endpoints and the AuthService. 

It simplifies token management by:
- Using the AuthService to acquire Azure AD access tokens.
- Caching tokens via TokenCache.
- Providing a single method to get a valid access token for SharePoint or Microsoft Graph API.
"""
import logging
from typing import Optional
from app.services.auth_service import AuthService
from app.utils.token_cache import TokenCache

logger = logging.getLogger(__name__)


class SharePointAuthManager:
    """
    Orchestrator that sits between FastAPI endpoints and AuthService.
    Ensures tokens are cached and provides a single method to get a token.
    """
    def __init__(self, token_cache: Optional[TokenCache] = None):
        """
        Initialize SharePoint auth manager.
        
        Args:
            token_cache: Optional shared token cache instance
        """
        self._token_cache = token_cache or TokenCache()
        self._service = AuthService(self._token_cache)

    async def get_access_token(self) -> str:
        """
        Higher-level method used to obtain tokens.
        """
        token_resp = await self._service.get_client_credentials_token()
        return token_resp.access_token

   
