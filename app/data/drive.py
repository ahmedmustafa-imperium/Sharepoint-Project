from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


# --- Drive / Library metadata ---
class DriveResponse(BaseModel):
    id: str
    name: str
    createdDateTime: datetime
    driveType: str  # e.g., "documentLibrary", "siteDrive"


# --- File / Folder metadata ---
class DriveItemResponse(BaseModel):
    id: str
    name: str
    type: str  # "file" or "folder"
    size: int
    createdDateTime: Optional[str] = None
    url: str


class DriveItemListResponse(BaseModel):
    items: List[DriveItemResponse]
    total_count: int


# --- File upload / download payloads ---
class FileUploadRequest(BaseModel):
    file_name: str
    content: bytes
    folder_id: Optional[str] = None


class FileDownloadResponse(BaseModel):
    pass
#     file_name: str
#     content: Bytes


