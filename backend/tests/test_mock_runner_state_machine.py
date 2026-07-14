from __future__ import annotations

import hashlib
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

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
from app.main import create_app
from app.models.asset import Asset
from app.models.job_attempt import JobAttempt
from app.models.provider_result import ProviderResult
from app.models.video_job import VideoJob
from app.providers.base import MockOutcome
from app.providers.mock import MockProvider, read_mock_result_fixture
from app.repositories.job_attempts import JobAttemptRepository
from app.repositories.provider_results import ProviderResultRepository
from app.runners.mock_provider import MockProviderRunner
from app.schemas.jobs import CreateVideoJobRequest
from app.services.startup_recovery import StartupRecoveryService
from app.services.video_jobs import VideoJobService
from app.state_machines.aggregation import ATTEMPT_TO_JOB_STATUS, aggregate_attempt_status
from app.state_machines.attempts import ATTEMPT_TRANSITIONS, assert_attempt_transition
from app.state_machines.jobs import JOB_TRANSITIONS, assert_job_transition
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


def now_utc() -> datetime:
    return datetime(2026, 7, 14, 12, 0, tzinfo=timezone.utc)


def settings_for(tmp_path: Path) -> Settings:
    return Settings(
        api_key="secret",
        owner_id="owner_1",
        database_url=f"sqlite:///{tmp_path / 'runner.db'}",
        public_base_url="http://testserver",
        mock_storage_directory=str(tmp_path / "mock-storage"),
    )


