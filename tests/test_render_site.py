from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import tempfile
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wcc_library.normalise import normalise_pages
from wcc_library.parser import discover_newsletters, parse_newsletter
from wcc_library.renderer import issue_records, render_site
from wcc_library.report import make_build_report
from wcc_library.validator import load_config, validate_pages


class RenderSiteTests(unittest.TestCase):
    def test_complete_static_site_is_generated_from_current_sources(self):
        config = load_config(ROOT)
        pages = [parse_newsletter(path) for path in discover_newsletters(ROOT)]
        records = normalise_pages(pages)
        findings = validate_pages(pages, config)
        report = make_build_report(pages, records, findings)

        # Render into an isolated temporary directory so the test can never
        # remove or overwrite the production _site/ build output.
        with tempfile.TemporaryDirectory(dir=ROOT, prefix="_test_site_") as tmpdir:
            test_config = deepcopy(config)
            test_config["site"]["generated_output_dir"] = Path(tmpdir).name
            output = render_site(ROOT, pages, records, test_config, report)

            for relative in [
                "index.html",
                "library.json",
                "latest.html",
                "previous.html",
                "build-report.json",
                "build-report.html",
                "assets/library.css",
                "assets/library.js",
            ]:
                self.assertTrue((output / relative).exists(), relative)

            issues = issue_records(pages)
            self.assertGreaterEqual(len(issues), 2)

            latest = (output / "latest.html").read_text(encoding="utf-8")
            previous = (output / "previous.html").read_text(encoding="utf-8")
            self.assertIn(issues[0].public_url, latest)
            self.assertIn(issues[1].public_url, previous)

            index = (output / "index.html").read_text(encoding="utf-8")
            limit = int(config["site"]["recent_editions_limit"])
            recent = issues[:limit]
            for issue in recent:
                self.assertIn(f'value="{issue.public_url}"', index)
            self.assertEqual(index.count('<option value="http'), len(recent))


if __name__ == "__main__":
    unittest.main()
