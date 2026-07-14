"""Job asset reference ORM model."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import utc_now


class JobAssetReference(Base):
    __tablename__ = "job_asset_references"
    __table_args__ = (
        UniqueConstraint(
            "job_id",
            "asset_id",
            "usage_role",
            "shot_number",
            name="uq_job_asset_references_job_asset_role_shot",
        ),
        Index("ix_job_asset_references_job_id", "job_id"),
        Index("ix_job_asset_references_asset_id", "asset_id"),
    )

    job_asset_reference_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    job_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("video_jobs.job_id"), nullable=False
    )
    asset_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("assets.asset_id"), nullable=False
    )
    usage_role: Mapped[str] = mapped_column(String(64), nullable=False)
    shot_number: Mapped[str] = mapped_column(String(64), nullable=False)
    linked_proof_need_ids_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    required_for_truth_gate: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    preservation_locks_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
