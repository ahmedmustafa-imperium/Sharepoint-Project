from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, HttpUrl
class SiteResponse(BaseModel):
    id: str
    title: str
    url: HttpUrl
    owner: Optional[str] = None
    created_at: Optional[datetime] = None
 


class SiteListResponse(BaseModel):
    sites: List[SiteResponse]
    total: Optional[int] = None
