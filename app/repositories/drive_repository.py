import httpx
from typing import Optional
from app.data.drive import DriveResponse, DriveItemResponse, DriveItemListResponse, FileDownloadResponse
from app.managers.sharepoint_auth_manager import SharePointAuthManager
from typing import Dict
import aiofiles
import httpx
import os

import asyncio
import aiofiles
import httpx
from typing import List
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



    async def download_file(self, drive_id: str, file_id: str, destination_path: str = None) -> FileDownloadResponse:
        headers = await self._get_headers()

        # 1️ Get file metadata (to get the download URL)
        metadata_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{file_id}"
        async with httpx.AsyncClient() as client:
            meta_resp = await client.get(metadata_url, headers=headers)
            meta_resp.raise_for_status()
            data = meta_resp.json()

        download_url = data.get("@microsoft.graph.downloadUrl")
        if not download_url:
            raise RuntimeError("No download URL found for the file.")

        file_name = data.get("name", "downloaded_file")

        if destination_path:
            # If destination is a directory, append the filename
            if os.path.isdir(destination_path):
                destination_path = os.path.join(destination_path, file_name)
        else:
            destination_path = os.path.join(os.getcwd(), file_name)

        async with httpx.AsyncClient() as client:
            async with client.stream("GET", download_url, timeout=120) as resp:
                resp.raise_for_status()
                async with aiofiles.open(destination_path, "wb") as f:
                    async for chunk in resp.aiter_bytes():
                        await f.write(chunk)

        # 3️ Return file metadata
        return FileDownloadResponse(
            id=data.get("id", ""),
            file_name=file_name,
            size=data.get("size"),
            created_at=data.get("createdDateTime"),
            last_modified_at=data.get("lastModifiedDateTime"),
            web_url=data.get("webUrl"),
            download_url=download_url
        )
    async def download_files(self, drive_id: str, parent_id: str = "root", destination_root: str = None):
        """
        Recursively download all files/folders from a given drive folder.
        """
        headers = await self._get_headers()
        list_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{parent_id}/children"

        async with httpx.AsyncClient() as client:
            resp = await client.get(list_url, headers=headers)
            resp.raise_for_status()
            items = resp.json().get("value", [])

        if not destination_root:
            destination_root = os.getcwd()

        tasks = []

        for item in items:
            name = item.get("name")
            item_id = item.get("id")
            local_path = os.path.join(destination_root, name)

            if "folder" in item:
                # Create local folder and recurse
                os.makedirs(local_path, exist_ok=True)
                tasks.append(self.download_files(drive_id, item_id, local_path))
            else:
                # File — download to correct path
                tasks.append(self.download_file(drive_id, item_id, local_path))

        # Run all tasks concurrently
        if tasks:
            await asyncio.gather(*tasks)

    


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
