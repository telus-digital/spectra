"""The install flow's coverage step, its already-present path, and its exit contract.

`spectra install` gained a fourth step: after the extension is in place, every installed integration that
lacks Spectra's commands gets them, and the project's default integration is put back where it was. Three
properties are asserted here rather than trusted:

* **Silence for the majority.** A project with one integration performs no activation and prints no fourth
  step, so its output is what it was before this feature existed (FR-038, SC-006).
* **Already installed is a state.** Re-running the install in a project that already has Spectra repairs
  coverage and exits 0, instead of failing on the extension step the way it used to (FR-020).
* **Attempt versus abstention.** A coverage step that was tried and failed exits non-zero; one deliberately
  skipped for a stated reason exits zero (spec 011 § Clarifications).

The install talks to `specify` through `ui.run_interactive` and `extension.delegate_*`, so the stub from
`helpers.fake_specify` covers both — with `argv_log` making the rotation's order assertable and `use_effect`
making the registry actually change, without which verification would pass vacuously.
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import helpers as h  # noqa: E402
from spectra_cli import coverage, install, net, project  # noqa: E402


def seed(root, *, installed, default, covered):
    h.write_integration(root, "0.16.5", integrations=list(installed), default_integration=default)
    h.write_registry(root, list(covered))


def recorded_default(root):
    return json.loads((Path(root) / ".specify" / "integration.json")
                      .read_text(encoding="utf-8")).get("default_integration")


def registry_agents(root):
    data = json.loads((Path(root) / ".specify" / "extensions" / ".registry")
                      .read_text(encoding="utf-8"))
    return sorted(data["extensions"]["spectra"]["registered_commands"])


@contextlib.contextmanager
def captured():
    """Run a block with stdout captured, returning the buffer."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        yield buffer


def published(version):
    """Pin the published extension version, so the already-installed path never touches the network."""
    return mock.patch.object(install.health.extension, "published_version", return_value=version)


def cover(root, **kwargs):
    """Run the coverage step against `root`, returning `(exit_code, output)`."""
    with captured() as out:
        code = install.cover_agents(root, **kwargs)
    return code, out.getvalue()


class CoverageStepOutput(unittest.TestCase):
    """What step 4 says, and what it costs in lines (FR-014, FR-033, SC-011)."""

    def test_the_disclosure_names_the_default_it_will_restore(self):
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude"], default="kiro-cli", covered=["kiro-cli"])
            with h.fake_specify(use_effect=root):
                code, out = cover(root)
        self.assertEqual(code, 0)
        self.assertIn("claude is installed here but has no SPECTRA commands", out)
        self.assertIn("This run will do that for", out)
        self.assertIn("set the default back to", out)
        self.assertIn("kiro-cli", out)
        # The disclosure precedes the work: the user is told before anything moves.
        self.assertLess(out.index("set the default back to"),
                        out.index("Registering SPECTRA's commands for"))

    def test_it_reports_what_was_covered_and_that_the_default_came_back(self):
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude"], default="kiro-cli", covered=["kiro-cli"])
            with h.fake_specify(use_effect=root):
                code, out = cover(root)
        self.assertEqual(code, 0)
        self.assertIn("claude — SPECTRA's commands registered", out)
        self.assertIn("default restored to", out)

    def test_the_step_costs_at_most_one_line_per_integration_plus_two(self):
        """SC-011: three integrations, two uncovered — the whole step stays inside its budget."""
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude", "copilot"], default="kiro-cli",
                 covered=["kiro-cli"])
            with h.fake_specify(use_effect=root):
                _, out = cover(root)
        # Lines that report an outcome: one per newly covered agent, plus the restoration confirmation.
        outcome_lines = [line for line in out.splitlines()
                         if "commands registered" in line or "default restored" in line]
        self.assertEqual(len(outcome_lines), 3)

    def test_the_default_only_case_makes_no_transient_default_claim(self):
        """FR-013. Nothing moves, so nothing is said about moving it."""
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude"], default="kiro-cli", covered=["claude"])
            with h.fake_specify(use_effect=root):
                code, out = cover(root)
        self.assertEqual(code, 0)
        self.assertNotIn("set the default back to", out)
        self.assertNotIn("default restored", out)
        self.assertIn("Registering SPECTRA's commands for", out)


