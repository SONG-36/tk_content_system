from __future__ import annotations

from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy.orm import Session, sessionmaker

from app.db.session import create_db_engine
from app.db.types import (
    AIReviewStatus,
    AssetKind,
    AssetStatus,
    AttemptStatus,
    GenerationStatus,
    IdempotencyStatus,
    ProviderNormalizedStatus,
    utc_now,
)
from app.main import create_app
from app.models import (
    Asset,
    GenerationRequestSnapshot,
    IdempotencyRecord,
    JobAttempt,
    ProviderResult,
    VideoJob,
)

APPROVED_TABLES = {
    "alembic_version",
    "assets",
    "video_jobs",
    "job_attempts",
    "generation_request_snapshots",
    "job_asset_references",
    "provider_results",
    "idempotency_records",
}


def alembic_config(database_url: str) -> Config:
    backend_dir = Path(__file__).resolve().parents[1]
    config = Config(str(backend_dir / "alembic.ini"))
    config.set_main_option("script_location", str(backend_dir / "alembic"))
    config.set_main_option("sqlalchemy.url", database_url)
    return config


def sqlite_url(tmp_path: Path) -> str:
    return f"sqlite:///{tmp_path / 'phase2a.db'}"


def upgrade(database_url: str) -> None:
    command.upgrade(alembic_config(database_url), "head")


def downgrade(database_url: str) -> None:
    command.downgrade(alembic_config(database_url), "base")


def session_for(database_url: str) -> Session:
    engine = create_db_engine(database_url)
    SessionLocal = sessionmaker(bind=engine, future=True)
    return SessionLocal()


def create_job(session: Session, job_id: str = "job_1") -> VideoJob:
    job = VideoJob(
        job_id=job_id,
        owner_id="owner_1",
        contract_version="v1",
        truth_rule_version="truth-rules-v0.4",
        provider_mapping_version="mock-provider-map-v0.4",
        selected_model="Seedance",
        execution_provider="mock",
        generation_status=GenerationStatus.QUEUED,
        ai_review_status=AIReviewStatus.NOT_RUN,
    )
    session.add(job)
    session.commit()
    return job


def test_alembic_upgrade_head_and_downgrade_base(tmp_path: Path) -> None:
    database_url = sqlite_url(tmp_path)

    upgrade(database_url)
    engine = create_db_engine(database_url)
    assert set(inspect(engine).get_table_names()) == APPROVED_TABLES

    downgrade(database_url)
    remaining = set(inspect(create_db_engine(database_url)).get_table_names())
    assert remaining <= {"alembic_version"}


def test_upgrade_creates_only_approved_tables(tmp_path: Path) -> None:
    database_url = sqlite_url(tmp_path)
    upgrade(database_url)

    table_names = set(inspect(create_db_engine(database_url)).get_table_names())

    assert table_names == APPROVED_TABLES
    assert "client_declared_facts" not in table_names
    assert "source_refs" not in table_names
    assert "proof_needs" not in table_names
    assert "truth_gate_decisions" not in table_names
    assert "hybrid_gate_decisions" not in table_names
    assert "backend_facts" not in table_names
    assert "verification_records" not in table_names
    assert "review_results" not in table_names
    assert "error_records" not in table_names


def test_sqlite_foreign_keys_enabled(tmp_path: Path) -> None:
    database_url = sqlite_url(tmp_path)
    upgrade(database_url)
    engine = create_db_engine(database_url)

    with engine.connect() as connection:
        enabled = connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one()

    assert enabled == 1


def test_asset_persists_across_sessions(tmp_path: Path) -> None:
    database_url = sqlite_url(tmp_path)
    upgrade(database_url)

    with session_for(database_url) as session:
        session.add(
            Asset(
                asset_id="asset_1",
                owner_id="owner_1",
                asset_kind=AssetKind.INPUT_MEDIA,
                status=AssetStatus.READY,
                content_type="image/png",
                size_bytes=10,
                checksum_sha256="a" * 64,
            )
        )
        session.commit()

    with session_for(database_url) as session:
        asset = session.get(Asset, "asset_1")

    assert asset is not None
    assert asset.owner_id == "owner_1"
    assert asset.status == AssetStatus.READY


def test_generation_request_snapshot_json_roundtrip(tmp_path: Path) -> None:
    database_url = sqlite_url(tmp_path)
    upgrade(database_url)

    with session_for(database_url) as session:
        create_job(session)
        snapshot = GenerationRequestSnapshot(
            snapshot_id="snapshot_1",
            job_id="job_1",
            canonical_request_hash="hash",
            request_json={
                "client_declared_facts": [{"client_fact_id": "cfact_1"}],
                "source_refs": [{"source_ref_id": "src_1"}],
                "proof_needs": [{"proof_need_id": "pneed_1"}],
            },
            gate_result_json={
                "truth_gate": {"result": "ALLOW"},
                "hybrid_gate": {"result": "ALLOW"},
            },
        )
        session.add(snapshot)
        session.commit()
        loaded = session.get(GenerationRequestSnapshot, "snapshot_1")

    assert loaded is not None
    assert loaded.request_json["proof_needs"][0]["proof_need_id"] == "pneed_1"
    assert loaded.gate_result_json["truth_gate"]["result"] == "ALLOW"


