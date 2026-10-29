"""Next-step suggestions (spec 041), asserted against the manifest and the command text that ships.

A command file is a prompt: its text *is* the implementation, so the enforceable surface is what it
says. These assertions cannot prove what a user sees at run time — that is the manual pass in
specs/041-next-step-suggestions/quickstart.md. What they prove is that the rules have not been quietly
deleted or bent, which is the regression that actually happens to prompt files and manifests.

Spectra suggests what comes next in two ways, and this module pins the line between them:

- **After a core Spec Kit command, a hook.** The set is closed: four events, six entries, every one an
  offer. Spec Kit's command templates show an event's hooks in list order and do not sort by priority, so
  list order is asserted directly and priority only has to agree with it.
- **After a Spectra agent, a closing suggestion** written from how the run turned out. Three agents gain
  one, in a shared layout that names Spec Kit's specify command rather than spelling it for one agent
  (Principle III). The other seven agents' endings are untouched.

Standard library only, like the rest of the suite.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import helpers as h  # noqa: E402

MANIFEST = h.repo_file("spectra", "extension.yml")

# A top-level event key inside `hooks:` — two spaces, an `after_` name, a colon, nothing else.
EVENT = re.compile(r"^  (after_[a-z_]+):[ \t]*$", re.M)
FIELD = re.compile(r"^[ \t]*(?:-[ \t]+)?(command|optional|priority|prompt|description|condition):[ \t]*(.*)$")

EXPECTED = {
    "after_specify": ["speckit.spectra.test-plan"],
    "after_clarify": ["speckit.spectra.test-plan"],
    "after_implement": ["speckit.converge", "speckit.spectra.uat", "speckit.spectra.create-pr"],
    "after_converge": ["speckit.spectra.uat"],
}

CONVERGE_PROMPT = "Check the build against the spec, plan, and tasks for work that is still unbuilt?"
AFTER_CONVERGE_PROMPT = (
    "Run UAT now? If converge just added tasks, finish them with implement first — "
    "UAT will tell you if any are still open."
)
AFTER_CLARIFY_PROMPT = (
    "Build or refresh the test plan from the clarified spec? "
    "It uses the feature this clarify run worked on, so no path is needed."
)

# What every new closing suggestion says, whichever agent carries it.
SHARED_LAYOUT = (
    "**next step**",
    "spec kit's specify command",
    "in whatever invocation syntax this agent uses",
    "the prompt is the only content of its code block",
    "the block runs nothing and asks no question",
)

UNCHANGED = ("adr", "brd", "domain-analyzer", "methodology", "test-strategy", "deployment-strategy", "kb-vault")


def manifest() -> str:
    return MANIFEST.read_text(encoding="utf-8")


def hooks_block() -> str:
    return manifest().partition("\nhooks:")[2].partition("\ntags:")[0]


def event_names() -> list[str]:
    return EVENT.findall(hooks_block())


def event_block(name: str) -> str:
    """One event's text, from its key to the next event key (or the end of the hooks block)."""
    text = hooks_block()
    match = re.search(rf"^  {re.escape(name)}:[ \t]*$", text, re.M)
    if not match:
        return ""
    following = EVENT.search(text, match.end())
    return text[match.end():following.start() if following else len(text)]


def entries(name: str) -> list[dict]:
    """The entries under one event, as dicts of the fields they set.

    The manifest uses two shapes: a single mapping (`after_specify:` then `command:` at four spaces) and
    a list (`after_implement:` then `- command:` items). Both are read here without a YAML library.
    """
    lines = [line for line in event_block(name).splitlines() if not line.strip().startswith("#")]
    chunks: list[list[str]] = []
    for line in lines:
        if re.match(r"^    - ", line) or not chunks:
            chunks.append([])
        chunks[-1].append(line)
    result = []
    for chunk in chunks:
        fields = {}
        for line in chunk:
            match = FIELD.match(line)
            if match:
                fields[match.group(1)] = match.group(2).strip().strip('"')
        if "command" in fields:
            result.append(fields)
    return result


def comments() -> str:
    return flat(" ".join(line.strip().lstrip("#") for line in hooks_block().splitlines()
                         if line.strip().startswith("#")))


def command_text(agent_id: str) -> str:
    return h.repo_file("spectra", "commands", f"{agent_id}.md").read_text(encoding="utf-8")


def flat(text: str) -> str:
    """Lowercased, whitespace collapsed — so an assertion survives a re-wrap of the prose."""
    return " ".join(text.split()).lower()


def section(agent_id: str, heading: str) -> str:
    """One `## ` section of a command, flattened: from its heading to the next `## ` heading."""
    text = command_text(agent_id)
    start = text.index(heading)
    end = text.find("\n## ", start + len(heading))
    return flat(text[start:end if end != -1 else len(text)])


