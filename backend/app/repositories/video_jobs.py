"""Video job persistence repository."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.db.types import AIReviewStatus, GenerationStatus, generate_prefixed_id
from app.idempotency.types import ensure_utc
from app.models.video_job import VideoJob

SessionFactory = Callable[[], Session]


@dataclass(frozen=True)
class VideoJobSnapshot:
    job_id: str
    owner_id: str
    contract_version: str
    truth_rule_version: str
    provider_mapping_version: str
    selected_model: str
    execution_provider: str
    generation_status: GenerationStatus
    ai_review_status: AIReviewStatus
    current_attempt_id: Optional[str]
    created_at: datetime
    updated_at: datetime


class VideoJobRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def create_queued_job(
        self,
        session: Session,
        *,
        owner_id: str,
        contract_version: str,
        truth_rule_version: str,
        provider_mapping_version: str,
        selected_model: str,
        execution_provider: str,
        now: datetime,
    ) -> VideoJobSnapshot:
        job = VideoJob(
            job_id=generate_prefixed_id("job"),
            owner_id=owner_id,
            contract_version=contract_version,
            truth_rule_version=truth_rule_version,
            provider_mapping_version=provider_mapping_version,
            selected_model=selected_model,
            execution_provider=execution_provider,
            generation_status=GenerationStatus.QUEUED,
            ai_review_status=AIReviewStatus.NOT_RUN,
            created_at=now,
            updated_at=now,
        )
        session.add(job)
        session.flush()
        return _snapshot(job)

    def update_current_attempt_id(
        self,
        session: Session,
        *,
        job_id: str,
        attempt_id: str,
        now: datetime,
    ) -> VideoJobSnapshot:
        job = session.get(VideoJob, job_id)
        if job is None:
            raise ValueError("Video job not found.")
        job.current_attempt_id = attempt_id
        job.updated_at = now
        session.flush()
        return _snapshot(job)

    def get_by_id_and_owner(
        self, *, job_id: str, owner_id: str
    ) -> Optional[VideoJobSnapshot]:
        with self._session_factory() as session:
            job = session.scalar(
                select(VideoJob).where(
                    VideoJob.job_id == job_id,
                    VideoJob.owner_id == owner_id,
                )
            )
            return _snapshot(job) if job is not None else None

    def get_by_id(self, job_id: str) -> Optional[VideoJobSnapshot]:
        with self._session_factory() as session:
            job = session.get(VideoJob, job_id)
            return _snapshot(job) if job is not None else None

    def transition_job(
        self,
        session: Session,
        *,
        job_id: str,
        expected_status: GenerationStatus,
        target_status: GenerationStatus,
        now: datetime,
    ) -> bool:
        result = session.execute(
            update(VideoJob)
            .where(VideoJob.job_id == job_id)
            .where(VideoJob.generation_status == expected_status)
            .values(generation_status=target_status, updated_at=now)
        )
        return result.rowcount == 1

    def mark_current_job_failed_for_attempt(
        self,
        session: Session,
        *,
        job_id: str,
        current_attempt_id: str,
        now: datetime,
    ) -> bool:
        result = session.execute(
            update(VideoJob)
            .where(VideoJob.job_id == job_id)
            .where(VideoJob.current_attempt_id == current_attempt_id)
            .where(
                VideoJob.generation_status.in_(
                    [GenerationStatus.QUEUED, GenerationStatus.PROCESSING]
                )
            )
            .values(generation_status=GenerationStatus.FAILED, updated_at=now)
        )
        return result.rowcount == 1


def _snapshot(job: VideoJob) -> VideoJobSnapshot:
    return VideoJobSnapshot(
        job_id=job.job_id,
        owner_id=job.owner_id,
        contract_version=job.contract_version,
        truth_rule_version=job.truth_rule_version,
        provider_mapping_version=job.provider_mapping_version,
        selected_model=job.selected_model,
        execution_provider=job.execution_provider,
        generation_status=job.generation_status,
        ai_review_status=job.ai_review_status,
        current_attempt_id=job.current_attempt_id,
        created_at=ensure_utc(job.created_at),
        updated_at=ensure_utc(job.updated_at),
    )
