"""Stateless signed result URL tokens for Phase 2A mock results."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from app.config import Settings
from app.idempotency.types import Clock, UtcClock, ensure_utc
from app.services.errors import ResultTokenInvalidError, ResultUrlExpiredError


@dataclass(frozen=True)
class ResultTokenPayload:
    purpose: str
    asset_id: str
    owner_id: str
    expires_at: datetime


class ResultTokenService:
    """Generates and verifies stateless HMAC result tokens."""

    PURPOSE = "mock_result"

    def __init__(self, *, settings: Settings, clock: Optional[Clock] = None) -> None:
        self._settings = settings
        self._clock = clock or UtcClock()

    def issue(self, *, asset_id: str, owner_id: str) -> tuple[str, datetime]:
        expires_at = ensure_utc(self._clock.now()) + timedelta(
            hours=self._settings.result_token_ttl_hours
        )
        payload = {
            "purpose": self.PURPOSE,
            "asset_id": asset_id,
            "owner_id": owner_id,
            "expires_at": int(expires_at.timestamp()),
        }
        payload_bytes = _json_bytes(payload)
        payload_part = _b64encode(payload_bytes)
        signature_part = _b64encode(self._sign(payload_part.encode("ascii")))
        return f"{payload_part}.{signature_part}", expires_at

    def verify(self, token: str) -> ResultTokenPayload:
        try:
            payload_part, signature_part = token.split(".", 1)
        except ValueError as exc:
            raise ResultTokenInvalidError() from exc
        expected_signature = _b64encode(self._sign(payload_part.encode("ascii")))
        if not hmac.compare_digest(signature_part, expected_signature):
            raise ResultTokenInvalidError()
        try:
            payload = json.loads(_b64decode(payload_part))
        except Exception as exc:
            raise ResultTokenInvalidError() from exc
        if payload.get("purpose") != self.PURPOSE:
            raise ResultTokenInvalidError()
        asset_id = payload.get("asset_id")
        owner_id = payload.get("owner_id")
        expires_at_raw = payload.get("expires_at")
        if not isinstance(asset_id, str) or not isinstance(owner_id, str):
            raise ResultTokenInvalidError()
        if not isinstance(expires_at_raw, int):
            raise ResultTokenInvalidError()
        expires_at = datetime.fromtimestamp(expires_at_raw, tz=timezone.utc)
        if expires_at <= ensure_utc(self._clock.now()):
            raise ResultUrlExpiredError()
        return ResultTokenPayload(
            purpose=self.PURPOSE,
            asset_id=asset_id,
            owner_id=owner_id,
            expires_at=expires_at,
        )

    def _sign(self, payload_part: bytes) -> bytes:
        return hmac.new(
            self._settings.result_token_secret.encode("utf-8"),
            payload_part,
            hashlib.sha256,
        ).digest()


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("ascii"))
