"""Job attempt persistence repository."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.types import AttemptStatus, generate_prefixed_id
from app.idempotency.types import ensure_utc
from app.models.job_attempt import JobAttempt

SessionFactory = Callable[[], Session]


@dataclass(frozen=True)
class JobAttemptSnapshot:
    attempt_id: str
    job_id: str
    attempt_no: int
    execution_provider: str
    provider_model: Optional[str]
    attempt_status: AttemptStatus
    cancellation_intent: bool
    created_at: datetime
    updated_at: datetime


class JobAttemptRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def create_prepared_attempt(
        self,
        session: Session,
        *,
        job_id: str,
        attempt_no: int,
        execution_provider: str,
        provider_model: Optional[str],
        now: datetime,
    ) -> JobAttemptSnapshot:
        attempt = JobAttempt(
            attempt_id=generate_prefixed_id("attempt"),
            job_id=job_id,
            attempt_no=attempt_no,
            execution_provider=execution_provider,
            provider_model=provider_model,
            attempt_status=AttemptStatus.PREPARED,
            cancellation_intent=False,
            created_at=now,
            updated_at=now,
        )
        session.add(attempt)
        session.flush()
        return _snapshot(attempt)

    def get_current_for_job(
        self, *, job_id: str, current_attempt_id: str
    ) -> Optional[JobAttemptSnapshot]:
        with self._session_factory() as session:
            attempt = session.scalar(
                select(JobAttempt).where(
                    JobAttempt.job_id == job_id,
                    JobAttempt.attempt_id == current_attempt_id,
                )
            )
            return _snapshot(attempt) if attempt is not None else None

    def get_by_id(self, attempt_id: str) -> Optional[JobAttemptSnapshot]:
        with self._session_factory() as session:
            attempt = session.get(JobAttempt, attempt_id)
            return _snapshot(attempt) if attempt is not None else None

    def count_for_job(self, job_id: str) -> int:
        with self._session_factory() as session:
            return session.scalar(
                select(func.count()).select_from(JobAttempt).where(JobAttempt.job_id == job_id)
            ) or 0


def _snapshot(attempt: JobAttempt) -> JobAttemptSnapshot:
    return JobAttemptSnapshot(
        attempt_id=attempt.attempt_id,
        job_id=attempt.job_id,
        attempt_no=attempt.attempt_no,
        execution_provider=attempt.execution_provider,
        provider_model=attempt.provider_model,
        attempt_status=attempt.attempt_status,
        cancellation_intent=attempt.cancellation_intent,
        created_at=ensure_utc(attempt.created_at),
        updated_at=ensure_utc(attempt.updated_at),
    )
