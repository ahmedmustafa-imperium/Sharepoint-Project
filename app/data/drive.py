"""
SharePoint Drive Data Models

This module defines Pydantic models for representing SharePoint drives, folders, files,
and the payloads required for file upload and download operations.

Models include:
- DriveResponse: Metadata for a SharePoint drive or library
- DriveItemResponse: Metadata for files or folders
- DriveItemListResponse: List of drive items with total count
- FileUploadRequest: Payload for uploading a file
- FileDownloadResponse: Metadata and content for downloaded files
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


# --- Drive / Library metadata ---
class DriveResponse(BaseModel):
    """
    Represents metadata for a SharePoint drive or document library.

    Attributes:
        id (str): Unique identifier of the drive.
        name (str): Name of the drive.
        createdDateTime (datetime): Creation timestamp of the drive.
        driveType (str): Type of the drive (e.g., "documentLibrary", "siteDrive").
    """
    id: str
    name: str
    createdDateTime: datetime
    driveType: str  # e.g., "documentLibrary", "siteDrive"


# --- File / Folder metadata ---
class DriveItemResponse(BaseModel):
    """
    Represents metadata for a file or folder in a SharePoint drive.

    Attributes:
        id (str): Unique identifier of the file/folder.
        name (str): Name of the file/folder.
        type (str): Either "file" or "folder".
        size (int): Size of the file in bytes; 0 for folders.
        createdDateTime (Optional[str]): Creation timestamp of the item.
        url (str): Web URL to access the item.
    """
    id: str
    name: str
    type: str  # "file" or "folder"
    size: int
    createdDateTime: Optional[str] = None
    url: str


class DriveItemListResponse(BaseModel):
    """
    Represents a list of files and folders within a SharePoint drive or folder.

    Attributes:
        items (List[DriveItemResponse]): List of drive items.
        total_count (int): Total number of items in the list.
    """
    items: List[DriveItemResponse]
    total_count: int


# --- File upload / download payloads ---
class FileUploadRequest(BaseModel):
    """
    Payload model for uploading a file to a SharePoint drive or folder.

    Attributes:
        file_name (str): Name of the file to upload.
        content (bytes): Binary content of the file.
        folder_id (Optional[str]): Target folder ID; defaults to root if None.
    """
    file_name: str
    content: bytes
    folder_id: Optional[str] = None


class FileDownloadResponse(BaseModel):
    """
    Represents the metadata and content of a downloaded SharePoint file.

    Attributes:
        id (str): Unique identifier of the file.
        file_name (str): Name of the file.
        size (Optional[int]): Size of the file in bytes.
        created_at (Optional[str]): Creation timestamp.
        last_modified_at (Optional[str]): Last modified timestamp.
        web_url (Optional[str]): Web URL to access the file.
        download_url (Optional[str]): Direct download URL from SharePoint.
        content (Optional[bytes]): Binary content of the file (if downloaded).
        saved_path (Optional[str]): Local path where the file was saved (if applicable).
    """
    id: str
    file_name: str
    size: Optional[int] = None
    created_at: Optional[str] = None
    last_modified_at: Optional[str] = None
    web_url: Optional[str] = None
    download_url: Optional[str] = None
    content: Optional[bytes] = None
    saved_path: Optional[str] = None
