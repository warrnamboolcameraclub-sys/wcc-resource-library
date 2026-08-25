# Production Build Pipeline

## Status

Phase 2 implements the production generator but deliberately does **not** deploy GitHub Pages yet.

The canonical flow is:

```text
content/newsletters/*.html
        |
        v
     parser
        |
        v
    validator  ---- blocking error ----> stop
        |
        v
   normaliser
        |
        v
  catalogue records
        |
        +----> _site/library.json
        +----> _site/index.html
        +----> _site/latest.html
        +----> _site/previous.html
        +----> _site/build-report.json
        +----> _site/build-report.html
        +----> _site/assets/
```

`_site/` is generated output. It is ignored by Git and may be deleted at any time.

## Source authority

Newsletter HTML remains the sole manually maintained content source. `library.json` is generated and must never be edited by hand.

## Build command

```bash
python scripts/build_library.py
```

The build performs source validation first. Blocking validation errors prevent generated output from being treated as successful.

## Automated reconciliation

The test suite verifies that:

- 12 migration newsletters are present
- the source contains exactly 172 indexed records
- each indexed source item produces exactly one catalogue record
- all 172 generated `(issue, anchor_id)` identities reconcile to the current baseline catalogue
- generated record IDs are globally unique composites
- all generated deep-link anchors exist in their source newsletter
- all 8 resources retain direct download URLs
- `data-people` and `data-locations` are retained as first-class search fields
- latest and previous resolve to Issues 012 and 011 for the current migration set
- the edition dropdown is generated from publication metadata

The baseline is used only for migration reconciliation tests. It is not read by the production generator.

## Hidden indexed events

Six historical event records are hidden metadata elements. Until those source records receive optional `data-source-anchor` metadata, the generator resolves their open URL to the nearest containing visible element with an ID. This is reported as a warning, not a blocking error.

## GitHub Actions

The Phase 2 workflow:

1. checks out the repository
2. installs Python dependencies
3. runs the production build
4. runs all automated tests
5. uploads `_site/` as a seven-day preview artifact

No Pages deployment occurs in Phase 2.
