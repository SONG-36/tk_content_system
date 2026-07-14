from __future__ import annotations

import hashlib
import json
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
from app.db.types import AIReviewStatus, AssetKind, AssetStatus, AttemptStatus, GenerationStatus
from app.main import create_app
from app.models.asset import Asset
from app.models.generation_request_snapshot import GenerationRequestSnapshot
from app.models.job_asset_reference import JobAssetReference
from app.models.job_attempt import JobAttempt
from app.models.provider_result import ProviderResult
from app.models.video_job import VideoJob
from app.providers.base import MockOutcome
from app.providers.mock import MockProvider, read_mock_result_fixture
from app.runners.mock_provider import MockProviderRunner
from app.schemas.jobs import CreateVideoJobRequest
from app.services.video_jobs import VideoJobService


def now_utc() -> datetime:
    return datetime(2026, 7, 14, 12, 0, tzinfo=timezone.utc)


def settings_for(tmp_path: Path, *, owner_id: str = "owner_1") -> Settings:
    return Settings(
        api_key="secret",
        owner_id=owner_id,
        database_url=f"sqlite:///{tmp_path / owner_id / 'phase2a.db'}",
        public_base_url="http://testserver",
        mock_storage_directory=str(tmp_path / owner_id / "mock-storage"),
        result_token_secret="phase-2a-e2e-result-token-secret",
    )


def prepare_database(settings: Settings):
    Path(settings.database_url.replace("sqlite:///", "")).parent.mkdir(parents=True, exist_ok=True)
    engine = create_db_engine(settings.database_url)
    import_models()
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def auth_headers(key: str) -> dict[str, str]:
    return {"Authorization": "Bearer secret", "Idempotency-Key": key}


def bearer() -> dict[str, str]:
    return {"Authorization": "Bearer secret"}


def upload_asset(client: TestClient, data: bytes, *, key: str = "upload") -> str:
    upload = client.post(
        "/v1/assets/upload-url",
        json={
            "contract_version": "v1",
            "content_type": "video/mp4",
            "size_bytes": len(data),
            "checksum_sha256": hashlib.sha256(data).hexdigest(),
            "intended_usage_role": "PRODUCT_IDENTITY",
        },
        headers=auth_headers(key),
    )
    assert upload.status_code == 201
    token_path = urlparse(upload.json()["upload_url"]).path
    complete = client.put(token_path, content=data, headers={"Content-Type": "video/mp4"})
    assert complete.status_code == 200
    return upload.json()["asset_id"]


