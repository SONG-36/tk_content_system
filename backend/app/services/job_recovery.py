"""Recovery resolver for expired PENDING create-job idempotency records."""

from __future__ import annotations

from app.idempotency import RecoveryResult, RecoveryStatus
from app.db.types import AttemptStatus, GenerationStatus
from app.repositories.job_attempts import JobAttemptRepository
from app.repositories.request_snapshots import GenerationRequestSnapshotRepository
from app.repositories.video_jobs import VideoJobRepository


class VideoJobRecoveryResolver:
    """Recover a create-job response from an already-created VideoJob."""

    def __init__(
        self,
        *,
        video_jobs: VideoJobRepository,
        attempts: JobAttemptRepository,
        snapshots: GenerationRequestSnapshotRepository,
    ) -> None:
        self._video_jobs = video_jobs
        self._attempts = attempts
        self._snapshots = snapshots

    def recover(self, resource_type: str, resource_id: str) -> RecoveryResult:
        if resource_type != "video_job":
            return RecoveryResult(status=RecoveryStatus.INCOMPLETE)
        job = self._video_jobs.get_by_id(resource_id)
        if job is None:
            return RecoveryResult(status=RecoveryStatus.NOT_FOUND)
        if job.current_attempt_id is None:
            return RecoveryResult(status=RecoveryStatus.INCOMPLETE)
        attempt = self._attempts.get_current_for_job(
            job_id=job.job_id,
            current_attempt_id=job.current_attempt_id,
        )
        snapshot = self._snapshots.get_by_job_id(job.job_id)
        if attempt is None or snapshot is None:
            return RecoveryResult(status=RecoveryStatus.INCOMPLETE)
        return RecoveryResult(
            status=RecoveryStatus.RECOVERED,
            response_status_code=202,
            response_json={
                "job_id": job.job_id,
                "generation_status": job.generation_status.value,
                "ai_review_status": job.ai_review_status.value,
                "execution_provider": job.execution_provider,
                "contract_version": job.contract_version,
                "truth_rule_version": job.truth_rule_version,
                "provider_mapping_version": job.provider_mapping_version,
                "idempotent_replay": False,
            },
        )


class CancelJobRecoveryResolver:
    """Recover a cancel response from a video job after a pending lease expires."""

    def __init__(
        self,
        *,
        video_jobs: VideoJobRepository,
        attempts: JobAttemptRepository,
    ) -> None:
        self._video_jobs = video_jobs
        self._attempts = attempts

    def recover(self, resource_type: str, resource_id: str) -> RecoveryResult:
        if resource_type != "video_job":
            return RecoveryResult(status=RecoveryStatus.INCOMPLETE)
        job = self._video_jobs.get_by_id(resource_id)
        if job is None or job.current_attempt_id is None:
            return RecoveryResult(status=RecoveryStatus.NOT_FOUND)
        attempt = self._attempts.get_current_for_job(
            job_id=job.job_id,
            current_attempt_id=job.current_attempt_id,
        )
        if attempt is None:
            return RecoveryResult(status=RecoveryStatus.INCOMPLETE)
        if (
            job.generation_status == GenerationStatus.CANCELLED
            and attempt.attempt_status == AttemptStatus.CANCELLED
        ):
            status_code = 200
        elif attempt.attempt_status in {
            AttemptStatus.CANCEL_REQUESTED,
            AttemptStatus.UNKNOWN_PROVIDER_STATE,
        }:
            status_code = 202
        else:
            return RecoveryResult(status=RecoveryStatus.INCOMPLETE)
        return RecoveryResult(
            status=RecoveryStatus.RECOVERED,
            response_status_code=status_code,
            response_json={
                "job_id": job.job_id,
                "generation_status": job.generation_status.value,
                "attempt_status": attempt.attempt_status.value,
                "cancellation_intent": attempt.cancellation_intent,
                "cancel_requested_at": (
                    attempt.cancel_requested_at.isoformat()
                    if attempt.cancel_requested_at is not None
                    else None
                ),
                "idempotent_replay": False,
            },
        )


class RetryJobRecoveryResolver:
    """Recover a retry response from a created retry attempt."""

    def __init__(
        self,
        *,
        video_jobs: VideoJobRepository,
        attempts: JobAttemptRepository,
    ) -> None:
        self._video_jobs = video_jobs
        self._attempts = attempts

    def recover(self, resource_type: str, resource_id: str) -> RecoveryResult:
        if resource_type != "job_attempt":
            return RecoveryResult(status=RecoveryStatus.INCOMPLETE)
        attempt = self._attempts.get_by_id(resource_id)
        if attempt is None:
            return RecoveryResult(status=RecoveryStatus.NOT_FOUND)
        job = self._video_jobs.get_by_id(attempt.job_id)
        if job is None:
            return RecoveryResult(status=RecoveryStatus.NOT_FOUND)
        return RecoveryResult(
            status=RecoveryStatus.RECOVERED,
            response_status_code=202,
            response_json={
                "job_id": job.job_id,
                "generation_status": GenerationStatus.QUEUED.value,
                "new_attempt_id": attempt.attempt_id,
                "idempotent_replay": False,
            },
        )
