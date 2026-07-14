"""FastAPI BackgroundTasks-compatible mock provider runner."""

from __future__ import annotations

import hashlib
from typing import Optional

from sqlalchemy.orm import Session

from app.config import Settings
from app.db.types import (
    AssetStatus,
    AttemptStatus,
    GenerationStatus,
    ProviderNormalizedStatus,
    generate_prefixed_id,
)
from app.idempotency.types import Clock, UtcClock, ensure_utc
from app.models.job_attempt import JobAttempt
from app.models.video_job import VideoJob
from app.providers.base import MockOutcome
from app.providers.mock import MockProvider
from app.repositories.assets import AssetRepository
from app.repositories.job_attempts import JobAttemptRepository
from app.repositories.provider_results import ProviderResultRepository
from app.repositories.request_snapshots import GenerationRequestSnapshotRepository
from app.repositories.video_jobs import VideoJobRepository
from app.state_machines.aggregation import aggregate_attempt_status
from app.state_machines.attempts import assert_attempt_transition
from app.state_machines.jobs import assert_job_transition
from app.storage.local_mock import LocalMockStorage


class MockProviderRunner:
    """Runs one prepared mock attempt using short transactions."""

    def __init__(
        self,
        *,
        settings: Settings,
        session_factory,
        provider: Optional[MockProvider] = None,
        clock: Optional[Clock] = None,
        storage: Optional[LocalMockStorage] = None,
        attempts: Optional[JobAttemptRepository] = None,
        jobs: Optional[VideoJobRepository] = None,
        snapshots: Optional[GenerationRequestSnapshotRepository] = None,
        assets: Optional[AssetRepository] = None,
        provider_results: Optional[ProviderResultRepository] = None,
    ) -> None:
        self._settings = settings
        self._session_factory = session_factory
        self._provider = provider or MockProvider()
        self._clock = clock or UtcClock()
        self._storage = storage or LocalMockStorage(settings.mock_storage_directory)
        self._attempts = attempts or JobAttemptRepository(session_factory)
        self._jobs = jobs or VideoJobRepository(session_factory)
        self._snapshots = snapshots or GenerationRequestSnapshotRepository(
            session_factory
        )
        self._assets = assets or AssetRepository(session_factory)
        self._provider_results = provider_results or ProviderResultRepository(
            session_factory
        )

    def run_job(self, job_id: str) -> None:
        try:
            started = self._start_attempt(job_id)
            if started is None:
                return
            attempt_id, provider_job_id, request_snapshot = started
            execution = self._provider.execute(provider_job_id, request_snapshot)
            if execution.outcome == MockOutcome.success:
                self._complete_success(
                    job_id=job_id,
                    attempt_id=attempt_id,
                    provider_job_id=provider_job_id,
                    result_bytes=execution.result_bytes or b"",
                    raw_payload=execution.raw_payload or {},
                )
            elif execution.outcome == MockOutcome.failed:
                self._complete_failed(job_id, attempt_id, "MOCK_PROVIDER_FAILED")
            elif execution.outcome == MockOutcome.unknown:
                self._mark_unknown(job_id, attempt_id)
            elif execution.outcome == MockOutcome.cancel:
                self._complete_cancelled(job_id, attempt_id)
        except Exception:
            self._best_effort_fail(job_id, "MOCK_RUNNER_INTERNAL_ERROR")

    def cancel_job(self, job_id: str) -> None:
        now = ensure_utc(self._clock.now())
        with self._session_factory() as session:
            job = session.get(VideoJob, job_id)
            if job is None or job.current_attempt_id is None:
                return
            attempt = session.get(JobAttempt, job.current_attempt_id)
            if attempt is None or attempt.attempt_status != AttemptStatus.CANCEL_REQUESTED:
                return
            assert_attempt_transition(AttemptStatus.CANCEL_REQUESTED, AttemptStatus.CANCELLED)
            assert_job_transition(GenerationStatus.PROCESSING, GenerationStatus.CANCELLED)
            attempt_ok = self._attempts.transition_attempt(
                session,
                attempt_id=attempt.attempt_id,
                expected_status=AttemptStatus.CANCEL_REQUESTED,
                target_status=AttemptStatus.CANCELLED,
                terminal_at=now,
                now=now,
            )
            job_ok = self._jobs.transition_job(
                session,
                job_id=job.job_id,
                expected_status=GenerationStatus.PROCESSING,
                target_status=GenerationStatus.CANCELLED,
                now=now,
            )
            if attempt_ok and job_ok:
                session.commit()
            else:
                session.rollback()

    def _start_attempt(
        self, job_id: str
    ) -> Optional[tuple[str, str, dict[str, object]]]:
        now = ensure_utc(self._clock.now())
        with self._session_factory() as session:
            job = session.get(VideoJob, job_id)
            if job is None or job.current_attempt_id is None:
                return None
            attempt = session.get(JobAttempt, job.current_attempt_id)
            if (
                attempt is None
                or job.generation_status != GenerationStatus.QUEUED
                or attempt.attempt_status != AttemptStatus.PREPARED
            ):
                return None
            assert_attempt_transition(AttemptStatus.PREPARED, AttemptStatus.SUBMITTED)
            assert_job_transition(GenerationStatus.QUEUED, GenerationStatus.PROCESSING)
            attempt_ok = self._attempts.transition_attempt(
                session,
                attempt_id=attempt.attempt_id,
                expected_status=AttemptStatus.PREPARED,
                target_status=AttemptStatus.SUBMITTED,
                submitted_at=now,
                now=now,
            )
            if not attempt_ok:
                session.rollback()
                return None
            job_ok = self._jobs.transition_job(
                session,
                job_id=job_id,
                expected_status=GenerationStatus.QUEUED,
                target_status=GenerationStatus.PROCESSING,
                now=now,
            )
            if not job_ok:
                session.rollback()
                return None
            session.commit()
            attempt_id = attempt.attempt_id

        snapshot = self._snapshots.get_by_job_id(job_id)
        if snapshot is None:
            self._best_effort_fail(job_id, "MOCK_RUNNER_INTERNAL_ERROR")
            return None
        submission = self._provider.submit(snapshot.request_json)
        with self._session_factory() as session:
            attempt = session.get(JobAttempt, attempt_id)
            if attempt is None or attempt.attempt_status != AttemptStatus.SUBMITTED:
                return None
            attempt.provider_job_id = submission.provider_job_id
            attempt.updated_at = ensure_utc(self._clock.now())
            session.commit()
            return attempt_id, submission.provider_job_id, snapshot.request_json

    def _complete_success(
        self,
        *,
        job_id: str,
        attempt_id: str,
        provider_job_id: str,
        result_bytes: bytes,
        raw_payload: dict[str, object],
    ) -> None:
        if b"ftyp" not in result_bytes[:32]:
            self._complete_failed(job_id, attempt_id, "MOCK_RESULT_INVALID")
            return
        result_asset_id = generate_prefixed_id("asset")
        checksum = hashlib.sha256(result_bytes).hexdigest()
        try:
            storage_path = self._storage.write_result_atomic(
                asset_id=result_asset_id,
                content_type="video/mp4",
                data=result_bytes,
            )
        except Exception:
            self._complete_failed(job_id, attempt_id, "MOCK_RESULT_STORAGE_FAILED")
            return

        now = ensure_utc(self._clock.now())
        try:
            with self._session_factory() as session:
                job = session.get(VideoJob, job_id)
                attempt = session.get(JobAttempt, attempt_id)
                if job is None or attempt is None or job.generation_status != GenerationStatus.PROCESSING:
                    session.rollback()
                    self._storage.delete(storage_path)
                    return
                if attempt.attempt_status in {
                    AttemptStatus.CANCELLED,
                    AttemptStatus.FAILED,
                    AttemptStatus.UNKNOWN_PROVIDER_STATE,
                }:
                    session.rollback()
                    self._storage.delete(storage_path)
                    return
                if attempt.attempt_status not in {
                    AttemptStatus.SUBMITTED,
                    AttemptStatus.PROCESSING,
                    AttemptStatus.CANCEL_REQUESTED,
                }:
                    session.rollback()
                    self._storage.delete(storage_path)
                    return
                if attempt.attempt_status == AttemptStatus.SUBMITTED:
                    assert_attempt_transition(
                        AttemptStatus.SUBMITTED, AttemptStatus.PROCESSING
                    )
                    if not self._attempts.transition_attempt(
                        session,
                        attempt_id=attempt_id,
                        expected_status=AttemptStatus.SUBMITTED,
                        target_status=AttemptStatus.PROCESSING,
                        now=now,
                    ):
                        session.rollback()
                        self._storage.delete(storage_path)
                        return
                    attempt = session.get(JobAttempt, attempt_id)
                    if attempt is None:
                        session.rollback()
                        self._storage.delete(storage_path)
                        return
                result_asset = self._assets.create_result_media(
                    session,
                    asset_id=result_asset_id,
                    owner_id=job.owner_id,
                    content_type="video/mp4",
                    size_bytes=len(result_bytes),
                    checksum_sha256=checksum,
                    storage_path=storage_path,
                    now=now,
                )
                self._provider_results.create_success_result(
                    session,
                    attempt_id=attempt_id,
                    result_asset_ids=[result_asset.asset_id],
                    raw_payload={
                        "provider": "mock",
                        "provider_job_id": provider_job_id,
                        **raw_payload,
                    },
                    now=now,
                )
                expected_attempt_status = attempt.attempt_status
                assert_attempt_transition(expected_attempt_status, AttemptStatus.SUCCEEDED)
                assert_job_transition(GenerationStatus.PROCESSING, GenerationStatus.SUCCEEDED)
                attempt_ok = self._attempts.transition_attempt(
                    session,
                    attempt_id=attempt_id,
                    expected_status=expected_attempt_status,
                    target_status=AttemptStatus.SUCCEEDED,
                    terminal_at=now,
                    now=now,
                )
                job_ok = self._jobs.transition_job(
                    session,
                    job_id=job_id,
                    expected_status=GenerationStatus.PROCESSING,
                    target_status=GenerationStatus.SUCCEEDED,
                    now=now,
                )
                if attempt_ok and job_ok:
                    session.commit()
                else:
                    session.rollback()
                    self._storage.delete(storage_path)
        except Exception:
            self._storage.delete(storage_path)
            self._best_effort_fail(job_id, "MOCK_RUNNER_INTERNAL_ERROR")

    def _complete_failed(self, job_id: str, attempt_id: str, error_code: str) -> None:
        now = ensure_utc(self._clock.now())
        with self._session_factory() as session:
            attempt = session.get(JobAttempt, attempt_id)
            job = session.get(VideoJob, job_id)
            if attempt is None or job is None:
                return
            if attempt.attempt_status == AttemptStatus.SUBMITTED:
                assert_attempt_transition(AttemptStatus.SUBMITTED, AttemptStatus.PROCESSING)
                self._attempts.transition_attempt(
                    session,
                    attempt_id=attempt_id,
                    expected_status=AttemptStatus.SUBMITTED,
                    target_status=AttemptStatus.PROCESSING,
                    now=now,
                )
            attempt = session.get(JobAttempt, attempt_id)
            if attempt is None or attempt.attempt_status != AttemptStatus.PROCESSING:
                session.commit()
                return
            assert_attempt_transition(AttemptStatus.PROCESSING, AttemptStatus.FAILED)
            assert_job_transition(GenerationStatus.PROCESSING, GenerationStatus.FAILED)
            self._attempts.transition_attempt(
                session,
                attempt_id=attempt_id,
                expected_status=AttemptStatus.PROCESSING,
                target_status=AttemptStatus.FAILED,
                error_code=error_code,
                terminal_at=now,
                now=now,
            )
            self._jobs.transition_job(
                session,
                job_id=job_id,
                expected_status=GenerationStatus.PROCESSING,
                target_status=GenerationStatus.FAILED,
                now=now,
            )
            session.commit()

    def _mark_unknown(self, job_id: str, attempt_id: str) -> None:
        now = ensure_utc(self._clock.now())
        with self._session_factory() as session:
            assert_attempt_transition(
                AttemptStatus.SUBMITTED, AttemptStatus.UNKNOWN_PROVIDER_STATE
            )
            self._attempts.transition_attempt(
                session,
                attempt_id=attempt_id,
                expected_status=AttemptStatus.SUBMITTED,
                target_status=AttemptStatus.UNKNOWN_PROVIDER_STATE,
                now=now,
            )
            # Aggregation keeps Job PROCESSING.
            session.commit()

    def _complete_cancelled(self, job_id: str, attempt_id: str) -> None:
        now = ensure_utc(self._clock.now())
        with self._session_factory() as session:
            if not self._attempts.transition_attempt(
                session,
                attempt_id=attempt_id,
                expected_status=AttemptStatus.SUBMITTED,
                target_status=AttemptStatus.PROCESSING,
                now=now,
            ):
                session.rollback()
                return
            assert_attempt_transition(AttemptStatus.PROCESSING, AttemptStatus.CANCEL_REQUESTED)
            self._attempts.transition_attempt(
                session,
                attempt_id=attempt_id,
                expected_status=AttemptStatus.PROCESSING,
                target_status=AttemptStatus.CANCEL_REQUESTED,
                cancellation_intent=True,
                cancel_requested_at=now,
                now=now,
            )
            assert_attempt_transition(AttemptStatus.CANCEL_REQUESTED, AttemptStatus.CANCELLED)
            assert_job_transition(GenerationStatus.PROCESSING, GenerationStatus.CANCELLED)
            self._attempts.transition_attempt(
                session,
                attempt_id=attempt_id,
                expected_status=AttemptStatus.CANCEL_REQUESTED,
                target_status=AttemptStatus.CANCELLED,
                terminal_at=now,
                now=now,
            )
            self._jobs.transition_job(
                session,
                job_id=job_id,
                expected_status=GenerationStatus.PROCESSING,
                target_status=GenerationStatus.CANCELLED,
                now=now,
            )
            session.commit()

    def _best_effort_fail(self, job_id: str, error_code: str) -> None:
        now = ensure_utc(self._clock.now())
        with self._session_factory() as session:
            job = session.get(VideoJob, job_id)
            if job is None or job.current_attempt_id is None:
                return
            attempt = session.get(JobAttempt, job.current_attempt_id)
            if attempt is None or attempt.attempt_status in {
                AttemptStatus.SUCCEEDED,
                AttemptStatus.FAILED,
                AttemptStatus.CANCELLED,
            }:
                return
            self._attempts.transition_attempt(
                session,
                attempt_id=attempt.attempt_id,
                expected_status=attempt.attempt_status,
                target_status=AttemptStatus.FAILED,
                error_code=error_code,
                terminal_at=now,
                now=now,
            )
            if job.generation_status in {
                GenerationStatus.QUEUED,
                GenerationStatus.PROCESSING,
            }:
                self._jobs.mark_current_job_failed_for_attempt(
                    session,
                    job_id=job.job_id,
                    current_attempt_id=attempt.attempt_id,
                    now=now,
                )
            session.commit()
