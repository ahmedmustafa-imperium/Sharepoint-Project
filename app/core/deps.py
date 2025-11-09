"""
dependency_providers.py

This module provides dependency functions for FastAPI endpoints.
"""
from app.managers.sharepoint_auth_manager import SharePointAuthManager

# Provide the manager as a dependency
def get_sharepoint_auth_manager() -> SharePointAuthManager:
    """
    FastAPI dependency provider for SharePointAuthManager.

    Returns:
        SharePointAuthManager: A new instance of SharePointAuthManager.
    """
    return SharePointAuthManager()
