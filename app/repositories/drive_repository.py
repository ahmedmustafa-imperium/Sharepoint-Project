"""Repository for interacting with SharePoint drive resources via Graph API."""

import asyncio
import os
from typing import List, Optional

import aiofiles
import httpx
from fastapi import status

from app.data.drive import (
    DriveItemListResponse,
    DriveItemResponse,
    DriveResponse,
    FileDownloadResponse,
    FileUploadRequest,
)
from app.core.exceptions.sharepoint_exceptions import map_graph_error
from app.utils.graph_client import GraphAPIError, GraphClient
from app.utils.mapper import (
    map_drive_response,
    map_drive_item_list_response,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


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

        logger.info("Listing drives for site %s", site_id)

        try:
            response = await self.graph_client.get(endpoint)
        except GraphAPIError as exc:
            logger.exception("Graph API error listing drives for site %s", site_id)
            raise map_graph_error(
                "list drives",
                status_code=exc.status_code,
                details=exc.response_body,
            ) from exc

        drives = response.get("value", [])
        logger.debug("Retrieved %d drives for site %s", len(drives), site_id)

        mapped_drives = []
        for drive in drives:
            try:
                mapped_drives.append(map_drive_response(drive))
            except Exception as exc:
                logger.warning("Failed to map drive response for drive %s: %s", drive.get("id"), exc)

        return mapped_drives

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

        logger.info("Listing items for drive %s in folder %s", drive_id, folder_id or "root")

        try:
            response = await self.graph_client.get(endpoint)
        except GraphAPIError as exc:
            logger.exception("Graph API error listing items for drive %s", drive_id)
            raise map_graph_error(
                "list drive items",
                status_code=exc.status_code,
                details=exc.response_body,
            ) from exc

        try:
            return map_drive_item_list_response(response)
        except Exception as exc:
            logger.exception("Failed to map drive items for drive %s", drive_id)
            raise map_graph_error(
                "map drive items",
                status_code=status.HTTP_502_BAD_GATEWAY,
                details=str(exc),
            ) from exc

    async def download_file(
        self,
        drive_id: str,
        file_id: str,
        destination_path: Optional[str] = None,
    ) -> FileDownloadResponse:
        """
        Download a file from a drive, streaming bytes directly to disk.

        If `destination_path` is a directory (or ends with a path separator), the file
        is saved inside that directory using its Graph-provided name. When no
        destination is provided, the file is written to the current working directory.
        """
        metadata_endpoint = f"drives/{drive_id}/items/{file_id}"

        logger.info("Downloading file %s from drive %s", file_id, drive_id)

        try:
            metadata = await self.graph_client.get(metadata_endpoint)
        except GraphAPIError as exc:
            logger.exception(
                "Graph API error retrieving metadata for file %s in drive %s",
                file_id,
                drive_id,
            )
            raise map_graph_error(
                "retrieve file metadata",
                status_code=exc.status_code,
                details=exc.response_body,
            ) from exc

        download_url = metadata.get("@microsoft.graph.downloadUrl")
        if not download_url:
            logger.error("No download URL returned for file %s", file_id)
            raise map_graph_error(
                "download file",
                status_code=status.HTTP_502_BAD_GATEWAY,  # type: ignore[name-defined]
                details="No download URL returned for the file.",
            )

        file_name = metadata.get("name", "downloaded_file")

        destination_path = destination_path or os.path.join(os.getcwd(), "")
        is_directory = destination_path.endswith(os.sep) or (
            os.path.exists(destination_path) and os.path.isdir(destination_path)
        )
        target_path = (
            os.path.join(destination_path, file_name) if is_directory else destination_path
        )
        os.makedirs(os.path.dirname(target_path) or ".", exist_ok=True)

        async with httpx.AsyncClient() as client:
            async with client.stream("GET", download_url, timeout=120) as response:
                response.raise_for_status()
                async with aiofiles.open(target_path, "wb") as file_handle:
                    async for chunk in response.aiter_bytes():
                        if chunk:
                            await file_handle.write(chunk)

        return FileDownloadResponse(
            id=metadata.get("id", ""),
            file_name=file_name,
            size=metadata.get("size"),
            created_at=metadata.get("createdDateTime"),
            last_modified_at=metadata.get("lastModifiedDateTime"),
            web_url=metadata.get("webUrl"),
            download_url=download_url,
            content=None,
            saved_path=target_path,
        )
        
    async def download_files(
        self,
        drive_id: str,
        parent_id: str = "root",
        destination_root: Optional[str] = None,
    ) -> None:
        """
        Recursively download all files/folders from a given drive folder.
        """
        destination_root = destination_root or os.getcwd()

        logger.info(
            "Recursively downloading items for drive %s under parent %s into %s",
            drive_id,
            parent_id,
            destination_root,
        )

        response = await self.list_items(drive_id, None if parent_id == "root" else parent_id)
        tasks = []

        for item in response.items:
            local_path = os.path.join(destination_root, item.name)

            if item.type == "folder":
                os.makedirs(local_path, exist_ok=True)
                tasks.append(self.download_files(drive_id, item.id, local_path))
            else:
                tasks.append(self.download_file(drive_id, item.id, local_path))

        if tasks:
            await asyncio.gather(*tasks)
            logger.debug("Completed downloading %d items from drive %s", len(tasks), drive_id)

    async def upload_file(self, drive_id: str, file_request: FileUploadRequest) -> DriveItemResponse:
        folder_path = file_request.folder_id or "root"
        endpoint = f"drives/{drive_id}/items/{folder_path}:/{file_request.file_name}:/content"

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
