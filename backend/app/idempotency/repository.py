"""Database repository for idempotency records."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import Select, delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.types import IdempotencyStatus, generate_prefixed_id
from app.idempotency.types import (
    IdempotencyRecordSnapshot,
    IdempotencyScope,
    ensure_utc,
)
from app.models.idempotency_record import IdempotencyRecord

SessionFactory = Callable[[], Session]


class IdempotencyRepository:
    """Owns short database transactions for idempotency records."""

    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def create_pending(
        self,
        *,
        scope: IdempotencyScope,
        canonical_request_hash: str,
        lease_expires_at: datetime,
        expires_at: datetime,
        now: datetime,
    ) -> IdempotencyRecordSnapshot:
        with self._session_factory() as session:
            record = IdempotencyRecord(
                idempotency_record_id=generate_prefixed_id("idem"),
                owner_id=scope.owner_id,
                http_method=scope.http_method,
                route_template=scope.route_template,
                path_params_hash=scope.path_params_hash,
                idempotency_key_hash=scope.idempotency_key_hash,
                canonical_request_hash=canonical_request_hash,
                status=IdempotencyStatus.PENDING,
                lease_expires_at=lease_expires_at,
                expires_at=expires_at,
                created_at=now,
                updated_at=now,
            )
            session.add(record)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                raise
            session.refresh(record)
            return _snapshot(record)

    def find_by_scope(
        self, scope: IdempotencyScope
    ) -> Optional[IdempotencyRecordSnapshot]:
        with self._session_factory() as session:
            record = session.scalar(_scope_query(scope))
            return _snapshot(record) if record is not None else None

    def acquire_expired_pending(
        self,
        *,
        record_id: str,
        canonical_request_hash: str,
        lease_expires_at: datetime,
        now: datetime,
        clear_resource: bool = False,
    ) -> Optional[IdempotencyRecordSnapshot]:
        values: dict[str, Any] = {
            "lease_expires_at": lease_expires_at,
            "updated_at": now,
        }
        if clear_resource:
            values.update({"resource_type": None, "resource_id": None})

        with self._session_factory() as session:
            result = session.execute(
                update(IdempotencyRecord)
                .where(IdempotencyRecord.idempotency_record_id == record_id)
                .where(IdempotencyRecord.status == IdempotencyStatus.PENDING)
                .where(
                    IdempotencyRecord.canonical_request_hash == canonical_request_hash
                )
                .where(IdempotencyRecord.lease_expires_at <= now)
                .values(**values)
            )
            session.commit()
            if result.rowcount != 1:
                return None
            record = session.get(IdempotencyRecord, record_id)
            return _snapshot(record) if record is not None else None

    def reset_expired_completed(
        self,
        *,
        record_id: str,
        canonical_request_hash: str,
        lease_expires_at: datetime,
        expires_at: datetime,
        now: datetime,
    ) -> Optional[IdempotencyRecordSnapshot]:
        with self._session_factory() as session:
            result = session.execute(
                update(IdempotencyRecord)
                .where(IdempotencyRecord.idempotency_record_id == record_id)
                .where(IdempotencyRecord.status == IdempotencyStatus.COMPLETED)
                .where(IdempotencyRecord.expires_at <= now)
                .values(
                    canonical_request_hash=canonical_request_hash,
                    status=IdempotencyStatus.PENDING,
                    lease_expires_at=lease_expires_at,
                    response_status_code=None,
                    response_json=None,
                    resource_type=None,
                    resource_id=None,
                    expires_at=expires_at,
                    updated_at=now,
                )
            )
            session.commit()
            if result.rowcount != 1:
                return None
            record = session.get(IdempotencyRecord, record_id)
            return _snapshot(record) if record is not None else None

    def bind_resource(
        self,
        *,
        record_id: str,
        resource_type: str,
        resource_id: str,
        now: datetime,
    ) -> IdempotencyRecordSnapshot:
        with self._session_factory() as session:
            record = session.get(IdempotencyRecord, record_id)
            if record is None:
                raise ValueError("Idempotency record not found.")
            if record.status != IdempotencyStatus.PENDING:
                raise ValueError("Only PENDING idempotency records can bind resources.")
            if record.resource_type is None and record.resource_id is None:
                record.resource_type = resource_type
                record.resource_id = resource_id
                record.updated_at = now
                session.commit()
                session.refresh(record)
                return _snapshot(record)
            if (
                record.resource_type == resource_type
                and record.resource_id == resource_id
            ):
                return _snapshot(record)
            raise ValueError("Idempotency record is already bound to another resource.")

    def bind_resource_in_session(
        self,
        session: Session,
        *,
        record_id: str,
        resource_type: str,
        resource_id: str,
        now: datetime,
    ) -> None:
        record = session.get(IdempotencyRecord, record_id)
        if record is None:
            raise ValueError("Idempotency record not found.")
        if record.status != IdempotencyStatus.PENDING:
            raise ValueError("Only PENDING idempotency records can bind resources.")
        if record.resource_type is None and record.resource_id is None:
            record.resource_type = resource_type
            record.resource_id = resource_id
            record.updated_at = now
            return
        if record.resource_type == resource_type and record.resource_id == resource_id:
            return
        raise ValueError("Idempotency record is already bound to another resource.")

    def complete(
        self,
        *,
        record_id: str,
        response_status_code: int,
        response_json: dict[str, Any],
        expires_at: datetime,
        now: datetime,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
    ) -> IdempotencyRecordSnapshot:
        with self._session_factory() as session:
            record = session.get(IdempotencyRecord, record_id)
            if record is None:
                raise ValueError("Idempotency record not found.")

            effective_resource_type = resource_type or record.resource_type
            effective_resource_id = resource_id or record.resource_id

            if record.status == IdempotencyStatus.COMPLETED:
                if (
                    record.response_status_code == response_status_code
                    and record.response_json == response_json
                    and record.resource_type == effective_resource_type
                    and record.resource_id == effective_resource_id
                ):
                    return _snapshot(record)
                raise ValueError("Completed idempotency response cannot be overwritten.")

            if record.status != IdempotencyStatus.PENDING:
                raise ValueError("Only PENDING idempotency records can be completed.")

            if resource_type is not None or resource_id is not None:
                if not resource_type or not resource_id:
                    raise ValueError("resource_type and resource_id must both be set.")
                if record.resource_type is None and record.resource_id is None:
                    record.resource_type = resource_type
                    record.resource_id = resource_id
                elif record.resource_type != resource_type or record.resource_id != resource_id:
                    raise ValueError("Idempotency record is bound to another resource.")

            record.status = IdempotencyStatus.COMPLETED
            record.lease_expires_at = None
            record.response_status_code = response_status_code
            record.response_json = response_json
            record.expires_at = expires_at
            record.updated_at = now
            session.commit()
            session.refresh(record)
            return _snapshot(record)

    def abandon_pending(self, record_id: str) -> bool:
        with self._session_factory() as session:
            result = session.execute(
                delete(IdempotencyRecord)
                .where(IdempotencyRecord.idempotency_record_id == record_id)
                .where(IdempotencyRecord.status == IdempotencyStatus.PENDING)
                .where(IdempotencyRecord.resource_type.is_(None))
                .where(IdempotencyRecord.resource_id.is_(None))
            )
            session.commit()
            return result.rowcount == 1


def _scope_query(scope: IdempotencyScope) -> Select[tuple[IdempotencyRecord]]:
    return select(IdempotencyRecord).where(
        IdempotencyRecord.owner_id == scope.owner_id,
        IdempotencyRecord.http_method == scope.http_method,
        IdempotencyRecord.route_template == scope.route_template,
        IdempotencyRecord.path_params_hash == scope.path_params_hash,
        IdempotencyRecord.idempotency_key_hash == scope.idempotency_key_hash,
    )


def _snapshot(record: IdempotencyRecord) -> IdempotencyRecordSnapshot:
    return IdempotencyRecordSnapshot(
        record_id=record.idempotency_record_id,
        scope=IdempotencyScope(
            owner_id=record.owner_id,
            http_method=record.http_method,
            route_template=record.route_template,
            path_params_hash=record.path_params_hash,
            idempotency_key_hash=record.idempotency_key_hash,
        ),
        canonical_request_hash=record.canonical_request_hash,
        status=record.status.value if isinstance(record.status, IdempotencyStatus) else record.status,
        lease_expires_at=(
            ensure_utc(record.lease_expires_at)
            if record.lease_expires_at is not None
            else None
        ),
        response_status_code=record.response_status_code,
        response_json=record.response_json,
        resource_type=record.resource_type,
        resource_id=record.resource_id,
        expires_at=ensure_utc(record.expires_at),
        created_at=ensure_utc(record.created_at),
        updated_at=ensure_utc(record.updated_at),
    )
