"""Asset ORM model."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import AssetKind, AssetStatus, enum_column, utc_now


class Asset(Base):
    __tablename__ = "assets"
    __table_args__ = (Index("ix_assets_owner_id", "owner_id"),)

    asset_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    owner_id: Mapped[str] = mapped_column(String(128), nullable=False)
    asset_kind: Mapped[AssetKind] = mapped_column(
        enum_column(AssetKind, "asset_kind"), nullable=False
    )
    status: Mapped[AssetStatus] = mapped_column(
        enum_column(AssetStatus, "asset_status"), nullable=False
    )
    content_type: Mapped[str] = mapped_column(String(255), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    checksum_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    storage_path: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    upload_token_hash: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    upload_token_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    upload_token_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    result_token_hash: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    result_token_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
