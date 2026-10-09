"""`spectra cli version` — the spectra command reports on itself, from anywhere (spec 030).

Two contracts are defended. Isolation: the command reports on the tool and only the tool, so it answers
the same in a folder with no Spec Kit project as inside one in any state, and never reads or writes
either. Honesty: "latest" and "available" are said only when the newest release was actually resolved
and compared, and the next step it names is one that works for this install. Everything else is the
outcome table in `specs/030-cli-version-check/data-model.md`.

The release feed and uv are always mocked: a suite that reached GitHub would fail for reasons that have
nothing to do with the code under test.
"""

from __future__ import annotations

import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import helpers as h  # noqa: E402
from spectra_cli import cli, coverage, extension, health, project, ui, version  # noqa: E402


def run(argv):
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            code = cli.main(argv)
    except SystemExit as exc:  # pragma: no cover
        code = exc.code
    return code, buffer.getvalue()


def plain(out):
    return "\n".join(h.plain_lines(out))


@contextlib.contextmanager
def release(status="update_available", installed="6.3.0", latest="6.4.0", *,
            kind=version.UV_MANAGED):
    """Fix the installed version, the release verdict, and the install kind.

    Yields the mocks so a test can assert which were reached — the order in which the command consults
    them is part of the contract (no install probe unless an update exists). The opt-out variable is
    cleared so a developer's own environment cannot change the outcome.
    """
    check = {"status": status, "installed": installed,
             "latest": None if status == "latest_unknown" else latest}
    env = {k: v for k, v in os.environ.items() if k != "SPECTRA_NO_UPDATE_CHECK"}
    with mock.patch.dict(os.environ, env, clear=True), \
         mock.patch.object(version, "read_installed_version", return_value=installed), \
         mock.patch.object(version, "check_update", return_value=check) as checked, \
         mock.patch.object(version, "resolve_latest") as resolved, \
         mock.patch.object(version, "passive_check") as nudged, \
         mock.patch.object(version, "classify_uninstall", return_value=kind) as classified, \
         mock.patch.object(version, "perform_update") as performed, \
         mock.patch.object(ui, "confirm") as confirmed:
        yield mock.Mock(checked=checked, resolved=resolved, nudged=nudged, classified=classified,
                        performed=performed, confirmed=confirmed)


# Every outcome in the data model, as (label, release kwargs). Used where a property must hold for all.
OUTCOMES = [
    ("latest", dict(status="up_to_date", installed="6.4.0")),
    ("ahead", dict(status="ahead", installed="6.5.0")),
    ("available", dict()),
    ("available-pip", dict(kind=version.PIP_OR_SOURCE)),
    ("available-source", dict(kind=version.NOT_INSTALLED)),
    ("available-no-uv", dict(kind=version.UNKNOWN_UV_ABSENT)),
    ("unreachable", dict(status="latest_unknown")),
    ("installed-unknown", dict(installed=None)),
]


