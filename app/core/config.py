"""
Configuration module for application runtime settings.

Loads environment variables such as Azure client credentials,
logging configuration, and Redis settings for token caching.
"""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, AnyHttpUrl

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables using Pydantic.

    This object centralizes all configuration such as Azure OAuth parameters
    and application runtime settings.
    """
    azure_tenant_id: str
    azure_client_id: str
    azure_client_secret: str
    AZURE_SCOPE: str = Field("https://graph.microsoft.com/.default", env="AZURE_SCOPE")

    # base URL for Microsoft Graph
    GRAPH_BASE_URL: AnyHttpUrl = Field("https://graph.microsoft.com/v1.0", env="GRAPH_BASE_URL")
    DEFAULT_PAGE_SIZE: int = Field(50, env="DEFAULT_PAGE_SIZE")

    # For JWT validation (incoming tokens)
    AZURE_OPENID_CONFIG_URL: Optional[AnyHttpUrl] = Field(
        None, env="AZURE_OPENID_CONFIG_URL")
    TOKEN_CACHE_REDIS_URL: Optional[str] = Field(None, env="TOKEN_CACHE_REDIS_URL")
    TOKEN_REFRESH_BUFFER_SECONDS: int = Field(60, env="TOKEN_REFRESH_BUFFER_SECONDS")

    # App settings
    ENV: str = Field("development", env="ENV")
    LOG_LEVEL: str = Field("DEBUG", env="LOG_LEVEL")

    # Microsoft Graph API settings
    GRAPH_BASE: str = Field("https://graph.microsoft.com/v1.0", env="GRAPH_BASE")

    class Config:
        """Pydantic BaseSettings configuration."""
        env_file = ".env"
        case_sensitive = False

settings = Settings()
