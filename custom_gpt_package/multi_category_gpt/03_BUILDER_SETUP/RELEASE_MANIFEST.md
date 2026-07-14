# Release Manifest

```yaml
release_manifest:
  release_name: "TikTok Shop Product Video Director"
  package_type: "multi_category"
  primary_release: true
  instructions_file: "00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md"
  instructions:
    file: "00_INSTRUCTIONS/MAIN_INSTRUCTIONS.md"
    character_count: 7195
    character_limit: 8000
    validation_passed: true
  knowledge_upload_directory: "01_KNOWLEDGE_UPLOAD"
  knowledge_file_count: 18
  builder_ready: true
  category_router: "11_Category_and_Main_Router.md"
  delivery_contract:
    file: "18_Deliverable_and_Output_Contract.md"
    required: true
  mature_categories:
    - automotive_cleaning
  complete_product_packs:
    - car_vacuum
  partial_categories:
    - home_cleaning
    - steam_cleaner
    - beauty_care_tools
  seedance_enabled: true
  seedance_api_connected: false
  builder_uploaded: false
  builder_preview_tested: false
  builder_published: false
  online_builder_verified: false
```

## Notes

- This is the only formal primary release package.
- Automotive standalone packaging is deprecated for formal release use.
- `02_SOURCE_FILES/`, `04_TESTS/`, and `05_AUDIT/` are not Builder upload inputs.
