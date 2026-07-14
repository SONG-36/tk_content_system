"""initial phase 2a persistence

Revision ID: 20260714_0001
Revises:
Create Date: 2026-07-14 00:00:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260714_0001"
down_revision = None
branch_labels = None
depends_on = None


asset_kind = sa.Enum(
    "INPUT_MEDIA",
    "RESULT_MEDIA",
    "REFERENCE",
    name="asset_kind",
    native_enum=False,
    create_constraint=True,
)
asset_status = sa.Enum(
    "PENDING_UPLOAD",
    "READY",
    "FAILED",
    "EXPIRED",
    "DELETED",
    name="asset_status",
    native_enum=False,
    create_constraint=True,
)
generation_status = sa.Enum(
    "QUEUED",
    "PROCESSING",
    "SUCCEEDED",
    "FAILED",
    "CANCELLED",
    name="generation_status",
    native_enum=False,
    create_constraint=True,
)
ai_review_status = sa.Enum(
    "NOT_RUN",
    name="ai_review_status",
    native_enum=False,
    create_constraint=True,
)
attempt_status = sa.Enum(
    "PREPARED",
    "SUBMITTED",
    "PROCESSING",
    "SUCCEEDED",
    "FAILED",
    "CANCEL_REQUESTED",
    "CANCELLED",
    "UNKNOWN_PROVIDER_STATE",
    name="attempt_status",
    native_enum=False,
    create_constraint=True,
)
provider_normalized_status = sa.Enum(
    "SUCCEEDED",
    "FAILED",
    "UNKNOWN_PROVIDER_STATE",
    name="provider_normalized_status",
    native_enum=False,
    create_constraint=True,
)
idempotency_status = sa.Enum(
    "PENDING",
    "COMPLETED",
    name="idempotency_status",
    native_enum=False,
    create_constraint=True,
)


def upgrade() -> None:
    op.create_table(
        "assets",
        sa.Column("asset_id", sa.String(length=64), primary_key=True),
        sa.Column("owner_id", sa.String(length=128), nullable=False),
        sa.Column("asset_kind", asset_kind, nullable=False),
        sa.Column("status", asset_status, nullable=False),
        sa.Column("content_type", sa.String(length=255), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("checksum_sha256", sa.String(length=64), nullable=False),
        sa.Column("storage_path", sa.String(length=1024), nullable=True),
        sa.Column("upload_token_hash", sa.String(length=128), nullable=True),
        sa.Column("upload_token_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("upload_token_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("result_token_hash", sa.String(length=128), nullable=True),
        sa.Column("result_token_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_assets_owner_id", "assets", ["owner_id"])

    op.create_table(
        "video_jobs",
        sa.Column("job_id", sa.String(length=64), primary_key=True),
        sa.Column("owner_id", sa.String(length=128), nullable=False),
        sa.Column("contract_version", sa.String(length=32), nullable=False),
        sa.Column("truth_rule_version", sa.String(length=64), nullable=False),
        sa.Column("provider_mapping_version", sa.String(length=64), nullable=False),
        sa.Column("selected_model", sa.String(length=64), nullable=False),
        sa.Column("execution_provider", sa.String(length=64), nullable=False),
        sa.Column("generation_status", generation_status, nullable=False),
        sa.Column("ai_review_status", ai_review_status, nullable=False),
        sa.Column("current_attempt_id", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_video_jobs_owner_id", "video_jobs", ["owner_id"])
    op.create_index(
        "ix_video_jobs_current_attempt_id", "video_jobs", ["current_attempt_id"]
    )

    op.create_table(
        "job_attempts",
        sa.Column("attempt_id", sa.String(length=64), primary_key=True),
        sa.Column(
            "job_id",
            sa.String(length=64),
            sa.ForeignKey("video_jobs.job_id"),
            nullable=False,
        ),
        sa.Column("attempt_no", sa.Integer(), nullable=False),
        sa.Column("execution_provider", sa.String(length=64), nullable=False),
        sa.Column("provider_model", sa.String(length=128), nullable=True),
        sa.Column("provider_job_id", sa.String(length=128), nullable=True),
        sa.Column("attempt_status", attempt_status, nullable=False),
        sa.Column("cancellation_intent", sa.Boolean(), nullable=False, default=False),
        sa.Column("cancel_requested_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_code", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("terminal_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "job_id", "attempt_no", name="uq_job_attempts_job_attempt_no"
        ),
    )
    op.create_index("ix_job_attempts_job_id", "job_attempts", ["job_id"])

    op.create_table(
        "generation_request_snapshots",
        sa.Column("snapshot_id", sa.String(length=64), primary_key=True),
        sa.Column(
            "job_id",
            sa.String(length=64),
            sa.ForeignKey("video_jobs.job_id"),
            nullable=False,
            unique=True,
        ),
        sa.Column("canonical_request_hash", sa.String(length=128), nullable=False),
        sa.Column("request_json", sa.JSON(), nullable=False),
        sa.Column("gate_result_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "job_asset_references",
        sa.Column("job_asset_reference_id", sa.String(length=64), primary_key=True),
        sa.Column(
            "job_id",
            sa.String(length=64),
            sa.ForeignKey("video_jobs.job_id"),
            nullable=False,
        ),
        sa.Column(
            "asset_id",
            sa.String(length=64),
            sa.ForeignKey("assets.asset_id"),
            nullable=False,
        ),
        sa.Column("usage_role", sa.String(length=64), nullable=False),
        sa.Column("shot_number", sa.String(length=64), nullable=False),
        sa.Column("linked_proof_need_ids_json", sa.JSON(), nullable=False),
        sa.Column("required_for_truth_gate", sa.Boolean(), nullable=False, default=False),
        sa.Column("preservation_locks_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "job_id",
            "asset_id",
            "usage_role",
            "shot_number",
            name="uq_job_asset_references_job_asset_role_shot",
        ),
    )
    op.create_index("ix_job_asset_references_job_id", "job_asset_references", ["job_id"])
    op.create_index(
        "ix_job_asset_references_asset_id", "job_asset_references", ["asset_id"]
    )

    op.create_table(
        "provider_results",
        sa.Column("provider_result_id", sa.String(length=64), primary_key=True),
        sa.Column(
            "attempt_id",
            sa.String(length=64),
            sa.ForeignKey("job_attempts.attempt_id"),
            nullable=False,
            unique=True,
        ),
        sa.Column("normalized_status", provider_normalized_status, nullable=False),
        sa.Column("result_asset_ids_json", sa.JSON(), nullable=False),
        sa.Column("raw_payload_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "idempotency_records",
        sa.Column("idempotency_record_id", sa.String(length=64), primary_key=True),
        sa.Column("owner_id", sa.String(length=128), nullable=False),
        sa.Column("http_method", sa.String(length=16), nullable=False),
        sa.Column("route_template", sa.String(length=255), nullable=False),
        sa.Column("path_params_hash", sa.String(length=128), nullable=False),
        sa.Column("idempotency_key_hash", sa.String(length=128), nullable=False),
        sa.Column("canonical_request_hash", sa.String(length=128), nullable=False),
        sa.Column("status", idempotency_status, nullable=False),
        sa.Column("lease_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("response_status_code", sa.Integer(), nullable=True),
        sa.Column("response_json", sa.JSON(), nullable=True),
        sa.Column("resource_type", sa.String(length=64), nullable=True),
        sa.Column("resource_id", sa.String(length=64), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "owner_id",
            "http_method",
            "route_template",
            "path_params_hash",
            "idempotency_key_hash",
            name="uq_idempotency_scope",
        ),
    )
    op.create_index(
        "ix_idempotency_records_owner_id", "idempotency_records", ["owner_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_idempotency_records_owner_id", table_name="idempotency_records")
    op.drop_table("idempotency_records")
    op.drop_table("provider_results")
    op.drop_index("ix_job_asset_references_asset_id", table_name="job_asset_references")
    op.drop_index("ix_job_asset_references_job_id", table_name="job_asset_references")
    op.drop_table("job_asset_references")
    op.drop_table("generation_request_snapshots")
    op.drop_index("ix_job_attempts_job_id", table_name="job_attempts")
    op.drop_table("job_attempts")
    op.drop_index("ix_video_jobs_current_attempt_id", table_name="video_jobs")
    op.drop_index("ix_video_jobs_owner_id", table_name="video_jobs")
    op.drop_table("video_jobs")
    op.drop_index("ix_assets_owner_id", table_name="assets")
    op.drop_table("assets")
