from __future__ import annotations

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.db.base import Base, import_models
from app.db import types as db_types
from app.main import create_app
from app.schemas.assets import UploadUrlRequest, UploadUrlResponse
from app.schemas.enums import (
    AIReviewStatus,
    AssetKind,
    AssetStatus,
    AttemptStatus,
    ExecutionProvider,
    GenerationMode,
    GenerationStatus,
    IdempotencyStatus,
    ProductionType,
    ProviderNormalizedStatus,
    SelectedModel,
    SourceType,
    UsageRole,
)
from app.schemas.facts import SourceRef
from app.schemas.jobs import (
    AssetSummary,
    AttemptSummary,
    CancelJobRequest,
    CancelJobResponse,
    CreateVideoJobRequest,
    CreateVideoJobResponse,
    GetVideoJobResponse,
    HybridAiLayer,
    HybridLayers,
    HybridRealLayer,
    ReferenceAsset,
    ResultMediaSummary,
    RetryJobRequest,
    RetryJobResponse,
    StoredJobError,
)


def valid_request(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "contract_version": "v1",
        "expected_truth_rule_version": "truth-rules-v0.4",
        "selected_model": "Seedance",
        "execution_provider": "mock",
        "shot_number": "Shot 03",
        "production_type": "AI_GENERATION",
        "generation_mode": "T2V",
        "prompt": "Premium garage atmosphere.",
        "negative_constraints": [],
        "preservation_constraints": [],
        "reference_assets": [],
        "truth_dependency": "low",
        "duration_seconds": 8,
        "aspect_ratio": "9:16",
        "client_declared_facts": [
            {
                "client_fact_id": "cfact_1",
                "fact_type": "category",
                "subject": "product",
                "value": {"name": "vacuum"},
                "source_ref_ids": ["src_1"],
            }
        ],
        "source_refs": [
            {
                "source_ref_id": "src_1",
                "source_type": "USER_INPUT",
                "source_value": "User supplied product note.",
            }
        ],
        "proof_needs": [
            {
                "proof_need_id": "pneed_1",
                "shot_id": "Shot 03",
                "proof_type": "identity",
                "linked_client_fact_ids": ["cfact_1"],
                "required_evidence_refs": ["src_1"],
                "production_type": "AI_GENERATION",
                "presentation_layer": "AI_ENVIRONMENT",
            }
        ],
    }
    payload.update(overrides)
    return payload


def hybrid_layers() -> dict[str, object]:
    return {
        "real_layer": {
            "required": True,
            "description": "real product hand footage",
            "reference_asset_ids": ["asset_1"],
            "carries_proof_need_ids": ["pneed_1"],
        },
        "ai_layer": {
            "required": True,
            "description": "garage atmosphere",
            "allowed_roles": ["environment"],
            "prohibited_roles": ["core_product_proof"],
        },
        "ai_must_not_rewrite": ["product_shape"],
    }


def first_frame_asset(asset_id: str = "asset_1") -> dict[str, object]:
    return {
        "asset_id": asset_id,
        "usage_role": "FIRST_FRAME",
        "shot_number": "Shot 03",
        "linked_proof_need_ids": ["pneed_1"],
        "required_for_truth_gate": False,
        "preservation_locks": {},
    }


def last_frame_asset(asset_id: str = "asset_2") -> dict[str, object]:
    return {
        "asset_id": asset_id,
        "usage_role": "LAST_FRAME",
        "shot_number": "Shot 03",
        "linked_proof_need_ids": ["pneed_1"],
        "required_for_truth_gate": False,
        "preservation_locks": {},
    }


