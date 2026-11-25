# Copyright 2026 TELUS Digital
# SPDX-License-Identifier: Apache-2.0
"""`tools/checks.py catalog-parity`: the catalog entry mirrors the manifest's Spec Kit floor.

`catalog.json` once said `>=0.11.0` while `spectra/extension.yml` said `>=0.11.2`, and no check noticed,
because catalog parity covered only the version and the command count. These cases pin the floor too.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))

import checks  # noqa: E402


def _catalog_with_floor(floor) -> dict:
    catalog = json.loads(checks.CATALOG.read_text(encoding="utf-8"))
    requires = catalog["extensions"]["spectra"].setdefault("requires", {})
    if floor is None:
        requires.pop("speckit_version", None)
    else:
        requires["speckit_version"] = floor
    return catalog


class SpeckitFloorParity(unittest.TestCase):
    def run_parity_against(self, catalog: dict) -> list:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "catalog.json"
            path.write_text(json.dumps(catalog), encoding="utf-8")
            with mock.patch.object(checks, "CATALOG", path):
                return checks.check_catalog_parity()

    def test_the_committed_catalog_and_manifest_agree(self):
        self.assertEqual(checks.check_catalog_parity(), [])

    def test_the_manifest_floor_is_read_from_the_requires_block(self):
        text = checks.MANIFEST.read_text(encoding="utf-8")
        catalog = json.loads(checks.CATALOG.read_text(encoding="utf-8"))
        self.assertEqual(checks.parse_manifest_speckit_version(text),
                         catalog["extensions"]["spectra"]["requires"]["speckit_version"])

    def test_a_deeper_speckit_version_line_is_not_the_floor(self):
        text = 'requires:\n  tools:\n    - name: x\n      speckit_version: ">=9.9.9"\n'
        self.assertIsNone(checks.parse_manifest_speckit_version(text))

    def test_a_different_catalog_floor_is_reported(self):
        problems = self.run_parity_against(_catalog_with_floor(">=0.11.0"))
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("Spec Kit", problems[0])
        self.assertIn(">=0.11.0", problems[0])

    def test_a_missing_catalog_floor_is_reported(self):
        problems = self.run_parity_against(_catalog_with_floor(None))
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("Spec Kit", problems[0])


if __name__ == "__main__":
    unittest.main()
