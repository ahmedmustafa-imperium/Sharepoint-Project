"""Service layer encapsulating SharePoint drive business logic."""

import logging
from typing import Optional

from app.repositories.drive_repository import DriveRepository
from app.data.drive import (
    DriveResponse,
    DriveItemListResponse,
    FileUploadRequest,
    DriveItemResponse,
    FileDownloadResponse,
)

logger = logging.getLogger(__name__)


class DriveService:
    """
    Business rules for drive/folder/file operations
    """

    def __init__(self, drive_repository: DriveRepository):
        self.drive_repository = drive_repository

    async def list_drives(self, site_id: str) -> list[DriveResponse]:
        logger.info("Service: listing drives for site %s", site_id)
        return await self.drive_repository.list_drives(site_id)

    async def list_items(self, drive_id: str, folder_id: Optional[str] = None) -> DriveItemListResponse:
        logger.info("Service: listing items for drive %s folder %s", drive_id, folder_id or "root")
        return await self.drive_repository.list_items(drive_id, folder_id)

    async def upload_file(self, drive_id: str, file_request: FileUploadRequest) -> DriveItemResponse:
        logger.info("Service: uploading file '%s' to drive %s", file_request.file_name, drive_id)
        return await self.drive_repository.upload_file(drive_id, file_request)

    async def download_file(
        self,
        drive_id: str,
        file_id: str,
        destination_path: Optional[str] = None,
    ) -> FileDownloadResponse:
        logger.info("Service: downloading file %s from drive %s", file_id, drive_id)
        return await self.drive_repository.download_file(drive_id, file_id, destination_path)

    async def download_files(
        self,
        drive_id: str,
        parent_id: str,
        destination_path: Optional[str] = None,
    ) -> None:
        logger.info(
            "Service: downloading files recursively from drive %s parent %s", drive_id, parent_id
        )
        await self.drive_repository.download_files(drive_id, parent_id, destination_path)
