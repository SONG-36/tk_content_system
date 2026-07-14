from __future__ import annotations

from datetime import datetime, timedelta, timezone
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
    generate_prefixed_id,
)
from app.gates import GateResult, evaluate_hybrid_gate, evaluate_truth_gate
from app.idempotency import FakeClock, IdempotencyService
from app.idempotency.canonical import canonicalize_request
from app.idempotency.repository import IdempotencyRepository
from app.main import create_app
from app.models.asset import Asset
from app.models.generation_request_snapshot import GenerationRequestSnapshot
from app.models.job_asset_reference import JobAssetReference
from app.models.job_attempt import JobAttempt
from app.models.video_job import VideoJob
from app.repositories.assets import AssetRepository
from app.repositories.job_asset_references import JobAssetReferenceRepository
from app.repositories.job_attempts import JobAttemptRepository
from app.repositories.request_snapshots import GenerationRequestSnapshotRepository
from app.repositories.video_jobs import VideoJobRepository
from app.schemas.jobs import (
    CreateVideoJobRequest,
    HybridAiLayer,
    HybridLayers,
    HybridRealLayer,
)
from app.services.video_jobs import TRUTH_RULE_VERSION, VideoJobService


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
        database_url=f"sqlite:///{tmp_path / 'video-jobs.db'}",
        public_base_url="http://testserver",
        mock_storage_directory=str(tmp_path / "mock-storage"),
    )


def prepare_database(settings: Settings):
    engine = create_db_engine(settings.database_url)
    import_models()
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def client_for(tmp_path: Path):
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    return TestClient(create_app(settings_override=settings)), settings, SessionLocal


def auth_headers(key: str = "job-key") -> dict[str, str]:
    return {"Authorization": "Bearer secret", "Idempotency-Key": key}


