---

description: "Task list for feature 041 — consistent next-step suggestions across the SDLC"
---

# Tasks: Consistent Next-Step Suggestions Across the SDLC

**Input**: Design documents from `/specs/041-next-step-suggestions/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/hooks.md, contracts/closing-suggestion.md, quickstart.md

**Tests**: Included. The spec's acceptance requires the test suite to pass and an acceptance test for UAT
after converge (FR-008), and plan.md / research R6 call for `tests/test_next_step_suggestions.py`. Command
files are prompts, so tests assert their text (the `*_flow.py` convention). Write each story's tests first
and confirm they fail before that story's implementation.

**Organization**: Tasks are grouped by user story. US1–US3 all edit `spectra/extension.yml` and the new test
module, so they run in sequence. US4–US6 edit different command files and can run in parallel once Phase 2
is done.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: The user story the task belongs to (US1–US6)

## Path Conventions

Repository root: `spectra/` (extension), `agents/` (agent source), `tests/` (unittest), `docs/` (pages, package), `tools/` (generator, packager, ship).

---

## Phase 1: Setup

**Purpose**: The new test module and its helpers, used by every story.

- [X] T001 Create `tests/test_next_step_suggestions.py`. Give it a module docstring in the style of `tests/test_uat_flow.py`: the command text is the enforceable surface, and the manual pass is in `specs/041-next-step-suggestions/quickstart.md`. Add these standard-library helpers:
  - `manifest()` reads `spectra/extension.yml`;
  - `hooks_block()` returns the text between `\nhooks:` and `\ntags:`;
  - `event_block(name)` returns the text from `name + ":"` up to the next line matching `^  after_[a-z_]+:$`, or the end of the block;
  - `entries(name)` splits an event block into per-command dicts of `command`, `optional`, `priority`, `prompt` and `condition`, using regexes and no YAML library. It must read both shapes the manifest uses: a single mapping (`after_specify`, `after_clarify`, `after_converge`) and a list of `- command:` entries (`after_implement`);
  - `command_text(id)` reads `spectra/commands/<id>.md`.

  Use `tests/helpers.py` (`repo_file`) where it already offers path helpers.

---

## Phase 2: Foundational (blocking)

**Purpose**: Fix the two existing tests that will mis-slice the manifest once new events exist (research R6), and correct the manifest's shared header. These must land before any new event is added.

- [X] T002 [P] In `tests/test_test_plan_flow.py`, `test_the_manifest_offers_it_after_specify_optionally` (around line 740): slice `after_specify` up to the next `^  after_[a-z_]+:$` line rather than to `after_implement:`. Keep every existing assertion.
- [X] T003 [P] In `tests/test_uat_flow.py`, `hooks_block()` callers that use `.partition("after_implement:")[2]` (around lines 316, 478, 482, 486, 487): bound the slice at the next `^  after_[a-z_]+:$` line, so a later `after_converge` entry can't satisfy or break an `after_implement` assertion. Add a module-level helper `after_implement_block()` and use it in those tests.
- [X] T004 Write the header tests in `tests/test_next_step_suggestions.py` (class `TheManifestHeaderIsAccurate`):
  - `requires.speckit_version` equals `">=0.11.2"`;
  - the comment lines in `hooks_block()` contain the phrase `list order` and state that priority does not set it;
  - `hooks_block()` contains no claim that Spec Kit sorts hooks by priority (no `sorts on`). The historical fact that per-event lists with priority arrived in Spec Kit 0.10.0 may stay; only the sorting claim is wrong.

  Run `python3 -m unittest tests.test_next_step_suggestions` and confirm these fail.
- [X] T005 In `spectra/extension.yml`:
  - raise `requires.speckit_version` from `">=0.11.0"` to `">=0.11.2"`, and update its comment to say 0.11.2 is the first release with `converge` and its `after_converge` event;
  - replace the `hooks:` header comment, and the comment above `after_implement`, with the header comment from `specs/041-next-step-suggestions/contracts/hooks.md` (offers only, no condition; list order sets what users see, priority agrees but doesn't set it; SPECTRA hooks only after core commands).

  Run T004's tests and T002/T003. All pass.

**Checkpoint**: The suite passes, and the manifest's comments describe ordering truthfully.

---

## Phase 3: User Story 1 — After implement, converge is offered before UAT and a PR (Priority: P1) 🎯 MVP

**Goal**: `implement` ends offering converge, then UAT, then a PR, all optional.

**Independent Test**: The US1 tests pass, and step 3 of the quickstart's manual pass shows the three offers in order.

### Tests for User Story 1

- [X] T006 [US1] In `tests/test_next_step_suggestions.py`, add class `AfterImplementOffersConvergeFirst`:
  - `entries("after_implement")` commands equal `["speckit.converge", "speckit.spectra.uat", "speckit.spectra.create-pr"]`, in that order;
  - every entry is `optional: true` with no `condition`;
  - priorities strictly increase in list order;
  - the converge prompt equals `"Check the build against the spec, plan, and tasks for work that is still unbuilt?"`;
  - the converge entry is preceded by a comment naming it a core Spec Kit command and stating that the extension reference does not document hooks on core commands (FR-010);
  - no prompt contains `specs/` or `SPEC_FILE`.

  Confirm they fail.

### Implementation for User Story 1

- [X] T007 [US1] In `spectra/extension.yml` under `after_implement`, insert the `speckit.converge` entry first, exactly as in `contracts/hooks.md`: `optional: true`, `priority: 3`, the prompt above, description `"Offer converge after implementation, before UAT and a pull request"`, and the core-command comment. Keep the uat (priority 5) and create-pr (priority 10) entries unchanged.
- [X] T008 [US1] In `tests/test_uat_flow.py`, `test_every_spectra_hook_is_optional`: raise the minimum `optional: true` count from 3 to 4. T013 and T018 raise it further. Run `python3 -m unittest tests.test_uat_flow tests.test_next_step_suggestions`; all pass.

**Checkpoint**: The `after_implement` contract is met.

---

## Phase 4: User Story 2 — After converge, UAT is offered before a PR (Priority: P1)

**Goal**: A new `after_converge` event offers UAT, with a prompt true for both converge outcomes. The UAT agent's implementation-incomplete check stays.

**Independent Test**: The US2 tests pass, and steps 4–5 of the quickstart's manual pass show the offer after both outcomes and the warning on an early UAT run.

### Tests for User Story 2

- [X] T009 [US2] In `tests/test_next_step_suggestions.py`, add class `AfterConvergeOffersUat`:
  - `entries("after_converge")` is exactly one entry, `speckit.spectra.uat`, `optional: true`, no `condition`;
  - its prompt equals `"Run UAT now? If converge just added tasks, finish them with implement first — UAT will tell you if any are still open."` (FR-007).
- [X] T010 [US2] In the same module, add class `UatStillGuardsAnEarlyRun`, asserting on `command_text("uat")` that the Step 3 gate text survives (FR-008): `**Implementation incomplete.**`, `Count the tasks outside the UAT phase that are still unchecked`, `give the count, and ask whether to go on`. Confirm the T009 tests fail. The T010 tests pass already, since they pin existing text.

### Implementation for User Story 2

- [X] T011 [US2] In `spectra/extension.yml`, add the `after_converge` event after `after_implement`, exactly as in `contracts/hooks.md`: the explanatory comment, `command: speckit.spectra.uat`, `optional: true`, the FR-007 prompt, and description `"Offer UAT after converge, so a converged feature is tested before a pull request"`.
- [X] T012 [US2] In `agents/uat.md` (body, "When to use", around line 46), reword the hook sentence to: "After implement, an optional hook offers it ahead of `create-pr`, and another offers it after converge; the hooks only ask." Check `tests/test_uat_flow.py` for any assertion on the old sentence and update it in the same task.
- [X] T013 [US2] In `tests/test_uat_flow.py`, `test_every_spectra_hook_is_optional`, raise the minimum count from 4 to 5 (after_specify, three under after_implement, after_converge). Run the UAT and next-step modules; all pass.
- [X] T014 [P] [US2] In `docs/getting-started/spectra.html` (hand-written, no generated region):
  - in the "For every feature" list, extend the `/speckit-converge` line (around line 280) with "A hook then offers UAT.";
  - in scenario 07's flow, change "After implement, accept the hook's offer" so it says implement first offers converge, then UAT, and that UAT is offered again after converge;
  - in the "For every feature" list, extend the `/speckit-specify` line ("A hook then offers the test plan.") to say the test plan is offered again after `/speckit-clarify`.

  Keep the page's existing markup classes.

**Checkpoint**: The `after_converge` contract is met, the UAT gate is pinned, and the walkthrough matches.

---

## Phase 5: User Story 3 — After clarify, the test plan is offered (Priority: P2)

**Goal**: `clarify` ends offering the test plan for the clarified feature, with no path needed.

**Independent Test**: The US3 tests pass, and step 2 of the quickstart's manual pass shows the offer.

### Tests for User Story 3

- [X] T015 [US3] In `tests/test_next_step_suggestions.py`, add class `AfterClarifyOffersTheTestPlan`:
  - `entries("after_clarify")` is exactly one entry, `speckit.spectra.test-plan`, `optional: true`, no `condition`;
  - its prompt equals `"Build or refresh the test plan from the clarified spec? It uses the feature this clarify run worked on, so no path is needed."`;
  - the prompt contains no `specs/` or `SPEC_FILE`.

  Confirm they fail.

### Implementation for User Story 3

- [X] T016 [US3] In `spectra/extension.yml`, add the `after_clarify` event directly after `after_specify`, exactly as in `contracts/hooks.md`, with description `"Offer a test plan built from the clarified specification"`. Leave `after_specify` byte-identical.
- [X] T017 [US3] In `agents/test-plan.md`:
  - in the `manifest:` header line, change "is offered by an optional hook after specify" to "is offered by an optional hook after specify or clarify";
  - in the body ("When to use", around line 81), change "After `specify`, an optional hook offers it — the hook only asks" to "After `specify` or `clarify`, an optional hook offers it — the hook only asks".

  Keep the rest of each sentence. Don't edit `spectra/commands/test-plan.md` or the manifest's `description:` line by hand; T031 regenerates them.
- [X] T018 [US3] In `tests/test_test_plan_flow.py`, `test_it_is_offered_by_an_optional_hook_that_only_asks` (around line 721): update the pinned phrase to `"offered by an optional hook after specify or clarify"`, and keep `"the hook only asks"`. In `tests/test_uat_flow.py`, raise the optional count from 5 to 6. Run all three hook-related modules; all pass.

**Checkpoint**: All four events and six entries exist. The hooks contract is met in full.

---

## Phase 6: User Story 4 — After a root cause analysis, specifying the fix is offered (Priority: P2)

**Goal**: `defect-rca` ends with the shared `**Next step**` block, offered only for a validated cause.

**Independent Test**: The US4 tests pass, and step 6 of the quickstart's manual pass shows the offer and the no-offer form.

### Tests for User Story 4

- [X] T019 [P] [US4] In `tests/test_next_step_suggestions.py`, add class `DefectRcaOffersAFixSpec`, asserting on `command_text("defect-rca")` (flattened whitespace) that it contains:
  - `**Next step**`, the phrase `specify command`, and the instruction to render it `in whatever invocation syntax this agent uses` (Principle III) — the test asserts no literal command spelling;
  - that the ready-to-paste prompt is the only content of its code block;
  - an instruction to cite the document path and the validated cause with its layer;
  - an instruction that a layer-2 cause is labelled the immediate technical cause;
  - the no-offer line `none: no cause was validated, so there is nothing yet to specify a fix for`;
  - a statement that exploration mode prints no Next step block;
  - a statement that the block runs nothing.

  Confirm they fail.

### Implementation for User Story 4

- [X] T020 [US4] In `spectra/commands/defect-rca.md`, Step 13 — Report, append the closing suggestion per `contracts/closing-suggestion.md`: the shared layout (offer form and `none:` form), the offer condition (a hypothesis reached `validated`), and the prompt contents:
  - defect id and source reference;
  - document path;
  - validated cause with its layer;
  - corrective actions from section 5;
  - preventive actions out of scope unless the user adds them.

  Name the command as Spec Kit's specify command and say "render it in whatever invocation syntax this agent uses"; don't write `/speckit-specify` as the only form. Also add the layer-2 labelling rule, the no-offer reason, "the block runs nothing and asks no question", and a sentence in Non-interactive mode saying the block is still printed. In Exploration mode, add one sentence: "No Next step block — exploration writes nothing." Change no other step. Run T019; it passes.

**Checkpoint**: The defect-rca contract is met.

---

## Phase 7: User Story 5 — After flaky-test detection, specifying unapplied fixes is offered (Priority: P3)

**Goal**: `flaky-test-detector` offers `/speckit-specify` only for rows a spec can act on, or for all open rows when Gate 2 is declined.

**Independent Test**: The US5 tests pass, and step 7 of the quickstart's manual pass shows each case.

### Tests for User Story 5

- [X] T021 [P] [US5] In `tests/test_next_step_suggestions.py`, add class `FlakyDetectorOffersSpecsForUnappliedFixes`, asserting on `command_text("flaky-test-detector")` that it contains:
  - `**Next step**`, the phrase `specify command`, and the instruction to render it `in whatever invocation syntax this agent uses` (Principle III) — no literal command spelling;
  - that the ready-to-paste prompt is the only content of its code block;
  - a statement that the block runs nothing and asks no question (FR-020);
  - the three offerable reasons named against the Step 8 table (production code, guardrail, not confident);
  - the Gate 2 decline offer covering every open row;
  - the no-offer lines `none: every proposed fix was applied`, `none: nothing was proposed`, and `none: the remaining rows no longer point at a test or evidence a spec could act on`;
  - a statement that rows deleted in review are never offered;
  - a statement that a Gate 1 decline prints no block;
  - the prompt contents: `FT-NNN`, test file and name, proposed fix, recorded reason, and `.specify/memory/flaky-test-analysis.md`.

  Confirm they fail.

### Implementation for User Story 5

- [X] T022 [US5] In `spectra/commands/flaky-test-detector.md`, add the closing suggestion per `contracts/closing-suggestion.md`:
  - **Step 9 — Report what you did**: after the example report and its "Every part of that is required" paragraph, add the shared layout, the offer condition (open rows whose outcome is production code, guardrail, or not confident), the prompt contents, the two `none:` cases for this step, and "rows the developer deleted are never offered";
  - **Step 7 decline path**: after "If they decline: the file stands, no source is edited, and you say so", add that the report ends with the offer for every open row;
  - **Step 10** and **Step 1b**: add the matching `none:` line;
  - **Step 5**: after "If the developer declines", add one sentence saying no Next step block follows;
  - in the shared-layout text, name Spec Kit's specify command with "render it in whatever invocation syntax this agent uses", and add "the block runs nothing and asks no question".

  Run T021; it passes.

**Checkpoint**: The flaky-test-detector contract is met.

---

## Phase 8: User Story 6 — After an impact analysis, the path to a spec is named (Priority: P3)

**Goal**: `impact` ends every run that writes an analysis with a conditional pointer to `/speckit-specify`, and never judges go / no-go.

**Independent Test**: The US6 tests pass, and step 8 of the quickstart's manual pass shows the pointer and nothing under `specs/`.

### Tests for User Story 6

- [X] T023 [P] [US6] In `tests/test_next_step_suggestions.py`, add class `ImpactNamesThePathToASpec`, asserting on `command_text("impact")` that:
  - it contains `**Next step**`, `If they approve`, the phrase `specify command`, and the instruction to render it `in whatever invocation syntax this agent uses` (Principle III) — no literal command spelling;
  - the ready-to-paste prompt is the only content of its code block;
  - it states the block runs nothing and asks no question (FR-020);
  - it states the pointer appears whatever the rating;
  - it states the pointer never states, implies, or predicts the decision;
  - it names the prompt contents: feature name, analysis path, rating and trigger, external contract changes, and the instruction to account for findings, risks and open questions;
  - `status` is still `draft` on every run;
  - the "never does" row still says nothing under `specs/` is written and the document carries no `spec_refs` (FR-017).

  Confirm the new assertions fail.

### Implementation for User Story 6

- [X] T024 [US6] In `spectra/commands/impact.md`:
  - **Step 14 — Report**: after the example's "Status is draft…" line, add the shared layout in its conditional form, worded as "the go / no-go decision is your stakeholders'; if they approve, this is the next step", plus the prompt contents, the never-states-the-decision rule, "the block runs nothing and asks no question", and the command named as Spec Kit's specify command with "render it in whatever invocation syntax this agent uses";
  - add one line to the "Nothing you say in this session may contain" list: "a prediction of the stakeholders' decision";
  - in "What this command never does", add one sentence to the "Create, reference, or link a specification" row: a pointer to the specify command in the session report is permitted, because it writes nothing and adds no reference to the document.

  Run T023 and `tests/test_impact_flow.py`; both pass.

**Checkpoint**: The impact contract is met. All six stories are done.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Whole-manifest invariants, untouched agents, and every Principle V artifact in one change.

- [X] T025 In `tests/test_next_step_suggestions.py`, add class `TheHookSetIsExactly`:
  - the event keys found in `hooks_block()` equal `{"after_specify", "after_clarify", "after_implement", "after_converge"}`;
  - `hooks_block()` has no `optional: false` and no non-null `condition:`;
  - the commands per event equal the contract table.
- [X] T026 [P] In the same module, add class `TheOtherAgentsAreUnchanged`:
  - `command_text("kb-vault")` contains no `/speckit-constitution` (FR-019);
  - none of `adr`, `brd`, `domain-analyzer`, `methodology`, `test-strategy`, `deployment-strategy`, or `kb-vault` contains `**Next step**`, which shows the shared layout was not applied to them (FR-018).
- [X] T027 In `spectra/extension.yml`, bump `extension.version` from `"1.29.1"` to `"1.30.0"`.
- [X] T028 [P] Add a `## [1.30.0] - <date of implement>` entry to the top of `spectra/CHANGELOG.md`, in the file's existing voice:
  - **Added**: the `after_clarify` → test-plan offer; the `after_implement` → converge offer ahead of UAT and a PR; the `after_converge` → UAT offer; closing next-step blocks in `defect-rca`, `impact`, and `flaky-test-detector`, with when each appears.
  - **Changed**: `requires.speckit_version` is now `>=0.11.2`, the first release with `converge`; the hooks comment now says list order, not priority, sets what users see.
  - **Note**: the converge offer relies on Spec Kit showing a hook that targets a core command, which works today but isn't documented. All hooks are offers and none runs automatically.
