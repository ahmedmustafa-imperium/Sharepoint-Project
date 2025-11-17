"""
Service layer for SharePoint site operations.

This module defines the `SiteService` class, which implements the business logic
for SharePoint site management. It acts as a bridge between the repository layer
(`SiteRepository`) and the manager or API layers.

Responsibilities:
- Handle application-level logic, validation, and orchestration.
- Delegate data mapping to the repository layer for consistency.
- Gracefully handle errors with logging for traceability.
"""

from typing import Optional
from app.repositories.site_repository import SiteRepository
from app.data.site import SiteResponse, SiteListResponse
from app.core.logging import get_logger


logger = get_logger(__name__)

class SiteService:
    """
    This class has 

    Responsibilities:
    - Handle application-level logic, validation, and orchestration.
    - Delegate mapping duties to the repository layer.
    - Gracefully handle errors with logging for traceability.
    """
    def __init__(self, repository: SiteRepository):
        """
        Initialize the SiteService with a repository dependency.

        Args:
            repository (SiteRepository): The repository class used to interact
                with Microsoft Graph API for SharePoint sites.
        """
        self.repository = repository

    async def list_sites(self, top: int = 50) -> SiteListResponse:
        """
        Retrieve a list of SharePoint sites already mapped into domain models.

        Args:
            top (int, optional): Maximum number of sites to retrieve. Defaults to 50.

        Returns:
            SiteListResponse: A response model containing the list of sites and total count.
        """
        sites = await self.repository.list_sites(top=top)
        return SiteListResponse(sites=sites, total=len(sites))

    async def get_site(self, site_id: str) -> Optional[SiteResponse]:
        """
        Retrieve details of a specific SharePoint site by its ID.

        Args:
            site_id (str): The unique identifier of the SharePoint site.

        Returns:
            Optional[SiteResponse]: The mapped site response model,
            or None if the site was not found.
        """
        site = await self.repository.get_site_by_id(site_id)
        if not site:
            return None
        return site

    async def search_sites(self, query: str) -> SiteListResponse:
        """
        Search for SharePoint sites by name.

        If no query is provided, this method defaults to listing all available sites.

        Args:
            query (str): The search string used to match sites.

        Returns:
            SiteListResponse: A structured response containing matched sites and total count.
        """
        if not query or query.strip() == "":
            return await self.list_sites()
        sites = await self.repository.search_sites(q=query)
        return SiteListResponse(sites=sites, total=len(sites))
