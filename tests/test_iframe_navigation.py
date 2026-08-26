from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "assets" / "library.js"


class IframeNavigationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")

    def test_issue_links_use_parent_navigation_same_tab(self):
        # Open in Issue must be a button carrying the issue URL.
        self.assertIn("data-open-url=", self.script)
        self.assertIn("record.open_url", self.script)

        # It must use the same parent-navigation function as the Go button.
        self.assertRegex(
            self.script,
            r"navigateParent\s*\(\s*button\.dataset\.openUrl\s*\)\s*;"
        )

        # Open in Issue must not deliberately open a new tab.
        self.assertNotRegex(
            self.script,
            r'target="_blank"[^>]*>\s*Open in Issue'
        )

    def test_download_links_still_open_in_new_tab(self):
        self.assertRegex(
            self.script,
            r'target="_blank"\s+rel="noopener">\s*Download File'
        )

    def test_edition_navigation_reuses_parent_frame(self):
        self.assertRegex(
            self.script,
            r'navigateParent\s*\(\s*\$\("editionSelect"\)\.value\s*\)\s*;'
        )

    def test_parent_navigation_function_exists(self):
        self.assertIn(
            "function navigateParent(url)",
            self.script
        )

        self.assertRegex(
            self.script,
            r"window\.parent\.location\.href\s*=\s*url\s*;"
        )

        self.assertRegex(
            self.script,
            r"window\.location\.href\s*=\s*url\s*;"
        )


if __name__ == "__main__":
    unittest.main()
