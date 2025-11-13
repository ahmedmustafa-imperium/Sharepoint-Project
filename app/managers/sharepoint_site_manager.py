"""
Manager layer for SharePoint site operations.

This module defines the `SharePointSiteManager` class, which acts as the orchestration
layer between the API routes and lower-level service.

Responsibilities:
- Coordinate site-related operations, such as listing, retrieving, and searching sites.
"""
import logging
from typing import Optional

from app.data.site import SiteListResponse, SiteResponse
from app.services.site_service import SiteService

logger = logging.getLogger(__name__)


class SharePointSiteManager:
    """
    Coordinates site-level operations for SharePoint.

    This manager serves as a facade to the `SiteService`, allowing
    higher-level components (such as API routes) to interact with
    SharePoint sites in a clean manner.
    """
    def __init__(self, site_service: SiteService):
        self.site_service = site_service

    async def list_sites(self, page_size: int = 50) -> SiteListResponse:
        """
        Retrieve a paginated list of SharePoint sites.

        Args:
            page_size (int, optional): The maximum number of sites to return. Defaults to 50.

        Returns:
            SiteListResponse: A structured list of SharePoint site metadata.
        """
        logger.info("Manager: listing sites with page size %s", page_size)
        return await self.site_service.list_sites(top=page_size)

    async def get_site(self, site_id: str) -> Optional[SiteResponse]:
        """
        Retrieve a specific SharePoint site by its unique ID.

        Args:
            site_id (str): The unique identifier of the SharePoint site.

        Returns:
            Optional[SiteResponse]: Details of the requested site, or None if not found.
        """
        logger.info("Manager: retrieving site %s", site_id)
        return await self.site_service.get_site(site_id=site_id)

    async def search_sites(self, query: str) -> SiteListResponse:
        """
        Search for SharePoint sites matching a given query string.

        Args:
            query (str): The text query to search site names.

        Returns:
            SiteListResponse: A structured list of sites matching the search.
        """
        logger.info("Manager: searching sites with query '%s'", query)
        return await self.site_service.search_sites(query)
