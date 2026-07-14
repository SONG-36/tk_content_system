# Phase 2A Implementation Plan

## Authority

`backend/docs/BACKEND_MASTER_DESIGN.md` is authoritative. This plan must be
updated if the Master Design changes.

## Implementation Order

1. Create FastAPI project skeleton under `backend/`.
2. Add settings, auth, request id, and error model.
3. Add SQLite + SQLAlchemy 2.x + Alembic.
4. Add models for the approved minimal tables.
5. Add schemas for the six public endpoints and nested objects.
6. Add idempotency service with 24-hour completed TTL and 60-second pending
   lease.
7. Add asset upload URL flow and internal mock upload route.
8. Add create job schema validation, reference integrity, mode
   cross-validation, Truth Gate, and HYBRID Gate.
9. Add Job/Attempt repositories and legal state transitions.
10. Add FastAPI BackgroundTasks mock runner with Fake Clock and dependency
   injected outcomes.
11. Add cancel and retry behavior.
12. Add get job and internal mock result route.
13. Generate the Custom GPT Action OpenAPI document from the approved public
   contract.
14. Add tests for schemas, gates, idempotency, state machines, runner,
   repository behavior, and API endpoints.
15. Add Action OpenAPI tests for `operationId`, Bearer auth, idempotency
   headers, success responses, and unified Error Schema.
16. Add startup recovery test for non-terminal mock attempts marked failed with
   `MOCK_RUNNER_INTERRUPTED`.

## Implementation Constraints

- Do not create real Seedance integration.
- Do not introduce Celery, Redis, or external queues.
- Do not create production object storage.
- Do not add public endpoints beyond the Master Design.
- Custom GPT Action OpenAPI must contain only the six public endpoints.
- `PUT /_internal/mock-uploads/{token}` and
  `GET /_internal/mock-results/{token}` must not enter Action OpenAPI.
- Do not modify frozen Custom GPT files.

## Acceptance

Phase 2A passes when the six public endpoints, two internal mock routes,
structural gates, idempotency, mock runner, persistence, and tests satisfy
`backend/docs/BACKEND_MASTER_DESIGN.md`.

The generated Custom GPT Action OpenAPI passes only when it exposes the six
public endpoints, includes stable `operationId` values, includes Bearer auth,
includes `Idempotency-Key` headers on side-effect endpoints, defines success
responses, uses the unified `error_response` schema, and excludes all
`/_internal` routes.
