# File Reference Status Report

## Scope

This report covers formal repository files in:

- `knowledge/`
- `core/`
- `categories/`
- `workflows/`
- `instructions/`
- `version/`
- `seedance_skills/`
- `tests/`
- `release_manifests/`

Status vocabulary:

- `REFERENCED`
- `ENTRY_POINT`
- `TEST_ONLY`
- `ARCHIVE`
- `ORPHAN`

---

## Summary

- Missing internal markdown path references: `0` after script validation
- Unique formal `Knowledge 08`: `knowledge/08_Shot_Production_Planning_Framework.md`
- Unique `Category_Router`: `workflows/Category_Router.md`
- Unique multi-category main router: `workflows/TikTok_Shop_Product_Video_Main_Router.md`
- Car Cleaning sub-router retained: `workflows/Car_Cleaning_Main_Router.md`
- Unexplained formal `ORPHAN` files: `0`

---

## Knowledge

| File | Referenced By | Role | Upload Package | Status |
| --- | --- | --- | --- | --- |
| `knowledge/01_TikTok_Viral_Analysis_Framework.md` | `instructions/TikTok_Shop_Product_Video_Director_Main_Instructions.md`, `workflows/Category_Router.md` | Core viral analysis | automotive, multi_category | REFERENCED |
| `knowledge/02_Car_Cleaning_Content_Psychology.md` | `core/core_knowledge_map.md`, `release_manifests/automotive_gpt_manifest.md` | Automotive category psychology | automotive | REFERENCED |
| `knowledge/03_Cleaning_Video_Hook_Database.md` | `core/core_knowledge_map.md`, `release_manifests/automotive_gpt_manifest.md` | Automotive hook knowledge | automotive | REFERENCED |
| `knowledge/04_Satisfying_Cleaning_Visual_Library.md` | `core/core_knowledge_map.md`, `release_manifests/automotive_gpt_manifest.md` | Automotive visual proof knowledge | automotive | REFERENCED |
| `knowledge/05_TikTok_Shop_Script_Writing_Rules.md` | `instructions/TikTok_Shop_Product_Video_Director_Main_Instructions.md`, `workflows/Category_Router.md` | Core script generation | automotive, multi_category | REFERENCED |
| `knowledge/06_Video_Script_Scoring_System.md` | `instructions/TikTok_Shop_Product_Video_Director_Main_Instructions.md`, `workflows/Category_Router.md` | Commercial scoring | automotive, multi_category | REFERENCED |
| `knowledge/07_Professional_Shooting_Standard.md` | `core/core_knowledge_map.md`, `release_manifests/automotive_gpt_manifest.md` | Legacy automotive shooting standard | automotive | REFERENCED |
| `knowledge/08_Shot_Production_Planning_Framework.md` | `instructions/TikTok_Shop_Product_Video_Director_Main_Instructions.md`, `workflows/TikTok_Shop_Product_Video_Main_Router.md` | Production planning and Seedance handoff | automotive, multi_category | REFERENCED |
| `knowledge/09_Seedance_Generation_Director.md` | `instructions/TikTok_Shop_Product_Video_Director_Main_Instructions.md`, `workflows/TikTok_Shop_Product_Video_Main_Router.md` | Seedance production package generation | automotive, multi_category | REFERENCED |
| `knowledge/10_AI_Generation_Quality_Review.md` | `instructions/TikTok_Shop_Product_Video_Director_Main_Instructions.md`, `workflows/TikTok_Shop_Product_Video_Main_Router.md` | AI material review | automotive, multi_category | REFERENCED |

---

## Core

| File | Referenced By | Role | Upload Package | Status |
| --- | --- | --- | --- | --- |
| `core/README.md` | `release_manifests/automotive_gpt_manifest.md`, `version/V2_1_Category_Expansion_Structure.md` | Core layer entry document | not_uploaded | ENTRY_POINT |
| `core/core_knowledge_map.md` | `core/README.md`, `release_manifests/automotive_gpt_manifest.md` | Legacy-to-core compatibility map | not_uploaded | REFERENCED |

---

## Categories

