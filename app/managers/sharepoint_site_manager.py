
from typing import Optional
from app.data.site import SiteListResponse, SiteResponse
from app.services.site_service import SiteService
from app.repositories.site_repository import SiteRepository

class SharePointSiteManager:
    def __init__(self):
        self.site_service = SiteService(SiteRepository)

    async def list_sites(self, page_size: int = 50) -> SiteListResponse:
        # orchestration point for caching, audit, or combining other sources
        return await self.site_service.list_sites(top=page_size)

    async def get_site(self, site_id: str) -> Optional[SiteResponse]:
        return await self.site_service.get_site(site_id=site_id)

    async def search_sites(self, query: str) -> SiteListResponse:
        return await self.site_service.search_sites(query)
