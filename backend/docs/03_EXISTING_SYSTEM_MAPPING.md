# Existing System Mapping

## Authority

`backend/docs/BACKEND_MASTER_DESIGN.md` is authoritative. This mapping is only a
bridge from the existing Custom GPT system to the backend contract.

## Runtime Files

- Main Instructions and Knowledge 01-18 remain Custom GPT runtime materials.
- Backend runtime must not parse or depend on those Markdown files.
- Backend receives structured JSON from the Custom GPT Action.

## Rule Translation

| Existing System Concept | Backend Representation |
| --- | --- |
| Product Truth | Structural Truth Gate validators. |
| HYBRID proof layer | `hybrid_layers`, `reference_assets`, proof need checks. |
| Seedance selected in Knowledge 09 | `selected_model=Seedance`. |
| Phase 2A mock execution | `execution_provider=mock`. |
| AI review timing | `ai_review_status=NOT_RUN` until future review flow. |
| Product/reference assets | `assets` and `job_asset_references`. |
| Source refs and proof needs | Snapshot JSON in `generation_request_snapshots`. |

## Non-authoritative Sources

`seedance_skills/**` and `source/open_source/**` remain reference material only
and must not be treated as backend API truth.
