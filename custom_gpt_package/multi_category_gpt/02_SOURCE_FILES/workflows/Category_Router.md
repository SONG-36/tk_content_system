# Category Router

## Purpose

This router selects the correct category pack and product pack before downstream script, production, or Seedance workflows begin.

It exists to prevent cross-category misuse of automotive rules.

## Task Router

```yaml
task_types:
  A: "viral_video_analysis_and_product_transfer"
  B: "product_to_video_generation"
  C: "existing_script_audit"
  D: "hook_or_visual_analysis"
  E: "approved_shot_to_seedance_package"
```

Task routing happens first, then Category Router resolves category and product support.

---

## Input Schema

```yaml
category_router_input:
  product_name: ""
  primary_category: ""
  secondary_category: ""
  product_type: ""
  use_environment: []
  target_surface_or_body_area: []
  target_user: []
  primary_job_to_be_done: ""
  transformation_type: ""
  human_demo_required: false
  safety_level: "low | medium | high"
  truth_dependency: "low | medium | high"
  product_claims: []
  available_product_pack: ""
```

---

## Supported Primary Categories

```yaml
supported_primary_categories:
  - automotive_cleaning
  - home_cleaning
  - beauty_care_tools
```

---

## Initial Product Types

```yaml
initial_product_types:
  automotive_cleaning:
    - car_vacuum
    - blower_vacuum
    - snow_foam_cannon
    - pressure_washer_accessory
    - detailing_brush
    - crevice_cleaning_tool
    - interior_cleaning_tool
    - car_cleaning_spray

  home_cleaning:
    - handheld_vacuum
    - electric_scrubber
    - window_cleaning_tool
    - upholstery_cleaning_tool
    - steam_cleaner
    - high_temperature_cleaner

  beauty_care_tools:
    - hair_styling_tool
    - straightening_brush
    - curling_brush
    - hot_air_brush
    - facial_cleansing_tool
    - grooming_tool
```

---

## Output Schema

```yaml
category_router_output:
  resolved_primary_category: ""
  resolved_secondary_category: ""
  selected_category_pack: ""
  selected_product_pack: ""
  core_knowledge_required: []
  category_knowledge_required: []
  product_knowledge_required: []
  human_demo_required: false
  required_truth_level: ""
  required_safety_review: []
  unsupported_knowledge_gaps: []
  routing_status: "ROUTED | GENERIC_SUPPORTED | PARTIAL | UNSUPPORTED"
  fallback_strategy: ""
```

---

## Routing Rules

### Automotive Cleaning

`car_vacuum`
-> `12_Automotive_Category_Pack.md`
-> `13_Car_Vacuum_Product_Pack.md`
-> shared core Knowledge files

Automotive-specific knowledge:

```yaml
automotive_specific_knowledge:
  - 02_Car_Cleaning_Content_Psychology.md
  - 03_Cleaning_Video_Hook_Database.md
  - 04_Satisfying_Cleaning_Visual_Library.md
```

If product type is automotive but no complete product pack exists:

- stay in automotive category pack
- do not route into `car_vacuum`
- mark result `GENERIC_SUPPORTED` or `PARTIAL`

### Home Cleaning

Home-cleaning products must use:

- `categories/home_cleaning/category_pack_skeleton.md`
- product pack if available

If the product pack is incomplete:

- return `PARTIAL`
- do not reuse automotive scenarios as if they were home-cleaning knowledge

### Steam Cleaner / High-Temperature Cleaner

`steam_cleaner` or `high_temperature_cleaner`
-> `home_cleaning`
-> `steam_cleaner` skeleton
-> force `safety_level=high`
-> force claim-boundary review

### Beauty Care Tools

Beauty-care products
-> `beauty_care_tools`
-> relevant skeleton
-> usually `human_demo_required=true`
-> force before/after authenticity and human safety review

---

## Prohibited Behavior

- Do not apply seat-gap automotive templates to kitchens, bathrooms, or body-care scenarios.
- Do not use cleaning “dirt disappearance” proof logic as beauty efficacy proof.
- Do not pretend an absent product pack already exists.
- If routing information is incomplete, return `PARTIAL` or `UNSUPPORTED`.

## Knowledge 10 Timing

AI generation routing marks Knowledge 10 as required and sets `ai_quality_review_status=NOT_RUN`.

Knowledge 10 executes only after actual generated AI media exists.

---

## Reference Resolution Rules

### Car Vacuum

If `product_type=car_vacuum`:

- `resolved_primary_category=automotive_cleaning`
- `selected_category_pack=categories/automotive_cleaning/category_pack.md`
- `selected_product_pack=categories/automotive_cleaning/products/car_vacuum/README.md`
- `routing_status=ROUTED`

### Steam Cleaner

If `product_type=steam_cleaner` or `high_temperature_cleaner`:

- `resolved_primary_category=home_cleaning`
- `selected_product_pack=categories/home_cleaning/products/steam_cleaner/README.md`
- `required_safety_review=["high_temperature_risk", "claim_boundary_review"]`
- `routing_status=PARTIAL`

### Beauty Care Tool

If `resolved_primary_category=beauty_care_tools`:

- `human_demo_required=true`
- add unsupported gaps unless a complete product pack exists

---

## Required Core Knowledge

Default core knowledge set:

- `knowledge/01_TikTok_Viral_Analysis_Framework.md`
- `knowledge/05_TikTok_Shop_Script_Writing_Rules.md`
- `knowledge/06_Video_Script_Scoring_System.md`
- `knowledge/08_Shot_Production_Planning_Framework.md`
- `knowledge/09_Seedance_Generation_Director.md`
- `knowledge/10_AI_Generation_Quality_Review.md`

Add category and product knowledge on top of this base.
