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
- **It resolves the feature only as the implement command does**, and says which one, because ticks
  against the wrong feature are undetectably wrong.
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


def flat(text: str) -> str:
    """Lowercased, whitespace collapsed — so an assertion survives a re-wrap of the prose."""
    return " ".join(text.split()).lower()


def phrases() -> str:
    return flat(command_text())


def section(heading: str) -> str:
    """One `## ` section of the command, flattened: from its heading to the next `## ` heading."""
    text = command_text()
    start = text.index(heading)
    end = text.find("\n## ", start + len(heading))
    return flat(text[start:end if end != -1 else len(text)])


def never_row(starts_with: str) -> str:
    """One row of the never-table, flattened."""
    for line in command_text().splitlines():
        if line.startswith(f"| {starts_with}"):
            return flat(line)
    raise AssertionError(f"no never-table row starts with {starts_with!r}")


STEP_1 = "## Step 1 — Resolve the feature"


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


class FeatureIsResolvedAsTheImplementCommandDoes(unittest.TestCase):
    """Spec 039 FR-001–FR-011, FR-014 — resolve as the implement command does, never otherwise."""

    def test_every_resolution_stop_starts_and_writes_nothing(self):
        self.assertIn("starts nothing and writes nothing", section(STEP_1))

    def test_it_resolves_only_as_the_implement_command_does(self):
        text = phrases()
        self.assertIn("resolve only as the implement command does", text)
        for source in ("branch", "modification time", "listing of `specs/`"):
            with self.subTest(source=source):
                self.assertIn(source, text)

    def test_it_offers_no_picker(self):
        self.assertIn("do not offer a list", phrases())

    def test_it_stops_when_the_feature_is_outside_the_project(self):
        self.assertIn("out-of-project", phrases())

    def test_the_sources_are_consulted_in_the_implement_commands_order(self):
        step = section(STEP_1)
        positions = [step.index(name) for name in
                     ("specify_init_dir", "specify_feature_directory", ".specify/feature.json")]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("nearest directory", step)
        self.assertIn(".specify/", step)

    def test_an_empty_variable_is_unset(self):
        step = section(STEP_1)
        self.assertIn("set but empty", step)
        self.assertIn("unset", step)

    def test_it_accepts_against_the_tasks_in_the_feature_directory(self):
        self.assertIn("`tasks.md` in the feature directory", section(STEP_1))

    def test_resolution_is_read_only(self):
        step = section(STEP_1)
        self.assertIn("never writes `.specify/feature.json`", step)
        self.assertIn("never creates the feature directory", step)

    def test_the_invoking_project_bounds_the_out_of_project_stop(self):
        step = section(STEP_1)
        self.assertIn("the invoking project is the nearest directory containing `.specify/`", step)
        self.assertIn("regardless of `specify_init_dir`", step)
        text = command_text()
        stop = flat(text[text.index("### The out-of-project stop"):text.index("## Step 2 —")])
        self.assertIn("the invoking project (step 1)", stop)

    def test_the_governing_rule_names_the_implement_command(self):
        rule = section("## The one rule that governs everything")
        self.assertIn("resolved exactly as the implement command resolves it", rule)

    def test_the_intro_no_longer_says_someone_hands_you_a_feature(self):
        text = command_text()
        self.assertNotIn("someone hands you a feature", flat(text[:text.index("## The one rule")]))

    def test_every_resolution_stop_is_in_the_table(self):
        step = section(STEP_1)
        for phrase in ("the shell read is denied or fails", "names no existing directory", "neither source",
                       "cannot be parsed", "does not exist", "has no `tasks.md`"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, step)

    def test_it_never_falls_back_to_the_feature_record_alone(self):
        self.assertIn("never fall back to `.specify/feature.json` alone", phrases())

    def test_every_stop_shows_the_one_remedy_block(self):
        step = section(STEP_1)
        self.assertIn("to choose the feature without uat writing anything", step)
        self.assertIn("for this session — set specify_feature_directory=", step)
        self.assertIn('for good — set "feature_directory" in .specify/feature.json', step)
        self.assertIn("to create a new feature, run the specify command", step)

    def test_step_one_counts_its_own_outcomes(self):
        text = command_text()
        step = text[text.index(STEP_1):text.index("### An argument only confirms")]
        stated = re.search(r"(\w+) outcomes:", step).group(1).lower()
        words = {"six": 6, "seven": 7, "eight": 8, "nine": 9}
        rows = [line for line in step.splitlines() if line.startswith("| ") and not line.startswith("| Input")]
        self.assertEqual(words[stated], len(rows), f"Step 1 says {stated} outcomes but lists {len(rows)}")


class TheEnvironmentReadStartsNothing(unittest.TestCase):
    """Spec 039 FR-006, FR-007, FR-017a — one read, before the confirmation, that starts nothing."""

    def test_exactly_one_read_in_both_shells(self):
        step = section(STEP_1)
        for phrase in ("exactly one shell read", "once per run", "specify_init_dir",
                       "specify_feature_directory", "posix", "powershell"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, step)

    def test_the_never_table_says_the_read_starts_nothing(self):
        row = never_row("Start a build, a server, or any process before the run confirmation")
        self.assertIn("the one shell read in step 1", row)
        self.assertIn("starts nothing", row)

    def test_the_feature_is_fixed_for_the_run(self):
        step = section(STEP_1)
        self.assertIn("reused for the whole run", step)
        self.assertIn("never read `.specify/feature.json` again", step)

    def test_the_read_is_recorded_as_an_input(self):
        self.assertIn("record the read as an input", section(STEP_1))

    def test_the_environment_read_is_recorded_as_a_source(self):
        self.assertIn("the environment read", section("## Step 2 —"))
        text = command_text()
        skeleton = text[text.index("## Inline template skeleton"):]
        line = next(l for l in skeleton.splitlines() if l.startswith("## Sources consulted and coverage"))
        self.assertIn("environment read", line)


