"""
This module provides the AuthService class which is responsible for
acquiring Azure AD access tokens using the client 
credentials flow. It integrates with a TokenCache to store tokens 
in memory (or Redis if configured) to avoid unnecessary network 
calls when a valid token already exists.
"""

import logging
from dataclasses import dataclass
import asyncio
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from app.utils.token_cache import TokenCache
from app.core.auth_models import TokenResponse
from app.core.config import settings

load_dotenv()
logger = logging.getLogger(__name__)
@dataclass
class AuthService:
    """
    Service responsible for acquiring Azure AD Access Tokens
    using Azure's DefaultAzureCredential chain.

    This service automatically supports multiple authentication methods such as:
    - Environment variables (client ID, client secret, tenant ID)
    - Managed Identity (Azure-hosted environment)
    - Azure CLI / Visual Studio authentication (for local development)

    The token is cached via TokenCache to minimize redundant requests.
    """
    
    token_cache: TokenCache
    
    def __post_init__(self):
        """
        Initialize the DefaultAzureCredential instance.
        This automatically picks the most appropriate authentication source.
        """
        self.credential = DefaultAzureCredential()
        


    async def get_client_credentials_token(self) -> TokenResponse:
        """
        Acquire an access token using DefaultAzureCredential.

        Uses the cache if a valid token exists and is not expiring soon.
        Otherwise, requests a fresh token from Azure AD.

        Returns:
            TokenResponse: A structured response containing the access token details.
        """
        # Return cached token if still valid
        cached = await self.token_cache.get_token_response()
        if cached and not cached.is_expiring_soon(settings.TOKEN_REFRESH_BUFFER_SECONDS):
            logger.debug("Using cached token from memory")
            return cached

        # Acquire new token asynchronously
        logger.debug("Requesting new access token via DefaultAzureCredential")
        loop = asyncio.get_running_loop()
        token = await loop.run_in_executor(None, self._acquire_token_sync)

        token_resp = TokenResponse(
            access_token=token.token,
            expires_in=int(token.expires_on - asyncio.get_event_loop().time()),
            token_type="Bearer"
        )
        await self.token_cache.set_token_response(token_resp)
        
        return token_resp

   
    def _acquire_token_sync(self):
        """
        Acquire a new access token synchronously using DefaultAzureCredential.

        Returns:
            AccessToken: The Azure SDK AccessToken object containing token and expiry info.
        """
        # Request Microsoft Graph scope
        return self.credential.get_token("https://graph.microsoft.com/.default")