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

The repository contains:

- canonical newsletter HTML
- metadata standards and audits
- agreed repository architecture
- controlled validation configuration
- a first-pass source parser/validator
- automated source-validation tests
- a GitHub Actions validation workflow

GitHub Pages deployment is intentionally not active in this initial package.

## Next implementation phase

Build the production normalisation and generation pipeline:

1. parse and normalise all indexed records
2. resolve catalogue titles and visible deep-link anchors deterministically
3. reconcile generated records against the 172-record baseline
4. generate `library.json`
5. generate the searchable Resource Library
6. generate `latest.html` and `previous.html`
7. generate a build report
8. add GitHub Pages artifact deployment only after validation passes

Do not create a second manually maintained article database.
