from __future__ import annotations

import json
import re
from pathlib import Path

from app.db.base import Base, import_models


REPO_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_DIR / "backend"
DOCKERFILE = BACKEND_DIR / "Dockerfile"
DOCKERIGNORE = BACKEND_DIR / ".dockerignore"
ENTRYPOINT = BACKEND_DIR / "deploy" / "entrypoint.sh"
COMPOSE = BACKEND_DIR / "deploy" / "docker-compose.phase2b.yml"
ENV_EXAMPLE = BACKEND_DIR / "deploy" / "env.phase2b.example"
OPENAPI = BACKEND_DIR / "openapi" / "custom_gpt_action.openapi.yaml"

APPROVED_BUSINESS_TABLES = {
    "assets",
    "video_jobs",
    "job_attempts",
    "generation_request_snapshots",
    "job_asset_references",
    "provider_results",
    "idempotency_records",
}

PUBLIC_PATHS = {
    "/health",
    "/v1/assets/upload-url",
    "/v1/video-jobs",
    "/v1/video-jobs/{job_id}",
    "/v1/video-jobs/{job_id}/cancel",
    "/v1/video-jobs/{job_id}/retry",
}


def test_dockerfile_uses_non_root_user_and_backend_dependencies() -> None:
    text = DOCKERFILE.read_text(encoding="utf-8")

    assert "FROM python:3.12-slim" in text
    assert "COPY pyproject.toml" in text
    assert "tomllib" in text
    assert "adduser --system" in text
    assert re.search(r"^USER app$", text, flags=re.MULTILINE)
    assert "USER root" not in text


def test_entrypoint_runs_alembic_single_worker_without_reload() -> None:
    text = ENTRYPOINT.read_text(encoding="utf-8")

    assert "from alembic import command" in text
    assert 'config.set_main_option("sqlalchemy.url", os.environ["BACKEND_DATABASE_URL"])' in text
    assert 'command.upgrade(config, "head")' in text
    assert "--workers 1" in text
    assert "--reload" not in text
    assert "0.0.0.0" in text
    assert "BACKEND_API_KEY" in text
    assert "BACKEND_RESULT_TOKEN_SECRET" in text
    assert "must differ" in text


def test_compose_has_single_service_local_bind_and_healthcheck() -> None:
    text = COMPOSE.read_text(encoding="utf-8")
    services_block = text.split("\nvolumes:", 1)[0]

    assert re.search(r"^  video-backend:$", text, flags=re.MULTILINE)
    assert (
        len(re.findall(r"^  [a-zA-Z0-9_-]+:$", services_block, flags=re.MULTILINE))
        == 1
    )
    assert "restart: unless-stopped" in text
    assert "127.0.0.1:8000:8000" in text
    assert "0.0.0.0:8000:8000" not in text
    assert "6379" not in text
    assert "5432" not in text
    assert "3306" not in text
    assert "GET /health" not in text
    assert "urllib.request.urlopen('http://127.0.0.1:8000/health'" in text


def test_compose_uses_persistent_sqlite_and_mock_storage_volumes() -> None:
    text = COMPOSE.read_text(encoding="utf-8")

    assert "BACKEND_DATABASE_URL: sqlite:////data/database/backend.db" in text
    assert "BACKEND_MOCK_STORAGE_DIRECTORY: /data/mock_storage" in text
    assert "phase2b_database:/data/database" in text
    assert "phase2b_mock_storage:/data/mock_storage" in text
    assert "phase2b_database:" in text
    assert "phase2b_mock_storage:" in text
    assert "redis" not in text.lower()
    assert "celery" not in text.lower()


def test_dockerignore_excludes_secrets_databases_and_runtime_artifacts() -> None:
    ignored = {
        line.strip()
        for line in DOCKERIGNORE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }

    for pattern in {
        ".env",
        ".env.*",
        "*.db",
        "*.sqlite",
        "*.sqlite3",
        "data/",
        "runtime/",
        "mock_storage/",
        "uploads/",
        "results/",
        "*.log",
        "*.tmp",
        "*.temp",
    }:
        assert pattern in ignored

    assert "*.mp4" not in ignored
    assert "openapi/" not in ignored
    assert "alembic/" not in ignored
    assert "tests/" not in ignored


def test_env_example_matches_settings_fields_and_secret_boundary() -> None:
    values = {}
    for line in ENV_EXAMPLE.read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            key, value = line.split("=", 1)
            values[key] = value

    assert values["BACKEND_DATABASE_URL"] == "sqlite:////data/database/backend.db"
    assert values["BACKEND_MOCK_STORAGE_DIRECTORY"] == "/data/mock_storage"
    assert values["BACKEND_PUBLIC_BASE_URL"] == "http://127.0.0.1:8000"
    assert values["BACKEND_API_KEY"] != values["BACKEND_RESULT_TOKEN_SECRET"]
    assert len(values["BACKEND_RESULT_TOKEN_SECRET"]) >= 32


def test_database_metadata_still_has_only_phase_2a_business_tables() -> None:
    import_models()

    assert set(Base.metadata.tables) == APPROVED_BUSINESS_TABLES


def test_openapi_still_has_only_public_action_paths() -> None:
    schema = json.loads(OPENAPI.read_text(encoding="utf-8"))

    assert set(schema["paths"]) == PUBLIC_PATHS
    assert "/_internal/mock-uploads/{token}" not in schema["paths"]
    assert "/_internal/mock-results/{token}" not in schema["paths"]
