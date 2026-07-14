# GPT Builder File Size Report

## Scope

This report measures the two release manifests defined in:

- `release_manifests/automotive_gpt_manifest.md`
- `release_manifests/multi_category_gpt_manifest.md`

Character and size measurements are repository-side estimates only.

---

## Per-File Sizes

### Automotive GPT Required Upload Files

| File | Bytes |
| --- | ---: |
| `instructions/Car_Cleaning_Custom_GPT_Main_Instructions.md` | 3568 |
| `workflows/Car_Cleaning_Main_Router.md` | 3374 |
| `knowledge/01_TikTok_Viral_Analysis_Framework.md` | 10179 |
| `knowledge/02_Car_Cleaning_Content_Psychology.md` | 8823 |
| `knowledge/03_Cleaning_Video_Hook_Database.md` | 6616 |
| `knowledge/04_Satisfying_Cleaning_Visual_Library.md` | 5671 |
| `knowledge/05_TikTok_Shop_Script_Writing_Rules.md` | 9743 |
| `knowledge/06_Video_Script_Scoring_System.md` | 7581 |
| `knowledge/07_Professional_Shooting_Standard.md` | 6396 |
| `knowledge/08_Shot_Production_Planning_Framework.md` | 8919 |
| `knowledge/09_Seedance_Generation_Director.md` | 8504 |
| `knowledge/10_AI_Generation_Quality_Review.md` | 3769 |
| `categories/automotive_cleaning/README.md` | 1045 |
| `categories/automotive_cleaning/category_pack.md` | 1787 |
| `categories/automotive_cleaning/product_matrix.md` | 1281 |
| `categories/automotive_cleaning/material_and_claim_boundaries.md` | 1220 |
| `categories/automotive_cleaning/products/README.md` | 295 |
| `categories/automotive_cleaning/products/car_vacuum/README.md` | 444 |
| `categories/automotive_cleaning/products/car_vacuum/product_knowledge.md` | 1122 |
| `categories/automotive_cleaning/products/car_vacuum/consumer_psychology.md` | 746 |
| `categories/automotive_cleaning/products/car_vacuum/hook_library.md` | 4358 |
| `categories/automotive_cleaning/products/car_vacuum/visual_proof_protocol.md` | 4401 |
| `categories/automotive_cleaning/products/car_vacuum/attachment_scenario_matrix.md` | 764 |
| `categories/automotive_cleaning/products/car_vacuum/claim_boundary.md` | 1200 |
| `categories/automotive_cleaning/products/car_vacuum/professional_shooting_standard.md` | 970 |
| `categories/automotive_cleaning/products/car_vacuum/seedance_and_hybrid_rules.md` | 1326 |
| `categories/automotive_cleaning/products/car_vacuum/script_templates.md` | 2036 |
| `categories/automotive_cleaning/products/car_vacuum/test_cases.md` | 4380 |
| `seedance_skills/reference-workflow.md` | 5894 |

### Multi-Category GPT Required Upload Files

| File | Bytes |
| --- | ---: |
| `instructions/TikTok_Shop_Product_Video_Director_Main_Instructions.md` | 2089 |
| `workflows/Category_Router.md` | 4510 |
| `workflows/TikTok_Shop_Product_Video_Main_Router.md` | 1775 |
| `knowledge/01_TikTok_Viral_Analysis_Framework.md` | 10179 |
| `knowledge/05_TikTok_Shop_Script_Writing_Rules.md` | 9743 |
| `knowledge/06_Video_Script_Scoring_System.md` | 7581 |
| `knowledge/08_Shot_Production_Planning_Framework.md` | 8919 |
| `knowledge/09_Seedance_Generation_Director.md` | 8504 |
| `knowledge/10_AI_Generation_Quality_Review.md` | 3769 |
| `categories/automotive_cleaning/README.md` | 1045 |
| `categories/automotive_cleaning/category_pack.md` | 1787 |
| `categories/automotive_cleaning/product_matrix.md` | 1281 |
| `categories/automotive_cleaning/material_and_claim_boundaries.md` | 1220 |
| `categories/automotive_cleaning/products/README.md` | 295 |
| `categories/automotive_cleaning/products/car_vacuum/README.md` | 444 |
| `categories/automotive_cleaning/products/car_vacuum/product_knowledge.md` | 1122 |
| `categories/automotive_cleaning/products/car_vacuum/consumer_psychology.md` | 746 |
| `categories/automotive_cleaning/products/car_vacuum/hook_library.md` | 4358 |
| `categories/automotive_cleaning/products/car_vacuum/visual_proof_protocol.md` | 4401 |
| `categories/automotive_cleaning/products/car_vacuum/attachment_scenario_matrix.md` | 764 |
| `categories/automotive_cleaning/products/car_vacuum/claim_boundary.md` | 1200 |
| `categories/automotive_cleaning/products/car_vacuum/professional_shooting_standard.md` | 970 |
| `categories/automotive_cleaning/products/car_vacuum/seedance_and_hybrid_rules.md` | 1326 |
| `categories/automotive_cleaning/products/car_vacuum/script_templates.md` | 2036 |
| `categories/automotive_cleaning/products/car_vacuum/test_cases.md` | 4380 |
| `categories/home_cleaning/README.md` | 495 |
| `categories/home_cleaning/category_pack_skeleton.md` | 1018 |
| `categories/home_cleaning/room_and_surface_matrix_skeleton.md` | 620 |
| `categories/home_cleaning/claim_and_material_risk_skeleton.md` | 759 |
| `categories/home_cleaning/products/README.md` | 202 |
| `categories/home_cleaning/products/steam_cleaner/README.md` | 215 |
| `categories/home_cleaning/products/steam_cleaner/product_pack_skeleton.md` | 537 |
| `categories/home_cleaning/products/steam_cleaner/safety_and_claim_boundary_skeleton.md` | 552 |
| `categories/home_cleaning/products/steam_cleaner/material_compatibility_skeleton.md` | 488 |
| `categories/beauty_care_tools/README.md` | 336 |
| `categories/beauty_care_tools/category_pack_skeleton.md` | 591 |
| `categories/beauty_care_tools/human_demo_and_safety_skeleton.md` | 471 |
| `categories/beauty_care_tools/before_after_authenticity_skeleton.md` | 468 |
| `categories/beauty_care_tools/product_matrix_skeleton.md` | 822 |
| `categories/beauty_care_tools/products/README.md` | 234 |
| `seedance_skills/reference-workflow.md` | 5894 |

---

## Package Summary

| 发布包 | 文件数量 | 总大小 | 风险 | 建议 |
| --- | ---: | ---: | --- | --- |
| Automotive GPT | 29 | 116,412 bytes | Medium | Full package is manageable but large; keep research/tests excluded. |
| Multi-category GPT | 41 | 98,146 bytes | High | More files and more status-sensitive skeletons; requires stronger manual Builder verification. |

---

## Optional Files

- `seedance_skills/reference-workflow.md`
- Skeleton category files for multi-category package

---

## Must Not Upload

- `archive/`
- `research/`
- `tests/`
- `core/`
- `version/`
- `.DS_Store`

---

## Minimal Viable Packages

### Automotive Minimal Package

- automotive instructions
- automotive router
- Knowledge `01-10`
- automotive category pack
- Car Vacuum product pack only when needed

### Multi-Category Minimal Package

- multi-category instructions
- `Category_Router`
- multi-category main router
- Knowledge `01`, `05`, `06`, `08`, `09`, `10`
- automotive category pack
- Car Vacuum product pack
- upload skeletons only if partial support must be explicitly surfaced
