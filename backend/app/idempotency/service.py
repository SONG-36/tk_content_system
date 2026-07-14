"""Reusable idempotency service independent from business resources."""

from __future__ import annotations

import copy
import json
from datetime import timedelta
from typing import Any, Mapping, Optional

from sqlalchemy.exc import IntegrityError

from app.idempotency.canonical import canonicalize_request, validate_idempotency_key
from app.idempotency.repository import IdempotencyRepository, SessionFactory
from app.idempotency.types import (
    Clock,
    IdempotencyAcquireResult,
    IdempotencyDisposition,
    IdempotencyRecordSnapshot,
    IdempotencyScope,
    RecoveryResolver,
    RecoveryStatus,
    UtcClock,
    ensure_utc,
)
from app.services.errors import (
    IdempotencyConflictError,
    IdempotencyPendingError,
)


class IdempotencyService:
    """Coordinates request hashing, record lifecycle, replay, and recovery."""

    def __init__(
        self,
        *,
        repository: Optional[IdempotencyRepository] = None,
        session_factory: Optional[SessionFactory] = None,
        clock: Optional[Clock] = None,
        completed_ttl_hours: int = 24,
        pending_lease_seconds: int = 60,
        recovery_resolver: Optional[RecoveryResolver] = None,
    ) -> None:
        if repository is None and session_factory is None:
            raise ValueError("repository or session_factory is required.")
        self._repository = repository or IdempotencyRepository(session_factory)  # type: ignore[arg-type]
        self._clock = clock or UtcClock()
        self._completed_ttl = timedelta(hours=completed_ttl_hours)
        self._pending_lease = timedelta(seconds=pending_lease_seconds)
        self._recovery_resolver = recovery_resolver

    def acquire(
        self,
        *,
        owner_id: str,
        http_method: str,
        route_template: str,
        path_params: Mapping[str, Any],
        request_body: Any,
        idempotency_key: Optional[str],
    ) -> IdempotencyAcquireResult:
        now = self._now()
        key_hash = validate_idempotency_key(idempotency_key)
        canonical = canonicalize_request(
            owner_id=owner_id,
            http_method=http_method,
            route_template=route_template,
            path_params=path_params,
            request_body=request_body,
        )
        scope = IdempotencyScope(
            owner_id=owner_id,
            http_method=http_method.upper(),
            route_template=route_template,
            path_params_hash=canonical.path_params_hash,
            idempotency_key_hash=key_hash,
        )

        try:
            record = self._repository.create_pending(
                scope=scope,
                canonical_request_hash=canonical.canonical_request_hash,
                lease_expires_at=now + self._pending_lease,
                expires_at=now + self._completed_ttl,
                now=now,
            )
            return _acquired(record)
        except IntegrityError:
            record = self._repository.find_by_scope(scope)
            if record is None:
                raise
            return self._handle_existing(
                record=record,
                canonical_request_hash=canonical.canonical_request_hash,
                now=now,
            )

    def bind_resource(
        self,
        *,
        record_id: str,
        resource_type: str,
        resource_id: str,
    ) -> IdempotencyRecordSnapshot:
        if not resource_type or not resource_id:
            raise ValueError("resource_type and resource_id must both be set.")
        return self._repository.bind_resource(
            record_id=record_id,
            resource_type=resource_type,
            resource_id=resource_id,
            now=self._now(),
        )

    def complete(
        self,
        *,
        record_id: str,
        response_status_code: int,
        response_json: dict[str, Any],
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
    ) -> IdempotencyRecordSnapshot:
        normalized_response = _normalize_response_json(response_json)
        return self._repository.complete(
            record_id=record_id,
            response_status_code=response_status_code,
            response_json=normalized_response,
            resource_type=resource_type,
            resource_id=resource_id,
            expires_at=self._now() + self._completed_ttl,
            now=self._now(),
        )

    def _handle_existing(
        self,
        *,
        record: IdempotencyRecordSnapshot,
        canonical_request_hash: str,
        now,
    ) -> IdempotencyAcquireResult:
        if record.canonical_request_hash != canonical_request_hash:
            if record.status == "COMPLETED" and record.expires_at <= now:
                return self._reset_expired_completed(
                    record=record,
                    canonical_request_hash=canonical_request_hash,
                    now=now,
                )
            raise IdempotencyConflictError()

        if record.status == "COMPLETED":
            if record.expires_at <= now:
                return self._reset_expired_completed(
                    record=record,
                    canonical_request_hash=canonical_request_hash,
                    now=now,
                )
            return _replay(record)

        if record.status == "PENDING":
            lease_expires_at = (
                ensure_utc(record.lease_expires_at)
                if record.lease_expires_at is not None
                else now
            )
            if lease_expires_at > now:
                raise IdempotencyPendingError()
            return self._handle_expired_pending(
                record=record,
                canonical_request_hash=canonical_request_hash,
                now=now,
            )

        raise IdempotencyConflictError()

    def _handle_expired_pending(
        self,
        *,
        record: IdempotencyRecordSnapshot,
        canonical_request_hash: str,
        now,
    ) -> IdempotencyAcquireResult:
        clear_resource = False
        if record.resource_type is not None or record.resource_id is not None:
            if not record.resource_type or not record.resource_id:
                raise IdempotencyPendingError()
            if self._recovery_resolver is None:
                raise IdempotencyPendingError()
            recovered = self._recovery_resolver.recover(
                record.resource_type, record.resource_id
            )
            if recovered.status == RecoveryStatus.RECOVERED:
                completed = self.complete(
                    record_id=record.record_id,
                    response_status_code=recovered.response_status_code or 200,
                    response_json=recovered.response_json or {},
                    resource_type=record.resource_type,
                    resource_id=record.resource_id,
                )
                return _replay(completed)
            if recovered.status == RecoveryStatus.INCOMPLETE:
                raise IdempotencyPendingError()
            if recovered.status == RecoveryStatus.NOT_FOUND:
                clear_resource = True

        acquired = self._repository.acquire_expired_pending(
            record_id=record.record_id,
            canonical_request_hash=canonical_request_hash,
            lease_expires_at=now + self._pending_lease,
            now=now,
            clear_resource=clear_resource,
        )
        if acquired is None:
            raise IdempotencyPendingError()
        return _acquired(acquired)

    def _reset_expired_completed(
        self,
        *,
        record: IdempotencyRecordSnapshot,
        canonical_request_hash: str,
        now,
    ) -> IdempotencyAcquireResult:
        reset = self._repository.reset_expired_completed(
            record_id=record.record_id,
            canonical_request_hash=canonical_request_hash,
            lease_expires_at=now + self._pending_lease,
            expires_at=now + self._completed_ttl,
            now=now,
        )
        if reset is None:
            latest = self._repository.find_by_scope(record.scope)
            if latest is None:
                raise IdempotencyPendingError()
            return self._handle_existing(
                record=latest,
                canonical_request_hash=canonical_request_hash,
                now=now,
            )
        return _acquired(reset)

    def _now(self):
        return ensure_utc(self._clock.now())


def _acquired(record: IdempotencyRecordSnapshot) -> IdempotencyAcquireResult:
    return IdempotencyAcquireResult(
        disposition=IdempotencyDisposition.ACQUIRED,
        record_id=record.record_id,
        resource_type=record.resource_type,
        resource_id=record.resource_id,
        idempotent_replay=False,
    )


def _replay(record: IdempotencyRecordSnapshot) -> IdempotencyAcquireResult:
    response_json = copy.deepcopy(record.response_json)
    if isinstance(response_json, dict) and "idempotent_replay" in response_json:
        response_json["idempotent_replay"] = True
    return IdempotencyAcquireResult(
        disposition=IdempotencyDisposition.REPLAY,
        record_id=record.record_id,
        response_status_code=record.response_status_code,
        response_json=response_json,
        resource_type=record.resource_type,
        resource_id=record.resource_id,
        idempotent_replay=True,
    )


def _normalize_response_json(response_json: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(response_json, dict):
        raise TypeError("response_json must be a JSON object.")
    copied = copy.deepcopy(response_json)
    if "idempotent_replay" in copied:
        copied["idempotent_replay"] = False
    serialized = json.dumps(copied, ensure_ascii=False, allow_nan=False)
    return json.loads(serialized)
