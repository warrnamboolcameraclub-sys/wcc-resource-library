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

    def test_show_more_button_exists(self):
        self.assertIn('id="showMoreBtn"', self.template)

    def test_show_more_adds_ten(self):
        self.assertIn("state.mobileVisible += MOBILE_PAGE_SIZE;", self.script)

    def test_filters_reset_mobile_limit(self):
        self.assertIn("if (resetMobile) state.mobileVisible = MOBILE_PAGE_SIZE;", self.script)

    def test_issue_navigation_still_uses_working_parent_function(self):
        self.assertIn("navigateParent(button.dataset.openUrl);", self.script)

    def test_downloads_still_open_new_tab(self):
        self.assertIn('target="_blank" rel="noopener">Download File', self.script)

if __name__ == "__main__":
    unittest.main()
