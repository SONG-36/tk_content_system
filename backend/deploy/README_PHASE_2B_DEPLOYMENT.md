# Phase 2B Mock Backend Docker Deployment

This deployment package runs the approved Phase 2A mock backend as a single
local Docker service for Phase 2B smoke testing. It does not connect real
Seedance, ByteDance, BytePlus, Redis, Celery, external databases, or object
storage.

## Files

- `backend/Dockerfile`: Builds the FastAPI backend image from the backend
  subproject only.
- `backend/.dockerignore`: Excludes secrets, local databases, runtime storage,
  logs, caches, and temporary files from the Docker build context.
- `backend/deploy/docker-compose.phase2b.yml`: Runs one `video-backend` service.
- `backend/deploy/env.phase2b.example`: Local example environment values using
  the existing `BACKEND_*` settings fields.
- `backend/deploy/entrypoint.sh`: Validates required environment variables,
  runs Alembic, then starts Uvicorn.

## Runtime Contract

- Single instance.
- Single Uvicorn worker: `--workers 1`.
- No `--reload`.
- Non-root container user: `app`.
- Startup migration: Alembic `upgrade head` with `BACKEND_DATABASE_URL`
  injected into Alembic config, so migrations target `/data/database/backend.db`.
- SQLite database path: `/data/database/backend.db`.
- Mock upload/result storage path: `/data/mock_storage`.
- Local bind only: `127.0.0.1:8000:8000`.
- Public health check: `GET /health`.

The API key and result token secret must be different. The entrypoint fails
fast if they are identical.

## Local Smoke Test

From the repository root:

```bash
docker compose -f backend/deploy/docker-compose.phase2b.yml build
docker compose -f backend/deploy/docker-compose.phase2b.yml up -d
curl http://127.0.0.1:8000/health
docker compose -f backend/deploy/docker-compose.phase2b.yml exec video-backend id -u
docker compose -f backend/deploy/docker-compose.phase2b.yml exec video-backend python - <<'PY'
from sqlalchemy import create_engine, inspect

engine = create_engine("sqlite:////data/database/backend.db")
print(sorted(name for name in inspect(engine).get_table_names() if name != "alembic_version"))
PY
docker compose -f backend/deploy/docker-compose.phase2b.yml restart video-backend
docker compose -f backend/deploy/docker-compose.phase2b.yml exec video-backend test -f /data/database/backend.db
```

Stop the service:

```bash
docker compose -f backend/deploy/docker-compose.phase2b.yml down
```

Use `down -v` only when you explicitly want to remove local Phase 2B data
volumes.

## Deployment Boundary

This package intentionally does not create:

- Redis, Celery, or queue services.
- External database services.
- External object storage.
- Real Seedance provider calls.
- Docker-published database ports.
- A production Action OpenAPI variant.
