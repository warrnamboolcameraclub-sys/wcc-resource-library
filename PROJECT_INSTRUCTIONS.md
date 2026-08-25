# Project Instructions - Warrnambool Camera Club Resource Library Automation

## Objective

Build a GitHub-based automation that generates the Warrnambool Camera Club **Photography Resource Library** from metadata embedded in the Club's Weekly Update HTML files.

The automation must eliminate manual index maintenance while retaining historical links, downloads and newsletter chronology.

## Source of Truth

The canonical newsletter HTML under:

```text
content/newsletters/
```

is the primary source of truth.

Do not maintain a second manual article database. Generated JSON and generated HTML are disposable outputs.

## Current Baseline

Issues **001 through 012** are included and metadata enabled.

The current hand-built baseline Resource Library contains **172 indexed records** across 12 Weekly Updates. It is retained under `baseline/` for reconciliation and visual/behaviour comparison only.

## Locked Metadata Standard

`docs/standards/WCC_Weekly_Update_Metadata_Index_Standard_v1.md` remains unchanged.

Automation-specific interpretation and additions belong in the separate automation addendum.

## Critical Rules

1. Preserve historical wording and chronology.
2. Do not casually rename published indexed IDs.
3. HTML IDs are required to be unique within their HTML document; the same real-world event ID may legitimately recur in different newsletter files.
4. Generated catalogue records require a globally unique composite record ID.
5. Use controlled category values from the metadata standard.
6. Tips are individually indexed using permanent Bxxx / Ixxx / Axxx codes and tip codes are globally unique.
7. Series use stable IDs and numbered parts where the source is a numbered instalment.
8. Downloadable resources use `data-index="resource"` on the real `<a href>`.
9. The published newsletter wrapper carries authoritative `data-url` metadata.
10. Zenfolio deep links depend on permanent anchors plus the delayed hash-scroll helper embedded in newsletter pages.
11. `data-title` and `data-source-anchor` are optional metadata fields for ambiguous title/deep-link cases.
12. Duplicate resource URLs can be historically valid and must not be silently collapsed from the canonical catalogue.
13. The latest-edition dropdown is generated automatically from publication metadata and displays the latest 12 issues.
14. Future substantive permanent website pages must be supportable without changing the newsletter source-of-truth principle.

## Target Repository Architecture

```text
content/
  newsletters/
  pages/

config/
  library-config.json

docs/
  standards/
  audits/
  architecture/

baseline/
  current-resource-library-index.html
  public-url-map.json

templates/
assets/
scripts/
wcc_library/
tests/

.github/
  workflows/
    build-library.yml

Generated only:
_site/
  index.html
  library.json
  latest.html
  previous.html
  build-report.html
  assets/
```

Do not generate the public site into `docs/`; `docs/` is reserved for project documentation, standards and audits.

## Production Build Flow

The intended one-way flow is:

```text
Newsletter HTML
    -> parser
    -> normalised records
    -> validation
    -> library.json
    -> Resource Library / navigation pages
```

On each production build:

1. Discover canonical newsletter and website source files.
2. Parse page-level publication metadata.
3. Parse every indexed element.
4. Normalise metadata into an internal record model.
5. Validate structural and semantic rules.
6. Fail before publication if blocking errors exist.
7. Generate the canonical machine-readable `library.json`.
8. Generate the searchable Resource Library.
9. Generate the most-recent-12 edition dropdown.
10. Generate stable `latest.html` and `previous.html` pages.
11. Generate a validation/build report.
12. Upload `_site/` as the GitHub Pages artifact and deploy only after successful validation.

## Record Identity

HTML anchor identity and catalogue-record identity are different concepts.

Example:

```text
anchor_id: wcc-event-2026-08-06-agm
record_id: weekly-update:008:wcc-event-2026-08-06-agm
```

The anchor can legitimately recur in another issue; the composite catalogue record ID cannot.

## URL Authority

The newsletter wrapper's `data-url` is authoritative.

`baseline/public-url-map.json` exists only as migration/audit evidence for the first 12 issues. It must not become a file that requires weekly manual maintenance.

## Resource Library Behaviour to Preserve

The baseline provides:

- free-text search
- category filter
- series filter
- skill-level filter
- issue filter
- item-type filter
- quick filters
- learning-series cards
- direct `Download File`
- `Open in Issue`
- recent-edition dropdown
- floating `Search & Filters` return button
- responsive mobile layout

These behaviours should be retained unless a deliberate improvement is tested.

Search should use the actual metadata fields, including `data-people` and `data-locations`, rather than relying on those values also appearing in titles or tags.

## Latest / Previous Logic

Sort newsletter pages by valid `data-published` descending, using issue number as a deterministic tie-breaker.

- `latest.html` = highest publication date
- `previous.html` = second-highest publication date
- recent-edition dropdown = first 12
- searchable archive = all valid issues

## Future Website Resources

`content/pages/` is reserved for substantive permanent website material such as competition rules, educational resources and photography guides.

The future UI must distinguish source type clearly, for example:

- Weekly Update
- Website Resource
- Download

Do not invent a permanent-page metadata contract until there is a real page to model, but keep the parser architecture extensible through source adapters.

## Weekly Operating Principle

The intended normal workflow remains:

**Publish newsletter -> save canonical metadata HTML -> commit it -> automation rebuilds everything else.**
