import httpx
from typing import Optional
from app.data.drive import DriveResponse, DriveItemResponse, DriveItemListResponse, FileDownloadResponse
from app.managers.sharepoint_auth_manager import SharePointAuthManager
from typing import Dict
import requests,os


class DriveRepository:
    """
    Handles SharePoint API calls for drives, folders, files, version history, and permissions.
    """

    def __init__(self):
        self.base_url = "https://graph.microsoft.com/v1.0/sites/{site_id}"
        
        
        
    async def _get_access_token(self) -> str:
        """
        Acquire or reuse a cached access token for Microsoft Graph.
        This uses token_cache interface; replace if you have another implementation.
        """
        token=SharePointAuthManager()
        access_token=await token.get_access_token()

        return access_token

    async def _get_headers(self) -> Dict[str, str]:
        """
        Build authorization 
        """
        token = await self._get_access_token()
        return {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    # --- Drives / Libraries ---
    async def list_drives(self, site_id: str) -> list[DriveResponse]:
        url = f"{self.base_url.format(site_id=site_id)}/drives"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            drives = resp.json().get("value", [])
            return [DriveResponse(**d) for d in drives]

    # --- Folder / File operations ---
    async def list_items(self, drive_id: str, folder_id: Optional[str] = None) -> DriveItemListResponse:
        folder_path = f"/items/{folder_id}" if folder_id else "/root"
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}{folder_path}/children"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            items = [
            DriveItemResponse(
                id=i.get("id"),
                name=i.get("name"),
                type="folder" if i.get("folder") else "file",
                size=i.get("size", 0),
                created_at=i.get("createdDateTime"),
                url=i.get("webUrl", "")
            )
            for i in resp.json().get("value", [])
            ]

            return DriveItemListResponse(items=items, total_count=len(items))



    async def download_file(self, drive_id: str, file_id: str, destination_path: str | None = None) :
        headers = await self._get_headers()

        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{file_id}"
        headers["Accept"] = "*/*"

        with requests.get(url, headers=headers, timeout=60, stream=True) as resp:
            if resp.status_code != 200:
                raise RuntimeError(f"Failed to download file (status {resp.status_code}): {resp.text}")

            if destination_path is None:
                destination_path = "downloaded_file"

            with open(destination_path, "wb") as out:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        out.write(chunk)

        return destination_path





    async def upload_file(self, drive_id: str, file_request) -> DriveItemResponse:
        folder_path = file_request.folder_id or "root"
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{folder_path}:/{file_request.file_name}:/content"
        headers = await self._get_headers()
        async with httpx.AsyncClient() as client:
            resp = await client.put(url, headers=headers, content=file_request.content)
            resp.raise_for_status()
            data = resp.json()
            return DriveItemResponse(
                id=data["id"],
                name=data["name"],
                type="file",
                size=data.get("size", 0),
                created_at=data.get("createdDateTime"),
                url=data.get("webUrl", "")
            )
