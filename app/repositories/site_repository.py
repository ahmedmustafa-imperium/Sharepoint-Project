"""
Repository layer for interacting with SharePoint sites via Microsoft Graph API.

This module defines the `SiteRepository` class, which provides low-level data access
methods for retrieving SharePoint site information. It communicates directly with
Microsoft Graph endpoints to perform operations such as:

- Listing available SharePoint sites.
- Fetching details of a site by its ID.
- Searching for sites by name.

Responsibilities:
- Handle HTTP communication using `httpx.AsyncClient`.
- Manage access tokens through the `SharePointAuthManager`.
"""
import logging
from typing import List, Dict, Any
import httpx
from app.core.config import settings
from app.managers.sharepoint_auth_manager import SharePointAuthManager


logger = logging.getLogger(__name__)

class SiteRepository:
    """
    Repository for performing HTTP requests to Microsoft Graph API
    to fetch SharePoint site information.
    """
    def __init__(self, base_url: str = None, timeout: int = 10):
        """
        Initialize the SiteRepository with API base URL and timeout settings.

        Args:
            base_url (str, optional): The base URL for Microsoft Graph API.
                Defaults to the value from `settings.GRAPH_BASE_URL`.
            timeout (int, optional): Timeout for HTTP requests in seconds.
                Defaults to 10 seconds.
        """
        self.base_url = base_url or str(settings.GRAPH_BASE_URL)
        self.timeout = timeout
        # client can be shared; httpx.AsyncClient recommended
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(self.timeout))

    async def _get_access_token(self) -> str:
        """
        Acquire or reuse a cached access token for Microsoft Graph.
        This uses token_cache interface; replace if you have another implementation.
        """
        token=SharePointAuthManager()
        access_token=await token.get_access_token()

        return access_token

    async def _get_headers(self) -> Dict[str, str]:
        """
        Build authorization 
        """
        token = await self._get_access_token()
        return {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    async def list_sites(self, top: int = 50) -> List[Dict[str, Any]]:
        """
        List site collections accessible to the app. Uses Graph: /sites?search=*
        Note: Graph permissions and tenant settings affect results.
        """
        headers = await self._get_headers()
        url = f"{self.base_url}/sites?search=*"
        params = {"$top": top}
        resp = await self._client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("value", [])
        return items


    async def get_site_by_id(self, site_id: str) -> Dict[str, Any]:
        """
        Retrieve details of a specific SharePoint site by its unique ID.

        Args:
            site_id (str): The unique identifier of the SharePoint site.

        Returns:
            Dict[str, Any]: A dictionary containing site metadata and details.
        """
        headers = await self._get_headers()
        url = f"{self.base_url}/sites/{site_id}"
        resp = await self._client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()


    async def search_sites(self, q: str) -> List[Dict[str, Any]]:
        """
        Search sites by display name.
        Use Graph Search or filter client-side if needed.
        For simplicity, we use /sites?search=<q>
        """
        headers = await self._get_headers()
        url = f"{self.base_url}/sites?search={q}"
        resp = await self._client.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data.get("value", [])

    async def close(self):
        """
        Close the underlying HTTP client connection.

        Should be called during application shutdown to clean up network resources.
        """
        await self._client.aclose()
