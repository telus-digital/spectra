"""The `defect-rca` flow, asserted against the command text that ships.

A command file is a prompt: its text *is* the implementation, so the enforceable surface is what it says.
These assertions cannot prove an agent behaves correctly at run time — that is the manual pass in
`test/README.md`. What they prove is that the rules it is supposed to follow have not been quietly
deleted, which is the regression that actually happens to prompt files.

This agent is the sixth Spectra document producer, so Principles VII and VIII are already enforced for it
by `test_doc_output_paths.py` (it is in `CANONICAL`) and `test_document_templates.py`; nothing here
duplicates those. What is left is the part that makes a root cause analysis worth reading, and every one
of these rules is the kind a well-meaning edit removes without anyone noticing:

- **It never asks for a credential.** This is the highest-consequence rule in the command and the one an
  agent will break with the best intentions — asked to fetch a JIRA ticket it cannot reach, requesting a
  token is *helpful*. It is also the one that would ship a phishing surface inside a zip, so it gets its
  own test class rather than a clause.
- **It degrades on `gh` rather than gating on it.** A third posture, different from `create-pr` and
  `review-pr` (hard gate) and from `impact` and `test-plan` (no network at all). Pinned in both
  directions, so neither a silent hard gate nor a silent removal of the check passes unnoticed.
- **Recurrence is judged on three named axes and never on title similarity**, and a preventive-action
  verdict of completed or not-completed requires a citation. An uncited "completed" against an action
  nobody finished makes a recurrence read as a fresh defect, which is the failure the whole corpus exists
  to catch.
- **A layer-two finding is never promoted to a root cause.** Reading the code creates a failure mode an
  interviewer does not have: the plausible path is genuinely there, so stopping feels like finishing.
- **Invalidated hypotheses are recorded**, and a hypothesis is never validated on evidence that cannot
  settle it. Together these are the difference between an analysis and a justification.
- **It writes two files, at the end, and never overwrites.** That is what makes an interrupted run
  harmless and keeps the corpus append-only.
- **The sequence is highest-plus-one, not a count**, and the slug names the symptom rather than the cause.
  Both are rules a future edit would plausibly "simplify" away, and both fail silently in production.

Standard library only, like the rest of the suite.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import helpers as h  # noqa: E402

COMMAND = h.repo_file("spectra", "commands", "defect-rca.md")
TEMPLATE = h.repo_file("spectra", "templates", "defect-rca-template.md")
MANIFEST = h.repo_file("spectra", "extension.yml")

COMMAND_NAME = "speckit.spectra.defect-rca"
WRITE_TARGET = "<artifact-root>/defect-rca/NNN-<slug>.md"
INDEX_TARGET = "<artifact-root>/defect-rca/README.md"


def text() -> str:
    return COMMAND.read_text(encoding="utf-8")


def flat() -> str:
    """Whitespace-flattened, so an assertion survives a reflow of the prose.

    The command file is hard-wrapped, so a rule that straddles a line break would not match a
    line-oriented search. Flattening means an assertion fails when a *rule* is deleted rather than when a
    paragraph is re-flowed.
    """
    return " ".join(text().split())


def lower() -> str:
    return flat().lower()


class TheCommandIsRegistered(unittest.TestCase):
    """Principles II and III: one file, under the existing extension, correctly namespaced."""

    def test_the_command_file_exists(self):
        self.assertTrue(COMMAND.is_file(), "spectra/commands/defect-rca.md does not exist")

    def test_it_carries_front_matter_with_a_description(self):
        head = text().split("---", 2)
        self.assertEqual("", head[0].strip(), "the file does not open with YAML front matter")
        self.assertIn("description:", head[1], "front matter carries no description key")

    def test_the_manifest_registers_the_command(self):
        manifest = MANIFEST.read_text(encoding="utf-8")
        self.assertIn(f'- name: "{COMMAND_NAME}"', manifest)
        self.assertIn('file: "commands/defect-rca.md"', manifest)

    def test_it_takes_its_input_through_the_generic_placeholder(self):
        """Principle III: no agent's invocation syntax, ever."""
        self.assertIn("$ARGUMENTS", text())

    def test_it_registers_no_hook(self):
        """A hook would make every project prompt for an RCA on flows with no defect in them."""
        manifest = MANIFEST.read_text(encoding="utf-8")
        hooks = manifest.partition("\nhooks:\n")[2]
        self.assertNotIn("defect-rca", hooks, "defect-rca registered a hook; spec 022 FR-005 forbids it")


