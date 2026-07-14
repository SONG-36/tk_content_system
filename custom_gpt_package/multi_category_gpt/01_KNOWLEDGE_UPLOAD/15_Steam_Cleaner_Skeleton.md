# Steam Cleaner Skeleton

```yaml
product_pack_status:
  category: home_cleaning
  product_type: steam_cleaner
  support_level: SKELETON_ONLY
  routing_status: PARTIAL
  production_ready: false
  safety_level: high
  unsupported_claims_must_be_blocked: true
  sterilization_claim_requires_evidence: true
```

---

# SOURCE FILE: categories/home_cleaning/products/steam_cleaner/README.md

---

# Steam Cleaner Product Pack Skeleton

```yaml
steam_cleaner_pack_status:
  status: SKELETON_ONLY
  support_level: SKELETON_ONLY
  routing_status: PARTIAL
  production_ready: false
  safety_level: high
  production_use: NOT_READY
  unsupported_claims_must_be_blocked: true
  sterilization_claim_requires_evidence: true
```

This folder is intentionally non-production-ready in Phase 1B.

It may provide high-level creativity, safety restrictions, missing information, and provisional Shot Plans only. It must not claim to be a complete Steam Cleaner Product Pack.
---

# SOURCE FILE: categories/home_cleaning/products/steam_cleaner/product_pack_skeleton.md

---

# Steam Cleaner Product Pack Skeleton

## Status

```yaml
steam_cleaner_pack_status:
  status: SKELETON_ONLY
  safety_level: high
  production_use: NOT_READY
```

---

## Future Coverage Requirements

Any production-ready steam-cleaner pack must define:

- temperature and pressure truth boundary
- warm-up time
- tank handling
- pressure release behavior
- nozzle installation
- real steam visualization vs real cleaning proof

---

## Proof Rule

Product proof must remain `REAL_SHOOT`.

AI may not generate fake steam-cleaning proof.
---

# SOURCE FILE: categories/home_cleaning/products/steam_cleaner/safety_and_claim_boundary_skeleton.md

---

# Steam Cleaner Safety And Claim Boundary Skeleton

## Mandatory Safety Areas

- burn risk
- electrical safety
- pressure release handling
- hot tank opening
- refill timing
- glass thermal shock risk
- child and pet exposure
- electronics
- adhesives
- sealed and unsealed surfaces

---

## High-Risk Claim Areas

Do not state without evidence:

- sterilization
- 100% sterilization
- disinfection
- complete disinfection
- mite removal
- kills all bacteria
- universal safe use
- safe use on every sealed and unsealed surface
- safe use on all fabrics
- safe use on all glass
- zero chemical risk

## Proof Rule

The following require `REAL_SHOOT`:

- actual steam output
- warm-up time
- pressure behavior
- nozzle installation
- water refill
- cleaning result
- material response

AI may generate non-proof steam atmosphere but not function, sterilization, or safety evidence.

---

## Routing Rule

Any steam cleaner request should force:

- `safety_level=high`
- claim boundary review
- `PARTIAL` or `UNSUPPORTED` unless the product pack is completed later
---

# SOURCE FILE: categories/home_cleaning/products/steam_cleaner/material_compatibility_skeleton.md

---

# Steam Cleaner Material Compatibility Skeleton

## Must-Cover Future Material Rules

- glass
- tile
- grout
- sealed stone
- sealed metal
- painted surfaces
- wood
- leather
- adhesives
- electronics

---

## Current Warning

This repo does not yet contain enough validated rules to guarantee:

- safe steam use on wood
- safe steam use on leather
- safe steam use near electronics
- safe steam use on glued or bonded structures

Do not imply such support in current production outputs.
