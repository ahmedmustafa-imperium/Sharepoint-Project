"""
This module contains functions for authenticating to Microsoft Graph using MSAL
and retrieving an access token for application-level operations on SharePoint.
"""
import msal
from common.settings import get_settings

_settings = get_settings()

def get_token() -> str:
    """
    Acquire an access token from Azure AD using MSAL Confidential Client.

    This uses the Client Credential flow (no user sign-in). 
    It first tries silent cache token, if not found then requests a new one.

    Returns:
        str: Access token string.

    Raises:
        RuntimeError: If token could not be obtained.
    """
    app = msal.ConfidentialClientApplication(
        _settings.CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{_settings.TENANT_ID}",
        client_credential=_settings.CLIENT_SECRET
    )

    scope = ["https://graph.microsoft.com/.default"]

    # try from cache
    result = app.acquire_token_silent(scope, account=None)

    # if not in cache → request from Azure AD
    if not result:
        result = app.acquire_token_for_client(scopes=scope)

    # validate
    if "access_token" not in result:
        raise RuntimeError(f"Failed to obtain access token: {result.get('error_description')}")

    return result["access_token"]
