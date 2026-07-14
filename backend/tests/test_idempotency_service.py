from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base, import_models
from app.db.session import create_db_engine
from app.idempotency import (
    CachePolicy,
    FakeClock,
    IdempotencyDisposition,
    IdempotencyService,
    RecoveryResult,
    RecoveryStatus,
    canonicalize_request,
    hash_idempotency_key,
    validate_idempotency_key,
)
from app.idempotency.types import ensure_utc
from app.main import create_app
from app.models.idempotency_record import IdempotencyRecord
from app.services.errors import (
    IdempotencyConflictError,
    IdempotencyKeyRequiredError,
    IdempotencyPendingError,
)


APPROVED_TABLES = {
    "assets",
    "video_jobs",
    "job_attempts",
    "generation_request_snapshots",
    "job_asset_references",
    "provider_results",
    "idempotency_records",
}


class FakeResolver:
    def __init__(self, result: RecoveryResult) -> None:
        self.result = result
        self.calls: list[tuple[str, str]] = []

    def recover(self, resource_type: str, resource_id: str) -> RecoveryResult:
        self.calls.append((resource_type, resource_id))
        return self.result


def now_utc() -> datetime:
    return datetime(2026, 7, 14, 12, 0, tzinfo=timezone.utc)


def session_factory(tmp_path: Path):
    database_url = f"sqlite:///{tmp_path / 'idempotency.db'}"
    engine = create_db_engine(database_url)
    import_models()
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def make_service(
    tmp_path: Path,
    *,
    clock: Optional[FakeClock] = None,
    resolver: Optional[FakeResolver] = None,
):
    SessionLocal = session_factory(tmp_path)
    service = IdempotencyService(
        session_factory=SessionLocal,
        clock=clock or FakeClock(now_utc()),
        recovery_resolver=resolver,
    )
    return service, SessionLocal


def acquire(
    service: IdempotencyService,
    *,
    key: str = "client-key",
    body: Optional[dict[str, Any]] = None,
    path_params: Optional[dict[str, Any]] = None,
    route_template: str = "/v1/video-jobs",
    owner_id: str = "owner_1",
    method: str = "post",
):
    return service.acquire(
        owner_id=owner_id,
        http_method=method,
        route_template=route_template,
        path_params=path_params or {},
        request_body=body or {"prompt": "clean garage"},
        idempotency_key=key,
    )


def get_record(session: Session, record_id: str) -> IdempotencyRecord:
    record = session.get(IdempotencyRecord, record_id)
    assert record is not None
    return record


@pytest.mark.parametrize("key", [None, "", "   "])
def test_idempotency_key_missing_or_blank_rejected(key: Optional[str]) -> None:
    with pytest.raises(IdempotencyKeyRequiredError):
        validate_idempotency_key(key)


def test_idempotency_key_too_long_rejected() -> None:
    with pytest.raises(IdempotencyKeyRequiredError):
        validate_idempotency_key("x" * 256)


def test_idempotency_key_control_character_rejected() -> None:
    with pytest.raises(IdempotencyKeyRequiredError):
        validate_idempotency_key("abc\n123")


def test_database_stores_hash_not_raw_key(tmp_path: Path) -> None:
    service, SessionLocal = make_service(tmp_path)
    raw_key = "never-store-this-key"

    result = acquire(service, key=raw_key)

    with SessionLocal() as session:
        record = get_record(session, result.record_id)
        assert record.idempotency_key_hash == hash_idempotency_key(raw_key)
        assert record.idempotency_key_hash != raw_key


def test_canonical_object_key_order_and_json_whitespace_are_stable() -> None:
    left = canonicalize_request(
        owner_id="owner_1",
        http_method="post",
        route_template="/v1/video-jobs",
        path_params={},
        request_body='{"b": 2, "a": 1}',
    )
    right = canonicalize_request(
        owner_id="owner_1",
        http_method="POST",
        route_template="/v1/video-jobs",
        path_params={},
        request_body='{ "a" : 1 , "b" : 2 }',
    )

    assert left.canonical_json == right.canonical_json
    assert left.canonical_request_hash == right.canonical_request_hash


