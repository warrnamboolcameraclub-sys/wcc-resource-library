#!/usr/bin/env python3
"""Validate canonical WCC newsletter HTML without generating or deploying the site."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wcc_library.parser import ParseError, discover_newsletters, parse_newsletter
from wcc_library.validator import load_config, validate_pages


def main() -> int:
    config = load_config(ROOT)
    paths = discover_newsletters(ROOT)
    pages = []

    for path in paths:
        try:
            pages.append(parse_newsletter(path))
        except ParseError as exc:
            print(f"ERROR parse_error [{path.name}] {exc}")
            return 1

    findings = validate_pages(pages, config)
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    type_counts = Counter(item.item_type for page in pages for item in page.items)

    print("WCC Resource Library source validation")
    print(f"Newsletter files : {len(pages)}")
    print(f"Indexed records  : {sum(len(page.items) for page in pages)}")
    for item_type in sorted(type_counts):
        print(f"  {item_type:<10}: {type_counts[item_type]}")
    print(f"Errors           : {len(errors)}")
    print(f"Warnings         : {len(warnings)}")

    if warnings:
        print("\nWarnings:")
        for finding in warnings:
            source = f" [{finding.source}]" if finding.source else ""
            print(f"- {finding.code}{source}: {finding.message}")

    if errors:
        print("\nErrors:")
        for finding in errors:
            source = f" [{finding.source}]" if finding.source else ""
            print(f"- {finding.code}{source}: {finding.message}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
