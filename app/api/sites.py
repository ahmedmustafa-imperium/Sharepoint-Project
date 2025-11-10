"""
API routes for SharePoint sites.
 
Handles HTTP requests for site operations.
"""
from app.core.deps import SharePointSiteManager
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

router = APIRouter(prefix="/sites", tags=["Sites"])


@router.get("/list_sites")
async def get_list_sites(manager = Depends(SharePointSiteManager)):
    list_sites = await manager.list_sites()
    return list_sites

@router.get("/site_by_id/{site_id}")
async def site_by_id(site_id: str,manager = Depends(SharePointSiteManager)):
    site = await manager.get_site(site_id)
    return site

@router.get("/search_sites/{query}")
async def site_by_query(query: str,manager = Depends(SharePointSiteManager)):
    site = await manager.search_sites(query)
    return site
