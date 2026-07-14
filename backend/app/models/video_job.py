"""Video job ORM model."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import AIReviewStatus, GenerationStatus, enum_column, utc_now


class VideoJob(Base):
    __tablename__ = "video_jobs"
    __table_args__ = (
        Index("ix_video_jobs_owner_id", "owner_id"),
        Index("ix_video_jobs_current_attempt_id", "current_attempt_id"),
    )

    job_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    owner_id: Mapped[str] = mapped_column(String(128), nullable=False)
    contract_version: Mapped[str] = mapped_column(String(32), nullable=False)
    truth_rule_version: Mapped[str] = mapped_column(String(64), nullable=False)
    provider_mapping_version: Mapped[str] = mapped_column(String(64), nullable=False)
    selected_model: Mapped[str] = mapped_column(String(64), nullable=False)
    execution_provider: Mapped[str] = mapped_column(String(64), nullable=False)
    generation_status: Mapped[GenerationStatus] = mapped_column(
        enum_column(GenerationStatus, "generation_status"), nullable=False
    )
    ai_review_status: Mapped[AIReviewStatus] = mapped_column(
        enum_column(AIReviewStatus, "ai_review_status"), nullable=False
    )
    current_attempt_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )
