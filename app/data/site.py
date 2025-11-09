from pydantic import BaseModel, AnyUrl
from datetime import datetime
from typing import Optional


class SiteResponse(BaseModel):
    id: str
    title: str
    url: AnyUrl
    owner: Optional[str]
    created_at: Optional[datetime]


class SiteListResponse(BaseModel):
    sites: list[SiteResponse]