import azure.functions as func
from azure_routes.drive import register_drive_routes

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Register all route groups
register_drive_routes(app)
