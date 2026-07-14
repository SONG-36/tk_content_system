"""Generation request snapshot persistence repository."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.types import generate_prefixed_id
from app.idempotency.types import ensure_utc
from app.models.generation_request_snapshot import GenerationRequestSnapshot

SessionFactory = Callable[[], Session]


@dataclass(frozen=True)
class GenerationRequestSnapshotView:
    snapshot_id: str
    job_id: str
    canonical_request_hash: str
    request_json: dict[str, Any]
    gate_result_json: dict[str, Any]
    created_at: datetime


class GenerationRequestSnapshotRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def create_snapshot(
        self,
        session: Session,
        *,
        job_id: str,
        canonical_request_hash: str,
        request_json: dict[str, Any],
        gate_result_json: dict[str, Any],
        now: datetime,
    ) -> GenerationRequestSnapshotView:
        snapshot = GenerationRequestSnapshot(
            snapshot_id=generate_prefixed_id("snapshot"),
            job_id=job_id,
            canonical_request_hash=canonical_request_hash,
            request_json=request_json,
            gate_result_json=gate_result_json,
            created_at=now,
        )
        session.add(snapshot)
        session.flush()
        return _snapshot(snapshot)

    def get_by_job_id(self, job_id: str) -> Optional[GenerationRequestSnapshotView]:
        with self._session_factory() as session:
            snapshot = session.scalar(
                select(GenerationRequestSnapshot).where(
                    GenerationRequestSnapshot.job_id == job_id
                )
            )
            return _snapshot(snapshot) if snapshot is not None else None


def _snapshot(
    snapshot: GenerationRequestSnapshot,
) -> GenerationRequestSnapshotView:
    return GenerationRequestSnapshotView(
        snapshot_id=snapshot.snapshot_id,
        job_id=snapshot.job_id,
        canonical_request_hash=snapshot.canonical_request_hash,
        request_json=snapshot.request_json,
        gate_result_json=snapshot.gate_result_json,
        created_at=ensure_utc(snapshot.created_at),
    )
