# Automotive Category Pack

```yaml
category_pack_status:
  category: automotive_cleaning
  support_level: MATURE
  production_ready: true
  dedicated_product_packs:
    - car_vacuum
  generic_supported_products:
    - snow_foam_cannon
    - detailing_brush

automotive_product_support:
  car_vacuum: COMPLETE
  snow_foam_cannon: GENERIC_SUPPORTED
  detailing_brush: GENERIC_SUPPORTED
  blower_vacuum: PARTIAL
  pressure_washer_accessory: PARTIAL
  crevice_cleaning_tool: PARTIAL
  interior_cleaning_tool: PARTIAL
  car_cleaning_spray: PARTIAL

support_level_definitions:
  COMPLETE: "Dedicated Product Pack exists and is production-ready."
  GENERIC_SUPPORTED: "Category knowledge can support a conservative generic plan, but no complete Product Pack exists."
  PARTIAL: "Routing is possible, but product-specific knowledge gaps must be disclosed."
```

---

# SOURCE FILE: categories/automotive_cleaning/README.md

---

# Automotive Cleaning Category Pack

## Status

```yaml
automotive_cleaning_category_status:
  status: ACTIVE
  maturity: HIGHEST_CURRENT_CATEGORY
  production_use: READY_WITH_PRODUCT_SPECIFIC_TRUTH_RULES
```

---

## Purpose

This category pack covers automotive cleaning products and scenarios.

It provides:

- automotive user psychology
- automotive cleaning hooks
- automotive cleaning proof logic
- automotive claim boundaries
- category-level routing into product packs

---

## Current Product Support

```yaml
automotive_product_support:
  car_vacuum: COMPLETE
  snow_foam_cannon: GENERIC_SUPPORTED
  detailing_brush: GENERIC_SUPPORTED
  blower_vacuum: PARTIAL
  pressure_washer_accessory: PARTIAL
  crevice_cleaning_tool: PARTIAL
  interior_cleaning_tool: PARTIAL
  car_cleaning_spray: PARTIAL

support_level_definitions:
  COMPLETE: "Dedicated Product Pack exists and is production-ready."
  GENERIC_SUPPORTED: "Category knowledge can support a conservative generic plan, but no complete Product Pack exists."
  PARTIAL: "Routing is possible, but product-specific knowledge gaps must be disclosed."
```

---

## Files

- `categories/automotive_cleaning/category_pack.md`
- `categories/automotive_cleaning/product_matrix.md`
- `categories/automotive_cleaning/material_and_claim_boundaries.md`
- `categories/automotive_cleaning/products/car_vacuum/`
---

# SOURCE FILE: categories/automotive_cleaning/category_pack.md

---

# Automotive Cleaning Category Pack

## Purpose

This file maps the existing automotive cleaning knowledge into the new category architecture without duplicating the entire legacy content set.

---

## Source Mapping

Use these Builder Knowledge files as the main automotive category references:

- Psychology:
  `02_Car_Cleaning_Content_Psychology.md`
- Hook logic:
  `03_Cleaning_Video_Hook_Database.md`
- Visual proof:
  `04_Satisfying_Cleaning_Visual_Library.md`
- Shooting standard:
  `07_Professional_Shooting_Standard.md`
- Production planning:
  `08_Shot_Production_Planning_Framework.md`
- Seedance routing and package generation:
  `09_Seedance_Generation_Director.md`
- AI output review:
  `10_AI_Generation_Quality_Review.md`

Commercial script generation and scoring remain:

- `05_TikTok_Shop_Script_Writing_Rules.md`
- `06_Video_Script_Scoring_System.md`

Repository paths are provenance only when shown in generated SOURCE FILE sections.

## Current Support Matrix

```yaml
automotive_product_support:
  car_vacuum: COMPLETE
  snow_foam_cannon: GENERIC_SUPPORTED
  detailing_brush: GENERIC_SUPPORTED
  blower_vacuum: PARTIAL
  pressure_washer_accessory: PARTIAL
  crevice_cleaning_tool: PARTIAL
  interior_cleaning_tool: PARTIAL
  car_cleaning_spray: PARTIAL
```

