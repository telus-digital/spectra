---

description: "Task list for UAT and Regression lenses, a tighter test handoff, and a UAT runner"
---

# Tasks: UAT and Regression Lenses, a Tighter Test Handoff, and a UAT Runner

**Input**: Design documents from `/specs/032-uat-and-test-handoff/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Requested. The repository's standard-library `unittest` suite asserts that each rule is still
present in the shipped prompt text, following the pattern of `tests/test_test_plan_flow.py`. Write each
story's tests first and confirm they fail before editing the command file.

**Organization**: Tasks are grouped by user story. Stories US1, US2, US5 and US6 all edit
`spectra/commands/test-plan.md`, so their command-file tasks run in sequence. Test files and other files
are marked [P] where they are independent of one another.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: US1–US6, from spec.md
- **[UAT]**: a user-acceptance task. It is not executed by `/speckit-implement`. This spec uses the
  convention it introduces.

---

## Phase 1: Setup (Governance prerequisite)

**Purpose**: Principle VII has to admit per-feature deliverables beside the spec before a second command
writes one (research R4).

- [X] T001 Amend Principle VII in `.specify/memory/constitution.md`:
  - Extend the "Spec Kit's own locations are outside this rule" paragraph so it explicitly admits
    **per-feature deliverables written beside the specification they concern**, naming
    `specs/<feature>/test-plan.md` (`speckit.spectra.test-plan`) and `specs/<feature>/uat-report.md`
    with its `uat/` evidence (`speckit.spectra.uat`). State that such a command still writes nowhere
    else and still checks that the spec lies inside the project.
  - Bump the version 1.10.0 → 1.11.0 and set Last Amended to 2026-10-15.
  - Replace the SYNC IMPACT REPORT with one for 1.10.0 → 1.11.0: MINOR, materially expanded guidance in
    VII. List the dependent files as `CONTRIBUTING.md`, `tests/test_doc_output_paths.py`,
    `spectra/commands/test-plan.md` and `spectra/commands/uat.md`.
- [X] T002 [P] In `tests/test_doc_output_paths.py`, generalize `TheOutputIsNotAnArtifactRootDocument`:
  - Parametrize it over `("test-plan.md", "test-plan.md")` and `("uat.md", "uat-report.md")`.
  - Assert that each command is absent from `CANONICAL` and `SINGLETON`.
  - Assert that each names its beside-the-spec output.
  - Assert that the constitution's VII paragraph names both files.
  - Update the class docstring to cite this spec as well as spec 021.

---

## Phase 2: Foundational (Blocking prerequisites)

**Purpose**: The new command file, its template and their registration exist, so the suite can find
them and every story has a file to extend.

- [X] T003 Create `spectra/commands/uat.md`:
  - YAML front matter with a `description`. Base it on the description line in
    `contracts/uat-command.md`: run UAT for one feature on explicit request, perform the scenarios the
    agent can drive, save evidence, tick only observed passes, and write `uat-report.md`.
  - A title and role paragraph.
  - "The one rule that governs everything".
  - A `## User Input` section with `$ARGUMENTS`, stating that the feature is required and is never
    inferred.
  - A "What this command never does" table taken from the contract's **Never** list.
  - The inline template skeleton at the end, with the seven sections from `contracts/uat-command.md`.
- [X] T004 [P] Create `spectra/templates/uat-report-template.md`:
  - A HOW-TO-USE comment that names what the template cannot change: the never-tick-unobserved rule,
    evidence linking, secret withholding, and the coverage statement.
  - The identifying block table.
  - Sections, in order: Scenarios (`| ID | Verifies | Executor | Outcome | Evidence | Reason |`), Totals,
    Tools and run, Withheld, Run log, and Sources consulted and coverage.
  - No checkboxes.
- [X] T005 Register both in `spectra/extension.yml`:
  - Add `speckit.spectra.uat` under `provides.commands` (`file: "commands/uat.md"`, with a description
    matching the T003 front matter).
  - Add `uat-report-template` under `provides.templates`, with a description naming the override path
    and the rules that stay with the command.
- [X] T006 [P] Add `"uat.md": "uat-report-template"` to `DOCUMENT_COMMANDS` in
  `tests/test_document_templates.py`.
