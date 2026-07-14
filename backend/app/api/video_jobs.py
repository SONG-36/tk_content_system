"""Public video job endpoints implemented in Phase 2A-6."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Header, Request
from fastapi.responses import JSONResponse

from app.dependencies import (
    OwnerContext,
    get_mock_provider_runner,
    get_video_job_service,
    require_owner_context,
)
from app.schemas.jobs import CreateVideoJobRequest
from app.runners.mock_provider import MockProviderRunner
from app.services.video_jobs import VideoJobService

router = APIRouter(prefix="/v1/video-jobs", tags=["video-jobs"])


@router.post("")
async def create_video_job(
    payload: CreateVideoJobRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    owner: OwnerContext = Depends(require_owner_context),
    video_job_service: VideoJobService = Depends(get_video_job_service),
    runner: MockProviderRunner = Depends(get_mock_provider_runner),
    idempotency_key: Optional[str] = Header(default=None, alias="Idempotency-Key"),
) -> JSONResponse:
    result = video_job_service.create_video_job(
        owner_id=owner.owner_id,
        request=payload,
        idempotency_key=idempotency_key,
        request_id=request.state.request_id,
    )
    if result.dispatch_required and result.job_id is not None:
        background_tasks.add_task(runner.run_job, result.job_id)
    return JSONResponse(status_code=result.status_code, content=result.payload)
