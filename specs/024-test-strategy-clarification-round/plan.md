# Implementation Plan: The Test Strategy Clarification Round

**Branch**: `024-test-strategy-clarification-round` | **Date**: 2026-09-12 | **Spec**: [spec.md](./spec.md)

## Summary

One interaction added. `test-strategy` derives its whole document from evidence and stops the user only for mechanical
reasons — where to write, whether to run the suite, whether to approve an amendment. Five judgment calls the repository
cannot settle become a clarification round: a new Step 5, asked one question at a time, each carrying the agent's own
recommendation and the evidence behind it. The coverage-run confirmation moves into that round and is asked first, so
the baseline informs the five. A third provenance marker, `stated`, keeps an answer distinguishable from a citation and
from a convention. Declining every question reproduces the 1.16.0 document exactly.

## Technical Context

**Language/Version**: Markdown command prompt; Python 3.9+ for tests

**Primary Dependencies**: unchanged — Spec Kit `>=0.11.0`. The command still makes no network request and runs nothing
without confirmation

**Testing**: `python3 -m unittest discover -s tests`; `tools/generate_agent_docs.py --check`

**Constraints**: Markdown only; agent-agnostic; the write scope is unchanged at exactly one file; the constitution is
never written; no named browser driver may enter the command's text

**Scale/Scope**: one new step and eight smaller edits in one command, a renumber of eight step headings, two blocks in
one template, one test assertion moved plus one new test class, version sync

## Evidence

| Claim | How it was verified |
|---|---|
| Today's three stops are all mechanical or terminal | `spectra/commands/test-strategy.md` Step 4 (root), Step 7 (coverage run), Step 12 (amendment gate) — no step asks about the strategy |
| Asking what the agent measures is already forbidden, with a reason that generalises | FR-006 and the Clarifications entry at [020-test-strategy-agent/spec.md:33](../020-test-strategy-agent/spec.md) — "asking them for something the agent is about to measure anyway" |
| R1 admits exactly two provenances today | `test-strategy.md:56` — a cited path, or the `convention` marker; a user's answer is neither |
| R5 covers stack capability, not organizational policy | `test-strategy.md:69` plus the tool tiers in Step 6 — a tool is barred when *this surface* lacks its prerequisites, which says nothing about a team that may not adopt it |
| Renumbering breaks exactly one assertion | `tests/test_test_strategy_flow.py:290` hard-codes `## Step 10 — Report`, `## Step 11 — …`, `## Step 12 — …` and asserts increasing order |
| A new top-level section would break three more | `tests/test_test_strategy_flow.py:356` pins the template's ten-section list; `tests/test_document_templates.py:249` requires the inline skeleton to match it; `docs/index.html:534` claims "Ten sections" |
| Comment annotations on skeleton headings are safe to edit | `sections()` at `tests/test_document_templates.py:93` strips trailing annotations before comparing |
| No browser driver may appear in the command | `tests/test_test_strategy_flow.py:184` — a blanket ban on Playwright, Cypress, Selenium, Puppeteer |
| Front matter is command-controlled, not template-shaped | No file under `spectra/templates/` carries YAML front matter; Step 9 of the command specifies its contents |
| The landing page hard-codes no version but does hand-write the blurb | `docs/index.html:645`/`:765` fetch `catalog.json`; `:534`–`:535` are hand-written prose and argument text |

## Constitution Check

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | This spec/plan/tasks set on branch `024-test-strategy-clarification-round`. |
| II. Single Self-Contained Extension | ✅ | No files added to or removed from the package. |
| III. Agent-Agnostic Commands | ✅ | The round is specified as prose — "ask one question, then wait" — and names no agent's turn-taking or prompting syntax. `$ARGUMENTS` still carries the input surface. |
| IV. Context-Aware by Default | ✅ | This is IV strengthened, not weakened. The never-ask list is the point: the command may only ask what it cannot read, and every question must name real paths in this project, which is why the round sits after Steps 1–4 rather than before them. |
| V. Catalog and Package in Sync | ✅ | Manifest, catalog, changelog, and zip move together. The roster is untouched — `agents-list.json` says what an agent is *for*, and the command count stays 11. |
| VI. Two Versioned Channels | ✅ | Extension channel only: 1.16.0 → 1.17.0. No tag; root `VERSION` untouched. |
| VII. Documents Under One Declared Root | ✅ | Unaffected. Root resolution keeps its own step and still precedes the round. |
| VIII. Shaped by Overridable Templates | ✅ | The answer record goes inside an existing section, so the template's section list is unchanged and a project override stays valid. Because VIII lets an override delete that section, the record is duplicated into front matter, which the command owns. |

**Amendment classification**: none.

**Extension version classification**: MINOR — 1.16.0 → 1.17.0. A new interaction and a new argument are added, so
behaviour differs observably; every input that worked before still works, and a user who declines everything gets the
1.16.0 document. Not a patch; not breaking.

## Phase 0 — Decisions

- **D1 — Ask judgment, never measurement.** FR-006's reasoning is the whole design constraint, generalised: a question
  whose answer the agent is about to measure invites a wrong answer to override a right one. The command therefore
  carries an explicit never-ask list — mode, stack, surfaces, frameworks, coverage figure, whether tests exist — so the
  boundary is stated rather than inferred by the next editor.

- **D2 — One question per turn, not a batch of five.** The questions are conditional: whether an external consumer
  exists determines whether the contract lens exists at all, and where the weight sits changes how much the journey
  question matters. A batch forces each question to be written as though the others do not exist, which turns a
  project-specific interview into a questionnaire — the failure Principle IV exists to prevent. The round-trip cost is
  paid back by the escape hatches in D3, not by batching.

