"""Convert raw newsletter metadata into stable searchable catalogue records."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from bs4 import BeautifulSoup, Tag

from .models import CatalogueRecord, NewsletterPage


SERIES_NAMES = {
    "ethical-bird-photography": "Ethical Bird Photography",
    "mastering-long-exposure-photography": "Mastering Long Exposure Photography",
    "lightroom-basics": "Lightroom Basics",
    "using-your-camera": "Using Your Camera",
}

_GENERIC_HEADINGS = {
    "convention corner",
    "editing corner",
    "photographer's tips",
    "photographers tips",
    "members on the move",
    "workshop corner",
    "around the club",
    "feature article",
    "club news",
    "community connections",
    "coming up",
    "what's coming up",
}

_ACRONYMS = {"agm": "AGM", "vaps": "VAPS", "apja": "APJA", "pdf": "PDF", "edpi": "EDPI", "nd": "ND", "iso": "ISO"}


def _clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def _split_csv(value: object) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for part in str(value or "").split(","):
        item = _clean(part)
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return tuple(result)


def _without_fragment(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))


def _humanise_slug(slug: str) -> str:
    words = [word for word in slug.replace("_", "-").split("-") if word]
    out: list[str] = []
    for word in words:
        low = word.lower()
        out.append(_ACRONYMS.get(low, word.capitalize()))
    return " ".join(out)


def _slug_title_from_anchor(anchor_id: str) -> str:
    slug = anchor_id
    slug = re.sub(r"^wcc-(?:event|resource)-", "", slug)
    slug = re.sub(r"^wcc-", "", slug)
    slug = re.sub(r"^\d{4}-\d{3}-", "", slug)
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug)
    slug = re.sub(r"^\d{4}-\d{2}-", "", slug)
    slug = re.sub(r"^\d{4}-", "", slug)
    slug = re.sub(r"^tip-", "", slug)
    return _humanise_slug(slug)


def _owned_nodes(element: Tag, names: list[str]) -> list[Tag]:
    nodes: list[Tag] = []
    for node in element.find_all(names):
        owner = node.find_parent(attrs={"data-index": True})
        if owner is element:
            nodes.append(node)
    return nodes


def _headings(element: Tag) -> list[str]:
    return [_clean(h.get_text(" ", strip=True)) for h in _owned_nodes(element, ["h1", "h2", "h3", "h4", "h5", "h6"]) if _clean(h.get_text(" ", strip=True))]


def _strongs(element: Tag) -> list[str]:
    return [_clean(h.get_text(" ", strip=True)) for h in _owned_nodes(element, ["strong", "b"]) if _clean(h.get_text(" ", strip=True))]


def _looks_date_only(value: str) -> bool:
    plain = re.sub(r"^[^\w]+", "", value).strip()
    month = r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
    weekday = r"(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"
    patterns = [
        rf"^{weekday},?\s+\d{{1,2}}(?:st|nd|rd|th)?\s+{month}(?:\s+\d{{4}})?$",
        rf"^\d{{1,2}}(?:st|nd|rd|th)?(?:[–-]\d{{1,2}})?\s+{month}(?:\s+\d{{4}})?$",
        rf"^(?:Late\s+)?{month}(?:\s+\d{{4}})?$",
    ]
    return any(re.match(pattern, plain, flags=re.I) for pattern in patterns)


def _looks_time_only(value: str) -> bool:
    plain = re.sub(r"^[^\w]+", "", value).strip()
    return bool(re.fullmatch(r"\d{1,2}(?::\d{2})?\s*(?:am|pm)", plain, flags=re.I))


def _strip_event_prefix(value: str) -> str:
    value = _clean(value)
    patterns = [
        r"^[📋🛠️✂️⚫]\s*Club Notices\s*[–-]\s*",
        r"^[📋]\s*Annual General Meeting$",
    ]
    for pattern in patterns:
        m = re.match(pattern, value, flags=re.I)
        if m:
            if "Annual General Meeting" in value:
                return "Annual General Meeting"
            value = value[m.end():]
    return value


def _is_generic_heading(value: str) -> bool:
    plain = re.sub(r"^[^\w]+", "", value).strip().lower()
    plain = re.sub(r"\s*[–-].*$", "", plain).strip()
    return plain in _GENERIC_HEADINGS


def _derive_title(element: Tag, attrs: dict, item_type: str, anchor_id: str) -> str:
    explicit = _clean(str(attrs.get("data-title") or ""))
    if explicit:
        return explicit

    headings = _headings(element)
    strongs = _strongs(element)
    summary = element.find("summary")
    summary_text = _clean(summary.get_text(" ", strip=True)) if summary else ""

    if item_type == "resource":
        series = _clean(str(attrs.get("data-series") or ""))
        part = _clean(str(attrs.get("data-part") or ""))
        if series and part:
            return f"{SERIES_NAMES.get(series, _humanise_slug(series))} Part {part} – Downloadable Guide"
        link_text = _clean(element.get_text(" ", strip=True))
        link_text = re.sub(r"^download(?:\s+the)?\s+", "", link_text, flags=re.I)
        if link_text and "this week's guide" not in link_text.lower():
            href = _clean(str(element.get("href") or ""))
            is_pdf = href.lower().split("?")[0].endswith(".pdf")
            if is_pdf and "guide" in link_text.lower():
                return f"{_slug_title_from_anchor(anchor_id)} – PDF Guide"
            if is_pdf and "pdf" not in link_text.lower():
                return f"{link_text} – PDF"
            return link_text
        return _slug_title_from_anchor(anchor_id)

    if item_type == "tip":
        # The instructional title is more useful in search than the generic level heading.
        if len(headings) >= 2:
            return headings[1]
        if strongs:
            return strongs[0]
        if headings:
            stripped = re.sub(r"\s*[–(-]\s*[BIA]\d{3}\)?$", "", headings[0]).strip()
            return stripped or headings[0]
        return _slug_title_from_anchor(anchor_id)

    if item_type == "event":
        candidates = [h for h in headings if not _is_generic_heading(h) and not _looks_date_only(h)]
        if candidates:
            title = _strip_event_prefix(candidates[0])
            # If the first useful heading is a broad wrapper, a following heading is usually more specific.
            if re.search(r"workshop corner|looking ahead", title, flags=re.I) and len(candidates) > 1:
                title = candidates[1]
            return title
        for strong in strongs:
            if not _looks_date_only(strong) and not _looks_time_only(strong) and len(strong) > 2:
                return re.sub(r"^[^\w]+\s*", "", strong).strip()
        if summary_text:
            return summary_text
        fallback = _slug_title_from_anchor(anchor_id)
        if fallback == "AGM":
            return "Annual General Meeting"
        if "craig-richards" in anchor_id and "landscape-photography" in str(attrs.get("data-tags") or ""):
            fallback = fallback.replace("Craig Richards Presentation", "Craig Richards Landscape Photography Presentation")
            fallback = fallback.replace("Craig Richards Workshop", "Craig Richards Landscape Photography Workshop")
        if fallback == "Bojangles Dinner":
            return "Dinner at Bojangles"
        return fallback

    # Series articles often use a hierarchy of section label -> series name -> article title.
    series = _clean(str(attrs.get("data-series") or ""))
    part = _clean(str(attrs.get("data-part") or ""))
    if series and headings:
        series_name_display = SERIES_NAMES.get(series, "")
        series_name = series_name_display.lower()
        useful = [h for h in headings if not _is_generic_heading(h) and h.lower() != series_name and not h.lower().startswith("read ")]
        if part:
            marker_re = re.compile(rf"\b(?:part|article)\s*{re.escape(part)}\b", re.I)
            for index, heading in enumerate(useful):
                match = marker_re.search(heading)
                if not match:
                    continue
                tail = heading[match.end():].strip(" :–—-")
                # A heading such as "Part 5: Neutral Density Filters" is already specific.
                if tail:
                    return heading
                # A heading such as "Lightroom Basics – Part 5" is only a series marker;
                # the next owned heading is the actual article title.
                if index + 1 < len(useful):
                    return useful[index + 1]
                return heading
        if useful:
            # Unnumbered series introductions commonly use kicker -> series title -> article title.
            return useful[-1]

    if headings:
        useful = [h for h in headings if not _is_generic_heading(h)]
        if useful:
            return useful[0]
        return headings[0]

    if summary_text:
        return summary_text

    # Competition image cards and similar compact records have meaningful visible text but no heading.
    text = _clean(element.get_text(" ", strip=True))
    if text:
        return text[:180].strip()
    return _slug_title_from_anchor(anchor_id)


def _derive_excerpt(element: Tag, item_type: str, title: str, parent_for_hidden: Tag | None = None) -> str:
    if item_type == "resource":
        return "Downloadable resource from the Weekly Update."

    context = parent_for_hidden if parent_for_hidden is not None else element
    paragraphs = [_clean(p.get_text(" ", strip=True)) for p in _owned_nodes(context, ["p"]) if context.has_attr("data-index")] if context.has_attr("data-index") else [_clean(p.get_text(" ", strip=True)) for p in context.find_all("p")]
    paragraphs = [p for p in paragraphs if p and p != title]
    if paragraphs:
        text = paragraphs[0]
    else:
        text = _clean(context.get_text(" ", strip=True))
        if text.startswith(title):
            text = _clean(text[len(title):])
    if not text:
        return ""
    # Keep the card layout compact and deterministic.
    limit = 170
    if len(text) <= limit:
        return text
    cut = text[:limit].rstrip()
    cut = re.sub(r"\s+\S*$", "", cut).rstrip(" ,.;:-")
    return (cut or text[:limit].rstrip()) + "…"


def _is_hidden(element: Tag) -> bool:
    style = str(element.get("style") or "").replace(" ", "").lower()
    return "display:none" in style or element.has_attr("hidden")


def _resolve_open_anchor(element: Tag, attrs: dict, anchor_id: str, all_ids: set[str]) -> str:
    explicit = _clean(str(attrs.get("data-source-anchor") or ""))
    if explicit and explicit in all_ids:
        return explicit
    if _is_hidden(element):
        parent = element.find_parent(id=True)
        if parent and parent.get("id"):
            return _clean(str(parent.get("id")))
    return anchor_id


def normalise_page(page: NewsletterPage) -> list[CatalogueRecord]:
    """Normalise every indexed element in one newsletter page."""
    soup = BeautifulSoup(page.source_path.read_text(encoding="utf-8"), "html.parser")
    all_ids = set(page.all_html_ids)
    records: list[CatalogueRecord] = []

    for raw in page.items:
        element = soup.find(id=raw.anchor_id)
        if element is None:
            # Validator will flag impossible source state; keep build deterministic.
            continue
        attrs = raw.attrs
        title = _derive_title(element, attrs, raw.item_type, raw.anchor_id)
        open_anchor = _resolve_open_anchor(element, attrs, raw.anchor_id, all_ids)
        hidden_parent = element.find_parent(id=True) if _is_hidden(element) else None
        excerpt = _derive_excerpt(element, raw.item_type, title, hidden_parent)
        source_url = _without_fragment(page.public_url)
        open_url = f"{source_url}#{open_anchor}" if source_url and open_anchor else source_url

        records.append(
            CatalogueRecord(
                record_id=raw.record_id,
                source_type="weekly-update",
                source_file=page.source_path.name,
                issue=page.issue,
                published=page.published,
                anchor_id=raw.anchor_id,
                open_anchor_id=open_anchor,
                item_type=raw.item_type,
                category=raw.category,
                title=title,
                excerpt=excerpt,
                tags=_split_csv(attrs.get("data-tags")),
                people=_split_csv(attrs.get("data-people")),
                locations=_split_csv(attrs.get("data-locations")),
                series=_clean(str(attrs.get("data-series") or "")) or None,
                part=_clean(str(attrs.get("data-part") or "")) or None,
                code=_clean(str(attrs.get("data-code") or "")) or None,
                level=_clean(str(attrs.get("data-level") or "")) or None,
                event_date=_clean(str(attrs.get("data-event-date") or "")) or None,
                event_status=_clean(str(attrs.get("data-event-status") or "")) or None,
                source_url=source_url,
                open_url=open_url,
                download_url=_clean(raw.href) or None if raw.item_type == "resource" else None,
            )
        )

    return records


def normalise_pages(pages: list[NewsletterPage]) -> list[CatalogueRecord]:
    records: list[CatalogueRecord] = []
    for page in pages:
        records.extend(normalise_page(page))
    return records
