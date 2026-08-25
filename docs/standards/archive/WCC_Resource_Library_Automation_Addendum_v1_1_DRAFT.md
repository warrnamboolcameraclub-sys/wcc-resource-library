# WCC Resource Library Automation Addendum v1.1 DRAFT

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

The generator builds the article destination as:

```text
data-url + "#" + element.id
```

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
- use the Weekly Update `data-url` plus the element ID as **Open in Issue**

Do not duplicate the download URL into another metadata field unless a later requirement makes it necessary.

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

## 5. Visible Link Target

If a metadata element is hidden or nested inside another visible section, generated `Open in Issue` links should prefer the nearest visible indexed parent anchor rather than a hidden target.

A future optional field could be:

```text
data-source-anchor="wcc-2026-012-parent-section"
```

Do not add this unless the parser actually needs it.

## 6. Recent Edition Dropdown

Generate the edition dropdown from newsletter page metadata:
- sort by `data-published` descending
- show the latest 12 editions
- use `data-url` as the destination
- do not maintain the dropdown manually

The searchable archive may contain more than 12 issues even though the quick edition dropdown shows only the latest 12.

## 7. Latest and Previous Stable Pages

GitHub Pages should expose stable navigation endpoints:

```text
/latest.html
/previous.html
```

On each build:
- Latest = highest `data-published`
- Previous = second-highest `data-published`

These pages may redirect to the Zenfolio issue while still displaying a visible fallback link.

This allows the permanent Zenfolio menu to contain:
- Photography Resource Library
- Latest Issue
- Previous Issue

without weekly menu maintenance.

## 8. Permanent Website Resources

A second collection should be supported:

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

The search result should clearly distinguish:
- Weekly Update
- Website Resource
- Download

## 9. Validation During Build

Fail the build, or at minimum issue a prominent warning, for:
- duplicate permanent IDs
- duplicate tip codes
- invalid controlled categories
- numbered series items missing `data-part`
- published newsletter missing `data-url`
- resource item missing `href`
- indexed item missing `id`
- issue number not three digits
- invalid ISO publication/event dates

Also warn about:
- duplicate downloadable resource URLs
- unknown series IDs
- indexed items with no usable title

## 10. Generated Outputs

Recommended GitHub Pages outputs:

```text
docs/index.html
docs/library.json
docs/latest.html
docs/previous.html
docs/build-report.html
```

`library.json` should become the reusable machine-readable catalogue.

## 11. Resource De-duplication

The same PDF can legitimately be mentioned in multiple newsletters.

Recommended future behaviour:
- preserve every historical article reference
- optionally collapse identical **download resources** by URL in the library UI
- retain a list of the issues in which the resource appeared

This is an enhancement, not a blocker for the first automated build.
