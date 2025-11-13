"""
API routes for SharePoint sites.
 
Handles HTTP requests for site operations.
"""

from fastapi import APIRouter, Depends
from app.core.deps import get_sharepoint_site_manager
from app.managers.sharepoint_site_manager import SharePointSiteManager

router = APIRouter(prefix="/sites", tags=["Sites"])


@router.get("/list_sites")
async def get_list_sites(manager: SharePointSiteManager = Depends(get_sharepoint_site_manager)):
    """
    Retrieve a list of all available SharePoint sites.

    Uses the injected SharePointSiteManager to fetch and return
    metadata for all accessible SharePoint sites.

    Args:
        manager: The SharePointSiteManager instance provided by dependency injection.

    Returns:
        list: A list of SharePoint sites with their associated details.
    """
    list_sites = await manager.list_sites()
    return list_sites

@router.get("/site_by_id/{site_id}")
async def site_by_id(site_id: str, manager: SharePointSiteManager = Depends(get_sharepoint_site_manager)):
    """
    Retrieve details of a specific SharePoint site by its unique ID.

    Args:
        site_id (str): The unique identifier of the SharePoint site.
        manager: The SharePointSiteManager instance provided by dependency injection.

    Returns:
        dict: A dictionary containing metadata and details of the requested site.
    """
    site = await manager.get_site(site_id)
    return site

@router.get("/search_sites/{query}")
async def site_by_query(query: str, manager: SharePointSiteManager = Depends(get_sharepoint_site_manager)):
    """
    Search for SharePoint sites that match a given query string.

    Args:
        query (str): The search string used to match site names.
        manager: The SharePointSiteManager instance provided by dependency injection.

    Returns:
        list: A list of sites that match the search criteria.
    """
    site = await manager.search_sites(query)
    return site
