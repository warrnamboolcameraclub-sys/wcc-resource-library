from pathlib import Path
import re
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
        self.assertRegex(
            self.script,
            r"const\s+MOBILE_PAGE_SIZE\s*=\s*10\s*;"
        )

    def test_mobile_paging_state_exists(self):
        self.assertIn("mobilePage: 0", self.script)

    def test_mobile_results_are_sliced_by_page(self):
        self.assertRegex(
            self.script,
            r"rows\.slice\s*\(\s*start\s*,\s*start\s*\+\s*MOBILE_PAGE_SIZE\s*\)"
        )

    def test_previous_and_next_controls_exist(self):
        # The visible button labels belong in the HTML template.
        self.assertIn("Previous 10", self.template)
        self.assertIn("Next 10", self.template)
        self.assertIn("data-mobile-prev", self.template)
        self.assertIn("data-mobile-next", self.template)

        # JavaScript wires those template controls to the paging behaviour.
        self.assertIn('querySelectorAll("[data-mobile-prev]")', self.script)
        self.assertIn('querySelectorAll("[data-mobile-next]")', self.script)

    def test_filters_reset_mobile_page(self):
        self.assertRegex(
            self.script,
            r"state\.mobilePage\s*=\s*0\s*;"
        )
        self.assertIn("applyFilters", self.script)

    def test_paging_does_not_append_results(self):
        self.assertRegex(
            self.script,
            r'\$\("cards"\)\.innerHTML\s*='
        )

    def test_next_and_previous_scroll_back_to_results(self):
        self.assertIn("function scrollToResults()", self.script)
        self.assertGreaterEqual(
            self.script.count("scrollToResults();"),
            2
        )
        self.assertIn('behavior: "smooth"', self.script)

    def test_issue_navigation_still_uses_working_parent_function(self):
        self.assertRegex(
            self.script,
            r"navigateParent\s*\(\s*button\.dataset\.openUrl\s*\)\s*;"
        )

    def test_downloads_still_open_in_new_tab(self):
        self.assertRegex(
            self.script,
            r'target="_blank"\s+rel="noopener">Download File'
        )

    def test_desktop_retains_full_results(self):
        self.assertIn("if (isMobile())", self.script)
        self.assertIn("let displayedRows = rows", self.script)

    def test_mobile_pager_ids_exist_in_template(self):
        self.assertIn('id="mobilePagerTop"', self.template)
        self.assertIn('id="mobilePagerBottom"', self.template)


if __name__ == "__main__":
    unittest.main()
