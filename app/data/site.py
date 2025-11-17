"""
Pydantic models for SharePoint Sites.

Defines response models for Site operations.
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, HttpUrl
class SiteResponse(BaseModel):
    """
    Response model for a Site
    """
    id: str
    title: str
    url: HttpUrl
    owner: Optional[str] = None
    created_at: Optional[datetime] = None
class SiteListResponse(BaseModel):
    """
    Response model for a SharePoint list.
    """
    sites: List[SiteResponse]
    total: Optional[int] = None