def t2v_payload(**overrides):
    payload = {
        "contract_version": "v1",
        "expected_truth_rule_version": "truth-rules-v0.4",
        "selected_model": "Seedance",
        "execution_provider": "mock",
        "shot_number": "Shot 01",
        "production_type": "AI_GENERATION",
        "generation_mode": "T2V",
        "prompt": "Low truth atmospheric garage product moment.",
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


def hybrid_payload(asset_id: str):
    return t2v_payload(
        production_type="HYBRID",
        generation_mode="I2V",
        truth_dependency="high",
        reference_assets=[
            {
                "asset_id": asset_id,
                "usage_role": "PRODUCT_IDENTITY",
                "shot_number": "Shot 01",
                "linked_proof_need_ids": ["pneed_1"],
                "required_for_truth_gate": True,
                "preservation_locks": {
                    "lock_identity": True,
                    "lock_structure": True,
                    "lock_motion": False,
                    "lock_environment": False,
                    "lock_text": False,
                },
            }
        ],
        proof_needs=[
            {
                "proof_need_id": "pneed_1",
                "shot_id": "Shot 01",
                "proof_type": "suction",
                "linked_client_fact_ids": [],
                "required_evidence_refs": [asset_id],
                "production_type": "HYBRID",
                "presentation_layer": "REAL_CAPTURE",
            }
        ],
        hybrid_layers={
            "real_layer": {
                "required": True,
                "description": "Real proof layer.",
                "reference_asset_ids": [asset_id],
                "carries_proof_need_ids": ["pneed_1"],
            },
            "ai_layer": {
                "required": True,
                "description": "AI environment only.",
                "allowed_roles": ["environment"],
                "prohibited_roles": ["core_product_proof"],
            },
            "ai_must_not_rewrite": [
                "product_shape",
                "logo",
                "controls",
                "accessory_set",
                "proof_result",
            ],
        },
    )


def count_rows(SessionLocal, model) -> int:
    with SessionLocal() as session:
        return session.scalar(select(func.count()).select_from(model)) or 0


def create_prepared_job(SessionLocal, settings: Settings, *, key: str = "prepared") -> str:
    result = VideoJobService(settings=settings, session_factory=SessionLocal).create_video_job(
        owner_id=settings.owner_id,
        request=CreateVideoJobRequest.model_validate(t2v_payload()),
        idempotency_key=key,
        request_id="req_e2e",
    )
    assert result.job_id is not None
    return result.job_id


def current_attempt(SessionLocal, job_id: str) -> JobAttempt:
    with SessionLocal() as session:
        job = session.get(VideoJob, job_id)
        assert job is not None and job.current_attempt_id is not None
        attempt = session.get(JobAttempt, job.current_attempt_id)
        assert attempt is not None
        session.expunge(attempt)
        return attempt


def test_e2e_hybrid_upload_generate_get_and_download_result(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    with TestClient(create_app(settings_override=settings)) as client:
        asset_id = upload_asset(client, read_mock_result_fixture())
        create = client.post(
            "/v1/video-jobs",
            json=hybrid_payload(asset_id),
            headers=auth_headers("create-hybrid"),
        )
        assert create.status_code == 202
        assert create.json()["generation_status"] == "QUEUED"
        job_id = create.json()["job_id"]
        job = client.get(f"/v1/video-jobs/{job_id}", headers=bearer()).json()
        result_url = job["result_media"][0]["result_url"]
        result = client.get(urlparse(result_url).path)

    assert job["generation_status"] == "SUCCEEDED"
    assert job["current_attempt"]["attempt_status"] == "SUCCEEDED"
    assert job["ai_review_status"] == "NOT_RUN"
    assert len(job["result_media"]) == 1
    assert "storage_path" not in json.dumps(job)
    assert "owner_id" not in json.dumps(job)
    assert "token_hash" not in json.dumps(job)
    assert result.status_code == 200
    assert result.headers["content-type"].startswith("video/mp4")
    assert result.content == read_mock_result_fixture()
    assert count_rows(SessionLocal, ProviderResult) == 1
    assert count_rows(SessionLocal, Asset) == 2


def test_e2e_low_truth_t2v_succeeds_without_input_asset(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    with TestClient(create_app(settings_override=settings)) as client:
        create = client.post(
            "/v1/video-jobs",
            json=t2v_payload(),
            headers=auth_headers("create-t2v"),
        )
        job = client.get(
            f"/v1/video-jobs/{create.json()['job_id']}",
            headers=bearer(),
        ).json()

    assert create.status_code == 202
    assert job["generation_status"] == "SUCCEEDED"
    assert job["assets"] == []
    assert len(job["result_media"]) == 1


@pytest.mark.parametrize(
    ("payload", "error_code"),
    [
        (t2v_payload(truth_dependency="high"), "TRUTH_GATE_BLOCKED"),
        (
            t2v_payload(
                proof_needs=[
                    {
                        "proof_need_id": "pneed_1",
                        "shot_id": "Shot 01",
                        "proof_type": "suction",
                        "linked_client_fact_ids": [],
                        "required_evidence_refs": [],
                        "production_type": "AI_GENERATION",
                        "presentation_layer": "AI_VISUALIZATION",
                    }
                ]
            ),
            "AI_PROOF_NOT_ALLOWED",
        ),
        (
            t2v_payload(
                proof_needs=[
                    {
                        "proof_need_id": "pneed_1",
                        "shot_id": "Shot 01",
                        "proof_type": "before_after",
                        "linked_client_fact_ids": [],
                        "required_evidence_refs": [],
                        "production_type": "AI_GENERATION",
                        "presentation_layer": "AI_VISUALIZATION",
                    }
                ]
            ),
            "AI_PROOF_NOT_ALLOWED",
        ),
        (
            t2v_payload(
                proof_needs=[
                    {
                        "proof_need_id": "pneed_1",
                        "shot_id": "Shot 01",
                        "proof_type": "safety",
                        "linked_client_fact_ids": [],
                        "required_evidence_refs": [],
                        "production_type": "AI_GENERATION",
                        "presentation_layer": "AI_VISUALIZATION",
                    }
                ]
            ),
            "AI_PROOF_NOT_ALLOWED",
        ),
        (
            t2v_payload(
                proof_needs=[
                    {
                        "proof_need_id": "pneed_1",
                        "shot_id": "Shot 01",
                        "proof_type": "identity",
                        "linked_client_fact_ids": [],
                        "required_evidence_refs": [],
                        "production_type": "AI_GENERATION",
                        "presentation_layer": "AI_VISUALIZATION",
                    }
                ]
            ),
            "TRUTH_GATE_BLOCKED",
        ),
    ],
)
def test_e2e_truth_blocks_are_cached_without_side_effects(tmp_path: Path, payload, error_code: str) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    with TestClient(create_app(settings_override=settings)) as client:
        first = client.post("/v1/video-jobs", json=payload, headers=auth_headers("blocked"))
        replay = client.post("/v1/video-jobs", json=payload, headers=auth_headers("blocked"))

    assert first.status_code == 422
    assert first.json()["error"]["code"] == error_code
    assert replay.status_code == 422
    assert replay.json() == first.json()
    assert count_rows(SessionLocal, VideoJob) == 0
    assert count_rows(SessionLocal, JobAttempt) == 0
    assert count_rows(SessionLocal, GenerationRequestSnapshot) == 0
    assert count_rows(SessionLocal, JobAssetReference) == 0


def test_e2e_idempotency_upload_create_cancel_retry(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    data = read_mock_result_fixture()
    upload_body = {
        "contract_version": "v1",
        "content_type": "video/mp4",
        "size_bytes": len(data),
        "checksum_sha256": hashlib.sha256(data).hexdigest(),
        "intended_usage_role": "PRODUCT_IDENTITY",
    }
    with TestClient(create_app(settings_override=settings)) as client:
        first_upload = client.post("/v1/assets/upload-url", json=upload_body, headers=auth_headers("upload-same"))
        replay_upload = client.post("/v1/assets/upload-url", json=upload_body, headers=auth_headers("upload-same"))
        conflict_upload = client.post(
            "/v1/assets/upload-url",
            json={**upload_body, "size_bytes": len(data) + 1},
            headers=auth_headers("upload-same"),
        )
        create = client.post("/v1/video-jobs", json=t2v_payload(), headers=auth_headers("create-same"))
        create_replay = client.post("/v1/video-jobs", json=t2v_payload(), headers=auth_headers("create-same"))
        failed_job = create_prepared_job(SessionLocal, settings, key="prepared-fail")
        MockProviderRunner(settings=settings, session_factory=SessionLocal, provider=MockProvider(MockOutcome.failed)).run_job(failed_job)
        retry = client.post(f"/v1/video-jobs/{failed_job}/retry", json={"reason": "again"}, headers=auth_headers("retry-same"))
        retry_replay = client.post(f"/v1/video-jobs/{failed_job}/retry", json={"reason": "again"}, headers=auth_headers("retry-same"))
        retry_conflict = client.post(f"/v1/video-jobs/{failed_job}/retry", json={"reason": "different"}, headers=auth_headers("retry-same"))
        cancel_job = create_prepared_job(SessionLocal, settings, key="prepared-cancel")
        cancel = client.post(f"/v1/video-jobs/{cancel_job}/cancel", json={"reason": "stop"}, headers=auth_headers("cancel-same"))
        cancel_replay = client.post(f"/v1/video-jobs/{cancel_job}/cancel", json={"reason": "stop"}, headers=auth_headers("cancel-same"))
        cancel_conflict = client.post(f"/v1/video-jobs/{cancel_job}/cancel", json={"reason": "different"}, headers=auth_headers("cancel-same"))

    assert replay_upload.json()["asset_id"] == first_upload.json()["asset_id"]
    assert replay_upload.json()["idempotent_replay"] is True
    assert conflict_upload.status_code == 409
    assert create_replay.json()["job_id"] == create.json()["job_id"]
    assert count_rows(SessionLocal, JobAttempt) >= 4
    assert retry.status_code == 202
    assert retry_replay.json()["new_attempt_id"] == retry.json()["new_attempt_id"]
    assert retry_replay.json()["idempotent_replay"] is True
    assert retry_conflict.status_code == 409
    assert cancel.status_code in {200, 202}
    assert cancel_replay.json()["idempotent_replay"] is True
    assert cancel_conflict.status_code == 409


def test_e2e_startup_recovery_and_owner_boundaries(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    job_id = create_prepared_job(SessionLocal, settings, key="prepared-recovery")
    with TestClient(create_app(settings_override=settings)) as client:
        response = client.get(f"/v1/video-jobs/{job_id}", headers=bearer())

    body = response.json()
    assert body["generation_status"] == "FAILED"
    assert body["errors"][0]["code"] == "MOCK_RUNNER_INTERRUPTED"
    assert count_rows(SessionLocal, ProviderResult) == 0
    assert count_rows(SessionLocal, Asset) == 0

    other_settings = Settings(
        api_key=settings.api_key,
        owner_id="owner_2",
        database_url=settings.database_url,
        public_base_url=settings.public_base_url,
        mock_storage_directory=settings.mock_storage_directory,
        result_token_secret=settings.result_token_secret,
    )
    with TestClient(create_app(settings_override=other_settings)) as other_client:
        assert other_client.get(f"/v1/video-jobs/{job_id}", headers=bearer()).json()["error"]["code"] == "JOB_NOT_FOUND"
        assert other_client.post(f"/v1/video-jobs/{job_id}/cancel", json={"reason": "x"}, headers=auth_headers("other-cancel")).json()["error"]["code"] == "JOB_NOT_FOUND"
        assert other_client.post(f"/v1/video-jobs/{job_id}/retry", json={"reason": "x"}, headers=auth_headers("other-retry")).json()["error"]["code"] == "JOB_NOT_FOUND"