| File | Referenced By | Role | Upload Package | Status |
| --- | --- | --- | --- | --- |
| `categories/automotive_cleaning/README.md` | `release_manifests/automotive_gpt_manifest.md`, `release_manifests/multi_category_gpt_manifest.md` | Automotive category entry | automotive, multi_category | ENTRY_POINT |
| `categories/automotive_cleaning/category_pack.md` | `instructions/Car_Cleaning_Custom_GPT_Main_Instructions.md`, `workflows/Category_Router.md` | Automotive category pack | automotive, multi_category | REFERENCED |
| `categories/automotive_cleaning/product_matrix.md` | `categories/automotive_cleaning/README.md`, manifests | Automotive product coverage map | automotive, multi_category | REFERENCED |
| `categories/automotive_cleaning/material_and_claim_boundaries.md` | `categories/automotive_cleaning/README.md`, manifests | Automotive category claim boundaries | automotive, multi_category | REFERENCED |
| `categories/automotive_cleaning/products/README.md` | manifests | Automotive products index | automotive, multi_category | REFERENCED |
| `categories/automotive_cleaning/products/car_vacuum/README.md` | `instructions/Car_Cleaning_Custom_GPT_Main_Instructions.md`, `workflows/Category_Router.md` | Car Vacuum pack entry | automotive, multi_category | REFERENCED |
| `categories/automotive_cleaning/products/car_vacuum/product_knowledge.md` | manifests | Car Vacuum product knowledge | automotive, multi_category | REFERENCED |
| `categories/automotive_cleaning/products/car_vacuum/consumer_psychology.md` | manifests | Car Vacuum psychology | automotive, multi_category | REFERENCED |
| `categories/automotive_cleaning/products/car_vacuum/hook_library.md` | manifests | Car Vacuum hook library | automotive, multi_category | REFERENCED |
| `categories/automotive_cleaning/products/car_vacuum/visual_proof_protocol.md` | manifests | Car Vacuum proof protocols | automotive, multi_category | REFERENCED |
| `categories/automotive_cleaning/products/car_vacuum/attachment_scenario_matrix.md` | manifests | Attachment-to-scenario map | automotive, multi_category | REFERENCED |
| `categories/automotive_cleaning/products/car_vacuum/claim_boundary.md` | manifests | Car Vacuum claim boundaries | automotive, multi_category | REFERENCED |
| `categories/automotive_cleaning/products/car_vacuum/professional_shooting_standard.md` | manifests | Car Vacuum shooting standard | automotive, multi_category | REFERENCED |
| `categories/automotive_cleaning/products/car_vacuum/seedance_and_hybrid_rules.md` | manifests | Car Vacuum AI boundary rules | automotive, multi_category | REFERENCED |
| `categories/automotive_cleaning/products/car_vacuum/script_templates.md` | manifests | Car Vacuum templates | automotive, multi_category | REFERENCED |
| `categories/automotive_cleaning/products/car_vacuum/test_cases.md` | manifests | Car Vacuum internal test cases | automotive, multi_category | REFERENCED |
| `categories/home_cleaning/README.md` | manifests | Home Cleaning skeleton entry | multi_category_optional | ENTRY_POINT |
| `categories/home_cleaning/category_pack_skeleton.md` | `workflows/Category_Router.md`, manifests | Home Cleaning skeleton pack | multi_category_optional | REFERENCED |
| `categories/home_cleaning/room_and_surface_matrix_skeleton.md` | manifests | Home Cleaning room/surface skeleton | multi_category_optional | REFERENCED |
| `categories/home_cleaning/claim_and_material_risk_skeleton.md` | manifests | Home Cleaning risk skeleton | multi_category_optional | REFERENCED |
| `categories/home_cleaning/products/README.md` | manifests | Home Cleaning products index | multi_category_optional | REFERENCED |
| `categories/home_cleaning/products/steam_cleaner/README.md` | `workflows/Category_Router.md`, manifests | Steam Cleaner skeleton entry | multi_category_optional | REFERENCED |
| `categories/home_cleaning/products/steam_cleaner/product_pack_skeleton.md` | manifests | Steam Cleaner skeleton pack | multi_category_optional | REFERENCED |
| `categories/home_cleaning/products/steam_cleaner/safety_and_claim_boundary_skeleton.md` | manifests | Steam Cleaner safety skeleton | multi_category_optional | REFERENCED |
| `categories/home_cleaning/products/steam_cleaner/material_compatibility_skeleton.md` | manifests | Steam Cleaner material skeleton | multi_category_optional | REFERENCED |
| `categories/beauty_care_tools/README.md` | manifests | Beauty skeleton entry | multi_category_optional | ENTRY_POINT |
| `categories/beauty_care_tools/category_pack_skeleton.md` | manifests | Beauty category skeleton | multi_category_optional | REFERENCED |
| `categories/beauty_care_tools/human_demo_and_safety_skeleton.md` | manifests | Beauty human-demo skeleton | multi_category_optional | REFERENCED |
| `categories/beauty_care_tools/before_after_authenticity_skeleton.md` | manifests | Beauty authenticity skeleton | multi_category_optional | REFERENCED |
| `categories/beauty_care_tools/product_matrix_skeleton.md` | manifests | Beauty product matrix skeleton | multi_category_optional | REFERENCED |
| `categories/beauty_care_tools/products/README.md` | manifests | Beauty products index | multi_category_optional | REFERENCED |

