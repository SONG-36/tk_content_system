"""Job state transition rules."""

from __future__ import annotations

from app.db.types import GenerationStatus

JOB_TRANSITIONS = {
    GenerationStatus.QUEUED: {
        GenerationStatus.PROCESSING,
        GenerationStatus.FAILED,
        GenerationStatus.CANCELLED,
    },
    GenerationStatus.PROCESSING: {
        GenerationStatus.SUCCEEDED,
        GenerationStatus.FAILED,
        GenerationStatus.CANCELLED,
    },
    GenerationStatus.FAILED: {GenerationStatus.QUEUED},
    GenerationStatus.CANCELLED: {GenerationStatus.QUEUED},
    GenerationStatus.SUCCEEDED: set(),
}
JOB_TERMINAL_STATES = {GenerationStatus.SUCCEEDED}


class InvalidJobTransitionError(ValueError):
    """Raised when a job transition is not allowed."""


def assert_job_transition(
    current: GenerationStatus,
    target: GenerationStatus,
) -> None:
    if target not in JOB_TRANSITIONS[current]:
        raise InvalidJobTransitionError(
            f"Job transition {current.value} -> {target.value} is not allowed."
        )
