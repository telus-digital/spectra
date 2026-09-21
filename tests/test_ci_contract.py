"""The workflow, the checks registry, and the ruleset's required contexts stay in agreement.

Three things have to say the same thing for `main` to remain both gated and pushable:

1. `.github/workflows/ci.yml` — the jobs that run, and the contexts their names produce.
2. `tools/checks.py` — the catalog checks, defined once and invoked by those jobs.
3. `.github/required-checks.json` — the committed copy of what the "Protect main — tested" ruleset
   requires, which `tools/ship.py` compares against the live ruleset before every push.

The third is the dangerous one. The ruleset lives on GitHub, outside this repository, so renaming a
job here leaves it waiting forever for a context that no longer exists — and because the fix cannot
be delivered by a push, `main` becomes unpushable until someone edits the ruleset by hand. This file
turns that from a trap into a failing test. See SHIPPING.md for the recovery order.

There is no YAML parser available — the repository is zero-dependency by constitution and `yaml` is
not importable here — so the workflow is read with anchored regexes over the exact committed shape,
the same approach `spectra_cli/extension.py` takes to `extension.yml` and for the same reason. Each
regex quotes the shape it matches. A scanner, not a parser.
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import helpers as h  # noqa: E402

sys.path.insert(0, str(h.repo_file("tools")))

import checks as checks_module  # noqa: E402

WORKFLOW = h.repo_file(".github", "workflows", "ci.yml")
REQUIRED_CHECKS = h.repo_file(".github", "required-checks.json")

# A job header is a two-space-indented key directly under `jobs:`:
#   cli:
JOB_HEADER = re.compile(r"^  ([a-z][a-z0-9-]*):$", re.M)

# Its display name — the thing GitHub turns into a status context — is four spaces deep:
#     name: CLI installs and runs
JOB_NAME = re.compile(r"^    name: (.+)$", re.M)

# A matrix suffixes the context with the value in parentheses:
#         python-version: ['3.9', '3.12']
MATRIX_VERSIONS = re.compile(r"^        python-version: \[(.+)\]$", re.M)

# What a step invokes:
#         run: python3 tools/checks.py zip-matches
CHECK_INVOCATION = re.compile(r"^        run: python3 tools/checks\.py ([a-z-]+)$", re.M)


def job_blocks() -> dict:
    """{job id: the text of that job's block} for every job in the workflow."""
    text = WORKFLOW.read_text(encoding="utf-8")
    headers = list(JOB_HEADER.finditer(text))
    blocks = {}
    for index, match in enumerate(headers):
        end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        blocks[match.group(1)] = text[match.end():end]
    return blocks


def workflow_contexts() -> set:
    """The status contexts `ci.yml` produces, matrix expansion included."""
    contexts = set()
    for block in job_blocks().values():
        name = JOB_NAME.search(block)
        if not name:
            continue
        versions = MATRIX_VERSIONS.search(block)
        if versions:
            for raw in versions.group(1).split(","):
                contexts.add(f"{name.group(1)} ({raw.strip().strip(chr(39))})")
        else:
            contexts.add(name.group(1))
    return contexts


class TheRequiredContexts(unittest.TestCase):
    """What the ruleset demands is exactly what the workflow produces."""

    def test_the_workflow_produces_every_committed_context(self):
        """Rename a job without updating the JSON and main becomes unpushable. Fail here instead."""
        committed = set(json.loads(REQUIRED_CHECKS.read_text(encoding="utf-8")))
        produced = workflow_contexts()
        self.assertEqual(
            committed,
            produced,
            "ci.yml and .github/required-checks.json disagree about the status contexts. "
            f"only in the JSON: {sorted(committed - produced)}; "
            f"only in the workflow: {sorted(produced - committed)}. "
            "Update the ruleset first, then this file — see SHIPPING.md, 'the rename deadlock'.",
        )

    def test_the_parse_found_something(self):
        """A scanner that silently matches nothing would make the assertion above vacuous."""
        self.assertGreaterEqual(
            len(workflow_contexts()), 2,
            "the workflow scanner found fewer than two contexts, so ci.yml's shape has changed "
            "and these regexes no longer match it",
        )


class TheChecksRegistry(unittest.TestCase):
    """Every check is registered once and invoked once; neither side may drift."""

    def setUp(self):
        self.invoked = set(CHECK_INVOCATION.findall(WORKFLOW.read_text(encoding="utf-8")))
        self.registered = set(checks_module.CHECKS)

    def test_every_registered_check_runs_in_ci(self):
        """A check nobody runs is worse than no check: it reads as coverage and provides none."""
        missing = self.registered - self.invoked
        self.assertEqual(
            set(), missing,
            f"tools/checks.py registers {sorted(missing)} but no ci.yml step invokes it; "
            "add a step to the catalog job",
        )

    def test_every_ci_invocation_names_a_registered_check(self):
        unknown = self.invoked - self.registered
        self.assertEqual(
            set(), unknown,
            f"ci.yml invokes {sorted(unknown)}, which tools/checks.py does not register; "
            "the step would fail with an argparse error",
        )


class ThePublishedDescription(unittest.TestCase):
    """The description constant has two copies; they may not disagree."""

    def test_the_checks_module_and_the_fixtures_agree(self):
        """FR-051/SC-010 is asserted against `checks.DESCRIPTION`; fixtures build from `h.DESCRIPTION`."""
        self.assertEqual(
            h.DESCRIPTION, checks_module.DESCRIPTION,
            "tests/helpers.py and tools/checks.py carry different extension descriptions, so the "
            "fixtures no longer describe what the check enforces",
        )


if __name__ == "__main__":
    unittest.main()
