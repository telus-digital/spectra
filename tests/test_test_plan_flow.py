"""The `test-plan` flow, asserted against the command text that ships.

A command file is a prompt: its text *is* the implementation, so the enforceable surface is what it
says. These assertions cannot prove an agent behaves correctly at run time — that is the manual pass in
`test/README.md`. What they prove is that the rules it is supposed to follow have not been quietly
deleted, which is the regression that actually happens to prompt files.

This agent is the fifth Spectra document producer but the **first that is not an artifact-root document
agent**: it writes beside the specification it was handed. So Principle VIII is enforced for it by
`test_document_templates.py` as usual, while Principle VII's module carries a *negative* assertion
instead of an entry — see `TheOutputIsNotAnArtifactRootDocument` in `test_doc_output_paths.py`.

What is left is the part that makes a test plan trustworthy rather than merely plausible, and every one
of these rules is the kind a well-meaning edit removes without anyone noticing:

- **It never infers which specification was meant.** This is the one an agent will violate with good
  intentions: the branch name is right there, `.specify/feature.json` is right there, and resolving it
  is *helpful*. Spec 021 refused all of it because the output is circulated and signed — a plan built
  against the wrong specification reads as authoritative and is undetectably wrong to whoever approves
  it. The failure mode is not an error message; it is a confidently wrong signed document.
- **Traceability runs both ways.** Every acceptance criterion reaches a condition or the not-covered
  list; every condition names what it verifies. Remove either half and the document still looks
  complete — forward-only produces conditions verifying nothing anyone asked for, backward-only
  produces silent gaps.
- **It never invents a decision the specification does not contain.** A fabricated condition for an
  ambiguous requirement is strictly worse than a stated gap, because it launders a guess into something
  a stakeholder approves.
- **No checkbox, anywhere, from any template layer.** The one invariant here that can be pinned by exact
  match rather than inferred from prose, so it is asserted on the artifacts themselves.
- **It runs nothing.** Existing coverage is read from test source. An unbidden test run on a stranger's
  repository is unbounded in time and may reach the network.
- **The handoff is printed, never invoked, and never a hook.** A hook would make every project that
  installs the extension prompt for a test plan on every feature, which is the opposite of the opt-in
  add-on this is.

Standard library only, like the rest of the suite.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import helpers as h  # noqa: E402

COMMAND = h.repo_file("spectra", "commands", "test-plan.md")
TEMPLATE = h.repo_file("spectra", "templates", "test-plan-template.md")
MANIFEST = h.repo_file("spectra", "extension.yml")
EXTENSIONS_YML = h.repo_file(".specify", "extensions.yml")

COMMAND_NAME = "speckit.spectra.test-plan"
OUTPUT_NAME = "test-plan.md"

# A Markdown checkbox is a list bullet followed by a bracketed space or x, at the start of a line.
# Anchored deliberately: the command has to *name* the construct it forbids, and an inline mention
# inside backticks mid-sentence is a reference, not a checkbox. Only a line-initial bullet renders as
# one, and that is the thing that must never appear.
CHECKBOX = re.compile(r"^[ \t]*[-*][ \t]\[[ xX]\]", re.M)

# The sources of truth a command must never quietly start consulting to resolve its argument.
INFERENCE_SOURCES = ("branch", "feature.json", "modification time")


def command_text() -> str:
    return COMMAND.read_text(encoding="utf-8")


def flat(text: str) -> str:
    """Lowercased, with every run of whitespace collapsed to one space.

    The command file is hard-wrapped prose, so any phrase long enough to be worth asserting on will
    eventually straddle a line break — and an assertion that breaks when a paragraph is re-flowed is a
    test that punishes formatting instead of guarding behaviour. Normalizing first means these
    assertions survive a re-wrap and still fail when the rule is deleted.
    """
    return " ".join(text.split()).lower()


def phrases() -> str:
    return flat(command_text())


class TheCommandIsRegistered(unittest.TestCase):
    """Identity, before anything about behaviour."""

    def test_the_command_file_exists(self):
        self.assertTrue(COMMAND.is_file(), f"{COMMAND} does not exist")

    def test_the_manifest_registers_it(self):
        text = MANIFEST.read_text(encoding="utf-8")
        self.assertIn(f'- name: "{COMMAND_NAME}"', text)
        self.assertIn('file: "commands/test-plan.md"', text)

    def test_it_has_front_matter_with_a_description(self):
        text = command_text()
        self.assertTrue(text.startswith("---\n"), "no YAML front matter")
        front = text.split("---\n", 2)[1]
        self.assertIn("description:", front)

    def test_it_takes_input_through_the_generic_placeholder(self):
        """Principle III: no agent's invocation syntax in the command's own input surface."""
        self.assertIn("$ARGUMENTS", command_text())


class TheSpecificationArgumentIsRequired(unittest.TestCase):
    """Spec 021 FR-007 to FR-009 — the gate, and the refusal to be helpful past it."""

    def test_it_states_the_argument_is_required(self):
        text = phrases()
        self.assertIn("required", text)
        self.assertTrue(
            "is required" in text,
            "the command no longer states that its argument is required",
        )

    def test_an_empty_argument_stops_without_reading_or_writing(self):
        text = phrases()
        self.assertIn("if no path was supplied", text)
        self.assertTrue(
            "read nothing, analyze nothing, write nothing" in text,
            "the empty-argument path no longer states that it reads and writes nothing; FR-009 "
            "requires the gate to fire before any project analysis",
        )

    def test_it_refuses_to_infer_the_specification(self):
        """FR-008. The rule an agent breaks with good intentions."""
        text = phrases()
        self.assertIn("never infer which specification", text)
        for source in INFERENCE_SOURCES:
            with self.subTest(source=source):
                self.assertIn(
                    source,
                    text,
                    f"the inference prohibition no longer names {source!r} as something it must not "
                    "consult; an unnamed source is one a future edit will treat as permitted",
                )

    def test_it_refuses_to_offer_a_picker(self):
        """A list the command assembled is the same failure with extra steps."""
        text = phrases()
        self.assertTrue(
            "do not offer a list" in text or "offering a picker" in text,
            "the command no longer rules out listing the specifications it can see",
        )

    def test_it_resolves_a_directory_to_the_spec_inside_it(self):
        text = phrases()
        self.assertIn("a directory containing exactly one", text)

    def test_it_does_not_choose_between_ambiguous_candidates(self):
        self.assertIn("Do not choose", command_text())

    def test_it_stops_when_the_specification_is_outside_the_project(self):
        """FR-022 — the guard that replaces a fixed output folder's write-scope protection."""
        text = phrases()
        self.assertIn("out-of-project", text)
        self.assertTrue(
            "stop before writing" in text,
            "the out-of-project path no longer stops before writing",
        )


