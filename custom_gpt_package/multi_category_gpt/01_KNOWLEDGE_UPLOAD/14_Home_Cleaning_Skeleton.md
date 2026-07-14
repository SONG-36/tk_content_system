# Home Cleaning Skeleton

```yaml
category_pack_status:
  category: home_cleaning
  support_level: SKELETON_ONLY
  routing_status: PARTIAL
  production_ready: false
  must_disclose_knowledge_gaps: true
  product_pack_required_for_full_support: true
```

---

# SOURCE FILE: categories/home_cleaning/README.md

---

# Home Cleaning Category Skeleton

```yaml
home_cleaning_category_status:
  status: SKELETON_ONLY
  support_level: SKELETON_ONLY
  routing_status: PARTIAL
  production_use: NOT_READY_WITHOUT_PRODUCT_PACK
  production_ready: false
  must_disclose_knowledge_gaps: true
  product_pack_required_for_full_support: true
```

---

## Purpose

This folder establishes the expansion skeleton for home-cleaning workflows.

Current phase supports:

- category routing
- gap declaration
- high-level guardrails

Current phase does not support:

- full production-grade home-cleaning knowledge
- detailed room-specific proof protocols
- unrestricted product claim generation

## Current Allowed Outputs

- category identification
- basic JTBD
- high-level Hook direction
- resource requirements
- risk list
- missing information
- provisional script outline

## Current Prohibited Outputs

Without a complete Product Pack, do not output definitive claims about:

- all-surface compatibility
- chemical safety
- waterproof behavior
- cleaning efficiency
- material safety
- absolute child or pet safety
- complete production-grade Proof Protocol
---

# SOURCE FILE: categories/home_cleaning/category_pack_skeleton.md

---

# Home Cleaning Category Pack Skeleton

## Status

```yaml
home_cleaning_category_status:
  status: SKELETON_ONLY
  production_use: NOT_READY_WITHOUT_PRODUCT_PACK
```

---

## Future Coverage Requirements

Future home-cleaning category work must cover:

- room context
- surface compatibility
- moisture and residue expectations
- tool-to-surface safety
- pet and child exposure context
- before/after proof logic by surface type

---

## Reusable Rules

Potentially reusable from core:

- viral analysis
- script generation
- commercial scoring
- truth-first production planning
- AI routing and AI review

---

## Non-Reusable Automotive Assumptions

Do not directly reuse these automotive assumptions:

- seat-gap specific hooks
- cup-holder and console dirt logic
- car-interior prestige environments
- “new car feel” psychology
- automotive trim safety assumptions

---

## Fallback Rule

If no product pack exists:

- return `PARTIAL`
- declare unsupported gaps
- do not fake surface compatibility knowledge
---

# SOURCE FILE: categories/home_cleaning/room_and_surface_matrix_skeleton.md

---

# Home Cleaning Room And Surface Matrix Skeleton

## Required Room Coverage

- kitchen
- bathroom
- living_room
- bedroom
- pet_area
- window_and_track
- upholstery
- carpet

---

## Required Surface Coverage

- glass
- tile
- grout
- stainless_steel
- fabric
- carpet
- sealed_wood
- plastic
- painted_surface
- stone

---

## Future Matrix Requirements

Future product packs must define:

- which rooms are valid
- which surfaces are valid
- which surfaces are risky
- whether moisture, heat, abrasion, or chemicals change the claim boundary

Current repo does not yet treat this matrix as production-ready knowledge.
---

# SOURCE FILE: categories/home_cleaning/claim_and_material_risk_skeleton.md

---

# Home Cleaning Claim And Material Risk Skeleton

## Purpose

This file marks the key unknowns that must be resolved before home-cleaning product packs are production-ready.

---

## Core Risk Areas

- porous vs sealed materials
- moisture tolerance
- heat tolerance
- abrasion risk
- residue risk
- electronic exposure risk
- odor and sanitation claims

---

## Claim Guardrails

Do not generate unsupported claims for:

- disinfecting
- sterilizing
- mold removal
- pet-safe universal use
- child-safe universal use
- compatibility with every floor or surface

---

## Production Rule

Until a complete product pack exists:

- no category-level professional conclusion should be presented as complete
- route status should remain `PARTIAL` or `UNSUPPORTED`
---

# SOURCE FILE: categories/home_cleaning/products/README.md

---

# Home Cleaning Product Packs

Current folders:

- `steam_cleaner/`

Support rule:

- `steam_cleaner` is currently `SKELETON_ONLY`
- any other home-cleaning product without a pack must return `PARTIAL`
