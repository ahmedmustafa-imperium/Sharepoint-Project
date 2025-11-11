"""
Mapper utility for converting Microsoft Graph API responses to domain models.

Converts raw API JSON responses to Pydantic models.
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from app.data.list import (
    ListResponse,
    ListListResponse,
    ListColumnResponse,
    ListContentTypeResponse
)

logger = logging.getLogger(__name__)


def parse_datetime(dt_string: Optional[str]) -> Optional[datetime]:
    """
    Parse ISO 8601 datetime string to datetime object.
    
    Args:
        dt_string: ISO 8601 datetime string
        
    Returns:
        datetime object or None
    """
    if not dt_string:
        return None

    try:
        # Normalize and parse ISO 8601 datetime string (Graph API returns 'Z' for UTC)
        dt_string = dt_string.replace('Z', '+00:00')
        return datetime.fromisoformat(dt_string)
    except ValueError as e:
        # Use lazy logging instead of f-string for better performance and Pylint compliance
        logger.warning("Failed to parse datetime '%s': %s", dt_string, e)
        return None


def map_list_response(api_response: Dict[str, Any]) -> ListResponse:
    """Map Graph API list response to ListResponse model."""
    return ListResponse(
        id=api_response.get("id", ""),
        display_name=api_response.get("displayName", ""),
        name=api_response.get("name"),
        description=api_response.get("description"),
        web_url=api_response.get("webUrl"),
        created_at=parse_datetime(api_response.get("createdDateTime")),
        modified_at=parse_datetime(api_response.get("lastModifiedDateTime")),
        created_by=api_response.get("createdBy"),
        list_template=api_response.get("list", {}).get("template") if api_response.get("list") else None
    )


def map_list_list_response(api_response: Dict[str, Any]) -> ListListResponse:
    """Map Graph API list of lists response to ListListResponse model."""
    lists = api_response.get("value", [])
    mapped_lists = [map_list_response(item) for item in lists]

    return ListListResponse(
        lists=mapped_lists,
        total_count=len(mapped_lists)
    )


def map_list_column_response(api_response: Dict[str, Any]) -> ListColumnResponse:
    """Map Graph API column response to ListColumnResponse model."""
    return ListColumnResponse(
        id=api_response.get("id", ""),
        name=api_response.get("name", ""),
        display_name=api_response.get("displayName"),
        type=api_response.get("text", {}).get("type") if api_response.get("text") else api_response.get("type"),
        required=api_response.get("required", False),
        read_only=api_response.get("readOnly", False)
    )


def map_list_content_type_response(api_response: Dict[str, Any]) -> ListContentTypeResponse:
    """Map Graph API content type response to ListContentTypeResponse model."""
    return ListContentTypeResponse(
        id=api_response.get("id", ""),
        name=api_response.get("name", ""),
        description=api_response.get("description")
    )
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
