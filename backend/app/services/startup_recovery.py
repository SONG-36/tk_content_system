"""Startup recovery for interrupted mock runner attempts."""

from __future__ import annotations

from typing import Optional

from sqlalchemy.exc import SQLAlchemyError

from app.db.types import AttemptStatus
from app.idempotency.types import Clock, UtcClock, ensure_utc
from app.repositories.job_attempts import JobAttemptRepository, SessionFactory
from app.repositories.video_jobs import VideoJobRepository


class StartupRecoveryService:
    def __init__(
        self,
        *,
        session_factory: SessionFactory,
        clock: Optional[Clock] = None,
        attempts: Optional[JobAttemptRepository] = None,
        jobs: Optional[VideoJobRepository] = None,
    ) -> None:
        self._session_factory = session_factory
        self._clock = clock or UtcClock()
        self._attempts = attempts or JobAttemptRepository(session_factory)
        self._jobs = jobs or VideoJobRepository(session_factory)

    def recover_mock_attempts(self) -> int:
        try:
            attempts = self._attempts.list_non_terminal_mock_attempts()
        except SQLAlchemyError:
            # Migrations may not have been applied in metadata-only tests.
            return 0
        recovered = 0
        now = ensure_utc(self._clock.now())
        for attempt in attempts:
            with self._session_factory() as session:
                if self._attempts.transition_attempt(
                    session,
                    attempt_id=attempt.attempt_id,
                    expected_status=attempt.attempt_status,
                    target_status=AttemptStatus.FAILED,
                    error_code="MOCK_RUNNER_INTERRUPTED",
                    terminal_at=now,
                    now=now,
                ):
                    self._jobs.mark_current_job_failed_for_attempt(
                        session,
                        job_id=attempt.job_id,
                        current_attempt_id=attempt.attempt_id,
                        now=now,
                    )
                    session.commit()
                    recovered += 1
                else:
                    session.rollback()
        return recovered
