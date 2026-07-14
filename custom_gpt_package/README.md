# Custom GPT Package

`multi_category_gpt/`

This is the current project's only formal Custom GPT release package.

Automotive Cleaning and Car Vacuum are mature internal modules within it.

Do not maintain two formal GPT release packages for this project.

## Regenerate

```bash
python3 tools/build_custom_gpt_package.py
```

- Do not manually edit generated package files.
- Modify source files first, then rebuild.
- Source files remain the only source of truth.
- The release package is a generated artifact.
- This repo does not automatically modify GPT Builder.
