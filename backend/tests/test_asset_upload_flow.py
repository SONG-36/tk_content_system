from __future__ import annotations

import hashlib
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import sessionmaker

from app.config import Settings
from app.db.base import Base, import_models
from app.db.session import create_db_engine
from app.db.types import AssetKind, AssetStatus
from app.idempotency import FakeClock, IdempotencyService
from app.idempotency.types import ensure_utc
from app.main import create_app
from app.models.asset import Asset
from app.repositories.assets import AssetRepository
from app.schemas.assets import UploadUrlRequest
from app.schemas.enums import UsageRole
from app.services.assets import AssetService, AssetUploadRecoveryResolver
from app.services.errors import IdempotencyPendingError, InternalServerError
from app.services.upload_tokens import generate_upload_token, hash_upload_token
from app.storage.local_mock import LocalMockStorage


APPROVED_TABLES = {
    "assets",
    "video_jobs",
    "job_attempts",
    "generation_request_snapshots",
    "job_asset_references",
    "provider_results",
    "idempotency_records",
}


def settings_for(tmp_path: Path, *, max_size: int = 1024) -> Settings:
    return Settings(
        api_key="secret",
        owner_id="owner_from_server",
        database_url=f"sqlite:///{tmp_path / 'asset-flow.db'}",
        public_base_url="http://testserver",
        mock_storage_directory=str(tmp_path / "mock-storage"),
        max_asset_size_bytes=max_size,
    )


def prepare_database(settings: Settings):
    engine = create_db_engine(settings.database_url)
    import_models()
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def client_for(tmp_path: Path, *, max_size: int = 1024):
    settings = settings_for(tmp_path, max_size=max_size)
    SessionLocal = prepare_database(settings)
    app = create_app(settings_override=settings)
    return TestClient(app), settings, SessionLocal


def upload_payload(data: bytes = b"hello") -> dict[str, Any]:
    return {
        "contract_version": "v1",
        "content_type": "image/png",
        "size_bytes": len(data),
        "checksum_sha256": hashlib.sha256(data).hexdigest(),
        "intended_usage_role": "PRODUCT_IDENTITY",
    }


def auth_headers(key: str = "idem-key") -> dict[str, str]:
    return {"Authorization": "Bearer secret", "Idempotency-Key": key}


def token_from_upload_url(upload_url: str) -> str:
    return Path(urlparse(upload_url).path).name


def asset_count(SessionLocal) -> int:
    with SessionLocal() as session:
        return session.scalar(select(func.count()).select_from(Asset))


def get_asset(SessionLocal, asset_id: str) -> Asset:
    with SessionLocal() as session:
        asset = session.get(Asset, asset_id)
        assert asset is not None
        session.expunge(asset)
        return asset


