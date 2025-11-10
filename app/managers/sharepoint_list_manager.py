"""
Manager for SharePoint Lists orchestration.

Coordinates list operations between API layer and services.
Handles caching, batch operations, and complex workflows.
"""
import logging
from typing import Optional, List
from app.services.list_service import ListService
from app.data.list import (
    ListResponse,
    ListListResponse,
    ListCreateRequest,
    ListUpdateRequest,
    ListColumnResponse,
    ListContentTypeResponse
)

logger = logging.getLogger(__name__)


class SharePointListManager:
    """
    Orchestrator for SharePoint list operations.
    
    Coordinates between FastAPI endpoints and ListService.
    Handles caching, batch operations, and complex workflows.
    """
    
    def __init__(self, list_service: ListService):
        """
        Initialize SharePoint list manager.
        
        Args:
            list_service: Service for list business logic
        """
        self.list_service = list_service

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
        logger.info("Getting lists for site %s",site_id)
        return await self.list_service.get_lists(site_id, top=top, skip=skip)

    async def get_list_by_id(self, site_id: str, list_id: str) -> ListResponse:
        """
        Get a list by ID.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            
        Returns:
            ListResponse with list details
        """
        logger.info("Getting list %s from site %s", list_id, site_id)

        return await self.list_service.get_list_by_id(site_id, list_id)

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
        logger.info("Creating list '%s' in site %s", request.display_name, site_id)
        return await self.list_service.create_list(site_id, request)

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
        logger.info("Updating list %s in site %s", list_id, site_id)
        return await self.list_service.update_list(site_id, list_id, request)

    async def delete_list(self, site_id: str, list_id: str) -> None:
        """
        Delete a list.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
        """
        logger.info("Deleting list %s from site %s", list_id, site_id)
        await self.list_service.delete_list(site_id, list_id)

    async def get_list_columns(self, site_id: str, list_id: str) -> List[ListColumnResponse]:
        """
        Get columns for a list.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            
        Returns:
            List of ListColumnResponse
        """
        logger.info("Getting columns for list %s in site %s", list_id, site_id)
        return await self.list_service.get_list_columns(site_id, list_id)

    async def get_list_content_types(self, site_id: str, list_id: str) -> List[ListContentTypeResponse]:
        """
        Get content types for a list.
        
        Args:
            site_id: SharePoint site ID
            list_id: List ID
            
        Returns:
            List of ListContentTypeResponse
        """
        logger.info("Getting content types for list %s in site %s", list_id, site_id)
        return await self.list_service.get_list_content_types(site_id, list_id)

