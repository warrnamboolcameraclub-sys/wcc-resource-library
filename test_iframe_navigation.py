from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class IframeNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = (ROOT / "assets" / "library.js").read_text(encoding="utf-8")

    def test_issue_links_use_parent_frame_same_tab(self):
        self.assertIn('class="action open-link"', self.script)
        self.assertIn('target="_parent">Open in Issue', self.script)
        self.assertNotIn('target="_blank">Open in Issue', self.script)
        self.assertNotIn('event.target.closest("a.open-link")', self.script)

    def test_download_links_still_open_in_new_tab(self):
        self.assertIn('class="action download-link"', self.script)
        self.assertIn('target="_blank" rel="noopener">Download File', self.script)

    def test_edition_navigation_reuses_parent_frame(self):
        self.assertIn('function navigateParent(url)', self.script)
        self.assertIn('window.parent.location.href = url;', self.script)
        self.assertIn('window.location.href = url;', self.script)
        self.assertIn('navigateParent($("editionSelect").value)', self.script)
        self.assertNotIn('window.top.location.assign(url);', self.script)


if __name__ == "__main__":
    unittest.main()