---

## Category-Level Truth Rules

Automotive cleaning usually carries `truth_dependency=high` when the shot shows:

- dirt removal
- foam interaction
- rinse result
- suction result
- pet hair removal
- interior restoration proof
- before/after
- tool-to-surface contact

These shots must remain:

- `REAL_SHOOT`
- or `HYBRID` with a clearly real proof layer

---

## Category-Level Reusable Hooks

Strong automotive cleaning hooks include:

- hidden dirt reveal
- difficult area challenge
- product test
- before/after
- satisfying transformation

---

## Category-Level AI Rules

AI may be used for:

- non-proof automotive hook visuals
- luxury environment enhancement
- non-functional atmosphere
- transitions

AI must not replace:

- proof of real cleaning
- product structure
- packaging
- logo accuracy
- performance validation
---

# SOURCE FILE: categories/automotive_cleaning/product_matrix.md

---

# Automotive Cleaning Product Matrix

| Product Type | Product Pack Status | Strong Hooks | Strong Proof | Truth Dependency |
| --- | --- | --- | --- | --- |
| car_vacuum | COMPLETE | Hidden Dirt / Product Test | Dirt Collection / Transparent Bin | High |
| snow_foam_cannon | GENERIC_SUPPORTED | Transformation | Foam Coverage / Real Rinse | High |
| detailing_brush | GENERIC_SUPPORTED | Hidden Dirt | Dirt Extraction | High |
| Blower Vacuum | PARTIAL | Difficult Area / Product Test | Dust Movement / Collection | High |
| Pressure Washer Accessory | PARTIAL | Visual Impact | Real Water Contact / Real Rinse | High |
| Crevice Cleaning Tool | PARTIAL | Hidden Dirt | Real Reach / Real Contact | High |
| Interior Cleaning Tool | PARTIAL | Problem Reveal | Real Touch / Real Removal | High |
| car_cleaning_spray | PARTIAL | Before/After | Surface Transformation | High |

---

## Interpretation Rules

- `COMPLETE` means a dedicated product pack exists.
- `GENERIC_SUPPORTED` means the category pack plus core rules can support basic work.
- `PARTIAL` means routing may continue, but unsupported gaps must be declared.

If a product pack is not complete:

- do not route to a different product pack
- do not fabricate product-specific claim logic
---

# SOURCE FILE: categories/automotive_cleaning/material_and_claim_boundaries.md

---

# Automotive Cleaning Material And Claim Boundaries

## Purpose

This file defines category-level material sensitivity and claim boundary rules for automotive cleaning workflows.

---

## Sensitive Automotive Surfaces

Always check whether the shot or script touches:

- piano black trim
- infotainment screen
- coated plastic
- leather
- stitched upholstery
- alcantara-like fabric
- painted trim
- vents and electronics

Do not claim universal surface safety without product evidence.

---

## Category Claim Boundaries

### Allowed With Direct Proof

- visible dirt removed from a shown area
- tool reaches a narrow space
- foam covers a shown surface
- collected debris becomes visible

### Requires Controlled Evidence

- suction comparison
- noise level
- runtime
- surface safety
- no-scratch behavior
- multi-surface compatibility

### Not Allowed Without Evidence

- safest for all interiors
- strongest in category
- zero risk to every trim type
- perfect cleaning every time
- professional detailing replacement

---

## Category Safety Rule

When the workflow cannot confirm:

- material compatibility
- coating sensitivity
- electronics safety

the output must downgrade wording and avoid universal claims.
---

# SOURCE FILE: categories/automotive_cleaning/products/README.md

---

# Automotive Cleaning Product Packs

Current product-pack directories:

- `car_vacuum/`

If a requested automotive product does not have a complete pack:

- route through the automotive category pack
- mark support as `PARTIAL` or `GENERIC_SUPPORTED`
- declare unsupported product-specific gaps