class SilenceForTheMajority(unittest.TestCase):
    """FR-037, FR-038, SC-006 — the feature is invisible to projects it does not serve."""

    def test_a_single_covered_integration_prints_nothing_and_activates_nothing(self):
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli"], default="kiro-cli", covered=["kiro-cli"])
            log = Path(root) / "argv.log"
            with h.fake_specify(argv_log=log, use_effect=root):
                code, out = cover(root)
            # Read while the project still exists: a deleted log reads empty too, so an assertion made
            # after cleanup would pass for the wrong reason.
            self.assertEqual(code, 0)
            self.assertEqual(out, "")
            self.assertEqual(h.integration_use_calls(log), [])

    def test_several_integrations_all_covered_print_nothing(self):
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude"], default="kiro-cli",
                 covered=["kiro-cli", "claude"])
            with h.fake_specify(use_effect=root):
                code, out = cover(root)
        self.assertEqual(code, 0)
        self.assertEqual(out, "")

    def test_unknown_coverage_prints_nothing_and_claims_nothing(self):
        """FR-003, FR-004. An unreadable registry is not evidence of a problem."""
        with h.temp_project() as root:
            h.write_integration(root, "0.16.5", integrations=["kiro-cli", "claude"],
                                default_integration="kiro-cli")
            h.write_registry(root, h.BAD_JSON)
            log = Path(root) / "argv.log"
            with h.fake_specify(argv_log=log):
                code, out = cover(root)
            self.assertEqual(code, 0)
            self.assertEqual(out, "")
            self.assertEqual(h.integration_use_calls(log), [])

    def test_a_single_integration_project_predicts_three_steps(self):
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli"], default="kiro-cli", covered=["kiro-cli"])
            self.assertFalse(install.coverage_expected(root))

    def test_a_two_integration_project_predicts_four_steps(self):
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude"], default="kiro-cli", covered=["kiro-cli"])
            self.assertTrue(install.coverage_expected(root))

    def test_a_fresh_project_with_two_integrations_predicts_four_steps(self):
        """The extension is not installed yet, so the prediction reasons from what the install will do."""
        with h.temp_project(installed_version=None) as root:
            h.write_integration(root, "0.16.5", integrations=["kiro-cli", "claude"],
                                default_integration="kiro-cli")
            self.assertTrue(install.coverage_expected(root))

    def test_a_folder_that_is_not_a_project_predicts_three_steps(self):
        self.assertFalse(install.coverage_expected(None))


class NonInteractiveStillCovers(unittest.TestCase):
    """FR-019 — the step is non-destructive and self-reversing, so automation is not excluded."""

    def test_no_terminal_attached_still_performs_the_rotation(self):
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude"], default="kiro-cli", covered=["kiro-cli"])
            log = Path(root) / "argv.log"
            with h.fake_specify(argv_log=log, use_effect=root), \
                    mock.patch("sys.stdin", io.StringIO("")):
                code, _ = cover(root)
            self.assertEqual(code, 0)
            self.assertEqual(h.integration_use_calls(log), ["claude", "kiro-cli"])
            self.assertEqual(registry_agents(root), ["claude", "kiro-cli"])

    def test_the_step_never_prompts(self):
        """It discloses and proceeds; a prompt here would hang an automated provisioning run."""
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude"], default="kiro-cli", covered=["kiro-cli"])
            with h.fake_specify(use_effect=root), \
                    mock.patch("spectra_cli.ui.confirm",
                               side_effect=AssertionError("must not prompt")):
                code, _ = cover(root)
        self.assertEqual(code, 0)


