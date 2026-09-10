"""The `test-strategy` flow, asserted against the command text that ships.

A command file is a prompt: its text *is* the implementation, so the enforceable surface is what it
says. These assertions cannot prove an agent behaves correctly at run time — that is the manual pass in
`test/README.md`. What they prove is that the rules it is supposed to follow have not been quietly
deleted, which is the regression that actually happens to prompt files.

This agent is the fourth Spectra document producer, so Principles VII and VIII are already enforced for
it by `test_doc_output_paths.py` and `test_document_templates.py`; nothing here duplicates those. What
is left is the part that makes a testing strategy trustworthy rather than merely plausible, and every
one of these rules is the kind a well-meaning edit removes without anyone noticing:

- **It never writes the constitution.** This is the one an agent will violate with good intentions: the
  user just approved the amendment, the file is right there, and applying it is *helpful*. Spec 020
  settled the applier as `/speckit-constitution` so one command owns the sync impact report, the
  bump-type judgement, and dependent-artifact propagation. Losing this rule puts a second, partial
  implementation of the amendment procedure in a command that is not about governance — and its failure
  mode is a subtly malformed constitution, not an obviously broken one.
- **A brownfield floor never exceeds the baseline.** Remove this and the command ships a document whose
  adoption breaks the project's next build. A floor that fails immediately gets deleted, which leaves
  the project worse off than if none had been proposed.
- **A baseline always carries its provenance.** `measured` means the tool ran this session; `reported`
  means a file was read, and then the date is mandatory. Collapse the distinction and the floor rests on
  a number nobody can date.
- **No tool is named that the stack cannot run.** This is what stops a browser driver being recommended
  to a command-line tool — the single most visible way a generated strategy loses a reader's trust.
- **Every recommendation cites evidence or is marked a convention.** Never neither. Unmarked, unevidenced
  advice is indistinguishable from a template fill-in.
- **It runs nothing without an explicit confirmation.** An unbidden coverage run is the largest side
  effect a foundation agent could have.

Standard library only, like the rest of the suite.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import helpers as h  # noqa: E402

COMMAND = h.repo_file("spectra", "commands", "test-strategy.md")
TEMPLATE = h.repo_file("spectra", "templates", "test-strategy-template.md")
MANIFEST = h.repo_file("spectra", "extension.yml")

COMMAND_NAME = "speckit.spectra.test-strategy"
CONSTITUTION_PATH = ".specify/memory/constitution.md"


def command_text() -> str:
    return COMMAND.read_text(encoding="utf-8")


class TheCommandIsRegistered(unittest.TestCase):
    """Identity, before anything about behaviour."""

    def test_the_command_file_exists(self):
        self.assertTrue(COMMAND.is_file(), f"{COMMAND} does not exist")

    def test_the_manifest_registers_it(self):
        text = MANIFEST.read_text(encoding="utf-8")
        self.assertIn(f'- name: "{COMMAND_NAME}"', text)
        self.assertIn('file: "commands/test-strategy.md"', text)

    def test_it_has_front_matter_with_a_description(self):
        text = command_text()
        self.assertTrue(text.startswith("---\n"), "no YAML front matter")
        front = text.split("---\n", 2)[1]
        self.assertIn("description:", front)

    def test_it_takes_input_through_the_generic_placeholder(self):
        """Principle III: no agent's invocation syntax in the command's own input surface."""
        self.assertIn("$ARGUMENTS", command_text())

    def test_it_runs_with_no_arguments(self):
        text = command_text().lower()
        self.assertIn("requires no arguments", text)


class TheConstitutionIsNeverWritten(unittest.TestCase):
    """Spec 020 FR-032 — the invariant the whole approval design rests on."""

    def test_it_states_that_it_never_writes_the_constitution(self):
        text = command_text().lower()
        self.assertIn(CONSTITUTION_PATH.lower(), text)
        self.assertTrue(
            "never write" in text or "never writes" in text,
            "test-strategy.md no longer states that it never writes the constitution",
        )

    def test_the_ban_is_unconditional(self):
        """Approval is the case that tempts an agent, so the text has to name it explicitly."""
        text = command_text().lower()
        self.assertIn("approved or not", text)
        self.assertIn("not on approval", text)

    def test_it_hands_off_rather_than_applying(self):
        text = command_text()
        self.assertIn("/speckit-constitution", text)
        self.assertIn("Do not invoke it", text)

    def test_it_does_not_create_a_constitution_either(self):
        text = command_text().lower()
        self.assertIn("create a constitution", text)

    def test_the_manifest_advertises_the_ban(self):
        """A consumer reading only the catalog must be able to see it."""
        text = MANIFEST.read_text(encoding="utf-8")
        entry = text.split(f'- name: "{COMMAND_NAME}"', 1)[1].split("- name:", 1)[0]
        self.assertIn("never writes the constitution", entry)


class TheCoverageFloorIsHoldable(unittest.TestCase):
    """FR-022, FR-023, FR-024, FR-026 — the numbers a team will actually enforce."""

    def test_the_floor_never_exceeds_the_baseline(self):
        text = command_text().lower()
        self.assertIn("at or below the baseline", text)

    def test_it_says_why_an_unholdable_floor_is_worse_than_none(self):
        text = command_text().lower()
        self.assertIn("gets deleted", text)

    def test_all_three_provenances_are_named(self):
        text = command_text()
        for provenance in ("measured", "reported", "unavailable"):
            with self.subTest(provenance=provenance):
                self.assertIn(f"`{provenance}`", text)

    def test_a_figure_read_from_a_file_is_never_called_measured(self):
        text = command_text()
        self.assertIn("A figure read from a file is `reported`", text)

    def test_a_reported_figure_carries_its_date(self):
        text = command_text().lower()
        self.assertIn("with its date", text)

    def test_an_unavailable_baseline_makes_the_floor_conditional(self):
        text = command_text().lower()
        self.assertIn("conditional", text)

    def test_it_forbids_inferring_a_figure(self):
        """A test-file-to-source-file ratio is the plausible-looking number to refuse."""
        text = command_text().lower()
        self.assertIn("never infer a figure", text)

    def test_the_ratchet_uses_triggers_not_dates(self):
        text = command_text()
        self.assertIn("Never as dates", text)
        self.assertIn("Do not state a schedule", text)

    def test_surfaces_with_different_baselines_get_their_own_floors(self):
        text = command_text().lower()
        self.assertIn("its own floor", text)


class ToolsAreGroundedInTheProject(unittest.TestCase):
    """FR-016, FR-017 — the rules that stop a browser driver reaching a CLI."""

    def test_the_three_tiers_are_named(self):
        text = command_text()
        for tier in ("present", "ecosystem-standard", "unverified"):
            with self.subTest(tier=tier):
                self.assertIn(f"**{tier}**", text)

    def test_an_unrunnable_tool_appears_at_no_tier(self):
        text = command_text()
        self.assertIn("appears at no tier", text)

    def test_the_end_to_end_surface_set_is_closed(self):
        text = command_text().lower()
        for surface in ("browser", "http", "cli", "none"):
            with self.subTest(surface=surface):
                self.assertIn(surface, text)

    def test_it_never_defaults_to_a_browser_driver(self):
        text = command_text()
        self.assertIn("Never default to a browser driver", text)

    def test_no_named_browser_driver_is_hard_coded_as_the_answer(self):
        """FR-017, enforced as a blanket ban on naming one in the prompt at all.

        The tier rule in Step 6 already derives the right driver for a project that has a browser: it
        will be sitting in a manifest (tier `present`) or be the conventional choice for a stack the
        project demonstrably uses (tier `ecosystem-standard`). Naming one *here* adds nothing to that
        and costs a great deal — a tool named in the prompt is the one an agent reaches for, which is
        exactly how a browser driver ends up recommended to a command-line tool.
        """
        text = command_text()
        for tool in ("Playwright", "Cypress", "Selenium", "Puppeteer"):
            with self.subTest(tool=tool):
                self.assertNotIn(
                    tool,
                    text,
                    f"test-strategy.md names {tool}; the end-to-end approach must be derived from "
                    "the project's own surface, not hard-coded into the prompt",
                )


class EveryRecommendationIsTraceable(unittest.TestCase):
    """FR-043, FR-044 — the difference between a strategy and a template fill-in."""

    def test_evidence_or_a_convention_marker_never_neither(self):
        text = command_text().lower()
        self.assertIn("convention-based default with no project evidence", text)
        self.assertIn("neither is a defect", text)

    def test_an_absence_claim_cites_what_was_searched(self):
        text = command_text().lower()
        self.assertIn("cite what you searched for and where", text)


class TheRunIsHonestAboutItself(unittest.TestCase):
    """FR-006, FR-013, FR-045 — what a reader needs to judge the document."""

    def test_the_mode_is_classified_from_signals(self):
        text = command_text().lower()
        for mode in ("greenfield", "brownfield", "mixed"):
            with self.subTest(mode=mode):
                self.assertIn(mode, text)

    def test_the_mode_is_never_asked_of_the_user(self):
        text = command_text()
        self.assertIn("Never ask the user", text)

    def test_classification_ignores_age_and_commit_count(self):
        text = command_text().lower()
        self.assertIn("repository age", text)
        self.assertIn("commit count", text)

    def test_it_states_its_own_coverage(self):
        text = command_text().lower()
        self.assertIn("checked and found nothing", text)
        self.assertIn("did not check", text)

    def test_reduced_search_capability_degrades_loudly(self):
        text = command_text()
        self.assertIn("Do not silently narrow", text)


class TheWriteScopeIsNarrow(unittest.TestCase):
    """FR-037, FR-047, FR-048, FR-049, FR-050 — one file, and nothing else."""

    def test_exactly_one_file_is_written(self):
        text = command_text()
        self.assertIn("exactly one file", text)

    def test_a_rerun_rewrites_in_place(self):
        text = command_text()
        self.assertIn("Rewrite the same file in place", text)
        self.assertIn("Never create a second strategy file", text)

    def test_it_never_edits_configuration_or_ci(self):
        text = command_text().lower()
        self.assertIn("coverage configuration", text)
        self.assertIn("ci workflow definitions", text)

    def test_it_states_the_change_instead_of_applying_it(self):
        text = command_text()
        self.assertIn("State it; do not apply it", text)

    def test_it_makes_no_network_request(self):
        text = command_text().lower()
        self.assertIn("no network request", text)

    def test_it_accepts_no_url_or_credential(self):
        text = command_text().lower()
        self.assertIn("repository url, credential, or token", text)

    def test_it_defers_flaky_tests_to_the_agent_that_owns_them(self):
        text = command_text()
        self.assertIn("speckit.spectra.flaky-test-detector", text)

    def test_it_runs_nothing_by_default(self):
        text = command_text()
        self.assertIn("You run nothing by default", text)


class TheReportPrecedesTheGate(unittest.TestCase):
    """FR-028, FR-031, FR-034 — a gate offered before the summary is not a gate."""

    def test_the_summary_comes_before_any_question(self):
        text = command_text()
        self.assertIn("Before you ask the user anything", text)

    def test_the_report_step_precedes_the_constitution_step(self):
        text = command_text()
        report = text.find("## Step 10 — Report")
        check = text.find("## Step 11 — Check the constitution")
        gate = text.find("## Step 12 — The amendment gate")
        self.assertNotEqual(-1, report)
        self.assertLess(report, check)
        self.assertLess(check, gate)

    def test_the_amendment_text_is_shown_before_the_choice(self):
        text = command_text()
        self.assertIn("Show the exact amendment text first", text)

    def test_all_three_paths_are_offered(self):
        text = command_text()
        for path in ("Approve it", "Modify the strategy first", "Talk it through"):
            with self.subTest(path=path):
                self.assertIn(path, text)

    def test_the_three_embedded_states_are_named(self):
        text = command_text()
        for state in ("**embedded**", "**partial**", "**absent**"):
            with self.subTest(state=state):
                self.assertIn(state, text)

    def test_the_embedded_check_is_semantic_not_a_string_match(self):
        text = command_text().lower()
        self.assertIn("never** match on the string", text)

    def test_a_conflicting_principle_is_surfaced_not_overridden(self):
        text = command_text().lower()
        self.assertIn("silently overrides an existing principle", text)

    def test_non_interactive_infers_no_approval(self):
        text = command_text().lower()
        self.assertIn("infer no approval from silence", text)


class TheFourLensesAreMandatory(unittest.TestCase):
    """FR-014, FR-020 — a lens that does not apply says so."""

    def test_all_four_lenses_are_named(self):
        text = command_text()
        for lens in ("Unit", "Integration", "API contract", "End-to-end"):
            with self.subTest(lens=lens):
                self.assertIn(lens, text)

    def test_a_lens_is_applicable_or_carries_a_reason(self):
        text = command_text()
        self.assertIn("Never omit a lens", text)

    def test_each_lens_states_what_it_proves_and_its_boundary(self):
        text = command_text()
        self.assertIn("Proves", text)
        self.assertIn("boundary", text.lower())

    def test_brownfield_reports_before_it_proposes(self):
        text = command_text()
        self.assertIn("report what exists before proposing anything", text)


class TheShippedTemplateMatchesTheDocumentedSections(unittest.TestCase):
    """The template ships structure only; the rules above stay in the command."""

    SECTION = re.compile(r"^## +(.+?)\s*$", re.M)

    def test_the_template_declares_the_ten_sections(self):
        names = self.SECTION.findall(TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual(
            names,
            [
                "Classification and evidence",
                "Testable surfaces",
                "Unit testing",
                "Integration testing",
                "API contract testing",
                "End-to-end testing",
                "Coverage floor",
                "Recommendations summary",
                "Proposed constitution amendment",
                "Sources consulted and coverage of analysis",
            ],
        )

    def test_the_template_carries_no_honesty_rule(self):
        """Principle VIII: an override may drop a section, never a rule."""
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertNotIn("at or below the baseline", text)
        self.assertNotIn("appears at no tier", text)

    def test_the_template_says_which_rules_it_cannot_change(self):
        text = TEMPLATE.read_text(encoding="utf-8").lower()
        self.assertIn("cannot change", text)


if __name__ == "__main__":
    unittest.main()
