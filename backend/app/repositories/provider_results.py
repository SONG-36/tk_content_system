"""Provider result persistence repository."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.types import ProviderNormalizedStatus, generate_prefixed_id
from app.idempotency.types import ensure_utc
from app.models.provider_result import ProviderResult

SessionFactory = Callable[[], Session]


@dataclass(frozen=True)
class ProviderResultSnapshot:
    provider_result_id: str
    attempt_id: str
    normalized_status: ProviderNormalizedStatus
    result_asset_ids_json: list[str]
    raw_payload_json: Optional[dict[str, Any]]
    created_at: datetime


class ProviderResultRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def create_success_result(
        self,
        session: Session,
        *,
        attempt_id: str,
        result_asset_ids: list[str],
        raw_payload: dict[str, Any],
        now: datetime,
    ) -> ProviderResultSnapshot:
        provider_result = ProviderResult(
            provider_result_id=generate_prefixed_id("pr"),
            attempt_id=attempt_id,
            normalized_status=ProviderNormalizedStatus.SUCCEEDED,
            result_asset_ids_json=result_asset_ids,
            raw_payload_json=raw_payload,
            created_at=now,
        )
        session.add(provider_result)
        session.flush()
        return _snapshot(provider_result)

    def get_by_attempt_id(self, attempt_id: str) -> Optional[ProviderResultSnapshot]:
        with self._session_factory() as session:
            provider_result = session.scalar(
                select(ProviderResult).where(ProviderResult.attempt_id == attempt_id)
            )
            return _snapshot(provider_result) if provider_result is not None else None

    def list_result_asset_ids(self, attempt_id: str) -> list[str]:
        result = self.get_by_attempt_id(attempt_id)
        return result.result_asset_ids_json if result is not None else []


def _snapshot(provider_result: ProviderResult) -> ProviderResultSnapshot:
    return ProviderResultSnapshot(
        provider_result_id=provider_result.provider_result_id,
        attempt_id=provider_result.attempt_id,
        normalized_status=provider_result.normalized_status,
        result_asset_ids_json=provider_result.result_asset_ids_json,
        raw_payload_json=provider_result.raw_payload_json,
        created_at=ensure_utc(provider_result.created_at),
    )
