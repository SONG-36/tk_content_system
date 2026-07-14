"""Internal mock upload route excluded from public Action OpenAPI."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from app.dependencies import get_asset_service
from app.schemas.assets import InternalUploadResponse
from app.services.assets import AssetService

router = APIRouter(tags=["internal"])


@router.put(
    "/_internal/mock-uploads/{token}",
    response_model=InternalUploadResponse,
    include_in_schema=False,
)
async def upload_mock_asset(
    token: str,
    request: Request,
    asset_service: AssetService = Depends(get_asset_service),
) -> InternalUploadResponse:
    body = await request.body()
    return asset_service.complete_mock_upload(
        token=token,
        content_type=request.headers.get("content-type"),
        body=body,
    )
