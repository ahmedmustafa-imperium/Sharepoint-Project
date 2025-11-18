"""
dependency_providers.py

This module provides dependency functions for FastAPI endpoints.
"""
from app.managers.sharepoint_auth_manager import SharePointAuthManager
from app.utils.graph_client import GraphClient
from app.utils.token_cache import TokenCache
from app.managers.sharepoint_drive_manager import SharePointDriveManager
from app.repositories.drive_repository import DriveRepository
from app.services.drive_service import DriveService

# Additional drive dependencies

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

    return GraphClient(token_getter)

def get_drive_repository() -> DriveRepository:
    """
    FastAPI dependency provider for DriveRepository.
    """
    graph_client: GraphClient =get_graph_client()
    return DriveRepository(graph_client=graph_client)


def get_drive_service() -> DriveService:
    """
    FastAPI dependency provider for DriveService.
    """
    drive_repository: DriveRepository = get_drive_repository()
    return DriveService(drive_repository=drive_repository)


def get_sharepoint_drive_manager() -> SharePointDriveManager:
    """
    FastAPI dependency provider for SharePointDriveManager.
    """
    drive_service: DriveService =get_drive_service()
    return SharePointDriveManager(drive_service=drive_service)
