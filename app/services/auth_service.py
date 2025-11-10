"""
This module provides the AuthService class which is responsible for
acquiring and refreshing Azure AD access tokens using the client 
credentials flow. It integrates with a TokenCache to store tokens 
in memory (or Redis if configured) to avoid unnecessary network 
calls when a valid token already exists.
"""
import logging
from dataclasses import dataclass
import asyncio
import msal
from app.utils.token_cache import TokenCache
from app.core.auth_models import TokenResponse
from app.core.config import settings


logger = logging.getLogger(__name__)
@dataclass
class AuthService:
    """
    Service responsible for acquiring and refreshing Azure AD Access Tokens
    using Client Credentials flow.

    This service uses a TokenCache to store the token in memory (or Redis).
    If the token already exists in cache and is not close to expiry, it is reused.
    Otherwise, a fresh token is acquired from Azure AD using MSAL.
    """
    token_cache: TokenCache

    async def get_client_credentials_token(self) -> TokenResponse:
        """
        Acquire a token using client credentials flow.
        Use token cache if available and not expiring soon.
        """
        # If cached, return
        cached = await self.token_cache.get_token_response()
        logging.debug(cached)
        if cached and not cached.is_expiring_soon(settings.TOKEN_REFRESH_BUFFER_SECONDS):
            logger.debug("Using cached token")
            return cached

        # Acquire a new token via MSAL (blocking) but run in executor
        loop = asyncio.get_running_loop()
        resp = await loop.run_in_executor(None, self._acquire_token_client_credentials_sync)
        token_resp = TokenResponse(**resp)
        await self.token_cache.set_token_response(token_resp)
        return token_resp
    # Refresh the token if it is about to expire or has already expired
    def _acquire_token_client_credentials_sync(self) -> TokenResponse:
        """
        Perform the actual token request synchronously using MSAL.

        This method is called inside a thread pool executor
        because MSAL is blocking. It sends a request to Azure AD
        with client_id + client_secret + scopes and returns the token.
        """
        app = msal.ConfidentialClientApplication(
            client_id=settings.AZURE_CLIENT_ID,
            client_credential=settings.AZURE_CLIENT_SECRET,
            authority=f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}"
        )
        # scope should be a list per msal: ["https://graph.microsoft.com/.default"]
        scopes = ["https://graph.microsoft.com/.default"]
        result = app.acquire_token_for_client(scopes=scopes)
        if "access_token" not in result:
            logger.error("Failed to acquire token: %s", result)
            raise RuntimeError(f"Token acquisition failed: {result.get('error_description') or result}")
        logger.debug("Acquiring new token")
        return {
            "access_token": result["access_token"],
            "expires_in": result.get("expires_in", 3600),
            "token_type": result.get("token_type", "Bearer")
        }
