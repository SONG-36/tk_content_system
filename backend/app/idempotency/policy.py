"""Idempotency response cache policy."""

from __future__ import annotations


class CachePolicy:
    """Centralized response caching rules for idempotency snapshots."""

    CACHEABLE_ERROR_CODES = {
        "SCHEMA_INVALID",
        "TRUTH_GATE_BLOCKED",
        "HYBRID_GATE_BLOCKED",
        "AI_PROOF_NOT_ALLOWED",
        "PROVIDER_UNSUPPORTED",
        "ASSET_TYPE_UNSUPPORTED",
        "ASSET_TOO_LARGE",
    }
    NON_CACHEABLE_ERROR_CODES = {
        "AUTH_REQUIRED",
        "AUTH_INVALID",
        "IDEMPOTENCY_KEY_REQUIRED",
        "IDEMPOTENCY_PENDING",
        "INTERNAL_ERROR",
        "PROVIDER_TRANSIENT_ERROR",
        "ASSET_NOT_READY",
        "ASSET_NOT_FOUND",
        "VERSION_CONFLICT",
        "JOB_INVALID_STATE",
        "JOB_NOT_RETRYABLE",
        "JOB_CANCEL_NOT_ALLOWED",
        "UNKNOWN_PROVIDER_STATE",
    }

    def is_cacheable(self, status_code: int, response_json: dict[str, object]) -> bool:
        if 200 <= status_code < 300:
            return True
        error = response_json.get("error")
        error_code = error.get("code") if isinstance(error, dict) else None
        if error_code in self.CACHEABLE_ERROR_CODES:
            return True
        if error_code in self.NON_CACHEABLE_ERROR_CODES:
            return False
        return False
