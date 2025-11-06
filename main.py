
from services.download.download_file import download_file_from_root
from common.settings import get_settings
_settings = get_settings()
if _settings.FILE_NAME:
    saved = download_file_from_root(file_path=_settings.FILE_NAME)
    print(f"Downloaded to: {saved}")