def prepare_database(settings: Settings):
    engine = create_db_engine(settings.database_url)
    import_models()
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def base_payload() -> dict[str, Any]:
    return {
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


def create_prepared_job(tmp_path: Path, *, provider: Optional[MockProvider] = None):
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    service = VideoJobService(settings=settings, session_factory=SessionLocal)
    result = service.create_video_job(
        owner_id=settings.owner_id,
        request=CreateVideoJobRequest.model_validate(base_payload()),
        idempotency_key="job-key",
        request_id="req_1",
    )
    runner = MockProviderRunner(
        settings=settings,
        session_factory=SessionLocal,
        provider=provider or MockProvider(),
    )
    return settings, SessionLocal, result.job_id, runner


def get_job(SessionLocal, job_id: str) -> VideoJob:
    with SessionLocal() as session:
        job = session.get(VideoJob, job_id)
        assert job is not None
        session.expunge(job)
        return job


def get_attempt(SessionLocal, attempt_id: str) -> JobAttempt:
    with SessionLocal() as session:
        attempt = session.get(JobAttempt, attempt_id)
        assert attempt is not None
        session.expunge(attempt)
        return attempt


def count_rows(SessionLocal, model) -> int:
    with SessionLocal() as session:
        return session.scalar(select(func.count()).select_from(model)) or 0


def test_attempt_state_machine_allowed_and_forbidden_transitions() -> None:
    for current, targets in ATTEMPT_TRANSITIONS.items():
        for target in targets:
            assert_attempt_transition(current, target)
    forbidden = [
        (AttemptStatus.PREPARED, AttemptStatus.SUCCEEDED),
        (AttemptStatus.PROCESSING, AttemptStatus.CANCELLED),
        (AttemptStatus.FAILED, AttemptStatus.PROCESSING),
        (AttemptStatus.SUCCEEDED, AttemptStatus.PREPARED),
        (AttemptStatus.UNKNOWN_PROVIDER_STATE, AttemptStatus.PROCESSING),
    ]
    for current, target in forbidden:
        with pytest.raises(ValueError):
            assert_attempt_transition(current, target)
    for terminal in {
        AttemptStatus.SUCCEEDED,
        AttemptStatus.FAILED,
        AttemptStatus.CANCELLED,
    }:
        assert ATTEMPT_TRANSITIONS[terminal] == set()


def test_job_state_machine_allowed_forbidden_and_aggregation_complete() -> None:
    for current, targets in JOB_TRANSITIONS.items():
        for target in targets:
            assert_job_transition(current, target)
    for current, target in [
        (GenerationStatus.QUEUED, GenerationStatus.SUCCEEDED),
        (GenerationStatus.PROCESSING, GenerationStatus.QUEUED),
        (GenerationStatus.SUCCEEDED, GenerationStatus.QUEUED),
    ]:
        with pytest.raises(ValueError):
            assert_job_transition(current, target)
    assert set(ATTEMPT_TO_JOB_STATUS) == set(AttemptStatus)
    for attempt_status, job_status in ATTEMPT_TO_JOB_STATUS.items():
        assert aggregate_attempt_status(attempt_status) == job_status


def test_cas_updates_only_expected_state(tmp_path: Path) -> None:
    settings, SessionLocal, job_id, _ = create_prepared_job(tmp_path)
    job = get_job(SessionLocal, job_id)
    assert job.current_attempt_id is not None
    repo = JobAttemptRepository(SessionLocal)
    with SessionLocal() as session:
        ok = repo.transition_attempt(
            session,
            attempt_id=job.current_attempt_id,
            expected_status=AttemptStatus.PROCESSING,
            target_status=AttemptStatus.FAILED,
            now=now_utc(),
        )
        session.commit()
    assert ok is False
    assert get_attempt(SessionLocal, job.current_attempt_id).attempt_status == AttemptStatus.PREPARED


def test_mock_result_fixture_is_mp4_like_and_stable() -> None:
    data = read_mock_result_fixture()

    assert data
    assert b"ftyp" in data[:32]
    assert hashlib.sha256(data).hexdigest()


def test_runner_success_creates_result_media_and_provider_result(tmp_path: Path) -> None:
    provider = MockProvider(MockOutcome.success)
    settings, SessionLocal, job_id, runner = create_prepared_job(tmp_path, provider=provider)

    runner.run_job(job_id)

    job = get_job(SessionLocal, job_id)
    assert job.generation_status == GenerationStatus.SUCCEEDED
    assert job.ai_review_status == AIReviewStatus.NOT_RUN
    assert job.current_attempt_id is not None
    attempt = get_attempt(SessionLocal, job.current_attempt_id)
    assert attempt.attempt_status == AttemptStatus.SUCCEEDED
    assert attempt.provider_job_id
    assert attempt.submitted_at is not None
    assert attempt.terminal_at is not None
    assert attempt.created_at <= attempt.submitted_at <= attempt.terminal_at
    assert count_rows(SessionLocal, ProviderResult) == 1
    result_assets = []
    with SessionLocal() as session:
        result_assets = session.scalars(
            select(Asset).where(Asset.asset_kind == AssetKind.RESULT_MEDIA)
        ).all()
    assert len(result_assets) == 1
    result_asset = result_assets[0]
    assert result_asset.status == AssetStatus.READY
    assert result_asset.content_type == "video/mp4"
    assert Path(result_asset.storage_path).exists()
    data = Path(result_asset.storage_path).read_bytes()
    assert b"ftyp" in data[:32]
    assert result_asset.size_bytes == len(data)
    assert result_asset.checksum_sha256 == hashlib.sha256(data).hexdigest()
    assert provider.submit_count == 1
    assert provider.execute_count == 1


@pytest.mark.parametrize(
    "outcome,attempt_status,job_status,error_code",
    [
        (MockOutcome.failed, AttemptStatus.FAILED, GenerationStatus.FAILED, "MOCK_PROVIDER_FAILED"),
        (MockOutcome.unknown, AttemptStatus.UNKNOWN_PROVIDER_STATE, GenerationStatus.PROCESSING, None),
        (MockOutcome.cancel, AttemptStatus.CANCELLED, GenerationStatus.CANCELLED, None),
    ],
)
def test_runner_failed_unknown_and_cancel_outcomes(
    tmp_path: Path,
    outcome: MockOutcome,
    attempt_status: AttemptStatus,
    job_status: GenerationStatus,
    error_code: Optional[str],
) -> None:
    settings, SessionLocal, job_id, runner = create_prepared_job(
        tmp_path,
        provider=MockProvider(outcome),
    )

    runner.run_job(job_id)

    job = get_job(SessionLocal, job_id)
    assert job.generation_status == job_status
    assert job.current_attempt_id is not None
    attempt = get_attempt(SessionLocal, job.current_attempt_id)
    assert attempt.attempt_status == attempt_status
    assert attempt.error_code == error_code
    if outcome == MockOutcome.cancel:
        assert attempt.cancellation_intent is True
        assert attempt.cancel_requested_at is not None
    assert count_rows(SessionLocal, ProviderResult) == 0
    with SessionLocal() as session:
        assert (
            session.scalar(
                select(func.count()).select_from(Asset).where(Asset.asset_kind == AssetKind.RESULT_MEDIA)
            )
            == 0
        )
    assert not list((Path(settings.mock_storage_directory) / "results").glob("*"))


def test_repeated_and_concurrent_runner_calls_execute_provider_once(tmp_path: Path) -> None:
    provider = MockProvider(MockOutcome.success)
    _, SessionLocal, job_id, runner = create_prepared_job(tmp_path, provider=provider)

    with ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(lambda _: runner.run_job(job_id), range(2)))
    runner.run_job(job_id)

    assert provider.submit_count == 1
    assert provider.execute_count == 1
    assert count_rows(SessionLocal, ProviderResult) == 1
    with SessionLocal() as session:
        assert (
            session.scalar(
                select(func.count()).select_from(Asset).where(Asset.asset_kind == AssetKind.RESULT_MEDIA)
            )
            == 1
        )
    job = get_job(SessionLocal, job_id)
    assert job.current_attempt_id is not None
    assert JobAttemptRepository(SessionLocal).count_for_job(job_id) == 1


