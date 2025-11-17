"""Service layer encapsulating SharePoint drive business logic."""

from typing import Optional

from app.repositories.drive_repository import DriveRepository
from app.data.drive import (
    DriveResponse,
    DriveItemListResponse,
    FileUploadRequest,
    DriveItemResponse,
    FileDownloadResponse,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


class DriveService:
    """
    Provides business logic and workflow orchestration for SharePoint drive operations,
    delegating API interactions to the DriveRepository layer.
    """

    def __init__(self, drive_repository: DriveRepository):
        """
        Initialize the DriveService with a DriveRepository instance.

        Args:
            drive_repository (DriveRepository): Repository responsible for calling Graph API endpoints.
        """
        self.drive_repository = drive_repository

    async def list_drives(self, site_id: str) -> list[DriveResponse]:
        """
        Retrieve available drives for the given SharePoint site.

        Args:
            site_id (str): The unique ID of the SharePoint site.

        Returns:
            list[DriveResponse]: Collection of drive metadata associated with the site.
        """
        logger.info("Service: listing drives for site %s", site_id)
        return await self.drive_repository.list_drives(site_id)

    async def list_items(self, drive_id: str, folder_id: Optional[str] = None) -> DriveItemListResponse:
        """
        Retrieve all items within a drive or a specific folder.

        Args:
            drive_id (str): The unique ID of the drive.
            folder_id (Optional[str]): The folder ID within the drive (defaults to root folder when None).

        Returns:
            DriveItemListResponse: Contains list of files and folders within the requested location.
        """
        logger.info("Service: listing items for drive %s folder %s", drive_id, folder_id or "root")
        return await self.drive_repository.list_items(drive_id, folder_id)

    async def upload_file(self, drive_id: str, file_request: FileUploadRequest) -> DriveItemResponse:
        """
        Upload a file to a specified drive and folder.

        Args:
            drive_id (str): The drive ID where the file will be saved.
            file_request (FileUploadRequest): Contains file metadata and byte content.

        Returns:
            DriveItemResponse: Response metadata for the uploaded file.
        """
        logger.info("Service: uploading file '%s' to drive %s", file_request.file_name, drive_id)
        return await self.drive_repository.upload_file(drive_id, file_request)

    async def download_file(
        self,
        drive_id: str,
        file_id: str,
        destination_path: Optional[str] = None,
    ) -> FileDownloadResponse:
        """
        Download a file from a SharePoint drive. If destination_path is provided,
        the file is streamed directly to disk without memory buffering.

        Args:
            drive_id (str): The drive ID the file belongs to.
            file_id (str): The unique ID of the file to download.
            destination_path (Optional[str]): Path for saving the downloaded file locally.

        Returns:
            FileDownloadResponse: Contains metadata and saved file path information.
        """
        logger.info("Service: downloading file %s from drive %s", file_id, drive_id)
        return await self.drive_repository.download_file(drive_id, file_id, destination_path)

    async def download_files(
        self,
        drive_id: str,
        parent_id: str,
        destination_path: Optional[str] = None,
    ) -> None:
        """
        Recursively download all files and folders starting from a given parent folder.
        All file contents are streamed directly to disk via aiofiles for efficient,
        memory-safe processing.

        Args:
            drive_id (str): The drive ID containing the files.
            parent_id (str): The starting folder ID ("root" for top-level).
            destination_path (Optional[str]): Local destination directory where files will be saved.

        Returns:
            None
        """
        logger.info(
            "Service: downloading files recursively from drive %s parent %s",
            drive_id,
            parent_id,
        )
        await self.drive_repository.download_files(drive_id, parent_id, destination_path)
