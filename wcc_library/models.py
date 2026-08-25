"""Core models for the WCC Resource Library build pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class IndexedItem:
    """Raw indexed element extracted from a canonical source document."""

    source_path: Path
    issue: str
    anchor_id: str
    item_type: str
    category: str
    attrs: dict[str, Any] = field(default_factory=dict)
    href: str | None = None
    text: str = ""

    @property
    def record_id(self) -> str:
        return f"weekly-update:{self.issue}:{self.anchor_id}"


@dataclass(frozen=True)
class NewsletterPage:
    """Raw newsletter-level metadata plus indexed items."""

    source_path: Path
    publication: str
    issue: str
    published: str
    public_url: str
    page_attrs: dict[str, Any]
    all_html_ids: tuple[str, ...]
    items: tuple[IndexedItem, ...]


@dataclass(frozen=True)
class CatalogueRecord:
    """Normalised, serialisable Resource Library record."""

    record_id: str
    source_type: str
    source_file: str
    issue: str
    published: str
    anchor_id: str
    open_anchor_id: str
    item_type: str
    category: str
    title: str
    excerpt: str
    tags: tuple[str, ...] = ()
    people: tuple[str, ...] = ()
    locations: tuple[str, ...] = ()
    series: str | None = None
    part: str | None = None
    code: str | None = None
    level: str | None = None
    event_date: str | None = None
    event_status: str | None = None
    source_url: str = ""
    open_url: str = ""
    download_url: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["tags"] = list(self.tags)
        data["people"] = list(self.people)
        data["locations"] = list(self.locations)
        return data


@dataclass(frozen=True)
class IssueRecord:
    issue: str
    published: str
    public_url: str
    source_file: str
    record_count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
