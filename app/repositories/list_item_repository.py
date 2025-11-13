"""
Repository for SharePoint List Items data access.

Handles all direct Microsoft Graph API calls for list item operations.
"""
import logging
import base64
from typing import Optional, Dict, Any
from fastapi import status
from app.utils.graph_client import GraphClient, GraphAPIError
from app.utils.mapper import (
    map_list_item_response,
    map_list_item_list_response,
    map_attachment_response,
    map_attachment_list_response,
    map_list_item_version_response,
    map_list_item_version_list_response,
)
from app.data.list_item import (
    ListItemResponse,
    ListItemListResponse,
    AttachmentResponse,
    AttachmentListResponse,
    ListItemVersionResponse,
    ListItemVersionListResponse,
)
from app.core.exceptions.sharepoint_exceptions import map_graph_error

logger = logging.getLogger(__name__)


class ListItemRepository:
    """
    Repository for SharePoint list item operations.
    
    Handles all direct API calls to Microsoft Graph API for list items.
    """

    def __init__(self, graph_client: GraphClient):
        """
        Initialize list item repository.
        
        Args:
            graph_client: HTTP client for making API requests
        """
        self.graph_client = graph_client

    async def get_list_items(
        self,
        site_id: str,
        list_id: str,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        expand_fields: bool = True
    ) -> ListItemListResponse:
        """
        Get all items in a list.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            top: Maximum number of items to return
            skip: Number of items to skip
            filter_query: OData filter query string
            expand_fields: Whether to expand fields in response
            
        Returns:
            ListItemListResponse with all items
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists/{list_id}/items"
        params: Dict[str, Any] = {}

        if top:
            params["$top"] = top
        if skip:
            params["$skip"] = skip
        if filter_query:
            params["$filter"] = filter_query
        if expand_fields:
            params["$expand"] = "fields"

        logger.info(
            "Fetching list items for site %s list %s (top=%s skip=%s)",
            site_id,
            list_id,
            top,
            skip,
        )

        try:
            response = await self.graph_client.get(endpoint, params=params)
            return map_list_item_list_response(response)
        except GraphAPIError as exc:
            logger.exception("Failed to get items for list %s in site %s", list_id, site_id)
            raise map_graph_error(
                "list SharePoint list items",
                status_code=exc.status_code or status.HTTP_502_BAD_GATEWAY,
                details=exc.response_body,
            ) from exc

    async def get_list_item_by_id(
        self,
        site_id: str,
        list_id: str,
        item_id: str,
        expand_fields: bool = True
    ) -> ListItemResponse:
        """
        Get a list item by ID.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            item_id: Item ID
            expand_fields: Whether to expand fields in response
            
        Returns:
            ListItemResponse with item details
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists/{list_id}/items/{item_id}"
        params = {}
        if expand_fields:
            params["$expand"] = "fields"

        logger.info("Fetching item %s for list %s in site %s", item_id, list_id, site_id)

        try:
            response = await self.graph_client.get(endpoint, params=params)
            return map_list_item_response(response)
        except GraphAPIError as exc:
            logger.exception("Failed to get item %s for list %s in site %s", item_id, list_id, site_id)
            raise map_graph_error(
                "retrieve list item",
                status_code=exc.status_code or status.HTTP_502_BAD_GATEWAY,
                details=exc.response_body,
            ) from exc

    async def create_list_item(
        self,
        site_id: str,
        list_id: str,
        fields: Dict[str, Any]
    ) -> ListItemResponse:
        """
        Create a new list item.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            fields: Dictionary of field values for the item
            
        Returns:
            ListItemResponse with created item details
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists/{list_id}/items"

        payload = {
            "fields": fields
        }

        try:
            response = await self.graph_client.post(endpoint, json=payload)
            item_id = response.get("id")
            if item_id:
                return await self.get_list_item_by_id(site_id, list_id, item_id, expand_fields=True)
            return map_list_item_response(response)
        except GraphAPIError as exc:
            logger.exception("Failed to create item for list %s in site %s", list_id, site_id)
            raise map_graph_error(
                "create list item",
                status_code=exc.status_code or status.HTTP_502_BAD_GATEWAY,
                details=exc.response_body,
            ) from exc

    async def update_list_item(
        self,
        site_id: str,
        list_id: str,
        item_id: str,
        fields: Dict[str, Any]
    ) -> ListItemResponse:
        """
        Update a list item.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            item_id: Item ID
            fields: Dictionary of field values to update
            
        Returns:
            ListItemResponse with updated item details
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists/{list_id}/items/{item_id}/fields"

        payload = fields

        try:
            await self.graph_client.patch(endpoint, json=payload)
            return await self.get_list_item_by_id(site_id, list_id, item_id, expand_fields=True)
        except GraphAPIError as exc:
            logger.exception("Failed to update item %s for list %s in site %s", item_id, list_id, site_id)
            raise map_graph_error(
                "update list item",
                status_code=exc.status_code or status.HTTP_502_BAD_GATEWAY,
                details=exc.response_body,
            ) from exc

    async def delete_list_item(self, site_id: str, list_id: str, item_id: str) -> None:
        """
        Delete a list item.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            item_id: Item ID
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists/{list_id}/items/{item_id}"

        try:
            await self.graph_client.delete(endpoint)
            logger.info("Successfully deleted item %s from list %s in site %s", item_id, list_id, site_id)
        except GraphAPIError as exc:
            logger.exception("Failed to delete item %s from list %s in site %s", item_id, list_id, site_id)
            raise map_graph_error(
                "delete list item",
                status_code=exc.status_code or status.HTTP_502_BAD_GATEWAY,
                details=exc.response_body,
            ) from exc

    async def get_item_attachments(
        self,
        site_id: str,
        list_id: str,
        item_id: str
    ) -> AttachmentListResponse:
        """
        Get attachments for a list item.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            item_id: Item ID
            
        Returns:
            AttachmentListResponse with all attachments
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists/{list_id}/items/{item_id}/attachments"

        try:
            response = await self.graph_client.get(endpoint)
            return map_attachment_list_response(response)
        except GraphAPIError as exc:
            logger.exception("Failed to get attachments for item %s in list %s", item_id, list_id)
            raise map_graph_error(
                "retrieve list item attachments",
                status_code=exc.status_code or status.HTTP_502_BAD_GATEWAY,
                details=exc.response_body,
            ) from exc

    async def add_attachment(
        self,
        site_id: str,
        list_id: str,
        item_id: str,
        name: str,
        content_bytes: bytes,
        content_type: str = "application/octet-stream"
    ) -> AttachmentResponse:
        """
        Add an attachment to a list item.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            item_id: Item ID
            name: Attachment file name
            content_bytes: Attachment file content as bytes
            content_type: MIME type of the attachment
            
        Returns:
            AttachmentResponse with attachment details
            
        Raises:
            GraphAPIError: If API request fails
        """

        endpoint = f"sites/{site_id}/lists/{list_id}/items/{item_id}/attachments"

        # Graph API requires base64 encoded content for attachments
        content_base64 = base64.b64encode(content_bytes).decode('utf-8')

        payload = {
            "name": name,
            "contentBytes": content_base64,
            "contentType": content_type
        }

        try:
            response = await self.graph_client.post(endpoint, json=payload)
            return map_attachment_response(response)
        except GraphAPIError as exc:
            logger.exception("Failed to add attachment to item %s in list %s", item_id, list_id)
            raise map_graph_error(
                "add list item attachment",
                status_code=exc.status_code or status.HTTP_502_BAD_GATEWAY,
                details=exc.response_body,
            ) from exc

    async def delete_attachment(
        self,
        site_id: str,
        list_id: str,
        item_id: str,
        attachment_id: str
    ) -> None:
        """
        Delete an attachment from a list item.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            item_id: Item ID
            attachment_id: Attachment ID
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists/{list_id}/items/{item_id}/attachments/{attachment_id}"

        try:
            await self.graph_client.delete(endpoint)
            logger.info("Successfully deleted attachment %s from item %s", attachment_id, item_id)
        except GraphAPIError as exc:
            logger.exception("Failed to delete attachment %s from item %s", attachment_id, item_id)
            raise map_graph_error(
                "delete list item attachment",
                status_code=exc.status_code or status.HTTP_502_BAD_GATEWAY,
                details=exc.response_body,
            ) from exc

    async def get_item_versions(
        self,
        site_id: str,
        list_id: str,
        item_id: str
    ) -> ListItemVersionListResponse:
        """
        Get version history for a list item.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            item_id: Item ID
            
        Returns:
            ListItemVersionListResponse with all versions
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists/{list_id}/items/{item_id}/versions"

        try:
            response = await self.graph_client.get(endpoint)
            return map_list_item_version_list_response(response)
        except GraphAPIError as exc:
            logger.exception("Failed to get versions for item %s in list %s", item_id, list_id)
            raise map_graph_error(
                "retrieve list item versions",
                status_code=exc.status_code or status.HTTP_502_BAD_GATEWAY,
                details=exc.response_body,
            ) from exc

    async def get_item_version_by_id(
        self,
        site_id: str,
        list_id: str,
        item_id: str,
        version_id: str
    ) -> ListItemVersionResponse:
        """
        Get a specific version of a list item.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            item_id: Item ID
            version_id: Version ID
            
        Returns:
            ListItemVersionResponse with version details
            
        Raises:
            GraphAPIError: If API request fails
        """
        endpoint = f"sites/{site_id}/lists/{list_id}/items/{item_id}/versions/{version_id}"

        try:
            response = await self.graph_client.get(endpoint)
            return map_list_item_version_response(response)
        except GraphAPIError as exc:
            logger.exception("Failed to get version %s for item %s", version_id, item_id)
            raise map_graph_error(
                "retrieve list item version",
                status_code=exc.status_code or status.HTTP_502_BAD_GATEWAY,
                details=exc.response_body,
            ) from exc