class TraceabilityRunsBothWays(unittest.TestCase):
    """FR-023 to FR-025 — the invariant that is the product."""

    def test_every_acceptance_criterion_reaches_a_condition_or_an_uncovered_item(self):
        text = phrases()
        self.assertTrue(
            "never neither" in text,
            "the forward half of the traceability invariant is gone; a criterion absent from both the "
            "conditions table and the not-covered list is the defect this command exists to prevent, "
            "and the document looks complete while it is wrong",
        )

    def test_every_condition_names_what_it_verifies(self):
        text = phrases()
        self.assertIn("verifies", text)
        self.assertTrue(
            "the specification's own identifier" in text or "specification's own identifier" in text,
            "the backward half of the invariant is gone; conditions that trace to nothing verify "
            "nothing anyone asked for",
        )

    def test_it_never_mints_an_identifier(self):
        self.assertIn("never mint an identifier", command_text())

    def test_it_composes_a_story_reference_rather_than_using_a_bare_one(self):
        """Acceptance scenarios are numbered per story, so a bare AC number is ambiguous."""
        self.assertIn("US2-AC1", command_text())

    def test_it_reports_the_covered_count(self):
        text = phrases()
        self.assertTrue(
            "covered out of" in text,
            "the run no longer reports criteria covered out of criteria found; without the count, a "
            "missing criterion is invisible",
        )