class TheManifestHeaderIsAccurate(unittest.TestCase):
    """FR-004, FR-009 — the floor, and what the comments say about ordering."""

    def test_the_spec_kit_floor_is_the_first_release_with_converge(self):
        version = re.search(r'^  speckit_version:[ \t]*"([^"]+)"', manifest(), re.M)
        self.assertIsNotNone(version, "requires.speckit_version not found")
        self.assertEqual(version.group(1), ">=0.11.2")

    def test_the_comments_say_list_order_sets_what_users_see(self):
        text = comments()
        self.assertIn("list order", text)
        self.assertIn("priority does not set it", text)

    def test_the_comments_make_no_claim_that_spec_kit_sorts_by_priority(self):
        self.assertNotIn("sorts on", comments())


class AfterImplementOffersConvergeFirst(unittest.TestCase):
    """US1 — FR-001, FR-002, FR-003, FR-006, FR-010."""

    def test_the_order_is_converge_then_uat_then_create_pr(self):
        self.assertEqual([e["command"] for e in entries("after_implement")], EXPECTED["after_implement"])

    def test_every_entry_is_an_offer_with_no_condition(self):
        for entry in entries("after_implement"):
            with self.subTest(command=entry["command"]):
                self.assertEqual(entry.get("optional"), "true")
                self.assertNotIn("condition", entry)

    def test_priorities_rise_with_list_position(self):
        priorities = [int(e["priority"]) for e in entries("after_implement")]
        self.assertEqual(priorities, sorted(set(priorities)), "priority must strictly increase in list order")

    def test_the_converge_prompt(self):
        self.assertEqual(entries("after_implement")[0].get("prompt"), CONVERGE_PROMPT)

    def test_the_converge_entry_records_its_core_command_dependency(self):
        block = event_block("after_implement")
        comment = flat(" ".join(line.strip().lstrip("#") for line in block[:block.index("- command: speckit.converge")]
                                .splitlines() if line.strip().startswith("#")))
        self.assertIn("core spec kit command", comment)
        self.assertIn("does not document", comment)

    def test_no_prompt_names_a_path(self):
        for entry in entries("after_implement"):
            with self.subTest(command=entry["command"]):
                self.assertNotIn("specs/", entry.get("prompt", ""))
                self.assertNotIn("SPEC_FILE", entry.get("prompt", ""))


class AfterConvergeOffersUat(unittest.TestCase):
    """US2 — FR-001, FR-002, FR-007."""

    def test_it_offers_uat_and_nothing_else(self):
        found = entries("after_converge")
        self.assertEqual([e["command"] for e in found], EXPECTED["after_converge"])
        self.assertEqual(found[0].get("optional"), "true")
        self.assertNotIn("condition", found[0])

    def test_the_prompt_reads_true_for_both_converge_outcomes(self):
        self.assertEqual(entries("after_converge")[0].get("prompt"), AFTER_CONVERGE_PROMPT)


class UatStillGuardsAnEarlyRun(unittest.TestCase):
    """US2 — FR-008: an early UAT run after converge appended tasks is caught by the UAT agent itself."""

    def test_the_implementation_incomplete_gate_survives(self):
        gate = section("uat", "## Step 3 — The gates")
        for phrase in ("**implementation incomplete.**",
                       "count the tasks outside the uat phase that are still unchecked",
                       "give the count, and ask whether to go on"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, gate)


class AfterClarifyOffersTheTestPlan(unittest.TestCase):
    """US3 — FR-001, FR-002, FR-005."""

    def test_it_offers_the_test_plan_and_nothing_else(self):
        found = entries("after_clarify")
        self.assertEqual([e["command"] for e in found], EXPECTED["after_clarify"])
        self.assertEqual(found[0].get("optional"), "true")
        self.assertNotIn("condition", found[0])

    def test_the_prompt_needs_no_path(self):
        prompt = entries("after_clarify")[0].get("prompt", "")
        self.assertEqual(prompt, AFTER_CLARIFY_PROMPT)
        self.assertNotIn("specs/", prompt)
        self.assertNotIn("SPEC_FILE", prompt)


class DefectRcaOffersAFixSpec(unittest.TestCase):
    """US4 — FR-011, FR-012, FR-013."""

    STEP = "## Step 13 — Report"

    def test_the_report_carries_the_shared_layout(self):
        report = section("defect-rca", self.STEP)
        for phrase in SHARED_LAYOUT:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, report)

    def test_it_offers_only_for_a_validated_cause_and_cites_it(self):
        report = section("defect-rca", self.STEP)
        for phrase in ("a hypothesis reached `validated`", "the document path", "the validated cause",
                       "its layer", "corrective actions"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, report)

    def test_a_layer_two_cause_is_labelled_as_such(self):
        self.assertIn("label it the immediate technical cause", section("defect-rca", self.STEP))

    def test_no_validated_cause_says_why(self):
        self.assertIn("none: no cause was validated, so there is nothing yet to specify a fix for",
                      section("defect-rca", self.STEP))

    def test_exploration_prints_no_block(self):
        self.assertIn("no next step block — exploration writes nothing",
                      section("defect-rca", "## Exploration mode"))

    def test_non_interactive_still_prints_it(self):
        self.assertIn("the next step block is still printed", section("defect-rca", "## Non-interactive mode"))


