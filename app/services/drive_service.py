from typing import Optional
from app.repositories.drive_repository import DriveRepository
from app.data.drive import DriveResponse, DriveItemListResponse, FileUploadRequest, DriveItemResponse, FileDownloadResponse


class DriveService:
    """
    Business rules for drive/folder/file operations
    """

    def __init__(self, repo: DriveRepository):
        self.repo = repo

    async def list_drives(self, site_id: str) -> list[DriveResponse]:
        return await self.repo.list_drives(site_id)

    async def list_items(self, drive_id: str, folder_id: Optional[str] = None) -> DriveItemListResponse:
        return await self.repo.list_items(drive_id, folder_id)

    async def upload_file(self, drive_id: str, file_request: FileUploadRequest) -> DriveItemResponse:
        # Add any business validation if needed
        return await self.repo.upload_file(drive_id, file_request)

    async def download_file(self, drive_id: str, file_id: str)->FileDownloadResponse:
        return await self.repo.download_file(drive_id, file_id)
