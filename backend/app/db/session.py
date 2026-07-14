"""SQLAlchemy engine and session helpers."""

from __future__ import annotations

from collections.abc import Generator
from typing import Optional

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings


def _is_sqlite_url(database_url: str) -> bool:
    return database_url.startswith("sqlite:")


def create_db_engine(database_url: Optional[str] = None) -> Engine:
    """Create a SQLAlchemy engine with SQLite-safe defaults."""

    url = database_url or get_settings().database_url
    connect_args = {"check_same_thread": False} if _is_sqlite_url(url) else {}
    engine = create_engine(url, connect_args=connect_args, future=True)

    if _is_sqlite_url(url):

        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record) -> None:  # type: ignore[no-untyped-def]
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


engine = create_db_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db_session() -> Generator[Session, None, None]:
    """FastAPI dependency for database sessions."""

    with SessionLocal() as session:
        yield session
