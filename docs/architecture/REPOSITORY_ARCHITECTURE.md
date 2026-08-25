# WCC Resource Library Repository and Build Architecture

## Status

Architecture baseline for the GitHub migration. GitHub Pages deployment is intentionally deferred until generated records have been reconciled against the existing 172-record Resource Library.

## Design goals

The system must be deterministic, inspectable and recoverable from source. A clean checkout containing the canonical newsletter HTML must be sufficient to regenerate every public Resource Library artefact.

## One source of truth

Canonical source:

```text
content/newsletters/*.html
```

Future permanent pages:

```text
content/pages/*.html
```

Generated data and generated site pages are outputs, not editorial sources.

## Separation of concerns

### Parser

Reads HTML and raw metadata without applying presentation rules.

### Normaliser

Converts raw metadata into stable catalogue records, including arrays, dates, source identity, title, excerpt and link targets.

### Validator

Applies structural and semantic rules and classifies findings as blocking errors or warnings.

### Renderer

Uses validated normalised records to create `library.json`, the Resource Library and stable navigation pages.

### Report

Records source counts, item counts, warnings, errors and build details.

## Identity model

An HTML `id` is an anchor within a document. It must be unique within that document.

The same anchor can legitimately occur in separate newsletter documents when the same event is referenced repeatedly.

The generated catalogue therefore uses a composite identity:

```text
{source_type}:{issue}:{anchor_id}
```

Example:

```text
weekly-update:012:wcc-tip-b008
```

Tip `data-code` remains globally unique.

## Title and visible-anchor resolution

Default title derivation can use visible headings/text where deterministic.

When it is not deterministic, the newsletter HTML may provide:

```html
data-title="Explicit catalogue title"
```

For a hidden/nested metadata element whose own anchor is not the desired reader destination, the HTML may provide:

```html
data-source-anchor="visible-section-id"
```

These fields remain embedded in the canonical newsletter HTML and therefore do not create a second catalogue database.

## URL model

The newsletter wrapper's `data-url` is authoritative.

Typical generated link:

```text
open_url = data-url + "#" + open_anchor_id
```

Resource download link:

```text
download_url = indexed <a> element href
```

The old `public-url-map.json` is retained in `baseline/` only to document/check the migration of Issues 001–012. New issues must not require it.

## Generated site

All generated public output belongs under:

```text
_site/
```

This directory is ignored by Git and uploaded by the future GitHub Pages workflow as a deployment artifact.

This keeps project documentation in `docs/` separate from public generated pages.

## Validation severity

### Blocking errors

Examples include:

- missing required newsletter wrapper metadata
- malformed issue number
- invalid required ISO dates
- duplicate HTML IDs inside one source document
- indexed item missing `id`, `data-index` or `data-category`
- invalid controlled category/item type
- invalid tip code/level relationship
- duplicate tip codes
- resource without a usable `href`
- duplicate generated catalogue record ID

### Warnings

Examples include:

- same anchor ID recurring in multiple newsletter files
- duplicate downloadable resource URL
- unknown series ID
- tag count outside the normal guidance range
- hidden indexed target without explicit visible source anchor
- title falling back to a weak heuristic

Warnings are reported but do not automatically block publication unless policy is tightened later.

## Deployment architecture

The production GitHub Actions workflow should have separate build/validate and deploy responsibilities.

Pull requests and pushes can run validation/build. Deployment must occur only from the production branch after successful validation.

Pages deployment should upload `_site/` as the Pages artifact. A failed build must leave the previous successful public site untouched.

## Current phase gate

Before Pages deployment is enabled:

1. parse all 12 canonical newsletters
2. produce exactly 172 normalised records
3. reconcile generated titles, links, resources, categories, series, tips and events against the existing baseline
4. resolve any intentional differences
5. only then enable the public deployment job
