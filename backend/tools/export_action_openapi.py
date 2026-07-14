#!/usr/bin/env python3
"""Export the Phase 2A Custom GPT Action OpenAPI artifact.

The backend implementation remains the source of truth. This script derives the
schema from FastAPI/Pydantic, filters out internal routes, and normalizes the
Action-specific contract deterministically.
"""

from __future__ import annotations

import copy
import json
import os
import sys
from pathlib import Path
from typing import Any

BACKEND_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = BACKEND_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.config import Settings  # noqa: E402
from app.main import create_app  # noqa: E402
from app.schemas.assets import UploadUrlResponse  # noqa: E402
from app.schemas.common import ErrorResponse, HealthResponse  # noqa: E402
from app.schemas.jobs import (  # noqa: E402
    AssetSummary,
    AttemptSummary,
    CancelJobResponse,
    CreateVideoJobResponse,
    GetVideoJobResponse,
    ResultMediaSummary,
    RetryJobResponse,
    StoredJobError,
)

OUTPUT_PATH = BACKEND_DIR / "openapi" / "custom_gpt_action.openapi.yaml"

ACTION_OPERATIONS = {
    ("GET", "/health"): ("healthCheck", {"200", "500"}, "HealthResponse"),
    (
        "POST",
        "/v1/assets/upload-url",
    ): (
        "createAssetUploadUrl",
        {"201", "401", "409", "413", "415", "422", "500"},
        "UploadUrlResponse",
    ),
    (
        "POST",
        "/v1/video-jobs",
    ): (
        "createVideoJob",
        {"202", "401", "409", "422", "500"},
        "CreateVideoJobResponse",
    ),
    (
        "GET",
        "/v1/video-jobs/{job_id}",
    ): (
        "getVideoJob",
        {"200", "401", "404", "500"},
        "GetVideoJobResponse",
    ),
    (
        "POST",
        "/v1/video-jobs/{job_id}/cancel",
    ): (
        "cancelVideoJob",
        {"200", "202", "401", "404", "409", "422", "500"},
        "CancelJobResponse",
    ),
    (
        "POST",
        "/v1/video-jobs/{job_id}/retry",
    ): (
        "retryVideoJob",
        {"202", "401", "404", "409", "422", "500"},
        "RetryJobResponse",
    ),
}

SUCCESS_RESPONSE_BY_STATUS = {
    "200": "Successful Response",
    "201": "Created",
    "202": "Accepted",
}

RESPONSE_MODELS = {
    "HealthResponse": HealthResponse,
    "UploadUrlResponse": UploadUrlResponse,
    "CreateVideoJobResponse": CreateVideoJobResponse,
    "GetVideoJobResponse": GetVideoJobResponse,
    "CancelJobResponse": CancelJobResponse,
    "RetryJobResponse": RetryJobResponse,
    "ErrorResponse": ErrorResponse,
    "AttemptSummary": AttemptSummary,
    "AssetSummary": AssetSummary,
    "ResultMediaSummary": ResultMediaSummary,
    "StoredJobError": StoredJobError,
}


def export_action_openapi() -> dict[str, Any]:
    settings = Settings(
        public_base_url=os.getenv("BACKEND_PUBLIC_BASE_URL", "http://localhost:8000"),
    )
    schema = create_app(settings_override=settings).openapi()
    action_schema: dict[str, Any] = {
        "openapi": schema["openapi"],
        "info": {
            "title": "TikTok Shop Product Video Backend Action API",
            "version": "v1",
            "description": (
                "Phase 2A mock backend Action contract. Backend design version 1.0; "
                "API contract v1; mock provider only."
            ),
        },
        "servers": [{"url": settings.public_base_url}],
        "paths": {},
        "components": {
            "schemas": copy.deepcopy(schema.get("components", {}).get("schemas", {})),
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                }
            },
        },
    }

    _ensure_response_models(action_schema)
    _normalize_fixed_request_fields(action_schema)
    for (method, path), (operation_id, status_codes, success_model) in sorted(
        ACTION_OPERATIONS.items(), key=lambda item: (item[0][1], item[0][0])
    ):
        lower_method = method.lower()
        operation = copy.deepcopy(schema["paths"][path][lower_method])
        operation["operationId"] = operation_id
        if path != "/health":
            operation["security"] = [{"BearerAuth": []}]
        operation["responses"] = _responses_for(status_codes, success_model)
        if method == "POST":
            _ensure_idempotency_header(operation)
        else:
            _remove_idempotency_header(operation)
        action_schema["paths"].setdefault(path, {})[lower_method] = operation

    return _sort_recursively(action_schema)


def write_action_openapi() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    schema = export_action_openapi()
    OUTPUT_PATH.write_text(
        json.dumps(schema, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _ensure_response_models(schema: dict[str, Any]) -> None:
    schemas = schema["components"]["schemas"]
    for name, model in RESPONSE_MODELS.items():
        model_schema = model.model_json_schema(ref_template="#/components/schemas/{model}")
        defs = model_schema.pop("$defs", {})
        schemas[name] = model_schema
        for def_name, def_schema in defs.items():
            schemas.setdefault(def_name, def_schema)


def _normalize_fixed_request_fields(schema: dict[str, Any]) -> None:
    schemas = schema["components"]["schemas"]
    for schema_name in {"CreateVideoJobRequest", "UploadUrlRequest"}:
        contract_version = schemas[schema_name]["properties"]["contract_version"]
        contract_version["enum"] = ["v1"]
        contract_version["default"] = "v1"
    aspect_ratio = schemas["CreateVideoJobRequest"]["properties"]["aspect_ratio"]
    aspect_ratio["enum"] = ["9:16"]
    aspect_ratio["default"] = "9:16"


def _responses_for(status_codes: set[str], success_model: str) -> dict[str, Any]:
    responses: dict[str, Any] = {}
    for status_code in sorted(status_codes, key=int):
        if status_code in {"200", "201", "202"}:
            model = success_model
            description = SUCCESS_RESPONSE_BY_STATUS[status_code]
        else:
            model = "ErrorResponse"
            description = "Error Response"
        responses[status_code] = {
            "description": description,
            "content": {
                "application/json": {
                    "schema": {"$ref": f"#/components/schemas/{model}"}
                }
            },
        }
    return responses


def _ensure_idempotency_header(operation: dict[str, Any]) -> None:
    parameters = [
        parameter
        for parameter in operation.get("parameters", [])
        if parameter.get("name") != "Idempotency-Key"
    ]
    parameters.append(
        {
            "name": "Idempotency-Key",
            "in": "header",
            "required": True,
            "schema": {
                "type": "string",
                "minLength": 1,
                "maxLength": 255,
                "title": "Idempotency-Key",
            },
        }
    )
    operation["parameters"] = sorted(
        parameters,
        key=lambda item: (item.get("in", ""), item.get("name", "")),
    )


def _remove_idempotency_header(operation: dict[str, Any]) -> None:
    parameters = [
        parameter
        for parameter in operation.get("parameters", [])
        if parameter.get("name") != "Idempotency-Key"
    ]
    if parameters:
        operation["parameters"] = parameters
    else:
        operation.pop("parameters", None)


def _sort_recursively(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _sort_recursively(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [_sort_recursively(item) for item in value]
    return value


if __name__ == "__main__":
    write_action_openapi()
