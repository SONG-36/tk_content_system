"""Idempotency record ORM model."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, Index, Integer, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import IdempotencyStatus, enum_column, utc_now


class IdempotencyRecord(Base):
    __tablename__ = "idempotency_records"
    __table_args__ = (
        UniqueConstraint(
            "owner_id",
            "http_method",
            "route_template",
            "path_params_hash",
            "idempotency_key_hash",
            name="uq_idempotency_scope",
        ),
        Index("ix_idempotency_records_owner_id", "owner_id"),
    )

    idempotency_record_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    owner_id: Mapped[str] = mapped_column(String(128), nullable=False)
    http_method: Mapped[str] = mapped_column(String(16), nullable=False)
    route_template: Mapped[str] = mapped_column(String(255), nullable=False)
    path_params_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    idempotency_key_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    canonical_request_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[IdempotencyStatus] = mapped_column(
        enum_column(IdempotencyStatus, "idempotency_status"), nullable=False
    )
    lease_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    response_status_code: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    response_json: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    resource_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    resource_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )
