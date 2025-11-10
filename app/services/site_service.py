from typing import  Optional
import logging
from app.repositories.site_repository import SiteRepository
from app.data.site import SiteResponse, SiteListResponse
from app.utils.mapper import map_site_json


logger = logging.getLogger(__name__)

class SiteService:
    def __init__(self, repository: SiteRepository):
        self.repository = repository()

    async def list_sites(self, top: int = 50) -> SiteListResponse:
        raw_sites = await self.repository.list_sites(top=top)
        sites = []
        for raw in raw_sites:
            try:
                site = map_site_json(raw)
                sites.append(site)
            except Exception as exc:
                logger.exception("Failed to map site JSON: %s", exc)
        return SiteListResponse(sites=sites, total=len(sites))

    async def get_site(self, site_id: str) -> Optional[SiteResponse]:
        raw = await self.repository.get_site_by_id(site_id)
        if not raw:
            return None
        return map_site_json(raw)

    async def search_sites(self, query: str) -> SiteListResponse:
        if not query or query.strip() == "":
            return await self.list_sites()
        raw_sites = await self.repository.search_sites(q=query)
        sites = []
        for raw in raw_sites:
            try:
                sites.append(map_site_json(raw))
            except Exception:
                logger.exception("Failed to map site JSON during search")
        return SiteListResponse(sites=sites, total=len(sites))
