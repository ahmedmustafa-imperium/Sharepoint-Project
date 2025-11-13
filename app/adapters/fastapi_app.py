"""
This module initializes and configures the FastAPI application for the SharePoint project.

It sets up:
- Application-level logging using the custom logging configuration.
- The main FastAPI app instance with metadata (title, description, version).
- API routing through the central router (`api_router`), which includes all endpoint modules.
"""

import logging
from fastapi import FastAPI
from app.core.logging import configure_logging
from app.api.router import api_router

configure_logging()
logger = logging.getLogger(__name__)
logger.propagate = True

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

    sharepoint_app.include_router(api_router, prefix="/api/v1")

    @sharepoint_app.get("/")
    async def root():
        return {
            "message": "SharePoint Project API",
            "version": "1.0.0",
        }

    return sharepoint_app


app = create_app()
