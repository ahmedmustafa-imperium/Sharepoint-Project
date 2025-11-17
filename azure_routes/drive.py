"""
Module for registering drive routes.
"""
import azure.functions as func
from app.core.deps import get_sharepoint_drive_manager
from app.managers.sharepoint_drive_manager import SharePointDriveManager
from app.data.drive import FileUploadRequest


def register_drive_routes(app: func.FunctionApp):
    """
    Register SharePoint Drive routes for Azure Functions.
    """

    # ---------------------------------------------------------
    # LIST DRIVES
    # ---------------------------------------------------------
    @app.function_name("list_drives")
    @app.route(route="drives/list_drives", methods=["GET"])
    async def list_drives(req: func.HttpRequest) -> func.HttpResponse:
        site_id = req.params.get("site_id")
        if not site_id:
            return func.HttpResponse("Missing site_id", status_code=400)

        manager: SharePointDriveManager = get_sharepoint_drive_manager()
        data = await manager.list_drives(site_id)
        return func.HttpResponse(
            body=data.json(),
            mimetype="application/json"
        )

    # ---------------------------------------------------------
    # LIST ITEMS
    # ---------------------------------------------------------
    @app.function_name("list_items")
    @app.route(route="drives/{drive_id}/items", methods=["GET"])
    async def list_items(req: func.HttpRequest) -> func.HttpResponse:
        drive_id = req.route_params.get("drive_id")
        folder_id = req.params.get("folder_id")

        manager = get_sharepoint_drive_manager()
        data = await manager.list_items(drive_id, folder_id)
        return func.HttpResponse(
            body=data.json(),
            mimetype="application/json"
        )

    # ---------------------------------------------------------
    # UPLOAD FILE
    # ---------------------------------------------------------
    @app.function_name("upload_file")
    @app.route(route="drives/{drive_id}/upload", methods=["POST"])
    async def upload_file(req: func.HttpRequest) -> func.HttpResponse:
        drive_id = req.route_params.get("drive_id")
        folder_id = req.params.get("folder_id")

        manager = get_sharepoint_drive_manager()
        try:
            file_bytes = await req.get_body()
            file_name = req.headers.get("x-file-name")
            if not file_name:
                return func.HttpResponse("Missing x-file-name header", status_code=400)

            file_req = FileUploadRequest(
                file_name=file_name,
                content=file_bytes,
                folder_id=folder_id
            )

            data = await manager.upload_file(drive_id, file_req)
            return func.HttpResponse(data.json(), mimetype="application/json")

        except Exception as e:
            return func.HttpResponse(str(e), status_code=500)

    # ---------------------------------------------------------
    # DOWNLOAD SINGLE FILE
    # ---------------------------------------------------------
    @app.function_name("download_file")
    @app.route(route="drives/{drive_id}/download/{file_id}", methods=["GET"])
    async def download_file(req: func.HttpRequest) -> func.HttpResponse:
        drive_id = req.route_params.get("drive_id")
        file_id = req.route_params.get("file_id")

        manager = get_sharepoint_drive_manager()
        file_response = await manager.download_file(drive_id, file_id)

        if file_response.content:
            headers = {
                "Content-Disposition": f'attachment; filename="{file_response.file_name or "download"}"'
            }
            return func.HttpResponse(
                body=file_response.content,
                status_code=200,
                headers=headers,
                mimetype="application/octet-stream"
            )

        return func.HttpResponse(
            body=file_response.json(exclude={"content"}),
            mimetype="application/json"
        )

    # ---------------------------------------------------------
    # DOWNLOAD MULTIPLE FILES
    # ---------------------------------------------------------
    @app.function_name("download_files")
    @app.route(route="drives/{drive_id}/download", methods=["GET"])
    async def download_files(req: func.HttpRequest) -> func.HttpResponse:
        drive_id = req.route_params.get("drive_id")
        parent_id = req.params.get("parent_id", "root")

        manager = get_sharepoint_drive_manager()
        await manager.download_files(drive_id, parent_id)

        return func.HttpResponse(
            body='{"status": "completed"}',
            mimetype="application/json"
        )
