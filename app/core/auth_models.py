"""
Models for token request/response and helpers for token expiry checks.
"""
import time
from pydantic import BaseModel

class TokenResponse(BaseModel):
    """
    Model representing an OAuth token response returned by Azure AD.
    """
    access_token: str
    expires_in: int
    token_type: str
    def is_expiring_soon(self, buffer_seconds: int = 60) -> bool:
        """
        Return True if token will expire in less than `buffer_seconds`.
        Default buffer = 60 seconds.
        """
        expire_time = int(time.time())+ self.expires_in
        return (expire_time - buffer_seconds) <= int(time.time())

class TokenRequest(BaseModel):
    """
    Data required to request an access token from Azure AD.
    """
    client_id: str
    client_secret: str
    scope: str
