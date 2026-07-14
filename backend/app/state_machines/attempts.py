"""Attempt state transition rules."""

from __future__ import annotations

from app.db.types import AttemptStatus

ATTEMPT_TRANSITIONS = {
    AttemptStatus.PREPARED: {AttemptStatus.SUBMITTED, AttemptStatus.CANCELLED},
    AttemptStatus.SUBMITTED: {
        AttemptStatus.PROCESSING,
        AttemptStatus.FAILED,
        AttemptStatus.UNKNOWN_PROVIDER_STATE,
    },
    AttemptStatus.PROCESSING: {
        AttemptStatus.SUCCEEDED,
        AttemptStatus.FAILED,
        AttemptStatus.CANCEL_REQUESTED,
    },
    AttemptStatus.CANCEL_REQUESTED: {
        AttemptStatus.CANCELLED,
        AttemptStatus.SUCCEEDED,
        AttemptStatus.UNKNOWN_PROVIDER_STATE,
    },
    AttemptStatus.UNKNOWN_PROVIDER_STATE: {
        AttemptStatus.SUCCEEDED,
        AttemptStatus.FAILED,
        AttemptStatus.CANCELLED,
    },
    AttemptStatus.SUCCEEDED: set(),
    AttemptStatus.FAILED: set(),
    AttemptStatus.CANCELLED: set(),
}
ATTEMPT_TERMINAL_STATES = {
    AttemptStatus.SUCCEEDED,
    AttemptStatus.FAILED,
    AttemptStatus.CANCELLED,
}


class InvalidAttemptTransitionError(ValueError):
    """Raised when an attempt transition is not allowed."""


def assert_attempt_transition(
    current: AttemptStatus,
    target: AttemptStatus,
) -> None:
    if target not in ATTEMPT_TRANSITIONS[current]:
        raise InvalidAttemptTransitionError(
            f"Attempt transition {current.value} -> {target.value} is not allowed."
        )