class ItRefusesToGuessWhichDefect(unittest.TestCase):
    """An analysis of the wrong defect reads as authoritative to everyone who did not run it."""

    def test_empty_input_asks_and_stops(self):
        self.assertIn("with no input, ask what defect to analyze and stop", lower())

    def test_it_names_each_inference_route_it_will_not_take(self):
        for route in ("branch name", "recent commits", "open issues", "failing tests"):
            with self.subTest(route=route):
                self.assertIn(route, lower(), f"the command no longer refuses to infer from the {route}")

    def test_it_reads_and_writes_nothing_before_a_defect_is_supplied(self):
        self.assertIn("read nothing, write nothing, and infer nothing", lower())


class ItNeverAsksForACredential(unittest.TestCase):
    """The highest-consequence rule here, and the cheapest to assert.

    A shipped prompt that asks a user to paste a JIRA token is a phishing surface distributed in a zip.
    The rule has to be present as a refusal, and no line may read as a request.
    """

    def test_the_refusal_is_stated(self):
        body = lower()
        self.assertIn("never attempt to authenticate", body)
        self.assertTrue(
            "ask for, accept, transmit, or store a credential" in body,
            "the command no longer forbids handling a credential",
        )

    def test_degrading_is_explicitly_not_asking_for_a_key(self):
        self.assertIn("ask for the content, not the key", lower())

    def test_no_line_requests_a_secret_from_the_user(self):
        """A request, as opposed to the quoted example of one the command refuses to make."""
        request = re.compile(
            r"\b(?:ask|prompt|request)\s+(?:the\s+)?(?:user\s+)?(?:for|to\s+(?:paste|enter|provide))\b"
            r"[^.]{0,60}\b(?:token|password|api key|credential|secret)\b",
            re.IGNORECASE,
        )
        refusals = ("never", "not", "forbidden", "must not", "no ")
        for number, line in enumerate(text().splitlines(), 1):
            if not request.search(line):
                continue
            with self.subTest(line=number):
                self.assertTrue(
                    any(word in line.lower() for word in refusals),
                    f"defect-rca.md:{number} reads as a request for a credential — {line.strip()!r}",
                )


class ItDegradesRatherThanGating(unittest.TestCase):
    """The third `gh` posture on the roster, pinned in both directions."""

    def test_both_gh_failure_modes_have_distinct_remedies(self):
        body = lower()
        self.assertIn("not installed", body)
        self.assertIn("gh auth login", body)

    def test_failure_continues_as_a_plain_description(self):
        self.assertIn("continue treating what you have as a plain description", lower())

    def test_it_states_that_it_does_not_stop(self):
        self.assertIn("you do not stop", lower())

    def test_it_fetches_the_comments_too(self):
        """An issue fetched without its comments is half an issue."""
        self.assertIn("issue body **and its comments**", flat())


class TheChannelIsResolvedAndStated(unittest.TestCase):
    def test_all_three_channels_are_named(self):
        body = lower()
        for channel in ("github issue", "jira", "plain description"):
            with self.subTest(channel=channel):
                self.assertIn(channel, body)

    def test_the_channel_is_stated_before_evidence_is_gathered(self):
        self.assertIn("state the channel you resolved to before you gather any evidence", lower())

    def test_ambiguity_resolves_to_the_channel_that_cannot_fail(self):
        self.assertIn("ambiguity resolves toward **plain description**", flat().lower())


