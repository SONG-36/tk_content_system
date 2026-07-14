"""SQLAlchemy declarative base and metadata imports."""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def import_models() -> None:
    """Import ORM models so Alembic can see all table metadata."""

    import app.models.asset  # noqa: F401
    import app.models.generation_request_snapshot  # noqa: F401
    import app.models.idempotency_record  # noqa: F401
    import app.models.job_asset_reference  # noqa: F401
    import app.models.job_attempt  # noqa: F401
    import app.models.provider_result  # noqa: F401
    import app.models.video_job  # noqa: F401
