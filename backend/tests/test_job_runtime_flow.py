from __future__ import annotations

import hashlib
import json
import uuid
import warnings
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import sessionmaker

from app.config import Settings
from app.db.base import Base, import_models
from app.db.session import create_db_engine
from app.db.types import (
    AIReviewStatus,
    AssetKind,
    AssetStatus,
    AttemptStatus,
    GenerationStatus,
)
from app.idempotency.types import FakeClock
from app.main import create_app
from app.models.asset import Asset
from app.models.job_attempt import JobAttempt
from app.models.provider_result import ProviderResult
from app.models.video_job import VideoJob
from app.providers.base import MockOutcome
from app.providers.mock import MockProvider, read_mock_result_fixture
from app.runners.mock_provider import MockProviderRunner
from app.schemas.jobs import CreateVideoJobRequest
from app.services.result_tokens import ResultTokenService, _b64encode, _json_bytes
from app.services.video_jobs import VideoJobService


APPROVED_TABLES = {
    "assets",
    "video_jobs",
    "job_attempts",
    "generation_request_snapshots",
    "job_asset_references",
    "provider_results",
    "idempotency_records",
}


def now_utc() -> datetime:
    return datetime(2026, 7, 14, 12, 0, tzinfo=timezone.utc)


def settings_for(tmp_path: Path, *, token_ttl_hours: int = 24) -> Settings:
    return Settings(
        api_key="secret",
        owner_id="owner_1",
        database_url=f"sqlite:///{tmp_path / 'runtime.db'}",
        public_base_url="http://testserver",
        mock_storage_directory=str(tmp_path / "mock-storage"),
        result_token_secret="test-result-token-secret-32-bytes",
        result_token_ttl_hours=token_ttl_hours,
    )


def prepare_database(settings: Settings):
    engine = create_db_engine(settings.database_url)
    import_models()
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def base_payload(**overrides):
    payload = {
        "contract_version": "v1",
        "expected_truth_rule_version": "truth-rules-v0.4",
        "selected_model": "Seedance",
        "execution_provider": "mock",
        "shot_number": "Shot 01",
        "production_type": "AI_GENERATION",
        "generation_mode": "T2V",
        "prompt": "Atmospheric garage hero shot.",
        "negative_constraints": [],
        "preservation_constraints": [],
        "reference_assets": [],
        "truth_dependency": "low",
        "duration_seconds": 8,
        "aspect_ratio": "9:16",
        "client_declared_facts": [],
        "source_refs": [],
        "proof_needs": [],
    }
    payload.update(overrides)
    return payload


def auth_headers(key: str = "idem-key") -> dict[str, str]:
    return {"Authorization": "Bearer secret", "Idempotency-Key": key}


def bearer() -> dict[str, str]:
    return {"Authorization": "Bearer secret"}


def create_job(SessionLocal, settings: Settings, *, payload=None) -> str:
    result = VideoJobService(settings=settings, session_factory=SessionLocal).create_video_job(
        owner_id=settings.owner_id,
        request=CreateVideoJobRequest.model_validate(payload or base_payload()),
        idempotency_key=f"create-{uuid.uuid4().hex}",
        request_id="req_1",
    )
    assert result.job_id is not None
    return result.job_id


def create_client_after_startup(settings: Settings):
    app = create_app(settings_override=settings)
    return TestClient(app)


def get_job(SessionLocal, job_id: str) -> VideoJob:
    with SessionLocal() as session:
        job = session.get(VideoJob, job_id)
        assert job is not None
        session.expunge(job)
        return job


def get_current_attempt(SessionLocal, job_id: str) -> JobAttempt:
    job = get_job(SessionLocal, job_id)
    assert job.current_attempt_id is not None
    with SessionLocal() as session:
        attempt = session.get(JobAttempt, job.current_attempt_id)
        assert attempt is not None
        session.expunge(attempt)
        return attempt


def set_job_attempt_state(
    SessionLocal,
    job_id: str,
    *,
    job_status: GenerationStatus,
    attempt_status: AttemptStatus,
) -> None:
    with SessionLocal() as session:
        job = session.get(VideoJob, job_id)
        assert job is not None and job.current_attempt_id is not None
        attempt = session.get(JobAttempt, job.current_attempt_id)
        assert attempt is not None
        job.generation_status = job_status
        attempt.attempt_status = attempt_status
        if attempt_status == AttemptStatus.FAILED:
            attempt.error_code = "MOCK_PROVIDER_FAILED"
            attempt.terminal_at = now_utc()
        if attempt_status == AttemptStatus.CANCELLED:
            attempt.cancellation_intent = True
            attempt.cancel_requested_at = now_utc()
            attempt.terminal_at = now_utc()
        session.commit()