class EvidenceIsCited(unittest.TestCase):
    """R1, in both directions: a presence claim and an absence claim each carry their source."""

    def test_a_code_claim_names_the_file(self):
        self.assertIn("every claim about the code cites its source", lower())

    def test_an_absence_claim_names_the_search(self):
        self.assertIn("states what you searched for and where", lower())

    def test_reduced_search_coverage_is_disclosed_rather_than_narrowed_silently(self):
        self.assertIn("rather than narrowing silently", lower())

    def test_the_scan_is_scoped_and_its_gap_stated(self):
        body = lower()
        self.assertIn("scope the scan outward from the symptom", body)
        self.assertIn("which you did not", body)


class TheLadderIsNamedAndEnforced(unittest.TestCase):
    """Reading the code makes stopping at a plausible path feel like finishing."""

    def test_all_five_layers_are_named(self):
        body = lower()
        for layer in (
            "symptom",
            "immediate technical cause",
            "contributing factors",
            "process and practice gaps",
            "systemic and organizational root cause",
        ):
            with self.subTest(layer=layer):
                self.assertIn(layer, body)

    def test_every_probe_states_its_layer(self):
        self.assertIn("name the layer on every probe", lower())

    def test_a_plausible_code_path_is_not_a_conclusion(self):
        self.assertIn("a plausible code path is a layer-2 finding, never a conclusion", lower())

    def test_synthesis_is_blocked_at_layer_two(self):
        self.assertIn(
            "if the deepest validated finding is still layer 2, say so and do not promote it",
            lower(),
        )


class HypothesesAreTrackedHonestly(unittest.TestCase):
    def test_every_status_is_named(self):
        body = lower()
        for status in ("open", "supported", "weakened", "invalidated", "validated"):
            with self.subTest(status=status):
                self.assertIn(status, body)

    def test_a_hypothesis_is_never_validated_on_evidence_that_cannot_settle_it(self):
        self.assertIn("never validated on evidence that cannot settle it", lower())

    def test_failure_to_disprove_is_open_rather_than_supported(self):
        self.assertIn("being unable to disprove something makes it `open`, not `supported`", lower())

    def test_invalidated_hypotheses_are_recorded(self):
        body = lower()
        self.assertIn("invalidated hypotheses are recorded, not just the surviving one", body)
        self.assertIn("justification, not an analysis", body)

    def test_it_never_answers_its_own_question(self):
        self.assertIn("never answer your own question", lower())

    def test_it_never_infers_an_unobserved_runtime_fact(self):
        self.assertIn("never infer a runtime fact you did not observe", lower())

    def test_an_invalidated_hypothesis_needs_new_evidence_to_be_revived(self):
        self.assertIn("never becomes `validated` without new evidence", lower())


class RecurrenceIsAuditable(unittest.TestCase):
    """Three named axes, the firing one disclosed, and title similarity excluded."""

    def test_the_search_runs_at_intake(self):
        self.assertIn("do this **at intake, while the analysis is still open**", flat().lower())

    def test_all_three_axes_are_named(self):
        body = lower()
        for axis in ("implicated code", "symptom", "root cause"):
            with self.subTest(axis=axis):
                self.assertIn(axis, body)

    def test_title_similarity_is_excluded(self):
        self.assertIn("title similarity is not an axis", lower())

    def test_the_firing_axis_is_disclosed(self):
        self.assertIn("disclose which axis fired", lower())

    def test_the_index_is_a_cache_and_the_documents_are_the_corpus(self):
        body = lower()
        self.assertIn("cache of the corpus, never the corpus", body)
        self.assertIn("it never means *no match exists*", body)

    def test_an_empty_corpus_is_not_an_error(self):
        self.assertIn("is not an error and not a prompt", lower())


class PreventiveActionVerdictsAreCited(unittest.TestCase):
    """R6. The judgement most likely to be wrong, so it is the one that must under-claim."""

    def test_all_three_verdicts_are_named(self):
        body = lower()
        for verdict in ("apparently completed", "apparently not completed", "undeterminable"):
            with self.subTest(verdict=verdict):
                self.assertIn(verdict, body)

    def test_undeterminable_is_the_default(self):
        self.assertIn("`undeterminable` is the default", lower())

    def test_a_bare_verdict_is_never_acceptable(self):
        self.assertIn('a bare "done" or "not done" is never acceptable', lower())

    def test_the_reason_for_under_claiming_is_stated(self):
        self.assertIn("read as a fresh defect", lower())


