# Backend Agent Rules

These rules apply to `backend/`.

## Purpose

`backend/` is reserved for an independently deployable FastAPI backend that will
serve the Custom GPT through versioned JSON APIs.

Phase 2A is boundary and contract work only unless a later task explicitly asks
for implementation.

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

Phase 2A supports only `execution_provider=mock`.

Do not connect real Seedance, ByteDance, BytePlus, storage, queue, Redis,
database, or billing services in Phase 2A.

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
any external adapter is introduced.
