from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "assets" / "library.js"
BROWSE_SCRIPT = ROOT / "assets" / "browse.js"
TEMPLATE = ROOT / "templates" / "index.html.j2"
BROWSE_TEMPLATE = ROOT / "templates" / "browse.html.j2"


class MobileResultsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.browse_script = BROWSE_SCRIPT.read_text(encoding="utf-8")
        cls.template = TEMPLATE.read_text(encoding="utf-8")
        cls.browse_template = BROWSE_TEMPLATE.read_text(encoding="utf-8")

    def test_mobile_page_size_is_ten(self):
        self.assertIn("const MOBILE_PAGE_SIZE = 10;", self.script)
        self.assertIn("const PAGE_SIZE = 10;", self.browse_script)

    def test_page_one_slices_first_ten_results(self):
        self.assertIn("rows.slice(0, MOBILE_PAGE_SIZE)", self.script)

    def test_previous_and_next_controls_exist(self):
        self.assertIn("Previous 10", self.template)
        self.assertIn("Next 10", self.template)
        self.assertIn("data-mobile-prev", self.template)
        self.assertIn("data-mobile-next", self.template)

    def test_next_page_opens_standalone_browse_page(self):
        self.assertIn('navigateParent(`browse.html?${currentBrowseParams(2)}`);', self.script)

    def test_browse_page_reads_page_query_parameter(self):
        self.assertIn('params.get("page")', self.browse_script)
        self.assertIn("rows.slice(start, start + PAGE_SIZE)", self.browse_script)

    def test_browse_page_has_back_to_library_link(self):
        self.assertIn("Back to Resource Library", self.browse_template)
        self.assertIn("data-back-index", self.browse_template)

    def test_filters_are_carried_to_browse_page(self):
        for name in ["q", "category", "series", "level", "issue", "type", "quick"]:
            self.assertIn(name, self.script)
            self.assertIn(name, self.browse_script)

    def test_downloads_still_open_in_new_tab(self):
        self.assertIn('target="_blank" rel="noopener">Download File', self.script)
        self.assertIn('target="_blank" rel="noopener">Download File', self.browse_script)

    def test_issue_navigation_from_index_uses_parent_navigation(self):
        self.assertIn("navigateParent(button.dataset.openUrl);", self.script)

    def test_desktop_retains_full_results(self):
        self.assertIn("let displayedRows = rows;", self.script)
        self.assertIn("if (isMobile())", self.script)


if __name__ == "__main__":
    unittest.main()