class AmbiguityIsReportedNeverResolved(unittest.TestCase):
    """FR-026, FR-027 — the rule that feels unhelpful and is not negotiable."""

    def test_it_never_invents_the_missing_decision(self):
        self.assertIn("Never invent the missing decision", command_text())

    def test_it_names_the_four_uncovered_reasons(self):
        text = phrases()
        for reason in ("unresolved clarification", "untestable as written", "out of scope", "deferred"):
            with self.subTest(reason=reason):
                self.assertIn(reason, text)

    def test_an_unresolved_marker_names_the_clarification_command(self):
        text = phrases()
        self.assertIn("clarification command", text)


class AbsenceIsAlwaysCited(unittest.TestCase):
    """FR-028, FR-029 — two different claims, two different duties."""

    def test_a_coverage_claim_cites_a_test_file(self):
        text = phrases()
        self.assertIn("cite the **test file**".lower(), text)

    def test_an_absence_claim_cites_the_search(self):
        text = phrases()
        self.assertIn("cite the **search**".lower(), text)

    def test_it_shows_the_permitted_and_forbidden_phrasings(self):
        text = phrases()
        self.assertIn("not permitted", text)
        self.assertTrue(
            "that is a claim about the system" in text,
            "the command no longer distinguishes a fact about a search from a claim about the system",
        )


