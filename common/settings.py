"""
settings.py

This module provides application configuration using environment variables.
It loads SharePoint + Azure AD application settings using Pydantic BaseSettings.
"""

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings model for environment configuration.

    This class loads values from environment variables using pydantic.
    These settings are used for authentication and building SharePoint/Graph URLs.
    """

    TENANT_ID: str = Field(..., env="TENANT_ID")
    CLIENT_ID: str = Field(..., env="CLIENT_ID")
    CLIENT_SECRET: str = Field(..., env="CLIENT_SECRET")

    GRAPH_BASE: str = "https://graph.microsoft.com/v1.0"

    SHAREPOINT_HOSTNAME: str = Field(..., env="SHAREPOINT_HOSTNAME")
    SITE_PATH: str = Field(..., env="SITE_PATH")
    FILE_NAME: str = Field("", env="FILE_NAME")

    class Config:
        """Pydantic configuration for environment variable loading."""
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of Settings.

    This ensures the environment variables are loaded only once in the app
    and improves performance by avoiding repeated parsing of the .env file.

    Returns:
        Settings: Application configuration instance.
    """
    return Settings()