- **D3 — Three ways out, announced once.** Answer several at once; take the recommendations wholesale; decline. The
  first preserves the batch for a maintainer who already knows their answers, so the sequential default costs them
  nothing. The second is what makes the feature safe to add at all: the worst case is 1.16.0's behaviour.

- **D4 — Always five; evidence reshapes, never skips.** A fixed count can be announced honestly up front, and the
  length of the commitment is what a user needs to know before the first question. The forcing case is the journey
  question at surface `none`, which is incoherent as an open choice and fine as a confirmation.

- **D5 — `stated` as a third provenance.** This is the load-bearing decision. With only a citation and `convention`
  available, an answer either launders into a fake citation or is mislabelled a convention, and R1 — the rule that
  makes the document trustworthy — quietly stops meaning anything.

- **D6 — An answer is an input, not a measurement.** Given R3 and a user asking for a floor above the baseline, the
  document must hold the baseline. This gets its own rule (R7) rather than a clause inside R1, because it is the
  obvious way the feature could corrupt the document and it needs to be findable.

- **D7 — The coverage confirmation moves into the round and goes first.** Its answer produces the baseline, and "where
  should the weight sit" is a different question at 31% than at 78%. It also collapses two interruptions into one.

- **D8 — No gate before the write.** The document is a singleton rewritten in place with Git carrying the history, and
  the amendment gate already offers "modify the strategy first". A second gate would add a failure path and a second
  non-interactive divergence for a file that costs nothing to rewrite.

- **D9 — The answer record lives inside the sources section.** A new top-level section would break the template's
  pinned section list, the inline skeleton that must match it, and the landing page's section count — for a table whose
  natural home is the section that already carries provenance. The user's answers *are* a source consulted.

- **D10 — Renumber rather than half-number.** Inserting `Step 4a` avoids touching ten cross-references and one test, but
  reads as an afterthought in a document this carefully structured. The renumber is mechanical and the test it breaks
  is pinning ordering, which the renumber preserves.

## Phase 1 — Design notes

`spectra/commands/test-strategy.md`:

1. **New `## Step 5 — The clarification round`**, after root resolution and before template resolution. Carries D1's
   governing line and never-ask list; the one-line announcement from D3; the coverage confirmation moved verbatim from
   Step 7 as question 0 (D7); the five questions, each stating what it settles and which section it changes; D4's
   reshaping rule; the presentation contract; and three handling rules — proceed-with-defaults, mid-flow abandonment,
   and the off-topic reply that re-asks rather than advancing.
2. **Steps 5–12 renumber to 6–13** (D10). Ten `Step N` cross-references; the two at lines 48 and 448 point at the
   coverage confirmation and retarget to the new Step 5, not to Step 8.
3. **The rules that never bend** — R1 gains `stated` (D5); a new R7 carries D6.
4. **`## User Input`** gains `--non-interactive`, matching `test-plan.md`'s treatment: strip the flag, read the
   remainder as the existing focus hint, report and ignore anything unrecognised.
5. **`## What this command never does`** gains a row for letting an answer override a measured or reported figure.
6. **Step 9 → 10 (write)** adds the answers to front matter (D9's redundancy); **Step 10 → 11 (report)** scopes "before
   you ask the user anything" to the amendment, settling the FR-028 tension; **`## Non-interactive mode`** adds the flag
   and the not-asked disposition; **`## Re-running`** pre-fills each question from the prior document; **`## Known
   limitations`** states that `stated` is a claim by the team, not evidence from the repository.
7. **Front matter `description`** names the round, following `brd.md`'s precedent, and retains the phrase
   `never writes the constitution`.

`spectra/templates/test-strategy-template.md`: an **Inputs from the user** table inside
`## Sources consulted and coverage of analysis`; `stated: Q<n>` added to the recommendations summary's evidence
guidance; the "what this template cannot change" block gains the new invariant. The ten `##` headings do not move.

`tests/test_test_strategy_flow.py`: the step literals in `test_the_report_step_precedes_the_constitution_step` shift to
11/12/13, and a new class covers the round — the never-ask list, the three provenances, R3 surviving an answer, the
escape hatches, the non-interactive disposition, and the flag.

Docs: `AGENTS_LIST.md` and `spectra/README.md` prose blocks gain a line on the round; `docs/index.html:534`–`535` gain
the round and the flag, with its "Ten sections" claim still accurate under D9.

## Risks

| Risk | Mitigation |
|---|---|
| The round drifts into asking what the agent should measure | D1's never-ask list is written into the command and asserted by test; the round is placed after Steps 1–4 so the evidence exists before any question does |
| A user's answer is read later as a finding about the repository | D5's `stated` marker, carried through R1, the recommendations table, and the answer record; asserted by test |
| An answer pushes the coverage floor above the baseline | D6's R7 plus R3, which is unchanged and absolute; asserted by test |
| Five sequential questions become an interrogation | D3's three escape hatches, announced before the first question; declining is one reply and costs the 1.16.0 document nothing |
| The renumber leaves a cross-reference pointing at the wrong step | Ten references enumerated in tasks; the two that retarget rather than shift are called out individually |
| A project override deletes the section holding the answer record | D9's front-matter duplication, which the command owns and Principle VIII does not reach |

## Complexity Tracking

> No violations. One step added, one moved question, one new provenance marker; no new file, no new surface, no change
> to what the command may write.
