"""
API routes for access token.
 """

from fastapi import APIRouter, Depends
from app.core.deps import get_sharepoint_auth_manager

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/token")
async def get_token(manager = Depends(get_sharepoint_auth_manager)):
    """
    Retrieve an access token for SharePoint API authentication.
    """
    token = await manager.get_access_token()
    return {"access_token": token}