class NoCheckboxAnywhere(unittest.TestCase):
    """FR-041, FR-042 — asserted on the artifacts, not inferred from the prose.

    This is the only rule in the feature that can be pinned by exact match with no false positives,
    which is why it is checked on the files themselves rather than only on what the command says about
    them. A checkbox reaching the output turns an approval document into a second progress tracker that
    will disagree with tasks.md.
    """

    def test_the_shipped_template_contains_no_checkbox(self):
        found = CHECKBOX.findall(TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual(
            [], found,
            f"{TEMPLATE.name} contains a checkbox construct; spec 021 FR-041 makes this document an "
            "approval artifact rather than a tracker, exit criteria included",
        )

    def test_the_inline_skeleton_contains_no_checkbox(self):
        _, _, tail = command_text().partition("Inline template skeleton")
        fences = re.findall(r"```(?:markdown)?\n(.*?)```", tail, re.S)
        self.assertTrue(fences, "the command has no inline template skeleton")
        self.assertEqual(
            [], CHECKBOX.findall(fences[0]),
            "the inline skeleton contains a checkbox construct; a project with no .specify/ would get "
            "a document the rule forbids",
        )

    def test_the_command_file_itself_ships_no_checkbox(self):
        self.assertEqual(
            [], CHECKBOX.findall(command_text()),
            "the command file contains a line-initial checkbox; the construct it forbids must be "
            "described, not reproduced",
        )

    def test_it_states_the_prohibition(self):
        text = phrases()
        self.assertIn("emit a checkbox, in any section", text)

    def test_it_converts_rather_than_honours_a_checkbox_from_a_template_layer(self):
        text = phrases()
        self.assertTrue(
            "rendered as a **plain statement**".lower() in text,
            "the command no longer converts a checkbox found in a resolved template layer; either it "
            "honours one (producing a tracker) or refuses the run (making a formatting choice fatal)",
        )

    def test_it_forbids_a_tracking_field(self):
        text = phrases()
        self.assertIn("status, progress, or completion field", text)


class TheVocabularyIsInherited(unittest.TestCase):
    """FR-013, FR-035, FR-036 — the project's own words win."""

    def test_it_looks_for_the_strategy_document(self):
        self.assertIn("docs/test-strategy/TEST_STRATEGY.md", command_text())

    def test_it_resolves_the_declared_artifact_root_to_find_it(self):
        self.assertIn("Artifact root:", command_text())

    def test_the_root_resolution_is_read_only(self):
        """R5: three write-time obligations deliberately do not apply to a lookup."""
        text = phrases()
        self.assertIn("this resolution is read-only", text)

    def test_it_takes_the_strategy_lens_names_verbatim(self):
        text = phrases()
        self.assertIn("verbatim", text)
        self.assertTrue(
            "not normalized" in text,
            "the command no longer forbids normalizing the project's lens names; a silent translation "
            "sits between two documents a reviewer reads side by side",
        )

    def test_the_default_vocabulary_is_stated(self):
        text = command_text()
        for level in ("`unit`", "`integration`", "`api-contract`", "`end-to-end`", "`manual`"):
            with self.subTest(level=level):
                self.assertIn(level, text)

    def test_manual_survives_an_inherited_vocabulary(self):
        text = phrases()
        self.assertIn("is always available", text)

    def test_the_constitution_outranks_the_strategy(self):
        text = phrases()
        self.assertIn("the constitution prevails", text)

    def test_an_absent_strategy_is_stated_and_the_run_continues(self):
        text = phrases()
        self.assertTrue(
            "neither is a precondition" in text,
            "the command no longer works without a strategy document; FR-014 keeps an optional add-on "
            "from becoming a prerequisite chain",
        )

    def test_the_coverage_floor_is_inherited_never_proposed(self):
        text = phrases()
        self.assertIn("inherited, never proposed", text)


class NoUnrunnableLevelOrTool(unittest.TestCase):
    """FR-037 — the plausibility failure, one phase later than test-strategy's."""

    def test_it_reads_the_surfaces_from_the_manifests(self):
        text = phrases()
        self.assertIn("dependency manifests", text)

    def test_an_unsupported_surface_makes_a_level_unreachable(self):
        text = phrases()
        self.assertTrue(
            "unreachable" in text,
            "the command no longer rules out a level the project cannot run; 'discouraged' is what "
            "lets a browser driver reach a command-line tool",
        )

    def test_it_names_the_browser_case_explicitly(self):
        text = phrases()
        self.assertIn("no browser anywhere in the manifests", text)


class ItRunsNothing(unittest.TestCase):
    """FR-020, research R9 — flaky-test-detector's posture, not test-strategy's."""

    def test_it_states_that_nothing_is_executed(self):
        text = phrases()
        self.assertIn("nothing is executed", text)

    def test_it_reads_test_source_instead(self):
        self.assertIn("Read test source. Never run it", command_text())

    def test_it_forbids_running_building_or_installing(self):
        text = phrases()
        self.assertIn("run, build, or install anything", text)

    def test_it_explains_why_a_coverage_tool_answers_the_wrong_question(self):
        text = phrases()
        self.assertIn("repository-level question", text)


class TheWriteScopeIsOneFile(unittest.TestCase):
    """FR-018 to FR-021 — the narrowest write scope on the roster."""

    def test_it_names_its_output_file(self):
        self.assertIn(OUTPUT_NAME, command_text())

    def test_it_writes_exactly_one_file(self):
        text = phrases()
        self.assertIn("exactly one file", text)

    def test_it_never_modifies_the_specification_it_read(self):
        text = phrases()
        self.assertIn("modify the specification you read", text)

    def test_the_output_carries_no_sequence_number(self):
        """FR-021: the identity is the feature directory, not a number scoped to a folder."""
        text = command_text()
        numbered = re.compile(r"(?:NNN|\d{3})[-_]test-plan\.md|test-plan/(?:NNN|\d{3})[-_]")
        self.assertIsNone(
            numbered.search(text),
            "the command numbers its output; spec 021 FR-021 places the plan beside its specification "
            "where the directory already supplies the identity, and the reading of Principle VII's "
            "carve-out that permits it is recorded in specs/021-test-plan-agent/plan.md under "
            "Complexity Tracking",
        )

    def test_it_states_that_no_artifact_root_is_resolved_for_the_output(self):
        text = phrases()
        self.assertIn("no artifact root is resolved for this output", text)

    def test_it_never_edits_governance_or_history(self):
        text = phrases()
        self.assertIn("edit the constitution, create a branch", text)

    def test_it_never_writes_test_code_or_configuration(self):
        text = phrases()
        self.assertIn("write, modify, or generate test code", text)
        self.assertIn("modify test framework, coverage, or ci", text)


class SecretsAreNeverReproduced(unittest.TestCase):
    """FR-020b — the error worth making in one direction only."""

    def test_it_states_the_prohibition(self):
        self.assertIn("Never reproduce a secret value", command_text())

    def test_it_gives_the_location_and_kind_instead(self):
        text = phrases()
        self.assertIn("kind and location", text)

    def test_it_prefers_over_withholding(self):
        text = phrases()
        self.assertIn("over-withholding is the correct error", text)


class TheHandoffIsPrintedNeverWired(unittest.TestCase):
    """FR-005, FR-047, FR-048 — what keeps the agent genuinely optional."""

    def test_it_emits_a_copyable_planning_invocation(self):
        text = phrases()
        self.assertIn("ready-to-copy invocation", text)

    def test_the_invocation_is_something_the_user_runs(self):
        text = phrases()
        self.assertIn("something the **user** runs".lower(), text)

    def test_it_never_invokes_another_command(self):
        text = phrases()
        self.assertIn("invoke another command", text)
        self.assertIn("not an invocation", text)

    def test_it_registers_no_hook(self):
        text = phrases()
        self.assertIn("not a hook", text)

    def test_it_writes_no_marker_into_the_specification(self):
        text = phrases()
        self.assertIn("not a marker in the specification", text)

    def test_no_hook_is_registered_in_the_manifest(self):
        """The claim above, checked against the file that would carry a registration."""
        manifest = MANIFEST.read_text(encoding="utf-8")
        hooks = manifest.partition("\nhooks:")[2].partition("\ntags:")[0]
        self.assertNotIn(
            "test-plan", hooks,
            "spectra/extension.yml registers a hook for test-plan; FR-005 keeps the agent opt-in, and "
            "a before_plan hook would prompt for a test plan on every feature in every install",
        )

    def test_it_withholds_the_handoff_when_nothing_was_written(self):
        text = phrases()
        self.assertIn("when you emit nothing", text)


class ReRunningPreservesDecisions(unittest.TestCase):
    """FR-050 to FR-052 — the asymmetry between creating and replacing."""

    def test_it_reads_an_existing_plan_as_an_input(self):
        text = phrases()
        self.assertIn("read it, treat it as an input", text)

    def test_it_confirms_before_rewriting(self):
        text = phrases()
        self.assertIn("ask before rewriting", text)

    def test_the_gate_fires_after_the_derivation(self):
        """A confirmation with no information attached is answered reflexively."""
        text = phrases()
        self.assertIn("after the derivation, before the write", text)

    def test_it_carries_forward_not_covered_decisions(self):
        self.assertIn("The preservation rule", command_text())

    def test_it_never_writes_a_second_file(self):
        text = phrases()
        self.assertIn("one file, one name", text)

    def test_non_interactive_creates_but_never_rewrites(self):
        text = phrases()
        self.assertIn("the asymmetry is the point", text)


class OptionalSectionsNeedATrigger(unittest.TestCase):
    """FR-044, FR-045, research R12."""

    def test_the_guidance_never_reaches_the_output(self):
        text = phrases()
        self.assertIn("optional-section guidance list", text)

    def test_three_sections_are_never_added_automatically(self):
        self.assertIn("Three are never added automatically", command_text())

    def test_a_schedule_is_not_invented(self):
        text = phrases()
        self.assertIn("project management, not test", text)


class ItDegradesLoudly(unittest.TestCase):
    """FR-015, FR-016, FR-049 — a reader can tell checked from unchecked."""

    def test_it_states_its_own_coverage(self):
        text = phrases()
        self.assertIn("checked and found nothing", text)

    def test_it_names_inputs_it_could_not_read(self):
        text = phrases()
        self.assertIn("could not read", text)

    def test_it_has_a_degradation_table(self):
        self.assertIn("Degrade loudly", command_text())

    def test_it_reports_the_resolved_template_by_path(self):
        text = phrases()
        self.assertIn("report which template you used, by path", text)


class ItMakesNoNetworkRequest(unittest.TestCase):
    """FR-020a — the same promise impact and test-strategy make."""

    def test_it_states_that_it_makes_no_network_request(self):
        text = phrases()
        self.assertIn("make a network request", text)

    def test_it_accepts_no_url_credential_or_token(self):
        text = phrases()
        self.assertIn("repository url, credential, or token", text)

    def test_no_url_scheme_appears_as_an_instruction(self):
        """A command that reads only local files has no business naming a fetchable address."""
        text = command_text()
        self.assertNotRegex(
            text, r"https?://(?!semver|spec-kit)",
            "the command names a network address; it is supposed to read only the project it was "
            "invoked in",
        )


if __name__ == "__main__":
    unittest.main()
