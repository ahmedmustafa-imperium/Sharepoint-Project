"""
Repository for SharePoint Lists data access.

Handles all direct Microsoft Graph API calls for list operations.
"""
import logging
from typing import Optional, Dict, Any, List
from app.utils.graph_client import GraphClient, GraphAPIError
from app.utils.mapper import (
    map_list_response,
    map_list_list_response,
    map_list_column_response,
    map_list_content_type_response
)
from app.data.list import (
    ListResponse,
    ListListResponse,
    ListColumnResponse,
    ListContentTypeResponse
)

logger = logging.getLogger(__name__)


class ListRepository:
    """
    Repository for SharePoint list operations.
    
    Handles all direct API calls to Microsoft Graph API for lists.
    """
    
    def __init__(self, graph_client: GraphClient):
        """
        Initialize list repository.
        
        Args:
            graph_client: HTTP client for making API requests
        """
        self.graph_client = graph_client

    async def get_lists(self, site_id: str, top: Optional[int] = None, skip: Optional[int] = None) -> ListListResponse:
        """
        Get all lists for a SharePoint site.
        
        Args:
            site_id: SharePoint site ID
            top: Maximum number of items to return
            skip: Number of items to skip
            
        Returns:
            ListListResponse with all lists
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists"
        params = {}
        if top:
            params["$top"] = top
        if skip:
            params["$skip"] = skip
        
        try:
            response = await self.graph_client.get(endpoint, params=params)
            return map_list_list_response(response)
        except GraphAPIError as e:
            logger.error(f"Failed to get lists for site {site_id}: {e}")
            raise

    async def get_list_by_id(self, site_id: str, list_id: str) -> ListResponse:
        """
        Get a list by ID.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            
        Returns:
            ListResponse with list details
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists/{list_id}"
        
        try:
            response = await self.graph_client.get(endpoint)
            return map_list_response(response)
        except GraphAPIError as e:
            logger.error(f"Failed to get list {list_id} from site {site_id}: {e}")
            raise

    async def create_list(
        self,
        site_id: str,
        display_name: str,
        description: Optional[str] = None,
        template: Optional[str] = None,
        columns: Optional[List[Dict[str, Any]]] = None
    ) -> ListResponse:
        """
        Create a new list in a SharePoint site.
        
        Args:
            site_id: SharePoint site ID
            display_name: Display name for the list
            description: Optional description
            template: List template (e.g., 'genericList', 'documentLibrary')
            columns: Optional list of column definitions
            
        Returns:
            ListResponse with created list details
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists"
        
        payload: Dict[str, Any] = {
            "displayName": display_name,
            "template": template or "genericList"
        }
        
        if description:
            payload["description"] = description
        
        if columns:
            payload["columns"] = columns
        
        try:
            response = await self.graph_client.post(endpoint, json=payload)
            return map_list_response(response)
        except GraphAPIError as e:
            logger.error(f"Failed to create list in site {site_id}: {e}")
            raise

    async def update_list(
        self,
        site_id: str,
        list_id: str,
        display_name: Optional[str] = None,
        description: Optional[str] = None
    ) -> ListResponse:
        """
        Update a list.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            display_name: New display name (optional)
            description: New description (optional)
            
        Returns:
            ListResponse with updated list details
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists/{list_id}"
        
        payload: Dict[str, Any] = {}
        if display_name:
            payload["displayName"] = display_name
        if description:
            payload["description"] = description
        
        if not payload:
            # Nothing to update, just return the current list
            return await self.get_list_by_id(site_id, list_id)
        
        try:
            response = await self.graph_client.patch(endpoint, json=payload)
            return map_list_response(response)
        except GraphAPIError as e:
            logger.error(f"Failed to update list {list_id} in site {site_id}: {e}")
            raise

    async def delete_list(self, site_id: str, list_id: str) -> None:
        """
        Delete a list.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists/{list_id}"
        
        try:
            await self.graph_client.delete(endpoint)
            logger.info(f"Successfully deleted list {list_id} from site {site_id}")
        except GraphAPIError as e:
            logger.error(f"Failed to delete list {list_id} from site {site_id}: {e}")
            raise

    async def get_list_columns(self, site_id: str, list_id: str) -> List[ListColumnResponse]:
        """
        Get columns for a list.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            
        Returns:
            List of ListColumnResponse
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists/{list_id}/columns"
        
        try:
            response = await self.graph_client.get(endpoint)
            columns = response.get("value", [])
            return [map_list_column_response(col) for col in columns]
        except GraphAPIError as e:
            logger.error(f"Failed to get columns for list {list_id} in site {site_id}: {e}")
            raise

    async def get_list_content_types(self, site_id: str, list_id: str) -> List[ListContentTypeResponse]:
        """
        Get content types for a list.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            
        Returns:
            List of ListContentTypeResponse
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists/{list_id}/contentTypes"
        
        try:
            response = await self.graph_client.get(endpoint)
            content_types = response.get("value", [])
            return [map_list_content_type_response(ct) for ct in content_types]
        except GraphAPIError as e:
            logger.error(f"Failed to get content types for list {list_id} in site {site_id}: {e}")
            raise