class FlakyDetectorOffersSpecsForUnappliedFixes(unittest.TestCase):
    """US5 — FR-011, FR-014, FR-015."""

    STEP_9 = "## Step 9 — Report what you did"

    def test_the_report_carries_the_shared_layout(self):
        report = section("flaky-test-detector", self.STEP_9)
        for phrase in SHARED_LAYOUT:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, report)

    def test_it_offers_only_rows_a_spec_can_act_on(self):
        report = section("flaky-test-detector", self.STEP_9)
        for phrase in ("production code", "guardrail", "not confident",
                       "rows the developer deleted are never offered"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, report)

    def test_the_prompt_lists_each_row_and_cites_the_analysis(self):
        report = section("flaky-test-detector", self.STEP_9)
        for phrase in ("ft-nnn", "proposed fix", "the recorded reason", ".specify/memory/flaky-test-analysis.md"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, report)

    def test_the_no_offer_lines(self):
        report = section("flaky-test-detector", self.STEP_9)
        for phrase in ("none: every proposed fix was applied",
                       "none: the remaining rows no longer point at a test or evidence a spec could act on"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, report)
        self.assertIn("none: nothing was proposed",
                      section("flaky-test-detector", "## Step 10 — When there is nothing to act on"))
        self.assertIn("none: every proposed fix was applied",
                      section("flaky-test-detector", "## Step 1b — The last run finished everything"))

    def test_declining_gate_two_offers_every_open_row(self):
        gate_2 = section("flaky-test-detector", "## Step 7 — Gate 2: ask before touching any code")
        self.assertIn("every row still open", gate_2)
        # Step 9's why line — "beyond what this agent may apply" — is false after a decline.
        self.assertIn("you chose not to have these fixes applied here", gate_2)

    def test_declining_gate_one_prints_no_block(self):
        self.assertIn("no next step block follows",
                      section("flaky-test-detector", "## Step 5 — Gate 1: ask before writing anything"))


class ImpactNamesThePathToASpec(unittest.TestCase):
    """US6 — FR-011, FR-016, FR-017."""

    STEP = "## Step 14 — Report"

    def test_the_report_carries_the_shared_layout(self):
        report = section("impact", self.STEP)
        for phrase in SHARED_LAYOUT:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, report)

    def test_the_pointer_is_conditional_and_never_judges(self):
        report = section("impact", self.STEP)
        for phrase in ("if they approve", "whatever the rating",
                       "never states, implies, or predicts the decision",
                       "a prediction of the stakeholders' decision"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, report)

    def test_the_prompt_carries_the_analysis(self):
        report = section("impact", self.STEP)
        for phrase in ("feature name", "analysis path", "rating and its trigger", "external contract changes",
                       "findings, risks, and open questions"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, report)

    def test_status_stays_draft(self):
        self.assertIn("`status` is `draft` on every run", flat(command_text("impact")))

    def test_it_still_writes_no_spec_and_records_no_reference(self):
        row = next(flat(line) for line in command_text("impact").splitlines()
                   if line.startswith("| Create, reference, or link a specification"))
        for phrase in ("nothing under `specs/` is written", "spec_refs",
                       "a pointer to spec kit's specify command in the session report is permitted"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, row)


class TheHookSetIsExactly(unittest.TestCase):
    """FR-001, FR-002 — four events, six entries, every one an offer."""

    def test_the_events(self):
        self.assertEqual(set(event_names()), set(EXPECTED))
        self.assertEqual(len(event_names()), len(EXPECTED), "an event key appears twice")

    def test_the_commands_per_event(self):
        for event, commands in EXPECTED.items():
            with self.subTest(event=event):
                self.assertEqual([e["command"] for e in entries(event)], commands)

    def test_no_hook_is_mandatory_or_conditional(self):
        block = hooks_block()
        self.assertNotIn("optional: false", block)
        self.assertNotRegex(block, r"(?m)^[ \t]*-?[ \t]*condition:")


class TheOtherAgentsAreUnchanged(unittest.TestCase):
    """FR-018, FR-019 — the shared layout is not applied elsewhere, and kb-vault never feeds the constitution."""

    def test_kb_vault_never_suggests_the_constitution_command(self):
        text = command_text("kb-vault")
        self.assertNotIn("/speckit-constitution", text)
        self.assertNotIn("/speckit.constitution", text)

    def test_the_shared_layout_is_only_where_this_feature_put_it(self):
        for agent_id in UNCHANGED:
            with self.subTest(agent=agent_id):
                self.assertNotIn("**next step**", flat(command_text(agent_id)))


if __name__ == "__main__":
    unittest.main()
