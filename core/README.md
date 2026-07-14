# Core Layer

## Purpose

The `core/` layer defines reusable logic that can be shared across product categories without forcing automotive-specific assumptions onto every workflow.

Core should contain:

- cross-category routing logic
- generic commercial video decision rules
- generic production and AI routing rules
- compatibility maps that explain how legacy `knowledge/01-10` can be reused

Core should not contain:

- category-specific dirt scenarios
- body-area safety rules
- category-specific proof protocols
- product-specific claims

---

## Current Phase 1B Status

Current repo strategy:

- keep `knowledge/01-10` in place for backward compatibility
- map reusable parts into the new architecture
- move category-specific expansion into `categories/`
- move product-specific expansion into `categories/<category>/products/`

This phase does not mass-migrate legacy knowledge files.

---

## Current Core Files

- `core/core_knowledge_map.md`

---

## Support Rule

If a category or product pack is incomplete:

- do not pretend the repo fully supports it
- route through `workflows/Category_Router.md`
- return `PARTIAL` or `UNSUPPORTED` when required
