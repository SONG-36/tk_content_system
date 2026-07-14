"""Deterministic Phase 2A mock provider."""

from __future__ import annotations

from importlib import resources
from typing import Any

from app.providers.base import (
    MockExecutionResult,
    MockOutcome,
    ProviderSubmissionResult,
)


class MockProvider:
    """Provider controlled by dependency injection, never by public request data."""

    def __init__(self, outcome: MockOutcome = MockOutcome.success) -> None:
        self.outcome = outcome
        self.submit_count = 0
        self.execute_count = 0

    def submit(self, request_snapshot: dict[str, Any]) -> ProviderSubmissionResult:
        self.submit_count += 1
        return ProviderSubmissionResult(provider_job_id=f"mock_job_{self.submit_count}")

    def execute(
        self,
        provider_job_id: str,
        request_snapshot: dict[str, Any],
    ) -> MockExecutionResult:
        self.execute_count += 1
        if self.outcome == MockOutcome.success:
            result_bytes = read_mock_result_fixture()
            return MockExecutionResult(
                outcome=self.outcome,
                normalized_status="SUCCEEDED",
                provider_job_id=provider_job_id,
                content_type="video/mp4",
                result_bytes=result_bytes,
                raw_payload={
                    "provider": "mock",
                    "outcome": "success",
                    "fixture": "mock_result.mp4",
                },
            )
        if self.outcome == MockOutcome.failed:
            return MockExecutionResult(
                outcome=self.outcome,
                normalized_status="FAILED",
                provider_job_id=provider_job_id,
                error_code="MOCK_PROVIDER_FAILED",
                raw_payload={"provider": "mock", "outcome": "failed"},
            )
        if self.outcome == MockOutcome.unknown:
            return MockExecutionResult(
                outcome=self.outcome,
                normalized_status="UNKNOWN_PROVIDER_STATE",
                provider_job_id=provider_job_id,
                raw_payload={"provider": "mock", "outcome": "unknown"},
            )
        return MockExecutionResult(
            outcome=self.outcome,
            normalized_status="CANCELLED",
            provider_job_id=provider_job_id,
            raw_payload={"provider": "mock", "outcome": "cancel"},
        )


def read_mock_result_fixture() -> bytes:
    return (
        resources.files("app.providers.fixtures")
        .joinpath("mock_result.mp4")
        .read_bytes()
    )