- [X] T007 [P] Add the roster entry to `agents-list.json`:
  - `{"id": "uat", "title": "UAT Runner", "status": "available", "phase": "testing-quality",
    "type": "add-on", "provider": "spectra", "command": "speckit.spectra.uat"}`.
  - The description should say: *Run the user-acceptance scenarios from your test plan on explicit
    request — perform what the agent can drive, save the evidence, and tick only what it saw pass.*
  - Place it after `converge` in the testing-quality block.

**Checkpoint**: `python3 -m unittest tests.test_document_templates tests.test_doc_output_paths` passes,
apart from rule-content assertions that later phases fill in.

---

## Phase 3: User Story 1 — A test plan that carries UAT scenarios and a regression scope (Priority: P1) 🎯 MVP

**Goal**: test-plan derives a lens *set* from the strategy and writes the Suggested UAT Scenarios and
Regression Scope sections.

**Independent Test**: Run test-plan in a project whose strategy marks UAT and regression applicable.
Every `UATn` cites a spec id and names an executor. Every regression row cites a test file, or the search
performed. The document contains no checkbox.

### Tests for User Story 1

- [X] T008 [P] [US1] Add a class `TheLensSetComesFromTheStrategy` to `tests/test_test_plan_flow.py`
  covering `contracts/test-plan-additions.md` § Vocabulary and lens set. It asserts the pinned phrases:
  - "this strategy predates the UAT and Regression lenses";
  - "no test strategy exists";
  - "distinct from a UAT scenario";
  - the `lenses:` front-matter key;
  - the fifth not-covered reason, "ruled out by the strategy", with "re-run test-strategy".

  Rename `test_it_names_the_four_uncovered_reasons` (line 210) to
  `test_it_names_the_five_uncovered_reasons`, and assert all five reasons.

  Extend `test_the_default_vocabulary_is_stated` to require `` `uat` `` and `` `regression` ``.
- [X] T009 [P] [US1] Add a class `UatScenariosAndRegressionScope` to `tests/test_test_plan_flow.py`. It
  asserts that the command names the section "Suggested UAT scenarios", the `UAT1` id form, the
  executors `agent`, `human` and `either`, and the phrases "agent only where the surface can actually be
  driven", "every user story" (FR-026), "not from this session's tools" (FR-021) and "Regression
  scope", plus the `existing` and `risk-driven addition` kinds. It also asserts
  that the shipped template declares `## 4. Suggested UAT Scenarios` and `## 5. Regression Scope`.

### Implementation for User Story 1

- [X] T010 [US1] In `spectra/commands/test-plan.md` Step 3, replace "Resolve the level vocabulary" with
  lens-set resolution per `contracts/test-plan-additions.md`:
  - Read the strategy's `lenses:` front matter first, falling back to headings.
  - Use the three-state table: has `lenses:`; pre-032; no strategy.
  - Treat UAT and Regression as section-bearing lenses, not condition levels (data-model § Level
    vocabulary).
  - Keep `manual` always available, "distinct from a UAT scenario".
  - Keep "verbatim" and "not normalized".
  - With no strategy, add `uat` and `regression` to the default set.
- [X] T011 [US1] In `spectra/commands/test-plan.md` Step 7:
  - Extend R1 so that an acceptance criterion is reached by a condition, a UAT scenario, or an
    explicitly-not-covered entry.
  - Add the fifth not-covered reason, `ruled out by the strategy`, with the remedy "re-run
    test-strategy" (FR-011).
  - Forbid assigning a ruled-out lens (FR-010).
  - Update the "The rules that never bend" R1 wording to match.
- [X] T012 [US1] Add a new step "Derive the UAT scenarios" to `spectra/commands/test-plan.md`, after the
  conditions step. Cover:
  - `UATn` ids;
  - a journey plus an expected outcome — not a script;
  - the "verifies" forms;
  - inherited priority;
  - the executor rule, with "agent only where the surface can actually be driven" and the strategy's
    executor policy (FR-020–023);
  - per-surface evidence from the strategy's rule;
  - **every user story** has at least one scenario, or is listed under Explicitly not covered with a
    reason (FR-026);
  - the executor is judged from the manifests' surface kind and the strategy's policy, "not from this
    session's tools" (FR-021).

  The section is omitted, and the omission stated, when UAT is unavailable.
- [X] T013 [US1] Add a new step "Derive the regression scope" to `spectra/commands/test-plan.md`. Reuse
  Step 6's search results: existing tests touching the feature's modules, cited by file; labelled
  risk-driven additions; and a mandatory search line when nothing is found (FR-024). The section is
  omitted, and the omission stated, when Regression is unavailable.