- [X] T029 [P] In `catalog.json`, set the `spectra` entry's `version` to `1.30.0`. Leave the description, tags, command count (14) and `download_url` unchanged, so they still match `spectra/extension.yml`.
- [X] T030 [P] Check `CONTRIBUTING.md` and `test/README.md` (track 2, the extension package) for any statement of which hooks SPECTRA registers. Update it to the four events, or note that none exists. Don't touch generated files.
- [X] T031 Run `python3 tools/generate_agent_docs.py` to regenerate `agents-list.json`, `AGENTS_LIST.md`, `spectra/README.md`, `docs/getting-started/agents.html`, and the `description:` lines in `spectra/extension.yml` and `spectra/commands/test-plan.md`. Then run `python3 tools/generate_agent_docs.py --check`; it passes.
- [X] T032 Run `python3 tools/build_package.py` to rebuild `docs/packages/spectra.zip`.
- [X] T033 Run `python3 -m unittest discover -s tests` and `python3 tools/ship.py --dry-run`. All checks and tests pass, and nothing is pushed.
- [X] T034 SC-005 diff review: `git diff main --stat -- spectra/commands/` lists only `defect-rca.md`, `impact.md`, `flaky-test-detector.md`, and `test-plan.md`, whose only change is the regenerated `description:` line. `git diff main -- spectra_cli/ VERSION` is empty (FR-023).
- [X] T035 Run the manual pass in `specs/041-next-step-suggestions/quickstart.md`, steps 1–9, in a throwaway Spec Kit 1.2.4 project with `specify extension add --dev`. Record any step that can't be performed, and why, under a `## Manual pass` note at the end of `quickstart.md`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (T001)**: no dependencies.
- **Phase 2 (T002–T005)**: depends on T001. Blocks every story, because the test fixes must precede new events.
- **US1 → US2 → US3 (Phases 3–5)**: each depends on Phase 2. They run in sequence because all three edit `spectra/extension.yml` and `tests/test_next_step_suggestions.py`.
- **US4, US5, US6 (Phases 6–8)**: each depends on Phase 2 only. Each edits a different command file; their tests share one module, so add the test classes one at a time.
- **Phase 9**: depends on every story. Order within it: T025–T026, then T027–T030, then T031, then T032, then T033, then T034, then T035.

