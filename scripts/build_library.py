#!/usr/bin/env python3
"""Validate newsletter sources and build the complete static Resource Library site."""

from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wcc_library.normalise import normalise_pages
from wcc_library.parser import discover_newsletters, parse_newsletter
from wcc_library.renderer import render_site
from wcc_library.report import make_build_report
from wcc_library.validator import load_config, validate_pages


def main() -> int:
    config = load_config(ROOT)
    paths = discover_newsletters(ROOT)
    pages = [parse_newsletter(path) for path in paths]
    findings = validate_pages(pages, config)
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]

    print(f"Newsletter files: {len(pages)}")
    print(f"Indexed source records: {sum(len(page.items) for page in pages)}")
    print(f"Validation errors: {len(errors)}")
    print(f"Validation warnings: {len(warnings)}")
    for finding in findings:
        print(f"{finding.severity.upper():7} {finding.code}: {finding.message}")

    if errors:
        print("\nBuild stopped because canonical source validation failed.")
        return 1

    records = normalise_pages(pages)
    expected = sum(len(page.items) for page in pages)
    if len(records) != expected:
        print(f"ERROR: normaliser produced {len(records)} records from {expected} indexed source items.")
        return 1

    report = make_build_report(pages, records, findings)
    output = render_site(ROOT, pages, records, config, report)

    # Machine-readable copy at repository root is intentionally NOT written.
    # _site is disposable generated output and remains ignored by git.
    print(f"\nGenerated records: {len(records)}")
    print(f"Static site: {output}")
    print(f"library.json: {output / 'library.json'}")
    print(f"latest.html: {output / 'latest.html'}")
    print(f"previous.html: {output / 'previous.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
