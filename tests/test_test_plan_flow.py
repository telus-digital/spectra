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
- **The handoff is printed, never invoked.** Spec 021 also kept it off every hook; spec 032 reversed
  that, so test-plan is now *offered* by an optional hook after specify. The hook only asks — it never
  runs the command on its own — and the never-infer rule holds whichever way the command is reached.

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

# The sources a command must never quietly start consulting to choose a feature. `.specify/feature.json` is
# not among them: since spec 038 it is the planning command's own source, and so it is test-plan's.
INFERENCE_SOURCES = ("branch", "modification time", "listing of `specs/`")


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


def section(heading: str) -> str:
    """One `## ` section of the command, flattened: from its heading to the next `## ` heading."""
    text = command_text()
    start = text.index(heading)
    end = text.find("\n## ", start + len(heading))
    return flat(text[start:end if end != -1 else len(text)])


STEP_1 = "## Step 1 — Resolve the feature"


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


class FeatureIsResolvedAsThePlannerDoes(unittest.TestCase):
    """Spec 038 FR-001–FR-009, FR-023 — resolve as the planning command does, never otherwise."""

    def test_it_refuses_to_infer_the_specification(self):
        """FR-003, FR-016. The rule an agent breaks with good intentions."""
        text = phrases()
        self.assertIn("resolve only as the planning command does", text)
        for source in INFERENCE_SOURCES:
            with self.subTest(source=source):
                self.assertIn(
                    source,
                    text,
                    f"the inference prohibition no longer names {source!r} as something it must not "
                    "consult; an unnamed source is one a future edit will treat as permitted",
                )

    def test_it_resolves_in_the_planning_commands_order(self):
        """FR-001, FR-001a — the order of Spec Kit's get_feature_paths, which the planner uses."""
        step = section(STEP_1)
        positions = [step.find(name) for name in
                     ("specify_init_dir", "specify_feature_directory", ".specify/feature.json")]
        self.assertNotIn(-1, positions, "Step 1 no longer names every source the planner reads")
        self.assertEqual(positions, sorted(positions), "Step 1 names the sources out of the planner's order")
        self.assertIn("nearest directory", step)
        self.assertIn(".specify/", step)

    def test_a_set_but_empty_variable_is_unset(self):
        """FR-001 — the planner tests with -n, so an empty value is no value."""
        step = section(STEP_1)
        self.assertIn("set but empty", step)
        self.assertIn("unset", step)

    def test_the_specification_is_spec_md_in_the_feature_directory(self):
        """FR-002."""
        self.assertIn("spec.md in the feature directory", section(STEP_1).replace("`", ""))

    def test_resolution_writes_nothing(self):
        """FR-004 — the planner persists and creates; test-plan does neither."""
        step = section(STEP_1)
        self.assertIn("never writes `.specify/feature.json`", step)
        self.assertIn("never creates the feature directory", step)

    def test_one_shell_read_once_per_run(self):
        """FR-005, research R2 — agent-agnostic, with both shells Spec Kit ships scripts for."""
        step = section(STEP_1)
        for phrase in ("exactly one shell read", "once per run", "specify_init_dir",
                       "specify_feature_directory", "posix", "powershell"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, step)

    def test_the_never_table_names_the_one_read(self):
        """FR-005, plan C1 — the read is the only command run to resolve the feature."""
        row = next(line for line in command_text().splitlines()
                   if line.startswith("| Run, build, or install anything"))
        self.assertIn("the only command run to resolve the feature", flat(row))

    def test_the_governing_rule_resolves_as_the_planner_does(self):
        """FR-016, analyze U1 — the rule every other rule narrows."""
        rule = section("## The one rule that governs everything")
        self.assertIn("resolved exactly as the planning command resolves it", rule)
        self.assertNotIn("the specification you were handed", rule)
        self.assertNotIn("never guess which specification was meant", rule)

    def test_the_introduction_no_longer_says_it_is_handed_a_specification(self):
        """Analyze U2."""
        intro = flat(command_text().partition("## The one rule")[0])
        self.assertNotIn("someone hands you a specification", intro)

    def test_every_resolution_stop_is_listed(self):
        """FR-001a, FR-005–FR-007 — each one writes nothing and emits no handoff."""
        step = section(STEP_1)
        for phrase in ("the shell read is denied or fails", "names no existing directory", "neither source",
                       "cannot be parsed", "has no `spec.md`"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, step)

    def test_an_unreadable_environment_never_falls_back(self):
        """FR-005, clarification Q2 — the fallback would reintroduce the split."""
        self.assertIn("never fall back to `.specify/feature.json` alone", phrases())

    def test_the_remedy_block_names_both_ways_to_switch(self):
        """FR-023 — and specify only as the way to create a feature."""
        step = section(STEP_1)
        self.assertIn("for this session", step)
        self.assertIn("set specify_feature_directory=", step)
        self.assertIn("for good", step)
        self.assertIn('"feature_directory" in .specify/feature.json', step)
        self.assertIn("to create a new feature, run the specify command", step)

    def test_the_invoking_project_is_defined(self):
        """Analyze U3 — SPECIFY_INIT_DIR can root resolution in another project."""
        step = section(STEP_1)
        self.assertIn("the invoking project is the nearest directory containing `.specify/`", step)
        self.assertIn("regardless of `specify_init_dir`", step)
        out_of_project = flat(command_text().partition("### The out-of-project stop")[2].partition("\n## ")[0])
        self.assertIn("the invoking project (step 1)", out_of_project)

    def test_the_skeleton_names_the_environment_read(self):
        """Analyze I3."""
        line = next(l for l in command_text().splitlines() if l.startswith("## Sources consulted and coverage"))
        self.assertIn("environment read", line)

    def test_it_refuses_to_offer_a_picker(self):
        """A list the command assembled is the same failure with extra steps."""
        text = phrases()
        self.assertTrue(
            "do not offer a list" in text or "offering a picker" in text,
            "the command no longer rules out listing the specifications it can see",
        )

    def test_it_stops_when_the_specification_is_outside_the_project(self):
        """FR-022 — the guard that replaces a fixed output folder's write-scope protection."""
        text = phrases()
        self.assertIn("out-of-project", text)
        self.assertTrue(
            "stop before writing" in text,
            "the out-of-project path no longer stops before writing",
        )


