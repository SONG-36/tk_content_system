# Multi-Category GPT Manifest

Repository-side reference manifest only.

The current formal Builder release package is generated under:

- `custom_gpt_package/multi_category_gpt/`
- `custom_gpt_package/multi_category_gpt/03_BUILDER_SETUP/RELEASE_MANIFEST.md`

```yaml
release_manifest:
  release_name: "TikTok Shop Product Video Director"
  primary_release: true
  instructions_file: "instructions/TikTok_Shop_Product_Video_Director_Main_Instructions.md"
  instructions:
    file: "00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md"
    character_count: 7195
    character_limit: 8000
    validation_passed: true
  main_router: "workflows/TikTok_Shop_Product_Video_Main_Router.md"
  category_router: "workflows/Category_Router.md"
  knowledge_file_count: 18
  builder_ready: true
  builder_uploaded: false
  builder_preview_tested: false
  builder_published: false
  delivery_contract:
    file: "18_Deliverable_and_Output_Contract.md"
    required: true
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
    - "custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/11_Category_and_Main_Router.md"
    - "custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/12_Automotive_Category_Pack.md"
    - "custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/13_Car_Vacuum_Product_Pack.md"
    - "custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/14_Home_Cleaning_Skeleton.md"
    - "custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/15_Steam_Cleaner_Skeleton.md"
    - "custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/16_Beauty_Care_Tools_Skeleton.md"
    - "custom_gpt_package/multi_category_gpt/01_KNOWLEDGE_UPLOAD/17_Seedance_Reference_Pack.md"
    - "knowledge/18_Deliverable_and_Output_Contract.md"
  category_files:
    - "categories/automotive_cleaning/README.md"
    - "categories/automotive_cleaning/category_pack.md"
    - "categories/automotive_cleaning/product_matrix.md"
    - "categories/automotive_cleaning/material_and_claim_boundaries.md"
    - "categories/home_cleaning/README.md"
    - "categories/home_cleaning/category_pack_skeleton.md"
    - "categories/home_cleaning/room_and_surface_matrix_skeleton.md"
    - "categories/home_cleaning/claim_and_material_risk_skeleton.md"
    - "categories/beauty_care_tools/README.md"
    - "categories/beauty_care_tools/category_pack_skeleton.md"
    - "categories/beauty_care_tools/human_demo_and_safety_skeleton.md"
    - "categories/beauty_care_tools/before_after_authenticity_skeleton.md"
    - "categories/beauty_care_tools/product_matrix_skeleton.md"
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
    - "categories/home_cleaning/products/README.md"
    - "categories/home_cleaning/products/steam_cleaner/README.md"
    - "categories/home_cleaning/products/steam_cleaner/product_pack_skeleton.md"
    - "categories/home_cleaning/products/steam_cleaner/safety_and_claim_boundary_skeleton.md"
    - "categories/home_cleaning/products/steam_cleaner/material_compatibility_skeleton.md"
    - "categories/beauty_care_tools/products/README.md"
  skeleton_files:
    - "categories/home_cleaning/category_pack_skeleton.md"
    - "categories/home_cleaning/room_and_surface_matrix_skeleton.md"
    - "categories/home_cleaning/claim_and_material_risk_skeleton.md"
    - "categories/home_cleaning/products/steam_cleaner/product_pack_skeleton.md"
    - "categories/home_cleaning/products/steam_cleaner/safety_and_claim_boundary_skeleton.md"
    - "categories/home_cleaning/products/steam_cleaner/material_compatibility_skeleton.md"
    - "categories/beauty_care_tools/category_pack_skeleton.md"
    - "categories/beauty_care_tools/human_demo_and_safety_skeleton.md"
    - "categories/beauty_care_tools/before_after_authenticity_skeleton.md"
    - "categories/beauty_care_tools/product_matrix_skeleton.md"
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
    - "archive/08_Shot_Production_Decision_Framework.md"
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
```

## Notes

- Automotive Cleaning is the only mature category.
- `car_vacuum` is the only complete Product Pack.
- Home Cleaning, Steam Cleaner, and Beauty Care remain skeleton or partial support.
- If skeleton files are uploaded, Instructions must clearly expose `PARTIAL` or `UNSUPPORTED`.
