"""
Main router that aggregates all API routes.
"""
from fastapi import APIRouter
from app.api.sites import router
 
# Create main API router
api_router = APIRouter()
# Include sub-routers
api_router.include_router(router)