"""Build and validation reporting helpers."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Iterable

from .models import CatalogueRecord, NewsletterPage
from .validator import Finding


def make_build_report(pages: list[NewsletterPage], records: list[CatalogueRecord], findings: Iterable[Finding]) -> dict:
    findings = list(findings)
    type_counts = Counter(record.item_type for record in records)
    category_counts = Counter(record.category for record in records)
    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_files": len(pages),
        "records": len(records),
        "record_types": dict(sorted(type_counts.items())),
        "categories": dict(sorted(category_counts.items())),
        "errors": [f.__dict__ for f in findings if f.severity == "error"],
        "warnings": [f.__dict__ for f in findings if f.severity == "warning"],
    }