class TheRelatedFieldIsFilledEitherWay(unittest.TestCase):
    def test_no_match_still_records_that_the_search_ran(self):
        body = lower()
        self.assertIn("the search **ran and found nothing**", flat().lower())
        self.assertIn("never blank, never omitted", body)


class TheWriteScopeHolds(unittest.TestCase):
    """Two files, one folder, and read-only everywhere else."""

    def test_both_write_targets_are_named(self):
        body = text()
        self.assertIn(WRITE_TARGET, body)
        self.assertIn(INDEX_TARGET, body)

    def test_nothing_else_is_written(self):
        self.assertIn("nothing else, anywhere, ever", lower())

    def test_it_writes_no_fix_and_no_test(self):
        body = lower()
        self.assertIn("no patch, no configuration change, no test code", body)

    def test_it_writes_back_to_no_tracker(self):
        self.assertIn("no comment, no issue, no transition, no label", lower())

    def test_it_offers_the_constitution_line_without_writing_it(self):
        body = lower()
        self.assertIn("never write it", body)
        self.assertIn("you may *offer* a constitution line", body)

    def test_working_artifacts_are_never_written_to_disk(self):
        self.assertIn("rendered in the session and never written to disk", lower())

    def test_exploration_writes_nothing(self):
        self.assertIn("exploration writes nothing", lower())


class TheNumberingCannotDrift(unittest.TestCase):
    """Both rules here fail silently in production, which is why they are pinned."""

    def test_the_sequence_is_highest_plus_one_not_a_count(self):
        self.assertIn(
            "one greater than the highest\nnumber already present — not a count of the files there",
            text(),
        )

    def test_a_deleted_analysis_cannot_cause_a_collision(self):
        self.assertIn("cannot\ncause a collision", text())

    def test_the_slug_names_the_symptom_not_the_cause(self):
        self.assertIn("names the **observed problem, never\nthe suspected cause**", text())

    def test_the_reason_for_the_symptom_slug_is_stated(self):
        self.assertIn("you name the file before you finish the analysis", lower())

    def test_it_never_overwrites(self):
        self.assertIn("never overwrite, replace, or amend an existing file", lower())

    def test_an_unconventionally_named_file_is_left_alone(self):
        self.assertIn("ignored for numbering, reported once, and left alone", lower())


class TheWriteHappensOnceAtTheEnd(unittest.TestCase):
    def test_the_document_and_the_index_are_written_together_as_the_final_act(self):
        self.assertIn("written together, as the run's final act", lower())

    def test_an_abandoned_run_consumes_no_number(self):
        body = lower()
        self.assertIn("no partial document", body)
        self.assertIn("no number consumed", body)


class TheDocumentStaysHonest(unittest.TestCase):
    def test_the_symptom_is_stated_adjacent_to_the_root_cause(self):
        self.assertIn("stated adjacently and distinguished", lower())

    def test_evidence_carries_a_source_attribution(self):
        self.assertIn("code / commit / config / test / user-supplied", lower())

    def test_a_user_supplied_finding_is_never_relabelled_as_code(self):
        self.assertIn("that is a second row, not an edit", lower())

    def test_unquantifiable_impact_is_stated_rather_than_omitted(self):
        self.assertIn("say so\nrather than omitting the section", text())

    def test_a_restated_corrective_action_is_flagged(self):
        self.assertIn("only restates the corrective one, say so plainly", lower())

    def test_nothing_validated_is_recorded_rather_than_filled_with_a_guess(self):
        body = lower()
        self.assertIn("do not promote a speculative cause to fill the section", body)
        self.assertIn("guessed a sixth", body)

    def test_the_advisory_status_line_is_never_softened(self):
        self.assertIn("never softened, reworded, or dropped", lower())

    def test_the_owner_is_read_rather_than_invented(self):
        body = lower()
        self.assertIn("configured git author name", body)
        self.assertIn("never invent one", body)