@pytest.mark.parametrize(
    "changed",
    [
        {"request_body": {"items": [2, 1]}},
        {"owner_id": "owner_2"},
        {"http_method": "PUT"},
        {"route_template": "/v1/assets/upload-url"},
        {"path_params": {"job_id": "job_2"}},
        {"request_body": {"items": [1, 2], "extra": True}},
    ],
)
def test_canonical_request_hash_changes_for_semantic_differences(
    changed: dict[str, Any]
) -> None:
    base_kwargs: dict[str, Any] = {
        "owner_id": "owner_1",
        "http_method": "POST",
        "route_template": "/v1/video-jobs/{job_id}/cancel",
        "path_params": {"job_id": "job_1"},
        "request_body": {"items": [1, 2]},
    }
    base = canonicalize_request(**base_kwargs)
    modified = canonicalize_request(**{**base_kwargs, **changed})

    assert base.canonical_request_hash != modified.canonical_request_hash


def test_path_params_hash_uses_sorted_params() -> None:
    left = canonicalize_request(
        owner_id="owner_1",
        http_method="POST",
        route_template="/v1/video-jobs/{job_id}/cancel",
        path_params={"b": 2, "a": 1},
        request_body={},
    )
    right = canonicalize_request(
        owner_id="owner_1",
        http_method="POST",
        route_template="/v1/video-jobs/{job_id}/cancel",
        path_params={"a": 1, "b": 2},
        request_body={},
    )

    assert left.path_params_hash == right.path_params_hash


@pytest.mark.parametrize("bad_number", [float("nan"), float("inf"), float("-inf")])
def test_canonical_request_rejects_nan_and_infinity(bad_number: float) -> None:
    with pytest.raises(ValueError):
        canonicalize_request(
            owner_id="owner_1",
            http_method="POST",
            route_template="/v1/video-jobs",
            path_params={},
            request_body={"value": bad_number},
        )


def test_new_request_creates_pending_with_lease_and_expiry(tmp_path: Path) -> None:
    clock = FakeClock(now_utc())
    service, SessionLocal = make_service(tmp_path, clock=clock)

    result = acquire(service)

    assert result.disposition == IdempotencyDisposition.ACQUIRED
    assert result.idempotent_replay is False
    with SessionLocal() as session:
        record = get_record(session, result.record_id)
        assert record.status.value == "PENDING"
        assert ensure_utc(record.lease_expires_at) == now_utc() + timedelta(seconds=60)
        assert ensure_utc(record.expires_at) == now_utc() + timedelta(hours=24)


def test_completed_same_payload_replays_without_modifying_snapshot(tmp_path: Path) -> None:
    service, SessionLocal = make_service(tmp_path)
    first = acquire(service)
    service.complete(
        record_id=first.record_id,
        response_status_code=202,
        response_json={"job_id": "job_1", "idempotent_replay": True},
    )

    replay = acquire(service)

    assert replay.disposition == IdempotencyDisposition.REPLAY
    assert replay.response_status_code == 202
    assert replay.response_json == {"job_id": "job_1", "idempotent_replay": True}
    assert replay.idempotent_replay is True
    with SessionLocal() as session:
        record = get_record(session, first.record_id)
        assert record.response_json == {"job_id": "job_1", "idempotent_replay": False}


def test_same_key_different_completed_payload_conflicts(tmp_path: Path) -> None:
    service, _ = make_service(tmp_path)
    first = acquire(service)
    service.complete(
        record_id=first.record_id,
        response_status_code=202,
        response_json={"job_id": "job_1"},
    )

    with pytest.raises(IdempotencyConflictError):
        acquire(service, body={"prompt": "different"})


def test_active_pending_same_payload_returns_pending(tmp_path: Path) -> None:
    service, _ = make_service(tmp_path)
    acquire(service)

    with pytest.raises(IdempotencyPendingError):
        acquire(service)


def test_active_pending_different_payload_conflicts(tmp_path: Path) -> None:
    service, _ = make_service(tmp_path)
    acquire(service)

    with pytest.raises(IdempotencyConflictError):
        acquire(service, body={"prompt": "different"})


