from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from wcc_library.parser import discover_newsletters, parse_newsletter
from wcc_library.validator import load_config, validate_pages


class ValidationTests(unittest.TestCase):
    def test_canonical_issues_have_no_blocking_validation_errors(self):
        config = load_config(ROOT)
        pages = [parse_newsletter(path) for path in discover_newsletters(ROOT)]
        findings = validate_pages(pages, config)
        errors = [finding for finding in findings if finding.severity == "error"]
        self.assertEqual(errors, [], "\n" + "\n".join(f"{f.code}: {f.message}" for f in errors))


if __name__ == "__main__":
    unittest.main()
