"""The `uat` flow, asserted against the command text that ships.

A command file is a prompt: its text *is* the implementation, so the enforceable surface is what it
says. These assertions cannot prove an agent behaves correctly at run time — that is the manual pass in
specs/032-uat-and-test-handoff/quickstart.md. What they prove is that the rules it is supposed to follow
have not been quietly deleted, which is the regression that actually happens to prompt files.

`speckit.spectra.uat` is the first Spectra command that **executes the user's application**, and the
first that writes ticks into `tasks.md` on the strength of its own observation. Both make it the
command whose rules matter most when they go missing:

- **It ticks only what it saw pass.** A tick is a claim that acceptance happened. The failure mode is not
  an error message; it is a confident `[X]` on a scenario nobody accepted.
- **It never infers the feature.** Same reason as test-plan: ticks against the wrong feature are
  undetectably wrong.
- **It starts nothing before a confirmation**, and acts on no environment the user did not name.
- **It changes nothing it is accepting** — not source, not tests, not the spec, not the test plan.
- **It reproduces no secret.** A committed screenshot cannot be recalled.

Standard library only, like the rest of the suite.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import helpers as h  # noqa: E402

COMMAND = h.repo_file("spectra", "commands", "uat.md")
TEMPLATE = h.repo_file("spectra", "templates", "uat-report-template.md")
MANIFEST = h.repo_file("spectra", "extension.yml")

COMMAND_NAME = "speckit.spectra.uat"

# A Markdown checkbox at the start of a line — the construct the report must never contain.
CHECKBOX = re.compile(r"^[ \t]*[-*][ \t]\[[ xX]\]", re.M)


def command_text() -> str:
    return COMMAND.read_text(encoding="utf-8")


def phrases() -> str:
    """Lowercased, whitespace collapsed — so an assertion survives a re-wrap of the prose."""
    return " ".join(command_text().split()).lower()


def hooks_block() -> str:
    manifest = MANIFEST.read_text(encoding="utf-8")
    return manifest.partition("\nhooks:")[2].partition("\ntags:")[0]


class TheCommandIsRegistered(unittest.TestCase):

    def test_the_command_file_exists(self):
        self.assertTrue(COMMAND.is_file())

    def test_the_manifest_registers_it(self):
        manifest = MANIFEST.read_text(encoding="utf-8")
        self.assertIn(f'name: "{COMMAND_NAME}"', manifest)
        self.assertIn('file: "commands/uat.md"', manifest)

    def test_it_has_front_matter_with_a_description(self):
        text = command_text()
        self.assertTrue(text.startswith("---\n"))
        self.assertIn("description:", text.split("---")[1])

    def test_it_takes_input_through_the_generic_placeholder(self):
        self.assertIn("$ARGUMENTS", command_text())


class TheFeatureIsRequiredAndNeverInferred(unittest.TestCase):

    def test_the_feature_is_required(self):
        self.assertIn("the feature is required", phrases())

    def test_an_empty_argument_stops(self):
        self.assertIn("read nothing, start nothing, write nothing", phrases())

    def test_it_never_infers_the_feature(self):
        text = phrases()
        self.assertIn("never infer which feature was meant", text)
        for source in ("branch", "feature.json", "modification time"):
            with self.subTest(source=source):
                self.assertIn(source, text)

    def test_it_offers_no_picker(self):
        self.assertIn("do not offer a list", phrases())

    def test_it_stops_when_the_feature_is_outside_the_project(self):
        self.assertIn("outside the project", phrases())


class ItRunsNothingUnconfirmed(unittest.TestCase):

    def test_incomplete_implementation_is_reported_and_asked(self):
        self.assertIn("implementation is incomplete", phrases())

    def test_the_run_confirmation_shows_the_exact_command(self):
        text = phrases()
        self.assertIn("the exact command", text)
        self.assertIn("before the run confirmation", text)

    def test_a_declined_run_blocks_rather_than_fails(self):
        self.assertIn("blocked — run declined", phrases())

    def test_it_acts_locally_unless_an_environment_is_named(self):
        text = phrases()
        self.assertIn("locally started build", text)
        self.assertIn("--env", text)
        self.assertIn("act on an environment the user did not name", text)


class ItAttemptsOnlyWhatItCanDrive(unittest.TestCase):

    def test_only_agent_or_either_scenarios_are_attempted(self):
        text = command_text()
        self.assertIn("`agent`", text)
        self.assertIn("`either`", text)
        self.assertIn("awaiting human", phrases())

    def test_drivability_is_judged_from_its_own_session(self):
        text = phrases()
        self.assertIn("the tools available in this session", text)
        self.assertIn("state which tools you relied on", text)

    def test_it_never_edits_code_to_make_a_scenario_pass(self):
        self.assertIn("edit code to make a scenario pass", phrases())


class EvidenceIsKeptAndNeverOverwritten(unittest.TestCase):

    def test_evidence_goes_to_a_run_stamped_folder(self):
        self.assertIn("uat/<yyyymmdd-hhmmss>/", phrases())

    def test_a_re_run_adds_rather_than_overwrites(self):
        self.assertIn("never overwrites earlier evidence", phrases())


class OnlyAnObservedPassIsTicked(unittest.TestCase):

    def test_a_tick_needs_an_observed_pass(self):
        self.assertIn("mark a uat task done that you did not observe pass", phrases())

    def test_a_tick_carries_its_evidence(self):
        self.assertIn("— evidence:", command_text())

    def test_a_human_tick_is_never_touched(self):
        self.assertIn("change a task a human already ticked", phrases())

    def test_a_pass_is_never_reverted(self):
        self.assertIn("revert a pass", phrases())

    def test_it_finds_a_task_by_its_id_not_its_wording(self):
        self.assertIn("by its `uat<n>` id, never by its wording", phrases())


class TheWriteScopeIsNarrow(unittest.TestCase):

    def test_it_changes_nothing_it_is_accepting(self):
        self.assertIn(
            "never modifies source, tests, test configuration, ci, the specification, the test plan, or "
            "the constitution",
            phrases(),
        )

    def test_only_uat_lines_of_tasks_md_are_edited(self):
        self.assertIn("other than a `[uat]` task's checkbox and evidence suffix", phrases())

    def test_it_names_its_report(self):
        self.assertIn("uat-report.md", command_text())


class SecretsAreNeverReproduced(unittest.TestCase):

    def test_transcripts_are_masked(self):
        self.assertIn("mask", phrases())

    def test_an_unsure_capture_is_withheld_and_recorded(self):
        text = phrases()
        self.assertIn("save no image", text)
        self.assertIn("record that you withheld", text)


class ItMakesNoNetworkRequestOfItsOwn(unittest.TestCase):

    def test_the_only_network_is_the_build_under_test(self):
        self.assertIn("beyond what the build under test makes", phrases())


class NonInteractiveStartsNothing(unittest.TestCase):

    def test_non_interactive_starts_and_attempts_nothing(self):
        text = phrases()
        self.assertIn("--non-interactive", text)
        self.assertIn("start nothing and attempt nothing", text)

    def test_non_interactive_is_declared_never_inferred(self):
        self.assertIn("never infer it", phrases())


class TheReportIsShapedAndHonest(unittest.TestCase):

    def test_it_names_every_outcome(self):
        text = phrases()
        for outcome in ("passed", "failed", "blocked", "awaiting human", "already done"):
            with self.subTest(outcome=outcome):
                self.assertIn(outcome, text)

    def test_it_reports_the_template_it_used(self):
        self.assertIn("report which template you used", phrases())

    def test_the_run_log_is_cumulative(self):
        self.assertIn("run log", phrases())


class ItInvokesNothing(unittest.TestCase):

    def test_it_never_invokes_another_command(self):
        self.assertIn("invoke another command", phrases())


class NoCheckboxInTheReport(unittest.TestCase):

    def test_the_shipped_template_contains_no_checkbox(self):
        self.assertIsNone(CHECKBOX.search(TEMPLATE.read_text(encoding="utf-8")))

    def test_the_inline_skeleton_contains_no_checkbox(self):
        text = command_text()
        skeleton = text[text.index("## Inline template skeleton"):]
        self.assertIsNone(CHECKBOX.search(skeleton))


class TheHooksOfferUatBeforeAPullRequest(unittest.TestCase):
    """Spec 032 FR-050 — offered after implement, ahead of create-pr, and only ever as an offer."""

    def test_uat_is_offered_after_implement(self):
        block = hooks_block().partition("after_implement:")[2]
        self.assertIn("speckit.spectra.uat", block)

    def test_uat_comes_before_create_pr(self):
        block = hooks_block().partition("after_implement:")[2]
        self.assertLess(block.index("speckit.spectra.uat"), block.index("speckit.spectra.create-pr"))

    def test_uat_has_the_lower_priority_number(self):
        block = hooks_block().partition("after_implement:")[2]
        entries = re.split(r"\n    - ", block)
        priority = {}
        for entry in entries:
            name = re.search(r"command: (\S+)", entry)
            value = re.search(r"priority: (\d+)", entry)
            if name and value:
                priority[name.group(1)] = int(value.group(1))
        self.assertLess(priority["speckit.spectra.uat"], priority["speckit.spectra.create-pr"])

    def test_every_spectra_hook_is_optional(self):
        block = hooks_block()
        self.assertNotIn("optional: false", block)
        self.assertGreaterEqual(block.count("optional: true"), 3)


if __name__ == "__main__":
    unittest.main()
