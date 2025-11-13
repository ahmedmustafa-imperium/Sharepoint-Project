import logging
import os
from typing import Optional, List

import aiofiles
import httpx

from app.data.drive import (
    DriveResponse,
    DriveItemResponse,
    DriveItemListResponse,
    FileDownloadResponse,
    FileUploadRequest,
)
from app.utils.graph_client import GraphClient, GraphAPIError

logger = logging.getLogger(__name__)


class DriveRepository:
    """
    Handles SharePoint API calls for drives, folders, files, version history, and permissions.
    """

    def __init__(self, graph_client: GraphClient):
        self.graph_client = graph_client

    async def list_drives(self, site_id: str) -> List[DriveResponse]:
        """
        Retrieve all drives for a given SharePoint site.
        """
        endpoint = f"sites/{site_id}/drives"

        try:
            response = await self.graph_client.get(endpoint)
            drives = response.get("value", [])
            return [DriveResponse(**drive) for drive in drives]
        except GraphAPIError as exc:
            logger.error("Failed to list drives for site %s: %s", site_id, exc)
            raise

    async def list_items(
        self,
        drive_id: str,
        folder_id: Optional[str] = None,
    ) -> DriveItemListResponse:
        """
        Retrieve drive items (files/folders) for the specified drive/folder.
        """
        folder_path = f"/items/{folder_id}" if folder_id else "/root"
        endpoint = f"drives/{drive_id}{folder_path}/children"

        try:
            response = await self.graph_client.get(endpoint)
        except GraphAPIError as exc:
            logger.error("Failed to list items for drive %s: %s", drive_id, exc)
            raise

        items_data = response.get("value", [])
        items = [
            DriveItemResponse(
                id=item.get("id", ""),
                name=item.get("name", ""),
                type="folder" if item.get("folder") else "file",
                size=item.get("size", 0),
                createdDateTime=item.get("createdDateTime"),
                url=item.get("webUrl", ""),
            )
            for item in items_data
        ]

        return DriveItemListResponse(items=items, total_count=len(items))

    async def download_file(
        self,
        drive_id: str,
        file_id: str,
        destination_path: Optional[str] = None,
    ) -> FileDownloadResponse:
        """
        Download a file from a drive. Optionally persists the content to disk.
        """
        metadata_endpoint = f"drives/{drive_id}/items/{file_id}"

        try:
            metadata = await self.graph_client.get(metadata_endpoint)
        except GraphAPIError as exc:
            logger.error(
                "Failed to retrieve metadata for file %s in drive %s: %s",
                file_id,
                drive_id,
                exc,
            )
            raise

        download_url = metadata.get("@microsoft.graph.downloadUrl")
        if not download_url:
            logger.error("No download URL returned for file %s", file_id)
            raise RuntimeError("No download URL found for the file.")

        file_name = metadata.get("name", "downloaded_file")
        resolved_path = destination_path or os.path.join(os.getcwd(), file_name)

        async with httpx.AsyncClient() as client:
            async with client.stream("GET", download_url, timeout=120) as response:
                response.raise_for_status()
                async with aiofiles.open(resolved_path, "wb") as file_handle:
                    async for chunk in response.aiter_bytes():
                        await file_handle.write(chunk)

        return FileDownloadResponse(
            id=metadata.get("id", ""),
            file_name=file_name,
            size=metadata.get("size"),
            created_at=metadata.get("createdDateTime"),
            last_modified_at=metadata.get("lastModifiedDateTime"),
            web_url=metadata.get("webUrl"),
            download_url=download_url,
            saved_path=resolved_path,
        )

    async def upload_file(
        self,
        drive_id: str,
        file_request: FileUploadRequest,
    ) -> DriveItemResponse:
        """
        Upload a file to the specified drive/folder.
        """
        folder_path = file_request.folder_id or "root"
        endpoint = (
            f"drives/{drive_id}/items/{folder_path}:/{file_request.file_name}:/content"
        )

        try:
            response = await self.graph_client.put(
                endpoint,
                headers={"Content-Type": "application/octet-stream"},
                content=file_request.content,
            )
        except GraphAPIError as exc:
            logger.error(
                "Failed to upload file %s to drive %s: %s",
                file_request.file_name,
                drive_id,
                exc,
            )
            raise

        return DriveItemResponse(
            id=response.get("id", ""),
            name=response.get("name", ""),
            type="file",
            size=response.get("size", 0),
            createdDateTime=response.get("createdDateTime"),
            url=response.get("webUrl", ""),
        )
