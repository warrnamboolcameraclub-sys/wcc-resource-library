# WCC Resource Library Automation Addendum v1.2 DRAFT

This is an automation addendum to the locked **WCC Weekly Update Metadata Index Standard v1**.
It does not silently replace or revise v1. Adopt it formally only after review.

## 1. Page URL

For a published Weekly Update, include the live page URL on the main wrapper:

```html
<div class="wcc-weekly"
     data-publication="weekly-update"
     data-issue="012"
     data-published="2026-08-24"
     data-url="https://warrnamboolcameraclub.zenfolio.com/weekly-newsletter-012">
```

The embedded `data-url` is authoritative for automation.

A legacy `public-url-map.json` may be retained for migration/audit comparison, but it must not become a second file that requires weekly maintenance.

## 2. Downloadable Resources

Put metadata directly on the actual download link:

```html
<a id="wcc-resource-2026-012-lightroom-005-guide"
   data-index="resource"
   data-category="editing"
   data-series="lightroom-basics"
   data-part="5"
   data-tags="lightroom,sharpening,pdf,downloadable-guide"
   href="https://.../guide.pdf">
   Download ...
</a>
```

The generator should:

- use the element `href` as **Download File**
- use the Weekly Update `data-url` plus the resolved source anchor as **Open in Issue**

Do not duplicate the download URL into another manually maintained metadata field.

The same PDF can legitimately occur in more than one issue. Each historical occurrence remains a catalogue record even if the UI later groups identical download URLs.

## 3. Source Types

The Resource Library is intended to grow beyond newsletters.

Recommended source field for future permanent site pages:

```text
data-source="weekly-update"
data-source="website"
```

Until formally adopted, newsletter pages can be inferred from `data-publication="weekly-update"`.

## 4. Deep Links on Zenfolio

Every newsletter source used by the Resource Library should retain:

- permanent `id` values on indexed items
- `scroll-margin-top`
- the delayed hash/deep-link helper script

This is required because Zenfolio may inject custom page content after the browser's first normal anchor attempt.

## 5. Optional Explicit Catalogue Title and Source Anchor

Most catalogue titles and open targets can be derived from the visible HTML.

Where title derivation would be ambiguous, an indexed element may supply:

```html
data-title="Understand What ISO Does"
```

Where a metadata element is hidden or nested and its own ID is not the preferred reader destination, it may supply:

```html
data-source-anchor="wcc-2026-012-parent-section"
```

These optional attributes remain part of the canonical newsletter HTML. They do not create a separate article database.

Recommended source-anchor resolution order:

1. explicit `data-source-anchor`
2. nearest suitable visible ancestor/section anchor
3. indexed element's own `id`

The build should verify that the resolved anchor actually exists in the source HTML.

## 6. Record Identity and ID Uniqueness

HTML anchor IDs and generated catalogue record IDs are different concepts.

An HTML `id` must be unique **within its HTML document**.

The same real-world event anchor may legitimately recur in different newsletter files. For example, an AGM event can be referenced in several successive issues.

The generator should create a globally unique composite record ID, for example:

```text
weekly-update:008:wcc-event-2026-08-06-agm
```

Tip `data-code` values remain globally unique.

## 7. Recent Edition Dropdown

Generate the edition dropdown from newsletter page metadata:

- sort by `data-published` descending
- use issue number as a deterministic tie-breaker if required
- show the latest 12 editions
- use `data-url` as the destination
- do not maintain the dropdown manually

The searchable archive may contain more than 12 issues even though the quick edition dropdown shows only the latest 12.

## 8. Latest and Previous Stable Pages

GitHub Pages should expose stable navigation endpoints:

```text
/latest.html
/previous.html
```

On each build:

- Latest = highest valid `data-published`
- Previous = second-highest valid `data-published`

These pages may redirect to the Zenfolio issue while still displaying a visible fallback link.

This allows the permanent Zenfolio menu to contain:

- Photography Resource Library
- Latest Issue
- Previous Issue

without weekly menu maintenance.

## 9. Permanent Website Resources

A second collection should be supportable:

```text
content/pages/
```

Only substantive pages should be indexed.

Examples:

- current Competition Rules
- educational resources
- workshop information
- VAPS information
- downloadable photography guides

The search result should clearly distinguish source type, for example:

- Weekly Update
- Website Resource
- Download

Do not invent a final permanent-page metadata contract until a real substantive page is available to model.

## 10. Validation During Build

### Blocking errors

Fail the build for conditions that prevent a deterministic, safe catalogue, including:

- duplicate HTML IDs within one source document
- duplicate tip codes
- invalid controlled categories
- invalid item types
- invalid tip code/level relationship
- numbered series instalment missing required `data-part`
- published newsletter missing `data-url`
- resource item missing a usable `href`
- indexed item missing `id`
- issue number not three digits
- invalid required ISO publication/event dates
- duplicate generated composite record IDs

### Warnings

Warn prominently for conditions that can be historically legitimate or require editorial review, including:

- same anchor ID appearing in different newsletter documents
- duplicate downloadable resource URLs
- unknown series IDs
- indexed items with no confidently derived title
- tag count outside the normal guidance range
- hidden indexed targets without an explicit or safely derived visible source anchor

## 11. Generated Outputs

Recommended GitHub Pages build output:

```text
_site/index.html
_site/library.json
_site/latest.html
_site/previous.html
_site/build-report.html
_site/assets/
```

`_site/` is generated, disposable output and should not be committed.

`library.json` becomes the reusable machine-readable catalogue but is generated from source HTML; it is not manually edited.

## 12. Resource De-duplication

The same PDF can legitimately be mentioned in multiple newsletters.

Canonical behaviour:

- preserve every historical article/resource occurrence
- never silently de-duplicate the generated record set

Optional UI enhancement:

- visually group identical download URLs
- show the issues in which that resource appeared

This UI grouping must not destroy historical catalogue records.
