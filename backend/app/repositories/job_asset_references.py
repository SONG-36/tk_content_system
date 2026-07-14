"""Job asset reference persistence repository."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.types import generate_prefixed_id
from app.idempotency.types import ensure_utc
from app.models.job_asset_reference import JobAssetReference
from app.schemas.jobs import ReferenceAsset

SessionFactory = Callable[[], Session]


@dataclass(frozen=True)
class JobAssetReferenceSnapshot:
    job_asset_reference_id: str
    job_id: str
    asset_id: str
    usage_role: str
    shot_number: str
    linked_proof_need_ids_json: list[str]
    required_for_truth_gate: bool
    preservation_locks_json: dict[str, Any]
    created_at: datetime


class JobAssetReferenceRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def create_many(
        self,
        session: Session,
        *,
        job_id: str,
        references: list[ReferenceAsset],
        now: datetime,
    ) -> list[JobAssetReferenceSnapshot]:
        created: list[JobAssetReferenceSnapshot] = []
        for reference in references:
            row = JobAssetReference(
                job_asset_reference_id=generate_prefixed_id("job_asset_ref"),
                job_id=job_id,
                asset_id=reference.asset_id,
                usage_role=reference.usage_role.value,
                shot_number=reference.shot_number,
                linked_proof_need_ids_json=list(reference.linked_proof_need_ids),
                required_for_truth_gate=reference.required_for_truth_gate,
                preservation_locks_json=reference.preservation_locks.model_dump(
                    mode="json"
                ),
                created_at=now,
            )
            session.add(row)
            session.flush()
            created.append(_snapshot(row))
        return created

    def list_for_job(self, job_id: str) -> list[JobAssetReferenceSnapshot]:
        with self._session_factory() as session:
            rows = session.scalars(
                select(JobAssetReference).where(JobAssetReference.job_id == job_id)
            ).all()
            return [_snapshot(row) for row in rows]


def _snapshot(row: JobAssetReference) -> JobAssetReferenceSnapshot:
    return JobAssetReferenceSnapshot(
        job_asset_reference_id=row.job_asset_reference_id,
        job_id=row.job_id,
        asset_id=row.asset_id,
        usage_role=row.usage_role,
        shot_number=row.shot_number,
        linked_proof_need_ids_json=row.linked_proof_need_ids_json,
        required_for_truth_gate=row.required_for_truth_gate,
        preservation_locks_json=row.preservation_locks_json,
        created_at=ensure_utc(row.created_at),
    )
