"""
Service for SharePoint Lists business logic.

Contains validation and business rules for list operations.
"""
import logging
from typing import Optional, List
from app.repositories.list_repository import ListRepository
from app.data.list import (
    ListResponse,
    ListListResponse,
    ListCreateRequest,
    ListUpdateRequest,
    ListColumnResponse,
    ListContentTypeResponse
)

logger = logging.getLogger(__name__)


class ListService:
    """
    Service for SharePoint list business logic.
    
    Handles validation and business rules for list operations.
    """
    
    def __init__(self, list_repository: ListRepository):
        """
        Initialize list service.
        
        Args:
            list_repository: Repository for list data access
        """
        self.list_repository = list_repository

    def validate_list_create_request(self, request: ListCreateRequest) -> None:
        """
        Validate list creation request.
        
        Args:
            request: List creation request
            
        Raises:
            ValueError: If validation fails
        """
        if not request.display_name or not request.display_name.strip():
            raise ValueError("List display name is required")
        
        if len(request.display_name) > 255:
            raise ValueError("List display name must be 255 characters or less")
        
        # Validate template if provided
        valid_templates = [
            "genericList",
            "documentLibrary",
            "survey",
            "links",
            "announcements",
            "contacts",
            "events",
            "tasks",
            "discussionBoard",
            "pictureLibrary"
        ]
        
        if request.template and request.template not in valid_templates:
            logger.warning("Unknown list template: %s , using genericList",request.template)
            request.template = "genericList"

    def validate_list_update_request(self, request: ListUpdateRequest) -> None:
        """
        Validate list update request.
        
        Args:
            request: List update request
            
        Raises:
            ValueError: If validation fails
        """
        if request.display_name is not None:
            if not request.display_name.strip():
                raise ValueError("List display name cannot be empty")
            if len(request.display_name) > 255:
                raise ValueError("List display name must be 255 characters or less")

    async def get_lists(
        self,
        site_id: str,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> ListListResponse:
        """
        Get all lists for a site.
        
        Args:
            site_id: SharePoint site ID
            top: Maximum number of items to return
            skip: Number of items to skip
            
        Returns:
            ListListResponse with all lists
        """
        if not site_id:
            raise ValueError("Site ID is required")
        
        # Validate pagination parameters
        if top is not None and top < 1:
            raise ValueError("Top must be greater than 0")
        if skip is not None and skip < 0:
            raise ValueError("Skip must be greater than or equal to 0")
        return await self.list_repository.get_lists(site_id, top=top, skip=skip)

    async def get_list_by_id(self, site_id: str, list_id: str) -> ListResponse:
        """
        Get a list by ID.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            
        Returns:
            ListResponse with list details
        """
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")
        
        return await self.list_repository.get_list_by_id(site_id, list_id)

    async def create_list(
        self,
        site_id: str,
        request: ListCreateRequest
    ) -> ListResponse:
        """
        Create a new list.
        
        Args:
            site_id: SharePoint site ID
            request: List creation request
            
        Returns:
            ListResponse with created list details
        """
        if not site_id:
            raise ValueError("Site ID is required")
        
        self.validate_list_create_request(request)
        
        return await self.list_repository.create_list(
            site_id=site_id,
            display_name=request.display_name,
            description=request.description,
            template=request.template,
            columns=request.columns
        )

    async def update_list(
        self,
        site_id: str,
        list_id: str,
        request: ListUpdateRequest
    ) -> ListResponse:
        """
        Update a list.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            request: List update request
            
        Returns:
            ListResponse with updated list details
        """
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")
        
        self.validate_list_update_request(request)
        
        return await self.list_repository.update_list(
            site_id=site_id,
            list_id=list_id,
            display_name=request.display_name,
            description=request.description
        )

    async def delete_list(self, site_id: str, list_id: str) -> None:
        """
        Delete a list.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
        """
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")
        
        await self.list_repository.delete_list(site_id, list_id)

    async def get_list_columns(self, site_id: str, list_id: str) -> List[ListColumnResponse]:
        """
        Get columns for a list.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            
        Returns:
            List of ListColumnResponse
        """
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")
        
        return await self.list_repository.get_list_columns(site_id, list_id)

    async def get_list_content_types(self, site_id: str, list_id: str) -> List[ListContentTypeResponse]:
        """
        Get content types for a list.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            
        Returns:
            List of ListContentTypeResponse
        """
        if not site_id:
            raise ValueError("Site ID is required")
        if not list_id:
            raise ValueError("List ID is required")
        
        return await self.list_repository.get_list_content_types(site_id, list_id)

