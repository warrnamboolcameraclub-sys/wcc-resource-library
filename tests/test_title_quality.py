from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wcc_library.normalise import normalise_pages
from wcc_library.parser import discover_newsletters, parse_newsletter


class TitleQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pages = [parse_newsletter(path) for path in discover_newsletters(ROOT)]
        cls.records = {record.record_id: record for record in normalise_pages(pages)}

    def test_modern_tip_titles_use_instructional_title(self):
        self.assertEqual(self.records["weekly-update:012:wcc-tip-b008"].title, "Understand What ISO Does")

    def test_series_download_title_is_derived_from_metadata(self):
        self.assertEqual(self.records["weekly-update:012:wcc-resource-2026-012-lightroom-005-guide"].title, "Lightroom Basics Part 5 – Downloadable Guide")

    def test_hidden_event_uses_visible_parent_for_deep_link(self):
        record = self.records["weekly-update:007:wcc-event-2026-08-06-craig-richards-presentation"]
        self.assertEqual(record.open_anchor_id, "wcc-2026-007-craig-richards-preview")

    def test_agm_acronym_is_humanised(self):
        record = self.records["weekly-update:008:wcc-event-2026-08-06-agm"]
        self.assertEqual(record.title, "Annual General Meeting")


if __name__ == "__main__":
    unittest.main()
