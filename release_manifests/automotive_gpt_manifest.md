# Automotive GPT Manifest

Historical diagnostic artifact only.

Do not use this manifest as a current primary release package.

Use `custom_gpt_package/multi_category_gpt/03_BUILDER_SETUP/RELEASE_MANIFEST.md` for the current formal release path.

```yaml
release_manifest:
  release_name: "Automotive Cleaning GPT"
  instructions_file: "instructions/Car_Cleaning_Custom_GPT_Main_Instructions.md"
  main_router: "workflows/Car_Cleaning_Main_Router.md"
  category_router_required: false
  knowledge_files:
    - "knowledge/01_TikTok_Viral_Analysis_Framework.md"
    - "knowledge/02_Car_Cleaning_Content_Psychology.md"
    - "knowledge/03_Cleaning_Video_Hook_Database.md"
    - "knowledge/04_Satisfying_Cleaning_Visual_Library.md"
    - "knowledge/05_TikTok_Shop_Script_Writing_Rules.md"
    - "knowledge/06_Video_Script_Scoring_System.md"
    - "knowledge/07_Professional_Shooting_Standard.md"
    - "knowledge/08_Shot_Production_Planning_Framework.md"
    - "knowledge/09_Seedance_Generation_Director.md"
    - "knowledge/10_AI_Generation_Quality_Review.md"
  category_files:
    - "categories/automotive_cleaning/README.md"
    - "categories/automotive_cleaning/category_pack.md"
    - "categories/automotive_cleaning/product_matrix.md"
    - "categories/automotive_cleaning/material_and_claim_boundaries.md"
  product_pack_files:
    - "categories/automotive_cleaning/products/README.md"
    - "categories/automotive_cleaning/products/car_vacuum/README.md"
    - "categories/automotive_cleaning/products/car_vacuum/product_knowledge.md"
    - "categories/automotive_cleaning/products/car_vacuum/consumer_psychology.md"
    - "categories/automotive_cleaning/products/car_vacuum/hook_library.md"
    - "categories/automotive_cleaning/products/car_vacuum/visual_proof_protocol.md"
    - "categories/automotive_cleaning/products/car_vacuum/attachment_scenario_matrix.md"
    - "categories/automotive_cleaning/products/car_vacuum/claim_boundary.md"
    - "categories/automotive_cleaning/products/car_vacuum/professional_shooting_standard.md"
    - "categories/automotive_cleaning/products/car_vacuum/seedance_and_hybrid_rules.md"
    - "categories/automotive_cleaning/products/car_vacuum/script_templates.md"
    - "categories/automotive_cleaning/products/car_vacuum/test_cases.md"
  seedance_files:
    - "seedance_skills/reference-workflow.md"
  test_files_not_uploaded:
    - "tests/test_category_router.md"
    - "tests/test_car_vacuum_product_pack.md"
    - "tests/test_incomplete_category_fallback.md"
    - "tests/test_cross_category_guardrails.md"
    - "tests/builder_smoke_test_cases.md"
    - "tests/builder_smoke_test_result_template.md"
  development_files_not_uploaded:
    - "core/README.md"
    - "core/core_knowledge_map.md"
    - "version/V1.md"
    - "version/V1_Final_Structure.md"
    - "version/V2_Final_Structure.md"
    - "version/V2_1_Category_Expansion_Structure.md"
    - "version/V2_2_Release_Candidate.md"
    - "version/GPT_Builder_Upload_Checklist.md"
    - "version/GPT_Builder_File_Size_Report.md"
    - "version/File_Reference_Status_Report.md"
    - "master_design.md"
    - "TikTok Shop Car Cleaning AI Video Production System V1.5.md"
  skeleton_files_not_uploaded:
    - "categories/home_cleaning/README.md"
    - "categories/home_cleaning/category_pack_skeleton.md"
    - "categories/home_cleaning/room_and_surface_matrix_skeleton.md"
    - "categories/home_cleaning/claim_and_material_risk_skeleton.md"
    - "categories/home_cleaning/products/README.md"
    - "categories/home_cleaning/products/steam_cleaner/README.md"
    - "categories/home_cleaning/products/steam_cleaner/product_pack_skeleton.md"
    - "categories/home_cleaning/products/steam_cleaner/safety_and_claim_boundary_skeleton.md"
    - "categories/home_cleaning/products/steam_cleaner/material_compatibility_skeleton.md"
    - "categories/beauty_care_tools/README.md"
    - "categories/beauty_care_tools/category_pack_skeleton.md"
    - "categories/beauty_care_tools/human_demo_and_safety_skeleton.md"
    - "categories/beauty_care_tools/before_after_authenticity_skeleton.md"
    - "categories/beauty_care_tools/product_matrix_skeleton.md"
    - "categories/beauty_care_tools/products/README.md"
```

## Notes

- Automotive Cleaning is formally supported.
- `car_vacuum` is the only complete Product Pack in this release.
- Other automotive product types remain generic or partial support.
- Do not upload research, archive, or tests.
