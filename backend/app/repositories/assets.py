"""Asset persistence repository."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.types import AssetKind, AssetStatus, generate_prefixed_id
from app.idempotency.types import ensure_utc
from app.models.asset import Asset

SessionFactory = Callable[[], Session]


@dataclass(frozen=True)
class AssetSnapshot:
    asset_id: str
    owner_id: str
    asset_kind: AssetKind
    status: AssetStatus
    content_type: str
    size_bytes: int
    checksum_sha256: str
    storage_path: Optional[str]
    upload_token_hash: Optional[str]
    upload_token_expires_at: Optional[datetime]
    upload_token_used_at: Optional[datetime]
    deleted_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class AssetRepository:
    """Owns database operations for assets only."""

    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def create_pending_upload(
        self,
        *,
        owner_id: str,
        asset_kind: AssetKind,
        content_type: str,
        size_bytes: int,
        checksum_sha256: str,
        upload_token_hash: str,
        upload_token_expires_at: datetime,
        now: datetime,
    ) -> AssetSnapshot:
        with self._session_factory() as session:
            asset = Asset(
                asset_id=generate_prefixed_id("asset"),
                owner_id=owner_id,
                asset_kind=asset_kind,
                status=AssetStatus.PENDING_UPLOAD,
                content_type=content_type,
                size_bytes=size_bytes,
                checksum_sha256=checksum_sha256,
                upload_token_hash=upload_token_hash,
                upload_token_expires_at=upload_token_expires_at,
                created_at=now,
                updated_at=now,
            )
            session.add(asset)
            session.commit()
            session.refresh(asset)
            return _snapshot(asset)

    def get_by_id_and_owner(
        self, *, asset_id: str, owner_id: str
    ) -> Optional[AssetSnapshot]:
        with self._session_factory() as session:
            asset = session.scalar(
                select(Asset).where(Asset.asset_id == asset_id, Asset.owner_id == owner_id)
            )
            return _snapshot(asset) if asset is not None else None

    def get_by_id(self, asset_id: str) -> Optional[AssetSnapshot]:
        with self._session_factory() as session:
            asset = session.get(Asset, asset_id)
            return _snapshot(asset) if asset is not None else None

    def get_by_upload_token_hash(
        self, upload_token_hash: str
    ) -> Optional[AssetSnapshot]:
        with self._session_factory() as session:
            asset = session.scalar(
                select(Asset).where(Asset.upload_token_hash == upload_token_hash)
            )
            return _snapshot(asset) if asset is not None else None

    def mark_ready(
        self,
        *,
        asset_id: str,
        storage_path: str,
        upload_token_used_at: datetime,
    ) -> AssetSnapshot:
        with self._session_factory() as session:
            asset = session.get(Asset, asset_id)
            if asset is None:
                raise ValueError("Asset not found.")
            if asset.status != AssetStatus.PENDING_UPLOAD:
                raise ValueError("Only PENDING_UPLOAD assets can be marked READY.")
            if asset.upload_token_used_at is not None:
                raise ValueError("Upload token already used.")
            asset.status = AssetStatus.READY
            asset.storage_path = storage_path
            asset.upload_token_used_at = upload_token_used_at
            asset.updated_at = upload_token_used_at
            session.commit()
            session.refresh(asset)
            return _snapshot(asset)


def _snapshot(asset: Asset) -> AssetSnapshot:
    return AssetSnapshot(
        asset_id=asset.asset_id,
        owner_id=asset.owner_id,
        asset_kind=asset.asset_kind,
        status=asset.status,
        content_type=asset.content_type,
        size_bytes=asset.size_bytes,
        checksum_sha256=asset.checksum_sha256,
        storage_path=asset.storage_path,
        upload_token_hash=asset.upload_token_hash,
        upload_token_expires_at=(
            ensure_utc(asset.upload_token_expires_at)
            if asset.upload_token_expires_at is not None
            else None
        ),
        upload_token_used_at=(
            ensure_utc(asset.upload_token_used_at)
            if asset.upload_token_used_at is not None
            else None
        ),
        deleted_at=ensure_utc(asset.deleted_at) if asset.deleted_at is not None else None,
        created_at=ensure_utc(asset.created_at),
        updated_at=ensure_utc(asset.updated_at),
    )