class ExitContract(unittest.TestCase):
    """Attempt versus abstention (spec § Clarifications, FR-017)."""

    def test_a_stated_skip_exits_zero(self):
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude"], default=h.NO_DEFAULT, covered=["kiro-cli"])
            with h.fake_specify():
                code, out = cover(root)
        self.assertEqual(code, 0)
        self.assertIn(coverage.REASON_NO_DEFAULT, out)
        self.assertIn("claude", out)

    def test_an_absent_extension_is_a_stated_skip(self):
        """FR-022. Nothing installed to register is not the same as everything covered."""
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude"], default="kiro-cli", covered=["kiro-cli"])
            with h.fake_specify():
                code, out = cover(root, extension_present=False)
        self.assertEqual(code, 0)
        self.assertIn(coverage.REASON_NOT_INSTALLED, out)

    def test_a_failed_activation_exits_four(self):
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude"], default="kiro-cli", covered=["kiro-cli"])
            with h.fake_specify(use_effect=root, use_fails=["claude"]):
                code, out = cover(root)
        self.assertEqual(code, 4)
        self.assertIn("claude — not registered", out)
        self.assertIn("still missing for: claude", out)
        self.assertIn("spectra install", out)

    def test_a_failed_restore_exits_four_and_names_the_recovery_command(self):
        """FR-034, SC-008 — the only place the dependency's own command is printed as advice."""
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude"], default="kiro-cli", covered=["kiro-cli"])
            with h.fake_specify(use_effect=root, use_fails=["kiro-cli"]):
                code, out = cover(root)
        self.assertEqual(code, 4)
        self.assertIn("Could not set the default integration back to kiro-cli", out)
        self.assertIn("currently defaulted to", out)
        self.assertIn("specify integration use kiro-cli", out)

    def test_an_interrupt_exits_130_and_is_reported_as_an_interruption(self):
        """FR-036. And the interrupted project is repairable by re-running the install (SC-010)."""
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude", "copilot"], default="kiro-cli",
                 covered=["kiro-cli"])
            real = install.coverage.extension.delegate_integration_use
            calls = []

            def interrupt_on_second(key):
                calls.append(key)
                if len(calls) == 2:
                    raise KeyboardInterrupt
                return real(key)

            with h.fake_specify(use_effect=root):
                install.coverage.extension.delegate_integration_use = interrupt_on_second
                try:
                    code, out = cover(root)
                finally:
                    install.coverage.extension.delegate_integration_use = real
            self.assertEqual(code, 130)
            self.assertIn("Interrupted", out)
            self.assertEqual(recorded_default(root), "kiro-cli")

            # SC-010: the interrupted state is repaired by running the step again.
            with h.fake_specify(use_effect=root):
                code, _ = cover(root)
            self.assertEqual(code, 0)
            self.assertEqual(registry_agents(root), ["claude", "copilot", "kiro-cli"])
            self.assertEqual(recorded_default(root), "kiro-cli")


class ConfigurationUnchanged(unittest.TestCase):
    """FR-043, SC-002, SC-013."""

    def test_committed_configuration_is_byte_identical_after_the_step(self):
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude"], default="kiro-cli", covered=["kiro-cli"])
            config = Path(root) / ".specify" / "integration.json"
            before = config.read_bytes()
            with h.fake_specify(use_effect=root):
                cover(root)
            self.assertEqual(config.read_bytes(), before)


