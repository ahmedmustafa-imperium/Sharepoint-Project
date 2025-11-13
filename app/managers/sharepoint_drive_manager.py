"""Top-level manager for orchestrating SharePoint drive operations."""

import logging
from typing import Optional

from app.services.drive_service import DriveService
from app.data.drive import FileUploadRequest

logger = logging.getLogger(__name__)

class SharePointDriveManager:
    """Facade to orchestrate all drive-related operations."""

    def __init__(self, drive_service: DriveService):
        """Initialize the manager with its drive service dependency."""
        self.drive_service = drive_service

    async def list_drives(self, site_id: str):
        """List all drives for the specified SharePoint site."""
        logger.info("Manager: listing drives for site %s", site_id)
        return await self.drive_service.list_drives(site_id)

    async def list_items(self, drive_id: str, folder_id: Optional[str] = None):
        """List items for a given drive and optional folder."""
        logger.info("Manager: listing items for drive %s folder %s", drive_id, folder_id or "root")
        return await self.drive_service.list_items(drive_id, folder_id)

    async def upload_file(self, drive_id: str, file_request: FileUploadRequest):
        """Upload a file to the given drive."""
        logger.info("Manager: uploading file '%s' to drive %s", file_request.file_name, drive_id)
        return await self.drive_service.upload_file(drive_id, file_request)

    async def download_file(
        self,
        drive_id: str,
        file_id: str,
        destination_path: Optional[str] = None,
    ):
        """Download a specific file from a drive."""
        logger.info("Manager: downloading file %s from drive %s", file_id, drive_id)
        return await self.drive_service.download_file(drive_id, file_id, destination_path)

    async def download_files(
        self,
        drive_id: str,
        parent_id: str,
        destination_path: Optional[str] = None,
    ):
        """Download all files recursively from the specified drive folder."""
        logger.info(
            "Manager: downloading files recursively for drive %s parent %s", drive_id, parent_id
        )
        await self.drive_service.download_files(drive_id, parent_id, destination_path)
