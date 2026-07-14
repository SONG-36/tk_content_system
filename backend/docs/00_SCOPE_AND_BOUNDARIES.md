# Scope And Boundaries

## Authority

`backend/docs/BACKEND_MASTER_DESIGN.md` is the authoritative backend design for
Phase 2A. If this document conflicts with the Master Design, the Master Design
wins.

## Backend Scope

Phase 2A may implement an independently deployable FastAPI backend under
`backend/` with the six public Action endpoints and two internal mock routes
defined in `BACKEND_MASTER_DESIGN.md`.

## Explicit Boundaries

- Do not modify frozen Custom GPT files or Knowledge 01-18.
- Do not parse Markdown Knowledge, Skills, or Custom GPT instructions at
  backend runtime.
- Do not connect real Seedance or external services in Phase 2A.
- Do not add public endpoints beyond the six public Action endpoints approved
  by `BACKEND_MASTER_DESIGN.md`.
- Internal mock routes must stay out of the public Custom GPT Action schema.

## Phase 2A Baseline

- `contract_version`: `v1`
- `truth_rule_version`: `truth-rules-v0.4`
- `provider_mapping_version`: `mock-provider-map-v0.4`
- `selected_model`: `Seedance`
- `execution_provider`: `mock`
