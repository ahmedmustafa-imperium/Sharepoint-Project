"""
Service for SharePoint List Items business logic.

Contains validation and business rules for list item operations.
"""
from typing import Optional
from app.repositories.list_item_repository import ListItemRepository
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
from app.core.logging import get_logger

logger = get_logger(__name__)


class ListItemService:
    """
    Service for SharePoint list item business logic.
    
    Handles validation and business rules for list item operations.
    """

    def __init__(self, list_item_repository: ListItemRepository):
        """
        Initialize list item service.
        
        Args:
            list_item_repository: Repository for list item data access
        """
        self.list_item_repository = list_item_repository

    def validate_list_item_create_request(self, request: ListItemCreateRequest) -> None:
        """
        Validate list item creation request.
        
        Args:
            request: List item creation request
            
        Raises:
            ValueError: If validation fails
        """
        if not request.fields:
            raise ValueError("Fields are required for list item creation")

        # Validate that Title field is present (common requirement)
        # Note: This might vary by list, so we'll log a warning but not fail
        if "Title" not in request.fields and "title" not in request.fields:
            logger.warning("List item does not have a Title field - this may be required by some lists")

    def validate_list_item_update_request(self, request: ListItemUpdateRequest) -> None:
        """
        Validate list item update request.
        
        Args:
            request: List item update request
            
        Raises:
            ValueError: If validation fails
        """
        if not request.fields:
            raise ValueError("Fields are required for list item update")

        # Validate that fields are not empty
        if not any(request.fields.values()):
            logger.warning("All fields are empty in update request")

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
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")

        # Validate pagination parameters
        if top is not None and top < 1:
            raise ValueError("Top must be greater than 0")
        if skip is not None and skip < 0:
            raise ValueError("Skip must be greater than or equal to 0")

        return await self.list_item_repository.get_list_items(
            site_id=site_id,
            list_id=list_id,
            top=top,
            skip=skip,
            filter_query=filter_query,
            expand_fields=True
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
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")
        if not item_id:
            raise ValueError("Item ID is required")
        
        return await self.list_item_repository.get_list_item_by_id(
            site_id=site_id,
            list_id=list_id,
            item_id=item_id,
            expand_fields=True
        )

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
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")

        self.validate_list_item_create_request(request)

        return await self.list_item_repository.create_list_item(
            site_id=site_id,
            list_id=list_id,
            fields=request.fields
        )

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
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")
        if not item_id:
            raise ValueError("Item ID is required")

        self.validate_list_item_update_request(request)

        return await self.list_item_repository.update_list_item(
            site_id=site_id,
            list_id=list_id,
            item_id=item_id,
            fields=request.fields
        )

    async def delete_list_item(self, site_id: str, list_id: str, item_id: str) -> None:
        """
        Delete a list item.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            item_id: Item ID
        """
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")
        if not item_id:
            raise ValueError("Item ID is required")

        await self.list_item_repository.delete_list_item(site_id, list_id, item_id)

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
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")
        if not item_id:
            raise ValueError("Item ID is required")

        return await self.list_item_repository.get_item_attachments(site_id, list_id, item_id)

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
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")
        if not item_id:
            raise ValueError("Item ID is required")
        if not name:
            raise ValueError("Attachment name is required")
        if not content_bytes:
            raise ValueError("Attachment content is required")

        # Validate file name
        if len(name) > 255:
            raise ValueError("Attachment name must be 255 characters or less")

        return await self.list_item_repository.add_attachment(
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
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")
        if not item_id:
            raise ValueError("Item ID is required")
        if not attachment_id:
            raise ValueError("Attachment ID is required")

        await self.list_item_repository.delete_attachment(site_id, list_id, item_id, attachment_id)

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
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")
        if not item_id:
            raise ValueError("Item ID is required")

        return await self.list_item_repository.get_item_versions(site_id, list_id, item_id)

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
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")
        if not item_id:
            raise ValueError("Item ID is required")
        if not version_id:
            raise ValueError("Version ID is required")

        return await self.list_item_repository.get_item_version_by_id(
            site_id, list_id, item_id, version_id
        )
