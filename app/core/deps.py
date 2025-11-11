"""
dependency_providers.py

This module provides dependency functions for FastAPI endpoints.
"""
from fastapi import Depends
from app.managers.sharepoint_auth_manager import SharePointAuthManager
from app.managers.sharepoint_site_manager import SharePointSiteManager
from app.utils.graph_client import GraphClient
from app.repositories.list_repository import ListRepository
from app.repositories.list_item_repository import ListItemRepository
from app.services.list_service import ListService
from app.services.list_item_service import ListItemService
from app.managers.sharepoint_list_manager import SharePointListManager
from app.managers.sharepoint_list_item_manager import SharePointListItemManager

from app.utils.token_cache import TokenCache

# Shared token cache instance (singleton pattern)
_token_cache = TokenCache()

# Shared auth manager instance (uses shared token cache)
_auth_manager = SharePointAuthManager(token_cache=_token_cache)


def get_sharepoint_auth_manager() -> SharePointAuthManager:
    """
    FastAPI dependency provider for SharePointAuthManager.

    Returns:
        SharePointAuthManager: A shared instance of SharePointAuthManager.
    """
    return _auth_manager


def get_graph_client() -> GraphClient:
    """
    FastAPI dependency provider for GraphClient.
    
    Creates an HTTP client with token getter from auth manager.

    Returns:
        GraphClient: A new instance of GraphClient.
    """
    async def token_getter() -> str:
        """Token getter function for HTTP client."""
        return await _auth_manager.get_access_token()
    
    return GraphClient(token_getter=token_getter)


def get_list_repository(graph_client: GraphClient = Depends(get_graph_client)) -> ListRepository:
    """
    FastAPI dependency provider for ListRepository.

    Returns:
        ListRepository: A new instance of ListRepository.
    """
    return ListRepository(graph_client=graph_client)



def get_list_service(list_repository: ListRepository=Depends(get_list_repository)) -> ListService:
    """
    FastAPI dependency provider for ListService.

    Returns:
        ListService: A new instance of ListService.
    """
    return ListService(list_repository=list_repository)



def get_sharepoint_list_manager(list_service : ListService = Depends(get_list_service)) -> SharePointListManager:
    """
    FastAPI dependency provider for SharePointListManager.

    Returns:
        SharePointListManager: A new instance of SharePointListManager.
    """
    return SharePointListManager(list_service=list_service)


def get_sharepoint_site_manager() -> SharePointSiteManager:
    return SharePointSiteManager()

def get_list_item_repository(graph_client: GraphClient = Depends(get_graph_client)) -> ListItemRepository:
    """
    FastAPI dependency provider for ListItemRepository.

    Returns:
        ListItemRepository: A new instance of ListItemRepository.
    """
    return ListItemRepository(graph_client=graph_client)

def get_list_item_service(list_item_repository: ListItemRepository = Depends( get_list_item_repository)) -> ListItemService:
    """
    FastAPI dependency provider for ListItemService.

    Returns:
        ListItemService: A new instance of ListItemService.
    """
    return ListItemService(list_item_repository=list_item_repository)

def get_sharepoint_list_item_manager(list_item_service: ListItemService = Depends(get_list_item_service)) -> SharePointListItemManager:
    """
    FastAPI dependency provider for SharePointListItemManager.

    Returns:
        SharePointListItemManager: A new instance of SharePointListItemManager.
    """
    return SharePointListItemManager(list_item_service=list_item_service)
