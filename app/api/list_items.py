"""
API routes for SharePoint List Items.

Handles HTTP requests for list item operations.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.deps import get_sharepoint_list_item_manager
from app.managers.sharepoint_list_item_manager import SharePointListItemManager
from app.data.list_item import (
    ListItemResponse,
    ListItemListResponse,
    ListItemCreateRequest,
    ListItemUpdateRequest,
    AttachmentListResponse,
    ListItemVersionListResponse
)

router = APIRouter(prefix="/sites/{site_id}/lists/{list_id}/items", tags=["List Items"])


@router.get("", response_model=ListItemListResponse)
async def get_list_items(
    site_id: str,
    list_id: str,
    top: Optional[int] = Query(None, description="Maximum number of items to return"),
    skip: Optional[int] = Query(None, description="Number of items to skip"),
    filter_query: Optional[str] = Query(None, alias="$filter", description="OData filter query"),
    manager: SharePointListItemManager = Depends(get_sharepoint_list_item_manager)
):
    """
    Get all items in a list.
    
    - **site_id**: SharePoint site ID
    - **list_id**: List ID
    - **top**: Maximum number of items to return (optional)
    - **skip**: Number of items to skip (optional)
    - **$filter**: OData filter query (optional)
    """
    try:
        return await manager.get_list_items(
            site_id=site_id,
            list_id=list_id,
            top=top,
            skip=skip,
            filter_query=filter_query
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@router.get("/{item_id}", response_model=ListItemResponse)
async def get_list_item_by_id(
    site_id: str,
    list_id: str,
    item_id: str,
    manager: SharePointListItemManager = Depends(get_sharepoint_list_item_manager)
):
    """
    Get a list item by ID.
    
    - **site_id**: SharePoint site ID
    - **list_id**: List ID
    - **item_id**: Item ID
    """
    try:
        return await manager.get_list_item_by_id(site_id, list_id, item_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Item not found: {str(e)}") from e


@router.post("", response_model=ListItemResponse, status_code=201)
async def create_list_item(
    site_id: str,
    list_id: str,
    request: ListItemCreateRequest,
    manager: SharePointListItemManager = Depends(get_sharepoint_list_item_manager)
):
    """
    Create a new list item.
    
    - **site_id**: SharePoint site ID
    - **list_id**: List ID
    - **request**: List item creation request (fields)
    """
    try:
        return await manager.create_list_item(site_id, list_id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create item: {str(e)}") from e


@router.patch("/{item_id}", response_model=ListItemResponse)
async def update_list_item(
    site_id: str,
    list_id: str,
    item_id: str,
    request: ListItemUpdateRequest,
    manager: SharePointListItemManager = Depends(get_sharepoint_list_item_manager)
):
    """
    Update a list item.
    
    - **site_id**: SharePoint site ID
    - **list_id**: List ID
    - **item_id**: Item ID
    - **request**: List item update request (fields)
    """
    try:
        return await manager.update_list_item(site_id, list_id, item_id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update item: {str(e)}") from e


@router.delete("/{item_id}", status_code=204)
async def delete_list_item(
    site_id: str,
    list_id: str,
    item_id: str,
    manager: SharePointListItemManager = Depends(get_sharepoint_list_item_manager)
):
    """
    Delete a list item.
    
    - **site_id**: SharePoint site ID
    - **list_id**: List ID
    - **item_id**: Item ID
    """
    try:
        await manager.delete_list_item(site_id, list_id, item_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete item: {str(e)}") from e


@router.get("/{item_id}/attachments", response_model=AttachmentListResponse)
async def get_item_attachments(
    site_id: str,
    list_id: str,
    item_id: str,
    manager: SharePointListItemManager = Depends(get_sharepoint_list_item_manager)
):
    """
    Get attachments for a list item.
    
    - **site_id**: SharePoint site ID
    - **list_id**: List ID
    - **item_id**: Item ID
    """
    try:
        return await manager.get_item_attachments(site_id, list_id, item_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get attachments: {str(e)}") from e


@router.get("/{item_id}/versions", response_model=ListItemVersionListResponse)
async def get_item_versions(
    site_id: str,
    list_id: str,
    item_id: str,
    manager: SharePointListItemManager = Depends(get_sharepoint_list_item_manager)
):
    """
    Get version history for a list item.
    
    - **site_id**: SharePoint site ID
    - **list_id**: List ID
    - **item_id**: Item ID
    """
    try:
        return await manager.get_item_versions(site_id, list_id, item_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get versions: {str(e)}") from e
