"""
Manager for SharePoint List Items orchestration.

Coordinates list item operations between API layer and services.
Handles caching, batch operations, and complex workflows.
"""
import logging
from typing import Optional
from app.services.list_item_service import ListItemService
from app.data.list_item import (
    ListItemResponse,
    ListItemListResponse,
    ListItemCreateRequest,
    ListItemUpdateRequest,
    AttachmentResponse,
    AttachmentListResponse,
    ListItemVersionResponse,
    ListItemVersionListResponse
)

logger = logging.getLogger(__name__)


class SharePointListItemManager:
    """
    Orchestrator for SharePoint list item operations.
    
    Coordinates between FastAPI endpoints and ListItemService.
    Handles caching, batch operations, and complex workflows.
    """
    
    def __init__(self, list_item_service: ListItemService):
        """
        Initialize SharePoint list item manager.
        
        Args:
            list_item_service: Service for list item business logic
        """
        self.list_item_service = list_item_service

    async def get_list_items(
        self,
        site_id: str,
        list_id: str,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None
    ) -> ListItemListResponse:
        """
        Get all items in a list.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            top: Maximum number of items to return
            skip: Number of items to skip
            filter_query: OData filter query string
            
        Returns:
            ListItemListResponse with all items
        """
        logger.info("Getting items for list %s in site %s",list_id,site_id)
        return await self.list_item_service.get_list_items(
            site_id=site_id,
            list_id=list_id,
            top=top,
            skip=skip,
            filter_query=filter_query
        )

    async def get_list_item_by_id(
        self,
        site_id: str,
        list_id: str,
        item_id: str
    ) -> ListItemResponse:
        """
        Get a list item by ID.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            item_id: Item ID
            
        Returns:
            ListItemResponse with item details
        """
        logger.info("Getting item %s from list %s in site %s",item_id,list_id,site_id)
        return await self.list_item_service.get_list_item_by_id(site_id, list_id, item_id)

    async def create_list_item(
        self,
        site_id: str,
        list_id: str,
        request: ListItemCreateRequest
    ) -> ListItemResponse:
        """
        Create a new list item.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            request: List item creation request
            
        Returns:
            ListItemResponse with created item details
        """
        logger.info("Creating item in list %s in site %s",list_id,site_id)
        return await self.list_item_service.create_list_item(site_id, list_id, request)

    async def update_list_item(
        self,
        site_id: str,
        list_id: str,
        item_id: str,
        request: ListItemUpdateRequest
    ) -> ListItemResponse:
        """
        Update a list item.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            item_id: Item ID
            request: List item update request
            
        Returns:
            ListItemResponse with updated item details
        """
        logger.info("Updating item %s in list %s in site %s",item_id,list_id,site_id)
        return await self.list_item_service.update_list_item(site_id, list_id, item_id, request)

    async def delete_list_item(self, site_id: str, list_id: str, item_id: str) -> None:
        """
        Delete a list item.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            item_id: Item ID
        """
        logger.info("Deleting item %s from list %s in site %s",item_id,list_id,site_id)
        await self.list_item_service.delete_list_item(site_id, list_id, item_id)

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
        """
        logger.info("Getting attachments for item %s in list %s",item_id,list_id)
        return await self.list_item_service.get_item_attachments(site_id, list_id, item_id)

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
        """
        logger.info("Adding attachment '%s' to item %s in list %s",name,item_id,list_id)
        return await self.list_item_service.add_attachment(
            site_id=site_id,
            list_id=list_id,
            item_id=item_id,
            name=name,
            content_bytes=content_bytes,
            content_type=content_type
        )

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
        """
        logger.info("Deleting attachment %s from item %s",attachment_id,item_id)
        await self.list_item_service.delete_attachment(site_id, list_id, item_id, attachment_id)

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
        """
        logger.info("Getting versions for item %s in list %s",item_id,list_id)
        return await self.list_item_service.get_item_versions(site_id, list_id, item_id)

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
        """
        logger.info("Getting version %s for item %s in list %s",version_id,item_id,list_id)
        return await self.list_item_service.get_item_version_by_id(
            site_id, list_id, item_id, version_id
        )

