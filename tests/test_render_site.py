from __future__ import annotations

from pathlib import Path
import shutil
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wcc_library.normalise import normalise_pages
from wcc_library.parser import discover_newsletters, parse_newsletter
from wcc_library.renderer import render_site
from wcc_library.report import make_build_report
from wcc_library.validator import load_config, validate_pages


class RenderSiteTests(unittest.TestCase):
    def test_complete_static_site_is_generated(self):
        config = load_config(ROOT)
        pages = [parse_newsletter(path) for path in discover_newsletters(ROOT)]
        records = normalise_pages(pages)
        findings = validate_pages(pages, config)
        report = make_build_report(pages, records, findings)
        output = render_site(ROOT, pages, records, config, report)
        try:
            for relative in ["index.html", "library.json", "latest.html", "previous.html", "build-report.json", "build-report.html", "assets/library.css", "assets/library.js"]:
                self.assertTrue((output / relative).exists(), relative)
            latest = (output / "latest.html").read_text(encoding="utf-8")
            previous = (output / "previous.html").read_text(encoding="utf-8")
            self.assertIn("weekly-newsletter-012", latest)
            self.assertIn("weekly-newsletter-011", previous)
            index = (output / "index.html").read_text(encoding="utf-8")
            self.assertEqual(index.count("<option value=\"https://warrnamboolcameraclub.zenfolio.com/weekly-newsletter-"), 12)
        finally:
            if output.exists():
                shutil.rmtree(output)


if __name__ == "__main__":
    unittest.main()
