# Repository Agent Rules

These rules apply to the whole repository unless a deeper `AGENTS.md` overrides
them.

## Project Boundary

This repository remains a monorepo for:

- Custom GPT Builder materials.
- Knowledge and workflow source files.
- Third-party Seedance skill references.
- Future independently deployable backend services.

Do not rename, move, or delete existing top-level directories without explicit
approval.

## Frozen Runtime Materials

Do not edit these files unless the task explicitly requests a new Custom GPT
release phase:

- `custom_gpt_package/multi_category_gpt/00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md`
- `custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/*.md`
- `knowledge/01_TikTok_Viral_Analysis_Framework.md` through
  `knowledge/10_AI_Generation_Quality_Review.md` when acting on backend-only tasks
- `knowledge/18_Deliverable_and_Output_Contract.md`
- `seedance_skills/**`

Generated package files must stay consistent with `tools/build_custom_gpt_package.py`.

## Backend Boundary

The future `backend/` directory is an independent deployable FastAPI subproject.

Backend runtime code must not parse or depend on Markdown Knowledge, Skills, or
Custom GPT instruction files. The Custom GPT talks to backend services only
through versioned JSON API contracts.

## External Services

Do not connect to real Seedance, ByteDance, BytePlus, payment, database, Redis,
object storage, or queue services unless the task explicitly enters that
implementation phase.

Any operation that may create cost, mutation, upload, or generation must support
`Idempotency-Key`.

## Git

Do not run `git add`, `git commit`, or `git push` unless the user explicitly asks
for Git publishing work in that turn.
