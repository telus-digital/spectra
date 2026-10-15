"""The `domain-analyzer` re-run and handoff rules, asserted against the command text that ships.

A command file is a prompt: its text *is* the implementation, so the enforceable surface is what it
says. These assertions cannot prove an agent behaves correctly at run time. What they prove is that the
rules it is supposed to follow have not been quietly deleted.

The rules pinned here are the ones that keep a re-run from undoing an SME's review:

- **An ID is frozen once written.** The ID is derived from the statement, so recomputing it after an SME
  rewords a guardrail would make the reworded item look new, and the original wording would come back.
- **A fresh candidate is matched by ID or by intent, against every existing item.** Including unchecked
  ones: an item left unticked is a decision, and offering it again asks the SME to reject it twice.
- **A checked item the constitution already carries is marked `adopted`, and the handoff skips it.**
  Without that, running the `/speckit-constitution` prompt a second time adopts the same guardrail
  twice.

Where the file lives is asserted in `test_doc_output_paths.py`, with the other singletons.

Standard library only, like the rest of the suite.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import helpers as h  # noqa: E402

COMMAND = h.repo_file("spectra", "commands", "domain-analyzer.md")
TEMPLATE = h.repo_file("spectra", "templates", "domain-analysis-template.md")


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


class IdentifiersAreFrozen(unittest.TestCase):
    def test_an_id_is_never_recomputed_from_the_current_statement(self):
        text = section("## Step 3")
        self.assertIn("frozen from then on", text)
        self.assertIn("never recompute it from the statement currently on the checkbox line", text)

    def test_existing_items_are_indexed_by_their_recorded_id(self):
        self.assertIn("by their recorded `id`", section("## Step 5"))

    def test_the_old_edited_means_new_rule_is_gone(self):
        """The rule that made a reworded guardrail resurface as new must not come back."""
        self.assertNotIn("its content-derived id changes; treat that as a new candidate", command())


class FreshCandidatesAreMatchedBeforeTheyAreNew(unittest.TestCase):
    def test_a_regenerated_original_wording_matches_by_id(self):
        self.assertIn("regenerated its original wording", section("## Step 5"))

    def test_a_reworded_guardrail_matches_by_intent_within_its_section(self):
        text = section("## Step 5")
        self.assertIn("same target section and asserts the **same intent**", text)

    def test_matching_covers_unchecked_items(self):
        text = section("## Step 5")
        self.assertIn("checked, unchecked, edited, or adopted", text)
        self.assertIn("asks them to reject it twice", text)

    def test_no_existing_candidate_is_ever_deleted(self):
        self.assertIn("never delete an existing candidate", section("## Step 5"))


class AdoptedItemsAreMarkedAndSkipped(unittest.TestCase):
    def test_a_rerun_marks_checked_items_the_constitution_carries(self):
        text = section("## Step 6")
        self.assertIn("existing checked (`- [x]`)", text)
        self.assertIn("`adopted: <principle name/number>`", text)

    def test_an_unchecked_item_is_never_marked_adopted(self):
        self.assertIn("leave an unchecked item's status alone", section("## Step 6"))

    def test_an_adopted_item_is_never_reverted(self):
        text = section("## Step 6")
        self.assertIn("is **never reverted**", text)
        self.assertIn("report the drift", text)

    def test_status_is_the_only_field_a_rerun_may_change(self):
        self.assertIn("the single exception is the `status` line", section("## Step 5"))

    def test_the_handoff_contract_excludes_adopted_items(self):
        text = section("## Handoff contract")
        self.assertIn("whose status is not `adopted: …`", text)

    def test_the_ready_prompt_excludes_adopted_items(self):
        self.assertIn('that are not marked "status: adopted"', section("## Step 7"))

    def test_no_prompt_is_given_when_nothing_is_left_to_adopt(self):
        self.assertIn("if no checked item is left to adopt", section("## Step 7"))

    def test_the_template_offers_the_adopted_status(self):
        self.assertIn("adopted: <Principle name/number>", TEMPLATE.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
