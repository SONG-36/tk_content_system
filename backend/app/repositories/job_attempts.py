"""Job attempt persistence repository."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import func, select, update
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
    provider_job_id: Optional[str]
    error_code: Optional[str]
    submitted_at: Optional[datetime]
    terminal_at: Optional[datetime]
    cancel_requested_at: Optional[datetime]
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

    def list_for_job(self, job_id: str) -> list[JobAttemptSnapshot]:
        with self._session_factory() as session:
            rows = session.scalars(
                select(JobAttempt)
                .where(JobAttempt.job_id == job_id)
                .order_by(JobAttempt.attempt_no.asc(), JobAttempt.created_at.asc())
            ).all()
            return [_snapshot(row) for row in rows]

    def next_attempt_no(self, session: Session, job_id: str) -> int:
        current_max = session.scalar(
            select(func.max(JobAttempt.attempt_no)).where(JobAttempt.job_id == job_id)
        )
        return int(current_max or 0) + 1

    def set_cancellation_intent(
        self,
        session: Session,
        *,
        attempt_id: str,
        now: datetime,
    ) -> bool:
        result = session.execute(
            update(JobAttempt)
            .where(JobAttempt.attempt_id == attempt_id)
            .where(JobAttempt.cancellation_intent.is_(False))
            .values(
                cancellation_intent=True,
                cancel_requested_at=now,
                updated_at=now,
            )
        )
        return result.rowcount == 1

    def transition_attempt(
        self,
        session: Session,
        *,
        attempt_id: str,
        expected_status: AttemptStatus,
        target_status: AttemptStatus,
        now: datetime,
        provider_job_id: Optional[str] = None,
        error_code: Optional[str] = None,
        cancellation_intent: Optional[bool] = None,
        cancel_requested_at: Optional[datetime] = None,
        submitted_at: Optional[datetime] = None,
        terminal_at: Optional[datetime] = None,
    ) -> bool:
        values: dict[str, object] = {
            "attempt_status": target_status,
            "updated_at": now,
        }
        if provider_job_id is not None:
            values["provider_job_id"] = provider_job_id
        if error_code is not None:
            values["error_code"] = error_code
        if cancellation_intent is not None:
            values["cancellation_intent"] = cancellation_intent
        if cancel_requested_at is not None:
            values["cancel_requested_at"] = cancel_requested_at
        if submitted_at is not None:
            values["submitted_at"] = submitted_at
        if terminal_at is not None:
            values["terminal_at"] = terminal_at
        result = session.execute(
            update(JobAttempt)
            .where(JobAttempt.attempt_id == attempt_id)
            .where(JobAttempt.attempt_status == expected_status)
            .values(**values)
        )
        return result.rowcount == 1

    def list_non_terminal_mock_attempts(self) -> list[JobAttemptSnapshot]:
        with self._session_factory() as session:
            rows = session.scalars(
                select(JobAttempt).where(
                    JobAttempt.execution_provider == "mock",
                    JobAttempt.attempt_status.in_(
                        [
                            AttemptStatus.PREPARED,
                            AttemptStatus.SUBMITTED,
                            AttemptStatus.PROCESSING,
                            AttemptStatus.CANCEL_REQUESTED,
                            AttemptStatus.UNKNOWN_PROVIDER_STATE,
                        ]
                    ),
                )
            ).all()
            return [_snapshot(row) for row in rows]

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
        provider_job_id=attempt.provider_job_id,
        error_code=attempt.error_code,
        submitted_at=(
            ensure_utc(attempt.submitted_at) if attempt.submitted_at is not None else None
        ),
        terminal_at=(
            ensure_utc(attempt.terminal_at) if attempt.terminal_at is not None else None
        ),
        cancel_requested_at=(
            ensure_utc(attempt.cancel_requested_at)
            if attempt.cancel_requested_at is not None
            else None
        ),
        created_at=ensure_utc(attempt.created_at),
        updated_at=ensure_utc(attempt.updated_at),
    )
