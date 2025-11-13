from app.services.drive_service import DriveService
from app.repositories.drive_repository import DriveRepository
from app.data.drive import FileUploadRequest



class SharePointDriveManager:
    """
    Facade to orchestrate all drive-related operations.
    """

    def __init__(self):
        self.repo = DriveRepository()
        self.service = DriveService(self.repo)

    async def list_drives(self, site_id: str):
        return await self.service.list_drives(site_id)

    async def list_items(self, drive_id: str, folder_id: str = None):
        return await self.service.list_items(drive_id, folder_id)

    async def upload_file(self, drive_id: str, file_request: FileUploadRequest):
        return await self.service.upload_file(drive_id, file_request)

    async def download_file(self, drive_id: str, file_id: str,destination_path: str):
        return await self.service.download_file(drive_id, file_id,destination_path)
    async def download_files(self, drive_id: str, parent_id: str,destination_path: str):
        return await self.service.download_files(drive_id, parent_id,destination_path)
