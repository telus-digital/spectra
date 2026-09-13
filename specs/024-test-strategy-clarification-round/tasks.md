# Tasks: The Test Strategy Clarification Round

**Input**: [spec.md](./spec.md), [plan.md](./plan.md)

**Branch**: `024-test-strategy-clarification-round`

---

## Phase 0 — Verification of the premise

- [X] T001 Confirm all three of today's stops are mechanical or terminal: `spectra/commands/test-strategy.md` Step 4
  (artifact root), Step 7 (coverage run), Step 12 (amendment gate). No step asks about the strategy itself.
- [X] T002 Confirm the never-ask boundary already exists with a stated reason: FR-006 plus the Clarifications entry in
  [020-test-strategy-agent/spec.md](../020-test-strategy-agent/spec.md), which forbids asking the mode because it is
  "something the agent is about to measure anyway" (D1).
- [X] T003 Confirm R1 admits exactly two provenances today — a cited path or `convention` — so a user's answer has no
  honest marker (`test-strategy.md:56`, D5).
- [X] T004 Confirm R5 covers stack capability, not organizational policy: `test-strategy.md:69` plus the Step 6 tool
  tiers bar a tool whose prerequisites *this surface* lacks, and say nothing about a team that may not adopt it.
- [X] T005 Enumerate the test constraints before editing: the step-order literals at `tests/test_test_strategy_flow.py:290`,
  the browser-driver ban at `:184`, the `requires no arguments` literal at `:79`, the manifest phrase
  `never writes the constitution` at `:110`, the template's ten-section list at `:356`, and the skeleton/template
  section agreement at `tests/test_document_templates.py:249`.

**Checkpoint**: the gap is real, the boundary that keeps it honest already exists, and every pinned literal is known.

---

## Phase 1 — User Story 1: the strategy reflects a decision the repository could not make (P1)

- [X] T006 Add `## Step 5 — The clarification round` to `spectra/commands/test-strategy.md`, after Step 4 and before the
  current Step 5, opening with the governing line — ask about judgment, intent and constraint; never ask about anything
  you are about to measure — and the never-ask list naming the mode, the stack, the surfaces, the frameworks in use, the
  coverage figure, and whether tests exist (FR-001, FR-002, D1).
- [X] T007 Add the one-line announcement that precedes the first question: the number of questions and the three ways
  out — answer several at once, take the recommendations wholesale, decline (FR-005, D3).
- [X] T008 Move the coverage-run confirmation out of Step 7 into the round as question 0, asked before the five, keeping
  its existing conditions: name the exact command, warn that the suite executes, make it declinable (FR-007, D7). Leave
  Step 7's provenance table and R4 where they are.
- [X] T009 Write the five questions, each stating what it settles and which document section its answer changes: where
  the weight sits; whether an external consumer exists; which journeys justify end-to-end; what has broken that tests
  did not catch; and what constraints the repository does not show (FR-001).
- [X] T010 Add the presentation contract: one question per turn, numbered within the fixed total, two to four labelled
  options, exactly one marked recommended with the project evidence behind the mark, and free text always valid
  (FR-003, FR-004, D2).
- [X] T011 Add the reshaping rule — where evidence settles a question it becomes a confirmation and keeps its number —
  with the end-to-end `none` case written out as the worked example (FR-006, D4).
- [X] T012 State that the round is placed after root resolution so every question can name real paths in this project
  (FR-008, Principle IV).
- [X] T013 Renumber Steps 5–12 to 6–13 and update all ten `Step N` cross-references. Lines 102 and 333 point at Steps 3
  and 4 and do **not** move; lines 48 and 448 point at the coverage confirmation and retarget to the **new Step 5**,
  not Step 8 (D10).

**Checkpoint**: the round exists, asks only what it cannot measure, and no cross-reference points at the wrong step.

---

## Phase 2 — User Story 2: declining costs nothing (P1)