- [X] T014 [US1] Renumber the following steps in `spectra/commands/test-plan.md` and fix every
  cross-reference ("Step N").
  - Extend the "What the document never contains" table with a UAT scenario written as a click script.
  - Extend the report (Step 14) with UAT and regression counts and the lens-set source.
  - Update the inline skeleton: sections 4 Suggested UAT Scenarios, 5 Regression Scope, 6 Environment &
    Data, 7 Exit Criteria.
- [X] T015 [P] [US1] Update `spectra/templates/test-plan-template.md`:
  - Insert `## 4. Suggested UAT Scenarios`, with a guidance comment and the table
    `| ID | Journey | Expected outcome | Verifies | Priority | Executor | Evidence |`.
  - Insert `## 5. Regression Scope`, with a guidance comment and the table `| Test | Touches | Kind |`.
  - Renumber Environment & Data and Exit Criteria to 6 and 7.
  - Add "ruled out by the strategy" to the not-covered reasons.
  - Add a plain-statement example exit criterion, "all P1 UAT scenarios passed".
  - No checkbox.

**Checkpoint**: `python3 -m unittest tests.test_test_plan_flow tests.test_document_templates` is green
(the skeleton and the template agree).

---

## Phase 4: User Story 2 — The test plan's obligations become tasks, and implement leaves UAT open (Priority: P1)

**Goal**: test-plan's handoff makes `plan.md`, and therefore `tasks.md`, carry the test obligations and a
labelled UAT phase.

**Independent Test**: The printed prompt links the written file and states the four obligations. It
drops clause 3 or clause 4 when the matching section is absent.

### Tests for User Story 2

- [X] T016 [P] [US2] Extend `PrintedNeverInvoked` (or the class that holds
  `test_it_emits_a_copyable_planning_invocation`) in `tests/test_test_plan_flow.py`. Assert:
  - "Testing obligations";
  - "not executed by the implement command" — and that no `/speckit-` slash form appears in that phrase (Principle III);
  - the task format `[UAT] UAT<n>`;
  - "writes the test before the implementation it covers";
  - that a conditional-clause rule exists ("never mentions a section the plan does not have").

  Keep "something the **user** runs", "not an invocation" and "when you emit nothing".

### Implementation for User Story 2

- [X] T017 [US2] Rewrite the planning-handoff step (formerly Step 15) in `spectra/commands/test-plan.md`
  to emit the exact prompt in `contracts/workflow-wiring.md` § The planning prompt:
  - a link to the written path;
  - the "Testing obligations" section with clauses 1–4;
  - the omission rule for clauses 3 and 4;
  - the UAT phase title and task-line format from research R5.

  State why the obligations go into `plan.md`: the core tasks command reads `plan.md`, not
  `test-plan.md`.
- [X] T018 [US2] Add a "Known limitations" bullet to `spectra/commands/test-plan.md`: the binding guard
  that keeps implement from ticking UAT tasks is the project constitution's UAT clause (drafted by
  test-strategy). Without it, the phase label is a convention the implement command is asked, not
  forced, to follow.

**Checkpoint**: `python3 -m unittest tests.test_test_plan_flow` is green.

---

## Phase 5: User Story 3 — The test strategy decides UAT and regression policy (Priority: P2)

**Goal**: Six mandatory lenses, front-matter applicability and ownership, a widened Q3 and Q5, and the
UAT amendment clause.

**Independent Test**: Run test-strategy on a browser project with CI. The document has UAT and Regression
sections, front-matter `lenses:` and `ownership:`, and an amendment carrying the UAT clause.

### Tests for User Story 3

- [X] T019 [P] [US3] In `tests/test_test_strategy_flow.py`, rename `TheFourLensesAreMandatory` to
  `TheSixLensesAreMandatory`. Assert:
  - `UAT` and `Regression` are named;
  - "six mandatory lenses" is present and "four mandatory lenses" is absent;
  - "evidence for a surface this project does not have is not named";
  - the regression gate and the fixed-defect rule;
  - the front-matter keys `lenses:` and `ownership:` with the values `applicable` and `not_applicable`;
  - the Q3 wording "or a UAT scenario" and the Q5 wording "whether an AI agent may execute UAT";
  - the amendment clause "MUST NOT be executed or marked complete by the implement command".

  Keep the "Always five" assertions unchanged.

### Implementation for User Story 3

