from __future__ import annotations

import requests

from auth.msal_token import get_token
from common.settings import get_settings


_settings = get_settings()


def _graph_headers() -> dict[str, str]:
    access_token = get_token()
    print(access_token)
    with open("access_token.txt","w",encoding="utf-8") as f:
        f.write(access_token)
    return {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def get_site_id() -> str:
    """
    Resolve the SharePoint Site ID using hostname and site path from settings.

    Uses: GRAPH_BASE, SHAREPOINT_HOSTNAME, SITE_PATH
    Endpoints:
    - If SITE_PATH is empty: GET /sites/{hostname}
    - If SITE_PATH starts with 'sites/' or 'teams/': GET /sites/{hostname}:/{SITE_PATH}
    - Otherwise: GET /sites/{hostname}:/sites/{SITE_PATH}
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


def get_drive_id(site_id: str, drive_name: str = "Documents") -> str:
    """
    Resolve a drive (document library) ID within a SharePoint site by name.

    - site_id: The site unique ID (from get_site_id)
    - drive_name: The display name of the document library (default: "Documents")

    Endpoint: GET /sites/{site-id}/drives
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


def download_file_from_root(site_id: str, file_path: str, destination_path: str | None = None) -> str:
    """
    Download a file from the site's default drive (root) using the path relative to drive root.

    Example URL used:
    {GRAPH_BASE}/sites/{site_id}/drive/root:/{file_path}:/content

    - site_id: site identifier string (hostname,siteId,webId or GUID form)
    - file_path: path to file relative to the drive root (e.g., "Folder/File.pdf" or just "File.pdf")
    - destination_path: local file path to save to. Defaults to the basename of file_path in current directory.
    Returns: local destination path saved to.
    """
    if not site_id:
        raise ValueError("site_id must be provided")
    if not file_path or file_path.strip() == "":
        raise ValueError("file_path must be provided")

    base = _settings.GRAPH_BASE.rstrip("/")
    safe_path = file_path.strip("/")
    url = f"{base}/sites/{site_id}/drive/root:/{safe_path}:/content"

    headers = _graph_headers()
    # For content download, Content-Type header is not required; keep Authorization only
    headers.pop("Content-Type", None)
    headers["Accept"] = "*/*"

    with requests.get(url, headers=headers, timeout=60, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError(f"Failed to download file (status {resp.status_code}): {resp.text}")
        if destination_path is None:
            # Save to current working directory using the file name
            import os
            destination_path = os.path.basename(safe_path) or "downloaded_file"
        with open(destination_path, "wb") as out:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    out.write(chunk)
    return destination_path
