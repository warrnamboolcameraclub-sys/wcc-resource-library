from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "assets" / "library.js"


class IframeNavigationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")

    def test_issue_links_use_parent_navigation_same_tab(self):
        self.assertIn(
            'data-open-url="${escapeHtml(record.open_url)}"',
            self.script
        )

        self.assertIn(
            'navigateParent(button.dataset.openUrl);',
            self.script
        )

        self.assertNotIn(
            'target="_blank">Open in Issue',
            self.script
        )

    def test_download_links_still_open_in_new_tab(self):
        self.assertIn(
            'target="_blank" rel="noopener">Download File',
            self.script
        )

    def test_edition_navigation_reuses_parent_frame(self):
        self.assertIn(
            'navigateParent($("editionSelect").value);',
            self.script
        )

    def test_parent_navigation_function_exists(self):
        self.assertIn(
            'function navigateParent(url)',
            self.script
        )

        self.assertIn(
            'window.parent.location.href = url;',
            self.script
        )


if __name__ == "__main__":
    unittest.main()
