from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse
from io import BytesIO
from app.data.drive import FileUploadRequest
from app.core.deps import get_sharepoint_drive_manager # returns token for MS Graph

router = APIRouter()

router = APIRouter(prefix="/drives", tags=["drives"])
@router.get("/list_drives")
async def list_drives(site_id: str, manager: str = Depends(get_sharepoint_drive_manager)):
    
    return await manager.list_drives(site_id)


@router.get("/drives/{drive_id}/items")
async def list_items(drive_id: str, folder_id: str = None, manager: str = Depends(get_sharepoint_drive_manager)):
  
    return await manager.list_items(drive_id, folder_id)


@router.post("/drives/{drive_id}/upload")
async def upload_file(drive_id: str, file: UploadFile = File(...), folder_id: str = None, manager: str = Depends(get_sharepoint_drive_manager)):
    content = await file.read()
    file_req = FileUploadRequest(file_name=file.filename, content=content, folder_id=folder_id)
 
    return await manager.upload_file(drive_id, file_req)


@router.get("/drives/{drive_id}/download/{file_id}")
def download_file(drive_id: str, file_id: str, manager: str = Depends(get_sharepoint_drive_manager)):
    file_response = manager.download_file(drive_id, file_id)

    # Return as a streaming response to trigger download
    return file_response
    

