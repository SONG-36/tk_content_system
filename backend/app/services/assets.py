"""Asset upload URL and internal mock upload service."""

from __future__ import annotations

import hashlib
from datetime import timedelta
from typing import Optional

from app.config import Settings
from app.db.types import AssetKind, AssetStatus
from app.idempotency import (
    IdempotencyDisposition,
    IdempotencyService,
    RecoveryResult,
    RecoveryStatus,
)
from app.idempotency.types import Clock, UtcClock, ensure_utc
from app.repositories.assets import AssetRepository, AssetSnapshot, SessionFactory
from app.schemas.assets import InternalUploadResponse, UploadUrlRequest, UploadUrlResponse
from app.schemas.enums import UsageRole
from app.services.errors import (
    AssetInvalidStateError,
    AssetTooLargeError,
    AssetTypeUnsupportedError,
    ChecksumMismatchError,
    InternalServerError,
    SchemaInvalidError,
    UploadAlreadyCompletedError,
    UploadTokenExpiredError,
    UploadTokenInvalidError,
)
from app.services.upload_tokens import generate_upload_token, hash_upload_token
from app.storage.local_mock import LocalMockStorage

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "video/mp4"}
INPUT_MEDIA_ROLES = {
    UsageRole.PRODUCT_IDENTITY,
    UsageRole.FIRST_FRAME,
    UsageRole.LAST_FRAME,
    UsageRole.SOURCE_CLIP,
}


class AssetUploadRecoveryResolver:
    """Prevents duplicate asset creation for expired PENDING idempotency records."""

    def __init__(self, *, repository: AssetRepository, clock: Clock) -> None:
        self._repository = repository
        self._clock = clock

    def recover(self, resource_type: str, resource_id: str) -> RecoveryResult:
        if resource_type != "asset":
            return RecoveryResult(status=RecoveryStatus.INCOMPLETE)
        asset = self._repository.get_by_id(resource_id)
        if asset is None:
            return RecoveryResult(status=RecoveryStatus.NOT_FOUND)
        if (
            asset.status == AssetStatus.PENDING_UPLOAD
            and asset.upload_token_expires_at is not None
            and ensure_utc(asset.upload_token_expires_at) > ensure_utc(self._clock.now())
        ):
            # The raw token is intentionally not persisted, so the original URL
            # cannot be reconstructed after a crash before complete().
            return RecoveryResult(status=RecoveryStatus.INCOMPLETE)
        return RecoveryResult(status=RecoveryStatus.NOT_FOUND)