def base_payload(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "contract_version": "v1",
        "expected_truth_rule_version": TRUTH_RULE_VERSION,
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


def proof_need(
    proof_type: str,
    *,
    proof_need_id: str = "pneed_1",
    presentation_layer: str = "AI_ENVIRONMENT",
    production_type: str = "AI_GENERATION",
) -> dict[str, Any]:
    return {
        "proof_need_id": proof_need_id,
        "shot_id": "Shot 01",
        "proof_type": proof_type,
        "linked_client_fact_ids": [],
        "required_evidence_refs": [],
        "production_type": production_type,
        "presentation_layer": presentation_layer,
    }


def reference_asset(
    asset_id: str,
    *,
    usage_role: str = "PROOF_EVIDENCE",
    linked: Optional[list[str]] = None,
    required: bool = True,
    locks: Optional[dict[str, bool]] = None,
) -> dict[str, Any]:
    return {
        "asset_id": asset_id,
        "usage_role": usage_role,
        "shot_number": "Shot 01",
        "linked_proof_need_ids": linked if linked is not None else ["pneed_1"],
        "required_for_truth_gate": required,
        "preservation_locks": locks or {},
    }


def hybrid_layers(asset_id: str) -> dict[str, Any]:
    return {
        "real_layer": {
            "required": True,
            "description": "Real product proof layer.",
            "reference_asset_ids": [asset_id],
            "carries_proof_need_ids": ["pneed_1"],
        },
        "ai_layer": {
            "required": True,
            "description": "AI atmosphere only.",
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
    }


def create_asset(
    SessionLocal,
    *,
    asset_id: str = "asset_1",
    owner_id: str = "owner_1",
    status: AssetStatus = AssetStatus.READY,
    content_type: str = "image/png",
    deleted: bool = False,
) -> str:
    with SessionLocal() as session:
        asset = Asset(
            asset_id=asset_id,
            owner_id=owner_id,
            asset_kind=AssetKind.INPUT_MEDIA,
            status=status,
            content_type=content_type,
            size_bytes=1,
            checksum_sha256="a" * 64,
            storage_path=f"/tmp/{asset_id}.png",
            created_at=now_utc(),
            updated_at=now_utc(),
            deleted_at=now_utc() if deleted else None,
        )
        session.add(asset)
        session.commit()
    return asset_id


def count_rows(SessionLocal, model) -> int:
    with SessionLocal() as session:
        return session.scalar(select(func.count()).select_from(model)) or 0


@pytest.mark.parametrize("truth_dependency", ["low", "medium"])
def test_truth_gate_allows_non_proof_ai_generation(truth_dependency: str) -> None:
    request = CreateVideoJobRequest.model_validate(
        base_payload(truth_dependency=truth_dependency)
    )

    result = evaluate_truth_gate(request, {})

    assert result.result == GateResult.ALLOW


def test_truth_gate_blocks_high_truth_ai_generation() -> None:
    request = CreateVideoJobRequest.model_validate(base_payload(truth_dependency="high"))

    result = evaluate_truth_gate(request, {})

    assert result.result == GateResult.BLOCK
    assert result.decisions[0].code == "TRUTH_GATE_BLOCKED"


@pytest.mark.parametrize(
    "blocked_type",
    [
        "suction",
        "dirt_intake",
        "before_after",
        "transparent_bin",
        "human_efficacy",
        "sterilization",
        "safety",
        "measurable_performance",
    ],
)
def test_truth_gate_blocks_forbidden_ai_proof_types(blocked_type: str) -> None:
    request = CreateVideoJobRequest.model_validate(
        base_payload(proof_needs=[proof_need(blocked_type)])
    )

    result = evaluate_truth_gate(request, {})

    assert result.result == GateResult.BLOCK
    assert result.decisions[0].code == "AI_PROOF_NOT_ALLOWED"


@pytest.mark.parametrize("proof_type", ["structure", "accessory"])
def test_truth_gate_blocks_protected_proof_without_real_binding(proof_type: str) -> None:
    request = CreateVideoJobRequest.model_validate(
        base_payload(proof_needs=[proof_need(proof_type)])
    )

    result = evaluate_truth_gate(request, {})

    assert result.result == GateResult.BLOCK


def test_truth_gate_blocks_identity_without_preservation_lock(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    asset_id = create_asset(SessionLocal)
    asset = AssetRepository(SessionLocal).get_by_id(asset_id)
    assert asset is not None
    request = CreateVideoJobRequest.model_validate(
        base_payload(
            proof_needs=[proof_need("identity")],
            reference_assets=[
                reference_asset(asset_id, locks={"lock_identity": False})
            ],
        )
    )

    result = evaluate_truth_gate(request, {asset_id: asset})

    assert result.result == GateResult.BLOCK


def test_truth_gate_accepts_ready_proof_asset_with_structure_binding(
    tmp_path: Path,
) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    asset_id = create_asset(SessionLocal)
    asset = AssetRepository(SessionLocal).get_by_id(asset_id)
    assert asset is not None
    request = CreateVideoJobRequest.model_validate(
        base_payload(
            proof_needs=[proof_need("identity")],
            reference_assets=[
                reference_asset(asset_id, locks={"lock_identity": True})
            ],
        )
    )

    result = evaluate_truth_gate(request, {asset_id: asset})
    rendered = str(result.to_json())

    assert result.result == GateResult.ALLOW
    assert "VERIFIED" not in rendered
    assert "semantically_proven" not in rendered


def test_truth_gate_does_not_access_network_or_mutate_request(monkeypatch) -> None:
    request = CreateVideoJobRequest.model_validate(base_payload())
    before = request.model_dump(mode="json")

    def fail_network(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("network access is forbidden")

    monkeypatch.setattr("urllib.request.urlopen", fail_network)
    result = evaluate_truth_gate(request, {})

    assert result.result == GateResult.ALLOW
    assert request.model_dump(mode="json") == before


def test_hybrid_gate_allows_real_proof_ai_environment(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    asset_id = create_asset(SessionLocal)
    asset = AssetRepository(SessionLocal).get_by_id(asset_id)
    assert asset is not None
    request = CreateVideoJobRequest.model_validate(
        base_payload(
            production_type="HYBRID",
            generation_mode="R2V",
            truth_dependency="high",
            proof_needs=[
                proof_need(
                    "function",
                    presentation_layer="REAL_CAPTURE",
                    production_type="HYBRID",
                )
            ],
            reference_assets=[
                reference_asset(asset_id, usage_role="PROOF_EVIDENCE")
            ],
            hybrid_layers=hybrid_layers(asset_id),
        )
    )

    result = evaluate_hybrid_gate(request, {asset_id: asset})

    assert result.result == GateResult.ALLOW
    assert result.details["real_layer_carries_proof"] is True
    assert result.details["ai_layer_presentation_only"] is True
    assert result.details["semantic_truth_verified"] is False


@pytest.mark.parametrize(
    "payload_update,field",
    [
        ({"hybrid_layers": None}, "hybrid_layers"),
        (
            {
                "hybrid_layers": {
                    "real_layer": {
                        "required": False,
                        "description": "",
                        "reference_asset_ids": [],
                        "carries_proof_need_ids": [],
                    },
                    "ai_layer": {"required": True, "description": "", "allowed_roles": []},
                    "ai_must_not_rewrite": ["product_shape"],
                }
            },
            "real_layer.required",
        ),
        (
            {
                "hybrid_layers": {
                    "real_layer": {
                        "required": True,
                        "description": "",
                        "reference_asset_ids": [],
                        "carries_proof_need_ids": [],
                    },
                    "ai_layer": {"required": False, "description": "", "allowed_roles": []},
                    "ai_must_not_rewrite": ["product_shape"],
                }
            },
            "ai_layer.required",
        ),
        (
            {
                "hybrid_layers": {
                    "real_layer": {
                        "required": True,
                        "description": "",
                        "reference_asset_ids": [],
                        "carries_proof_need_ids": [],
                    },
                    "ai_layer": {"required": True, "description": "", "allowed_roles": []},
                    "ai_must_not_rewrite": [],
                }
            },
            "ai_must_not_rewrite",
        ),
    ],
)
def test_hybrid_gate_defensively_blocks_missing_required_layers(
    payload_update: dict[str, Any],
    field: str,
) -> None:
    payload = base_payload(production_type="HYBRID", **payload_update)
    raw_layers = payload.get("hybrid_layers")
    if isinstance(raw_layers, dict):
        payload["hybrid_layers"] = HybridLayers.model_construct(
            real_layer=HybridRealLayer.model_construct(**raw_layers["real_layer"]),
            ai_layer=HybridAiLayer.model_construct(**raw_layers["ai_layer"]),
            ai_must_not_rewrite=raw_layers["ai_must_not_rewrite"],
        )
    request = CreateVideoJobRequest.model_construct(**payload)

    result = evaluate_hybrid_gate(request, {})

    assert result.result == GateResult.BLOCK
    assert field in result.decisions[0].field


@pytest.mark.parametrize(
    "allowed_role",
    ["core_product_proof", "before_after", "measurable_performance"],
)
def test_hybrid_gate_blocks_ai_proof_roles(allowed_role: str, tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    asset_id = create_asset(SessionLocal)
    asset = AssetRepository(SessionLocal).get_by_id(asset_id)
    assert asset is not None
    layers = hybrid_layers(asset_id)
    layers["ai_layer"]["allowed_roles"] = [allowed_role]
    request = CreateVideoJobRequest.model_validate(
        base_payload(
            production_type="HYBRID",
            generation_mode="R2V",
            proof_needs=[
                proof_need("function", presentation_layer="REAL_CAPTURE", production_type="HYBRID")
            ],
            reference_assets=[reference_asset(asset_id)],
            hybrid_layers=layers,
        )
    )

    result = evaluate_hybrid_gate(request, {asset_id: asset})

    assert result.result == GateResult.BLOCK


@pytest.mark.parametrize("missing_lock", ["product_shape", "proof_result"])
def test_hybrid_gate_blocks_missing_rewrite_locks(
    missing_lock: str, tmp_path: Path
) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    asset_id = create_asset(SessionLocal)
    asset = AssetRepository(SessionLocal).get_by_id(asset_id)
    assert asset is not None
    layers = hybrid_layers(asset_id)
    layers["ai_must_not_rewrite"] = [
        item for item in layers["ai_must_not_rewrite"] if item != missing_lock
    ]
    request = CreateVideoJobRequest.model_validate(
        base_payload(
            production_type="HYBRID",
            generation_mode="R2V",
            proof_needs=[
                proof_need("function", presentation_layer="REAL_CAPTURE", production_type="HYBRID")
            ],
            reference_assets=[reference_asset(asset_id)],
            hybrid_layers=layers,
        )
    )

    result = evaluate_hybrid_gate(request, {asset_id: asset})

    assert result.result == GateResult.BLOCK
    assert missing_lock in result.decisions[0].details["missing_rewrite_locks"]


def test_create_video_job_requires_auth_key_and_version(tmp_path: Path) -> None:
    client, _, _ = client_for(tmp_path)
    payload = base_payload()

    assert client.post("/v1/video-jobs", json=payload).json()["error"]["code"] == "AUTH_REQUIRED"
    assert client.post(
        "/v1/video-jobs",
        json=payload,
        headers={"Authorization": "Bearer wrong", "Idempotency-Key": "k"},
    ).json()["error"]["code"] == "AUTH_INVALID"
    assert client.post(
        "/v1/video-jobs",
        json=payload,
        headers={"Authorization": "Bearer secret"},
    ).json()["error"]["code"] == "IDEMPOTENCY_KEY_REQUIRED"
    version = client.post(
        "/v1/video-jobs",
        json=base_payload(expected_truth_rule_version="old"),
        headers=auth_headers("version"),
    )
    assert version.status_code == 409
    assert version.json()["error"]["code"] == "VERSION_CONFLICT"


def test_create_video_job_asset_validation_errors(tmp_path: Path) -> None:
    client, _, SessionLocal = client_for(tmp_path)
    missing_payload = base_payload(
        generation_mode="I2V",
        reference_assets=[
            reference_asset("asset_missing", usage_role="FIRST_FRAME", linked=[])
        ],
    )
    missing = client.post(
        "/v1/video-jobs",
        json=missing_payload,
        headers=auth_headers("missing"),
    )
    other_owner = create_asset(SessionLocal, asset_id="asset_other", owner_id="owner_2")
    pending = create_asset(SessionLocal, asset_id="asset_pending", status=AssetStatus.PENDING_UPLOAD)
    failed = create_asset(SessionLocal, asset_id="asset_failed", status=AssetStatus.FAILED)

    assert missing.status_code == 422
    assert missing.json()["error"]["code"] == "ASSET_NOT_FOUND"
    assert client.post(
        "/v1/video-jobs",
        json=base_payload(
            generation_mode="I2V",
            reference_assets=[reference_asset(other_owner, usage_role="FIRST_FRAME", linked=[])],
        ),
        headers=auth_headers("other-owner"),
    ).json()["error"]["code"] == "ASSET_NOT_FOUND"
    assert client.post(
        "/v1/video-jobs",
        json=base_payload(
            generation_mode="I2V",
            reference_assets=[reference_asset(pending, usage_role="FIRST_FRAME", linked=[])],
        ),
        headers=auth_headers("pending"),
    ).json()["error"]["code"] == "ASSET_NOT_READY"
    assert client.post(
        "/v1/video-jobs",
        json=base_payload(
            generation_mode="I2V",
            reference_assets=[reference_asset(failed, usage_role="FIRST_FRAME", linked=[])],
        ),
        headers=auth_headers("failed"),
    ).json()["error"]["code"] == "ASSET_INVALID_STATE"


def test_create_video_job_success_persists_job_attempt_snapshot_and_refs(
    tmp_path: Path,
) -> None:
    client, _, SessionLocal = client_for(tmp_path)
    asset_id = create_asset(SessionLocal)
    payload = base_payload(
        generation_mode="I2V",
        reference_assets=[
            reference_asset(asset_id, usage_role="FIRST_FRAME", linked=[], required=False)
        ],
    )

    response = client.post("/v1/video-jobs", json=payload, headers=auth_headers("success"))

    assert response.status_code == 202
    body = response.json()
    assert body["job_id"].startswith("job_")
    assert body["generation_status"] == "QUEUED"
    assert body["ai_review_status"] == "NOT_RUN"
    assert body["execution_provider"] == "mock"
    assert body["idempotent_replay"] is False
    with SessionLocal() as session:
        job = session.get(VideoJob, body["job_id"])
        assert job is not None
        assert job.generation_status == GenerationStatus.QUEUED
        assert job.ai_review_status == AIReviewStatus.NOT_RUN
        attempt = session.get(JobAttempt, job.current_attempt_id)
        assert attempt is not None
        assert attempt.attempt_status == AttemptStatus.PREPARED
        assert attempt.attempt_no == 1
        snapshot = session.scalar(
            select(GenerationRequestSnapshot).where(
                GenerationRequestSnapshot.job_id == job.job_id
            )
        )
        assert snapshot is not None
        assert snapshot.request_json["generation_mode"] == "I2V"
        assert snapshot.gate_result_json["truth_gate"]["result"] == "ALLOW"
        refs = session.scalars(
            select(JobAssetReference).where(JobAssetReference.job_id == job.job_id)
        ).all()
        assert len(refs) == 1


def test_create_hybrid_job_success(tmp_path: Path) -> None:
    client, _, SessionLocal = client_for(tmp_path)
    asset_id = create_asset(SessionLocal)
    payload = base_payload(
        production_type="HYBRID",
        generation_mode="R2V",
        truth_dependency="high",
        proof_needs=[
            proof_need("function", presentation_layer="REAL_CAPTURE", production_type="HYBRID")
        ],
        reference_assets=[reference_asset(asset_id)],
        hybrid_layers=hybrid_layers(asset_id),
    )

    response = client.post("/v1/video-jobs", json=payload, headers=auth_headers("hybrid"))

    assert response.status_code == 202


def test_gate_block_creates_no_business_resources_and_is_cached(tmp_path: Path) -> None:
    client, _, SessionLocal = client_for(tmp_path)
    payload = base_payload(truth_dependency="high")

    first = client.post("/v1/video-jobs", json=payload, headers=auth_headers("gate"))
    second = client.post("/v1/video-jobs", json=payload, headers=auth_headers("gate"))

    assert first.status_code == 422
    assert first.json()["error"]["code"] == "TRUTH_GATE_BLOCKED"
    assert second.status_code == 422
    assert second.json() == first.json()
    assert count_rows(SessionLocal, VideoJob) == 0
    assert count_rows(SessionLocal, JobAttempt) == 0
    assert count_rows(SessionLocal, GenerationRequestSnapshot) == 0
    assert count_rows(SessionLocal, JobAssetReference) == 0


def test_success_replay_and_conflict_do_not_create_second_attempt(tmp_path: Path) -> None:
    client, _, SessionLocal = client_for(tmp_path)
    payload = base_payload()

    first = client.post("/v1/video-jobs", json=payload, headers=auth_headers("replay"))
    second = client.post("/v1/video-jobs", json=payload, headers=auth_headers("replay"))
    conflict = client.post(
        "/v1/video-jobs",
        json=base_payload(prompt="Different"),
        headers=auth_headers("replay"),
    )

    assert first.status_code == 202
    assert second.status_code == 202
    assert second.json()["job_id"] == first.json()["job_id"]
    assert second.json()["idempotent_replay"] is True
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "IDEMPOTENCY_CONFLICT"
    assert count_rows(SessionLocal, VideoJob) == 1
    assert count_rows(SessionLocal, JobAttempt) == 1


def test_active_pending_returns_idempotency_pending(tmp_path: Path) -> None:
    client, settings, _ = client_for(tmp_path)
    payload = base_payload()
    idem = IdempotencyService(
        session_factory=prepare_database(settings),
        clock=FakeClock(now_utc()),
    )
    idem.acquire(
        owner_id=settings.owner_id,
        http_method="POST",
        route_template="/v1/video-jobs",
        path_params={},
        request_body=CreateVideoJobRequest.model_validate(payload).model_dump(mode="json"),
        idempotency_key="active-pending",
    )

    response = client.post(
        "/v1/video-jobs",
        json=payload,
        headers=auth_headers("active-pending"),
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "IDEMPOTENCY_PENDING"


def test_expired_pending_bound_job_recovers_existing_job(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    clock = FakeClock(now_utc())
    idem_repo = IdempotencyRepository(SessionLocal)
    service = VideoJobService(
        settings=settings,
        session_factory=SessionLocal,
        clock=clock,
        idempotency_repository=idem_repo,
    )
    payload = base_payload()
    request = CreateVideoJobRequest.model_validate(payload)
    acquired = IdempotencyService(
        repository=idem_repo,
        clock=clock,
    ).acquire(
        owner_id=settings.owner_id,
        http_method="POST",
        route_template="/v1/video-jobs",
        path_params={},
        request_body=request.model_dump(mode="json"),
        idempotency_key="recover",
    )
    with SessionLocal() as session:
        job = VideoJobRepository(SessionLocal).create_queued_job(
            session,
            owner_id=settings.owner_id,
            contract_version="v1",
            truth_rule_version=TRUTH_RULE_VERSION,
            provider_mapping_version="mock-provider-map-v0.4",
            selected_model="Seedance",
            execution_provider="mock",
            now=clock.now(),
        )
        GenerationRequestSnapshotRepository(SessionLocal).create_snapshot(
            session,
            job_id=job.job_id,
            canonical_request_hash=canonicalize_request(
                owner_id=settings.owner_id,
                http_method="POST",
                route_template="/v1/video-jobs",
                path_params={},
                request_body=payload,
            ).canonical_request_hash,
            request_json=payload,
            gate_result_json={"truth_gate": {"result": "ALLOW"}, "hybrid_gate": {"result": "ALLOW"}},
            now=clock.now(),
        )
        attempt = JobAttemptRepository(SessionLocal).create_prepared_attempt(
            session,
            job_id=job.job_id,
            attempt_no=1,
            execution_provider="mock",
            provider_model="Seedance",
            now=clock.now(),
        )
        VideoJobRepository(SessionLocal).update_current_attempt_id(
            session,
            job_id=job.job_id,
            attempt_id=attempt.attempt_id,
            now=clock.now(),
        )
        idem_repo.bind_resource_in_session(
            session,
            record_id=acquired.record_id,
            resource_type="video_job",
            resource_id=job.job_id,
            now=clock.now(),
        )
        session.commit()
    clock.set(clock.now() + timedelta(seconds=61))

    response = service.create_video_job(
        owner_id=settings.owner_id,
        request=request,
        idempotency_key="recover",
        request_id="req_recover",
    )

    assert response.status_code == 202
    assert response.payload["job_id"] == job.job_id
    assert response.payload["idempotent_replay"] is True
    assert count_rows(SessionLocal, VideoJob) == 1


class FailingAttemptRepository(JobAttemptRepository):
    def create_prepared_attempt(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("attempt failed")


class FailingJobAssetReferenceRepository(JobAssetReferenceRepository):
    def create_many(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("refs failed")


def test_transaction_rolls_back_when_attempt_or_refs_fail(tmp_path: Path) -> None:
    settings = settings_for(tmp_path)
    SessionLocal = prepare_database(settings)
    request = CreateVideoJobRequest.model_validate(base_payload())
    failing_attempt = VideoJobService(
        settings=settings,
        session_factory=SessionLocal,
        attempts=FailingAttemptRepository(SessionLocal),
    )
    with pytest.raises(Exception):
        failing_attempt.create_video_job(
            owner_id=settings.owner_id,
            request=request,
            idempotency_key="fail-attempt",
            request_id="req_fail",
        )
    assert count_rows(SessionLocal, VideoJob) == 0
    assert count_rows(SessionLocal, GenerationRequestSnapshot) == 0

    asset_id = create_asset(SessionLocal)
    request_with_ref = CreateVideoJobRequest.model_validate(
            base_payload(
                generation_mode="I2V",
                reference_assets=[
                    reference_asset(
                        asset_id,
                        usage_role="FIRST_FRAME",
                        linked=[],
                        required=False,
                    )
                ],
            )
    )
    failing_refs = VideoJobService(
        settings=settings,
        session_factory=SessionLocal,
        job_asset_references=FailingJobAssetReferenceRepository(SessionLocal),
    )
    with pytest.raises(Exception):
        failing_refs.create_video_job(
            owner_id=settings.owner_id,
            request=request_with_ref,
            idempotency_key="fail-refs",
            request_id="req_fail_refs",
        )
    assert count_rows(SessionLocal, VideoJob) == 0
    assert count_rows(SessionLocal, JobAttempt) == 0
    assert count_rows(SessionLocal, GenerationRequestSnapshot) == 0
    assert count_rows(SessionLocal, JobAssetReference) == 0


def test_error_response_has_request_id_and_no_internal_secrets(tmp_path: Path) -> None:
    client, _, _ = client_for(tmp_path)

    response = client.post(
        "/v1/video-jobs",
        json=base_payload(truth_dependency="high"),
        headers=auth_headers("no-secrets"),
    )
    payload = response.json()

    assert payload["error"]["request_id"] == response.headers["x-request-id"]
    rendered = str(payload)
    assert "canonical_request_hash" not in rendered
    assert "Idempotency-Key" not in rendered
    assert "SELECT " not in rendered


def test_phase_2a_6_openapi_and_tables_boundary() -> None:
    app = create_app()
    paths = set(app.openapi()["paths"])
    import_models()

    assert paths == {"/health", "/v1/assets/upload-url", "/v1/video-jobs"}
    assert "/_internal/mock-uploads/{token}" not in paths
    assert "/_internal/mock-results/{token}" not in paths
    assert "/v1/video-jobs/{job_id}" not in paths
    assert "/v1/video-jobs/{job_id}/cancel" not in paths
    assert "/v1/video-jobs/{job_id}/retry" not in paths
    assert set(Base.metadata.tables) == APPROVED_TABLES
