from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "assets" / "library.js"
TEMPLATE = ROOT / "templates" / "index.html.j2"

class MobileResultsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.template = TEMPLATE.read_text(encoding="utf-8")

    def test_mobile_page_size_is_ten(self):
        self.assertIn("const MOBILE_PAGE_SIZE = 10;", self.script)

    def test_mobile_pager_exists_above_and_below_results(self):
        self.assertEqual(self.template.count("data-mobile-next"), 2)
        self.assertEqual(self.template.count("data-mobile-prev"), 2)

    def test_next_page_replaces_results_instead_of_appending(self):
        self.assertIn("state.mobilePage += 1;", self.script)
        self.assertIn("rows.slice(start, end)", self.script)
        self.assertNotIn("state.mobileVisible += MOBILE_PAGE_SIZE", self.script)

    def test_previous_page_is_supported(self):
        self.assertIn("state.mobilePage -= 1;", self.script)

    def test_filters_reset_mobile_page(self):
        self.assertIn("if (resetMobile) state.mobilePage = 0;", self.script)


    def test_mobile_stats_are_compact(self):
        css = (ROOT / "assets" / "library.css").read_text(encoding="utf-8")
        self.assertIn("min-height:74px", css)
        self.assertIn(".stat strong{font-size:22px", css)
        self.assertIn(".stat span{margin-top:4px;font-size:10px", css)

    def test_issue_navigation_still_uses_working_parent_function(self):
        self.assertIn("navigateParent(button.dataset.openUrl);", self.script)

    def test_downloads_still_open_new_tab(self):
        self.assertIn('target="_blank" rel="noopener">Download File', self.script)

if __name__ == "__main__":
    unittest.main()
