"""
download_file.py

Provides function to download a file from the root of the default drive
of a SharePoint site using Microsoft Graph API.
"""

import os
import requests
from services.retrieve.site_id import get_site_id
from services.retrieve.drive_id import get_drive_id
from services.retrieve.graph_headers import _graph_headers
from common.settings import get_settings


_settings = get_settings()


def download_file_from_root(
    file_path: str,
    destination_path: str | None = None,
    drive_name: str = "Documents",
) -> str:
    """
    Download a file from a site's document library (drive) using path relative to drive root.

    Example:
        GRAPH_BASE/sites/{site_id}/drives/{drive_id}/root:/{file_path}:/content

    Args:
        file_path (str): Path to file relative to drive root. e.g. "Folder/File.pdf" or "File.pdf"
        destination_path (str | None): Local file path to save. If None, uses basename(file_path).
        drive_name (str): Drive display name. Defaults to "Documents".
    Returns:
        str: Local destination file path.

    Raises:
        ValueError: Missing site_id or file_path.
        RuntimeError: Download failed or Graph API returned non-200.
    """
    site_id = get_site_id()
    if not site_id:
        raise ValueError("site_id must be provided")
    if not file_path or file_path.strip() == "":
        raise ValueError("file_path must be provided")

    base = _settings.GRAPH_BASE.rstrip("/")
    safe_path = file_path.strip("/")
    # Resolve drive_id if not explicitly provided
    resolved_drive_id =get_drive_id(site_id=site_id, drive_name=drive_name)
    url = f"{base}/sites/{site_id}/drives/{resolved_drive_id}/root:/{safe_path}:/content"

    headers = _graph_headers()
    # For binary download, remove JSON content-type
    headers.pop("Content-Type", None)
    headers["Accept"] = "*/*"

    with requests.get(url, headers=headers, timeout=60, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError(f"Failed to download file (status {resp.status_code}): {resp.text}")

        if destination_path is None:
            destination_path = os.path.basename(safe_path) or "downloaded_file"

        with open(destination_path, "wb") as out:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    out.write(chunk)

    return destination_path