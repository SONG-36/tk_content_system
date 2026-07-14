"""Provider protocol types."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Protocol


class MockOutcome(str, Enum):
    success = "success"
    failed = "failed"
    unknown = "unknown"
    cancel = "cancel"


@dataclass(frozen=True)
class ProviderSubmissionResult:
    provider_job_id: str


@dataclass(frozen=True)
class MockExecutionResult:
    outcome: MockOutcome
    normalized_status: str
    provider_job_id: str
    content_type: Optional[str] = None
    result_bytes: Optional[bytes] = None
    raw_payload: Optional[dict[str, Any]] = None
    error_code: Optional[str] = None


class Provider(Protocol):
    def submit(self, request_snapshot: dict[str, Any]) -> ProviderSubmissionResult:
        """Submit provider work and return a provider job id."""

    def execute(
        self,
        provider_job_id: str,
        request_snapshot: dict[str, Any],
    ) -> MockExecutionResult:
        """Execute provider work for Phase 2A mock tests."""
