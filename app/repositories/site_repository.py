"""
Repository layer for interacting with SharePoint sites via Microsoft Graph API.

Provides low-level data access methods for retrieving SharePoint site information.
"""
from typing import List, Optional

from fastapi import status

from app.core.exceptions.sharepoint_exceptions import map_graph_error
from app.utils.graph_client import GraphClient, GraphAPIError
from app.utils.mapper import map_site_json
from app.data.site import SiteResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


class SiteRepository:
    """
    Repository for performing HTTP requests to Microsoft Graph API
    to fetch SharePoint site information.
    """

    def __init__(self, graph_client: GraphClient):
        self.graph_client = graph_client

    async def list_sites(self, top: int = 50) -> List[SiteResponse]:
        """
        List site collections accessible to the app. Uses Graph: /sites?search=*
        Note: Graph permissions and tenant settings affect results.
        """
        params = {"search": "*", "$top": top}
        logger.info("Listing SharePoint sites with top=%d", top)

        try:
            response = await self.graph_client.get("sites", params=params)
            sites = []
            for raw_site in response.get("value", []):
                try:
                    sites.append(map_site_json(raw_site))
                except Exception as exc:
                    logger.warning("Failed to map site response: %s", exc)
            return sites
        except GraphAPIError as exc:
            logger.exception("Failed to list sites")
            raise map_graph_error(
                "list SharePoint sites",
                status_code=exc.status_code or status.HTTP_502_BAD_GATEWAY,
                details=exc.response_body,
            ) from exc

    async def get_site_by_id(self, site_id: str) -> Optional[SiteResponse]:
        """
        Retrieve details of a specific SharePoint site by its unique ID.

        Args:
            site_id (str): The unique identifier of the SharePoint site.

        Returns:
            Dict[str, Any]: A dictionary containing site metadata and details.
        """
        endpoint = f"sites/{site_id}"
        logger.info("Retrieving SharePoint site %s", site_id)

        try:
            response = await self.graph_client.get(endpoint)
            if not response:
                return None
            try:
                return map_site_json(response)
            except Exception as exc:
                logger.exception("Failed to map site %s", site_id)
                raise map_graph_error(
                    "map SharePoint site",
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    details=str(exc),
                ) from exc
        except GraphAPIError as exc:
            logger.exception("Failed to retrieve site %s", site_id)
            raise map_graph_error(
                "retrieve SharePoint site",
                status_code=exc.status_code or status.HTTP_502_BAD_GATEWAY,
                details=exc.response_body,
            ) from exc

    async def search_sites(self, q: str) -> List[SiteResponse]:
        """
        Search sites by display name.
        Uses /sites?search=<q>
        """
        params = {"search": q}
        logger.info("Searching SharePoint sites with query '%s'", q)

        try:
            response = await self.graph_client.get("sites", params=params)
            sites = []
            for raw_site in response.get("value", []):
                try:
                    sites.append(map_site_json(raw_site))
                except Exception as exc:
                    logger.warning("Failed to map site response during search: %s", exc)
            return sites
        except GraphAPIError as exc:
            logger.exception("Failed to search sites with query '%s'", q)
            raise map_graph_error(
                "search SharePoint sites",
                status_code=exc.status_code or status.HTTP_502_BAD_GATEWAY,
                details=exc.response_body,
            ) from exc