def count_rows(SessionLocal, model) -> int:
    with SessionLocal() as session:
        return session.scalar(select(func.count()).select_from(model)) or 0


def test_lifespan_startup_recovery_without_on_event_warning(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    job_id = create_job(SessionLocal, settings)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with TestClient(create_app(settings_override=settings)) as client:
            response = client.get("/health")

    assert response.status_code == 200
    assert not [item for item in caught if "on_event is deprecated" in str(item.message)]
    assert get_job(SessionLocal, job_id).generation_status == GenerationStatus.FAILED


def test_get_job_auth_visibility_and_queued_aggregation(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    with TestClient(create_app(settings_override=settings)) as client:
        job_id = create_job(SessionLocal, settings)
        assert client.get(f"/v1/video-jobs/{job_id}").status_code == 401
        assert client.get(
            f"/v1/video-jobs/{job_id}",
            headers={"Authorization": "Bearer wrong"},
        ).json()["error"]["code"] == "AUTH_INVALID"
        assert client.get("/v1/video-jobs/job_missing", headers=bearer()).json()["error"]["code"] == "JOB_NOT_FOUND"
        response = client.get(f"/v1/video-jobs/{job_id}", headers=bearer())

    payload = response.json()
    assert response.status_code == 200
    assert payload["generation_status"] == "QUEUED"
    assert payload["ai_review_status"] == "NOT_RUN"
    assert payload["current_attempt"]["attempt_status"] == "PREPARED"
    assert payload["result_media"] == []


def test_get_job_assets_result_media_and_internal_result_download(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    with SessionLocal() as session:
        session.add(
            Asset(
                asset_id="asset_input",
                owner_id=settings.owner_id,
                asset_kind=AssetKind.INPUT_MEDIA,
                status=AssetStatus.READY,
                content_type="image/png",
                size_bytes=1,
                checksum_sha256="a" * 64,
                storage_path="/tmp/input.png",
                created_at=now_utc(),
                updated_at=now_utc(),
            )
        )
        session.commit()
    payload = base_payload(
        generation_mode="I2V",
        reference_assets=[
            {
                "asset_id": "asset_input",
                "usage_role": "PRODUCT_IDENTITY",
                "shot_number": "Shot 01",
                "linked_proof_need_ids": [],
                "required_for_truth_gate": False,
                "preservation_locks": {},
            }
        ],
    )
    with TestClient(create_app(settings_override=settings)) as client:
        job_id = create_job(SessionLocal, settings, payload=payload)
        MockProviderRunner(settings=settings, session_factory=SessionLocal).run_job(job_id)
        response = client.get(f"/v1/video-jobs/{job_id}", headers=bearer())
        result_url = response.json()["result_media"][0]["result_url"]
        result_response = client.get(urlparse(result_url).path)

    body = response.json()
    assert body["generation_status"] == "SUCCEEDED"
    assert body["assets"][0]["asset_id"] == "asset_input"
    assert all(asset["asset_kind"] != "RESULT_MEDIA" for asset in body["assets"])
    assert "storage_path" not in json.dumps(body)
    assert result_response.status_code == 200
    assert result_response.headers["content-type"].startswith("video/mp4")
    assert result_response.content == read_mock_result_fixture()


def test_result_token_rejects_tamper_expiry_and_not_ready_assets(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    with TestClient(create_app(settings_override=settings)) as client:
        job_id = create_job(SessionLocal, settings)
        MockProviderRunner(settings=settings, session_factory=SessionLocal).run_job(job_id)
        result_url = client.get(f"/v1/video-jobs/{job_id}", headers=bearer()).json()["result_media"][0]["result_url"]
        token = Path(urlparse(result_url).path).name
        assert client.get(f"/_internal/mock-results/{token}x").json()["error"]["code"] == "RESULT_TOKEN_INVALID"
        with SessionLocal() as session:
            result_asset = session.scalar(select(Asset).where(Asset.asset_kind == AssetKind.RESULT_MEDIA))
            assert result_asset is not None
            result_asset.status = AssetStatus.FAILED
            session.commit()
        assert client.get(urlparse(result_url).path).json()["error"]["code"] == "RESULT_NOT_READY"

    expired_dir = tmp_path / "expired"
    expired_dir.mkdir()
    expired_settings = settings_for(expired_dir, token_ttl_hours=0)
    prepare_database(expired_settings)
    expired_service = ResultTokenService(settings=expired_settings)
    expired_token, _ = expired_service.issue(asset_id="asset_missing", owner_id="owner_1")
    with TestClient(create_app(settings_override=expired_settings)) as client:
        assert client.get(f"/_internal/mock-results/{expired_token}").json()["error"]["code"] == "RESULT_URL_EXPIRED"


def test_result_token_secret_is_separate_from_api_key() -> None:
    with pytest.raises(ValueError):
        Settings(api_key="same-secret", result_token_secret="same-secret")


def test_cancel_prepared_processing_submitted_unknown_and_terminal_states(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    with TestClient(create_app(settings_override=settings)) as client:
        prepared_job = create_job(SessionLocal, settings)
        response = client.post(
            f"/v1/video-jobs/{prepared_job}/cancel",
            json={"reason": "user"},
            headers=auth_headers("cancel-prepared"),
        )
        assert response.status_code == 200
        assert get_current_attempt(SessionLocal, prepared_job).attempt_status == AttemptStatus.CANCELLED

        processing_job = create_job(SessionLocal, settings)
        set_job_attempt_state(
            SessionLocal,
            processing_job,
            job_status=GenerationStatus.PROCESSING,
            attempt_status=AttemptStatus.PROCESSING,
        )
        response = client.post(
            f"/v1/video-jobs/{processing_job}/cancel",
            json={"reason": "user"},
            headers=auth_headers("cancel-processing"),
        )
        assert response.status_code == 202
        assert get_current_attempt(SessionLocal, processing_job).attempt_status == AttemptStatus.CANCELLED
        assert count_rows(SessionLocal, ProviderResult) == 0

        submitted_job = create_job(SessionLocal, settings)
        set_job_attempt_state(
            SessionLocal,
            submitted_job,
            job_status=GenerationStatus.PROCESSING,
            attempt_status=AttemptStatus.SUBMITTED,
        )
        assert client.post(
            f"/v1/video-jobs/{submitted_job}/cancel",
            json={"reason": "user"},
            headers=auth_headers("cancel-submitted"),
        ).status_code == 202
        assert get_current_attempt(SessionLocal, submitted_job).attempt_status == AttemptStatus.CANCELLED

        unknown_job = create_job(SessionLocal, settings)
        set_job_attempt_state(
            SessionLocal,
            unknown_job,
            job_status=GenerationStatus.PROCESSING,
            attempt_status=AttemptStatus.UNKNOWN_PROVIDER_STATE,
        )
        response = client.post(
            f"/v1/video-jobs/{unknown_job}/cancel",
            json={"reason": "user"},
            headers=auth_headers("cancel-unknown"),
        )
        unknown_attempt = get_current_attempt(SessionLocal, unknown_job)
        assert response.status_code == 202
        assert unknown_attempt.attempt_status == AttemptStatus.UNKNOWN_PROVIDER_STATE
        assert unknown_attempt.cancellation_intent is True
        assert get_job(SessionLocal, unknown_job).generation_status == GenerationStatus.PROCESSING

        succeeded_job = create_job(SessionLocal, settings)
        MockProviderRunner(settings=settings, session_factory=SessionLocal).run_job(succeeded_job)
        response = client.post(
            f"/v1/video-jobs/{succeeded_job}/cancel",
            json={"reason": "late"},
            headers=auth_headers("cancel-succeeded"),
        )
        assert response.status_code == 409
        assert response.json()["error"]["code"] == "JOB_CANCEL_NOT_ALLOWED"
        replay = client.post(
            f"/v1/video-jobs/{succeeded_job}/cancel",
            json={"reason": "late"},
            headers=auth_headers("cancel-succeeded"),
        )
        assert replay.status_code == 409
        assert replay.json()["error"]["code"] == "JOB_CANCEL_NOT_ALLOWED"


def test_cancel_idempotency_replay_and_conflict(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    with TestClient(create_app(settings_override=settings)) as client:
        job_id = create_job(SessionLocal, settings)
        first = client.post(
            f"/v1/video-jobs/{job_id}/cancel",
            json={"reason": "same"},
            headers=auth_headers("cancel-replay"),
        )
        replay = client.post(
            f"/v1/video-jobs/{job_id}/cancel",
            json={"reason": "same"},
            headers=auth_headers("cancel-replay"),
        )
        conflict = client.post(
            f"/v1/video-jobs/{job_id}/cancel",
            json={"reason": "different"},
            headers=auth_headers("cancel-replay"),
        )

    assert first.status_code == 200
    assert replay.status_code == 200
    assert replay.json()["idempotent_replay"] is True
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "IDEMPOTENCY_CONFLICT"


def test_retry_failed_cancelled_replay_and_blocked_states(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    with TestClient(create_app(settings_override=settings)) as client:
        failed_job = create_job(SessionLocal, settings)
        MockProviderRunner(
            settings=settings,
            session_factory=SessionLocal,
            provider=MockProvider(MockOutcome.failed),
        ).run_job(failed_job)
        original_attempt = get_current_attempt(SessionLocal, failed_job).attempt_id
        first = client.post(
            f"/v1/video-jobs/{failed_job}/retry",
            json={"reason": "retry"},
            headers=auth_headers("retry-failed"),
        )
        replay = client.post(
            f"/v1/video-jobs/{failed_job}/retry",
            json={"reason": "retry"},
            headers=auth_headers("retry-failed"),
        )
        assert first.status_code == 202
        assert replay.json()["new_attempt_id"] == first.json()["new_attempt_id"]
        assert replay.json()["idempotent_replay"] is True
        assert count_rows(SessionLocal, JobAttempt) == 2
        assert get_job(SessionLocal, failed_job).current_attempt_id != original_attempt
        assert get_job(SessionLocal, failed_job).ai_review_status == AIReviewStatus.NOT_RUN

        cancelled_job = create_job(SessionLocal, settings)
        client.post(
            f"/v1/video-jobs/{cancelled_job}/cancel",
            json={"reason": "user"},
            headers=auth_headers("cancel-before-retry"),
        )
        response = client.post(
            f"/v1/video-jobs/{cancelled_job}/retry",
            json={"reason": "retry"},
            headers=auth_headers("retry-cancelled"),
        )
        assert response.status_code == 202

        processing_job = create_job(SessionLocal, settings)
        set_job_attempt_state(
            SessionLocal,
            processing_job,
            job_status=GenerationStatus.PROCESSING,
            attempt_status=AttemptStatus.UNKNOWN_PROVIDER_STATE,
        )
        response = client.post(
            f"/v1/video-jobs/{processing_job}/retry",
            json={"reason": "retry"},
            headers=auth_headers("retry-unknown"),
        )
        assert response.status_code == 409
        assert response.json()["error"]["code"] == "UNKNOWN_PROVIDER_STATE"


def test_runner_success_cancel_race_has_single_terminal_result(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    job_id = create_job(SessionLocal, settings)
    set_job_attempt_state(
        SessionLocal,
        job_id,
        job_status=GenerationStatus.PROCESSING,
        attempt_status=AttemptStatus.CANCEL_REQUESTED,
    )

    runner = MockProviderRunner(settings=settings, session_factory=SessionLocal)
    runner.cancel_job(job_id)
    runner._complete_success(
        job_id=job_id,
        attempt_id=get_current_attempt(SessionLocal, job_id).attempt_id,
        provider_job_id="mock_job_late",
        result_bytes=read_mock_result_fixture(),
        raw_payload={},
    )

    assert get_current_attempt(SessionLocal, job_id).attempt_status == AttemptStatus.CANCELLED
    assert get_job(SessionLocal, job_id).generation_status == GenerationStatus.CANCELLED
    assert count_rows(SessionLocal, ProviderResult) == 0


def test_phase_2a_8_openapi_tables_and_no_action_yaml() -> None:
    paths = set(create_app().openapi()["paths"])
    import_models()

    assert paths == {
        "/health",
        "/v1/assets/upload-url",
        "/v1/video-jobs",
        "/v1/video-jobs/{job_id}",
        "/v1/video-jobs/{job_id}/cancel",
        "/v1/video-jobs/{job_id}/retry",
    }
    assert "/_internal/mock-uploads/{token}" not in paths
    assert "/_internal/mock-results/{token}" not in paths
    assert set(Base.metadata.tables) == APPROVED_TABLES
