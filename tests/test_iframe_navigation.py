from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class IframeNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = (ROOT / "assets" / "library.js").read_text(encoding="utf-8")

    def test_issue_links_use_same_top_level_tab(self):
        self.assertIn('class="action open-link"', self.script)
        self.assertNotIn('class="action open-link" href="${escapeHtml(record.open_url)}" target="_blank"', self.script)
        self.assertNotIn('target="_top">Open in Issue', self.script)
        self.assertIn('event.target.closest("a.open-link")', self.script)
        self.assertIn('event.preventDefault();', self.script)
        self.assertIn('navigateTop(link.href);', self.script)

    def test_download_links_still_open_in_new_tab(self):
        self.assertIn('class="action download-link"', self.script)
        self.assertIn('target="_blank" rel="noopener">Download File', self.script)

    def test_top_navigation_reuses_current_browser_tab(self):
        self.assertIn('function navigateTop(url)', self.script)
        self.assertIn('window.top.location.assign(url);', self.script)
        self.assertNotIn('link.target = "_top";', self.script)
        self.assertIn('navigateTop($("editionSelect").value)', self.script)
        self.assertNotIn('location.href = $("editionSelect").value', self.script)


if __name__ == "__main__":
    unittest.main()
