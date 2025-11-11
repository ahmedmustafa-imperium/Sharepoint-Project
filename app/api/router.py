"""
Main router that aggregates all API routes.
"""
from fastapi import APIRouter
from app.api import lists,sites,list_items
#from app.api import list_items

# Create main API router
api_router = APIRouter()
# Include sub-routers
api_router.include_router(lists.router)
api_router.include_router(sites.router)
api_router.include_router(list_items.router)