def test_provider_result_json_roundtrip(tmp_path: Path) -> None:
    database_url = sqlite_url(tmp_path)
    upgrade(database_url)

    with session_for(database_url) as session:
        create_job(session)
        session.add(
            JobAttempt(
                attempt_id="attempt_1",
                job_id="job_1",
                attempt_no=1,
                execution_provider="mock",
                attempt_status=AttemptStatus.SUCCEEDED,
            )
        )
        session.commit()
        session.add(
            ProviderResult(
                provider_result_id="pr_1",
                attempt_id="attempt_1",
                normalized_status=ProviderNormalizedStatus.SUCCEEDED,
                result_asset_ids_json=["asset_result_1"],
                raw_payload_json={"mock": True},
            )
        )
        session.commit()
        loaded = session.get(ProviderResult, "pr_1")

    assert loaded is not None
    assert loaded.result_asset_ids_json == ["asset_result_1"]
    assert loaded.raw_payload_json == {"mock": True}


def test_job_attempt_unique_job_id_attempt_no(tmp_path: Path) -> None:
    database_url = sqlite_url(tmp_path)
    upgrade(database_url)

    with pytest.raises(IntegrityError):
        with session_for(database_url) as session:
            create_job(session)
            session.add_all(
                [
                    JobAttempt(
                        attempt_id="attempt_1",
                        job_id="job_1",
                        attempt_no=1,
                        execution_provider="mock",
                        attempt_status=AttemptStatus.PREPARED,
                    ),
                    JobAttempt(
                        attempt_id="attempt_2",
                        job_id="job_1",
                        attempt_no=1,
                        execution_provider="mock",
                        attempt_status=AttemptStatus.PREPARED,
                    ),
                ]
            )
            session.commit()


def test_idempotency_scope_unique_constraint(tmp_path: Path) -> None:
    database_url = sqlite_url(tmp_path)
    upgrade(database_url)

    now = utc_now()
    with pytest.raises(IntegrityError):
        with session_for(database_url) as session:
            session.add_all(
                [
                    IdempotencyRecord(
                        idempotency_record_id="idem_1",
                        owner_id="owner_1",
                        http_method="POST",
                        route_template="/v1/video-jobs",
                        path_params_hash="path",
                        idempotency_key_hash="key",
                        canonical_request_hash="body1",
                        status=IdempotencyStatus.PENDING,
                        expires_at=now,
                    ),
                    IdempotencyRecord(
                        idempotency_record_id="idem_2",
                        owner_id="owner_1",
                        http_method="POST",
                        route_template="/v1/video-jobs",
                        path_params_hash="path",
                        idempotency_key_hash="key",
                        canonical_request_hash="body1",
                        status=IdempotencyStatus.PENDING,
                        expires_at=now,
                    ),
                ]
            )
            session.commit()


def test_invalid_enum_value_cannot_be_saved(tmp_path: Path) -> None:
    database_url = sqlite_url(tmp_path)
    upgrade(database_url)

    with pytest.raises(StatementError):
        with session_for(database_url) as session:
            session.add(
                Asset(
                    asset_id="asset_bad",
                    owner_id="owner_1",
                    asset_kind=AssetKind.INPUT_MEDIA,
                    status="INVALID_STATUS",
                    content_type="image/png",
                    size_bytes=10,
                    checksum_sha256="b" * 64,
                )
            )
            session.commit()


def test_invalid_foreign_key_fails(tmp_path: Path) -> None:
    database_url = sqlite_url(tmp_path)
    upgrade(database_url)

    with pytest.raises(IntegrityError):
        with session_for(database_url) as session:
            session.add(
                JobAttempt(
                    attempt_id="attempt_missing_job",
                    job_id="job_missing",
                    attempt_no=1,
                    execution_provider="mock",
                    attempt_status=AttemptStatus.PREPARED,
                )
            )
            session.commit()


def test_transaction_rollback_leaves_no_partial_write(tmp_path: Path) -> None:
    database_url = sqlite_url(tmp_path)
    upgrade(database_url)

    with session_for(database_url) as session:
        session.add(
            Asset(
                asset_id="asset_rollback",
                owner_id="owner_1",
                asset_kind=AssetKind.INPUT_MEDIA,
                status=AssetStatus.READY,
                content_type="image/png",
                size_bytes=10,
                checksum_sha256="c" * 64,
            )
        )
        session.add(
            JobAttempt(
                attempt_id="attempt_bad_fk",
                job_id="job_missing",
                attempt_no=1,
                execution_provider="mock",
                attempt_status=AttemptStatus.PREPARED,
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

    with session_for(database_url) as session:
        assert session.get(Asset, "asset_rollback") is None


def test_only_create_video_job_route_added() -> None:
    app = create_app()
    schema_paths = set(app.openapi()["paths"])

    assert schema_paths == {"/health", "/v1/assets/upload-url", "/v1/video-jobs"}
    assert "/v1/video-jobs/{job_id}" not in schema_paths
