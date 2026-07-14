# Beauty Care Tools Skeleton

```yaml
category_pack_status:
  category: beauty_care_tools
  support_level: SKELETON_ONLY
  routing_status: PARTIAL
  production_ready: false
  human_demo_required_by_default: true
  ai_generated_core_before_after_prohibited: true
  human_safety_review_required: true
```

---

# SOURCE FILE: categories/beauty_care_tools/README.md

---

# Beauty Care Tools Category Skeleton

```yaml
beauty_care_tools_status:
  status: SKELETON_ONLY
  support_level: SKELETON_ONLY
  routing_status: PARTIAL
  human_demo_required_by_default: true
  production_use: NOT_READY_WITHOUT_PRODUCT_PACK
  production_ready: false
  ai_generated_core_before_after_prohibited: true
  human_safety_review_required: true
```

---

## Purpose

This folder defines the minimal safe skeleton for beauty-care tool expansion without pretending the category is fully supported.

Without a completed Product Pack, it may provide conservative human-demo structure and missing information, but it cannot provide final efficacy, medical, beauty, or skin-safety conclusions.
---

# SOURCE FILE: categories/beauty_care_tools/category_pack_skeleton.md

---

# Beauty Care Tools Category Pack Skeleton

## Status

```yaml
beauty_care_tools_status:
  status: SKELETON_ONLY
  human_demo_required_by_default: true
  production_use: NOT_READY_WITHOUT_PRODUCT_PACK
```

---

## Core Rules

- human demonstration is usually the primary proof
- AI may support atmosphere, transitions, and non-proof hooks
- AI may not replace core human-result proof

---

## Unsupported Areas In Current Phase

- detailed hair-texture protocols
- device-specific skin-contact safety logic
- regulated efficacy claims
- final product-specific scripts without a product pack
---

# SOURCE FILE: categories/beauty_care_tools/human_demo_and_safety_skeleton.md

---

# Beauty Care Tools Human Demo And Safety Skeleton

## Human Demo Rules

For most beauty-care tools:

- `human_demo_required=true`
- body area must be declared
- heat or skin contact risk must be declared
- real product must be shown
- real operation must be shown
- same person, same body area, same angle, same lighting, and same baseline preparation are required for core efficacy proof

---

## High-Risk Areas

- eye area
- direct skin contact
- hot tools
- electrical grooming tools
- hygiene-sensitive reusable heads
- scalp contact
- wet-use restrictions
- temperature settings

---

## Current Guardrail

Without a completed product pack, do not give final safety advice or professional efficacy conclusions.
---

# SOURCE FILE: categories/beauty_care_tools/before_after_authenticity_skeleton.md

---

# Beauty Care Tools Before And After Authenticity Skeleton

## Authenticity Rules

Before/after should keep:

- same person
- same body area
- same lighting
- same angle
- same styling baseline

Do not fake results with:

- beauty filters
- exposure changes
- hidden re-touching
- framing cheats

---

## AI Restriction

AI may not generate core human efficacy proof for:

- hair straightening result
- curl retention result
- skin cleansing result
- grooming outcome
- body-area transformation
- before/after
- redness reduction
- pore change
- hair-volume result
---

# SOURCE FILE: categories/beauty_care_tools/product_matrix_skeleton.md

---

# Beauty Care Tools Product Matrix Skeleton

| Product Type | Status | Human Demo | Core Truth Mode | Notes |
| --- | --- | --- | --- | --- |
| hair_styling_tool | SKELETON_ONLY | true | REAL_SHOOT | Heat and hair-state controls required. |
| straightening_brush | SKELETON_ONLY | true | REAL_SHOOT | Before/after authenticity required. |
| curling_brush | SKELETON_ONLY | true | REAL_SHOOT | Curl hold claims need controlled proof. |
| hot_air_brush | SKELETON_ONLY | true | REAL_SHOOT | Heat + styling claims remain sensitive. |
| facial_cleansing_tool | SKELETON_ONLY | true | REAL_SHOOT | Skin-contact safety required. |
| grooming_tool | SKELETON_ONLY | true | REAL_SHOOT | Hygiene and skin-contact claims required. |

---

## Support Rule

No beauty-care product type in this matrix is production-ready in Phase 1B.
---

# SOURCE FILE: categories/beauty_care_tools/products/README.md

---

# Beauty Care Tools Product Packs

No complete product pack is present in Phase 1B.

Routing rule:

- route into beauty-care skeletons
- mark support as `PARTIAL` or `UNSUPPORTED`
- do not generate product-specific expert conclusions
