from app.services.drive_service import DriveService
from app.data.drive import FileUploadRequest



class SharePointDriveManager:
    """
    Facade to orchestrate all drive-related operations.
    """

    def __init__(self, drive_service: DriveService):
        self.drive_service = drive_service

    async def list_drives(self, site_id: str):
        return await self.drive_service.list_drives(site_id)

    async def list_items(self, drive_id: str, folder_id: str = None):
        return await self.drive_service.list_items(drive_id, folder_id)

    async def upload_file(self, drive_id: str, file_request: FileUploadRequest):
        return await self.drive_service.upload_file(drive_id, file_request)

    async def download_file(self, drive_id: str, file_id: str):
        return await self.drive_service.download_file(drive_id, file_id)
