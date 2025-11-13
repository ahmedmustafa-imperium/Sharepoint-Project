"""
Repository layer for interacting with SharePoint sites via Microsoft Graph API.

Provides low-level data access methods for retrieving SharePoint site information.
"""
import logging
from typing import List, Dict, Any

from app.utils.graph_client import GraphClient, GraphAPIError

logger = logging.getLogger(__name__)


class SiteRepository:
    """
    Repository for performing HTTP requests to Microsoft Graph API
    to fetch SharePoint site information.
    """

    def __init__(self, graph_client: GraphClient):
        self.graph_client = graph_client

    async def list_sites(self, top: int = 50) -> List[Dict[str, Any]]:
        """
        List site collections accessible to the app. Uses Graph: /sites?search=*
        Note: Graph permissions and tenant settings affect results.
        """
        params = {"search": "*", "$top": top}

        try:
            response = await self.graph_client.get("sites", params=params)
            return response.get("value", [])
        except GraphAPIError as exc:
            logger.error("Failed to list sites: %s", exc)
            raise

    async def get_site_by_id(self, site_id: str) -> Dict[str, Any]:
        """
        Retrieve details of a specific SharePoint site by its unique ID.

        Args:
            site_id (str): The unique identifier of the SharePoint site.

        Returns:
            Dict[str, Any]: A dictionary containing site metadata and details.
        """
        endpoint = f"sites/{site_id}"

        try:
            return await self.graph_client.get(endpoint)
        except GraphAPIError as exc:
            logger.error("Failed to retrieve site %s: %s", site_id, exc)
            raise

    async def search_sites(self, q: str) -> List[Dict[str, Any]]:
        """
        Search sites by display name.
        Uses /sites?search=<q>
        """
        params = {"search": q}

        try:
            response = await self.graph_client.get("sites", params=params)
            return response.get("value", [])
        except GraphAPIError as exc:
            logger.error("Failed to search sites with query '%s': %s", q, exc)
            raise
