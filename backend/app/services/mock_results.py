"""Internal mock result download service."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from app.config import Settings
from app.db.types import AssetKind, AssetStatus
from app.idempotency.repository import SessionFactory
from app.idempotency.types import Clock
from app.repositories.assets import AssetRepository
from app.services.errors import InternalServerError, ResultNotReadyError
from app.services.result_tokens import ResultTokenService
from app.storage.local_mock import LocalMockStorage


class MockResultService:
    """Validates signed result tokens and resolves safe local result files."""

    def __init__(
        self,
        *,
        settings: Settings,
        session_factory: SessionFactory,
        clock: Optional[Clock] = None,
        assets: Optional[AssetRepository] = None,
        storage: Optional[LocalMockStorage] = None,
        result_tokens: Optional[ResultTokenService] = None,
    ) -> None:
        self._settings = settings
        self._assets = assets or AssetRepository(session_factory)
        self._storage = storage or LocalMockStorage(settings.mock_storage_directory)
        self._result_tokens = result_tokens or ResultTokenService(
            settings=settings,
            clock=clock,
        )

    def resolve_result_file(self, token: str) -> tuple[Path, str]:
        payload = self._result_tokens.verify(token)
        asset = self._assets.get_result_asset_by_id_and_owner(
            asset_id=payload.asset_id,
            owner_id=payload.owner_id,
        )
        if (
            asset is None
            or asset.asset_kind != AssetKind.RESULT_MEDIA
            or asset.status != AssetStatus.READY
            or asset.content_type != "video/mp4"
            or asset.storage_path is None
            or asset.deleted_at is not None
        ):
            raise ResultNotReadyError()
        try:
            path = self._storage.resolve_result_path(asset.storage_path)
        except ValueError as exc:
            raise InternalServerError() from exc
        if not path.exists() or not path.is_file():
            raise InternalServerError()
        return path, asset.content_type
