from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wcc_library.parser import discover_newsletters, parse_newsletter

MIGRATION_ISSUES = tuple(f"{n:03d}" for n in range(1, 13))


class SourceInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = discover_newsletters(ROOT)
        cls.pages = [parse_newsletter(path) for path in cls.paths]
        cls.pages_by_issue = {page.issue: page for page in cls.pages}

    def test_frozen_migration_newsletters_001_012_remain_present(self):
        missing = [issue for issue in MIGRATION_ISSUES if issue not in self.pages_by_issue]
        self.assertEqual(missing, [])

    def test_frozen_migration_001_012_still_contains_172_indexed_records(self):
        count = sum(len(self.pages_by_issue[issue].items) for issue in MIGRATION_ISSUES)
        self.assertEqual(count, 172)

    def test_migration_embedded_urls_match_frozen_legacy_map(self):
        legacy = json.loads((ROOT / "baseline" / "public-url-map.json").read_text(encoding="utf-8"))
        for issue in MIGRATION_ISSUES:
            page = self.pages_by_issue[issue]
            key_candidates = [page.issue, f"issue-{page.issue}", f"weekly-newsletter-{page.issue}"]
            expected = None
            if isinstance(legacy, dict):
                for key in key_candidates:
                    if key in legacy:
                        expected = legacy[key]
                        break
                if expected is None:
                    # The migration map uses filenames as keys in the starter package.
                    expected = legacy.get(page.source_path.name)
            self.assertIsNotNone(expected, f"No frozen legacy URL-map entry found for issue {page.issue}")
            if isinstance(expected, dict):
                expected = expected.get("url") or expected.get("data-url")
            self.assertEqual(page.public_url, expected)

    def test_future_newsletters_do_not_require_legacy_url_map_entries(self):
        # The legacy URL map is intentionally a migration audit artefact only.
        # Its absence for Issue 013+ must never make a future newsletter fail.
        future_pages = [page for page in self.pages if page.issue not in MIGRATION_ISSUES]
        for page in future_pages:
            self.assertTrue(page.public_url.startswith(("http://", "https://")), page.issue)


if __name__ == "__main__":
    unittest.main()
