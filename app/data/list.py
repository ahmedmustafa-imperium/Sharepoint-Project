"""
Pydantic models for SharePoint Lists.

Defines request and response models for list operations.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ListResponse(BaseModel):
    """
    Response model for a SharePoint list.
    """
    id: str
    display_name: str
    name: Optional[str] = None
    description: Optional[str] = None
    web_url: Optional[str] = None
    created_at: Optional[datetime] = Field(None, alias="createdDateTime")
    modified_at: Optional[datetime] = Field(None, alias="lastModifiedDateTime")
    created_by: Optional[Dict[str, Any]] = Field(None, alias="createdBy")
    list_template: Optional[str] = Field(None, alias="list", json_schema_extra={"template": "template"})
    
    class Config:
        populate_by_name = True
        from_attributes = True


class ListListResponse(BaseModel):
    """
    Response model for a list of SharePoint lists.
    """
    lists: List[ListResponse]
    total_count: Optional[int] = None


class ListCreateRequest(BaseModel):
    """
    Request model for creating a SharePoint list.
    """
    display_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    template: Optional[str] = Field(None, description="List template (e.g., 'genericList', 'documentLibrary')")
    columns: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "display_name": "My List",
                "description": "A sample list",
                "template": "genericList",
                "columns": []
            }
        }


class ListUpdateRequest(BaseModel):
    """
    Request model for updating a SharePoint list.
    """
    display_name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "display_name": "Updated List Name",
                "description": "Updated description"
            }
        }


class ListColumnResponse(BaseModel):
    """
    Response model for a list column.
    """
    id: str
    name: str
    display_name: Optional[str] = None
    type: Optional[str] = None
    required: Optional[bool] = None
    read_only: Optional[bool] = None
    
    class Config:
        from_attributes = True


class ListContentTypeResponse(BaseModel):
    """
    Response model for a list content type.
    """
    id: str
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True