- [X] T014 Add the three handling rules to Step 5: a request to proceed takes every remaining recommendation and ends
  the round; an unanswered question takes its recommendation and is recorded as not asked; a reply that does not answer
  is addressed and then the same question is asked again, without advancing (FR-015, FR-016, FR-017, D3).
- [X] T015 State that a run in which nothing is answered produces the recommendations the command produced before this
  feature (FR-018).
- [X] T016 Add `--non-interactive` to `## User Input`, matching `spectra/commands/test-plan.md:37`: strip the flag, read
  the remainder as the existing focus hint, report and ignore an unrecognised flag. Keep the sentence
  `requires no arguments`, which stays true and is pinned by test (FR-019).
- [X] T017 Extend `## Non-interactive mode`: add `--non-interactive` to the detection list, ask none of the five, record
  each as not asked with the default taken, and retarget the Step 7 reference from T013 (FR-020).
- [X] T018 Extend `## Re-running`: read the prior document's recorded answers and offer each as the pre-filled answer to
  its question, so a re-run confirms rather than re-interrogates (FR-021).

**Checkpoint**: every path out of the round is written down, and the cheapest one reproduces 1.16.0.

---

## Phase 3 — User Story 3: an answer cannot launder itself into evidence (P2)

- [X] T019 Amend R1 in `## The rules that never bend` to admit a third provenance, `stated`, alongside a cited project
  path and `convention` (FR-009, D5).
- [X] T020 Add R7 — an answer is an input, not a measurement: answers shape judgment and never move a measured or
  reported figure; R3 stays absolute; a contradicting answer is applied where legitimate and the disagreement recorded
  (FR-010, FR-011, D6).
- [X] T021 Add a row to `## What this command never does`: let an answer override a measured or reported figure.
- [X] T022 Extend the write step (Step 9 → 10) so front matter carries the clarification answers, surviving a template
  override that reshapes the sources section (FR-013, D9).
- [X] T023 Scope the report step's (Step 10 → 11) "Before you ask the user anything" to the amendment, settling the
  FR-028 tension recorded in the spec. The pinned substring must survive the edit.
- [X] T024 Add to `## Known limitations`: a `stated` recommendation is a claim by the team, not evidence from the
  repository.
- [X] T025 Update the command's front-matter `description` to name the round, retaining the phrase
  `never writes the constitution`, which is pinned by `tests/test_test_strategy_flow.py:110`.
- [X] T026 Extend the `Sources consulted` annotation in the command's inline skeleton to name the answer record. Safe:
  `sections()` at `tests/test_document_templates.py:93` strips trailing annotations before comparing.
- [X] T027 Confirm no named browser driver entered the command's text at any point in Phases 1–3 (FR-024).

**Checkpoint**: three provenances, one of which can never move a number.

---

## Phase 4 — The template (FR-012, FR-013)

- [X] T028 Add the **Inputs from the user** table to `## Sources consulted and coverage of analysis` in
  `spectra/templates/test-strategy-template.md`: number, question, recommended, answer, and a disposition of answered,
  default taken, or not asked (D9).
- [X] T029 Add `stated: Q<n>` to the evidence-column guidance in `## Recommendations summary`.
- [X] T030 Extend the "what this template cannot change" comment block with the new invariant, avoiding the literals
  `at or below the baseline` and `appears at no tier`, which `tests/test_test_strategy_flow.py:375` asserts are absent.
- [X] T031 Confirm the ten `##` headings are unchanged and still match the command's inline skeleton.

---

## Phase 5 — Tests (FR-025)

- [X] T032 Shift the step literals in `test_the_report_step_precedes_the_constitution_step` to
  `## Step 11 — Report`, `## Step 12 — Check the constitution`, `## Step 13 — The amendment gate`. The invariant it
  protects is ordering, which the renumber preserves.
- [X] T033 Add `TheClarificationRoundAsksOnlyWhatItCannotMeasure` to `tests/test_test_strategy_flow.py`: the governing
  line, the never-ask list naming the mode and the coverage figure, the fixed count, the one-at-a-time rule, the
  recommended option with its evidence, and free text as a valid answer.
