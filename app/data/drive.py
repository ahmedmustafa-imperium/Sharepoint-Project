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
    id: str
    file_name: str
    size: Optional[int] = None
    created_at: Optional[str] = None
    last_modified_at: Optional[str] = None
    web_url: Optional[str] = None
    download_url: Optional[str] = None
    content: Optional[bytes] = None
    saved_path: Optional[str] = None


