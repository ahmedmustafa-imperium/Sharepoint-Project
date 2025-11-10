import logging
from fastapi import FastAPI, Depends
from app.core.deps import get_sharepoint_auth_manager  
from app.core.auth import get_current_user
from app.core.logging import configure_logging
from app.api.router import api_router


configure_logging()
logger = logging.getLogger(__name__)
logger.propagate = True 

def create_app() -> FastAPI:
    app = FastAPI(title="SharePoint Project")

    @app.get("/token")
    async def get_token(manager = Depends(get_sharepoint_auth_manager)):
        token = await manager.get_access_token()
        return {"access_token": token}
    app.include_router(api_router, prefix="/api/v1")
 



    return app


app = create_app()
