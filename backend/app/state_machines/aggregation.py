"""Attempt-to-job status aggregation."""

from __future__ import annotations

from app.db.types import AttemptStatus, GenerationStatus

ATTEMPT_TO_JOB_STATUS = {
    AttemptStatus.PREPARED: GenerationStatus.QUEUED,
    AttemptStatus.SUBMITTED: GenerationStatus.PROCESSING,
    AttemptStatus.PROCESSING: GenerationStatus.PROCESSING,
    AttemptStatus.SUCCEEDED: GenerationStatus.SUCCEEDED,
    AttemptStatus.FAILED: GenerationStatus.FAILED,
    AttemptStatus.CANCEL_REQUESTED: GenerationStatus.PROCESSING,
    AttemptStatus.CANCELLED: GenerationStatus.CANCELLED,
    AttemptStatus.UNKNOWN_PROVIDER_STATE: GenerationStatus.PROCESSING,
}


def aggregate_attempt_status(attempt_status: AttemptStatus) -> GenerationStatus:
    return ATTEMPT_TO_JOB_STATUS[attempt_status]
