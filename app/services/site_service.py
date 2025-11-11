"""
Service layer for SharePoint site operations.

This module defines the `SiteService` class, which implements the business logic
for SharePoint site management. It acts as a bridge between the repository layer
(`SiteRepository`) and the manager or API layers.

Responsibilities:
- Handle application-level logic, validation, and data transformation.
- Map raw JSON data from Microsoft Graph into Pydantic response models.
- Gracefully handle mapping and data errors with logging for traceability.
"""

from typing import  Optional
import logging
from app.repositories.site_repository import SiteRepository
from app.data.site import SiteResponse, SiteListResponse
from app.utils.mapper import map_site_json


logger = logging.getLogger(__name__)

class SiteService:
    """
    This class has 

    Responsibilities:
    - Handle application-level logic, validation, and data transformation.
    - Map raw JSON data from Microsoft Graph into Pydantic response models.
    - Gracefully handle mapping and data errors with logging for traceability.
    """
    def __init__(self, repository: SiteRepository):
        """
        Initialize the SiteService with a repository dependency.

        Args:
            repository (SiteRepository): The repository class used to interact
                with Microsoft Graph API for SharePoint sites.
        """
        self.repository = repository()

    async def list_sites(self, top: int = 50) -> SiteListResponse:
        """
        Retrieve and map a list of SharePoint sites.

        Fetches raw site data from the repository and converts each item into
        a structured `SiteResponse` model using the `map_site_json` utility.

        Args:
            top (int, optional): Maximum number of sites to retrieve. Defaults to 50.

        Returns:
            SiteListResponse: A response model containing the list of sites and total count.
        """
        raw_sites = await self.repository.list_sites(top=top)
        sites = []
        for raw in raw_sites:
            try:
                site = map_site_json(raw)
                sites.append(site)
            except Exception as exc:
                logger.exception("Failed to map site JSON: %s", exc)
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
        raw = await self.repository.get_site_by_id(site_id)
        if not raw:
            return None
        return map_site_json(raw)

    async def search_sites(self, query: str) -> SiteListResponse:
        """
        Search for SharePoint sites by name.

        If no query is provided, this method defaults to listing all available sites.
        Raw results are mapped to `SiteResponse` models using the map_site_json utility.

        Args:
            query (str): The search string used to match sites.

        Returns:
            SiteListResponse: A structured response containing matched sites and total count.
        """
        if not query or query.strip() == "":
            return await self.list_sites()
        raw_sites = await self.repository.search_sites(q=query)
        sites = []
        for raw in raw_sites:
            try:
                sites.append(map_site_json(raw))
            except Exception:
                logger.exception("Failed to map site JSON during search")
        return SiteListResponse(sites=sites, total=len(sites))
