"""
dependency_providers.py

This module provides dependency functions for FastAPI endpoints.
"""
from app.managers.sharepoint_auth_manager import SharePointAuthManager
from app.managers.sharepoint_site_manager import SharePointSiteManager


# Provide the manager as a dependency
def get_sharepoint_auth_manager() -> SharePointAuthManager:
    """
    FastAPI dependency provider for SharePointAuthManager.

    Returns:
        SharePointAuthManager: A new instance of SharePointAuthManager.
    """
    return SharePointAuthManager()


def get_sharepoint_site_manager() -> SharePointSiteManager:
    return SharePointSiteManager()