class AnArgumentOnlyConfirms(unittest.TestCase):
    """Spec 038 FR-008, FR-009, research R3 — a path can confirm the feature, never choose it."""

    def test_a_match_is_the_feature_directory_or_its_spec(self):
        self.assertIn("the feature directory or its `spec.md`", section(STEP_1))

    def test_spelling_is_normalized_before_comparing(self):
        self.assertIn("trailing slash", section(STEP_1))

    def test_any_other_path_stops_before_reading(self):
        step = section(STEP_1)
        self.assertIn("any other path", step)
        self.assertIn("stop before reading the specification", step)

    def test_the_mismatch_names_both_sides_and_the_source(self):
        self.assertIn("the argument's path, the resolved directory, and its source", section(STEP_1))

    def test_an_argument_never_replaces_resolution(self):
        self.assertIn("an argument is never used in place of", section(STEP_1))


class TheResolutionIsAnnounced(unittest.TestCase):
    """Spec 038 FR-010–FR-012, research R5 — the approver can see which specification was used."""

    def test_it_is_the_first_thing_said(self):
        step = section(STEP_1)
        self.assertIn("the first thing you say", step)
        self.assertIn("feature: specs/", step)
        self.assertIn("(from .specify/feature.json)", step)

    def test_a_disagreeing_record_is_named(self):
        self.assertIn("; .specify/feature.json names", section(STEP_1))

    def test_the_identifying_block_records_the_source(self):
        self.assertIn("resolved from", section("## Step 13 — The identifying block"))

    def test_the_report_carries_the_source(self):
        self.assertIn("the source the feature was resolved from", section("## Step 16 — Report"))

    def test_the_environment_read_is_a_recorded_input(self):
        """Analyze C1 — FR-005 requires the read to appear among the sources."""
        step = section(STEP_1)
        self.assertIn("record the read as an input", step)
        self.assertIn("sources consulted and coverage", step)

    def test_the_non_interactive_announcement_comes_first(self):
        """Analyze I1 — two announcements, one order."""
        self.assertIn("the non-interactive announcement comes first", section(STEP_1))
        self.assertIn("before the feature line in step 1", section("## Non-interactive mode"))


