"""
drive_id.py

Provides helper function to resolve a Drive ID (document library ID)
within a SharePoint Site using Microsoft Graph API.
"""

import requests
from services.retrieve.graph_headers import _graph_headers
from common.settings import get_settings


_settings = get_settings()


def get_drive_id(site_id: str, drive_name: str = "Documents") -> str:
    """
    Resolve a drive (document library) ID within a SharePoint site by name.

    Args:
        site_id (str): The site unique ID (returned from get_site_id).
        drive_name (str): The display name of the document library (default: "Documents").

    Returns:
        str: Drive ID string.

    Raises:
        ValueError: If site_id argument is missing.
        RuntimeError: If Graph API fails or drive not found.

    Endpoint:
        GET /sites/{site-id}/drives
    """
    if not site_id:
        raise ValueError("site_id must be provided")

    base = _settings.GRAPH_BASE.rstrip("/")
    url = f"{base}/sites/{site_id}/drives"

    response = requests.get(url, headers=_graph_headers(), timeout=30)
    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to list drives (status {response.status_code}): {response.text}"
        )

    payload = response.json()
    drives = payload.get("value", [])

    # First, try exact match on name/displayName
    for drive in drives:
        if drive.get("name") == drive_name or drive.get("displayName") == drive_name:
            drive_id = drive.get("id")
            if drive_id:
                return drive_id

    # If not found, attempt case-insensitive match
    lowered = drive_name.lower()
    for drive in drives:
        name = (drive.get("name") or drive.get("displayName") or "").lower()
        if name == lowered:
            drive_id = drive.get("id")
            if drive_id:
                return drive_id

    raise RuntimeError(f"Drive named '{drive_name}' not found in site '{site_id}'")