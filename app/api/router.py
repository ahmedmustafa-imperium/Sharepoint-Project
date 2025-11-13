"""
Main router that aggregates all API routes.
"""
from fastapi import APIRouter
from app.api import lists,sites,list_items,auth,drives


# Create main API router
api_router = APIRouter()
# Include sub-routers
api_router.include_router(lists.router)
api_router.include_router(sites.router)
api_router.include_router(auth.router)
api_router.include_router(list_items.router)
api_router.include_router(drives.router)
