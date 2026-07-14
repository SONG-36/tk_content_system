"""Public video job endpoints implemented in Phase 2A-6."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import JSONResponse

from app.dependencies import (
    OwnerContext,
    get_video_job_service,
    require_owner_context,
)
from app.schemas.jobs import CreateVideoJobRequest
from app.services.video_jobs import VideoJobService

router = APIRouter(prefix="/v1/video-jobs", tags=["video-jobs"])


@router.post("")
async def create_video_job(
    payload: CreateVideoJobRequest,
    request: Request,
    owner: OwnerContext = Depends(require_owner_context),
    video_job_service: VideoJobService = Depends(get_video_job_service),
    idempotency_key: Optional[str] = Header(default=None, alias="Idempotency-Key"),
) -> JSONResponse:
    result = video_job_service.create_video_job(
        owner_id=owner.owner_id,
        request=payload,
        idempotency_key=idempotency_key,
        request_id=request.state.request_id,
    )
    return JSONResponse(status_code=result.status_code, content=result.payload)
