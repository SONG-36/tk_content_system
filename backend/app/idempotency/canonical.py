"""Canonical request hashing and Idempotency-Key validation."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Mapping, Optional

from pydantic import BaseModel

from app.idempotency.types import CanonicalRequest
from app.services.errors import IdempotencyKeyRequiredError

MAX_IDEMPOTENCY_KEY_LENGTH = 255


def _sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def validate_idempotency_key(idempotency_key: Optional[str]) -> str:
    """Validate a client key and return its stable SHA-256 hash."""

    if idempotency_key is None or idempotency_key.strip() == "":
        raise IdempotencyKeyRequiredError()
    if len(idempotency_key) > MAX_IDEMPOTENCY_KEY_LENGTH:
        raise IdempotencyKeyRequiredError(
            "Idempotency-Key exceeds the maximum length.",
            required_action="Use an Idempotency-Key of 255 characters or fewer.",
        )
    if any(ord(character) < 32 or ord(character) == 127 for character in idempotency_key):
        raise IdempotencyKeyRequiredError(
            "Idempotency-Key contains unsupported control characters.",
            required_action="Use visible ASCII or UTF-8 characters only.",
        )
    return hash_idempotency_key(idempotency_key)


def hash_idempotency_key(idempotency_key: str) -> str:
    """Hash the raw key without mixing body, route, or auth material."""

    return _sha256_hex(idempotency_key)


def _to_json_data(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return copy.deepcopy(value)


def _canonical_json(value: Any) -> str:
    return json.dumps(
        _to_json_data(value),
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def canonicalize_request(
    *,
    owner_id: str,
    http_method: str,
    route_template: str,
    path_params: Mapping[str, Any],
    request_body: Any,
) -> CanonicalRequest:
    """Build a deterministic hashable request representation.

    The Idempotency-Key is intentionally excluded. This function is pure: it does
    not access databases, read networks, or mutate caller-owned request objects.
    """

    normalized_path_params = {
        key: _to_json_data(path_params[key]) for key in sorted(path_params)
    }
    path_params_json = _canonical_json(normalized_path_params)
    canonical_payload = {
        "owner_id": owner_id,
        "http_method": http_method.upper(),
        "route_template": route_template,
        "path_params": normalized_path_params,
        "request_body": _to_json_data(request_body),
    }
    canonical_json = _canonical_json(canonical_payload)
    return CanonicalRequest(
        canonical_json=canonical_json,
        canonical_request_hash=_sha256_hex(canonical_json),
        path_params_hash=_sha256_hex(path_params_json),
    )
