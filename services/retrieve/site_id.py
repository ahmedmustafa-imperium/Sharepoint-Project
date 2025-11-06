"""
site_id.py

Contains helper function to resolve and return a SharePoint Site ID
using the Microsoft Graph API, based on tenant configuration values.
"""

import requests
from services.retrieve.graph_headers import _graph_headers
from common.settings import get_settings


_settings = get_settings()

def get_site_id() -> str:
    """
    Resolve the SharePoint Site ID using hostname and site path from settings.

    Uses: GRAPH_BASE, SHAREPOINT_HOSTNAME, SITE_PATH
    Endpoints:
    - If SITE_PATH is empty: GET /sites/{hostname}
    - If SITE_PATH starts with 'sites/' or 'teams/': GET /sites/{hostname}:/{SITE_PATH}
    - Otherwise: GET /sites/{hostname}:/sites/{SITE_PATH}

    Returns:
        str: The resolved SharePoint Site ID from Graph API.
    """
    base = _settings.GRAPH_BASE.rstrip("/")
    hostname = _settings.SHAREPOINT_HOSTNAME
    site_path_raw = (_settings.SITE_PATH or "").strip()

    if not site_path_raw or site_path_raw.strip("/ ") == "":
        # Root site collection
        url = f"{base}/sites/{hostname}"
    else:
        site_path = site_path_raw.strip("/")
        if site_path.startswith("sites/") or site_path.startswith("teams/"):
            url = f"{base}/sites/{hostname}:/{site_path}"
        else:
            url = f"{base}/sites/{hostname}:/sites/{site_path}"

    response = requests.get(url, headers=_graph_headers(), timeout=30)
    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to get site id (status {response.status_code}): {response.text}"
        )

    payload = response.json()
    site_id = payload.get("id")
    if not site_id:
        raise RuntimeError("Graph response did not include 'id' for site")

    return site_id