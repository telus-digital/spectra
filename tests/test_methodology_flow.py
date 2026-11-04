"""The `methodology` mode, lens, round, record, and handoff rules, asserted against the command text that ships.

A command file is a prompt: its text *is* the implementation, so the enforceable surface is what it
says. These assertions cannot prove an agent behaves correctly at run time. What they prove is that the
rules it is supposed to follow have not been quietly deleted.

The rules pinned here (spec 035):

- **The run states its mode and goal first.** Brownfield or greenfield, from three named signals, and
  whether the constitution will be created or updated.
- **Nine fixed lenses, ten fixed questions.** A fixed set is what lets a reader tell "found nothing" from
  "never looked", and a fixed count is what lets the round be announced honestly.
- **Spec-driven development is the base.** Every other methodology enters the constitution only as an
  obligation bound to a spec-kit phase, and an implement-phase obligation names its `tasks.md` evidence.
- **Sibling ground is referred, never proposed.** Testing, deployment, product technology, and domain
  content each have one source.
- **Only a human choice adopts.** Skip, silence, and a non-interactive run adopt nothing.
- **A re-run never undoes a team's decision.** IDs are frozen, declined items are not re-offered, and an
  adopted item is never reverted — including the Delivery & workflow records carried over from the
  domain analyzer.

The rules added by spec 042:

- **The persistence model is one decision inside lens 4.** Question 5 offers four exclusive models and
  Skip, the accepted one becomes one guardrail written as phase obligations, and the round still holds
  ten questions.

Where the file lives is asserted in `test_doc_output_paths.py`, with the other singletons.

Standard library only, like the rest of the suite.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import helpers as h  # noqa: E402

COMMAND = h.repo_file("spectra", "commands", "methodology.md")
TEMPLATE = h.repo_file("spectra", "templates", "engineering-methodology-template.md")

LENSES = (
    "Methodology stack",
    "Work modes & classification",
    "Requirements intake",
    "Spec lifecycle & traceability",
    "Branching & integration",
    "Review & merge gates",
    "Change records",
    "AI collaboration rules",
    "Governance & evolution",
)

MODELS = ("Living Spec", "Flow-Forward", "Flow-Back", "Hybrid")


def flat(text: str) -> str:
    """Lowercased, with every run of whitespace collapsed, so hard-wrapped prose can be matched."""
    return " ".join(text.lower().split())


def command() -> str:
    return flat(COMMAND.read_text(encoding="utf-8"))


def section(heading: str) -> str:
    """The flattened body of one `## ` section of the command."""
    text = COMMAND.read_text(encoding="utf-8")
    start = text.index(heading)
    end = text.find("\n## ", start + len(heading))
    return flat(text[start : end if end != -1 else None])


class WhatItNeverDoes(unittest.TestCase):
    def test_the_constitution_is_never_written(self):
        self.assertIn("write `.specify/memory/constitution.md` — in any run, approved or not", command())

    def test_no_other_phase_is_run(self):
        text = section("## What this command never does")
        self.assertIn("run any other spec-kit phase", text)
        for phase in ("specify", "clarify", "plan", "tasks", "analyze", "implement"):
            with self.subTest(phase=phase):
                self.assertIn(phase, text)

    def test_one_file_and_no_other_edits(self):
        text = section("## What this command never does")
        self.assertIn("write more than one file, or edit a sibling document, source, configuration, ci", text)

    def test_no_network_request(self):
        self.assertIn("make a network request", section("## What this command never does"))

    def test_practice_is_never_invented(self):
        self.assertIn("report a practice the evidence does not show", section("## What this command never does"))
        self.assertIn("current practice is cited, never invented", command())

    def test_the_one_flag_is_non_interactive(self):
        text = section("## User Input")
        self.assertIn("the one flag** is `--non-interactive`", text)
        self.assertIn("a hint narrows nothing", text)


class TheModeAndGoalAreStatedFirst(unittest.TestCase):
    def test_step_zero_is_the_first_output(self):
        text = section("## Step 0")
        self.assertIn("your **first output**", text)
        self.assertIn("**mode:**", text)
        self.assertIn("**signals:**", text)
        self.assertIn("**goal:** create", text)
        self.assertIn("**goal:** update", text)
        self.assertIn("version 1.4.0", text)

    def test_three_named_signals_with_their_thresholds(self):
        text = section("## Step 0")
        self.assertIn("git rev-list --count head", text)
        self.assertIn("more than 10", text)
        for config in (".github/workflows/", ".gitlab-ci.yml", "codeowners", "contributing.md"):
            with self.subTest(config=config):
                self.assertIn(config, text)
        self.assertIn(
            "at least one source file with more than 20 non-blank lines changed in more than one commit, "
            "or at least five such files when the history has at most one commit (including no history)",
            text,
        )

    def test_the_signals_decide_the_mode(self):
        text = section("## Step 0")
        self.assertIn("**two or more** signals: `brownfield`", text)
        self.assertIn("**none**: `greenfield`", text)
        self.assertIn("**exactly one**: a mixed reading", text)

    def test_a_mixed_reading_is_settled_before_the_lenses(self):
        text = section("## Step 2")
        self.assertIn("before any lens is worked", text)
        self.assertIn("not counted among the ten", text)


class TheProjectIsReadFirst(unittest.TestCase):
    def test_every_input_is_named(self):
        text = section("## Step 1")
        for source in (
            "git log",
            "git branch -a",
            "pull request",
            "issue templates",
            "codeowners",
            "ci workflows",
            "commitlint",
            "changelog",
            "contributing.md",
            "specs/",
            "constitution",
            "domain_analysis.md",
            "test_strategy.md",
            "deployment_strategy.md",
        ):
            with self.subTest(source=source):
                self.assertIn(source, text)

    def test_history_wins_over_documentation(self):
        self.assertIn("treat the history as current practice", section("## Step 1"))


class NineLensesAlwaysWorked(unittest.TestCase):
    def test_every_lens_is_named(self):
        text = COMMAND.read_text(encoding="utf-8")
        for lens in LENSES:
            with self.subTest(lens=lens):
                self.assertIn(f"**{lens}**", text)

    def test_no_lens_is_omitted(self):
        text = section("## Step 4")
        self.assertIn("never omit a lens", text)
        self.assertIn("say what you searched", text)

    def test_the_default_section_mapping(self):
        text = section("## Step 4")
        self.assertIn("use **its** section names instead", text)
        for target in ("core principles", "development workflow", "additional constraints", "governance"):
            with self.subTest(section=target):
                self.assertIn(target, text)

    def test_current_practice_comes_before_candidates(self):
        self.assertIn("in brownfield mode, report current practice before proposing", section("## Step 4"))

    def test_every_candidate_has_a_basis_and_the_lens_a_cap(self):
        text = section("## Step 4")
        self.assertIn("`observed` or `aspirational`", text)
        self.assertIn("at most five candidates per lens", text)
        self.assertIn("em-<lens-slug>-<hash>", text)

    def test_an_asserted_candidate_is_suppressed(self):
        text = section("## Step 4")
        self.assertIn("**suppress** any candidate whose intent a ratified principle already asserts", text)
        self.assertIn("amends: <principle name/number>", text)

    def test_work_modes_classify_six_change_types_and_bind_spikes(self):
        text = section("## Step 4")
        for change in ("feature", "fix", "refactor", "docs", "spike", "hotfix"):
            with self.subTest(change=change):
                self.assertIn(f"`{change}`", text)
        for rule in ("timebox", "single owner", "never merged", "findings, not code"):
            with self.subTest(rule=rule):
                self.assertIn(rule, text)

    def test_the_brd_format_is_referred(self):
        self.assertIn("speckit.spectra.brd", section("## Step 4"))

    def test_lens_eight_offers_three_autonomy_levels(self):
        text = section("## Step 5")
        self.assertIn("**every phase a human checkpoint** *(recommended)*", text)
        self.assertIn("**human gates at spec approval and pr review**", text)
        self.assertIn("**autonomous to pr**", text)
        self.assertIn("tools and secrets candidates", text)
        self.assertIn("unless free text excludes them", text)


class AHandWrittenFileIsRespected(unittest.TestCase):
    def test_it_is_read_as_evidence_and_replaced_only_with_consent(self):
        text = section("## Step 3")
        self.assertIn("without** `command: speckit.spectra.methodology`", text)
        self.assertIn("read it as `claimed`", text)
        self.assertIn("not evidence of current practice", text)
        self.assertIn("written by\n`speckit.spectra.kb-vault` before 1.25.0".replace("\n", " "), text)
        self.assertIn("ask the team for consent", text)
        self.assertIn("show the document in the session instead", text)
        self.assertIn("no second file is ever written", text)

    def test_no_staging_copy_is_named(self):
        self.assertNotIn(".proposed", COMMAND.read_text(encoding="utf-8"))


class TheClarificationRound(unittest.TestCase):
    def test_ten_questions_one_per_turn(self):
        text = section("## Step 5")
        self.assertIn("always ten", text)
        self.assertIn("one question per turn", text)
        self.assertIn("question 3 of 10", text)

    def test_the_round_is_announced_with_its_ways_out(self):
        text = section("## Step 5")
        self.assertIn("**use your defaults**", text)
        self.assertIn("**skip** any one", text)
        self.assertIn("nothing is written until the last answer", text)

    def test_at_least_four_options_one_recommended_one_skip(self):
        text = section("## Step 5")
        self.assertIn("at least four labelled, distinct options", text)
        self.assertIn("mark **exactly one** as recommended", text)
        self.assertIn("one option is **always skip**", text)
        self.assertIn("free text is always valid", text)

    def test_a_question_with_nothing_to_choose_keeps_its_number(self):
        text = section("## Step 5")
        self.assertIn("never drop a question and never renumber the rest", text)
        self.assertIn("four options still", text)

    def test_only_a_human_choice_adopts(self):
        text = section("## Step 5")
        self.assertIn("**skip.** adopt nothing from that question", text)
        self.assertIn("**a question goes unanswered.** adopt nothing from it", text)
        self.assertIn("record each as `default_taken`", text)

    def test_nothing_is_written_before_the_round_ends(self):
        self.assertIn("after the round, never before", section("## Step 7"))

    def test_question_five_is_excluded_from_the_four_option_shape(self):
        text = section("## Step 5")
        self.assertIn("for questions 3, 4, 6–8 and 10, the four are", text)
        self.assertNotIn("for questions 3–8 and 10", text)


class TheDocument(unittest.TestCase):
    def test_the_candidate_record_keys_in_order(self):
        text = COMMAND.read_text(encoding="utf-8")
        keys = ("- id:", "- lens:", "- section:", "- evidence:", "- basis:", "- decision:", "- status:")
        block = text[text.index("### The candidate record") :]
        positions = [block.index(k) for k in keys]
        self.assertEqual(positions, sorted(positions))

    def test_the_constitution_input_holds_only_accepted_unadopted_items(self):
        # The example block opens with `## Constitution input`, which ends `section("## Step 7")`, so the
        # format is checked against the whole command.
        self.assertIn("whose decision is `accepted` and whose status is not `adopted: …`", section("## Step 7"))
        self.assertIn("## constitution input", command())
        self.assertIn("placement: add | amends:", command())

    def test_decisions_and_sources_carries_every_question(self):
        text = command()
        self.assertIn("### decisions and sources", text)
        self.assertIn("carry **all ten** questions", text)

    def test_the_template_cannot_drop_the_constitution_input(self):
        self.assertIn("if a template omits the constitution input section, write it anyway", section("## Step 6"))


class TheHandoff(unittest.TestCase):
    def test_both_ready_prompts_name_the_constitution_input(self):
        text = section("## Step 8")
        self.assertIn('/speckit-constitution create the project constitution from the "constitution input"', text)
        self.assertIn('/speckit-constitution amend the constitution with every guardrail in the "constitution input"', text)

    def test_no_prompt_is_given_when_nothing_is_left_to_adopt(self):
        self.assertIn("if the constitution input section is empty**, say so and give no command", section("## Step 8"))

    def test_missing_siblings_are_listed_in_order(self):
        text = section("## Step 8")
        self.assertIn(
            "speckit.spectra.domain-analyzer → speckit.spectra.methodology → speckit.spectra.test-strategy "
            "→ speckit.spectra.deployment-strategy",
            text,
        )
        self.assertIn("only siblings whose document does not exist", text)
        self.assertIn("no sibling's input is folded into", text)


class TheMethodologyStack(unittest.TestCase):
    def test_sdd_is_the_base_and_never_optional(self):
        text = section("## Step 4")
        self.assertIn("spec-driven development (sdd) is the base", text)
        self.assertIn("never optional", text)

    def test_each_overlay_is_offered_with_its_evidence(self):
        text = section("## Step 4")
        for overlay, signal in (
            ("tdd", "test changes landing before or with"),
            ("bdd", "`.feature` files"),
            ("ddd", "glossary"),
            ("contract-first", "contracts committed ahead of"),
            ("adr-driven", "an `adr/` directory"),
        ):
            with self.subTest(overlay=overlay):
                self.assertIn(overlay, text)
                self.assertIn(signal, text)

    def test_obligations_come_only_from_the_matrix(self):
        text = section("## Step 4")
        self.assertIn("the closed set", text)
        self.assertIn("an overlay that cannot be expressed as such an obligation", text)

    def test_each_adopted_overlay_is_one_candidate(self):
        text = section("## Step 4")
        self.assertIn("**one** candidate, `em-overlay-<name>`", text)
        self.assertIn("lens 1 holds at most five", text)

    def test_implement_phase_obligations_name_their_tasks_md_evidence(self):
        self.assertIn(
            "records that it was run and failed before the implementation task is ticked", section("## Step 4")
        )

    def test_unpractised_overlays_are_aspirational_and_scoped_to_new_code(self):
        text = command()
        self.assertIn("unpractised overlay is `aspirational`", text)
        self.assertIn("new and changed code", text)

    def test_process_cadences_never_enter_the_constitution(self):
        text = section("## Step 4")
        for cadence in ("scrum", "kanban", "shape up"):
            with self.subTest(cadence=cadence):
                self.assertIn(cadence, text)
        self.assertIn("never enter constitution input", text)

    def test_conflicting_obligations_need_a_precedence_before_writing(self):
        text = section("## Step 5")
        self.assertIn("two adopted overlays conflict at one phase", text)
        self.assertIn("ask which takes precedence", text)
        self.assertIn("before anything is written", text)

    def test_question_two_is_one_table_with_four_options(self):
        text = section("## Step 5")
        for option in ("accept all as proposed", "make every overlay should", "choose per row", "skip"):
            with self.subTest(option=option):
                self.assertIn(f"**{option}**", text)
        self.assertIn("one table, a row per adopted overlay", text)


def question_five() -> str:
    """The flattened question 5 bullet of Step 5; Step 5 holds earlier `**Skip**` labels of its own."""
    text = section("## Step 5")
    start = text.index("question 5 has its own shape")
    return text[start : text.index("**free text is always valid.**", start)]


def persistence_rules() -> str:
    """The flattened lens 4 persistence paragraphs of Step 4, up to the lens 8 paragraph that follows."""
    text = COMMAND.read_text(encoding="utf-8")
    start = text.index("**The persistence guardrail.**")
    return flat(text[start : text.index("**Lens 8 is about", start)])


class TheSpecPersistenceModel(unittest.TestCase):
    """Lens 4 settles the spec persistence model (spec 042, contracts/question-five.md and
    contracts/persistence-guardrail.md)."""

    # US1 — the question

    def test_question_five_has_its_own_shape(self):
        text = section("## Step 5")
        self.assertIn("question 5 has its own shape", text)
        self.assertIn("four persistence models exclude each other", text)

    def test_five_options_in_order(self):
        text = question_five()
        labels = (
            "**living spec**",
            "**flow-forward**",
            "**flow-back**",
            "**hybrid (living spec by default)**",
            "**skip**",
        )
        positions = [text.index(label) for label in labels]
        self.assertEqual(positions, sorted(positions))

    def test_one_model_accepted_the_rest_declined(self):
        text = question_five()
        self.assertIn("the chosen model is accepted and the other three declined", text)
        self.assertIn(
            "other lens 4 candidates take the same decision as the model unless free text excludes them", text
        )

    def test_skip_leaves_lens_four_skipped(self):
        self.assertIn("skip leaves every lens 4 candidate `skipped`", question_five())

    def test_each_model_states_fit_and_risk(self):
        text = question_five()
        for phrase in (
            "the spec is the contract",
            "losing implementation rationale",
            "audit trails",
            "context spread over several directories",
            "small teams, fast iteration",
            "silent drift",
            "the spec stays authoritative",
            "the threshold is only as good as the mapping",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_the_models_count_as_one_slot(self):
        self.assertIn("the four persistence models count as one slot", section("## Step 4"))

    # US2 — the guardrail

    def test_preamble_new_capability_and_delivered(self):
        text = persistence_rules()
        self.assertIn("a new capability must get its own feature directory", text)
        self.assertIn("merged to the default branch", text)

    def test_each_model_names_all_five_phases(self):
        text = persistence_rules()
        labels = [f"**{model.lower()}**" for model in MODELS]
        starts = [text.index(label) for label in labels]
        for i, model in enumerate(MODELS):
            block = text[starts[i] : starts[i + 1] if i + 1 < len(starts) else None]
            for phase in ("specify", "plan", "tasks", "implement", "converge"):
                with self.subTest(model=model, phase=phase):
                    self.assertIn(phase, block)

    def test_divergence_updates_an_artifact_first(self):
        text = persistence_rules()
        self.assertIn("`spec.md` must be updated first", text)
        self.assertIn("the **new** `spec.md` must be updated first", text)

    def test_cross_link_wording_is_exact(self):
        text = persistence_rules()
        for phrase in ("extends spec nnn", "supersedes spec nnn", "extended by spec nnn", "superseded by spec nnn"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertIn("no other edit is allowed in a completed feature directory", text)

    def test_flow_back_agrees_before_merge(self):
        text = persistence_rules()
        self.assertIn("before the pull request carrying the change merges", text)
        self.assertIn("analyze phase", text)

    def test_phases_not_invocations(self):
        text = persistence_rules()
        self.assertNotIn("/speckit-", text)
        self.assertNotIn("$speckit-", text)

    def test_guardrail_is_must_in_lens_four(self):
        text = persistence_rules()
        self.assertIn("em-spec-lifecycle-traceability-", text)
        self.assertIn("strictness is **must**", text)

    def test_existing_constitution_rules_apply(self):
        self.assertIn("suppress and `amends:` rules", persistence_rules())

    def test_persistence_never_conflicts_with_an_overlay(self):
        self.assertIn(
            "the persistence guardrail's implement obligation is not an overlay and never conflicts with one",
            section("## Step 5"),
        )

    # US3 — brownfield evidence

    def test_three_signals_are_named(self):
        text = section("## Step 4")
        for phrase in (
            "first-parent",
            "delivery point",
            "changes that directory's `spec.md`",
            "`plan.md` or `tasks.md` while its `spec.md` is unchanged",
            "names another spec directory it builds on",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_recommendation_follows_one_signal_or_hybrid(self):
        text = section("## Step 4")
        self.assertIn("exactly one signal", text)
        self.assertIn("two or more signals, or none, recommend hybrid", text)

    def test_counts_and_citations(self):
        self.assertIn("with a count and up to three citations", section("## Step 4"))

    def test_greenfield_recommends_hybrid(self):
        self.assertIn("**spec lifecycle & traceability** — hybrid", section("## Step 4"))

    # US4 — Hybrid's mapping

    def test_default_mapping_is_pinned(self):
        text = command()
        for pair in (
            "`feature` → flow-forward",
            "`fix` → living",
            "`refactor` → living",
            "`hotfix` → living",
            "`docs` → —",
            "`spike` → —",
        ):
            with self.subTest(pair=pair):
                self.assertIn(pair, text)

    def test_dash_only_where_no_spec_is_required(self):
        self.assertIn(
            "`—` only where the accepted mode-choice table says that change type needs no spec", command()
        )

    def test_hybrid_needs_no_extra_question(self):
        text = section("## Step 5")
        self.assertIn("choosing hybrid accepts the mapping as shown", text)
        self.assertIn("no further question", text)

    def test_mapping_always_in_the_statement(self):
        self.assertIn("the hybrid guardrail always carries the mapping in its statement", command())

    def test_persistence_column_only_under_hybrid(self):
        text = section("## Step 7")
        self.assertIn("a **persistence** column", text)
        self.assertIn("only when hybrid is accepted", text)

    def test_no_table_means_statement_only(self):
        self.assertIn("when question 3 adopted no mode-choice table", command())

    def test_defaults_take_hybrid_with_its_mapping(self):
        self.assertIn(
            "**use your defaults** accepts the recommended model and, for hybrid, the proposed mapping",
            section("## Step 5"),
        )

    # US5 — front matter, reference, re-runs, non-interactive, template

    def test_front_matter_key(self):
        text = section("## Step 7")
        self.assertIn("persistence: hybrid", text)
        self.assertIn(
            "`persistence` is `living`, `flow-forward`, `flow-back`, or `hybrid`, and absent when question 5 "
            "was skipped or not asked",
            text,
        )

    def test_five_references_are_written(self):
        text = section("## Step 7")
        self.assertIn("five references are always written", text)
        self.assertIn("**a persistence reference**", text)
        self.assertNotIn("four references are always written", text)

    def test_reference_when_nothing_accepted(self):
        self.assertIn("no spec persistence model was chosen", section("## Step 7"))

    def test_rerun_offers_prior_model(self):
        text = section("## Re-running")
        self.assertIn("pre-filled from the `persistence` key", text)
        self.assertIn("last run you chose", text)
        self.assertIn("a prior document with no `persistence` key leaves the model undecided", text)

    def test_rerun_declined_model_stays_selectable(self):
        self.assertIn("a declined model stays selectable", section("## Re-running"))

    def test_decisions_record_the_hybrid_mapping(self):
        # Step 7's Constitution input example holds a `## ` line, so slice the whole command instead.
        text = command()
        start = text.index("### decisions and sources")
        self.assertIn(
            "for question 5, the answer taken records the accepted model and, for hybrid, the accepted "
            "per-change-type mapping, including any free-text adjustment",
            text[start:],
        )

    def test_non_interactive_asks_no_model(self):
        self.assertIn("no `persistence` key", section("## Non-interactive mode"))

    def test_template_describes_the_reference(self):
        text = flat(TEMPLATE.read_text(encoding="utf-8"))
        start = text.index("## spec lifecycle & traceability")
        self.assertIn("persistence reference", text[start : text.index("## ", start + 3)])


class SiblingGroundIsReferred(unittest.TestCase):
    """One source per constitution clause (contracts/sibling-boundaries.md)."""

    OWNERS = (
        ("speckit.spectra.test-strategy", ("test levels", "coverage floor", "ratchet", "uat")),
        (
            "speckit.spectra.deployment-strategy",
            ("environments", "promotion", "rollback", "versioning scheme", "release cut", "hotfix promotion"),
        ),
        (
            "speckit.spectra.domain-analyzer",
            ("product languages", "frameworks", "dependency policy", "bounded contexts", "invariants", "glossary"),
        ),
        ("speckit.spectra.adr", ("architecture-level choices", "layering", "security, data handling, or reliability")),
    )

    def test_each_owner_and_its_ground_is_named(self):
        text = section("## Step 4")
        self.assertIn("sibling ground is referred, not proposed", text)
        for owner, grounds in self.OWNERS:
            for ground in grounds:
                with self.subTest(owner=owner, ground=ground):
                    self.assertIn(owner, text)
                    self.assertIn(ground, text)

    def test_five_agents_feed_the_constitution(self):
        """037 M2 — the ADR agent is the fifth feeder."""
        self.assertIn("five agents feed the constitution", section("## Step 4"))
        self.assertNotIn("four agents feed", command())

    def test_the_adr_agent_is_not_in_the_foundation_sequence(self):
        """037 M3 — ADRs are written on demand, one per decision, not as a foundation step."""
        text = COMMAND.read_text(encoding="utf-8")
        start = text.index("**Then the other agents that feed the constitution.**")
        fence = text.index("```text", start)
        sequence = text[fence : text.index("```", fence + 3)]
        self.assertIn("speckit.spectra.deployment-strategy", sequence)
        self.assertNotIn("speckit.spectra.adr", sequence)

    def test_cite_the_document_or_name_the_command(self):
        self.assertIn("cite it if it exists, or name the command that writes it", section("## Step 4"))

    def test_tdd_decides_when_and_test_strategy_decides_what(self):
        self.assertIn("tdd governs *when* tests are written", section("## Step 4"))

    def test_ddd_records_only_the_commitment(self):
        self.assertIn("ddd records the commitment", section("## Step 4"))

    def test_lens_seven_stops_at_commits_and_changelog(self):
        self.assertIn("lens 7 covers the commit convention and the changelog only", section("## Step 4"))


class Greenfield(unittest.TestCase):
    def test_each_lens_has_no_practice_to_report(self):
        self.assertIn("no practice to report", section("## Step 4"))

    def test_every_default_candidate_is_aspirational(self):
        self.assertIn("every default candidate is `aspirational`", section("## Step 4"))

    def test_codify_only_what_exists_is_replaced(self):
        self.assertIn(
            "in greenfield mode, **codify only what exists** has nothing to take, so **choose individually** replaces it",
            section("## Step 5"),
        )

    def test_the_named_defaults(self):
        text = section("## Step 4")
        for default in (
            "trunk-based development",
            "short-lived branches",
            "squash-and-merge",
            "conventional commits",
            "one approval",
        ):
            with self.subTest(default=default):
                self.assertIn(default, text)


class ReRunsRespectDecisions(unittest.TestCase):
    def test_ids_are_frozen(self):
        text = section("## Step 4")
        self.assertIn("frozen from then on", text)
        self.assertIn("never recompute it from the statement as it now reads", text)

    def test_prior_items_are_matched_by_id_then_by_intent(self):
        text = section("## Re-running")
        self.assertIn("by their recorded `id`", text)
        self.assertIn("same lens and asserts the **same intent**", text)

    def test_the_round_is_pre_filled_from_prior_answers(self):
        self.assertIn("pre-fill the round from the prior answers", section("## Re-running"))

    def test_a_declined_item_is_not_offered_again(self):
        self.assertIn("a declined candidate is not offered again as new", section("## Re-running"))

    def test_no_prior_candidate_is_ever_deleted(self):
        self.assertIn("never delete one", section("## Re-running"))

    def test_an_adopted_item_is_never_reverted(self):
        text = section("## Re-running")
        self.assertIn("is never reverted", text)
        self.assertIn("report the drift", text)


class CarriedOverFromTheDomainAnalyzer(unittest.TestCase):
    """Spec 035 (E4): the domain analyzer's Delivery & workflow decisions are prior answers here."""

    def test_records_are_read_from_the_domain_analysis(self):
        text = section("## Re-running")
        self.assertIn("domain_analysis.md", text)
        self.assertIn("handed on to `speckit.spectra.methodology`", text)

    def test_each_decision_carries_over(self):
        text = section("## Re-running")
        self.assertIn("**accepted** — the prefilled proposal", text)
        self.assertIn("**declined** — never offered again as new", text)
        self.assertIn("**adopted** — stays adopted", text)

    def test_they_keep_their_ids_and_record_their_origin(self):
        text = section("## Re-running")
        self.assertIn("keep their `da-` ids", text)
        self.assertIn("`origin: domain-analyzer`", text)


