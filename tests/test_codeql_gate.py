"""`tools/codeql_gate.py` — the step that turns CodeQL findings into a failing job.

The analyze action stays green whatever it finds, and with no pull requests nothing else blocks on its
results, so this script is the whole of CodeQL's say over `main`. Each test builds the smallest SARIF
that exercises one decision: what blocks, what is only reported, and what must never pass vacuously.
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import helpers as h  # noqa: E402

sys.path.insert(0, str(h.repo_file("tools")))

import codeql_gate  # noqa: E402


def rule(rule_id, severity=None):
    properties = {} if severity is None else {"security-severity": severity}
    return {"id": rule_id, "properties": properties}


def result(rule_id, uri="spectra_cli/cli.py", line=10, **extra):
    return {
        "ruleId": rule_id,
        "message": {"text": f"{rule_id} found here\nsecond line is dropped"},
        "locations": [{"physicalLocation": {
            "artifactLocation": {"uri": uri}, "region": {"startLine": line},
        }}],
        **extra,
    }


def sarif(results, driver_rules=(), extension_rules=()):
    return {"runs": [{
        "tool": {
            "driver": {"name": "CodeQL", "rules": list(driver_rules)},
            "extensions": [{"name": "codeql/python-queries", "rules": list(extension_rules)}],
        },
        "results": list(results),
    }]}


class GateCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name, log):
        (self.dir / name).write_text(json.dumps(log), encoding="utf-8")

    def gate(self, *args):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = codeql_gate.main([str(self.dir), *args])
        return code, buffer.getvalue()


class WhatBlocks(GateCase):
    def test_a_high_finding_fails_the_job(self):
        self.write("python.sarif", sarif([result("py/sql-injection")],
                                         extension_rules=[rule("py/sql-injection", "8.8")]))
        code, out = self.gate()
        self.assertEqual(1, code)
        self.assertIn("::error file=spectra_cli/cli.py,line=10::py/sql-injection (severity 8.8)", out)

    def test_a_critical_finding_fails_the_job(self):
        self.write("python.sarif", sarif([result("py/code-injection")],
                                         extension_rules=[rule("py/code-injection", "9.3")]))
        self.assertEqual(1, self.gate()[0])

    def test_exactly_the_threshold_blocks(self):
        """GitHub's "high" starts at 7.0 inclusive; the gate must agree at the boundary."""
        self.write("python.sarif", sarif([result("py/x")], extension_rules=[rule("py/x", "7.0")]))
        self.assertEqual(1, self.gate()[0])

    def test_rules_on_the_driver_are_resolved_too(self):
        self.write("actions.sarif", sarif([result("actions/code-injection", uri=".github/x.yml")],
                                          driver_rules=[rule("actions/code-injection", "9.3")]))
        self.assertEqual(1, self.gate()[0])

    def test_one_bad_file_among_several_fails_the_job(self):
        self.write("actions.sarif", sarif([]))
        self.write("python.sarif", sarif([result("py/x")], extension_rules=[rule("py/x", "7.5")]))
        self.assertEqual(1, self.gate()[0])


class WhatIsOnlyReported(GateCase):
    def test_a_medium_finding_is_a_warning(self):
        self.write("python.sarif", sarif([result("py/weak")], extension_rules=[rule("py/weak", "5.0")]))
        code, out = self.gate()
        self.assertEqual(0, code)
        self.assertIn("::warning file=spectra_cli/cli.py,line=10::py/weak (severity 5.0)", out)

    def test_a_quality_finding_is_a_warning(self):
        """Quality queries carry no security-severity; they inform and never block."""
        self.write("python.sarif", sarif([result("py/unused-import")],
                                         extension_rules=[rule("py/unused-import")]))
        code, out = self.gate()
        self.assertEqual(0, code)
        self.assertIn("py/unused-import (quality)", out)

    def test_a_suppressed_finding_is_ignored(self):
        self.write("python.sarif", sarif(
            [result("py/x", suppressions=[{"kind": "inSource"}])],
            extension_rules=[rule("py/x", "9.8")]))
        code, out = self.gate()
        self.assertEqual(0, code)
        self.assertNotIn("py/x", out)

    def test_the_threshold_can_be_raised(self):
        self.write("python.sarif", sarif([result("py/x")], extension_rules=[rule("py/x", "8.0")]))
        self.assertEqual(0, self.gate("--threshold", "9.0")[0])

    def test_only_the_first_line_of_a_message_is_printed(self):
        """A workflow annotation ends at the newline; the rest would be printed as a stray log line."""
        self.write("python.sarif", sarif([result("py/x")], extension_rules=[rule("py/x", "2.0")]))
        self.assertNotIn("second line", self.gate()[1])

    def test_a_clean_scan_passes(self):
        self.write("python.sarif", sarif([]))
        code, out = self.gate()
        self.assertEqual(0, code)
        self.assertIn("No finding at security-severity 7.0 or above", out)


class NothingPassesVacuously(GateCase):
    def test_an_empty_directory_fails(self):
        code, out = self.gate()
        self.assertEqual(1, code)
        self.assertIn("no SARIF files", out)

    def test_a_missing_directory_fails(self):
        self._tmp.cleanup()
        self.assertEqual(1, self.gate()[0])


if __name__ == "__main__":
    unittest.main()