class NoStaleProse(unittest.TestCase):
    """Spec 038 FR-018, FR-019 — every surface that describes the command describes the new contract."""

    STALE_DESCRIPTION = ("requires the spec path", "never inferred")

    def test_the_descriptions_no_longer_require_a_path(self):
        front = flat(command_text().split("---", 2)[1])
        manifest = MANIFEST.read_text(encoding="utf-8")
        entry = flat(manifest.partition('name: "speckit.spectra.test-plan"')[2].partition("- name:")[0])
        for text, where in ((front, "front matter"), (entry, "extension.yml")):
            for phrase in self.STALE_DESCRIPTION:
                with self.subTest(where=where, phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_the_prose_drops_the_feature_record_prohibition(self):
        agents = h.repo_file("AGENTS_LIST.md").read_text(encoding="utf-8")
        block = agents.partition("<!-- SPECTRA:AGENT id=test-plan -->")[2].partition("<!-- SPECTRA:AGENT id=")[0]
        site = h.repo_file("docs", "getting-started", "agents.html").read_text(encoding="utf-8")
        card = site.partition('<span class="name">speckit.spectra.test-plan</span>')[2].partition("</li>")[0]
        for text, where in ((block, "AGENTS_LIST.md"), (card, "docs/getting-started/agents.html")):
            with self.subTest(where=where):
                self.assertNotIn("no feature record", flat(text))
                self.assertNotIn("never inferred", flat(text))
        self.assertIn("<pre><code>/speckit-spectra-test-plan</code></pre>", card)


class TraceabilityRunsBothWays(unittest.TestCase):
    """FR-023 to FR-025 — the invariant that is the product."""

    def test_every_acceptance_criterion_reaches_a_condition_or_an_uncovered_item(self):
        text = phrases()
        self.assertTrue(
            "never none of them" in text,
            "the forward half of the traceability invariant is gone; a criterion absent from the "
            "conditions table, the UAT scenarios, and the not-covered list is the defect this command "
            "exists to prevent, and the document looks complete while it is wrong",
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

    def test_it_names_the_five_uncovered_reasons(self):
        """Spec 032 added the fifth: a criterion only a lens the strategy ruled out could verify."""
        text = phrases()
        for reason in ("unresolved clarification", "untestable as written", "out of scope", "deferred",
                       "ruled out by the strategy"):
            with self.subTest(reason=reason):
                self.assertIn(reason, text)

    def test_an_unresolved_marker_names_the_clarification_command(self):
        text = phrases()
        self.assertIn("clarification command", text)


class TheLensSetComesFromTheStrategy(unittest.TestCase):
    """Spec 032 FR-010 to FR-014 — the plan has exactly the lenses the strategy chose.

    Before spec 032 the plan took only the strategy's *names*. Now it takes the *set*: a lens the strategy
    marks not applicable is unavailable here, so two documents a reviewer reads side by side can no longer
    disagree about whether, say, UAT is part of how this project tests itself.
    """

    def test_it_reads_the_strategy_front_matter(self):
        self.assertIn("`lenses:`", command_text())

    def test_a_ruled_out_lens_sends_the_criterion_to_not_covered(self):
        text = phrases()
        self.assertIn("ruled out by the strategy", text)
        self.assertIn("re-run test-strategy", text)

    def test_a_pre_032_strategy_is_named_loudly(self):
        self.assertIn("this strategy predates the uat and regression lenses", phrases())

    def test_no_strategy_is_named_loudly(self):
        self.assertIn("no test strategy exists", phrases())

    def test_uat_and_regression_are_sections_not_levels(self):
        text = phrases()
        self.assertIn("section-bearing", text)
        self.assertIn("never a condition's level", text)

    def test_manual_stays_distinct_from_uat(self):
        self.assertIn("distinct from a uat scenario", phrases())


class UatScenariosAndRegressionScope(unittest.TestCase):
    """Spec 032 FR-020 to FR-026 — the two sections everything downstream starts from."""

    def test_it_derives_suggested_uat_scenarios(self):
        text = phrases()
        self.assertIn("suggested uat scenarios", text)
        self.assertIn("`uat1`", text)

    def test_every_scenario_names_an_executor(self):
        text = command_text()
        for executor in ("`agent`", "`human`", "`either`"):
            with self.subTest(executor=executor):
                self.assertIn(executor, text)

    def test_the_agent_executor_needs_a_drivable_surface(self):
        text = phrases()
        self.assertIn("agent only where the surface can actually be driven", text)
        self.assertIn(
            "not from this session's tools", text,
            "test-plan must judge the executor from the surface kind and the strategy's policy; uat runs "
            "later, possibly in a different agent, so the planning session's tools prove nothing (FR-021)",
        )

    def test_every_user_story_gets_a_scenario_or_a_reason(self):
        self.assertIn("every user story", phrases())

    def test_it_derives_a_regression_scope(self):
        text = phrases()
        self.assertIn("regression scope", text)
        for kind in ("`existing`", "`risk-driven addition`"):
            with self.subTest(kind=kind):
                self.assertIn(kind, command_text())

    def test_the_template_declares_both_sections(self):
        template = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("## 4. Suggested UAT Scenarios", template)
        self.assertIn("## 5. Regression Scope", template)


class ItHonoursTheWholeStrategy(unittest.TestCase):
    """Spec 032 FR-030 to FR-037 — more of the strategy than its vocabulary and its floor."""

    def test_the_ownership_map_decides_the_level(self):
        text = phrases()
        self.assertIn("honour the strategy's ownership map", text)
        self.assertIn("`ownership:`", command_text())

    def test_a_ruled_out_tool_is_never_named(self):
        self.assertIn("a tool the strategy ruled out", phrases())

    def test_a_known_risk_area_raises_likelihood(self):
        self.assertIn("at least medium", phrases())

    def test_the_strategy_journeys_are_favoured(self):
        self.assertIn("journeys the strategy names", phrases())

    def test_the_floor_is_per_surface(self):
        self.assertIn("the floor of each surface the feature touches", phrases())

    def test_inherited_policy_keeps_its_provenance(self):
        text = phrases()
        self.assertIn("carries the strategy's provenance", text)
        for provenance in ("`cited`", "`convention`", "`stated`"):
            with self.subTest(provenance=provenance):
                self.assertIn(provenance, command_text())

    def test_a_stale_strategy_is_flagged(self):
        text = phrases()
        self.assertIn("possibly stale", text)
        self.assertIn("the history lookup is a read", text)

    def test_step_one_counts_its_own_outcomes(self):
        """The defect spec 032 found: the prose said four, the table listed six."""
        text = command_text()
        step = text[text.index("## Step 1 — Resolve the feature"):text.index("### Resolve only as the planning command does")]
        stated = re.search(r"(\w+) outcomes:", step).group(1).lower()
        words = {"four": 4, "five": 5, "six": 6, "seven": 7}
        rows = [line for line in step.splitlines() if line.startswith("| ") and not line.startswith("| Input")]
        self.assertEqual(words[stated], len(rows), f"Step 1 says {stated} outcomes but lists {len(rows)}")


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
        self.assertIn("docs/TEST_STRATEGY.md", command_text())

    def test_it_falls_back_to_the_earlier_strategy_location(self):
        self.assertIn("<artifact-root>/test-strategy/TEST_STRATEGY.md", command_text())

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
        for level in ("`unit`", "`integration`", "`api-contract`", "`end-to-end`", "`manual`", "`uat`",
                      "`regression`"):
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

    def test_it_is_offered_by_an_optional_hook_that_only_asks(self):
        """Spec 032 FR-040 to FR-042, reversing spec 021 FR-005."""
        text = phrases()
        self.assertIn("offered by an optional hook after specify", text)
        self.assertIn("the hook only asks", text)

    def test_the_hook_does_not_relax_the_never_infer_rule(self):
        self.assertIn("reached through the hook or not, the feature is resolved identically", phrases())

    def test_the_handoff_waits_for_the_planner_to_agree(self):
        """FR-014, research R4 — a parallel specify can move the feature record mid-run."""
        step = section("## Step 17 — Hand the plan to the planner")
        self.assertIn("the planning command would still resolve", step)
        self.assertIn("re-read only `.specify/feature.json`", step)

    def test_it_writes_no_marker_into_the_specification(self):
        text = phrases()
        self.assertIn("not a marker in the specification", text)

    def test_the_manifest_offers_it_after_specify_optionally(self):
        """The claim above, checked against the file that carries the registration."""
        manifest = MANIFEST.read_text(encoding="utf-8")
        hooks = manifest.partition("\nhooks:")[2].partition("\ntags:")[0]
        after_specify = hooks.partition("after_specify:")[2].partition("after_implement:")[0]
        self.assertIn("speckit.spectra.test-plan", after_specify)
        self.assertIn("optional: true", after_specify)
        self.assertNotIn(
            "optional: false", after_specify,
            "a mandatory test-plan hook would run on every feature in every install; spec 032 makes it "
            "an offer, never an automatic step",
        )
        self.assertNotIn(
            "SPEC_FILE", after_specify,
            "spec 038: test-plan resolves the feature specify recorded, so the hook passes no path",
        )
        self.assertIn("feature", after_specify)
        self.assertNotIn("reported above", after_specify, "core specify prints hooks before SPEC_FILE")

    def test_the_prompt_writes_the_obligations_into_plan_md(self):
        """Spec 032 FR-043: the core tasks command reads plan.md, never test-plan.md."""
        text = phrases()
        self.assertIn("testing obligations", text)
        self.assertIn("writes the test before the implementation it covers", text)

    def test_uat_scenarios_become_a_final_phase_implement_does_not_execute(self):
        text = phrases()
        self.assertIn("not executed by the implement command", text)
        self.assertIn("[uat] uat<n>", text)

    def test_the_phase_title_names_no_agent_syntax(self):
        """Principle III: the title lands in every user's tasks.md, whatever agent they use."""
        text = command_text()
        start = text.index("User Acceptance (UAT)")
        title = text[start:start + 80]
        self.assertNotIn("/speckit", title, "the UAT phase title hard-codes one agent's slash syntax")

    def test_a_clause_for_an_absent_section_is_dropped(self):
        self.assertIn("never mentions a section the plan does not have", phrases())

    def test_the_prompt_links_the_written_file(self):
        self.assertIn("link to the path you actually wrote", phrases())

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


class NonInteractiveIsDeclaredNeverDetected(unittest.TestCase):
    """The same trigger `test-strategy` carried, fixed in both places at once.

    "Piped input, no terminal, an automated runner" are process facts, and a command file is a prompt:
    no file descriptors, no parent process, nothing to inspect. So the reader guessed, and the guess
    that cannot leave it blocked is *assume nobody is there*. Here a false positive is the quieter of
    the two failures — an existing plan is reported rather than rewritten, which is conservative and
    recoverable — but it is wrong for the same reason, so it moves in the same change rather than
    waiting for someone to hit it.
    """

    def test_interactive_is_the_default(self):
        text = command_text()
        self.assertIn("A session is interactive unless someone declares otherwise", text)

    def test_the_declarations_are_a_closed_set(self):
        text = command_text()
        self.assertIn("exactly two declarations", text)
        self.assertIn("`--non-interactive` in the arguments", text)
        self.assertIn("no answer can be given", text)

    def test_inference_is_forbidden_with_its_reason(self):
        text = command_text()
        self.assertIn("**Never infer it.**", text)
        self.assertIn("you are reading a prompt, not inspecting", text)

    def test_the_cost_of_a_wrong_guess_is_named(self):
        text = command_text()
        self.assertIn("instead of the rewrite they asked for", text)

    def test_the_removed_criteria_never_return_as_instructions(self):
        self.assertNotIn("Detect a session that cannot answer", command_text())

    def test_a_feature_that_does_not_resolve_still_stops(self):
        """Plan C2 — the argument is optional now, so the stop moves to resolution."""
        text = phrases()
        self.assertIn("a feature that does not resolve still stops", text)
        self.assertNotIn("an empty argument still stops", text)

    def test_the_rewrite_asymmetry_survives_alongside_it(self):
        """Two different asymmetries live in this section; neither may displace the other."""
        text = command_text()
        self.assertIn("Creating is additive and recoverable", text)
        self.assertIn("silence is not approval", text)


if __name__ == "__main__":
    unittest.main()