class _InEmptyFolder(unittest.TestCase):
    """Every test runs from a fresh folder with no Spec Kit project above it (US1)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.folder = Path(self._tmp.name)
        ctx = h.cwd(self._tmp.name)
        ctx.__enter__()
        self.addCleanup(ctx.__exit__, None, None, None)


class Outcomes(_InEmptyFolder):
    """FR-004 – FR-009: one test per row of the data model; every answer exits 0."""

    def test_latest_says_so_and_does_not_mention_cli_update(self):
        with release(status="up_to_date", installed="6.4.0") as m:
            code, out = run(["cli", "version"])
        self.assertEqual(code, cli.EXIT_OK)
        self.assertIn("spectra 6.4.0 is the latest release.", plain(out))
        self.assertNotIn("spectra cli update", out)
        m.classified.assert_not_called()

    def test_ahead_is_reported_as_latest_and_never_offers_a_downgrade(self):
        with release(status="ahead", installed="6.5.0") as m:
            code, out = run(["cli", "version"])
        self.assertEqual(code, cli.EXIT_OK)
        text = plain(out)
        self.assertIn("6.5.0 is the latest", text)
        self.assertIn("ahead of the newest release (6.4.0)", text)
        self.assertNotIn("available", text)
        self.assertNotIn("spectra cli update", text)
        m.classified.assert_not_called()

    def test_an_available_update_names_both_versions_and_cli_update(self):
        with release() as m:
            code, out = run(["cli", "version"])
        self.assertEqual(code, cli.EXIT_OK)
        text = plain(out)
        self.assertIn("spectra 6.3.0 — a new version 6.4.0 is available.", text)
        self.assertEqual(h.plain_lines(out)[-1], "  Update it with: spectra cli update")
        m.classified.assert_called_once()

    def test_a_pip_or_source_install_is_told_how_to_update_instead(self):
        """FR-007 / SC-002: `cli update` cannot help this install, so it is not offered as the fix."""
        for kind in (version.PIP_OR_SOURCE, version.NOT_INSTALLED):
            with self.subTest(kind=kind), release(kind=kind):
                code, out = run(["cli", "version"])
            self.assertEqual(code, cli.EXIT_OK)
            text = plain(out)
            self.assertIn("a new version 6.4.0 is available", text)
            self.assertIn("not installed as a uv tool", text)
            self.assertIn("Source checkout: pull the latest changes.", text)
            self.assertNotIn("Update it with", text)

    def test_a_missing_uv_gets_the_pinned_manual_command(self):
        with release(kind=version.UNKNOWN_UV_ABSENT):
            code, out = run(["cli", "version"])
        self.assertEqual(code, cli.EXIT_OK)
        text = plain(out)
        self.assertIn("uv was not found on PATH", text)
        self.assertIn(f"uv tool install {version.DIST_NAME} --from '{version.git_source('6.4.0')}' "
                      "--force", text)
        self.assertNotIn("Update it with", text)

    def test_the_hints_match_what_cli_update_says_for_the_same_install(self):
        """Research R4: one helper, so the two commands cannot drift apart."""
        hint = "Source checkout: pull the latest changes. pip install: reinstall with the tool you used."
        for argv in (["cli", "version"], ["cli", "update", "--yes"]):
            with self.subTest(argv=argv), release(kind=version.PIP_OR_SOURCE):
                _, out = run(argv)
            self.assertIn(hint, plain(out))

    def test_an_unreachable_feed_still_names_the_installed_version_and_exits_zero(self):
        """FR-008 / FR-009 / SC-004 (clarification Q2)."""
        with release(status="latest_unknown") as m:
            code, out = run(["cli", "version"])
        self.assertEqual(code, cli.EXIT_OK)
        text = plain(out)
        self.assertIn("spectra 6.3.0 — the newest release could not be checked.", text)
        self.assertNotIn("latest", text)
        self.assertNotIn("available", text)
        m.classified.assert_not_called()

    def test_an_unknown_installed_version_makes_no_comparison_claim(self):
        """Data-model row 3: an unknown sorts below every release, which would be a false "available"."""
        with release(installed=None) as m:
            code, out = run(["cli", "version"])
        self.assertEqual(code, cli.EXIT_OK)
        text = plain(out)
        self.assertIn("installed spectra version could not be determined", text)
        self.assertIn("6.4.0", text)
        self.assertNotIn("available", text)
        self.assertNotIn("spectra cli update", text)
        m.classified.assert_not_called()


class ReadOnly(_InEmptyFolder):
    """FR-003 / FR-006 / US1-AS3: whatever the outcome, it only reports."""

    def test_no_outcome_prompts_updates_or_nudges(self):
        for label, kwargs in OUTCOMES:
            with self.subTest(outcome=label), release(**kwargs) as m:
                code, _ = run(["cli", "version"])
            self.assertEqual(code, cli.EXIT_OK)
            m.performed.assert_not_called()
            m.confirmed.assert_not_called()
            m.nudged.assert_not_called()

    def test_no_outcome_talks_about_projects_or_retirement(self):
        for label, kwargs in OUTCOMES:
            with self.subTest(outcome=label), release(**kwargs):
                _, out = run(["cli", "version"])
            for wrong in ("not a Spec Kit project", "retired", "spectra install"):
                self.assertNotIn(wrong, out)

    def test_it_writes_nothing_into_the_current_folder(self):
        for label, kwargs in OUTCOMES:
            with self.subTest(outcome=label), release(**kwargs):
                run(["cli", "version"])
            self.assertEqual(list(self.folder.iterdir()), [])

    def test_yes_changes_nothing(self):
        with release():
            _, plain_run = run(["cli", "version"])
        with release() as m:
            code, with_yes = run(["cli", "version", "--yes"])
        self.assertEqual(code, cli.EXIT_OK)
        self.assertEqual(with_yes, plain_run)
        m.performed.assert_not_called()

    def test_force_is_not_accepted(self):
        with release(), contextlib.redirect_stderr(io.StringIO()):
            code, _ = run(["cli", "version", "--force"])
        self.assertEqual(code, cli.EXIT_USAGE)


def _snapshot(root: Path):
    return {p.relative_to(root): (p.read_bytes() if p.is_file() else None)
            for p in sorted(root.rglob("*"))}


class InsideAProject(unittest.TestCase):
    """US2: inside a project, in any state, the answer is the same and nothing is touched."""

    STATES = {
        "installed": dict(),
        "not-installed": dict(installed_version=None),
        "incomplete": dict(incomplete=True),
    }

    def _outside(self):
        with tempfile.TemporaryDirectory() as tmp, h.cwd(tmp), release():
            return run(["cli", "version"])

    def test_every_project_state_gets_the_no_project_answer_and_is_untouched(self):
        expected = self._outside()
        for label, kwargs in self.STATES.items():
            with self.subTest(state=label), h.temp_project(**kwargs) as path:
                root = Path(path)
                while not (root / ".specify").exists() and root != root.parent:
                    root = root.parent
                before = _snapshot(root)
                with h.cwd(path), release():
                    result = run(["cli", "version"])
                self.assertEqual(result, expected)
                self.assertEqual(_snapshot(root), before)

    def test_it_never_consults_the_project_or_the_other_components(self):
        """FR-002 / FR-003, by construction: every project-facing entry point raises if reached."""
        boom = mock.Mock(side_effect=AssertionError("cli version reached project code"))
        with h.temp_project() as path, h.cwd(path), \
             mock.patch.object(project, "classify", boom), \
             mock.patch.object(health, "check_all", boom), \
             mock.patch.object(extension, "delegate_update", boom), \
             mock.patch.object(coverage, "plan", boom), \
             mock.patch.object(coverage, "apply", boom):
            for label, kwargs in OUTCOMES:
                with self.subTest(outcome=label), release(**kwargs):
                    code, out = run(["cli", "version"])
                self.assertEqual(code, cli.EXIT_OK)
                for other in ("Spec Kit CLI", "core agents", "Core agents", "agents installed"):
                    self.assertNotIn(other, out)
        boom.assert_not_called()


class OptOuts(_InEmptyFolder):
    """FR-010 (clarification Q3): the opt-outs make it offline; it still names the installed version."""

    def _assert_offline(self, argv, env=None):
        with release() as m, mock.patch.dict(os.environ, env or {}):
            code, out = run(argv)
        self.assertEqual(code, cli.EXIT_OK)
        m.checked.assert_not_called()
        m.resolved.assert_not_called()
        m.classified.assert_not_called()
        m.nudged.assert_not_called()
        text = plain(out)
        self.assertIn("spectra 6.3.0 (update check skipped).", text)
        self.assertNotIn("latest", text)
        self.assertNotIn("available", text)

    def test_the_flag_after_the_subcommand(self):
        self._assert_offline(["cli", "version", "--no-update-check"])

    def test_the_flag_before_the_subcommand(self):
        self._assert_offline(["--no-update-check", "cli", "version"])

    def test_the_environment_variable(self):
        self._assert_offline(["cli", "version"], env={"SPECTRA_NO_UPDATE_CHECK": "1"})


class Help(_InEmptyFolder):
    """US3 / FR-013: discoverable from both help screens, first among the tool commands."""

    def test_the_tool_panel_lists_version_then_update_then_uninstall(self):
        with release():
            code, out = run(["--help"])
        self.assertEqual(code, cli.EXIT_OK)
        text = plain(out)
        tool_panel = text[text.index("Tool commands"):text.index("Options")]
        positions = [tool_panel.index(label) for label in ("cli version", "cli update", "cli uninstall")]
        self.assertEqual(positions, sorted(positions))

    def test_the_description_says_tool_only_and_anywhere(self):
        described = dict(cli.TOOL_COMMANDS)["cli version"]
        self.assertIn("any folder", described)
        self.assertIn("never checks the agents", described)

    def test_the_cli_group_lists_all_three(self):
        with release():
            code, out = run(["cli"])
        self.assertEqual(code, cli.EXIT_USAGE)
        panel = plain(out)[plain(out).index("Tool commands"):]
        positions = [panel.index(name) for name in ("version", "update", "uninstall")]
        self.assertEqual(positions, sorted(positions))


if __name__ == "__main__":
    unittest.main()