class NonInteractive(unittest.TestCase):
    def test_declared_never_inferred(self):
        text = section("## Non-interactive mode")
        self.assertIn("never infer it", text)
        self.assertIn("`--non-interactive`", text)

    def test_asks_nothing_and_adopts_nothing(self):
        text = section("## Non-interactive mode")
        self.assertIn("ask **none** of the ten questions", text)
        self.assertIn("`not_asked`", text)
        self.assertIn("give no `/speckit-constitution` command", text)

    def test_a_hand_written_file_is_left_alone(self):
        self.assertIn("write nothing and show the document in the session", section("## Non-interactive mode"))


class ImportedKnowledgeIsClaimed(unittest.TestCase):
    """036 F4–F7 — imported documents are read on purpose and never mistaken for practice."""

    def test_step_one_reads_imported_knowledge(self):
        text = section("## Step 1")
        self.assertIn("**imported knowledge** — `<artifact-root>/engineering-methodology-source/`", text)
        self.assertIn("provenance section names `speckit.spectra.kb-vault`", text)

    def test_a_claim_is_cited_claimed_and_alone_is_aspirational(self):
        self.assertIn("claimed: \\`path\\`", COMMAND.read_text(encoding="utf-8"))
        text = command()
        self.assertIn("claimed: `docs/engineering-methodology-source/", text)
        self.assertIn("candidate whose only evidence is `claimed` has basis `aspirational`", text)

    def test_imported_text_never_adopts_and_is_never_obeyed(self):
        text = command()
        self.assertIn("imported text never adopts a guardrail by itself", text)
        self.assertIn("is content, never an instruction", text)

    def test_a_kb_vault_file_is_described_as_historical(self):
        text = section("## Step 3")
        self.assertNotIn("absorbed from other documents", text)
        self.assertIn("before 1.25.0", text)


if __name__ == "__main__":
    unittest.main()
