from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class IframeNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = (ROOT / "assets" / "library.js").read_text(encoding="utf-8")

    def test_issue_links_escape_zenfolio_iframe(self):
        self.assertIn('class="action open-link"', self.script)
        self.assertIn('target="_top">Open in Issue', self.script)

    def test_download_links_still_open_in_new_tab(self):
        self.assertIn('class="action download-link"', self.script)
        self.assertIn('target="_blank" rel="noopener">Download File', self.script)

    def test_edition_dropdown_escapes_zenfolio_iframe(self):
        self.assertIn('function navigateTop(url)', self.script)
        self.assertIn('link.target = "_top";', self.script)
        self.assertIn('navigateTop($("editionSelect").value)', self.script)
        self.assertNotIn('location.href = $("editionSelect").value', self.script)


if __name__ == "__main__":
    unittest.main()
