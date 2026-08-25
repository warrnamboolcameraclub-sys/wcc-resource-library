"""Core source models used by the WCC Resource Library parser and validator."""

from __future__ import annotations

from dataclasses import dataclass, field
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
