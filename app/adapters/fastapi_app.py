import logging
from fastapi import FastAPI, Depends
from app.core.deps import get_sharepoint_auth_manager  
from app.core.auth import get_current_user
from app.core.logging import configure_logging


configure_logging()
logger = logging.getLogger(__name__)
logger.propagate = True 
logger.debug("hello")
def create_app() -> FastAPI:
    app = FastAPI(title="SharePoint Project")

    

    @app.get("/token")
    async def get_token(manager = Depends(get_sharepoint_auth_manager)):
        token = await manager.get_access_token()
        return {"access_token": token}

    # Example protected route that validates incoming JWT (user context)
    # @app.get("/me")
    # async def me(user = Depends(get_current_user)):
    #     # `user` is JWT payload dict
    #     return {"user": user}

    return app


app = create_app()
