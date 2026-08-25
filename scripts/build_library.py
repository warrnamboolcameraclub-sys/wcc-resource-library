#!/usr/bin/env python3
"""Production build entry point - intentionally gated during repository setup.

Phase 1 validates the canonical source set only. The production normaliser,
renderer, library.json generation and GitHub Pages output are implemented next,
after reconciliation against the 172-record baseline.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_sources import main as validate_main


def main() -> int:
    result = validate_main()
    if result:
        return result
    print("\nSource validation passed.")
    print("Production _site generation is intentionally not enabled in this initial repository package.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