- [X] T020 [US3] In `spectra/commands/test-strategy.md`:
  - Update the description front matter and every "four lenses" mention to six.
  - Add the UAT and Regression rows to "The four lenses, defined", renaming the heading to "The six
    lenses, defined".
  - Extend Step 7 to work the two new lenses: the UAT executor policy and per-surface evidence; the
    Regression gate citation and the fixed-defect rule, with its default marked `convention` (FR-001–005).
- [X] T021 [US3] In `spectra/commands/test-strategy.md` Step 5:
  - Widen the Q3 and Q5 rows and their "What it changes" cells (research R3).
  - Make the Q3 confirmation case for a `none` end-to-end surface also cover UAT.
  - Keep the count at five.
- [X] T022 [US3] In `spectra/commands/test-strategy.md` Step 10, add `lenses:` and `ownership:` to the
  emitted front-matter example and to the enumerated values (research R9), with the reason: test-plan
  reads them, and they survive a template override. Make the lens-ownership statement in "The lenses,
  defined" point at `ownership:` (FR-007).
- [X] T023 [US3] In `spectra/commands/test-strategy.md` Step 13, add the UAT clause from
  `contracts/strategy-lenses.md` to the drafted amendment, only where UAT is applicable. Treat it as
  part of the `embedded` / `partial` check in Step 12. Keep the "never write the constitution" invariant
  unchanged (FR-006).
- [X] T024 [P] [US3] Update `spectra/templates/test-strategy-template.md` and the inline skeleton in
  `spectra/commands/test-strategy.md` together:
  - Add `## UAT` (applicability, proves, boundary, executors, evidence per surface, today, approach) and
    `## Regression testing` (applicability, gate, where it runs, defect rule, today) after
    `## End-to-end testing`.
  - Make the recommendations-summary lens column accept the two new lenses.

**Checkpoint**: `python3 -m unittest tests.test_test_strategy_flow tests.test_document_templates` is
green.

---

## Phase 6: User Story 4 — The agent performs UAT on explicit request (Priority: P2)

**Goal**: The full behaviour of `speckit.spectra.uat`, per `contracts/uat-command.md`.

**Independent Test**: With one passing, one failing, and one human-only scenario, only the passing one
is ticked, with evidence. The others stay open with reasons, and no source file changes.

### Tests for User Story 4

- [X] T025 [P] [US4] Create `tests/test_uat_flow.py`, modelled on `tests/test_test_plan_flow.py` (the
  `flat`/`phrases` helpers and the `CHECKBOX` regex reused through `helpers`). Add classes for:
  - **Registration**: the manifest and the front matter.
  - **Input**: the feature is required, never inferred, with no branch, `feature.json` or picker; an
    empty argument stops.
  - **Gates**: the incomplete-implementation ask; the run confirmation showing the exact command;
    declined → `blocked — run declined`.
  - **Drivability**: only `agent` or `either`; only a surface the session's tools can operate; the
    tools are stated.
  - **Environment**: local by default; `--env` only.
  - **Evidence**: the `uat/<YYYYMMDD-HHMMSS>/` path; added, never overwritten.
  - **Marking**: tick only an observed pass; evidence suffix; never touch a human-ticked task; never
    revert a pass.
  - **Write scope**: "never modifies source, tests, test configuration, CI, the specification, the test
    plan, or the constitution".
  - **Secrets**: masked or withheld, and recorded.
  - **Network**: no request beyond the build under test.
  - **Non-interactive**: nothing started or attempted.
  - **Report**: the outcomes `passed`, `failed`, `blocked`, `awaiting human` and `already done`; the
    template resolved by path.
  - **No invocation** of another command.
  - **No checkbox** in the shipped template or skeleton.

### Implementation for User Story 4

- [X] T026 [US4] Write the input-resolution and reading steps in `spectra/commands/uat.md`:
  - Resolve the feature: a dir or a `spec.md`; the out-of-project stop; never infer, with the reason
    copied from test-plan's rationale.
  - Read `tasks.md` (UAT phase, matched by `UAT<n>` id), `test-plan.md`, the strategy's evidence rule,
    the constitution, and the manifests, README or quickstart for the start command.
  - Handle "nothing to run".
  - Name every missing input (FR-051, FR-052).
