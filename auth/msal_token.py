<<<<<<< Updated upstream
=======
from common.settings import get_settings
import msal

_settings = get_settings()

def get_token() -> str:
    app = msal.ConfidentialClientApplication(
        _settings.CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{_settings.TENANT_ID}",
        client_credential=_settings.CLIENT_SECRET
    )
    scope = ["https://graph.microsoft.com/.default"]
    result = app.acquire_token_silent(scope, account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=scope)
    if "access_token" not in result:
        raise Exception(f"Could not obtain access token: {result}")
    return result["access_token"]
>>>>>>> Stashed changes
