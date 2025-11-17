## SharePoint Project API

This service exposes a consistent FastAPI interface for working with Microsoft SharePoint through Microsoft Graph. It wraps authentication, sites, lists, list item operations, and drive/file management behind clean REST routes so other services can integrate without learning the Graph surface area.

### What’s Included
- Centralized OAuth token acquisition and caching.
- Site discovery, lookup, and search helpers.
- Rich list management with CRUD, column, and content-type metadata.
- List item CRUD endpoints plus attachments and version history.
- Drive and file utilities to browse, upload, and download SharePoint content.

### Getting Started
1. Install dependencies with PDM:
   ```
   pdm install
   ```
2. Configure your Microsoft Graph credentials via the environment entries referenced in `app/core/config.py`.
3. Start the API (defaults to uvicorn) with:
   ```
   pdm start
   ```

### Feature Highlights
- **Authentication**: Issued tokens are cached to minimize round trips to Microsoft identity endpoints, ensuring every manager/service automatically has the bearer token it needs.
- **Sites**: Quickly list every accessible site, fetch by ID for details, or run search queries for friendly names.
- **Lists**: Build, inspect, update, or remove lists; introspect schema (columns, content types) for downstream validation.
- **List Items**: Standard CRUD plus advanced helpers to pull attachment payloads or audit version history.
- **Drives & Files**: Navigate site drives, inspect folders, upload new documents, or pull full directory trees locally.

### HTTP Routes

| Area | Method | Path | Description |
| --- | --- | --- | --- |
| Auth | GET | `/auth/token` | Return the current SharePoint access token. |
| Sites | GET | `/sites/list_sites` | List every SharePoint site the app can access. |
| Sites | GET | `/sites/site_by_id/{site_id}` | Fetch metadata for a single site. |
| Sites | GET | `/sites/search_sites/{query}` | Search sites by display name fragment. |
| Lists | GET | `/sites/{site_id}/lists` | Retrieve lists for a site with optional `top`/`skip`. |
| Lists | GET | `/sites/{site_id}/lists/{list_id}` | Fetch a list by ID. |
| Lists | POST | `/sites/{site_id}/lists` | Create a list from the payload schema. |
| Lists | PATCH | `/sites/{site_id}/lists/{list_id}` | Update list properties. |
| Lists | DELETE | `/sites/{site_id}/lists/{list_id}` | Remove a list. |
| Lists | GET | `/sites/{site_id}/lists/{list_id}/columns` | Inspect list columns. |
| Lists | GET | `/sites/{site_id}/lists/{list_id}/content-types` | Inspect list content types. |
| List Items | GET | `/sites/{site_id}/lists/{list_id}/items` | List items with optional `$filter`, `top`, `skip`. |
| List Items | GET | `/sites/{site_id}/lists/{list_id}/items/{item_id}` | Fetch a specific item. |
| List Items | POST | `/sites/{site_id}/lists/{list_id}/items` | Create a list item. |
| List Items | PATCH | `/sites/{site_id}/lists/{list_id}/items/{item_id}` | Update a list item. |
| List Items | DELETE | `/sites/{site_id}/lists/{list_id}/items/{item_id}` | Delete a list item. |
| List Items | GET | `/sites/{site_id}/lists/{list_id}/items/{item_id}/attachments` | Return item attachments. |
| List Items | GET | `/sites/{site_id}/lists/{list_id}/items/{item_id}/versions` | Return version history. |
| Drives | GET | `/drives/list_drives?site_id={site_id}` | List drives/libraries within a site. |
| Drives | GET | `/drives/drives/{drive_id}/items?folder_id=...` | List drive or folder contents. |
| Drives | POST | `/drives/drives/{drive_id}/upload` | Upload a file (optionally supply `folder_id`). |
| Drives | GET | `/drives/drives/{drive_id}/download/{file_id}` | Download a single file. |
| Drives | GET | `/drives/drives/{drive_id}/download?parent_id=...` | Download all content under a folder recursively. |

> For deeper module documentation or type reference material, see the `docs/` directory when available or inspect the `app/data` models for request/response schemas.
