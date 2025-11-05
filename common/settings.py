from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    # Azure AD settings
    AZURE_CLIENT_ID: str = Field(..., env="CLIENT_ID")
    AZURE_CLIENT_SECRET: str = Field(..., env="CLIENT_SECRET")
    AZURE_TENANT_ID: str = Field(..., env="TENANT_ID")
    AZURE_AUTHORITY: str = Field(..., env="AZURE_AUTHORITY")
    AZURE_AUTHORITY = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    AZURE_SCOPE = ["https://graph.microsoft.com/.default"]
    GRAPH_BASE_URL = "https://graph.mi"
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


from dotenv import dotenv_values
 
config = dotenv_values(".env")
 
CLIENT_ID = config["CLIENT_ID"]
CLIENT_SECRET = config["CLIENT_SECRET"]
TENANT_ID = config["TENANT_ID"]
 