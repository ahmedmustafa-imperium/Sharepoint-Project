from auth.msal_token import get_token
from services.retrieve.sharepoint import get_drive_id, get_site_id, download_file_from_root
from common.settings import get_settings
site_id=get_site_id()
app=get_drive_id(site_id)
print(app)
_settings = get_settings()
if _settings.FILE_NAME:
    saved = download_file_from_root(site_id=site_id, file_path=_settings.FILE_NAME)
    print(f"Downloaded to: {saved}")
