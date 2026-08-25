"""Render the static GitHub Pages site from normalised catalogue data."""

from __future__ import annotations

from collections import Counter
from datetime import date
import json
from pathlib import Path
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .models import CatalogueRecord, IssueRecord, NewsletterPage
from .normalise import SERIES_NAMES


CATEGORY_NAMES = {
    "club-news": "Club News",
    "education": "Education",
    "editing": "Editing",
    "photography-tips": "Photographer's Tips",
    "challenge": "Camera Challenges",
    "competition": "Competition",
    "events": "Events & Outings",
    "community": "Community",
    "members-on-the-move": "Members on the Move",
    "feature": "Features",
}


def _display_date(value: str) -> str:
    if not value:
        return ""
    d = date.fromisoformat(value)
    return f"{d.day} {d.strftime('%b %Y')}"


def issue_records(pages: list[NewsletterPage]) -> list[IssueRecord]:
    issues = [
        IssueRecord(
            issue=page.issue,
            published=page.published,
            public_url=page.public_url,
            source_file=page.source_path.name,
            record_count=len(page.items),
        )
        for page in pages
    ]
    return sorted(issues, key=lambda x: (x.published, x.issue), reverse=True)


def build_library_payload(pages: list[NewsletterPage], records: list[CatalogueRecord], config: dict) -> dict:
    issues = issue_records(pages)
    type_counts = Counter(record.item_type for record in records)
    category_counts = Counter(record.category for record in records)
    series_counts = Counter(record.series for record in records if record.series and record.item_type == "article")
    learning_categories = {"education", "editing", "photography-tips", "challenge"}
    return {
        "schema_version": 1,
        "site": {
            "title": config["site"]["title"],
            "recent_editions_limit": config["site"]["recent_editions_limit"],
        },
        "summary": {
            "issues": len(issues),
            "records": len(records),
            "learning_resources": sum(1 for r in records if r.category in learning_categories),
            "tips": type_counts.get("tip", 0),
            "types": dict(sorted(type_counts.items())),
            "categories": dict(sorted(category_counts.items())),
        },
        "labels": {
            "categories": CATEGORY_NAMES,
            "series": SERIES_NAMES,
        },
        "issues": [item.to_dict() for item in issues],
        "series": [
            {"id": series_id, "name": SERIES_NAMES.get(series_id, series_id), "article_count": series_counts[series_id]}
            for series_id in sorted(series_counts, key=lambda s: SERIES_NAMES.get(s, s))
        ],
        "records": [record.to_dict() for record in sorted(records, key=lambda r: (r.published, r.issue, r.title), reverse=True)],
    }


def _write_redirect(path: Path, target_url: str, label: str, template) -> None:
    path.write_text(template.render(target_url=target_url, label=label), encoding="utf-8")


def render_site(root: Path, pages: list[NewsletterPage], records: list[CatalogueRecord], config: dict, report: dict) -> Path:
    output = root / config["site"]["generated_output_dir"]
    if output.exists():
        shutil.rmtree(output)
    (output / "assets").mkdir(parents=True)

    payload = build_library_payload(pages, records, config)
    (output / "library.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "build-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    env = Environment(
        loader=FileSystemLoader(root / "templates"),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    index_template = env.get_template("index.html.j2")
    redirect_template = env.get_template("redirect.html.j2")
    report_template = env.get_template("build-report.html.j2")

    issues = issue_records(pages)
    recent = issues[: int(config["site"]["recent_editions_limit"])]
    coverage = f"Issues {issues[-1].issue}–{issues[0].issue}" if issues else "No issues"
    (output / "index.html").write_text(
        index_template.render(
            site_title=config["site"]["title"],
            coverage=coverage,
            recent_issues=recent,
            display_date=_display_date,
        ),
        encoding="utf-8",
    )

    (output / "build-report.html").write_text(report_template.render(report=report), encoding="utf-8")

    if issues:
        _write_redirect(output / "latest.html", issues[0].public_url, f"Latest Issue {issues[0].issue}", redirect_template)
    if len(issues) > 1:
        _write_redirect(output / "previous.html", issues[1].public_url, f"Previous Issue {issues[1].issue}", redirect_template)

    shutil.copy2(root / "assets" / "library.css", output / "assets" / "library.css")
    shutil.copy2(root / "assets" / "library.js", output / "assets" / "library.js")
    return output
