from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wcc_library.normalise import normalise_pages
from wcc_library.parser import discover_newsletters, parse_newsletter
from wcc_library.renderer import build_library_payload, issue_records
from wcc_library.validator import load_config


class GenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config(ROOT)
        cls.pages = [parse_newsletter(path) for path in discover_newsletters(ROOT)]
        cls.records = normalise_pages(cls.pages)
        cls.payload = build_library_payload(cls.pages, cls.records, cls.config)

    def test_every_indexed_source_item_becomes_one_record(self):
        self.assertEqual(len(self.records), 172)
        self.assertEqual(len({record.record_id for record in self.records}), 172)

    def test_all_generated_open_anchors_exist_in_source_document(self):
        ids_by_file = {page.source_path.name: set(page.all_html_ids) for page in self.pages}
        for record in self.records:
            self.assertIn(record.open_anchor_id, ids_by_file[record.source_file], record.record_id)

    def test_resources_keep_direct_download_urls(self):
        resources = [record for record in self.records if record.item_type == "resource"]
        self.assertEqual(len(resources), 8)
        self.assertTrue(all(record.download_url for record in resources))

    def test_people_and_locations_are_first_class_search_fields(self):
        self.assertEqual(sum(bool(record.people) for record in self.records), 58)
        self.assertEqual(sum(bool(record.locations) for record in self.records), 36)

    def test_latest_and_previous_are_012_and_011(self):
        issues = issue_records(self.pages)
        self.assertEqual(issues[0].issue, "012")
        self.assertEqual(issues[1].issue, "011")

    def test_latest_12_dropdown_source_is_automatic(self):
        issues = issue_records(self.pages)
        self.assertEqual(len(issues[: self.config["site"]["recent_editions_limit"]]), 12)

    def test_generated_identity_reconciles_to_legacy_172_record_baseline(self):
        text = (ROOT / "baseline" / "current-resource-library-index.html").read_text(encoding="utf-8")
        match = re.search(r"const I=(\[.*?\]);\s*const C=", text, flags=re.S)
        self.assertIsNotNone(match)
        baseline = json.loads(match.group(1))
        baseline_keys = {(row["n"], row["i"]) for row in baseline}
        generated_keys = {(record.issue, record.anchor_id) for record in self.records}
        self.assertEqual(generated_keys, baseline_keys)

    def test_payload_has_expected_summary(self):
        self.assertEqual(self.payload["summary"]["records"], 172)
        self.assertEqual(self.payload["summary"]["learning_resources"], 68)
        self.assertEqual(self.payload["summary"]["tips"], 21)
        self.assertEqual(self.payload["summary"]["issues"], 12)


if __name__ == "__main__":
    unittest.main()