def test_upload_url_requires_authentication(tmp_path: Path) -> None:
    client, _, _ = client_for(tmp_path)

    response = client.post(
        "/v1/assets/upload-url",
        json=upload_payload(),
        headers={"Idempotency-Key": "key"},
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTH_REQUIRED"


def test_upload_url_rejects_invalid_api_key(tmp_path: Path) -> None:
    client, _, _ = client_for(tmp_path)

    response = client.post(
        "/v1/assets/upload-url",
        json=upload_payload(),
        headers={"Authorization": "Bearer wrong", "Idempotency-Key": "key"},
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTH_INVALID"


def test_upload_url_requires_idempotency_key(tmp_path: Path) -> None:
    client, _, _ = client_for(tmp_path)

    response = client.post(
        "/v1/assets/upload-url",
        json=upload_payload(),
        headers={"Authorization": "Bearer secret"},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "IDEMPOTENCY_KEY_REQUIRED"


def test_upload_url_invalid_content_type_uses_error_envelope(tmp_path: Path) -> None:
    client, _, _ = client_for(tmp_path)
    payload = upload_payload()
    payload["content_type"] = "application/pdf"

    response = client.post(
        "/v1/assets/upload-url",
        json=payload,
        headers=auth_headers(),
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "SCHEMA_INVALID"


def test_upload_url_rejects_oversize_asset(tmp_path: Path) -> None:
    client, _, _ = client_for(tmp_path, max_size=4)

    response = client.post(
        "/v1/assets/upload-url",
        json=upload_payload(b"hello"),
        headers=auth_headers(),
    )

    assert response.status_code == 413
    assert response.json()["error"]["code"] == "ASSET_TOO_LARGE"


def test_upload_url_creates_pending_asset_and_hashes_token(tmp_path: Path) -> None:
    client, settings, SessionLocal = client_for(tmp_path)

    response = client.post(
        "/v1/assets/upload-url",
        json=upload_payload(),
        headers=auth_headers(),
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["asset_id"].startswith("asset_")
    assert payload["asset_status"] == "PENDING_UPLOAD"
    assert payload["upload_url"].startswith("http://testserver/_internal/mock-uploads/")
    assert payload["idempotent_replay"] is False
    token = token_from_upload_url(payload["upload_url"])
    asset = get_asset(SessionLocal, payload["asset_id"])
    assert asset.owner_id == "owner_from_server"
    assert asset.status == AssetStatus.PENDING_UPLOAD
    assert asset.asset_kind == AssetKind.INPUT_MEDIA
    assert asset.upload_token_hash == hash_upload_token(token)
    assert asset.upload_token_hash != token
    assert token not in str(asset.storage_path)
    assert settings.mock_storage_directory not in payload["upload_url"]


def test_upload_url_replay_returns_same_asset(tmp_path: Path) -> None:
    client, _, SessionLocal = client_for(tmp_path)

    first = client.post(
        "/v1/assets/upload-url",
        json=upload_payload(),
        headers=auth_headers("same-key"),
    )
    second = client.post(
        "/v1/assets/upload-url",
        json=upload_payload(),
        headers=auth_headers("same-key"),
    )

    assert first.status_code == 201
    assert second.status_code == 201
    assert second.json()["asset_id"] == first.json()["asset_id"]
    assert second.json()["idempotent_replay"] is True
    assert asset_count(SessionLocal) == 1


def test_upload_url_same_key_different_payload_conflicts(tmp_path: Path) -> None:
    client, _, _ = client_for(tmp_path)
    first_payload = upload_payload(b"hello")
    second_payload = upload_payload(b"world!")

    assert client.post(
        "/v1/assets/upload-url",
        json=first_payload,
        headers=auth_headers("conflict-key"),
    ).status_code == 201
    response = client.post(
        "/v1/assets/upload-url",
        json=second_payload,
        headers=auth_headers("conflict-key"),
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "IDEMPOTENCY_CONFLICT"


def test_concurrent_same_scope_creates_one_asset(tmp_path: Path) -> None:
    client, _, SessionLocal = client_for(tmp_path)

    def post_once() -> int:
        return client.post(
            "/v1/assets/upload-url",
            json=upload_payload(),
            headers=auth_headers("race-key"),
        ).status_code

    with ThreadPoolExecutor(max_workers=2) as executor:
        statuses = list(executor.map(lambda _: post_once(), range(2)))

    assert asset_count(SessionLocal) == 1
    assert sorted(statuses) in ([201, 201], [201, 409])


def test_expired_pending_bound_asset_does_not_create_second_asset(
    tmp_path: Path,
) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    clock = FakeClock(
        ensure_utc(__import__("datetime").datetime(2026, 7, 14, 12, 0))
    )
    repo = AssetRepository(SessionLocal)
    resolver = AssetUploadRecoveryResolver(repository=repo, clock=clock)
    idem = IdempotencyService(
        session_factory=SessionLocal,
        clock=clock,
        recovery_resolver=resolver,
    )
    service = AssetService(
        settings=settings,
        session_factory=SessionLocal,
        clock=clock,
        repository=repo,
        idempotency_service=idem,
    )
    request = UploadUrlRequest.model_validate(upload_payload())
    acquired = idem.acquire(
        owner_id=settings.owner_id,
        http_method="POST",
        route_template="/v1/assets/upload-url",
        path_params={},
        request_body=request.model_dump(mode="json"),
        idempotency_key="expired-pending",
    )
    token = generate_upload_token(settings.upload_token_bytes)
    asset = repo.create_pending_upload(
        owner_id=settings.owner_id,
        asset_kind=AssetKind.INPUT_MEDIA,
        content_type=request.content_type,
        size_bytes=request.size_bytes,
        checksum_sha256=request.checksum_sha256,
        upload_token_hash=hash_upload_token(token),
        upload_token_expires_at=clock.now() + timedelta(hours=24),
        now=clock.now(),
    )
    idem.bind_resource(
        record_id=acquired.record_id,
        resource_type="asset",
        resource_id=asset.asset_id,
    )
    clock.set(clock.now() + timedelta(seconds=61))

    with pytest.raises(IdempotencyPendingError):
        service.request_upload_url(
            owner_id=settings.owner_id,
            request=request,
            idempotency_key="expired-pending",
        )

    assert asset_count(SessionLocal) == 1


def test_internal_upload_route_is_not_in_openapi(tmp_path: Path) -> None:
    client, _, _ = client_for(tmp_path)

    paths = set(client.get("/openapi.json").json()["paths"])

    assert "/health" in paths
    assert "/v1/assets/upload-url" in paths
    assert "/_internal/mock-uploads/{token}" not in paths
    assert not any(path.startswith("/v1/video-jobs") for path in paths)


def test_internal_upload_invalid_token_returns_error_envelope(tmp_path: Path) -> None:
    client, _, _ = client_for(tmp_path)

    response = client.put(
        "/_internal/mock-uploads/not-a-token",
        content=b"hello",
        headers={"Content-Type": "image/png"},
    )

    assert response.status_code == 404
    payload = response.json()
    assert payload["error"]["code"] == "UPLOAD_TOKEN_INVALID"
    assert payload["error"]["request_id"] == response.headers["x-request-id"]
    assert "not-a-token" not in str(payload["error"]["details"])


def create_upload(client: TestClient, data: bytes = b"hello") -> dict[str, Any]:
    response = client.post(
        "/v1/assets/upload-url",
        json=upload_payload(data),
        headers=auth_headers(generate_upload_token(32)),
    )
    assert response.status_code == 201
    return response.json()


def test_internal_upload_expired_token(tmp_path: Path) -> None:
    client, _, SessionLocal = client_for(tmp_path)
    created = create_upload(client)
    token = token_from_upload_url(created["upload_url"])
    with SessionLocal() as session:
        asset = session.get(Asset, created["asset_id"])
        assert asset is not None
        asset.upload_token_expires_at = ensure_utc(asset.upload_token_expires_at) - timedelta(
            hours=25
        )
        session.commit()

    response = client.put(
        f"/_internal/mock-uploads/{token}",
        content=b"hello",
        headers={"Content-Type": "image/png"},
    )

    assert response.status_code == 410
    assert response.json()["error"]["code"] == "UPLOAD_TOKEN_EXPIRED"


def test_internal_upload_rejects_content_type_size_and_checksum_errors(
    tmp_path: Path,
) -> None:
    client, _, SessionLocal = client_for(tmp_path, max_size=4)
    created = create_upload(client, b"abcd")
    token = token_from_upload_url(created["upload_url"])

    content_type = client.put(
        f"/_internal/mock-uploads/{token}",
        content=b"abcd",
        headers={"Content-Type": "video/mp4"},
    )
    size_mismatch = client.put(
        f"/_internal/mock-uploads/{token}",
        content=b"abc",
        headers={"Content-Type": "image/png"},
    )
    checksum = client.put(
        f"/_internal/mock-uploads/{token}",
        content=b"wxyz",
        headers={"Content-Type": "image/png"},
    )
    too_large = client.put(
        f"/_internal/mock-uploads/{token}",
        content=b"abcde",
        headers={"Content-Type": "image/png"},
    )

    assert content_type.status_code == 415
    assert content_type.json()["error"]["code"] == "ASSET_TYPE_UNSUPPORTED"
    assert size_mismatch.status_code == 422
    assert size_mismatch.json()["error"]["code"] == "SCHEMA_INVALID"
    assert checksum.status_code == 422
    assert checksum.json()["error"]["code"] == "CHECKSUM_MISMATCH"
    assert too_large.status_code == 413
    assert too_large.json()["error"]["code"] == "ASSET_TOO_LARGE"
    asset = get_asset(SessionLocal, created["asset_id"])
    assert asset.status == AssetStatus.PENDING_UPLOAD
    assert asset.upload_token_used_at is None


def test_internal_upload_success_for_image_and_video_and_rejects_repeat(
    tmp_path: Path,
) -> None:
    client, _, SessionLocal = client_for(tmp_path)

    for data, content_type in [(b"png-bytes", "image/png"), (b"mp4-bytes", "video/mp4")]:
        payload = {
            "contract_version": "v1",
            "content_type": content_type,
            "size_bytes": len(data),
            "checksum_sha256": hashlib.sha256(data).hexdigest(),
            "intended_usage_role": "SOURCE_CLIP",
        }
        created = client.post(
            "/v1/assets/upload-url",
            json=payload,
            headers=auth_headers(generate_upload_token(32)),
        ).json()
        token = token_from_upload_url(created["upload_url"])
        response = client.put(
            f"/_internal/mock-uploads/{token}",
            content=data,
            headers={"Content-Type": content_type},
        )
        repeat = client.put(
            f"/_internal/mock-uploads/{token}",
            content=data,
            headers={"Content-Type": content_type},
        )

        assert response.status_code == 200
        assert response.json()["asset_status"] == "READY"
        assert repeat.status_code == 409
        assert repeat.json()["error"]["code"] == "UPLOAD_ALREADY_COMPLETED"
        asset = get_asset(SessionLocal, created["asset_id"])
        assert asset.status == AssetStatus.READY
        assert asset.upload_token_used_at is not None
        assert asset.storage_path is not None
        assert token not in asset.storage_path
        assert Path(asset.storage_path).read_bytes() == data


def test_internal_upload_rejects_asset_not_pending(tmp_path: Path) -> None:
    client, _, SessionLocal = client_for(tmp_path)
    created = create_upload(client)
    token = token_from_upload_url(created["upload_url"])
    with SessionLocal() as session:
        asset = session.get(Asset, created["asset_id"])
        assert asset is not None
        asset.status = AssetStatus.FAILED
        session.commit()

    response = client.put(
        f"/_internal/mock-uploads/{token}",
        content=b"hello",
        headers={"Content-Type": "image/png"},
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "ASSET_INVALID_STATE"


def test_local_storage_prevents_path_traversal_and_cleans_temp_files(
    tmp_path: Path,
) -> None:
    storage = LocalMockStorage(str(tmp_path / "storage"))

    with pytest.raises(ValueError):
        storage.path_for(asset_id="../asset_escape", content_type="image/png")
    temp = storage.base_directory / ".asset_1.png.tmp"
    storage.base_directory.mkdir(parents=True)
    temp.write_bytes(b"partial")
    storage.cleanup_temp_files()

    assert not temp.exists()


class FailingStorage(LocalMockStorage):
    def write_atomic(self, *, asset_id: str, content_type: str, data: bytes) -> str:
        raise OSError("disk full")


class FailingMarkReadyRepository(AssetRepository):
    def mark_ready(self, *, asset_id: str, storage_path: str, upload_token_used_at):
        raise RuntimeError("database down")


def test_file_write_failure_does_not_mark_asset_ready(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    service = AssetService(
        settings=settings,
        session_factory=SessionLocal,
        storage=FailingStorage(settings.mock_storage_directory),
    )
    created = service.request_upload_url(
        owner_id=settings.owner_id,
        request=UploadUrlRequest.model_validate(upload_payload()),
        idempotency_key="write-fail",
    )
    token = token_from_upload_url(str(created.upload_url))

    with pytest.raises(InternalServerError):
        service.complete_mock_upload(
            token=token,
            content_type="image/png",
            body=b"hello",
        )

    assert get_asset(SessionLocal, created.asset_id).status == AssetStatus.PENDING_UPLOAD
    assert not list(Path(settings.mock_storage_directory).glob("*"))


def test_database_failure_after_file_write_deletes_final_file(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    normal_repo = AssetRepository(SessionLocal)
    service = AssetService(
        settings=settings,
        session_factory=SessionLocal,
        repository=normal_repo,
    )
    created = service.request_upload_url(
        owner_id=settings.owner_id,
        request=UploadUrlRequest.model_validate(upload_payload()),
        idempotency_key="db-fail",
    )
    token = token_from_upload_url(str(created.upload_url))
    failing_service = AssetService(
        settings=settings,
        session_factory=SessionLocal,
        repository=FailingMarkReadyRepository(SessionLocal),
    )

    with pytest.raises(InternalServerError):
        failing_service.complete_mock_upload(
            token=token,
            content_type="image/png",
            body=b"hello",
        )

    asset = get_asset(SessionLocal, created.asset_id)
    assert asset.status == AssetStatus.PENDING_UPLOAD
    assert not list(Path(settings.mock_storage_directory).glob(f"{created.asset_id}.*"))


def test_database_tables_remain_approved() -> None:
    import_models()

    assert set(Base.metadata.tables) == APPROVED_TABLES