class FailingStorage(LocalMockStorage):
    def write_result_atomic(self, *, asset_id: str, content_type: str, data: bytes) -> str:
        raise OSError("disk full")


class FailingProviderResultRepository(ProviderResultRepository):
    def create_success_result(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("db failure")


class ExplodingProvider(MockProvider):
    def execute(self, provider_job_id: str, request_snapshot: dict[str, Any]):
        raise RuntimeError("unexpected provider failure")


def test_runner_file_write_failure_marks_failed_without_result(tmp_path: Path) -> None:
    settings, SessionLocal, job_id, _ = create_prepared_job(tmp_path)
    runner = MockProviderRunner(
        settings=settings,
        session_factory=SessionLocal,
        provider=MockProvider(MockOutcome.success),
        storage=FailingStorage(settings.mock_storage_directory),
    )

    runner.run_job(job_id)

    job = get_job(SessionLocal, job_id)
    assert job.current_attempt_id is not None
    attempt = get_attempt(SessionLocal, job.current_attempt_id)
    assert job.generation_status == GenerationStatus.FAILED
    assert attempt.attempt_status == AttemptStatus.FAILED
    assert attempt.error_code == "MOCK_RESULT_STORAGE_FAILED"
    assert count_rows(SessionLocal, ProviderResult) == 0


def test_runner_db_failure_deletes_result_file_and_marks_internal_error(
    tmp_path: Path,
) -> None:
    settings, SessionLocal, job_id, _ = create_prepared_job(tmp_path)
    runner = MockProviderRunner(
        settings=settings,
        session_factory=SessionLocal,
        provider=MockProvider(MockOutcome.success),
        provider_results=FailingProviderResultRepository(SessionLocal),
    )

    runner.run_job(job_id)

    assert not list((Path(settings.mock_storage_directory) / "results").glob("*.mp4"))
    assert count_rows(SessionLocal, ProviderResult) == 0
    with SessionLocal() as session:
        assert (
            session.scalar(
                select(func.count()).select_from(Asset).where(Asset.asset_kind == AssetKind.RESULT_MEDIA)
            )
            == 0
        )
    job = get_job(SessionLocal, job_id)
    assert job.current_attempt_id is not None
    assert get_attempt(SessionLocal, job.current_attempt_id).error_code == "MOCK_RUNNER_INTERNAL_ERROR"


def test_unexpected_runner_exception_is_converted_to_failed(tmp_path: Path) -> None:
    _, SessionLocal, job_id, _ = create_prepared_job(tmp_path)
    runner = MockProviderRunner(
        settings=settings_for(tmp_path),
        session_factory=SessionLocal,
        provider=ExplodingProvider(),
    )

    runner.run_job(job_id)

    job = get_job(SessionLocal, job_id)
    assert job.current_attempt_id is not None
    attempt = get_attempt(SessionLocal, job.current_attempt_id)
    assert job.generation_status == GenerationStatus.FAILED
    assert attempt.error_code == "MOCK_RUNNER_INTERNAL_ERROR"


def test_create_job_background_task_and_replay_dispatch_rules(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    provider = MockProvider(MockOutcome.success)
    from app.dependencies import get_mock_provider_runner

    app = create_app(settings_override=settings)
    runner = MockProviderRunner(
        settings=settings,
        session_factory=SessionLocal,
        provider=provider,
    )
    app.dependency_overrides[get_mock_provider_runner] = lambda: runner
    client = TestClient(app)
    headers = {"Authorization": "Bearer secret", "Idempotency-Key": "bg"}

    first = client.post("/v1/video-jobs", json=base_payload(), headers=headers)
    replay = client.post("/v1/video-jobs", json=base_payload(), headers=headers)
    blocked = client.post(
        "/v1/video-jobs",
        json={**base_payload(), "truth_dependency": "high"},
        headers={"Authorization": "Bearer secret", "Idempotency-Key": "blocked"},
    )

    assert first.status_code == 202
    assert first.json()["generation_status"] == "QUEUED"
    assert replay.status_code == 202
    assert replay.json()["idempotent_replay"] is True
    assert blocked.status_code == 422
    assert provider.submit_count == 1
    assert provider.execute_count == 1


def create_job_and_attempt(
    SessionLocal,
    *,
    attempt_status: AttemptStatus,
    job_status: GenerationStatus,
) -> tuple[str, str]:
    with SessionLocal() as session:
        job = VideoJob(
            job_id=f"job_{attempt_status.value.lower()}",
            owner_id="owner_1",
            contract_version="v1",
            truth_rule_version="truth-rules-v0.4",
            provider_mapping_version="mock-provider-map-v0.4",
            selected_model="Seedance",
            execution_provider="mock",
            generation_status=job_status,
            ai_review_status=AIReviewStatus.NOT_RUN,
            created_at=now_utc(),
            updated_at=now_utc(),
        )
        attempt = JobAttempt(
            attempt_id=f"attempt_{attempt_status.value.lower()}",
            job_id=job.job_id,
            attempt_no=1,
            execution_provider="mock",
            provider_model="Seedance",
            attempt_status=attempt_status,
            cancellation_intent=attempt_status == AttemptStatus.CANCEL_REQUESTED,
            cancel_requested_at=now_utc()
            if attempt_status == AttemptStatus.CANCEL_REQUESTED
            else None,
            provider_job_id="mock_job_existing",
            created_at=now_utc(),
            updated_at=now_utc(),
        )
        session.add(job)
        session.flush()
        session.add(attempt)
        session.flush()
        job.current_attempt_id = attempt.attempt_id
        session.commit()
        return job.job_id, attempt.attempt_id


@pytest.mark.parametrize(
    "attempt_status",
    [
        AttemptStatus.PREPARED,
        AttemptStatus.SUBMITTED,
        AttemptStatus.PROCESSING,
        AttemptStatus.CANCEL_REQUESTED,
        AttemptStatus.UNKNOWN_PROVIDER_STATE,
    ],
)
def test_startup_recovery_marks_non_terminal_mock_attempts_failed(
    tmp_path: Path,
    attempt_status: AttemptStatus,
) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    job_id, attempt_id = create_job_and_attempt(
        SessionLocal,
        attempt_status=attempt_status,
        job_status=aggregate_attempt_status(attempt_status),
    )

    recovered = StartupRecoveryService(session_factory=SessionLocal).recover_mock_attempts()

    assert recovered == 1
    attempt = get_attempt(SessionLocal, attempt_id)
    job = get_job(SessionLocal, job_id)
    assert attempt.attempt_status == AttemptStatus.FAILED
    assert attempt.error_code == "MOCK_RUNNER_INTERRUPTED"
    assert attempt.terminal_at is not None
    assert job.generation_status == GenerationStatus.FAILED
    assert count_rows(SessionLocal, ProviderResult) == 0


@pytest.mark.parametrize(
    "attempt_status",
    [AttemptStatus.SUCCEEDED, AttemptStatus.FAILED, AttemptStatus.CANCELLED],
)
def test_startup_recovery_does_not_modify_terminal_attempts(
    tmp_path: Path,
    attempt_status: AttemptStatus,
) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    _, attempt_id = create_job_and_attempt(
        SessionLocal,
        attempt_status=attempt_status,
        job_status=aggregate_attempt_status(attempt_status),
    )

    assert StartupRecoveryService(session_factory=SessionLocal).recover_mock_attempts() == 0
    assert get_attempt(SessionLocal, attempt_id).attempt_status == attempt_status


def test_phase_2a_7_openapi_and_table_boundary() -> None:
    paths = set(create_app().openapi()["paths"])
    import_models()

    assert paths == {"/health", "/v1/assets/upload-url", "/v1/video-jobs"}
    assert "/v1/video-jobs/{job_id}" not in paths
    assert "/v1/video-jobs/{job_id}/cancel" not in paths
    assert "/v1/video-jobs/{job_id}/retry" not in paths
    assert "/_internal/mock-results/{token}" not in paths
    assert "/_internal/mock-uploads/{token}" not in paths
    assert set(Base.metadata.tables) == APPROVED_TABLES