### Within Each Story

Tests first, confirmed failing, then the implementation, then a re-run.

### Parallel Opportunities

- T002 and T003 (different test files).
- After Phase 2, the implementation tasks T020 (defect-rca.md), T022 (flaky-test-detector.md) and T024 (impact.md) can run alongside the US1–US3 chain, since none touches `extension.yml`.
- T014 (walkthrough page) alongside T012 and T013.
- T028, T029 and T030 in Phase 9.

## Parallel Example: closing suggestions

```text
Task: "T020 [US4] Add the closing suggestion to spectra/commands/defect-rca.md Step 13"
Task: "T022 [US5] Add the closing suggestion to spectra/commands/flaky-test-detector.md Steps 5, 7, 9, 10, 1b"
Task: "T024 [US6] Add the conditional pointer to spectra/commands/impact.md Step 14"
```

## Implementation Strategy

### MVP first (User Story 1)

Do Phases 1–3. That gives truthful ordering comments, the raised floor, and converge offered after implement.
Validate with the US1 tests and quickstart step 3.

### Incremental delivery

1. US2 closes the UAT-skipping gap after converge.
2. US3 adds the clarify offer, which completes the hooks contract.
3. US4–US6 add the closing suggestions in any order.
4. Phase 9 does the version, changelog, catalog, generator and package in one change, as Principle V
   requires. Nothing ships until it's done.

## Notes

- Never hand-edit a generated output. Change `agents/` and run the generator.
- Every SPECTRA hook stays `optional: true`, with no `condition`.
- The CLI channel is untouched: no `VERSION` bump and no tag.
- Land through `tools/ship.py`, never `git push origin main`.

## Phase 10: Convergence

- [X] T036 In `spectra/commands/flaky-test-detector.md`, give the Next step block a separate why line for the Gate 2 decline, "you chose not to have these fixes applied here", used when Step 7 ends with the block. Step 9's only why line, "these fixes are beyond what this agent may apply", is false after a decline. Add an assertion for the new line to `FlakyDetectorOffersSpecsForUnappliedFixes.test_declining_gate_two_offers_every_open_row` in `tests/test_next_step_suggestions.py`, per contracts/closing-suggestion.md (flaky-test-detector, Gate 2 declined) and FR-014 (partial)