- [X] T027 [US4] Write the gates in `spectra/commands/uat.md`:
  - the incomplete-implementation ask (FR-053);
  - the run confirmation, showing the exact command and target environment, with declined →
    `blocked — run declined` (FR-055);
  - the `--env` rule;
  - non-interactive mode — nothing started, and the would-attempt list reported — with the "never infer
    non-interactive" text carried over from test-plan.
- [X] T028 [US4] Write the execution step in `spectra/commands/uat.md`:
  - The drivability rule (research R6), judged from this session's own tools, with the tools relied on
    stated. A plan-marked `agent` scenario this session cannot drive is `awaiting human`, with that
    reason (FR-054).
  - Perform the journey as a user would and compare against the expected outcome.
  - Never edit code to make a scenario pass.
  - The outcome definitions from data-model § UAT run and outcome.
  - Blocked handling for missing credentials, sandboxes or hardware (FR-054).
- [X] T029 [US4] Write the evidence and secrets steps in `spectra/commands/uat.md`:
  - the run-stamped folder and file naming;
  - add-never-overwrite;
  - masking transcripts with test-plan's secret-shape list;
  - skipping a screenshot when it may show a secret, with the withholding recorded (FR-056, FR-058,
    research R7).
- [X] T030 [US4] Write the marking and re-run step in `spectra/commands/uat.md`:
  - edit only `[UAT]` lines;
  - tick and append ` — evidence: <path>` only on `passed`;
  - leave human-ticked tasks alone;
  - retry only open tasks on a re-run;
  - never revert a pass (FR-057, FR-059, FR-061).
- [X] T031 [US4] Write the template-resolution, report and session-report steps in
  `spectra/commands/uat.md`:
  - resolution through the four layers, then the inline skeleton;
  - honour, don't repair;
  - strip guidance;
  - report the path;
  - the `uat-report.md` rewritten per run, with a cumulative run log;
  - the session report order and the closing next step, from `contracts/uat-command.md` (FR-060).

  Add "Known limitations" bullets: an observation is not proof of correctness beyond the scenario; a
  drivable surface depends on the session's tools; there is no registry or network check.

**Checkpoint**: `python3 -m unittest tests.test_uat_flow tests.test_document_templates
tests.test_doc_output_paths` is green.

---

## Phase 7: User Story 5 — test-plan is offered right after specify (Priority: P2)

**Goal**: An optional `after_specify` hook for test-plan, and an optional `after_implement` hook for uat
ordered before create-pr.

**Independent Test**: The manifest carries both hooks as optional, in the right order. test-plan still
refuses an empty input.

### Tests for User Story 5

- [X] T032 [P] [US5] In `tests/test_test_plan_flow.py`, replace `test_it_registers_no_hook` and
  `test_no_hook_is_registered_in_the_manifest` (spec 021 FR-005, reversed by FR-040). The new tests
  assert:
  - the manifest's `after_specify` names `speckit.spectra.test-plan` with `optional: true`, and its
    prompt contains "SPEC_FILE";
  - the command contains "offered by an optional hook after specify", "the hook only asks", and
    "reached through the hook or not".

  Update the module docstring's "never a hook" bullet to cite spec 032.
- [X] T033 [P] [US5] Add a hooks class to `tests/test_uat_flow.py`. It asserts that `after_implement`
  lists `speckit.spectra.uat` before `speckit.spectra.create-pr`, that uat's priority is lower than
  create-pr's, and that both are `optional: true`. Confirm that `tests/test_create_pr_flow.py` still
  passes with the list form, and adjust its parsing if it reads the hooks block.

### Implementation for User Story 5

- [X] T034 [US5] Rewrite `hooks:` in `spectra/extension.yml` exactly as in `contracts/workflow-wiring.md`:
  `after_specify` for test-plan, and `after_implement` as a list of uat (priority 5) then create-pr
  (priority 10).
- [X] T035 [US5] In `spectra/commands/test-plan.md`:
  - Rewrite the "What the handoff is not" bullets and the "Edit a core command file, or register a hook"
    row of the never-table. The row becomes "Edit a core command file": registration now happens in the
    manifest, not by the command.
  - Add the pinned phrases "offered by an optional hook after specify" and "the hook only asks".
  - Add to Step 1 that an input reached through the hook or not is resolved identically, and that an
    empty one stops (FR-041, FR-042).
  - Update the opening paragraph ("You run after `speckit.specify`…") to mention the offer.

**Checkpoint**: `python3 -m unittest tests.test_test_plan_flow tests.test_uat_flow
tests.test_create_pr_flow tests.test_extension` is green.

---