class AnArgumentOnlyConfirms(unittest.TestCase):
    """Spec 039 FR-012, FR-013 — a path confirms the resolved feature; it never chooses one."""

    def test_it_matches_the_directory_or_its_spec(self):
        step = section(STEP_1)
        self.assertIn("the feature directory or its `spec.md`", step)
        self.assertIn("trailing slash", step)

    def test_any_other_path_stops_before_anything_is_read(self):
        step = section(STEP_1)
        self.assertIn("any other path", step)
        self.assertIn("stop before reading anything else", step)
        self.assertIn("the argument's path, the resolved directory, and its source", step)

    def test_an_argument_never_replaces_resolution(self):
        step = section(STEP_1)
        self.assertIn("an argument is never used in place of", step)
        self.assertIn("when no feature resolves", step)
        self.assertIn("names the argument's path and the reason", step)

    def test_options_are_removed_first(self):
        self.assertIn("after `--env` and `--non-interactive` are removed", section(STEP_1))

    def test_options_never_become_the_path(self):
        user_input = section("## User Input")
        self.assertIn("`--env <name-or-url>`", user_input)
        self.assertIn("never silently becomes part of the path", user_input)


class TheResolutionIsAnnounced(unittest.TestCase):
    """Spec 039 FR-015–FR-017 — visible first, at the moment of consent, and in the record."""

    def test_it_is_the_first_thing_said(self):
        step = section(STEP_1)
        self.assertIn("the first thing you say", step)
        self.assertIn("feature: specs/", step)
        self.assertIn("(from .specify/feature.json)", step)
        self.assertIn("; .specify/feature.json names", step)

    def test_non_interactive_announces_first(self):
        self.assertIn("the non-interactive announcement comes first", section(STEP_1))
        self.assertIn("before the feature line in step 1", section("## Non-interactive mode"))

    def test_the_run_confirmation_names_the_feature(self):
        self.assertIn("the feature directory whose `tasks.md` will be ticked", section("## Step 3 —"))

    def test_the_report_records_the_source(self):
        self.assertIn("resolved from", section("## Step 8 —"))

    def test_the_session_report_names_the_feature(self):
        step = section("## Step 9 —")
        self.assertIn("**feature**", step)
        self.assertIn("the source it was resolved from", step)

    def test_the_skeleton_names_where_it_was_resolved_from(self):
        text = command_text()
        self.assertIn("where it was resolved from", flat(text[text.index("## Inline template skeleton"):]))

    def test_the_template_is_unchanged(self):
        self.assertIn("| **Feature** | [project-relative path to the feature directory] |",
                      TEMPLATE.read_text(encoding="utf-8"))


class NoStaleProse(unittest.TestCase):
    """Spec 039 FR-019–FR-022 — every surface describes the new rule, with the no-argument form first."""

    def test_the_front_matter_and_manifest_drop_the_old_rule(self):
        front = flat(command_text().split("---")[1])
        manifest = MANIFEST.read_text(encoding="utf-8")
        entry = manifest[manifest.index(f'name: "{COMMAND_NAME}"'):]
        description = flat(entry[entry.index("description:"):entry.index("\n", entry.index("description:"))])
        for text in (front, description):
            with self.subTest(text=text[:40]):
                self.assertNotIn("required", text)
                self.assertNotIn("never inferred", text)
                self.assertIn("the way the implement command does", text)

    def test_the_command_drops_the_old_rule(self):
        text = phrases()
        self.assertNotIn("never infer which feature was meant", text)
        self.assertNotIn("the feature is required", text)

    def test_the_docs_drop_the_exact_stale_strings(self):
        agents = h.repo_file("AGENTS_LIST.md").read_text(encoding="utf-8")
        block = agents[agents.index("<!-- SPECTRA:AGENT id=uat -->"):]
        block = block[:block.index("<!-- SPECTRA:AGENT", 10)]
        readme = h.repo_file("spectra", "README.md").read_text(encoding="utf-8")
        readme = readme[readme.index("## `speckit.spectra.uat`"):]
        readme = readme[:readme.index("\n## ", 5)]
        card = self.uat_card()
        for name, text, stale in (
            ("AGENTS_LIST.md", block, "**required**, and never inferred"),
            ("spectra/README.md", readme, "The feature is required."),
            ("docs/getting-started/agents.html", card, "<b>required</b> — never inferred"),
        ):
            with self.subTest(file=name):
                self.assertNotIn(flat(stale), flat(text))

    def test_the_card_shows_the_no_argument_form_first(self):
        first = re.search(r"<pre><code>(.*?)</code></pre>", self.uat_card()).group(1)
        self.assertEqual(first.strip(), "/speckit-spectra-uat")

    def test_the_after_implement_prompt_names_no_path(self):
        block = hooks_block().partition("after_implement:")[2]
        entry = block[block.index("speckit.spectra.uat"):]
        prompt = entry[entry.index("prompt:"):entry.index("\n", entry.index("prompt:"))]
        self.assertNotIn("specs/", prompt)
        self.assertNotIn("SPEC_FILE", prompt)

    @staticmethod
    def uat_card() -> str:
        html = h.repo_file("docs", "getting-started", "agents.html").read_text(encoding="utf-8")
        start = html.index('<span class="name">speckit.spectra.uat</span>')
        return html[start:html.index("</li>", start)]


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

    def test_a_feature_that_does_not_resolve_still_stops(self):
        text = phrases()
        self.assertIn("a feature that does not resolve still stops", text)
        self.assertNotIn("a missing feature still stops", text)


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
