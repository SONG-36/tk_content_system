"""Structured types for the idempotency service."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional, Protocol


class Clock(Protocol):
    """Injectable time source."""

    def now(self) -> datetime:
        """Return an aware UTC timestamp."""


class UtcClock:
    """Production UTC clock."""

    def now(self) -> datetime:
        return datetime.now(timezone.utc)


class FakeClock:
    """Deterministic clock for tests."""

    def __init__(self, current: datetime) -> None:
        self.current = ensure_utc(current)

    def now(self) -> datetime:
        return self.current

    def set(self, current: datetime) -> None:
        self.current = ensure_utc(current)


class IdempotencyDisposition(str, Enum):
    ACQUIRED = "ACQUIRED"
    REPLAY = "REPLAY"


class RecoveryStatus(str, Enum):
    RECOVERED = "RECOVERED"
    NOT_FOUND = "NOT_FOUND"
    INCOMPLETE = "INCOMPLETE"


@dataclass(frozen=True)
class CanonicalRequest:
    canonical_json: str
    canonical_request_hash: str
    path_params_hash: str


@dataclass(frozen=True)
class IdempotencyScope:
    owner_id: str
    http_method: str
    route_template: str
    path_params_hash: str
    idempotency_key_hash: str


@dataclass(frozen=True)
class IdempotencyRequest:
    scope: IdempotencyScope
    canonical_request_hash: str


@dataclass(frozen=True)
class IdempotencyAcquireResult:
    disposition: IdempotencyDisposition
    record_id: str
    response_status_code: Optional[int] = None
    response_json: Optional[dict[str, Any]] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    idempotent_replay: bool = False


@dataclass(frozen=True)
class RecoveryResult:
    status: RecoveryStatus
    response_status_code: Optional[int] = None
    response_json: Optional[dict[str, Any]] = None


class RecoveryResolver(Protocol):
    """Recover a response from a resource created before a lease expired."""

    def recover(self, resource_type: str, resource_id: str) -> RecoveryResult:
        """Return resource recovery status without causing a duplicate side effect."""


@dataclass(frozen=True)
class IdempotencyRecordSnapshot:
    record_id: str
    scope: IdempotencyScope
    canonical_request_hash: str
    status: str
    lease_expires_at: Optional[datetime]
    response_status_code: Optional[int]
    response_json: Optional[dict[str, Any]]
    resource_type: Optional[str]
    resource_id: Optional[str]
    expires_at: datetime
    created_at: datetime
    updated_at: datetime


def ensure_utc(value: datetime) -> datetime:
    """Normalize timestamps returned by SQLite into aware UTC datetimes."""

    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
