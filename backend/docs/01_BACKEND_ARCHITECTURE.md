# Backend Architecture

## Authority

`backend/docs/BACKEND_MASTER_DESIGN.md` is authoritative. This document is a
short architecture map only. Any conflict is resolved in favor of the Master
Design.

## Architecture Shape

```text
Custom GPT Action
  -> FastAPI API layer
  -> Auth and owner mapping
  -> Schema validation
  -> Idempotency service
  -> Structural Truth Gate
  -> HYBRID Gate
  -> Job and Asset repositories
  -> FastAPI BackgroundTasks Mock Provider Runner
  -> Mock result asset
```

## Runtime Rules

- Backend receives versioned JSON only.
- Backend must not parse Markdown Knowledge or Skills at runtime.
- Phase 2A uses SQLite + SQLAlchemy 2.x + Alembic.
- Phase 2A uses single-tenant Bearer API key auth.
- Phase 2A uses FastAPI BackgroundTasks for mock execution.
- Phase 2A does not introduce Celery, Redis, durable queues, or real provider
  adapters.

## State Ownership

- Public Job state is owned by `video_jobs`.
- Provider execution state is owned by `job_attempts`.
- Result metadata is owned by `provider_results` and `assets`.
- Idempotency state is owned by `idempotency_records`.
- Facts, source refs, proof needs, and gate decisions are stored inside
  `generation_request_snapshots` JSON for Phase 2A.
