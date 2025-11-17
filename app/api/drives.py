"""
SharePoint Drive API Router

This module provides FastAPI endpoints to interact with SharePoint drives, folders, and files.
It allows clients to:
- List drives in a SharePoint site
- List items (files/folders) within a drive
- Upload files to a drive/folder
- Download a single file or multiple files from a drive

Dependencies:
- SharePointDriveManager: Handles actual communication with SharePoint and file operations.
- FileUploadRequest: Data model for file uploads.
"""

from io import BytesIO
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from app.data.drive import FileUploadRequest
from app.core.deps import get_sharepoint_drive_manager
from app.managers.sharepoint_drive_manager import SharePointDriveManager

router = APIRouter(prefix="/drives", tags=["drives"])

@router.get("/list_drives")
async def list_drives(
    site_id: str,
    manager: SharePointDriveManager = Depends(get_sharepoint_drive_manager)):
    """
    List all drives/libraries in a given SharePoint site.

    Args:
        site_id (str): The SharePoint site ID.
        manager (SharePointDriveManager): Injected dependency to manage SharePoint drives.

    Returns:
        List of drives with metadata.
    """
    return await manager.list_drives(site_id)


@router.get("/drives/{drive_id}/items")
async def list_items(
    drive_id: str,
    folder_id: str | None = None,
    manager: SharePointDriveManager = Depends(get_sharepoint_drive_manager),
):
    """
    List all items (files and folders) in a specific drive or folder.

    Args:
        drive_id (str): ID of the SharePoint drive.
        folder_id (str | None): Optional folder ID to list contents; defaults to root.
        manager (SharePointDriveManager): Injected dependency.

    Returns:
        List of items with metadata and total count.
    """
    return await manager.list_items(drive_id, folder_id)


@router.post("/drives/{drive_id}/upload")
async def upload_file(
    drive_id: str,
    file: UploadFile = File(...),
    folder_id: str | None = None,
    manager: SharePointDriveManager = Depends(get_sharepoint_drive_manager),
):
    """
    Upload a file to a SharePoint drive or folder.

    Args:
        drive_id (str): ID of the SharePoint drive.
        file (UploadFile): File uploaded by the client.
        folder_id (str | None): Optional folder ID to upload into; defaults to root.
        manager (SharePointDriveManager): Injected dependency.

    Returns:
        Metadata of the uploaded file.
    """
    content = await file.read()
    file_req = FileUploadRequest(file_name=file.filename, content=content, folder_id=folder_id)
    return await manager.upload_file(drive_id, file_req)


@router.get("/drives/{drive_id}/download/{file_id}")
async def download_file(
    drive_id: str,
    file_id: str,
    destination_path: str | None = None,
    manager: SharePointDriveManager = Depends(get_sharepoint_drive_manager),
):
    """
    Download a single file from a SharePoint drive.

    Args:
        drive_id (str): ID of the SharePoint drive.
        file_id (str): ID of the file to download.
        destination_path (str | None): Optional local path to save the file.
        manager (SharePointDriveManager): Injected dependency.

    Returns:
        StreamingResponse with file content if available, or JSON metadata.
    """
    file_response = await manager.download_file(drive_id, file_id, destination_path)

    if file_response.content:
        headers = {
            "Content-Disposition": f'attachment; filename="{file_response.file_name or "downloaded_file"}"'
        }
        return StreamingResponse(
            BytesIO(file_response.content), media_type="application/octet-stream", headers=headers)

    payload = file_response.dict(exclude={"content"}, exclude_none=True)
    return JSONResponse(content=payload)


@router.get("/drives/{drive_id}/download")
async def download_files(
    drive_id: str,
    parent_id: str = "root",
    destination_path: str | None = None,
    manager: SharePointDriveManager = Depends(get_sharepoint_drive_manager),
):
    """
    Download all files from a SharePoint drive or folder recursively.

    Args:
        drive_id (str): ID of the SharePoint drive.
        parent_id (str): Folder ID to download from; defaults to root.
        destination_path (str | None): Optional local directory to save files.
        manager (SharePointDriveManager): Injected dependency.

    Returns:
        JSON object indicating download completion status.
    """
    await manager.download_files(drive_id, parent_id, destination_path)
    return {"status": "completed"}
