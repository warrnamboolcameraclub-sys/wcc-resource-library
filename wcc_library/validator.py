"""First-pass structural and semantic validation for canonical newsletter sources."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path
import re
from urllib.parse import urlparse

from .models import NewsletterPage


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str
    source: str | None = None


def load_config(root: Path) -> dict:
    return json.loads((root / "config" / "library-config.json").read_text(encoding="utf-8"))


def _valid_iso_date(value: str) -> bool:
    try:
        return date.fromisoformat(value).isoformat() == value
    except (TypeError, ValueError):
        return False


def _is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_pages(pages: list[NewsletterPage], config: dict) -> list[Finding]:
    findings: list[Finding] = []
    rules = config["validation"]
    categories = set(rules["categories"])
    item_types = set(rules["item_types"])
    tip_levels = set(rules["tip_levels"])
    event_statuses = set(rules["event_statuses"])
    known_series = set(rules["series"])

    issues = Counter(page.issue for page in pages)
    for issue, count in issues.items():
        if issue and count > 1:
            findings.append(Finding("error", "duplicate_issue", f"Issue {issue} occurs in {count} source files."))

    global_anchor_sources: dict[str, set[str]] = defaultdict(set)
    tip_codes: dict[str, list[str]] = defaultdict(list)
    resource_urls: dict[str, list[str]] = defaultdict(list)
    record_ids: Counter[str] = Counter()

    for page in pages:
        src = page.source_path.name
        for field in rules["required_newsletter_page_fields"]:
            if not str(page.page_attrs.get(field) or "").strip():
                findings.append(Finding("error", "missing_page_field", f"Missing required newsletter field {field}.", src))

        if not re.fullmatch(r"\d{3}", page.issue):
            findings.append(Finding("error", "invalid_issue", f"Issue must be exactly three digits; found {page.issue!r}.", src))

        if page.published and not _valid_iso_date(page.published):
            findings.append(Finding("error", "invalid_published_date", f"Invalid ISO publication date {page.published!r}.", src))

        if page.public_url and not _is_http_url(page.public_url):
            findings.append(Finding("error", "invalid_public_url", f"Invalid public URL {page.public_url!r}.", src))

        id_counts = Counter(page.all_html_ids)
        for anchor_id, count in id_counts.items():
            if count > 1:
                findings.append(Finding("error", "duplicate_html_id", f"HTML id {anchor_id!r} occurs {count} times in one document.", src))

        for item in page.items:
            for field in rules["required_index_item_fields"]:
                if field == "id":
                    value = item.anchor_id
                elif field == "data-index":
                    value = item.item_type
                elif field == "data-category":
                    value = item.category
                else:
                    value = str(item.attrs.get(field) or "").strip()
                if not value:
                    findings.append(Finding("error", "missing_item_field", f"Indexed item missing required field {field}.", src))

            if item.item_type and item.item_type not in item_types:
                findings.append(Finding("error", "invalid_item_type", f"Invalid data-index value {item.item_type!r} on {item.anchor_id or '<missing-id>'}.", src))

            if item.category and item.category not in categories:
                findings.append(Finding("error", "invalid_category", f"Invalid category {item.category!r} on {item.anchor_id or '<missing-id>'}.", src))

            if item.anchor_id:
                global_anchor_sources[item.anchor_id].add(src)
                record_ids[item.record_id] += 1

            series = str(item.attrs.get("data-series") or "").strip()
            if series and series not in known_series:
                findings.append(Finding("warning", "unknown_series", f"Unknown series {series!r} on {item.anchor_id}.", src))

            tags = [x.strip() for x in str(item.attrs.get("data-tags") or "").split(",") if x.strip()]
            if tags and not 3 <= len(tags) <= 7:
                findings.append(Finding("warning", "tag_count", f"{item.anchor_id} has {len(tags)} tags; standard guidance is approximately 3–7.", src))

            if item.item_type == "tip":
                code = str(item.attrs.get("data-code") or "").strip()
                level = str(item.attrs.get("data-level") or "").strip()
                if not code:
                    findings.append(Finding("error", "missing_tip_code", f"Tip {item.anchor_id} is missing data-code.", src))
                else:
                    tip_codes[code].append(src)
                if level not in tip_levels:
                    findings.append(Finding("error", "invalid_tip_level", f"Tip {item.anchor_id} has invalid data-level {level!r}.", src))
                prefix_map = {"B": "beginner", "I": "intermediate", "A": "advanced"}
                if code and re.fullmatch(r"[BIA]\d{3}", code):
                    expected = prefix_map[code[0]]
                    if level and level != expected:
                        findings.append(Finding("error", "tip_code_level_mismatch", f"Tip {code} must use level {expected!r}, not {level!r}.", src))
                elif code:
                    findings.append(Finding("error", "invalid_tip_code", f"Invalid tip code {code!r}; expected Bxxx, Ixxx or Axxx.", src))

            if item.item_type == "event":
                event_date = str(item.attrs.get("data-event-date") or "").strip()
                if event_date and not _valid_iso_date(event_date):
                    findings.append(Finding("error", "invalid_event_date", f"Event {item.anchor_id} has invalid ISO date {event_date!r}.", src))
                status = str(item.attrs.get("data-event-status") or "").strip()
                if status and status not in event_statuses:
                    findings.append(Finding("error", "invalid_event_status", f"Event {item.anchor_id} has invalid status {status!r}.", src))

            if item.item_type == "resource":
                if not item.href or not _is_http_url(item.href):
                    findings.append(Finding("error", "invalid_resource_href", f"Resource {item.anchor_id} is missing a usable HTTP(S) href.", src))
                else:
                    resource_urls[item.href].append(f"{src}#{item.anchor_id}")

    for code, sources in sorted(tip_codes.items()):
        if len(sources) > 1:
            findings.append(Finding("error", "duplicate_tip_code", f"Tip code {code} occurs {len(sources)} times: {', '.join(sources)}."))

    for record_id, count in record_ids.items():
        if count > 1:
            findings.append(Finding("error", "duplicate_record_id", f"Generated record ID {record_id} occurs {count} times."))

    for anchor_id, sources in sorted(global_anchor_sources.items()):
        if len(sources) > 1:
            findings.append(Finding("warning", "repeated_anchor_across_issues", f"Anchor {anchor_id!r} recurs across {len(sources)} newsletter documents: {', '.join(sorted(sources))}."))

    for url, occurrences in sorted(resource_urls.items()):
        if len(occurrences) > 1:
            findings.append(Finding("warning", "duplicate_resource_url", f"Resource URL occurs {len(occurrences)} times: {url} ({', '.join(occurrences)})."))

    return findings