- [X] T034 Add assertions for the ways out: proceed-with-defaults, the not-asked disposition, the re-ask on an off-topic
  reply, and `--non-interactive` documented in both `## User Input` and `## Non-interactive mode`.
- [X] T035 Add assertions for provenance: `stated` present alongside `convention`, R7 present, and R3's
  at-or-below-the-baseline rule surviving an answer.
- [X] T036 Add an assertion that the round precedes the write step and the write step precedes the report, so the
  ordering in FR-014 is enforced rather than assumed.
- [X] T037 Mutation-check the new class: remove the never-ask list and confirm the suite fails by name, then revert.

---

## Phase 6 — Release (Principle V, one change)

- [X] T038 Bump `extension.version` to `1.17.0` in `spectra/extension.yml`, preserving the two-space indent CI's `sed`
  depends on (FR-026).
- [X] T039 Update the `speckit.spectra.test-strategy` description in `spectra/extension.yml` to name the round, as one
  unwrapped line, retaining `never writes the constitution` (FR-026).
- [X] T040 Mirror `version` and both `updated_at` fields in `catalog.json`. `provides.commands` stays `11` (FR-026).
- [X] T041 Add the `[1.17.0]` entry to `spectra/CHANGELOG.md` under `### Changed`: what the agent could not know, what
  it now asks, why declining is free, and why an answer can never move a measured figure (FR-026).
- [X] T042 Rebuild `docs/packages/spectra.zip` with `python3 tools/build_package.py` (FR-026).

---

## Phase 7 — Documentation

- [X] T043 `spectra/README.md` — the test-strategy prose block gains a line on the round and the flag.
- [X] T044 `AGENTS_LIST.md` — the test-strategy prose block gains the same, in its own idiom.
- [X] T045 `docs/index.html` — the `cdesc` blurb gains the round; the `args` span gains `--non-interactive`. Its
  "Ten sections" claim stays accurate because Phase 4 adds no section.

---

## Phase 8 — Verification

- [X] T046 `python3 -m unittest discover -s tests` — full suite green.
- [X] T047 `python3 tools/generate_agent_docs.py --check` — no drift.
- [X] T048 `python3 tools/build_package.py` — deterministic rebuild, zip contents match `spectra/`.
- [X] T049 Grep the command for `Step [0-9]` and check each of the ten cross-references against its target, confirming
  the two retargets from T013 (D10).
- [X] T050 Confirm the never-ask list contradicts nothing in Steps 1–3, which measure those same facts (SC-003).
- [X] T051 Confirm `stated` is spelled identically in R1, the recommendations guidance, and the answer record (SC-003).
- [X] T052 Install into a scratch project per `CONTRIBUTING.md:269` and run the command end to end: five questions one at
  a time, "use your defaults" short-circuiting to a complete document, and the answer record matching what was asked.
  Then re-run with `--non-interactive` and confirm nothing is asked (SC-001, SC-002, SC-005).
- [X] T053 Set the spec's **Status** to Implemented.
- [X] T054 Add the round to the `test-strategy` manual pass in `test/README.md`. The three behaviours a
  prompt-text test cannot settle — that it really asks one at a time, that declining really is free, and
  that an answer really cannot move a number — belong in the checklist a human works through, alongside
  the floor and browser-driver checks already there. Outside `spectra/`, so no rebuild.

---

## Dependencies

- T001–T005 precede everything: the premise is verified and every pinned literal is known before an edit lands.
- T006 → T007 → T008 → T009 → T010 → T011 → T012 (one section, in order). T013 follows the section existing.
- T014–T018 depend on T006–T013; T017 depends on T013's renumber.
- T019–T027 are independent of Phase 2 but depend on T006 for the round to refer to.
- T028–T031 depend on T019 for the `stated` vocabulary.
- T032 depends on T013. T033–T036 depend on Phases 1–4 being final; T037 depends on T033.
- T038–T042 depend on every prose edit being final; T042 depends on T038 and T039.
- T043–T045 depend on Phases 1–4.
- T046–T053 last. T052 depends on T042.