def test_expired_pending_same_payload_can_be_acquired(tmp_path: Path) -> None:
    clock = FakeClock(now_utc())
    service, _ = make_service(tmp_path, clock=clock)
    first = acquire(service)
    clock.set(now_utc() + timedelta(seconds=61))

    second = acquire(service)

    assert second.disposition == IdempotencyDisposition.ACQUIRED
    assert second.record_id == first.record_id


def test_expired_pending_different_payload_still_conflicts(tmp_path: Path) -> None:
    clock = FakeClock(now_utc())
    service, _ = make_service(tmp_path, clock=clock)
    acquire(service)
    clock.set(now_utc() + timedelta(seconds=61))

    with pytest.raises(IdempotencyConflictError):
        acquire(service, body={"prompt": "different"})


def test_expired_pending_competition_has_one_winner(tmp_path: Path) -> None:
    clock = FakeClock(now_utc())
    service, SessionLocal = make_service(tmp_path, clock=clock)
    acquire(service)
    clock.set(now_utc() + timedelta(seconds=61))

    def worker() -> str:
        worker_service = IdempotencyService(
            session_factory=SessionLocal,
            clock=clock,
        )
        try:
            return worker_service.acquire(
                owner_id="owner_1",
                http_method="POST",
                route_template="/v1/video-jobs",
                path_params={},
                request_body={"prompt": "clean garage"},
                idempotency_key="client-key",
            ).disposition.value
        except IdempotencyPendingError:
            return "PENDING"

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: worker(), range(2)))

    assert sorted(results) == ["ACQUIRED", "PENDING"]
    with SessionLocal() as session:
        count = session.scalar(select(func.count()).select_from(IdempotencyRecord))
        assert count == 1


def test_completed_expired_key_can_be_reused_for_same_or_different_payload(
    tmp_path: Path,
) -> None:
    clock = FakeClock(now_utc())
    service, _ = make_service(tmp_path, clock=clock)
    first = acquire(service)
    service.complete(
        record_id=first.record_id,
        response_status_code=202,
        response_json={"job_id": "job_1"},
    )
    clock.set(now_utc() + timedelta(hours=24, seconds=1))

    second = acquire(service, body={"prompt": "different"})

    assert second.disposition == IdempotencyDisposition.ACQUIRED
    assert second.record_id == first.record_id


def test_bind_resource_success_repeat_and_rebind_rejected(tmp_path: Path) -> None:
    service, _ = make_service(tmp_path)
    first = acquire(service)

    bound = service.bind_resource(
        record_id=first.record_id,
        resource_type="video_job",
        resource_id="job_1",
    )
    repeated = service.bind_resource(
        record_id=first.record_id,
        resource_type="video_job",
        resource_id="job_1",
    )

    assert bound.resource_type == "video_job"
    assert repeated.resource_id == "job_1"
    with pytest.raises(ValueError):
        service.bind_resource(
            record_id=first.record_id,
            resource_type="video_job",
            resource_id="job_2",
        )


def test_recovery_recovered_completes_and_replays(tmp_path: Path) -> None:
    clock = FakeClock(now_utc())
    resolver = FakeResolver(
        RecoveryResult(
            status=RecoveryStatus.RECOVERED,
            response_status_code=202,
            response_json={"job_id": "job_1", "idempotent_replay": False},
        )
    )
    service, _ = make_service(tmp_path, clock=clock, resolver=resolver)
    first = acquire(service)
    service.bind_resource(
        record_id=first.record_id,
        resource_type="video_job",
        resource_id="job_1",
    )
    clock.set(now_utc() + timedelta(seconds=61))

    recovered = acquire(service)

    assert recovered.disposition == IdempotencyDisposition.REPLAY
    assert recovered.response_json == {"job_id": "job_1", "idempotent_replay": True}
    assert resolver.calls == [("video_job", "job_1")]


def test_recovery_not_found_allows_reexecution_and_clears_resource(
    tmp_path: Path,
) -> None:
    clock = FakeClock(now_utc())
    resolver = FakeResolver(RecoveryResult(status=RecoveryStatus.NOT_FOUND))
    service, _ = make_service(tmp_path, clock=clock, resolver=resolver)
    first = acquire(service)
    service.bind_resource(
        record_id=first.record_id,
        resource_type="video_job",
        resource_id="job_missing",
    )
    clock.set(now_utc() + timedelta(seconds=61))

    acquired = acquire(service)

    assert acquired.disposition == IdempotencyDisposition.ACQUIRED
    assert acquired.resource_type is None
    assert acquired.resource_id is None