def assert_invalid(payload: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        CreateVideoJobRequest.model_validate(payload)


def test_all_valid_schema_models_serialize() -> None:
    now = datetime.now(timezone.utc)
    UploadUrlRequest(
        contract_version="v1",
        content_type="image/png",
        size_bytes=1,
        checksum_sha256="a" * 64,
        intended_usage_role=UsageRole.PRODUCT_IDENTITY,
    ).model_dump()
    UploadUrlResponse(
        asset_id="asset_1",
        upload_url="https://example.test/upload",
        upload_url_expires_at=now,
        idempotent_replay=False,
    ).model_dump()
    CreateVideoJobRequest.model_validate(valid_request()).model_dump()
    CreateVideoJobResponse(
        job_id="job_1",
        truth_rule_version="truth-rules-v0.4",
        provider_mapping_version="mock-provider-map-v0.4",
        idempotent_replay=False,
    ).model_dump()
    attempt = AttemptSummary(
        attempt_id="attempt_1",
        attempt_no=1,
        attempt_status=AttemptStatus.PREPARED,
        execution_provider=ExecutionProvider.mock,
        cancellation_intent=False,
        created_at=now,
        updated_at=now,
    )
    asset = AssetSummary(
        asset_id="asset_1",
        asset_kind=AssetKind.INPUT_MEDIA,
        asset_status=AssetStatus.READY,
        content_type="image/png",
        size_bytes=1,
        checksum_sha256="a" * 64,
        usage_role=UsageRole.PRODUCT_IDENTITY,
    )
    result = ResultMediaSummary(
        asset_id="asset_2",
        content_type="video/mp4",
        size_bytes=2,
        result_url="https://example.test/result",
        result_url_expires_at=now,
        checksum_sha256="b" * 64,
    )
    error = StoredJobError(code="MOCK", message="mock", created_at=now)
    GetVideoJobResponse(
        job_id="job_1",
        generation_status=GenerationStatus.QUEUED,
        current_attempt=attempt,
        assets=[asset],
        result_media=[result],
        errors=[error],
    ).model_dump()
    CancelJobRequest(reason="stop").model_dump()
    CancelJobResponse(
        job_id="job_1",
        generation_status=GenerationStatus.CANCELLED,
        attempt_status=AttemptStatus.CANCELLED,
        cancellation_intent=False,
        idempotent_replay=False,
    ).model_dump()
    RetryJobRequest(reason="retry").model_dump()
    RetryJobResponse(
        job_id="job_1",
        new_attempt_id="attempt_2",
        idempotent_replay=False,
    ).model_dump()


def test_request_models_reject_extra_fields() -> None:
    with pytest.raises(ValidationError):
        UploadUrlRequest(
            contract_version="v1",
            content_type="image/png",
            size_bytes=1,
            checksum_sha256="a" * 64,
            intended_usage_role=UsageRole.PRODUCT_IDENTITY,
            extra_field=True,
        )
    assert_invalid(valid_request(extra_field=True))


@pytest.mark.parametrize(
    "field",
    [
        "owner_id",
        "truth_rule_version",
        "provider_mapping_version",
        "verification_status",
        "trust_level",
        "backend_gate_result",
        "generation_status",
        "ai_review_status",
        "attempt_status",
        "provider_job_id",
        "provider_result",
        "scenario",
        "outcome",
    ],
)
def test_server_controlled_fields_are_rejected(field: str) -> None:
    assert_invalid(valid_request(**{field: "forbidden"}))


def test_upload_checksum_must_be_64_hex() -> None:
    with pytest.raises(ValidationError):
        UploadUrlRequest(
            contract_version="v1",
            content_type="image/png",
            size_bytes=1,
            checksum_sha256="not-a-checksum",
            intended_usage_role=UsageRole.PRODUCT_IDENTITY,
        )


def test_upload_size_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        UploadUrlRequest(
            contract_version="v1",
            content_type="image/png",
            size_bytes=0,
            checksum_sha256="a" * 64,
            intended_usage_role=UsageRole.PRODUCT_IDENTITY,
        )


def test_upload_response_rejects_non_http_url() -> None:
    with pytest.raises(ValidationError):
        UploadUrlResponse(
            asset_id="asset_1",
            upload_url="ftp://example.test/upload",
            upload_url_expires_at=datetime.now(timezone.utc),
            idempotent_replay=False,
        )


def test_duplicate_client_fact_id_rejected() -> None:
    payload = valid_request()
    payload["client_declared_facts"] = [
        payload["client_declared_facts"][0],  # type: ignore[index]
        payload["client_declared_facts"][0],  # type: ignore[index]
    ]
    assert_invalid(payload)


def test_duplicate_source_ref_id_rejected() -> None:
    payload = valid_request()
    payload["source_refs"] = [
        payload["source_refs"][0],  # type: ignore[index]
        payload["source_refs"][0],  # type: ignore[index]
    ]
    assert_invalid(payload)


def test_duplicate_proof_need_id_rejected() -> None:
    payload = valid_request()
    payload["proof_needs"] = [
        payload["proof_needs"][0],  # type: ignore[index]
        payload["proof_needs"][0],  # type: ignore[index]
    ]
    assert_invalid(payload)


def test_unknown_source_ref_rejected() -> None:
    payload = valid_request()
    payload["client_declared_facts"][0]["source_ref_ids"] = ["src_missing"]  # type: ignore[index]
    assert_invalid(payload)


def test_unknown_proof_need_ref_rejected() -> None:
    payload = valid_request(reference_assets=[first_frame_asset()])
    payload["reference_assets"][0]["linked_proof_need_ids"] = ["pneed_missing"]  # type: ignore[index]
    assert_invalid(payload)


def test_unknown_client_fact_ref_rejected() -> None:
    payload = valid_request()
    payload["proof_needs"][0]["linked_client_fact_ids"] = ["cfact_missing"]  # type: ignore[index]
    assert_invalid(payload)


def test_invalid_evidence_ref_prefix_rejected() -> None:
    payload = valid_request()
    payload["proof_needs"][0]["required_evidence_refs"] = ["bad_1"]  # type: ignore[index]
    assert_invalid(payload)


def test_shot_number_mismatch_rejected() -> None:
    payload = valid_request(reference_assets=[first_frame_asset()])
    payload["reference_assets"][0]["shot_number"] = "Shot 99"  # type: ignore[index]
    assert_invalid(payload)
    payload = valid_request()
    payload["proof_needs"][0]["shot_id"] = "Shot 99"  # type: ignore[index]
    assert_invalid(payload)


def test_production_type_mismatch_rejected() -> None:
    payload = valid_request()
    payload["proof_needs"][0]["production_type"] = "HYBRID"  # type: ignore[index]
    assert_invalid(payload)


def test_hybrid_requires_hybrid_layers() -> None:
    assert_invalid(valid_request(production_type="HYBRID"))


def test_ai_generation_must_not_include_hybrid_layers() -> None:
    assert_invalid(valid_request(hybrid_layers=hybrid_layers()))


def test_i2v_requires_first_frame_or_product_identity() -> None:
    assert_invalid(valid_request(generation_mode="I2V"))


def test_r2v_requires_reference_asset() -> None:
    assert_invalid(valid_request(generation_mode="R2V"))


def test_flf2v_requires_first_frame() -> None:
    assert_invalid(valid_request(generation_mode="FLF2V", reference_assets=[last_frame_asset()]))


def test_flf2v_requires_last_frame() -> None:
    assert_invalid(valid_request(generation_mode="FLF2V", reference_assets=[first_frame_asset()]))


def test_flf2v_rejects_duplicate_first_frame() -> None:
    assert_invalid(
        valid_request(
            generation_mode="FLF2V",
            reference_assets=[first_frame_asset("asset_1"), first_frame_asset("asset_2"), last_frame_asset("asset_3")],
        )
    )


def test_flf2v_rejects_duplicate_last_frame() -> None:
    assert_invalid(
        valid_request(
            generation_mode="FLF2V",
            reference_assets=[first_frame_asset("asset_1"), last_frame_asset("asset_2"), last_frame_asset("asset_3")],
        )
    )


def test_product_link_is_opaque_metadata(monkeypatch) -> None:
    def fail_network(*args: object, **kwargs: object) -> None:
        raise AssertionError("network should not be used")

    monkeypatch.setattr("urllib.request.urlopen", fail_network)
    SourceRef(
        source_ref_id="src_link",
        source_type=SourceType.PRODUCT_LINK,
        source_value="https://example.test/product",
    )


def enum_values(enum_cls: type) -> set[str]:
    return {item.value for item in enum_cls}


def test_api_enums_match_database_enums() -> None:
    assert enum_values(AssetKind) == enum_values(db_types.AssetKind)
    assert enum_values(AssetStatus) == enum_values(db_types.AssetStatus)
    assert enum_values(GenerationStatus) == enum_values(db_types.GenerationStatus)
    assert enum_values(AttemptStatus) == enum_values(db_types.AttemptStatus)
    assert enum_values(AIReviewStatus) == enum_values(db_types.AIReviewStatus)
    assert enum_values(IdempotencyStatus) == enum_values(db_types.IdempotencyStatus)
    assert enum_values(ProviderNormalizedStatus) == enum_values(db_types.ProviderNormalizedStatus)
    assert enum_values(ExecutionProvider) == {"mock"}
    assert enum_values(SelectedModel) == {"Seedance"}
    assert enum_values(ProductionType) == {"AI_GENERATION", "HYBRID"}
    assert enum_values(GenerationMode) == {"T2V", "I2V", "R2V", "FLF2V"}


def test_request_validation_error_uses_unified_422_envelope() -> None:
    app = create_app(include_test_routes=True)
    client = TestClient(app)

    response = client.post(
        "/_test/upload-url-schema",
        json={
            "contract_version": "v1",
            "content_type": "image/png",
            "size_bytes": 1,
            "checksum_sha256": "bad",
            "intended_usage_role": "PRODUCT_IDENTITY",
        },
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["error"]["code"] == "SCHEMA_INVALID"
    assert payload["error"]["field"] == "checksum_sha256"
    assert payload["error"]["request_id"] == response.headers["x-request-id"]
    assert payload["error"]["retryable"] is False
    assert payload["error"]["details"]["errors"]


def test_formal_api_routes_match_phase_2a_6_surface() -> None:
    app = create_app()
    schema_paths = set(app.openapi()["paths"])

    assert schema_paths == {
        "/health",
        "/v1/assets/upload-url",
        "/v1/video-jobs",
        "/v1/video-jobs/{job_id}",
        "/v1/video-jobs/{job_id}/cancel",
        "/v1/video-jobs/{job_id}/retry",
    }
    assert "/_internal/mock-uploads/{token}" not in schema_paths


def test_database_metadata_still_has_only_seven_tables() -> None:
    import_models()

    assert set(Base.metadata.tables) == {
        "assets",
        "video_jobs",
        "job_attempts",
        "generation_request_snapshots",
        "job_asset_references",
        "provider_results",
        "idempotency_records",
    }
