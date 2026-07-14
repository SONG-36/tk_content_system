"""Public asset endpoints."""

from __future__ import annotations

from typing import Optional, Union

from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import JSONResponse

from app.dependencies import OwnerContext, get_asset_service, require_owner_context
from app.schemas.assets import UploadUrlRequest, UploadUrlResponse
from app.services.assets import AssetService

router = APIRouter(prefix="/v1/assets", tags=["assets"])


@router.post(
    "/upload-url",
    response_model=UploadUrlResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_upload_url(
    payload: UploadUrlRequest,
    owner: OwnerContext = Depends(require_owner_context),
    asset_service: AssetService = Depends(get_asset_service),
    idempotency_key: Optional[str] = Header(default=None, alias="Idempotency-Key"),
) -> Union[UploadUrlResponse, JSONResponse]:
    response = asset_service.request_upload_url(
        owner_id=owner.owner_id,
        request=payload,
        idempotency_key=idempotency_key,
    )
    status_code = status.HTTP_201_CREATED
    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(mode="json"),
    )
