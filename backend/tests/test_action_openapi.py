from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_DIR / "backend"
OPENAPI_PATH = BACKEND_DIR / "openapi" / "custom_gpt_action.openapi.yaml"
EXPORT_SCRIPT = BACKEND_DIR / "tools" / "export_action_openapi.py"

EXPECTED_OPERATIONS = {
    ("get", "/health"): ("healthCheck", {"200", "500"}),
    ("post", "/v1/assets/upload-url"): (
        "createAssetUploadUrl",
        {"201", "401", "409", "413", "415", "422", "500"},
    ),
    ("post", "/v1/video-jobs"): (
        "createVideoJob",
        {"202", "401", "409", "422", "500"},
    ),
    ("get", "/v1/video-jobs/{job_id}"): (
        "getVideoJob",
        {"200", "401", "404", "500"},
    ),
    ("post", "/v1/video-jobs/{job_id}/cancel"): (
        "cancelVideoJob",
        {"200", "202", "401", "404", "409", "422", "500"},
    ),
    ("post", "/v1/video-jobs/{job_id}/retry"): (
        "retryVideoJob",
        {"202", "401", "404", "409", "422", "500"},
    ),
}

SIDE_EFFECT_PATHS = {
    "/v1/assets/upload-url",
    "/v1/video-jobs",
    "/v1/video-jobs/{job_id}/cancel",
    "/v1/video-jobs/{job_id}/retry",
}


def load_schema() -> dict:
    subprocess.run([sys.executable, str(EXPORT_SCRIPT)], cwd=REPO_DIR, check=True)
    return json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))


def test_action_openapi_export_is_deterministic() -> None:
    subprocess.run([sys.executable, str(EXPORT_SCRIPT)], cwd=REPO_DIR, check=True)
    first = OPENAPI_PATH.read_bytes()
    subprocess.run([sys.executable, str(EXPORT_SCRIPT)], cwd=REPO_DIR, check=True)
    second = OPENAPI_PATH.read_bytes()

    assert first == second
    assert hashlib.sha256(first).hexdigest() == hashlib.sha256(second).hexdigest()


def test_action_openapi_paths_operation_ids_security_and_headers() -> None:
    schema = load_schema()

    assert set(schema["paths"]) == {path for _, path in EXPECTED_OPERATIONS}
    assert "/_internal/mock-uploads/{token}" not in schema["paths"]
    assert "/_internal/mock-results/{token}" not in schema["paths"]
    assert schema["components"]["securitySchemes"]["BearerAuth"] == {
        "type": "http",
        "scheme": "bearer",
    }

    operation_ids = []
    for (method, path), (operation_id, status_codes) in EXPECTED_OPERATIONS.items():
        operation = schema["paths"][path][method]
        operation_ids.append(operation["operationId"])
        assert operation["operationId"] == operation_id
        assert set(operation["responses"]) == status_codes
        if path == "/health":
            assert "security" not in operation
        else:
            assert operation["security"] == [{"BearerAuth": []}]
        headers = [
            parameter
            for parameter in operation.get("parameters", [])
            if parameter.get("in") == "header"
            and parameter.get("name") == "Idempotency-Key"
        ]
        if path in SIDE_EFFECT_PATHS:
            assert len(headers) == 1
            assert headers[0]["required"] is True
            assert headers[0]["schema"]["minLength"] == 1
            assert headers[0]["schema"]["maxLength"] == 255
        else:
            assert headers == []

    assert len(operation_ids) == 6
    assert len(set(operation_ids)) == 6


def test_action_openapi_schema_contract_and_error_responses() -> None:
    schema = load_schema()
    schemas = schema["components"]["schemas"]

    assert schemas["SelectedModel"]["enum"] == ["Seedance"]
    assert schemas["ExecutionProvider"]["enum"] == ["mock"]
    assert schemas["ProductionType"]["enum"] == ["AI_GENERATION", "HYBRID"]
    assert schemas["GenerationMode"]["enum"] == ["T2V", "I2V", "R2V", "FLF2V"]
    assert schemas["CreateVideoJobRequest"]["additionalProperties"] is False
    assert schemas["CreateVideoJobRequest"]["properties"]["contract_version"]["enum"] == ["v1"]
    assert schemas["CreateVideoJobRequest"]["properties"]["aspect_ratio"]["enum"] == ["9:16"]
    assert schemas["ProofNeed"]["properties"]["production_type"]["$ref"] == "#/components/schemas/ProductionType"

    forbidden_request_fields = {
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
        "upload_token_hash",
        "result_token_hash",
        "storage_path",
    }
    assert not forbidden_request_fields & set(
        schemas["CreateVideoJobRequest"]["properties"]
    )

    for required_schema in {
        "UploadUrlResponse",
        "CreateVideoJobResponse",
        "GetVideoJobResponse",
        "CancelJobResponse",
        "RetryJobResponse",
        "ErrorResponse",
        "AttemptSummary",
        "AssetSummary",
        "ResultMediaSummary",
        "StoredJobError",
    }:
        assert required_schema in schemas

    for path, methods in schema["paths"].items():
        for method, operation in methods.items():
            for status_code, response in operation["responses"].items():
                if status_code.startswith(("4", "5")):
                    assert response["content"]["application/json"]["schema"] == {
                        "$ref": "#/components/schemas/ErrorResponse"
                    }


def test_action_openapi_does_not_expose_secrets_or_internal_paths() -> None:
    raw = OPENAPI_PATH.read_text(encoding="utf-8")
    forbidden_text = [
        "dev-api-key",
        "secret",
        "result_token_secret",
        "idempotency key",
        "token_hash",
        "storage_path",
        "/Users/",
        "sqlite://",
        "backend.db",
        "mock_result.mp4",
        "scenario",
        "outcome",
        "ByteDance",
        "BytePlus",
        "Seedance API",
    ]
    for token in forbidden_text:
        assert token not in raw
