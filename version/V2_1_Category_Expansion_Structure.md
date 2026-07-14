# V2.1 Category Expansion Structure

## Purpose

This file defines the repository structure after Phase 1B:

- multi-category routing
- category packs
- product packs
- automotive backward compatibility

---

## 1. Core Layer

Core layer files:

- `core/README.md`
- `core/core_knowledge_map.md`
- `knowledge/01_TikTok_Viral_Analysis_Framework.md`
- `knowledge/05_TikTok_Shop_Script_Writing_Rules.md`
- `knowledge/06_Video_Script_Scoring_System.md`
- `knowledge/08_Shot_Production_Planning_Framework.md`
- `knowledge/09_Seedance_Generation_Director.md`
- `knowledge/10_AI_Generation_Quality_Review.md`
- `workflows/Category_Router.md`
- `workflows/TikTok_Shop_Product_Video_Main_Router.md`

---

## 2. Category Packs

### Active Category Pack

- `categories/automotive_cleaning/`

### Skeleton Category Packs

- `categories/home_cleaning/`
- `categories/beauty_care_tools/`

---

## 3. Product Packs

### Complete Product Pack

- `categories/automotive_cleaning/products/car_vacuum/`

### Skeleton Product Pack

- `categories/home_cleaning/products/steam_cleaner/`

---

## 4. Legacy Knowledge Compatibility

Current legacy files remain active for backward compatibility:

- `knowledge/02_Car_Cleaning_Content_Psychology.md`
- `knowledge/03_Cleaning_Video_Hook_Database.md`
- `knowledge/04_Satisfying_Cleaning_Visual_Library.md`
- `knowledge/07_Professional_Shooting_Standard.md`
- `workflows/Car_Cleaning_Main_Router.md`
- `instructions/Car_Cleaning_Custom_GPT_Main_Instructions.md`

These now function as the automotive-specialized layer.

---

## 5. Support Status

| Layer | Status |
| --- | --- |
| Multi-category router | COMPLETE |
| Automotive category pack | COMPLETE |
| Car vacuum product pack | COMPLETE |
| Home cleaning category | SKELETON_ONLY |
| Steam cleaner product pack | SKELETON_ONLY |
| Beauty care tools category | SKELETON_ONLY |

---

## 6. Builder Upload Strategy

### Automotive-Cleaning GPT Upload Pack

Use:

- `instructions/Car_Cleaning_Custom_GPT_Main_Instructions.md`
- automotive legacy knowledge
- `knowledge/08-10`
- automotive category pack
- car vacuum product pack when needed
- `workflows/Car_Cleaning_Main_Router.md`
- `release_manifests/automotive_gpt_manifest.md`

### Multi-Category GPT Upload Pack

Use:

- `instructions/TikTok_Shop_Product_Video_Director_Main_Instructions.md`
- core knowledge
- `workflows/Category_Router.md`
- `workflows/TikTok_Shop_Product_Video_Main_Router.md`
- active category packs
- complete product packs
- `release_manifests/multi_category_gpt_manifest.md`

### Validation Companions

- `version/GPT_Builder_Upload_Checklist.md`
- `version/GPT_Builder_File_Size_Report.md`
- `tests/builder_smoke_test_cases.md`
- `tests/builder_smoke_test_result_template.md`

---

## 7. File-Limit Merge Strategy

If Builder file count becomes constrained:

- merge category-pack index files before merging product packs
- do not merge archive or research files into formal upload bundles
- keep skeleton files clearly labeled if uploaded at all

---

## 8. Exclusions

Do not treat these as complete production knowledge:

- `research/`
- `archive/`
- any `*_skeleton.md`

Only complete packs may be treated as full production support.
