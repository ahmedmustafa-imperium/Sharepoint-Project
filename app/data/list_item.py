"""
Pydantic models for SharePoint List Items.

Defines request and response models for list item operations.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
class ListItemResponse(BaseModel):
    """
    Response model for a SharePoint list item.
    """
    id: str
    fields: Dict[str, Any] = Field(default_factory=dict)
    created_by: Optional[Dict[str, Any]] = Field(None, alias="createdBy")
    created_at: Optional[datetime] = Field(None, alias="createdDateTime")
    modified_by: Optional[Dict[str, Any]] = Field(None, alias="lastModifiedBy")
    modified_at: Optional[datetime] = Field(None, alias="lastModifiedDateTime")
    web_url: Optional[str] = None
    content_type: Optional[Dict[str, Any]] = Field(None, alias="contentType")
    
    class Config:
        populate_by_name = True
        from_attributes = True


class ListItemListResponse(BaseModel):
    """
    Response model for a list of SharePoint list items.
    """
    items: List[ListItemResponse]
    total_count: Optional[int] = None
    next_link: Optional[str] = Field(None, alias="@odata.nextLink")
    
    class Config:
        populate_by_name = True


class ListItemCreateRequest(BaseModel):
    """
    Request model for creating a SharePoint list item.
    """
    fields: Dict[str, Any] = Field(..., description="Fields for the list item")
    
    class Config:
        json_schema_extra = {
            "example": {
                "fields": {
                    "Title": "New Item"
                }
            }
        }


class ListItemUpdateRequest(BaseModel):
    """
    Request model for updating a SharePoint list item.
    """
    fields: Dict[str, Any] = Field(..., description="Fields to update for the list item")
    
    class Config:
        json_schema_extra = {
            "example": {
                "fields": {
                    "Title": "Updated Title"
                }
            }
        }


class AttachmentResponse(BaseModel):
    """
    Response model for a list item attachment.
    """
    id: str
    name: str
    content_type: Optional[str] = Field(None, alias="contentType")
    size: Optional[int] = None
    content_id: Optional[str] = Field(None, alias="contentId")
    content_location: Optional[str] = Field(None, alias="contentLocation")
    
    class Config:
        populate_by_name = True
        from_attributes = True


class AttachmentListResponse(BaseModel):
    """
    Response model for a list of attachments.
    """
    attachments: List[AttachmentResponse]
    total_count: Optional[int] = None


class ListItemVersionResponse(BaseModel):
    """
    Response model for a list item version.
    """
    id: str
    fields: Optional[Dict[str, Any]] = None
    created_by: Optional[Dict[str, Any]] = Field(None, alias="createdBy")
    created_at: Optional[datetime] = Field(None, alias="createdDateTime")
    
    class Config:
        populate_by_name = True
        from_attributes = True


class ListItemVersionListResponse(BaseModel):
    """
    Response model for a list of list item versions.
    """
    versions: List[ListItemVersionResponse]
    total_count: Optional[int] = None

