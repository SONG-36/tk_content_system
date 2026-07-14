"""Internal mock result route excluded from public Action OpenAPI."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.dependencies import get_mock_result_service
from app.services.mock_results import MockResultService

router = APIRouter(tags=["internal"])


@router.get(
    "/_internal/mock-results/{token}",
    include_in_schema=False,
)
async def download_mock_result(
    token: str,
    result_service: MockResultService = Depends(get_mock_result_service),
) -> FileResponse:
    path, content_type = result_service.resolve_result_file(token)
    return FileResponse(path=path, media_type=content_type)
