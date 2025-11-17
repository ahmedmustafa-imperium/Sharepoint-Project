"""
This module initializes and configures the FastAPI application for the SharePoint project.

It sets up:
- Application-level logging using the custom logging configuration.
- The main FastAPI app instance with metadata (title, description, version).
- API routing through the central router (`api_router`), which includes all endpoint modules.
"""

from fastapi import APIRouter, FastAPI, Request
from app.api import lists,sites,list_items,auth,drives
from app.core.filter import generate_request_id, set_request_id
from app.core.logging import get_logger, setup_logger

setup_logger(name="sharepoint_app")
app_logger = get_logger(__name__)

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.

    This function sets up the application metadata, registers all API routes
    """
    sharepoint_app = FastAPI(
        title="SharePoint Project",
        description="SharePoint integration API for managing sites, lists, and list items",
        version="1.0.0"
    )

    @sharepoint_app.middleware("http")
    async def add_request_id(request: Request, call_next):
        """
        Attach a correlation/request ID to each incoming request for logging.
        """
        request_id = request.headers.get("X-Request-ID") or generate_request_id()
        set_request_id(request_id)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

# Create main API router
    api_router = APIRouter()
    # Include sub-routers
    api_router.include_router(lists.router)
    api_router.include_router(sites.router)
    api_router.include_router(auth.router)
    api_router.include_router(list_items.router)
    api_router.include_router(drives.router)
    sharepoint_app.include_router(api_router, prefix="/api/v1")
    @sharepoint_app.get("/")
    async def root():
        app_logger.debug("Root endpoint accessed")
        return {
            "message": "SharePoint Project API",
            "version": "1.0.0",
        }

    return sharepoint_app


app = create_app()
