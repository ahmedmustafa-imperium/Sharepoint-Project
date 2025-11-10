from typing import Any, Dict
from datetime import datetime
from pydantic import HttpUrl
from app.data.site import SiteResponse



def map_site_json(raw: Dict[str, Any]) -> SiteResponse:
    """
    Map a Graph API site JSON to SiteResponse domain model.
    Adjust keys according to actual Graph response.
    """
    # Graph site object commonly has fields: id, displayName, webUrl, createdDateTime, lastModifiedDateTime, createdBy
    created = raw.get("createdDateTime")
    
    owner = None
    # owner info might be nested; try a couple of fallbacks
    owner = raw.get("name")
    url_str = raw.get("webUrl") or raw.get("url") or ""
    if url_str and not url_str.startswith("https://"):
        url_str = "https://" + url_str.lstrip("/")

    
    return SiteResponse(
        id=str(raw.get("id", "")),
        title=raw.get("displayName"),
        url=url_str,
        owner=owner,
        created_at=datetime.fromisoformat(created) if created else None,
        
    )