---

## Workflows And Instructions

| File | Referenced By | Role | Upload Package | Status |
| --- | --- | --- | --- | --- |
| `workflows/Category_Router.md` | `README.md`, `instructions/TikTok_Shop_Product_Video_Director_Main_Instructions.md`, `core/core_knowledge_map.md` | Formal multi-category entry router | multi_category | ENTRY_POINT |
| `workflows/TikTok_Shop_Product_Video_Main_Router.md` | `README.md`, `release_manifests/multi_category_gpt_manifest.md` | Formal multi-category main router | multi_category | ENTRY_POINT |
| `workflows/Car_Cleaning_Main_Router.md` | `README.md`, `version/V2_1_Category_Expansion_Structure.md` | Automotive sub-router | automotive | ENTRY_POINT |
| `instructions/TikTok_Shop_Product_Video_Director_Main_Instructions.md` | `release_manifests/multi_category_gpt_manifest.md`, `version/GPT_Builder_Upload_Checklist.md` | Multi-category instruction file | multi_category | ENTRY_POINT |
| `instructions/Car_Cleaning_Custom_GPT_Main_Instructions.md` | `release_manifests/automotive_gpt_manifest.md`, `version/GPT_Builder_Upload_Checklist.md` | Automotive-only instruction file | automotive | ENTRY_POINT |

---

## Version, Seedance, Tests, And Release

| File | Referenced By | Role | Upload Package | Status |
| --- | --- | --- | --- | --- |
| `version/GPT_Builder_Upload_Checklist.md` | `README.md`, manifests | Builder upload checklist | not_uploaded | REFERENCED |
| `version/V2_1_Category_Expansion_Structure.md` | `README.md`, `version/GPT_Builder_Upload_Checklist.md` | Multi-category structure record | not_uploaded | REFERENCED |
| `version/V2_2_Release_Candidate.md` | manifests | Release candidate state record | not_uploaded | REFERENCED |
| `version/V2_Final_Structure.md` | `version/V2_1_Category_Expansion_Structure.md`, manifests | Automotive-only historical release structure | not_uploaded | REFERENCED |
| `seedance_skills/reference-workflow.md` | `knowledge/09_Seedance_Generation_Director.md`, manifests | Seedance reference syntax rules | optional_upload | REFERENCED |
| `seedance_skills/seedance-prompt/SKILL.md` | `knowledge/09_Seedance_Generation_Director.md` | Seedance prompt source | source_reference | REFERENCED |
| `seedance_skills/seedance-camera/SKILL.md` | `knowledge/09_Seedance_Generation_Director.md` | Seedance camera source | source_reference | REFERENCED |
| `seedance_skills/seedance-motion/SKILL.md` | `knowledge/09_Seedance_Generation_Director.md` | Seedance motion source | source_reference | REFERENCED |
| `tests/test_category_router.md` | `README.md`, manifests | Document-level category router tests | not_uploaded | TEST_ONLY |
| `tests/test_car_vacuum_product_pack.md` | `README.md`, manifests | Document-level Car Vacuum tests | not_uploaded | TEST_ONLY |
| `tests/test_incomplete_category_fallback.md` | `README.md`, manifests | Document-level fallback tests | not_uploaded | TEST_ONLY |
| `tests/test_cross_category_guardrails.md` | `README.md`, manifests | Document-level guardrail tests | not_uploaded | TEST_ONLY |
| `tests/builder_smoke_test_cases.md` | manifests | Manual Builder smoke test definitions | not_uploaded | TEST_ONLY |
| `tests/builder_smoke_test_result_template.md` | manifests | Manual Builder smoke test record template | not_uploaded | TEST_ONLY |
| `release_manifests/automotive_gpt_manifest.md` | `version/V2_2_Release_Candidate.md` | Automotive release manifest | not_uploaded | ENTRY_POINT |
| `release_manifests/multi_category_gpt_manifest.md` | `version/V2_2_Release_Candidate.md` | Multi-category release manifest | not_uploaded | ENTRY_POINT |

---

## Archive

| File | Referenced By | Role | Upload Package | Status |
| --- | --- | --- | --- | --- |
| `archive/08_Shot_Production_Decision_Framework.md` | `knowledge/08_Shot_Production_Planning_Framework.md` deprecation note, version docs | Historical archived 08 | not_uploaded | ARCHIVE |
