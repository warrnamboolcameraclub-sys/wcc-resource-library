# START HERE

This repository has been prepared for the Warrnambool Camera Club Photography Resource Library automation project.

## Before implementation

Read these files in order:

1. `PROJECT_INSTRUCTIONS.md`
2. `docs/standards/WCC_Weekly_Update_Metadata_Index_Standard_v1.md`
3. `docs/standards/WCC_Resource_Library_Automation_Addendum_v1_2_DRAFT.md`
4. `docs/architecture/REPOSITORY_ARCHITECTURE.md`
5. `config/library-config.json`

Then inspect:

- all files under `content/newsletters/`
- `baseline/current-resource-library-index.html`
- `baseline/public-url-map.json` as migration/audit evidence only

## Current baseline

Issues 001–012 are metadata enabled and contain 172 indexed records.

The baseline Resource Library is reference material for reconciliation and front-end behaviour. It is not a source of truth.

## Current repository state

Phase 2 is complete. The repository contains:

- canonical newsletter HTML
- metadata standards and audits
- controlled validation configuration
- production parser, validator, normaliser and renderer
- generated `library.json` logic
- generated searchable Resource Library logic
- automatic latest-12 edition navigation
- generated `latest.html` and `previous.html`
- direct resource-download preservation
- deep-link resolution
- build reports
- automated reconciliation and generation tests
- a GitHub Actions build workflow that uploads a preview artifact

GitHub Pages deployment is intentionally not active yet.

## Current build

Run:

```bash
python scripts/build_library.py
```

The complete disposable site is generated under `_site/`. The current migration set produces **172 catalogue records with zero blocking validation errors**.

## Next phase

Review the generated preview site, then add GitHub Pages deployment for `_site/`. After that, the normal weekly operation becomes:

**Publish newsletter -> commit canonical HTML -> automation validates, rebuilds and publishes.**

Do not create a second manually maintained article database.