class SecretsAreLocatedNeverQuoted(unittest.TestCase):
    """The document is committed, and pasted logs are the likeliest carrier in the extension."""

    def test_the_rule_is_stated(self):
        self.assertIn("a secret is located and described, never quoted", lower())

    def test_it_covers_fragments_too(self):
        self.assertIn("in whole or in fragment", lower())

    def test_over_withholding_is_named_as_the_correct_error(self):
        self.assertIn("over-withholding is the correct error to make", lower())

    def test_the_substitution_is_disclosed(self):
        self.assertIn("say in the session that you substituted it", lower())


class TheNonInteractiveModeIsStated(unittest.TestCase):
    def test_it_proceeds_and_writes(self):
        self.assertIn("proceed on repository evidence alone and **write the document**", flat().lower())

    def test_unanswered_questions_become_recorded_gaps(self):
        self.assertIn("record every unanswered question as an open data gap", lower())

    def test_it_is_not_a_licence_to_guess(self):
        self.assertIn("not a licence to guess", lower())


class TheBudgetsAreStated(unittest.TestCase):
    def test_the_question_cap_is_five(self):
        self.assertIn("**at most five questions**", flat().lower())

    def test_the_hypothesis_tree_has_at_least_five_branches(self):
        self.assertIn("at least **five major branches**", flat().lower())

    def test_the_issue_tree_has_at_least_four_branches(self):
        self.assertIn("at least four major branches", lower())

    def test_each_question_states_its_stakes(self):
        self.assertIn("state why each one matters", lower())

    def test_reaching_a_cap_is_disclosed(self):
        self.assertIn("a **disclosure**, never a silent stop", flat().lower())

    def test_the_root_question_does_not_count_against_the_budget(self):
        self.assertIn("does not count against the question budget", lower())


class ItMakesNoOtherNetworkRequest(unittest.TestCase):
    def test_the_outbound_surface_is_bounded_to_the_named_retrieval(self):
        self.assertIn("is the entire outbound surface", lower())

    def test_it_accepts_no_repository_url_to_clone(self):
        self.assertIn("no repository url accepted for cloning", lower())


class ReflectionRefusesToInventAnAssessment(unittest.TestCase):
    def test_all_four_dimensions_are_named(self):
        body = lower()
        for dimension in (
            "analysis depth",
            "hypothesis discipline",
            "data-gap closure",
            "answer-first structure",
        ):
            with self.subTest(dimension=dimension):
                self.assertIn(dimension, body)

    def test_it_requires_a_concrete_improvement(self):
        self.assertIn("at least one concrete, specific improvement", lower())

    def test_it_declines_when_there_is_nothing_to_reflect_on(self):
        self.assertIn("say there is nothing to reflect on", lower())


class MethodologyIsAppliedNotReproduced(unittest.TestCase):
    """The BRD's copyright constraint, restated where a reader of the command will meet it."""

    def test_it_forbids_reproducing_the_source_texts(self):
        self.assertIn("never reproduce substantial portions of the copyrighted texts", lower())


class TheTemplateCarriesStructureOnly(unittest.TestCase):
    """Principle VIII's division of labour: sections belong to the template, rules to the command."""

    def test_the_template_ships(self):
        self.assertTrue(TEMPLATE.is_file(), "spectra/templates/defect-rca-template.md does not exist")

    def test_the_template_carries_no_command_owned_rule(self):
        body = TEMPLATE.read_text(encoding="utf-8").lower()
        for rule in ("title similarity", "undeterminable", "layer 2", "$arguments"):
            with self.subTest(rule=rule):
                self.assertNotIn(
                    rule,
                    body,
                    f"the template carries {rule!r}; that rule stays with the command so an override "
                    "cannot switch it off",
                )

    def test_the_command_lists_the_rules_that_survive_an_override(self):
        self.assertIn("the rules that survive any template", lower())

    def test_a_template_cannot_disable_a_safety_rule(self):
        self.assertIn("an override that could disable a safety rule", lower())

    def test_an_omitted_section_is_reported_rather_than_reinstated(self):
        self.assertIn("report the omission rather than reinstating it", lower())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
