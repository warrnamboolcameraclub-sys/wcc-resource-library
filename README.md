# Warrnambool Camera Club Photography Resource Library

This repository is the automation home for the Warrnambool Camera Club **Photography Resource Library**.

The canonical Weekly Update HTML files are the source of truth. The Resource Library, `library.json`, Latest/Previous navigation pages and build reports will be generated from those files. There is no separately maintained article database.

## Current phase

Phase 2 is implemented: the repository now validates, normalises and generates the complete static Resource Library from Issues 001–012.

The production generator has been reconciled against all **172 baseline record identities**. GitHub Pages deployment is still **not enabled**; the GitHub Action builds `_site/`, runs the test suite and uploads the generated site as a preview artifact for review before publication.

## Source of truth

Canonical newsletter source files live in:

```text
content/newsletters/
```

Future substantive permanent website pages can live in:

```text
content/pages/
```

Generated site output will be written to:

```text
_site/
```

`_site/` is disposable build output and must not be manually maintained or committed.

## Repository layout

```text
content/
  newsletters/       Canonical Weekly Update HTML
  pages/             Future substantive website resources

config/
  library-config.json

docs/
  standards/         Metadata and automation standards
  audits/            Historical metadata audits
  architecture/      Repository/build design

baseline/
  current-resource-library-index.html
  public-url-map.json

templates/            Generated-page templates
assets/               Resource Library CSS/JavaScript
scripts/              Validation/build entry points
wcc_library/          Python parser/validator/normaliser/renderer modules
tests/                Automated tests
.github/workflows/    GitHub Actions workflow

_site/                Generated output; never committed
```

## Local source validation

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Build the complete static site:

```bash
python scripts/build_library.py
```

The generated site is written to `_site/`.

Run source validation only:

```bash
python scripts/validate_sources.py
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

The current canonical set is expected to contain **12 newsletters and 172 indexed records**.

## Important architecture decisions

- HTML IDs must be unique **within each HTML document**. The same real-world event anchor may legitimately recur in different issues.
- A generated catalogue record will use a composite identity such as `weekly-update:012:wcc-tip-b008`.
- `data-url` embedded in each newsletter is authoritative. `baseline/public-url-map.json` is retained only for migration/audit comparison and is not part of the weekly publishing workflow.
- `data-title` and `data-source-anchor` are optional embedded metadata fields for records where title or visible deep-link target cannot be derived safely.
- Duplicate PDF/resource URLs are preserved as separate historical occurrences and reported as warnings rather than errors.
- The latest-edition dropdown will be generated from publication metadata and limited to the most recent 12 editions, while the searchable archive can include all editions.

See `PROJECT_INSTRUCTIONS.md` and `docs/architecture/REPOSITORY_ARCHITECTURE.md` for the implementation contract.
