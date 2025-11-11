import logging
from typing import List, Dict, Any
import httpx
from app.core.config import settings
from app.managers.sharepoint_auth_manager import SharePointAuthManager


logger = logging.getLogger(__name__)

class SiteRepository:
    def __init__(self, base_url: str = None, timeout: int = 10):
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
        token = await self._get_access_token()
        return {"Authorization": f"Bearer {token}", "Accept": "application/json"}

   
    async def list_sites(self, top: int = 50) -> List[Dict[str, Any]]:
        """
        List site collections accessible to the app. Uses Graph: /sites?search=*
        Note: Graph permissions and tenant settings affect results.
        """
        headers = await self._get_headers()
        # Graph doesn't have direct "list all sites" for tenant without Search permission; common approach is to use /sites?search=*
        url = f"{self.base_url}/sites?search=*"
        params = {"$top": top}
        resp = await self._client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("value", [])
        return items


    async def get_site_by_id(self, site_id: str) -> Dict[str, Any]:
        headers = await self._get_headers()
        url = f"{self.base_url}/sites/{site_id}"
        resp = await self._client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    async def search_sites(self, q: str) -> List[Dict[str, Any]]:
        """
        Search sites by display name or url.
        Use Graph Search or filter client-side if needed.
        For simplicity, we use /sites?search=<q>
        """
        headers = await self._get_headers()
        url = f"{self.base_url}/sites?search={q}"
      
        resp = await self._client.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data.get("value", [])

    # Optional: cleanup
    async def close(self):
        await self._client.aclose()
