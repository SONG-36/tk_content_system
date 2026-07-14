"""Job attempt ORM model."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import AttemptStatus, enum_column, utc_now


class JobAttempt(Base):
    __tablename__ = "job_attempts"
    __table_args__ = (
        UniqueConstraint("job_id", "attempt_no", name="uq_job_attempts_job_attempt_no"),
        Index("ix_job_attempts_job_id", "job_id"),
    )

    attempt_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    job_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("video_jobs.job_id"), nullable=False
    )
    attempt_no: Mapped[int] = mapped_column(Integer, nullable=False)
    execution_provider: Mapped[str] = mapped_column(String(64), nullable=False)
    provider_model: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    provider_job_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    attempt_status: Mapped[AttemptStatus] = mapped_column(
        enum_column(AttemptStatus, "attempt_status"), nullable=False
    )
    cancellation_intent: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    cancel_requested_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error_code: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    submitted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    terminal_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )
