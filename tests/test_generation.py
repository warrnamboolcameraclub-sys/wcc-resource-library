from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wcc_library.normalise import normalise_pages
from wcc_library.parser import discover_newsletters, parse_newsletter
from wcc_library.renderer import build_library_payload, issue_records
from wcc_library.validator import load_config

MIGRATION_ISSUES = {f"{n:03d}" for n in range(1, 13)}
LEARNING_CATEGORIES = {"education", "editing", "photography-tips", "challenge"}


def _split_csv(value: object) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for part in str(value or "").split(","):
        item = " ".join(part.split()).strip()
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return tuple(result)


class GenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config(ROOT)
        cls.pages = [parse_newsletter(path) for path in discover_newsletters(ROOT)]
        cls.records = normalise_pages(cls.pages)
        cls.payload = build_library_payload(cls.pages, cls.records, cls.config)

    def test_every_indexed_source_item_becomes_one_record(self):
        expected = sum(len(page.items) for page in self.pages)
        self.assertEqual(len(self.records), expected)
        self.assertEqual(len({record.record_id for record in self.records}), expected)

    def test_all_generated_open_anchors_exist_in_source_document(self):
        ids_by_file = {page.source_path.name: set(page.all_html_ids) for page in self.pages}
        for record in self.records:
            self.assertIn(record.open_anchor_id, ids_by_file[record.source_file], record.record_id)

    def test_resources_keep_direct_download_urls(self):
        expected = sum(1 for page in self.pages for item in page.items if item.item_type == "resource")
        resources = [record for record in self.records if record.item_type == "resource"]
        self.assertEqual(len(resources), expected)
        self.assertTrue(all(record.download_url for record in resources))

    def test_people_and_locations_are_first_class_search_fields(self):
        records_by_id = {record.record_id: record for record in self.records}
        for page in self.pages:
            for item in page.items:
                record = records_by_id[item.record_id]
                self.assertEqual(record.people, _split_csv(item.attrs.get("data-people")), item.record_id)
                self.assertEqual(record.locations, _split_csv(item.attrs.get("data-locations")), item.record_id)

    def test_latest_and_previous_follow_source_publication_order(self):
        issues = issue_records(self.pages)
        expected_pages = sorted(self.pages, key=lambda page: (page.published, page.issue), reverse=True)
        self.assertGreaterEqual(len(issues), 2)
        self.assertEqual(issues[0].issue, expected_pages[0].issue)
        self.assertEqual(issues[0].public_url, expected_pages[0].public_url)
        self.assertEqual(issues[1].issue, expected_pages[1].issue)
        self.assertEqual(issues[1].public_url, expected_pages[1].public_url)

    def test_latest_12_dropdown_source_is_automatic(self):
        issues = issue_records(self.pages)
        limit = int(self.config["site"]["recent_editions_limit"])
        self.assertEqual(len(issues[:limit]), min(len(issues), limit))

    def test_migration_001_012_identity_remains_equal_to_frozen_172_record_baseline(self):
        text = (ROOT / "baseline" / "current-resource-library-index.html").read_text(encoding="utf-8")
        match = re.search(r"const I=(\[.*?\]);\s*const C=", text, flags=re.S)
        self.assertIsNotNone(match)
        baseline = json.loads(match.group(1))
        baseline_keys = {(row["n"], row["i"]) for row in baseline}
        generated_keys = {
            (record.issue, record.anchor_id)
            for record in self.records
            if record.issue in MIGRATION_ISSUES
        }
        self.assertEqual(len(baseline_keys), 172)
        self.assertEqual(generated_keys, baseline_keys)

    def test_payload_summary_is_derived_from_current_sources(self):
        self.assertEqual(self.payload["summary"]["records"], len(self.records))
        self.assertEqual(
            self.payload["summary"]["learning_resources"],
            sum(1 for record in self.records if record.category in LEARNING_CATEGORIES),
        )
        self.assertEqual(
            self.payload["summary"]["tips"],
            sum(1 for record in self.records if record.item_type == "tip"),
        )
        self.assertEqual(self.payload["summary"]["issues"], len(self.pages))


if __name__ == "__main__":
    unittest.main()