## Phase 8: User Story 6 — The test plan honours the whole strategy (Priority: P3)

**Goal**: FR-030 to FR-037.

**Independent Test**: The scenario in spec US6: a ruled-out container tool is not named; a known-risk
area is rated at least Medium; Q3 journeys are favoured; the touched surface's floor is used; provenance
is shown; staleness is flagged.

### Tests for User Story 6

- [X] T036 [P] [US6] Add a class `ItHonoursTheWholeStrategy` to `tests/test_test_plan_flow.py`. It
  asserts each pinned phrase in `contracts/test-plan-additions.md` § Honouring the strategy. It also
  checks that Step 1's outcome count matches its table: parse the word before "outcomes" and count the
  table rows (FR-037).

### Implementation for User Story 6

- [X] T037 [US6] In `spectra/commands/test-plan.md`:
  - Choosing the level: "honour the strategy's ownership map", with a stated departure (FR-030).
  - Step 5: forbid "a tool the strategy ruled out" through a stated constraint or the tool tiers
    (FR-031).
  - Step 5: inherit "the floor of each surface the feature touches", naming the surface (FR-034).
- [X] T038 [US6] In `spectra/commands/test-plan.md`:
  - Risks step: known risk areas raise likelihood to "at least Medium", citing the strategy (FR-032).
  - Conditions and UAT steps: favour the "journeys the strategy names", and say when one is not
    (FR-033).
  - Any inherited item "carries the strategy's provenance" (FR-035).
- [X] T039 [US6] In `spectra/commands/test-plan.md`:
  - Add the "possibly stale" check (research R8), with its line in the degradation table (FR-036).
    State that the history lookup is a read, not a run, and that where history is unavailable it falls
    back to the mode check alone and says so.
  - Fix Step 1: "Four outcomes" → "Six outcomes" (FR-037).

**Checkpoint**: `python3 -m unittest tests.test_test_plan_flow` is green.

---

## Phase 9: Polish & publishing (Principle V)

- [X] T040 Bump `spectra/extension.yml` `extension.version` 1.20.0 → 1.21.0. Update the `test-plan` and
  `test-strategy` command descriptions and the `test-plan-template` and `test-strategy-template`
  descriptions to mention UAT and regression. Add the tags `uat`, `regression` and
  `acceptance-testing`.
- [X] T041 Add a `## 1.21.0` entry to `spectra/CHANGELOG.md`:
  - **Added**: `speckit.spectra.uat`, `uat-report-template`, and the two hooks.
  - **Changed**: the six-lens test-strategy, test-plan's lens-set consistency, new sections, handoff and
    strategy-honouring rules.
  - **Fixed**: the "Four outcomes" miscount.
  - A note that existing strategies should be re-run.
- [X] T042 Update the `spectra` entry in `catalog.json`: version 1.21.0, command count 13, description
  if it lists commands, and the tags to match the manifest.
- [X] T043 [P] Write the hand-authored `<!-- SPECTRA:AGENT id=uat -->` prose blocks in `README.md`,
  `AGENTS_LIST.md` and `spectra/README.md`, in the style of the test-plan block. Revise the test-plan and
  test-strategy prose blocks for the new lenses, sections and hook, and the SDD flow
  `/specify → /test-plan → /plan → /tasks → /implement → uat`.
- [X] T044 Run `python3 tools/generate_agent_docs.py` to regenerate the structured listings, then
  `python3 tools/generate_agent_docs.py --check`.
- [X] T045 [P] Update `docs/index.html`:
  - Add a `speckit.spectra.uat` command entry (description, arguments, a Claude example
    `/speckit-spectra-uat specs/001-signup`).
  - Revise the test-plan and test-strategy entries.
  - Do not hard-code versions or the roster (Principle V).
- [X] T046 [P] Update `docs/e-learning/customization.html`: add a `uat-report-template` row to the
  template table. Update `docs/e-learning/module-6.html` and `docs/e-learning/AI-DLC.html` wherever they
  describe the test-plan flow, the "not a hook" behaviour, or the four lenses.
- [X] T047 [P] Update `CONTRIBUTING.md` wherever it restates Principle VII's carve-out, to name
  per-feature deliverables beside the spec (`test-plan.md`, `uat-report.md`).