class AlreadyInstalledIsAState(unittest.TestCase):
    """FR-020, FR-021, FR-023 — the repair path for every project that predates this feature."""

    def test_an_already_present_extension_is_not_reinstalled(self):
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli", "claude"], default="kiro-cli", covered=["kiro-cli"])
            log = Path(root) / "argv.log"
            with h.fake_specify(argv_log=log), \
                    mock.patch.object(install, "catalog_extension_ids", return_value=["spectra"]), \
                    mock.patch.object(install, "register_catalog", return_value=True), \
                    published("1.3.1"):
                with captured() as out:
                    ok = install.add_catalog(root, total_steps=4)
            self.assertTrue(ok)
            self.assertIn("already installed here", out.getvalue())
            # The decisive assertion: `specify` was not invoked at all — no add, no download, no
            # overwrite (FR-023). The log is absent precisely because nothing ran, which is the point.
            self.assertEqual(h.read_argv_log(log), [])
            self.assertFalse(log.exists())

    def already_installed_output(self, publisher):
        with h.temp_project() as root:
            seed(root, installed=["kiro-cli"], default="kiro-cli", covered=["kiro-cli"])
            with h.fake_specify(), \
                    mock.patch.object(install, "catalog_extension_ids", return_value=["spectra"]), \
                    mock.patch.object(install, "register_catalog", return_value=True), \
                    publisher:
                with captured() as out:
                    self.assertTrue(install.add_catalog(root, total_steps=3))
        return h.plain_lines(out.getvalue())

    def test_a_current_extension_says_up_to_date_and_does_not_suggest_updating(self):
        text = "\n".join(self.already_installed_output(published("1.3.1")))
        self.assertIn("already installed here (1.3.1) and up to date", text)
        self.assertNotIn("spectra update", text)

    def test_a_published_version_older_than_the_installed_one_is_still_up_to_date(self):
        text = "\n".join(self.already_installed_output(published("1.2.0")))
        self.assertIn("and up to date", text)
        self.assertNotIn("spectra update", text)

    def test_a_newer_published_extension_offers_the_update(self):
        lines = self.already_installed_output(published("1.4.0"))
        self.assertIn("  An update is available (1.4.0) — run: spectra update", lines)
        self.assertNotIn("up to date", "\n".join(lines))

    def test_an_unreachable_catalog_does_not_claim_up_to_date(self):
        unreachable = mock.patch.object(install.health.extension, "published_version",
                                        side_effect=net.FetchError("offline"))
        text = "\n".join(self.already_installed_output(unreachable))
        self.assertIn("Couldn't check for updates", text)
        self.assertIn("spectra update", text)
        self.assertNotIn("up to date", text)

    def test_the_decision_comes_from_project_state_not_from_message_text(self):
        """FR-021. The presence check is a filesystem question, asked before anything is attempted."""
        with h.temp_project() as root:
            self.assertTrue(project.extension_present(root, "spectra"))
            self.assertFalse(project.extension_present(root, "not-a-real-extension"))

    def test_an_incomplete_extension_folder_is_treated_as_absent(self):
        """research R6 — an unusable folder must not block the add that would repair it."""
        with h.temp_project(installed_version=h.NO_VERSION) as root:
            self.assertEqual(project.classify(root).state, project.INCOMPLETE)
            seed(root, installed=["kiro-cli", "claude"], default="kiro-cli", covered=["kiro-cli"])
            log = Path(root) / "argv.log"
            with h.fake_specify(argv_log=log), \
                    mock.patch.object(install, "catalog_extension_ids", return_value=["spectra"]), \
                    mock.patch.object(install, "register_catalog", return_value=True):
                with captured():
                    install.add_catalog(root, total_steps=4)
            self.assertEqual([argv for argv in h.read_argv_log(log)
                              if argv[:2] == ["extension", "add"]], [["extension", "add", "spectra"]])

    def test_an_absent_extension_is_installed_as_before(self):
        with h.temp_project(installed_version=None) as root:
            h.write_integration(root, "0.16.5", integrations=["kiro-cli"],
                                default_integration="kiro-cli")
            log = Path(root) / "argv.log"
            with h.fake_specify(argv_log=log), \
                    mock.patch.object(install, "catalog_extension_ids", return_value=["spectra"]), \
                    mock.patch.object(install, "register_catalog", return_value=True):
                with captured() as out:
                    ok = install.add_catalog(root, total_steps=3)
            self.assertTrue(ok)
            self.assertIn("Installing the SPECTRA extension", out.getvalue())
            self.assertEqual([argv for argv in h.read_argv_log(log)
                              if argv[:2] == ["extension", "add"]], [["extension", "add", "spectra"]])


class FinalMessage(unittest.TestCase):
    """A successful run ends by pointing at Spec Kit for integrations — first install and re-run alike."""

    def run_install(self, add_catalog_result=True):
        with h.temp_project() as root, h.cwd(root), \
                mock.patch.object(install.ui, "intro_note"), \
                mock.patch.object(install, "coverage_expected", return_value=False), \
                mock.patch.object(install, "ensure_specify_installed"), \
                mock.patch.object(install, "check_in_specify_project", return_value=Path(root)), \
                mock.patch.object(install, "add_catalog", return_value=add_catalog_result):
            with captured() as out:
                code = install.run_install()
        return code, h.plain_lines(out.getvalue())

    def test_the_integrations_pointer_follows_all_set(self):
        code, lines = self.run_install()
        self.assertEqual(code, 0)
        index = next(i for i, line in enumerate(lines) if line.startswith("All set!"))
        self.assertEqual(lines[index + 1],
                         "To manage coding agent integrations, use: specify integration --help")

    def test_a_failed_install_does_not_show_it(self):
        _, lines = self.run_install(add_catalog_result=False)
        self.assertNotIn("specify integration --help", "\n".join(lines))


class DecliningInitialization(unittest.TestCase):
    """Declining `specify init` points back at Spectra's own command, not at Spec Kit's."""

    def test_the_remedy_is_spectra_install(self):
        with h.temp_project(is_project=False) as root, h.cwd(root):
            with mock.patch.object(install.ui, "confirm", return_value=False), captured() as out:
                with self.assertRaises(SystemExit) as raised:
                    install.check_in_specify_project()
        self.assertEqual(raised.exception.code, 1)
        remedy = out.getvalue().split("A Spec Kit project is required to continue.", 1)[1]
        self.assertIn("Re-run `spectra install`", remedy)
        self.assertNotIn("specify init", remedy)

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
