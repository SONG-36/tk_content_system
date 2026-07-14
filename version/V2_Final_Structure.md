# V2 Final Structure

## Status Note

This file records the Phase 1A automotive-only structure.

For the multi-category Phase 1B architecture, use:

- `version/V2_1_Category_Expansion_Structure.md`

## Purpose

This file defines the formal V2 document structure for the Car Cleaning Custom GPT repository after Seedance workflow integration phase 1.

---

## 1. Official Files

### 1.1 Main Instructions

- `instructions/Car_Cleaning_Custom_GPT_Main_Instructions.md`

### 1.2 Official Knowledge Files

- `knowledge/01_TikTok_Viral_Analysis_Framework.md`
- `knowledge/02_Car_Cleaning_Content_Psychology.md`
- `knowledge/03_Cleaning_Video_Hook_Database.md`
- `knowledge/04_Satisfying_Cleaning_Visual_Library.md`
- `knowledge/05_TikTok_Shop_Script_Writing_Rules.md`
- `knowledge/06_Video_Script_Scoring_System.md`
- `knowledge/07_Professional_Shooting_Standard.md`
- `knowledge/08_Shot_Production_Planning_Framework.md`
- `knowledge/09_Seedance_Generation_Director.md`
- `knowledge/10_AI_Generation_Quality_Review.md`

### 1.3 Official Workflow File

- `workflows/Car_Cleaning_Main_Router.md`

---

## 2. Seedance Source Files

These files remain in the repo as source materials and should not be deleted:

- `seedance_skills/seedance-prompt/SKILL.md`
- `seedance_skills/seedance-camera/SKILL.md`
- `seedance_skills/seedance-motion/SKILL.md`
- `seedance_skills/reference-workflow.md`

Usage rule:

- `reference-workflow.md` may be uploaded as supplementary knowledge if Builder context needs explicit reference-role syntax.
- The three raw `SKILL.md` files are source references for repo maintenance and Knowledge 09 alignment.

---

## 3. Builder Upload Order

Recommended order:

1. `instructions/Car_Cleaning_Custom_GPT_Main_Instructions.md`
2. `knowledge/01_TikTok_Viral_Analysis_Framework.md`
3. `knowledge/02_Car_Cleaning_Content_Psychology.md`
4. `knowledge/03_Cleaning_Video_Hook_Database.md`
5. `knowledge/04_Satisfying_Cleaning_Visual_Library.md`
6. `knowledge/05_TikTok_Shop_Script_Writing_Rules.md`
7. `knowledge/06_Video_Script_Scoring_System.md`
8. `knowledge/07_Professional_Shooting_Standard.md`
9. `knowledge/08_Shot_Production_Planning_Framework.md`
10. `knowledge/09_Seedance_Generation_Director.md`
11. `knowledge/10_AI_Generation_Quality_Review.md`
12. `seedance_skills/reference-workflow.md`
13. `workflows/Car_Cleaning_Main_Router.md`

---

## 4. Development-Only Files

These files are useful for repo development but are not formal GPT Knowledge by default:

- `master_design.md`
- `TikTok Shop Car Cleaning AI Video Production System V1.5.md`
- `version/V1.md`
- `version/V1_Final_Structure.md`

---

## 5. Research Files Not For Formal Upload

Do not treat these files as official Knowledge uploads:

- `research/car_cleaning_psychology_research.md`
- `research/cleaning_hook_research.md`
- `research/cleaning_visual_research.md`
- `research/marketing_framework_analysis.md`
- `research/prompt_framework_analysis.md`
- `research/shot_production_planning_research.md`

Reason:

- they are source research and design support files
- they contain exploratory material and alternate structures
- they should not compete with the formal Knowledge files

---

## 6. Deprecated Files

- `archive/08_Shot_Production_Decision_Framework.md`

Rule:

- never upload this archived file together with formal Knowledge 08

---

## 7. V2 Routing Summary

Formal chain:

`01 -> 02 -> 03 -> 04 -> 05 -> 07 -> 08 -> 09 -> 10 -> 06`

Branch logic:

- `REAL_SHOOT` stops at real production brief
- `STOCK_ASSET` stops at stock asset brief
- `AI_GENERATION + Seedance` must go through `09` then `10`
- `HYBRID + Seedance` must output both real brief and `09`, then pass `10`
