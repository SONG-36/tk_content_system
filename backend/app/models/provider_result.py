"""Provider result ORM model."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import ProviderNormalizedStatus, enum_column, utc_now


class ProviderResult(Base):
    __tablename__ = "provider_results"

    provider_result_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    attempt_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("job_attempts.attempt_id"), nullable=False, unique=True
    )
    normalized_status: Mapped[ProviderNormalizedStatus] = mapped_column(
        enum_column(ProviderNormalizedStatus, "provider_normalized_status"),
        nullable=False,
    )
    result_asset_ids_json: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    raw_payload_json: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
