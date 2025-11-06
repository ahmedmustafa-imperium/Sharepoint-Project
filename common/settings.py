<<<<<<< Updated upstream
=======
from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
class Settings(BaseSettings):
    TENANT_ID: str = Field(..., env="TENANT_ID")
    CLIENT_ID: str = Field(..., env="CLIENT_ID")
    CLIENT_SECRET: str = Field(..., env="CLIENT_SECRET")
    GRAPH_BASE: str = "https://graph.microsoft.com/v1.0"
    SHAREPOINT_HOSTNAME: str = Field(..., env="SHAREPOINT_HOSTNAME")
    SITE_PATH: str = Field(..., env="SITE_PATH")
    FILE_NAME: str = Field("", env="FILE_NAME")
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
>>>>>>> Stashed changes
