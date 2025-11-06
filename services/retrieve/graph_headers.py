"""
graph_headers.py

Provides helper functions for generating Microsoft Graph HTTP headers
with a valid bearer access token.
"""

from __future__ import annotations
from auth.msal_token import get_token
from common.settings import get_settings

_settings = get_settings()


def _graph_headers() -> dict[str, str]:
    """
    Generate and return http headers for Microsoft Graph API.

    Returns:
        dict[str, str]: Dictionary containing Authorization, Accept, and Content-Type headers.
    """
    access_token = get_token()
    # print(access_token)

    # Saving token to file for debugging purposes
    with open("access_token.txt", "w", encoding="utf-8") as f:
        f.write(access_token)

    return {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }