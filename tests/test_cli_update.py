"""`spectra cli update` — the spectra command updates itself, from anywhere (spec 029).

The contract being defended is isolation: the command updates the tool and only the tool, so it runs the
same in a folder with no Spec Kit project as inside one, and never reads or writes either. Everything
else here is the outcome table in `specs/029-cli-self-update/contracts/cli-update-command.md`.

The release feed and uv are always mocked: a suite that reached GitHub or reinstalled the tool would fail
for reasons that have nothing to do with the code under test.
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


@contextlib.contextmanager
def release(status="update_available", installed="6.2.2", latest="6.3.0", *,
            kind=version.UV_MANAGED, tty=False, answer=None, update_error=None):
    """Fix the release verdict, the install kind, the terminal, and the user's answer.

    Yields the mocks so a test can assert which of them were reached — the order in which the command
    consults them is part of the contract (no install probe when nothing needs doing).
    """
    check = {"status": status, "installed": installed,
             "latest": None if status == "latest_unknown" else latest}
    with mock.patch.object(version, "check_update", return_value=check) as checked, \
         mock.patch.object(version, "classify_uninstall", return_value=kind) as classified, \
         mock.patch.object(version, "perform_update",
                           side_effect=update_error) as performed, \
         mock.patch.object(ui, "confirm", return_value=answer) as confirmed, \
         mock.patch.object(sys.stdin, "isatty", return_value=tty):
        yield mock.Mock(checked=checked, classified=classified, performed=performed,
                        confirmed=confirmed)


class _InEmptyFolder(unittest.TestCase):
    """Every test runs from a fresh folder with no Spec Kit project above it (US1)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        ctx = h.cwd(self._tmp.name)
        ctx.__enter__()
        self.addCleanup(ctx.__exit__, None, None, None)


class Updates(_InEmptyFolder):
    """Update available, uv-managed: confirm, update, report old → new."""

    def test_yes_after_the_subcommand_updates_without_asking(self):
        with release() as m:
            code, out = run(["cli", "update", "--yes"])
        self.assertEqual(code, cli.EXIT_OK)
        m.performed.assert_called_once_with("6.3.0")
        m.confirmed.assert_not_called()
        plain = "\n".join(h.plain_lines(out))
        self.assertIn("6.2.2 → 6.3.0", plain)
        self.assertIn("takes effect the next time you run spectra", plain)

    def test_yes_before_the_subcommand_means_the_same(self):
        with release() as m:
            code, _ = run(["--yes", "cli", "update"])
        self.assertEqual(code, cli.EXIT_OK)
        m.performed.assert_called_once_with("6.3.0")

    def test_answering_yes_at_a_terminal_updates(self):
        with release(tty=True, answer=True) as m:
            code, out = run(["cli", "update"])
        self.assertEqual(code, cli.EXIT_OK)
        m.confirmed.assert_called_once()
        m.performed.assert_called_once_with("6.3.0")
        self.assertIn("Updated the spectra command", out)

    def test_the_plan_names_both_versions_and_says_projects_are_untouched(self):
        with release() as m:
            _, out = run(["cli", "update", "--yes"])
        self.assertIn("A new version", out)
        self.assertIn("(you have 6.2.2)", out)
        self.assertIn("Your projects and their agents are not touched", out)
        m.performed.assert_called_once()

    def test_it_never_says_this_is_not_a_spec_kit_project(self):
        """US1-AS2: there is nothing here to initialize, and the command must not suggest it."""
        with release():
            _, out = run(["cli", "update", "--yes"])
        self.assertNotIn("not a Spec Kit project", out)
        self.assertNotIn("spectra install", out)


class AlreadyCurrent(_InEmptyFolder):
    """FR-006: nothing to do, so no prompt, no install probe, and exit 0."""

    def test_up_to_date_and_ahead_both_report_current(self):
        for status in ("up_to_date", "ahead"):
            with self.subTest(status=status), release(status=status, installed="6.3.0") as m:
                code, out = run(["cli", "update"])
            self.assertEqual(code, cli.EXIT_OK)
            self.assertIn("The spectra command is up to date (6.3.0).", h.plain_lines(out)[-1])
            m.classified.assert_not_called()
            m.performed.assert_not_called()
            m.confirmed.assert_not_called()


class Unreachable(_InEmptyFolder):
    """FR-007, SC-005: an unknown answer is never reported as "up to date"."""

    def test_an_unreachable_feed_exits_three_and_changes_nothing(self):
        with release(status="latest_unknown") as m:
            code, out = run(["cli", "update", "--yes"])
        self.assertEqual(code, cli.EXIT_UNREACHABLE)
        self.assertIn("Could not check for a newer spectra command", out)
        self.assertIn("Nothing was changed", out)
        self.assertNotIn("up to date", out)
        m.classified.assert_not_called()
        m.performed.assert_not_called()


class Confirmation(_InEmptyFolder):
    """FR-004, FR-005 (spec 029 Clarifications): ask first, like `spectra update`."""

    def test_declining_changes_nothing_and_exits_one(self):
        with release(tty=True, answer=False) as m:
            code, out = run(["cli", "update"])
        self.assertEqual(code, cli.EXIT_DECLINED)
        self.assertIn("Nothing was changed.", out)
        m.performed.assert_not_called()

    def test_non_interactive_without_yes_refuses_without_prompting(self):
        with release(tty=False) as m:
            code, out = run(["cli", "update"])
        self.assertEqual(code, cli.EXIT_DECLINED)
        self.assertIn("Re-run with --yes", h.plain_lines(out)[-1])
        m.confirmed.assert_not_called()
        m.performed.assert_not_called()


class InstallKinds(_InEmptyFolder):
    """FR-008, FR-009: an install the command cannot update is explained, never attempted."""

    def test_a_source_or_pip_install_is_explained_and_left_alone(self):
        for kind in (version.NOT_INSTALLED, version.PIP_OR_SOURCE):
            with self.subTest(kind=kind), release(kind=kind, tty=True) as m:
                code, out = run(["cli", "update"])
            self.assertEqual(code, cli.EXIT_OK)
            self.assertIn("not installed as a uv tool, so it cannot update itself", out)
            m.confirmed.assert_not_called()
            m.performed.assert_not_called()

    def test_missing_uv_prints_a_manual_command_pinned_to_the_release(self):
        with release(kind=version.UNKNOWN_UV_ABSENT, tty=True) as m:
            code, out = run(["cli", "update"])
        self.assertEqual(code, cli.EXIT_DELEGATION)
        plain = "\n".join(h.plain_lines(out))
        self.assertIn("uv was not found on PATH", plain)
        self.assertIn(f"uv tool install {version.DIST_NAME} --from '", plain)
        self.assertIn("@6.3.0' --force", plain)
        m.confirmed.assert_not_called()
        m.performed.assert_not_called()


class Failure(_InEmptyFolder):
    """FR-009, SC-005: a failed uv run is reported as a failure, never as an update."""

    def test_a_failed_update_exits_four_and_says_the_version_is_unchanged(self):
        error = version.UpdateError("uv exited with code 1; your current version is unchanged.")
        with release(update_error=error):
            code, out = run(["cli", "update", "--yes"])
        self.assertEqual(code, cli.EXIT_DELEGATION)
        self.assertIn("Update failed", out)
        self.assertIn("unchanged", out)
        self.assertNotIn("Updated the spectra command", out)


class Flags(_InEmptyFolder):
    """FR-011: the opt-out is for unasked-for checks; this command is the ask."""

    def test_no_update_check_flag_does_not_skip_the_check(self):
        with release(status="up_to_date", installed="6.3.0") as m:
            code, out = run(["cli", "update", "--no-update-check"])
        self.assertEqual(code, cli.EXIT_OK)
        m.checked.assert_called_once()
        self.assertIn("up to date", out)

    def test_no_update_check_environment_does_not_skip_the_check(self):
        with mock.patch.dict(os.environ, {"SPECTRA_NO_UPDATE_CHECK": "1"}), \
             release(status="up_to_date", installed="6.3.0") as m:
            code, _ = run(["cli", "update"])
        self.assertEqual(code, cli.EXIT_OK)
        m.checked.assert_called_once()

    def test_force_is_not_accepted(self):
        """`--force` authorizes overwriting project files, which this command never does."""
        with release() as m:
            code, _ = run(["cli", "update", "--force"])
        self.assertEqual(code, cli.EXIT_USAGE)
        m.performed.assert_not_called()


class Isolation(unittest.TestCase):
    """US2 — FR-002, FR-003, SC-002: inside a project, only the command changes."""

    def test_it_never_consults_the_project_or_another_component(self):
        boom = mock.Mock(side_effect=AssertionError("cli update must not reach this"))
        with h.temp_project() as path, h.cwd(path), \
             mock.patch.object(project, "classify", boom), \
             mock.patch.object(health, "check_all", boom), \
             mock.patch.object(health, "apply_updates", boom), \
             mock.patch.object(extension, "delegate_update", boom), \
             mock.patch.object(coverage, "plan", boom), \
             mock.patch.object(coverage, "apply", boom), \
             release() as m:
            code, out = run(["cli", "update", "--yes"])
        self.assertEqual(code, cli.EXIT_OK, out)
        m.performed.assert_called_once_with("6.3.0")
        boom.assert_not_called()

    def test_the_project_tree_is_byte_for_byte_unchanged(self):
        def snapshot(root):
            return {p.relative_to(root).as_posix(): p.read_bytes()
                    for p in sorted(Path(root).rglob("*")) if p.is_file()}

        with h.temp_project(integration_version="0.16.4") as path, h.cwd(path):
            before = snapshot(path)
            with release():
                _, out = run(["cli", "update", "--yes"])
            after = snapshot(path)
        self.assertTrue(before)
        self.assertEqual(before, after)
        for other in ("Spec Kit CLI", "Spec Kit CLI", "Core agents", "SPECTRA agents"):
            self.assertNotIn(other, out)


class Help(unittest.TestCase):
    """US3 — FR-012, FR-013: the command is where a reader looks for it."""

    def test_top_level_help_lists_cli_update_first_in_the_tool_panel(self):
        _, out = run(["--help"])
        lines = h.plain_lines(out)
        panel = next(i for i, line in enumerate(lines)
                     if "Tool commands — act on the spectra command itself" in line)
        update = next(i for i, line in enumerate(lines) if "cli update" in line)
        uninstall = next(i for i, line in enumerate(lines) if "cli uninstall" in line)
        self.assertLess(panel, update)
        self.assertLess(update, uninstall)

    def test_the_description_says_what_where_and_what_it_leaves_alone(self):
        described = dict(cli.TOOL_COMMANDS)["cli update"]
        self.assertIn("spectra command itself", described)
        self.assertIn("any folder", described)
        self.assertIn("never touches the agents", described)

    def test_the_cli_group_lists_update_before_uninstall(self):
        _, out = run(["cli"])
        plain = "\n".join(h.plain_lines(out))
        self.assertIn("work from any folder", plain)
        self.assertNotIn("use the top-level commands instead", plain)
        self.assertLess(plain.index(" update "), plain.index(" uninstall "))


if __name__ == "__main__":
    unittest.main()
