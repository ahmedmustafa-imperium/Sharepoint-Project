import logging
from fastapi import FastAPI, Depends
from app.core.deps import get_sharepoint_auth_manager  
from app.core.logging import configure_logging
from app.api.router import api_router


configure_logging()
logger = logging.getLogger(__name__)
logger.propagate = True 
logger.debug("hello")

def create_app() -> FastAPI:
    sharepoint_app = FastAPI(
        title="SharePoint Project",
        description="SharePoint integration API for managing sites, lists, and list items",
        version="1.0.0"
    )

    sharepoint_app.include_router(api_router, prefix="/api/v1")

    @sharepoint_app.get("/token")
    async def get_token(manager = Depends(get_sharepoint_auth_manager)):
        token = await manager.get_access_token()
        return {"access_token": token}

    @sharepoint_app.get("/")
    async def root():
        return {
            "message": "SharePoint Project API",
            "version": "1.0.0",
        }

    return sharepoint_app


app = create_app()

