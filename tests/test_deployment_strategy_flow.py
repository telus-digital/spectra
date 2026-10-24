"""The `deployment-strategy` command's rules, asserted against the command text that ships.

A command file is a prompt: its text *is* the implementation, so the enforceable surface is what it
says. These assertions cannot prove an agent behaves correctly at run time. What they prove is that the
rules it is supposed to follow have not been quietly deleted — the six lenses, the four provenances, the
one-question-per-turn round, the invariants-only amendment, and above all that it never writes the
constitution.

Where the file lives is asserted in `test_doc_output_paths.py`, with the other singletons; which
template shapes it, in `test_document_templates.py`.

Standard library only, like the rest of the suite.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import helpers as h  # noqa: E402

COMMAND = h.repo_file("spectra", "commands", "deployment-strategy.md")
TEMPLATE = h.repo_file("spectra", "templates", "deployment-strategy-template.md")
MANIFEST = h.repo_file("spectra", "extension.yml")

COMMAND_NAME = "speckit.spectra.deployment-strategy"
CONSTITUTION_PATH = ".specify/memory/constitution.md"

LENSES = (
    "Environments & promotion",
    "Pipeline, artifact & traceability",
    "Release & versioning",
    "Data & schema change",
    "Rollback & recovery",
    "Operability & configuration",
)

CLASSES = ("`service`", "`static-site`", "`library`", "`cli-desktop`", "`mobile`", "`infra`")


def command_text() -> str:
    return COMMAND.read_text(encoding="utf-8")


def flat(text: str) -> str:
    """Lowercased, blockquote markers dropped, every run of whitespace collapsed, so hard-wrapped prose
    — including a wrapped blockquote — can be matched."""
    return " ".join(text.replace("\n>", "\n").lower().split())


def has(phrase: str) -> bool:
    return flat(phrase) in flat(command_text())


def front_matter_example() -> str:
    blocks = re.findall(r"```yaml\n(.*?)```", command_text(), re.S)
    return blocks[0] if blocks else ""


class TheCommandIsRegistered(unittest.TestCase):
    def test_the_command_file_exists(self):
        self.assertTrue(COMMAND.is_file())

    def test_the_template_file_exists(self):
        self.assertTrue(TEMPLATE.is_file())

    def test_the_manifest_registers_command_and_template(self):
        manifest = MANIFEST.read_text(encoding="utf-8")
        self.assertIn(f'name: "{COMMAND_NAME}"', manifest)
        self.assertIn('file: "commands/deployment-strategy.md"', manifest)
        self.assertIn('name: "deployment-strategy-template"', manifest)
        self.assertIn('file: "templates/deployment-strategy-template.md"', manifest)

    def test_it_has_front_matter_with_a_description(self):
        text = command_text()
        self.assertTrue(text.startswith("---\ndescription: "))

    def test_it_takes_input_through_the_generic_placeholder(self):
        self.assertIn("$ARGUMENTS", command_text())

    def test_it_runs_with_no_arguments(self):
        self.assertTrue(has("This command requires no arguments."))

    def test_the_one_flag_is_documented(self):
        self.assertIn("`--non-interactive`", command_text())

    def test_an_unknown_flag_is_reported_not_absorbed(self):
        self.assertTrue(has("An unrecognized flag is reported and ignored"))


class TheSixLenses(unittest.TestCase):
    def test_every_lens_is_named(self):
        for lens in LENSES:
            with self.subTest(lens=lens):
                self.assertIn(lens, command_text())

    def test_no_lens_is_omitted(self):
        self.assertTrue(has("Never omit a lens."))

    def test_not_applicable_carries_a_reason(self):
        self.assertTrue(has("**not applicable**, with a one-line reason"))

    def test_brownfield_reports_before_proposing(self):
        self.assertTrue(has("report what exists before proposing anything"))

    def test_conditional_lenses_need_evidence(self):
        for lens in ("Rollout technique", "Multi-region or multi-tenant", "Compliance and audit gates",
                     "Environment cost"):
            with self.subTest(lens=lens):
                self.assertIn(lens, command_text())
        self.assertTrue(has("only where the evidence warrants"))

    def test_the_test_strategy_owns_which_tests_exist(self):
        self.assertIn("TEST_STRATEGY.md", command_text())
        self.assertTrue(has("decides only where they gate"))

    def test_a_missing_test_strategy_is_a_gap_not_a_stop(self):
        self.assertTrue(has("Do not stop, and do not recommend which tests should exist"))
        self.assertIn("`speckit.spectra.test-strategy`", command_text())

    def test_app_rollback_is_not_db_rollback(self):
        self.assertTrue(has("rolling back the application does not roll back the database"))

    def test_recovery_claims_are_drilled_or_assumed(self):
        self.assertTrue(has("**drilled**"))
        self.assertTrue(has("**assumed**"))

    def test_no_floating_tag(self):
        self.assertIn("`latest`", command_text())

    def test_operability_stays_high_level(self):
        self.assertTrue(has("what should be monitored and who owns it"))
        self.assertTrue(has("Alert definitions, thresholds, and runbook procedure"))
        self.assertTrue(has("only on an explicit request"))

    def test_existing_jobs_and_alerts_are_listed_not_redefined(self):
        self.assertTrue(has("list and link them; never redefine them"))


class TheDiagram(unittest.TestCase):
    def test_one_mermaid_flowchart(self):
        self.assertIn("flowchart LR", command_text())

    def test_it_draws_only_what_the_table_states(self):
        self.assertTrue(has("a node or gate with no row in the table is a defect"))

    def test_recommended_environments_are_marked(self):
        self.assertTrue(has("dashed edge labelled `recommended`"))


class TheHonestyRules(unittest.TestCase):
    def test_four_provenances_exactly_one_each(self):
        for label in ("**`verified`**", "**`claimed`**", "**`stated`**", "**`convention`**"):
            with self.subTest(label=label):
                self.assertIn(label, command_text())
        self.assertTrue(has("exactly one of four provenances"))

    def test_an_absence_is_cited(self):
        self.assertTrue(has("An absence is cited too."))

    def test_an_answer_is_an_input_not_a_measurement(self):
        self.assertTrue(has("An answer is an input, not a measurement."))

    def test_open_questions_are_never_invented(self):
        self.assertIn("Open questions / confirmation items", command_text())
        self.assertTrue(has("Never invent a value only the client or ops owner can supply"))

    def test_coverage_of_analysis_is_stated(self):
        self.assertTrue(has("State your own coverage."))

    def test_secrets_are_never_reproduced(self):
        self.assertTrue(has("Never reproduce a secret."))

    def test_it_runs_nothing(self):
        self.assertTrue(has("It runs nothing."))

    def test_no_network(self):
        self.assertTrue(has("Make a network request"))


class TheClarificationRound(unittest.TestCase):
    QUESTIONS = (
        "Where this project is hosted or published",
        "Who approves a production deploy, and how",
        "stakeholder-review or pre-release environment",
        "Availability and RPO/RTO targets",
        "Release cadence",
    )

    def test_the_round_is_its_own_step(self):
        self.assertIn("## Step 4 — The clarification round", command_text())

    def test_the_five_questions_in_order(self):
        text = command_text()
        positions = [text.find(q) for q in self.QUESTIONS]
        self.assertNotIn(-1, positions, f"missing a question: {list(zip(self.QUESTIONS, positions))}")
        self.assertEqual(positions, sorted(positions))

    def test_the_round_is_announced_once(self):
        self.assertTrue(has("Five judgment calls the repository cannot settle, one at a time."))
        self.assertTrue(has("say **use your defaults**"))

    def test_one_question_per_turn(self):
        self.assertTrue(has("**One question per turn.**"))

    def test_numbered_within_the_total(self):
        self.assertIn("Question N of 5", command_text())

    def test_a_recommendation_with_evidence(self):
        self.assertTrue(has("mark exactly one as recommended"))
        self.assertTrue(has("convention, nothing in this project"))

    def test_free_text_is_valid(self):
        self.assertTrue(has("Free text is always valid"))

    def test_settled_questions_are_confirmed_not_dropped(self):
        self.assertTrue(has("turn it into a confirmation and keep its number"))

    def test_once_per_project_not_per_deployable(self):
        self.assertTrue(has("once per project, never once per deployable"))

    def test_question_four_never_offers_a_number(self):
        self.assertTrue(has("never a number you supply"))

    def test_defaults_end_the_round(self):
        self.assertTrue(has("end the round immediately"))

    def test_a_non_answer_re_asks(self):
        self.assertTrue(has("then ask the same question again"))

    def test_it_never_asks_what_it_reads(self):
        self.assertIn("### What you may never ask", command_text())

    def test_dispositions(self):
        self.assertIn("`answered`, `default_taken`, or `not_asked`", command_text())


class NonInteractiveMode(unittest.TestCase):
    def test_declared_never_inferred(self):
        self.assertIn("## Non-interactive mode", command_text())
        self.assertTrue(has("**Never infer it.**"))

    def test_nothing_is_asked_and_everything_is_recorded(self):
        self.assertTrue(has("ask **none** of the five clarification questions"))
        self.assertTrue(has("record every one as **not asked**"))


class TheDocument(unittest.TestCase):
    def test_exactly_one_file(self):
        self.assertTrue(has("Write **exactly one file**"))

    def test_front_matter_rules(self):
        self.assertTrue(has("Front matter is YAML, and it has to parse"))
        self.assertTrue(has("Quote every free-text value"))
        self.assertTrue(has("A key takes a scalar or a collection, never both"))

    def test_an_example_block_is_shown_with_every_key(self):
        block = front_matter_example()
        for key in ("mode:", "generated:", "template:", "run:", "deployables:", "class:",
                    "coverage_of_analysis:", "amendment_state:", "clarification:", "disposition:"):
            with self.subTest(key=key):
                self.assertIn(key, block)

    def test_the_enumerations(self):
        self.assertTrue(has("`greenfield`, `brownfield`, or `mixed`"))
        self.assertTrue(has("`embedded`, `partial`, `absent`, `none`, or `not_asked`"))
        for cls in CLASSES:
            with self.subTest(cls=cls):
                self.assertIn(cls, command_text())

    def test_a_write_failure_stops_before_the_gate(self):
        self.assertTrue(has("If the file cannot be written"))

    def test_the_template_stack(self):
        text = command_text()
        for layer in (".specify/templates/overrides/deployment-strategy-template.md",
                      ".specify/presets/<preset-id>/templates/deployment-strategy-template.md",
                      ".specify/extensions/spectra/templates/deployment-strategy-template.md",
                      ".specify/templates/deployment-strategy-template.md"):
            with self.subTest(layer=layer):
                self.assertIn(layer, text)
        self.assertTrue(has("Honour the resolved template; do not repair it."))
        self.assertTrue(has("Report which template you used"))

    def test_the_template_carries_no_rules(self):
        template = TEMPLATE.read_text(encoding="utf-8").lower()
        self.assertNotIn("never reproduce", template)
        self.assertNotIn("exactly one of four", template)

    def test_the_template_has_every_section(self):
        template = TEMPLATE.read_text(encoding="utf-8")
        for heading in LENSES + ("Open questions / confirmation items", "Proposed constitution amendment"):
            with self.subTest(heading=heading):
                self.assertIn(heading, template)


class TheConstitutionHandoff(unittest.TestCase):
    def test_it_never_writes_the_constitution(self):
        self.assertIn(f"You never write `{CONSTITUTION_PATH}`", command_text())

    def test_the_ban_is_unconditional(self):
        self.assertTrue(has("Not on approval. Not on a re-run. Not when the file is missing. Not when the user insists."))

    def test_it_does_not_create_one_either(self):
        self.assertTrue(has("Create a constitution"))

    def test_the_four_states(self):
        for state in ("**embedded**", "**partial**", "**absent**", "**no constitution**"):
            with self.subTest(state=state):
                self.assertIn(state, command_text())

    def test_semantic_not_keyword(self):
        self.assertTrue(has("Read it **semantically**"))

    def test_contradictions_are_findings(self):
        self.assertTrue(has("surface the contradiction as a finding in its own right"))

    def test_draft_format(self):
        text = command_text()
        self.assertIn("- [ ] <statement in the constitution's voice", text)
        self.assertIn("status: add | amends: <principle name>", text)

    def test_invariants_only(self):
        self.assertTrue(has("durable invariants"))
        self.assertTrue(has("never appear as obligations"))

    def test_three_gate_paths(self):
        for path in ("**Approve it**", "**Modify the strategy first**", "**Talk it through**"):
            with self.subTest(path=path):
                self.assertIn(path, command_text())

    def test_the_ready_to_paste_line(self):
        text = command_text()
        self.assertIn(
            '/speckit-constitution Adopt the checked items in the "Proposed constitution amendment" '
            "section of docs/DEPLOYMENT_STRATEGY.md",
            text,
        )
        self.assertIn("[DEPLOYMENT_STRATEGY.md](docs/DEPLOYMENT_STRATEGY.md)", text)

    def test_it_hands_off_rather_than_invoking(self):
        self.assertIn("Do not invoke `/speckit-constitution` yourself", command_text())

    def test_the_manifest_advertises_the_ban(self):
        manifest = MANIFEST.read_text(encoding="utf-8")
        entry = manifest[manifest.index(f'name: "{COMMAND_NAME}"'):]
        entry = entry[: entry.index("- name:", 1)] if "- name:" in entry[1:] else entry
        self.assertIn("never edits the constitution", entry)


class ReferencedDocuments(unittest.TestCase):
    def test_they_are_inputs_cited_as_claimed(self):
        self.assertTrue(has("Every claim drawn from a referenced document is `claimed`"))

    def test_code_confirmation_promotes_a_claim(self):
        self.assertTrue(has("Where the repository confirms a document's claim, the claim is `verified`"))

    def test_urls_are_never_fetched(self):
        self.assertTrue(has("A URL is never fetched"))

    def test_an_unreadable_document_is_named(self):
        self.assertTrue(has("name it and the reason"))


class ReRuns(unittest.TestCase):
    def test_rewrite_in_place(self):
        self.assertIn("## Re-running on a project you have analysed before", command_text())
        self.assertTrue(has("Never create a second strategy file."))

    def test_prior_answers_are_pre_filled(self):
        self.assertTrue(has("last run you said this; still true?"))

    def test_recommendations_are_marked(self):
        for mark in ("`new`", "`adopted`", "`carried`"):
            with self.subTest(mark=mark):
                self.assertIn(mark, command_text())

    def test_what_changed_is_stated(self):
        self.assertTrue(has("State what changed"))


class OnlyAcceptedDomainGuardrailsShapeGates(unittest.TestCase):
    """A domain analysis records what the SME declined as well as what they accepted (spec 034, FR-022).

    A declined guardrail shaping a deployment gate would enforce a rule the project explicitly rejected.
    """

    def test_only_accepted_entries_shape_a_gate(self):
        self.assertTrue(has("only entries whose `decision` is `accepted`"))
        self.assertTrue(has("a `declined`, `skipped`, or `not_asked` entry never does"))

    def test_a_legacy_checkbox_file_counts_only_ticked_items(self):
        self.assertTrue(has("only `- [x]` items count"))


class NonServiceDeployables(unittest.TestCase):
    def test_the_adaptation_table(self):
        self.assertIn("### How each lens reads for each class", command_text())

    def test_a_library_publishes(self):
        self.assertTrue(has("release channels"))
        self.assertTrue(has("yank"))

    def test_store_review_is_an_uncontrolled_gate(self):
        self.assertTrue(has("store review is a gate the team does not control"))

    def test_two_classes_are_two_deployables(self):
        self.assertTrue(has("matches two classes is two deployables"))

    def test_no_infrastructure_without_evidence(self):
        self.assertTrue(has("Never recommend infrastructure the evidence does not show"))


class TheBranchingModelBelongsToTheMethodology(unittest.TestCase):
    """Spec 035 (E5): one source per clause — deployment keeps the release cut, the scheme, and the hotfix
    promotion; the branching model is the methodology's."""

    def test_release_and_versioning_no_longer_decides_the_branching_model(self):
        row = next(line for line in command_text().splitlines() if line.startswith("| **Release & versioning** |"))
        decides = row.split("|")[2]
        self.assertNotIn("branching model", decides)
        self.assertIn("versioning scheme", decides)
        self.assertIn("ENGINEERING_METHODOLOGY.md", row)
        self.assertIn("speckit.spectra.methodology", row)

    def test_the_methodology_is_read_as_a_sibling(self):
        self.assertTrue(has("`ENGINEERING_METHODOLOGY.md`"))
        self.assertTrue(has("cite it for the branching model"))


if __name__ == "__main__":
    unittest.main()
