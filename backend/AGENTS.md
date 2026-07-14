# Backend Agent Rules

These rules apply to `backend/`.

## Purpose

`backend/` is reserved for an independently deployable FastAPI backend that will
serve the Custom GPT through versioned JSON APIs.

`backend/docs/BACKEND_MASTER_DESIGN.md` is the authoritative backend design.
All backend implementation and contract work must follow it. If any other
backend document conflicts with it, the Master Design wins.

Phase 2A implementation is allowed only within the scope approved by
`BACKEND_MASTER_DESIGN.md`.

## Runtime Boundary

Backend runtime code must not:

- Parse `knowledge/*.md`.
- Parse `custom_gpt_package/**`.
- Parse `seedance_skills/**`.
- Import or execute Custom GPT prompt logic.
- Treat Markdown as runtime configuration.

Rules from Knowledge must be translated into deterministic schemas, enums,
validators, service code, and tests before backend runtime can use them.

## Provider Boundary

Phase 2A supports only `selected_model=Seedance` and
`execution_provider=mock` in the public Custom GPT Action contract.

Phase 2A requires local SQLite + SQLAlchemy 2.x + Alembic. Do not prohibit or
remove the local SQLite database required by the Master Design.

Do not connect real Seedance, ByteDance, BytePlus, production/external object
storage, queue, Redis, external database services, or billing services in
Phase 2A.

Local mock upload/result storage is allowed for Phase 2A tests and local
development.

Keep `selected_model` separate from `execution_provider`:

- `selected_model` is the model intent chosen by the Custom GPT plan.
- `execution_provider` is the backend adapter used to execute a job.

## Status Boundary

Keep generation and review states separate:

- `generation_status` describes backend job execution.
- `ai_review_status` describes post-generation AI quality review.

Do not collapse them into one status field.

## Idempotency

All endpoints that can create jobs, upload assets, trigger generation, retry
generation, or create cost must require `Idempotency-Key`.

## Tests

Backend behavior must be deterministic and testable with mock providers before
any external adapter is introduced. State-machine tests should verify runner and
repository transitions directly; API polling is not required to observe every
short-lived intermediate state.
