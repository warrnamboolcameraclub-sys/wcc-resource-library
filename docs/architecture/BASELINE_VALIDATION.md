# Baseline Source Validation

Validation run against the repository-ready migration package before delivery.

## Canonical inventory

- Newsletter source files: **12**
- Indexed records: **172**
- Articles: **100**
- Events: **43**
- Resources: **8**
- Tips: **21**
- Blocking validation errors: **0**

## Expected warnings

The first-pass validator reports **16 non-blocking warnings** from the historical source set:

- 6 items contain 8 tags where the metadata standard recommends approximately 3–7
- 9 event anchor IDs recur across separate newsletter documents
- 1 downloadable resource URL (the APJA judging PDF) appears in two issues

These warnings are intentional examples of why warning/error severity is separated.

## Tests

The initial automated tests confirm:

- Issues 001–012 are present
- the canonical source contains exactly 172 indexed records
- embedded newsletter `data-url` values match the legacy migration URL map for Issues 001–012
- the canonical source set has no blocking validation errors

## Source preservation

The 12 newsletter HTML files in this repository-ready package were copied unchanged from the supplied starter package.

The automation-specific architecture is captured outside the locked newsletter metadata standard, including the revised draft automation addendum.
