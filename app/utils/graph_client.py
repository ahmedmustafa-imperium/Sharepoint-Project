from typing import Any, Dict, Optional
import httpx


class GraphClient:
    """
    Thin async wrapper around httpx.AsyncClient.
    Reuse a single AsyncClient to maintain connection pooling.
    """

    def __init__(self, timeout: int = 60):
        self._timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._timeout)
        return self._client

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def request(self, method: str, url: str, *, headers: Optional[Dict[str, str]] = None,
                      params: Optional[Dict[str, Any]] = None, data: Any = None, json: Any = None,
                      stream: bool = False) -> httpx.Response:
        client = await self._get_client()
        # httpx will handle stream param inside client.request if needed
        resp = await client.request(method, url, headers=headers, params=params, data=data, json=json)
        return resp

    async def stream(self, method: str, url: str, *, headers: Optional[Dict[str, str]] = None):
        client = await self._get_client()
        return client.stream(method, url, headers=headers)
    
class GraphAPIError:
    pass
