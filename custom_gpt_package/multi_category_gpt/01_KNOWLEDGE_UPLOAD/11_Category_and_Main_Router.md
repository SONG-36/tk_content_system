# Category And Main Router

```yaml
builder_knowledge_aliases:
  viral_analysis: "01_TikTok_Viral_Analysis_Framework.md"
  automotive_psychology: "02_Car_Cleaning_Content_Psychology.md"
  automotive_hook_database: "03_Cleaning_Video_Hook_Database.md"
  automotive_visual_library: "04_Satisfying_Cleaning_Visual_Library.md"
  script_rules: "05_TikTok_Shop_Script_Writing_Rules.md"
  script_scoring: "06_Video_Script_Scoring_System.md"
  professional_shooting: "07_Professional_Shooting_Standard.md"
  production_planning: "08_Shot_Production_Planning_Framework.md"
  seedance_director: "09_Seedance_Generation_Director.md"
  ai_quality_review: "10_AI_Generation_Quality_Review.md"
  category_and_main_router: "11_Category_and_Main_Router.md"
  automotive_category_pack: "12_Automotive_Category_Pack.md"
  car_vacuum_product_pack: "13_Car_Vacuum_Product_Pack.md"
  home_cleaning_skeleton: "14_Home_Cleaning_Skeleton.md"
  steam_cleaner_skeleton: "15_Steam_Cleaner_Skeleton.md"
  beauty_tools_skeleton: "16_Beauty_Care_Tools_Skeleton.md"
  seedance_reference_pack: "17_Seedance_Reference_Pack.md"
```

Runtime Resolution Rule

Repository paths inside SOURCE FILE sections are provenance only.

Inside GPT Builder, resolve runtime Knowledge through the Builder filenames above.

Do not treat a Knowledge file as missing merely because its original repository path was not separately uploaded.

This Builder upload file combines the only top-level routing documents for the single primary multi-category GPT release.

- `Category_Router` is the only top-level entry.
- `TikTok_Shop_Product_Video_Main_Router` is the formal overall flow.
- `Car_Cleaning_Main_Router` is an automotive sub-router only.
- Missing Product Packs must return generic, partial, or unsupported handling.
- `car_vacuum` rules must not be applied to other products.
- Knowledge 10 is REQUIRED / NOT_RUN until actual generated AI media exists.

---

# SOURCE FILE: workflows/Category_Router.md

---

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
---

# SOURCE FILE: workflows/TikTok_Shop_Product_Video_Main_Router.md

---

# TikTok Shop Product Video Main Router

## Purpose

This is the formal multi-category top-level router.

It sits above the automotive sub-router and decides:

- which category pack to load
- which product pack to load
- whether support is routed, generic supported, partial, or unsupported

---

## Canonical Flow

```text
User Input
-> Category Router
-> Core Viral Analysis
-> Selected Category Pack
-> Selected Product Pack
-> Script Generation
-> Professional Shooting
-> Shot Production Planning
-> REAL_SHOOT / STOCK / AI_GENERATION / HYBRID
-> Seedance Director when routed
-> mark AI Generation Quality Review as REQUIRED / NOT_RUN until generated media exists
-> Commercial Script Scoring
```

---

## Router Layers

### Layer 1: Category Routing

Use `workflows/Category_Router.md` first.

Inside GPT Builder, resolve runtime Knowledge by Builder filenames such as `11_Category_and_Main_Router.md`, not by repository paths.

### Layer 2: Category Logic

Load:

- automotive category pack
- home-cleaning skeleton
- beauty-care skeleton

based on the routing result.

### Layer 3: Product Logic

If a complete product pack exists:

- load it

If only a skeleton or no product pack exists:

- declare `PARTIAL` or `UNSUPPORTED`
- declare `GENERIC_SUPPORTED` where category knowledge can support a conservative generic plan
- do not fabricate expert support

### Layer 4: Production And AI Routing

Use:

- `knowledge/08_Shot_Production_Planning_Framework.md`
- `knowledge/09_Seedance_Generation_Director.md`
- `knowledge/10_AI_Generation_Quality_Review.md`

only after category and product context are known.

Knowledge 10 must not return `PASS` for prompts or storyboards. It executes only after actual generated AI material exists.

---

## Automotive Sub-Chain

```text
Category Router
-> automotive_cleaning
-> Car Cleaning Router
-> Optional Product Pack
```

### Car Vacuum Path