- [X] T048 Run `python3 tools/build_package.py` to rebuild `docs/packages/spectra.zip`.
- [X] T049 Run the full suite with `python3 -m unittest discover -s tests`, then
  `python3 tools/ship.py --dry-run`, and fix anything they report. Then confirm the negative constraints:
  `git diff --stat main -- spectra_cli VERSION .specify/templates .claude/skills` must print nothing. That
  covers FR-044 (no core command or template edited) and FR-071 (CLI channel untouched).

---

## Phase 10: User Acceptance (UAT) — not executed by /speckit-implement

**Purpose**: The manual pass from [quickstart.md](quickstart.md), done in a throwaway project with the
working copy installed via `specify extension add --dev`. These scenarios use the convention this spec
introduces: `/speckit-implement` leaves them open, and a human ticks them (or runs the new uat command
against the throwaway project's own feature).

- [X] T050 [UAT] UAT1 (US3) test-strategy on a browser project writes six lenses, `lenses:` and `ownership:` front matter, screenshot evidence, and the UAT amendment clause — executor: human
- [X] T051 [UAT] UAT2 (US5) After `/speckit-specify`, the test-plan hook is offered with the SPEC_FILE instruction, and accepting it plans that spec — executor: human
- [X] T052 [UAT] UAT3 (US1) The generated test-plan.md has Suggested UAT Scenarios with executors, a cited Regression Scope, no checkbox, and the printed planning prompt — executor: human
- [X] T053 [UAT] UAT4 (US2) Pasting the prompt, then `/speckit-tasks`, yields Testing obligations in plan.md and a final UAT phase in tasks.md — executor: human
- [X] T054 [UAT] UAT5 (US2) `/speckit-implement` leaves every [UAT] task open and offers uat before create-pr — executor: human
- [X] T055 [UAT] UAT6 (US4) `/speckit-spectra-uat` asks before running, ticks only the passing scenario with evidence, and leaves the failed and human ones open, with no source change — executor: human
- [X] T056 [UAT] UAT7 (US4) A re-run retries only open tasks, adds a new evidence folder, and appends to the run log — executor: human
- [X] T057 [UAT] UAT8 (US1, US6) UAT `not_applicable`, a pre-032 strategy, and no strategy each produce the stated behaviour (quickstart scenarios 8–10) — executor: human

---

## Dependencies & Execution Order

- **Phase 1** (T001–T002): no dependencies. T001 gates T002's constitution assertion.
- **Phase 2** (T003–T007): after Phase 1. T005 depends on T003 and T004.
- **US1** (Phase 3): after Phase 2. It is the MVP: plan sections exist even before the handoff changes.
- **US2** (Phase 4): after US1, since the prompt's clauses 3 and 4 refer to US1's sections.
- **US3** (Phase 5): after Phase 2. It is independent of US1 and US2 on disk (a different command file),
  so it can run in parallel with them. US1 reads the `lenses:` key that US3 defines; the contract fixes
  the key's shape, so the two can be built side by side.
- **US4** (Phase 6): after Phase 2. Its own file, so it can run in parallel with US1 to US3.
- **US5** (Phase 7): T034 after T005 (the manifest). T035 after US2, since both touch test-plan's handoff
  text.
- **US6** (Phase 8): after US1 (step numbering) and US5 (the same file).
- **Polish** (Phase 9): after every story. T044 after T043; T048 after every `spectra/` edit; T049 last.
- **UAT** (Phase 10): after Phase 9. Not executed by `/speckit-implement`.

## Parallel Examples

```text
# After Phase 2, three files are independent:
US1 tests T008, T009          (tests/test_test_plan_flow.py — same file, sequential with each other)
US3 tasks T019–T024           (spectra/commands/test-strategy.md + its template + its test)
US4 tasks T025–T031           (spectra/commands/uat.md + tests/test_uat_flow.py)

# Polish in parallel:
T043 prose · T045 index.html · T046 e-learning · T047 CONTRIBUTING.md
```

## Implementation Strategy

1. **MVP** = Phases 1 to 3. The test plan carries UAT scenarios and a regression scope that is
   consistent with the strategy.
2. **Then US2**, so the obligations flow into `plan.md` and `tasks.md`. This completes the user's core
   loop with a human doing UAT.
3. **Then US3 and US4 in parallel**: the strategy policy and the agent-run UAT.
4. **Then US5**, the hooks that make the flow automatic to discover.
5. **Then US6**, the tightening fixes.
6. **Polish and publish together**, because Principle V forbids a partial release. Land via
   `python3 tools/ship.py` and never push to `main` directly.
