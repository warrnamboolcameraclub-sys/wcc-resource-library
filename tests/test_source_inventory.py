from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wcc_library.parser import discover_newsletters, parse_newsletter


class SourceInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = discover_newsletters(ROOT)
        cls.pages = [parse_newsletter(path) for path in cls.paths]

    def test_expected_12_migration_newsletters_present(self):
        self.assertEqual(len(self.pages), 12)
        self.assertEqual([page.issue for page in self.pages], [f"{n:03d}" for n in range(1, 13)])

    def test_expected_172_indexed_records_present(self):
        self.assertEqual(sum(len(page.items) for page in self.pages), 172)

    def test_embedded_urls_match_legacy_migration_map(self):
        legacy = json.loads((ROOT / "baseline" / "public-url-map.json").read_text(encoding="utf-8"))
        for page in self.pages:
            key_candidates = [page.issue, f"issue-{page.issue}", f"weekly-newsletter-{page.issue}"]
            expected = None
            if isinstance(legacy, dict):
                for key in key_candidates:
                    if key in legacy:
                        expected = legacy[key]
                        break
                if expected is None:
                    # Starter map uses filenames as keys.
                    expected = legacy.get(page.source_path.name)
            self.assertIsNotNone(expected, f"No legacy URL-map entry found for issue {page.issue}")
            if isinstance(expected, dict):
                expected = expected.get("url") or expected.get("data-url")
            self.assertEqual(page.public_url, expected)


if __name__ == "__main__":
    unittest.main()