```text
automotive_cleaning
-> car_vacuum
-> Car Vacuum Product Pack
-> Core 01–10
```

---

## Safety And Truth Rule

If the category or product pack is incomplete:

- do not generate unsupported hard claims
- do not generate unsupported safety assurances
- do not auto-upgrade to production-ready guidance
---

# SOURCE FILE: workflows/Car_Cleaning_Main_Router.md

---

# Car Cleaning Main Router

## Purpose

This file defines the automotive-cleaning sub-router.

- It is retained as the automotive sub-router inside the single multi-category GPT.
- It is not a separate primary release.
- In the multi-category architecture, it sits below `workflows/Category_Router.md`.

---

## Canonical Flow

`Category Router`
-> `automotive_cleaning`
-> optional product-pack selection
-> `01 Viral Analysis`
-> `02 Psychology`
-> `03 Hook`
-> `04 Visual Mechanism`
-> `05 Script Generation`
-> `07 Professional Shooting`
-> `08 Shot Production Planning`
-> branch by production type
-> `09 Seedance Director` only for AI_GENERATION/HYBRID routed to Seedance
-> mark `10 AI Generation Quality Review` as REQUIRED / NOT_RUN until actual AI media exists
-> `06 Commercial Script Evaluation`

Written as branches:

```text
Category Router
-> automotive_cleaning
-> optional product pack
-> 01 Viral Analysis
-> 02 Psychology
-> 03 Hook
-> 04 Visual Mechanism
-> 05 Script Generation
-> 07 Professional Shooting
-> 08 Shot Production Planning
    -> REAL_SHOOT: Real Production Brief
    -> STOCK_ASSET: Stock Asset Brief
    -> AI_GENERATION + Seedance: 09 Seedance Director, 10 REQUIRED / NOT_RUN
    -> HYBRID + Seedance: Real Production Brief + 09 Seedance Director, 10 REQUIRED / NOT_RUN
-> 10 AI Generation Quality Review only after generated media exists
-> 06 Commercial Script Evaluation
```

---

## Routing Rules

### 1. Upstream Strategy

- Category selection must already resolve to `automotive_cleaning`.
- If `product_type=car_vacuum`, load the dedicated car-vacuum product pack.
- `01` explains why the benchmark content works.
- `02` defines user psychology and purchase drivers.
- `03` selects hook mechanisms.
- `04` selects visual proof and satisfying mechanisms.
- `05` generates three commercial script versions.
- `07` upgrades each script into professional shot language.

### 2. Production Planning

- `08` is the production gate.
- `08` must decide `REAL_SHOOT | AI_GENERATION | HYBRID | STOCK_ASSET`.
- `08` must decide truth dependency before any AI routing.

### 3. Seedance Routing

- `REAL_SHOOT` does not enter `09`.
- `STOCK_ASSET` does not enter `09`.
- `AI_GENERATION + selected_model=Seedance` must enter `09`.
- `HYBRID + selected_model=Seedance` must output both a real brief and `09` input.

### 4. AI Review

- `10` reviews generated material consistency, truth, continuity, and usability.
- `10` is required before AI-generated footage is accepted.
- Prompt-only or storyboard-only outputs must keep `ai_quality_review_status=NOT_RUN`.

### 5. Commercial Review

- `06` reviews hook, visual, product value, conversion, and production feasibility.
- `06` does not replace `10`.
- `10` does not replace `06`.

### 6. Product-Pack Rule

- `car_vacuum` should use the dedicated product pack.
- other automotive products without a dedicated pack should remain in category-level support and declare `PARTIAL` or `GENERIC_SUPPORTED`.

---

## Per-Branch Outputs

### `REAL_SHOOT`

Output:

- real production brief
- required assets
- fallback

### `STOCK_ASSET`

Output:

- stock usage purpose
- stock search queries
- license requirements
- fallback

### `AI_GENERATION + Seedance`

Output:

- `seedance_input` from `08`
- `seedance_production_package` from `09`
- `ai_quality_review_status=NOT_RUN` until actual generated media exists

### `HYBRID + Seedance`

Output:

- real production brief
- `seedance_input` from `08`
- `seedance_production_package` from `09`
- `ai_quality_review_status=NOT_RUN` until actual generated media exists

---

## Final Acceptance Rule

Do not accept final output unless:

- the commercial script can pass `06`
- every AI-generated shot can pass `10`
- no product-truth shot is left as unsupported pure AI
