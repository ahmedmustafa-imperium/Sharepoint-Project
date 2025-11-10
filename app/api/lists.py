"""
API routes for SharePoint Lists.

Handles HTTP requests for list operations.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.core.deps import get_sharepoint_list_manager
from app.managers.sharepoint_list_manager import SharePointListManager
from app.data.list import (
    ListResponse,
    ListListResponse,
    ListCreateRequest,
    ListUpdateRequest,
    ListColumnResponse,
    ListContentTypeResponse
)

router = APIRouter(prefix="/sites/{site_id}/lists", tags=["Lists"])


@router.get("", response_model=ListListResponse)
async def get_lists(
    site_id: str,
    top: Optional[int] = Query(None, description="Maximum number of items to return"),
    skip: Optional[int] = Query(None, description="Number of items to skip"),
    manager: SharePointListManager = Depends(get_sharepoint_list_manager)
):
    """
    Get all lists for a SharePoint site.
    
    - **site_id**: SharePoint site ID
    - **top**: Maximum number of lists to return (optional)
    - **skip**: Number of lists to skip (optional)
    """
    try:
        return await manager.get_lists(site_id, top=top, skip=skip)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@router.get("/{list_id}", response_model=ListResponse)
async def get_list_by_id(
    site_id: str,
    list_id: str,
    manager: SharePointListManager = Depends(get_sharepoint_list_manager)
):
    """
    Get a list by ID.
    
    - **site_id**: SharePoint site ID
    - **list_id**: List ID
    """
    try:
        return await manager.get_list_by_id(site_id, list_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"List not found: {str(e)}") from e


@router.post("", response_model=ListResponse, status_code=201)
async def create_list(
    site_id: str,
    request: ListCreateRequest,
    manager: SharePointListManager = Depends(get_sharepoint_list_manager)
):
    """
    Create a new list.
    
    - **site_id**: SharePoint site ID
    - **request**: List creation request (display_name, description, template, etc.)
    """
    try:
        return await manager.create_list(site_id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create list: {str(e)}") from e


@router.patch("/{list_id}", response_model=ListResponse)
async def update_list(
    site_id: str,
    list_id: str,
    request: ListUpdateRequest,
    manager: SharePointListManager = Depends(get_sharepoint_list_manager)
):
    """
    Update a list.
    
    - **site_id**: SharePoint site ID
    - **list_id**: List ID
    - **request**: List update request (display_name, description)
    """
    try:
        return await manager.update_list(site_id, list_id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update list: {str(e)}") from e


@router.delete("/{list_id}", status_code=204)
async def delete_list(
    site_id: str,
    list_id: str,
    manager: SharePointListManager = Depends(get_sharepoint_list_manager)
):
    """
    Delete a list.
    
    - **site_id**: SharePoint site ID
    - **list_id**: List ID
    """
    try:
        await manager.delete_list(site_id, list_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete list: {str(e)}") from e


@router.get("/{list_id}/columns", response_model=list[ListColumnResponse])
async def get_list_columns(
    site_id: str,
    list_id: str,
    manager: SharePointListManager = Depends(get_sharepoint_list_manager)
):
    """
    Get columns for a list.
    
    - **site_id**: SharePoint site ID
    - **list_id**: List ID
    """
    try:
        return await manager.get_list_columns(site_id, list_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get columns: {str(e)}") from e


@router.get("/{list_id}/content-types", response_model=list[ListContentTypeResponse])
async def get_list_content_types(
    site_id: str,
    list_id: str,
    manager: SharePointListManager = Depends(get_sharepoint_list_manager)
):
    """
    Get content types for a list.
    
    - **site_id**: SharePoint site ID
    - **list_id**: List ID
    """
    try:
        return await manager.get_list_content_types(site_id, list_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get content types: {str(e)}") from e

