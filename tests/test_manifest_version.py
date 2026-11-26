"""Reading the extension version from `extension.yml` without a YAML parser.

`tools/checks.py catalog-parity` compares this value with `catalog.json`, so a scanner that misreads
the manifest would either pass a real mismatch or fail a correct catalog. The scan is the risky part of
holding the zero-dependency line, so it is tested against the real manifest shape and against every way
a manifest can fail to yield a version.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tests"))
sys.path.insert(0, str(REPO_ROOT / "tools"))

import helpers as h  # noqa: E402
from checks import parse_manifest_version  # noqa: E402


class VersionScan(unittest.TestCase):
    def test_reads_the_version_from_the_real_committed_manifest(self):
        """If Spec Kit ever changes the manifest shape, this is the test that notices."""
        found = parse_manifest_version(h.repo_file("spectra", "extension.yml").read_text(encoding="utf-8"))
        self.assertIsNotNone(found)
        self.assertRegex(found, r"^\d+\.\d+\.\d+$")

    def test_reads_the_version_from_a_generated_manifest(self):
        self.assertEqual(parse_manifest_version(h.manifest_yaml("2.5.9")), "2.5.9")

    def test_ignores_a_version_nested_deeper_than_the_extension_block(self):
        """`requires:` and friends carry their own version keys at other indentations."""
        text = 'requires:\n  tools:\n    version: "9.9.9"\n'
        self.assertIsNone(parse_manifest_version(text))

    def test_takes_the_extension_block_version_when_others_follow(self):
        text = h.manifest_yaml("1.4.0") + 'other:\n  version: "8.8.8"\n'
        self.assertEqual(parse_manifest_version(text), "1.4.0")

    def test_tolerates_an_unquoted_version(self):
        self.assertEqual(parse_manifest_version("extension:\n  version: 1.5.0\n"), "1.5.0")

    def test_tolerates_a_single_quoted_version(self):
        self.assertEqual(parse_manifest_version("extension:\n  version: '1.5.0'\n"), "1.5.0")

    def test_tolerates_a_trailing_comment(self):
        text = 'extension:\n  version: "1.5.0"  # bumped for the release\n'
        self.assertEqual(parse_manifest_version(text), "1.5.0")

    def test_mismatched_quotes_do_not_match(self):
        self.assertIsNone(parse_manifest_version("extension:\n  version: '1.5.0\"\n"))

    def test_a_spec_kit_reserialized_manifest_reads_the_same_version(self):
        # Spec Kit rewrites an installed manifest with single quotes throughout; the quotes must not
        # leak into the version.
        installed = ("schema_version: '1.0'\nextension:\n  id: spectra\n  version: '1.22.0'\n"
                     "requires:\n  speckit_version: '>=0.11.0'\n")
        self.assertEqual(parse_manifest_version(installed), "1.22.0")

    def test_a_manifest_with_no_version_yields_none(self):
        self.assertIsNone(parse_manifest_version('extension:\n  id: "spectra"\n'))

    def test_an_empty_manifest_yields_none(self):
        self.assertIsNone(parse_manifest_version(""))


if __name__ == "__main__":
    unittest.main()
