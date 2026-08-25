"""HTML source discovery and raw metadata parsing."""

from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup

from .models import IndexedItem, NewsletterPage


class ParseError(ValueError):
    """Raised when a source document cannot be parsed deterministically."""


def discover_newsletters(root: Path) -> list[Path]:
    return sorted((root / "content" / "newsletters").glob("*.html"))


def parse_newsletter(path: Path) -> NewsletterPage:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    wrappers = soup.find_all(attrs={"data-publication": "weekly-update"})
    if len(wrappers) != 1:
        raise ParseError(
            f"{path.name}: expected exactly one data-publication='weekly-update' wrapper; found {len(wrappers)}"
        )

    wrapper = wrappers[0]
    issue = str(wrapper.get("data-issue") or "").strip()

    items: list[IndexedItem] = []
    for element in soup.find_all(attrs={"data-index": True}):
        attrs = {str(k): v for k, v in element.attrs.items()}
        items.append(
            IndexedItem(
                source_path=path,
                issue=issue,
                anchor_id=str(element.get("id") or "").strip(),
                item_type=str(element.get("data-index") or "").strip(),
                category=str(element.get("data-category") or "").strip(),
                attrs=attrs,
                href=str(element.get("href")).strip() if element.get("href") else None,
                text=element.get_text(" ", strip=True),
            )
        )

    all_html_ids = tuple(
        str(element.get("id"))
        for element in soup.find_all(id=True)
        if element.get("id") is not None
    )

    return NewsletterPage(
        source_path=path,
        publication=str(wrapper.get("data-publication") or "").strip(),
        issue=issue,
        published=str(wrapper.get("data-published") or "").strip(),
        public_url=str(wrapper.get("data-url") or "").strip(),
        page_attrs={str(k): v for k, v in wrapper.attrs.items()},
        all_html_ids=all_html_ids,
        items=tuple(items),
    )
