"""
HTTP client utility for making requests to Microsoft Graph API.

Provides async HTTP client with automatic token injection, retry policy,
and error handling.
"""
import logging
from typing import Optional, Dict, Any, Callable, Awaitable
import httpx
from app.core.config import settings
from app.utils.retry_policy import RetryPolicy, retry_with_policy

logger = logging.getLogger(__name__)


class GraphAPIError(Exception):
    """Exception raised for Graph API errors."""
    def __init__(self, message: str, status_code: int, response_body: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class GraphClient:
    """
    HTTP client for Microsoft Graph API requests.
    
    Handles:
    - Automatic token injection
    - Retry policy for transient failures
    - Error handling and logging
    """
    
    def __init__(
        self,
        token_getter: Callable[[], Awaitable[str]],
        retry_policy: Optional[RetryPolicy] = None,
        timeout: float = 30.0
    ):
        """
        Initialize HTTP client.
        
        Args:
            token_getter: Async function that returns an access token
            retry_policy: Retry policy for requests
            timeout: Request timeout in seconds
        """
        self.token_getter = token_getter
        self.retry_policy = retry_policy or RetryPolicy()
        self.timeout = timeout
        self.base_url = settings.GRAPH_BASE.rstrip("/")

    async def _get_headers(self) -> Dict[str, str]:
        """
        Get HTTP headers with authorization token.
        
        Returns:
            Dictionary of HTTP headers
        """
        token = await self.token_getter()
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> httpx.Response:
        """
        Make an HTTP request to Microsoft Graph API.
        
        Args:
            method: HTTP method (GET, POST, PATCH, DELETE, etc.)
            endpoint: API endpoint (relative to base URL)
            headers: Additional headers (authorization is added automatically)
            json: JSON body for request
            params: Query parameters
            **kwargs: Additional arguments for httpx request
            
        Returns:
            HTTP response
            
        Raises:
            GraphAPIError: If request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = await self._get_headers()
        if headers:
            request_headers.update(headers)
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    json=json,
                    params=params,
                    **kwargs
                )
                
                # Raise exception for non-2xx status codes
                if not response.is_success:
                    error_msg = f"Graph API request failed: {method} {url}"
                    try:
                        error_body = response.json()
                        error_msg = error_body.get("error", {}).get("message", error_msg)
                    except Exception:
                        error_body = response.text
                    
                    raise GraphAPIError(
                        message=error_msg,
                        status_code=response.status_code,
                        response_body=error_body if isinstance(error_body, str) else str(error_body)
                    )
                
                return response
                
            except httpx.HTTPStatusError as e:
                raise GraphAPIError(
                    message=str(e),
                    status_code=e.response.status_code,
                    response_body=e.response.text
                )
            except httpx.RequestError as e:
                logger.error(f"HTTP request error: {e}")
                raise GraphAPIError(
                    message=f"Request failed: {str(e)}",
                    status_code=0,
                    response_body=None
                )

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make a GET request to Microsoft Graph API.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers
            **kwargs: Additional arguments
            
        Returns:
            JSON response as dictionary
        """
        async def _get():
            response = await self._make_request(
                method="GET",
                endpoint=endpoint,
                params=params,
                headers=headers,
                **kwargs
            )
            return response.json()
        
        # Apply retry policy
        response_data = await retry_with_policy(_get, self.retry_policy)
        return response_data

    async def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make a POST request to Microsoft Graph API.
        
        Args:
            endpoint: API endpoint
            json: JSON body
            headers: Additional headers
            **kwargs: Additional arguments
            
        Returns:
            JSON response as dictionary
        """
        async def _post():
            response = await self._make_request(
                method="POST",
                endpoint=endpoint,
                json=json,
                headers=headers,
                **kwargs
            )
            return response.json()
        
        response_data = await retry_with_policy(_post, self.retry_policy)
        return response_data

    async def patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make a PATCH request to Microsoft Graph API.
        
        Args:
            endpoint: API endpoint
            json: JSON body
            headers: Additional headers
            **kwargs: Additional arguments
            
        Returns:
            JSON response as dictionary
        """
        async def _patch():
            response = await self._make_request(
                method="PATCH",
                endpoint=endpoint,
                json=json,
                headers=headers,
                **kwargs
            )
            return response.json()
        
        response_data = await retry_with_policy(_patch, self.retry_policy)
        return response_data

    async def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> None:
        """
        Make a DELETE request to Microsoft Graph API.
        
        Args:
            endpoint: API endpoint
            headers: Additional headers
            **kwargs: Additional arguments
        """
        async def _delete():
            response = await self._make_request(
                method="DELETE",
                endpoint=endpoint,
                headers=headers,
                **kwargs
            )
            return response
        
        await retry_with_policy(_delete, self.retry_policy)