class AssetService:
    """Coordinates asset upload URLs, local uploads, and idempotency."""

    def __init__(
        self,
        *,
        settings: Settings,
        session_factory: SessionFactory,
        clock: Optional[Clock] = None,
        repository: Optional[AssetRepository] = None,
        storage: Optional[LocalMockStorage] = None,
        idempotency_service: Optional[IdempotencyService] = None,
    ) -> None:
        self._settings = settings
        self._clock = clock or UtcClock()
        self._repository = repository or AssetRepository(session_factory)
        self._storage = storage or LocalMockStorage(settings.mock_storage_directory)
        self._idempotency = idempotency_service or IdempotencyService(
            session_factory=session_factory,
            clock=self._clock,
            completed_ttl_hours=settings.idempotency_completed_ttl_hours,
            pending_lease_seconds=settings.idempotency_pending_lease_seconds,
            recovery_resolver=AssetUploadRecoveryResolver(
                repository=self._repository,
                clock=self._clock,
            ),
        )

    def request_upload_url(
        self,
        *,
        owner_id: str,
        request: UploadUrlRequest,
        idempotency_key: Optional[str],
    ) -> UploadUrlResponse:
        acquired = self._idempotency.acquire(
            owner_id=owner_id,
            http_method="POST",
            route_template="/v1/assets/upload-url",
            path_params={},
            request_body=request.model_dump(mode="json"),
            idempotency_key=idempotency_key,
        )
        if acquired.disposition == IdempotencyDisposition.REPLAY:
            return UploadUrlResponse.model_validate(acquired.response_json)

        self._validate_upload_request(request)
        now = ensure_utc(self._clock.now())
        token = generate_upload_token(self._settings.upload_token_bytes)
        token_hash = hash_upload_token(token)
        token_expires_at = now + timedelta(
            hours=self._settings.mock_upload_token_ttl_hours
        )
        asset = self._repository.create_pending_upload(
            owner_id=owner_id,
            asset_kind=_asset_kind_for_role(request.intended_usage_role),
            content_type=request.content_type,
            size_bytes=request.size_bytes,
            checksum_sha256=request.checksum_sha256,
            upload_token_hash=token_hash,
            upload_token_expires_at=token_expires_at,
            now=now,
        )
        self._idempotency.bind_resource(
            record_id=acquired.record_id,
            resource_type="asset",
            resource_id=asset.asset_id,
        )
        response = UploadUrlResponse(
            asset_id=asset.asset_id,
            upload_url=_build_upload_url(self._settings.public_base_url, token),
            upload_url_expires_at=token_expires_at,
            idempotent_replay=False,
        )
        self._idempotency.complete(
            record_id=acquired.record_id,
            response_status_code=201,
            response_json=response.model_dump(mode="json"),
            resource_type="asset",
            resource_id=asset.asset_id,
        )
        return response

    def complete_mock_upload(
        self,
        *,
        token: str,
        content_type: Optional[str],
        body: bytes,
    ) -> InternalUploadResponse:
        now = ensure_utc(self._clock.now())
        asset = self._repository.get_by_upload_token_hash(hash_upload_token(token))
        if asset is None:
            raise UploadTokenInvalidError()
        if asset.upload_token_expires_at is None or asset.upload_token_expires_at <= now:
            raise UploadTokenExpiredError()
        if asset.upload_token_used_at is not None:
            raise UploadAlreadyCompletedError()
        if asset.status != AssetStatus.PENDING_UPLOAD:
            raise AssetInvalidStateError()
        if content_type is None or content_type.strip() == "":
            raise SchemaInvalidError(
                "Content-Type header is required.",
                field="Content-Type",
                required_action="Provide the declared Content-Type header.",
            )
        if content_type != asset.content_type:
            raise AssetTypeUnsupportedError(
                "Uploaded Content-Type does not match the asset declaration.",
                field="Content-Type",
                required_action="Upload bytes with the declared Content-Type.",
            )
        if len(body) > self._settings.max_asset_size_bytes:
            raise AssetTooLargeError()
        if len(body) != asset.size_bytes:
            raise SchemaInvalidError(
                "Uploaded byte length does not match the asset declaration.",
                field="size_bytes",
                required_action="Upload bytes matching the declared size_bytes.",
            )
        checksum = hashlib.sha256(body).hexdigest()
        if checksum != asset.checksum_sha256:
            raise ChecksumMismatchError()

        storage_path: Optional[str] = None
        try:
            storage_path = self._storage.write_atomic(
                asset_id=asset.asset_id,
                content_type=asset.content_type,
                data=body,
            )
        except Exception as exc:
            raise InternalServerError("Failed to write mock upload file.") from exc

        try:
            ready = self._repository.mark_ready(
                asset_id=asset.asset_id,
                storage_path=storage_path,
                upload_token_used_at=now,
            )
        except ValueError as exc:
            self._storage.delete(storage_path)
            raise AssetInvalidStateError() from exc
        except Exception as exc:
            self._storage.delete(storage_path)
            raise InternalServerError("Failed to persist uploaded asset.") from exc

        return InternalUploadResponse(
            asset_id=ready.asset_id,
            content_type=ready.content_type,
            size_bytes=ready.size_bytes,
            checksum_sha256=ready.checksum_sha256,
        )

    def _validate_upload_request(self, request: UploadUrlRequest) -> None:
        if request.content_type not in ALLOWED_CONTENT_TYPES:
            raise AssetTypeUnsupportedError()
        if request.size_bytes > self._settings.max_asset_size_bytes:
            raise AssetTooLargeError()


def _asset_kind_for_role(role: UsageRole) -> AssetKind:
    return AssetKind.INPUT_MEDIA if role in INPUT_MEDIA_ROLES else AssetKind.REFERENCE


def _build_upload_url(public_base_url: str, token: str) -> str:
    return f"{public_base_url.rstrip('/')}/_internal/mock-uploads/{token}"
