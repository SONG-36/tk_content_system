"""Reusable idempotency primitives for side-effect endpoints."""

from app.idempotency.canonical import (
    canonicalize_request,
    hash_idempotency_key,
    validate_idempotency_key,
)
from app.idempotency.policy import CachePolicy
from app.idempotency.service import IdempotencyService
from app.idempotency.types import (
    CanonicalRequest,
    FakeClock,
    IdempotencyAcquireResult,
    IdempotencyDisposition,
    IdempotencyScope,
    RecoveryResult,
    RecoveryStatus,
    UtcClock,
)

__all__ = [
    "CachePolicy",
    "CanonicalRequest",
    "FakeClock",
    "IdempotencyAcquireResult",
    "IdempotencyDisposition",
    "IdempotencyScope",
    "IdempotencyService",
    "RecoveryResult",
    "RecoveryStatus",
    "UtcClock",
    "canonicalize_request",
    "hash_idempotency_key",
    "validate_idempotency_key",
]