def test_recovery_incomplete_does_not_repeat_side_effect(tmp_path: Path) -> None:
    clock = FakeClock(now_utc())
    resolver = FakeResolver(RecoveryResult(status=RecoveryStatus.INCOMPLETE))
    service, _ = make_service(tmp_path, clock=clock, resolver=resolver)
    first = acquire(service)
    service.bind_resource(
        record_id=first.record_id,
        resource_type="video_job",
        resource_id="job_1",
    )
    clock.set(now_utc() + timedelta(seconds=61))

    with pytest.raises(IdempotencyPendingError):
        acquire(service)


def test_complete_pending_repeat_same_and_reject_different_response(
    tmp_path: Path,
) -> None:
    service, _ = make_service(tmp_path)
    first = acquire(service)

    completed = service.complete(
        record_id=first.record_id,
        response_status_code=201,
        response_json={"asset_id": "asset_1"},
    )
    repeated = service.complete(
        record_id=first.record_id,
        response_status_code=201,
        response_json={"asset_id": "asset_1"},
    )

    assert completed.status == "COMPLETED"
    assert repeated.response_json == {"asset_id": "asset_1"}
    with pytest.raises(ValueError):
        service.complete(
            record_id=first.record_id,
            response_status_code=201,
            response_json={"asset_id": "asset_2"},
        )


def test_complete_rejects_non_json_response_without_partial_write(
    tmp_path: Path,
) -> None:
    service, SessionLocal = make_service(tmp_path)
    first = acquire(service)

    with pytest.raises(TypeError):
        service.complete(
            record_id=first.record_id,
            response_status_code=201,
            response_json={"bad": object()},
        )

    with SessionLocal() as session:
        record = get_record(session, first.record_id)
        assert record.status.value == "PENDING"
        assert record.response_json is None


def test_concurrent_insert_uses_unique_constraint_without_duplicate_records(
    tmp_path: Path,
) -> None:
    clock = FakeClock(now_utc())
    service, SessionLocal = make_service(tmp_path, clock=clock)

    def worker() -> str:
        try:
            return acquire(service).disposition.value
        except IdempotencyPendingError:
            return "PENDING"

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: worker(), range(2)))

    assert sorted(results) == ["ACQUIRED", "PENDING"]
    with SessionLocal() as session:
        count = session.scalar(select(func.count()).select_from(IdempotencyRecord))
        assert count == 1

    assert acquire(service, key="other-key").disposition == IdempotencyDisposition.ACQUIRED


def test_cache_policy_classifies_cacheable_and_non_cacheable_responses() -> None:
    policy = CachePolicy()

    assert policy.is_cacheable(201, {"idempotent_replay": False}) is True
    assert (
        policy.is_cacheable(
            422,
            {"error": {"code": "SCHEMA_INVALID"}},
        )
        is True
    )
    assert (
        policy.is_cacheable(
            409,
            {"error": {"code": "IDEMPOTENCY_PENDING"}},
        )
        is False
    )
    assert (
        policy.is_cacheable(
            500,
            {"error": {"code": "INTERNAL_ERROR"}},
        )
        is False
    )


def test_clock_returns_utc() -> None:
    naive = datetime(2026, 7, 14, 12, 0)
    clock = FakeClock(naive)

    assert clock.now().tzinfo == timezone.utc


def test_no_formal_routes_or_database_tables_added_by_idempotency() -> None:
    app = create_app()
    schema_paths = set(app.openapi()["paths"])
    import_models()

    assert schema_paths == {
        "/health",
        "/v1/assets/upload-url",
        "/v1/video-jobs",
        "/v1/video-jobs/{job_id}",
        "/v1/video-jobs/{job_id}/cancel",
        "/v1/video-jobs/{job_id}/retry",
    }
    assert "/_internal/mock-uploads/{token}" not in schema_paths
    assert set(Base.metadata.tables) == APPROVED_TABLES
