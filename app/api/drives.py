from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from io import BytesIO
from app.data.drive import FileUploadRequest
from app.core.deps import get_sharepoint_drive_manager  # returns token for MS Graph
from app.managers.sharepoint_drive_manager import SharePointDriveManager

router = APIRouter()

router = APIRouter(prefix="/drives", tags=["drives"])
@router.get("/list_drives")
async def list_drives(site_id: str, manager: SharePointDriveManager = Depends(get_sharepoint_drive_manager)):
    
    return await manager.list_drives(site_id)


@router.get("/drives/{drive_id}/items")
async def list_items(drive_id: str, folder_id: str = None, manager: SharePointDriveManager = Depends(get_sharepoint_drive_manager)):
  
    return await manager.list_items(drive_id, folder_id)


@router.post("/drives/{drive_id}/upload")
async def upload_file(drive_id: str, file: UploadFile = File(...), folder_id: str = None, manager: SharePointDriveManager = Depends(get_sharepoint_drive_manager)):
    content = await file.read()
    file_req = FileUploadRequest(file_name=file.filename, content=content, folder_id=folder_id)
 
    return await manager.upload_file(drive_id, file_req)


@router.get("/drives/{drive_id}/download/{file_id}")
async def download_file(drive_id: str, file_id: str, manager: SharePointDriveManager = Depends(get_sharepoint_drive_manager)):
    file_response = await manager.download_file(drive_id, file_id)

    if file_response.content:
        headers = {
            "Content-Disposition": f'attachment; filename="{file_response.file_name or "downloaded_file"}"'
        }
        return StreamingResponse(BytesIO(file_response.content), media_type="application/octet-stream", headers=headers)

    payload = file_response.dict(exclude={"content"}, exclude_none=True)
    return JSONResponse(content=payload)
    

