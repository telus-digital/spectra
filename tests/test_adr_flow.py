"""The `adr` constitution handoff rules, asserted against the command text that ships.

A command file is a prompt: its text *is* the implementation, so the enforceable surface is what it
says. These assertions cannot prove an agent behaves correctly at run time. What they prove is that the
rules it is supposed to follow have not been quietly deleted.

The rules pinned here (spec 037):

- **It never writes the constitution.** Before 1.26.0 the ADR agent edited
  `.specify/memory/constitution.md` when the user agreed, which skipped the version bump, the sync impact
  report, and the propagation that `/speckit-constitution` owns. It now drafts and hands off, like the
  other four feeders.
- **A significant decision becomes records, one approval step, and two sections.** Constitution
  guardrails holds every record offered; Constitution input holds only what was accepted, because
  `/speckit-constitution` adopts everything in it.
- **The handoff is a printed line that names the ADR.** None when nothing was accepted, and none when no
  constitution exists — that goal is `pending`.
- **Sibling ground is referred, never drafted.** Each constitution clause keeps one source. Ground shared
  with domain-analyzer is settled clause by clause, and a superseded or deprecated ADR never constrains.
- **Supersession amends.** A decision that reverses one already in the constitution drafts `amends:`.

Where the ADR lives and which template it uses are asserted in `test_doc_output_paths.py` and
`test_document_templates.py`.

Standard library only, like the rest of the suite.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import helpers as h  # noqa: E402

COMMAND = h.repo_file("spectra", "commands", "adr.md")


def flat(text: str) -> str:
    """Lowercased, with every run of whitespace collapsed, so hard-wrapped prose can be matched."""
    return " ".join(text.lower().split())


def command() -> str:
    return flat(COMMAND.read_text(encoding="utf-8"))


def section(heading: str) -> str:
    """The flattened body of one `## ` section of the command.

    Step 7 shows the ADR's own `## Constitution input` heading inside a fenced example, so a `## ` line
    inside a code fence does not end the section.
    """
    lines = COMMAND.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(heading))
    body, fenced = [lines[start]], False
    for line in lines[start + 1 :]:
        if line.startswith("```"):
            fenced = not fenced
        elif line.startswith("## ") and not fenced:
            break
        body.append(line)
    return flat("\n".join(body))


class WhatItNeverDoes(unittest.TestCase):
    def test_the_constitution_is_never_written(self):
        text = section("## What this command never does")
        self.assertIn("write `.specify/memory/constitution.md` — in any run, approved or not", text)
        self.assertIn("`/speckit-constitution` owns that file", text)

    def test_the_constitution_command_is_never_invoked(self):
        self.assertIn("invoke `/speckit-constitution`", section("## What this command never does"))

    def test_no_sentence_offers_to_edit_the_constitution(self):
        text = command()
        for phrase in (
            "offer to make the edit",
            "only modify `.specify/memory/constitution.md` if the user agrees",
            "if a constitution update was made",
        ):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)


class TheSignificanceTestIsUnchanged(unittest.TestCase):
    def test_the_three_conditions_remain(self):
        text = section("## Step 7")
        for condition in (
            "cross-cutting standard or principle",
            "contradicts, narrows, or extends an existing constitution principle",
            "establishes a convention future work is expected to follow",
        ):
            with self.subTest(condition=condition):
                self.assertIn(condition, text)


class TheRecord(unittest.TestCase):
    def test_keys_appear_in_order(self):
        text = section("## Step 7")
        keys = (
            "id: `adr-nnn-<section-slug>-<hash>`",
            "section: <target constitution section>",
            "basis: observed | aspirational",
            "decision: accepted | declined | skipped | not_asked",
            "status: new | amends: <principle name/number> | adopted: <principle name/number>",
        )
        positions = []
        for key in keys:
            with self.subTest(key=key):
                self.assertIn(key, text)
                positions.append(text.index(key))
        self.assertEqual(positions, sorted(positions))

    def test_the_id_is_frozen(self):
        text = section("## Step 7")
        self.assertIn("computed once, when first drafted, and frozen", text)
        self.assertIn("a reword at the gate keeps the id", text)


class TheGate(unittest.TestCase):
    def test_every_record_is_shown_then_one_question(self):
        text = section("## Step 7")
        self.assertIn("show every drafted record", text)
        for outcome in (
            "approve",
            "revise the adr first",
            "talk it through",
            "decline the whole gate",
            "no answer, or a non-interactive run",
        ):
            with self.subTest(outcome=outcome):
                self.assertIn(outcome, text)

    def test_only_a_human_choice_adopts(self):
        text = section("## Step 7")
        self.assertIn("`skipped`", text)
        self.assertIn("`not_asked`", text)
        self.assertIn("silence adopts nothing", text)

    def test_the_gate_is_outside_the_five_questions(self):
        self.assertIn("does not count against the five clarifying questions", section("## Step 7"))


class TheSections(unittest.TestCase):
    def test_guardrails_hold_every_record(self):
        text = section("## Step 7")
        self.assertIn("## constitution guardrails", text)
        self.assertIn("every drafted record, accepted or not", text)

    def test_input_holds_only_accepted_records(self):
        text = section("## Step 7")
        self.assertIn("## constitution input", text)
        self.assertIn("exactly the records whose `decision` is `accepted`", text)
        for opener in ("constitution check:", "adr status at drafting:", "goal:"):
            with self.subTest(opener=opener):
                self.assertIn(opener, text)

    def test_the_format_belongs_to_the_command(self):
        text = section("## Step 7")
        self.assertIn("where the resolved template places either heading", text)
        self.assertIn("after the template's last section", text)
        self.assertIn("say so once", text)

    def test_a_decision_that_is_not_significant_gets_no_section(self):
        self.assertIn("write no constitution section", section("## Step 7"))

    def test_the_sections_go_into_the_same_adr(self):
        self.assertIn("the adr you wrote in step 6", section("## Step 7"))


class TheHandoff(unittest.TestCase):
    def test_the_amend_line_names_and_cites_the_adr(self):
        text = section("## Step 7")
        self.assertIn(
            '/speckit-constitution amend the constitution with every guardrail in the "constitution input" section of',
            text,
        )
        self.assertIn("cite adr-nnn as the source of each change", text)
        self.assertIn("resolved root, not the default", text)

    def test_nothing_reaches_the_constitution_until_it_runs(self):
        self.assertIn("nothing reaches the constitution until that command runs", section("## Step 7"))

    def test_the_command_is_printed_not_invoked(self):
        self.assertIn("do not invoke it", section("## Step 7"))

    def test_nothing_accepted_gives_no_command(self):
        self.assertIn("if nothing was accepted, say so and give no command", section("## Step 7"))


class NoConstitution(unittest.TestCase):
    def test_the_goal_is_pending_and_no_command_is_given(self):
        text = section("## Step 7")
        self.assertIn("goal: **pending** — no constitution exists; these records are for a later amend.", text)
        self.assertIn("give no command", text)

    def test_the_user_is_pointed_to_the_domain_analyzer_first(self):
        text = section("## Step 7")
        self.assertIn("`speckit.spectra.domain-analyzer` first", text)
        self.assertIn("once a constitution exists", text)


class AProposedAdr(unittest.TestCase):
    def test_it_hands_off_with_advice(self):
        self.assertIn("run it once the decision is accepted", section("## Step 7"))


class SiblingGroundIsReferred(unittest.TestCase):
    OWN_GROUND = (
        "architecture-level choices",
        "datastores",
        "messaging",
        "architecture style",
        "service and data boundaries",
        "layering",
        "integration patterns",
        "security, data handling, or reliability",
        "governed clause by clause",
    )
    OWNERS = (
        ("speckit.spectra.test-strategy", ("test levels", "coverage floor", "ratchet", "uat")),
        (
            "speckit.spectra.deployment-strategy",
            ("environments", "promotion", "rollback", "versioning scheme", "release cut", "hotfix promotion"),
        ),
        (
            "speckit.spectra.domain-analyzer",
            ("languages", "frameworks", "runtimes", "dependency policy", "bounded contexts", "invariants",
             "glossary"),
        ),
        (
            "speckit.spectra.methodology",
            ("methodology overlays", "work modes", "branching", "review gates", "change records"),
        ),
    )

    def test_its_own_ground_is_stated(self):
        text = section("## Step 7")
        for ground in self.OWN_GROUND:
            with self.subTest(ground=ground):
                self.assertIn(ground, text)

    def test_each_owner_and_its_ground_is_named(self):
        text = section("## Step 7")
        for owner, grounds in self.OWNERS:
            for ground in grounds:
                with self.subTest(owner=owner, ground=ground):
                    self.assertIn(owner, text)
                    self.assertIn(ground, text)

    def test_sibling_ground_is_referred_not_drafted(self):
        text = section("## Step 7")
        self.assertIn("draft nothing on another feeder's ground", text)
        self.assertIn("name the owner", text)
        self.assertIn("whether its document exists", text)
        self.assertIn("re-run", text)
        self.assertIn("read only records whose `decision` is `accepted`", text)

    def test_a_mixed_decision_drafts_only_its_own_part(self):
        self.assertIn("drafts only the architecture-level part", section("## Step 7"))

    def test_a_superseded_or_deprecated_adr_never_constrains(self):
        text = section("## Step 7")
        self.assertIn("`superseded` or `deprecated`", text)
        self.assertIn("only as the principle a supersession amends", text)


class SupersessionAmends(unittest.TestCase):
    def test_a_superseding_adr_amends_its_predecessors_principle(self):
        text = section("## Step 7")
        self.assertIn("when step 5 recorded a supersession", text)
        self.assertIn("draft the new record as `amends: <that principle>`", text)

    def test_an_embedded_guardrail_is_quoted_not_drafted(self):
        text = section("## Step 7")
        self.assertIn("quote the governing clause; draft nothing", text)

    def test_a_contradiction_is_surfaced_never_silently_overridden(self):
        text = section("## Step 7")
        self.assertIn("surface the contradiction as a finding", text)
        self.assertIn("never draft a clause that silently overrides one", text)

    def test_step_five_points_to_step_seven(self):
        self.assertIn("step 7 drafts the matching constitution amendment", section("## Step 5"))


class StepEight(unittest.TestCase):
    def test_the_constitution_is_never_staged(self):
        text = section("## Step 8")
        self.assertNotIn("constitution.md", text)
        self.assertIn("superseded", text)


class NoStaleProse(unittest.TestCase):
    """037 R4 — no hand-written description still says the ADR agent edits the constitution."""

    def agents_list_block(self) -> str:
        text = h.repo_file("AGENTS_LIST.md").read_text(encoding="utf-8")
        start = text.index("<!-- SPECTRA:AGENT id=adr -->")
        return flat(text[start : text.index("<!-- SPECTRA:AGENT id=", start + 1)])

    def landing_card(self) -> str:
        text = h.repo_file("docs", "getting-started", "agents.html").read_text(encoding="utf-8")
        start = text.index('<span class="name">speckit.spectra.adr</span>')
        return flat(text[start : text.index("</span>", text.index('class="cdesc"', start))])

    def extension_readme(self) -> str:
        text = h.repo_file("spectra", "README.md").read_text(encoding="utf-8")
        start = text.index("## `speckit.spectra.adr`")
        return flat(text[start : text.index("\n## ", start + 1)])

    def test_the_customization_module_teaches_the_handoff(self):
        """037 T029 — the e-learning ADR gate described the pre-1.26.0 edit-on-agreement behaviour."""
        text = flat(h.repo_file("docs", "e-learning", "customization.html").read_text(encoding="utf-8"))
        self.assertNotIn("edits the constitution only if you agree", text)
        self.assertIn("never edited the constitution", text)

    def test_each_surface_names_the_handoff(self):
        for name, text in (
            ("AGENTS_LIST.md", self.agents_list_block()),
            ("docs/getting-started/agents.html", self.landing_card()),
            ("spectra/README.md", self.extension_readme()),
        ):
            with self.subTest(surface=name):
                self.assertIn("/speckit-constitution", text)

    def test_no_surface_says_it_edits_the_constitution(self):
        for name, text in (
            ("AGENTS_LIST.md", self.agents_list_block()),
            ("docs/getting-started/agents.html", self.landing_card()),
            ("spectra/README.md", self.extension_readme()),
        ):
            for phrase in ("flags any constitution update", "offers to make it"):
                with self.subTest(surface=name, phrase=phrase):
                    self.assertNotIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
