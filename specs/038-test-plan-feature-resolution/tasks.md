# Tasks: Test plan finds its feature the way the planner does

**Input**: [spec.md](./spec.md), [plan.md](./plan.md), [research.md](./research.md),
[data-model.md](./data-model.md), [contracts/resolution-behaviour.md](./contracts/resolution-behaviour.md),
[quickstart.md](./quickstart.md)

**Branch**: `038-test-plan-feature-resolution`

**Tests**: requested (FR-021, SC-005). The behaviour contract pins B1–B24 as text assertions in
standard-library `unittest`. Every test goes in `tests/test_test_plan_flow.py` (abbreviated `TP`). It uses the
`phrases()` / `command_text()` / `flat()` helpers it already defines. Within each story the test task comes
first and must fail before the command text it pins is written.

**Format**: `- [ ] [ID] [P?] [Story] Description`. `[P]` means a different file, with no dependency on an
incomplete task.

Every edit to `spectra/commands/test-plan.md` keeps the file hard-wrapped at the width it already uses (≈105
columns). The command is agent-agnostic (Principle III): name no agent's tool, and call the planner "the
planning command".

---

## Phase 1: Setup (verify the premise)

- [X] T001 Confirm that the Evidence rows in `specs/038-test-plan-feature-resolution/plan.md` still hold on this branch:
  - `.specify/scripts/bash/common.sh:38-73` (`resolve_specify_init_dir`, `get_repo_root`) and `:187-215` (feature-directory order);
  - `spectra/commands/test-plan.md:25-38` (User Input), `:84-125` (Step 1 and "Never infer"), `:223-227` (git lookups as reads), `:781` (handoff withheld), `:814` (empty-argument bullet);
  - `spectra/extension.yml:129` (hook prompt with `SPEC_FILE`);
  - `tests/test_test_plan_flow.py:109-165`, `:325-332`, `:576-599`;
  - `spectra/extension.yml` and `catalog.json` at `1.26.0`.

  Correct any line reference in later tasks that has moved.
- [X] T002 [P] Run `python3 -m unittest discover -s tests` and `python3 tools/generate_agent_docs.py --check` on the unchanged branch. Record the baseline pass count here. **Baseline (2026-10-25)**: 1654 tests OK; `--check` clean (55 agents, 14 prose blocks).

**Checkpoint**: the premises hold, and the suite is green before any change.

---

## Phase 2: Foundational (retire the old contract in the tests)

- [X] T003 In `tests/test_test_plan_flow.py`, rename class `TheSpecificationArgumentIsRequired` to `FeatureIsResolvedAsThePlannerDoes`, with docstring "Spec 038 FR-001–FR-009, FR-023 — resolve as the planning command does, never otherwise". Delete `test_it_states_the_argument_is_required`, `test_an_empty_argument_stops_without_reading_or_writing`, `test_it_resolves_a_directory_to_the_spec_inside_it`, and `test_it_does_not_choose_between_ambiguous_candidates`. Keep `test_it_refuses_to_offer_a_picker` and `test_it_stops_when_the_specification_is_outside_the_project` unchanged. Change `INFERENCE_SOURCES` to `("branch", "modification time", "listing of `specs/`")`, since `feature.json` is now a permitted source. In `test_step_one_counts_its_own_outcomes`, change the slice to run from `"## Step 1 — Resolve the feature"` to `"### Resolve only as the planning command does"`. This blocks every story phase.

**Checkpoint**: `python3 -m unittest tests.test_test_plan_flow` fails only on the renamed headings, which US1 writes.

---

## Phase 3: User Story 1 — The test plan lands in the feature the planner will plan (Priority: P1) 🎯 MVP

**Goal**: With no argument, test-plan resolves `SPECIFY_INIT_DIR` → root, then `SPECIFY_FEATURE_DIRECTORY` → `feature_directory`
in `.specify/feature.json`, reads `<dir>/spec.md`, writes `test-plan.md` there, and hands off only if the planner
would still resolve that directory (FR-001–FR-005, FR-013–FR-017; research R1, R2, R4; plan C1, C2).

**Independent Test**: quickstart M1, M2, M3, M10: test-plan and `setup-plan.sh --json` report the same `FEATURE_DIR`.

### Tests for User Story 1

- [X] T004 [US1] Add to `FeatureIsResolvedAsThePlannerDoes` in `tests/test_test_plan_flow.py`:
  - **Order (B1, B2)**: in `phrases()`, the first occurrences of `specify_init_dir`, `specify_feature_directory`, and `.specify/feature.json` inside the Step 1 section appear in that order. The section also contains `nearest directory` and `.specify/`.
  - **Empty (B3)**: the section contains "set but empty" and "unset".
  - **Spec file (B4)**: it contains "spec.md in the feature directory".
  - **Forbidden sources (B5)**: the rewritten `test_it_refuses_to_infer_the_specification` asserts "resolve only as the planning command does" and every item of `INFERENCE_SOURCES`.
  - **Read-only (B6)**: it contains "never writes `.specify/feature.json`" and "never creates the feature directory" (flattened).
  - **One read (B7)**: it contains "exactly one shell read", "once per run", both variable names, "posix", and "powershell".
  - **Never-table (C1)**: in the never-table, the "run, build, or install anything" row contains "the only command run to resolve the feature".
  - **Governing rule (U1)**: the section "## The one rule that governs everything" contains "resolved exactly as the planning command resolves it" and no longer contains "the specification you were handed" or "never guess which specification was meant".
  - **Intro (U2)**: the text before "## The one rule" no longer contains "someone hands you a specification".
- [X] T005 [US1] Add to `TheHandoffIsPrintedNeverWired` in `tests/test_test_plan_flow.py`:
  - `test_the_handoff_waits_for_the_planner_to_agree` (B17): the Step 17 section contains "the planning command would still resolve" and "re-read only `.specify/feature.json`".
  - Rewrite `test_the_hook_does_not_relax_the_never_infer_rule` to assert "reached through the hook or not, the feature is resolved identically".
  - In `test_the_manifest_offers_it_after_specify_optionally`, replace the `SPEC_FILE` assertion with `assertNotIn("SPEC_FILE", after_specify, …)` plus `assertIn("feature", after_specify)` (B20). Keep the "reported above" check.
- [X] T006 [US1] Add `test_a_feature_that_does_not_resolve_still_stops` to `NonInteractiveIsDeclaredNeverDetected` (C2): the command contains "a feature that does not resolve still stops" and no longer contains "an empty argument still stops". Run `TP`; T004–T006 fail.

### Implementation for User Story 1

- [X] T007 [US1] In `spectra/commands/test-plan.md`, rewrite "## User Input". Change "A **required** path…" to: the input is optional; with no argument the feature is resolved as Step 1 describes; an argument, if given, only confirms it (US2 fills in the detail). Delete the "If no path was supplied … stop" paragraph. Keep the `--non-interactive` paragraph and the unrecognized-flag rule unchanged.
- [X] T008 [US1] In the never-table of `spectra/commands/test-plan.md`:
  - Change the "Infer which specification was meant" row to "Choose a feature by any rule but the planning command's". Its reason: a test plan and a plan in different directories leave the approved obligations out of the tasks, and a plan built from the wrong spec reads as authoritative to whoever approves it.
  - Append to the "Run, build, or install anything" row's reason: "The one shell read in Step 1 — the values of two environment variables — is the only command run to resolve the feature; like the git lookups in Step 3 it is a read, not a run."
- [X] T008a [US1] In `spectra/commands/test-plan.md`, rewrite the quoted rule under "## The one rule that governs everything" to:
  > **Read the feature's specification — resolved exactly as the planning command resolves it — and the
  > project around it, then write exactly one file, `test-plan.md`, beside that specification. Never choose
  > the feature any other way.**

  Keep "Every rule that follows narrows that sentence. None widens it." unchanged. In the opening paragraph, change "Someone hands you a specification; you read it and the project around it, and write…" to "You resolve the feature specify recorded, read its specification and the project around it, and write…"; the rest of the paragraph is unchanged (U1, U2).
- [X] T009 [US1] Replace "## Step 1 — Resolve the specification", its six-outcome table, and the "reached through the hook" paragraph in `spectra/commands/test-plan.md` with "## Step 1 — Resolve the feature", written as research R1 and R2 describe:
  - (1) **The environment read.** One shell read, once per run, of `SPECIFY_INIT_DIR` and `SPECIFY_FEATURE_DIRECTORY`, in the POSIX and PowerShell forms from R2. A set but empty variable is unset. The values are reused for the whole run. Record the read as an input: "environment: SPECIFY_INIT_DIR, SPECIFY_FEATURE_DIRECTORY" in the inputs consulted (Step 2) and under **Sources consulted and coverage**, with which one was set — never more than the resolved directory (C1).
  - (2) **Project root.** `SPECIFY_INIT_DIR`, else the nearest directory containing `.specify/`.
  - (2a) **The invoking project** is the nearest directory containing `.specify/`, walking up from the current directory — regardless of `SPECIFY_INIT_DIR`. When `SPECIFY_INIT_DIR` names a different root, a feature directory under it lies outside the invoking project, and "### The out-of-project stop" fires (U3).
  - (3) **Feature directory.** `SPECIFY_FEATURE_DIRECTORY`, else `feature_directory` in `<root>/.specify/feature.json`, relative values joined to the root.
  - (4) **The specification.** `spec.md` in the feature directory.
  - (5) Resolution never writes `.specify/feature.json` and never creates the feature directory.
  - Then the sentence "Reached through the hook or not, the feature is resolved identically."
  - Leave a placeholder sentence "Stops: see the table below." for US4, and keep the existing "Read the resolved specification in full first…" list and everything after it.
- [X] T010 [US1] Replace "### Never infer which specification was meant" with "### Resolve only as the planning command does".
  - It MUST NOT consult the branch name, file modification times, the contents or listing of `specs/`, a cache, a prior run, or session history; it MUST NOT offer a picker.
  - Rewrite the reasoning paragraph: the test plan is consumed by the planning command, so the two must agree on the feature; the planning command reads only these sources; and the announcement (Step 1, US3) is what lets the approver see which spec was used. Keep the sentence that offering a picker is the same failure with extra steps.
  - In "### The out-of-project stop", change "the project you were invoked in" to "the invoking project (Step 1)"; keep the rest unchanged (U3).
- [X] T011 [US1] Update the cross-references in `spectra/commands/test-plan.md`:
  - Step 3's "your own output destination is fixed by Step 1 either way" stays valid; leave it.
  - In Step 15, change "the directory of the specification resolved in Step 1" to "the feature directory resolved in Step 1".
- [X] T012 [US1] In "## Step 17 — Hand the plan to the planner" of `spectra/commands/test-plan.md`, add before the example block: "**Before printing, confirm the planning command would still resolve the directory you wrote to.**"
  - If `SPECIFY_FEATURE_DIRECTORY` was set, it would.
  - Otherwise, re-read only `.specify/feature.json` (the variables are not read again).
  - If the record now names a different directory or is gone, print no handoff and say what it now names.

  Change "**When you emit nothing**: if no path was supplied, if either stop in Step 1 fired, …" to "if any stop in Step 1 fired, if an existing plan was not rewritten, or if the agreement check failed". Leave the prompt block and its clauses unchanged (FR-013).
- [X] T013 [US1] In "## Non-interactive mode" of `spectra/commands/test-plan.md`, replace the bullet "an **empty argument still stops** …" with "a feature that **does not resolve still stops**. That is a missing required input, not a gate, and nothing infers it for you;" (C2).
- [X] T014 [P] [US1] In `spectra/extension.yml`, change the `after_specify` `prompt` to: "Generate a test plan for this spec? It uses the feature this specify run just recorded, so no path is needed." Run `TP`; T004–T006 pass.

**Checkpoint**: US1 complete. Quickstart M1–M3 and M10 would pass.

---

## Phase 4: User Story 2 — A mismatched path stops the run instead of splitting the feature (Priority: P1)

**Goal**: An argument only confirms: it must be the feature directory or its `spec.md` after normalizing,
otherwise stop (FR-008, FR-009; research R3).

**Independent Test**: quickstart M4, M5.

### Tests for User Story 2

- [X] T015 [US2] Add class `AnArgumentOnlyConfirms` to `tests/test_test_plan_flow.py` (B11, B12). The Step 1 section contains:
  - "the feature directory or its `spec.md`"
  - "trailing slash"
  - "any other path" with "stop before reading the specification"
  - "the argument's path, the resolved directory, and its source"
  - "an argument is never used in place of"

  Run `TP`; it fails.

### Implementation for User Story 2

- [X] T016 [US2] In Step 1 of `spectra/commands/test-plan.md`, add "### An argument only confirms" after the resolution list. Follow research R3:
  - Resolve the argument against the project root and normalize it: drop the trailing slash and any `./` segments.
  - It matches when it is the feature directory or its `spec.md`; any other path (including another file in that directory) is a mismatch.
  - On a mismatch, stop before reading the specification, write nothing, and report the argument's path, the resolved directory, and its source, then the remedy block.
  - An argument is never used in place of resolution, including when no feature resolves.

  Run `TP`; T015 passes.

**Checkpoint**: US1 + US2 close the defect. Quickstart M4 and M5 would pass.

---

## Phase 5: User Story 3 — The approver can see which specification the plan was built against (Priority: P2)

**Goal**: The resolution is the run's first statement, and is recorded in the document and the report
(FR-010–FR-012; research R5; data-model "Announcement").

**Independent Test**: quickstart M1, M2: the first line and the identifying block name the directory and source.

### Tests for User Story 3

- [X] T017 [US3] Add class `TheResolutionIsAnnounced` to `tests/test_test_plan_flow.py` (B13–B15):
  - Step 1 contains "the first thing you say", the example line `Feature: specs/`, and "(from .specify/feature.json)".
  - Step 1 contains the disagreeing form "names" (as in `; .specify/feature.json names`).
  - The Step 13 section contains "resolved from".
  - The Step 16 section contains "the source the feature was resolved from".
  - The Step 1 section contains "record the read as an input" and "sources consulted and coverage" (C1).
  - The Step 1 section contains "the non-interactive announcement comes first"; "## Non-interactive mode" contains "before the feature line in step 1" (I1).

  Run `TP`; it fails.

### Implementation for User Story 3

- [X] T018 [US3] In Step 1 of `spectra/commands/test-plan.md`, add after resolution: "**Announce it before reading anything else** — the first thing you say", with the two example lines from data-model.md "Announcement". Add: "Under `--non-interactive`, the non-interactive announcement comes first and this line immediately after it; both precede reading the specification." In "## Non-interactive mode", change "**Announce it once, up front.**" to "**Announce it once, up front** — before the feature line in Step 1." (I1)
- [X] T019 [US3] In "## Step 13 — The identifying block", extend the **Spec** fact: the resolved specification as a project-relative path, followed by "resolved from `SPECIFY_FEATURE_DIRECTORY`" or "resolved from `.specify/feature.json`". When the two disagreed, add the record's value. The template is not changed (R5).
- [X] T020 [US3] In "## Step 16 — Report", extend the first bullet: "**The written path**, whether it was **created** or **rewritten**, and the source the feature was resolved from." Run `TP`; T017 passes.

**Checkpoint**: US3 complete.

---

## Phase 6: User Story 4 — Nothing resolves, and the run says how to fix it (Priority: P2)

**Goal**: Every resolution stop writes nothing and names the one remedy block (FR-005 failure, FR-001a,
FR-006, FR-007, FR-023; research R6; data-model "Stops").

**Independent Test**: quickstart M6, M7, M8.

### Tests for User Story 4

- [X] T021 [US4] Add to `FeatureIsResolvedAsThePlannerDoes` in `tests/test_test_plan_flow.py` (B8–B10):
  - Step 1 contains a table whose rows name the following stops (assert each phrase): "the shell read is denied or fails", "names no existing directory", "neither source", "cannot be parsed", "has no `spec.md`".
  - The text contains "never fall back to `.specify/feature.json` alone".
  - It contains the remedy block's two lines, "for this session" with `set SPECIFY_FEATURE_DIRECTORY=` and "for good" with `"feature_directory" in .specify/feature.json`, plus "to create a new feature, run the specify command".
  - The Step 1 section contains "the invoking project is the nearest directory containing `.specify/`" and "regardless of `specify_init_dir`"; "### The out-of-project stop" contains "the invoking project (step 1)" (U3).

  - The inline skeleton's "Sources consulted and coverage" comment contains "environment read" (I3).

  `test_step_one_counts_its_own_outcomes` must still pass against the new table (its prose says "<N> outcomes:"). Run `TP`; it fails.

### Implementation for User Story 4

- [X] T022 [US4] Replace the placeholder from T009 in `spectra/commands/test-plan.md` with "Seven outcomes:" and a table (`| Input | What you do |`) of exactly seven rows:
  - resolved, with no argument or a matching one → announce and continue;
  - the shell read denied or fails → stop, and never fall back to `.specify/feature.json` alone;
  - `SPECIFY_INIT_DIR` names no existing directory, or one with no `.specify/` → stop with its value and reason, and say to unset it;
  - neither source set → stop, remedy block;
  - `.specify/feature.json` cannot be parsed or has no `feature_directory` → stop, remedy block;
  - the feature directory is missing or has no `spec.md` → stop, remedy block;
  - an argument that does not match → stop (US2), remedy block.

  Each stop writes nothing and emits no handoff. Then add the remedy block verbatim from research R6 once, introduced by "The remedy block, used by every stop that concerns which feature is active:".
- [X] T023 [US4] In the inline skeleton of `spectra/commands/test-plan.md`, change the comment on "## Sources consulted and coverage" from "read; coverage n of m; could not read; nothing executed" to "read; environment read; coverage n of m; could not read; nothing executed" (I3). In the "### Degrade loudly" table, add one row: `| The environment read was denied or failed | That the variables could not be checked, so the planning command's feature could not be confirmed, and that nothing was written |`. Run `TP`; T021 passes, and so does `test_step_one_counts_its_own_outcomes`.

**Checkpoint**: all four stories complete.

---

## Phase 7: Polish & Cross-Cutting Concerns (release surfaces, Principle V)

- [X] T024 In the front matter `description` of `spectra/commands/test-plan.md`, change "Requires the spec path and never guesses which spec was meant." to "Finds the feature the way the planning command does — from SPECIFY_FEATURE_DIRECTORY or .specify/feature.json — announces which one, and stops rather than guess or split a feature."
- [X] T025 [P] In `spectra/extension.yml`:
  - Set `version` to `1.27.0`.
  - In the `speckit.spectra.test-plan` description, replace "The spec path is required and never inferred: no branch name, no feature record, no most-recent-file guess, because a plan generated against the wrong spec is undetectably wrong to whoever approves it." with "It finds the feature the way the planning command does — SPECIFY_FEATURE_DIRECTORY, then .specify/feature.json — and says which one it used; a path argument only confirms it, and a mismatch stops, so the test plan and the plan always share a directory."
- [X] T026 [P] Set the `spectra` entry's `version` in `catalog.json` to `1.27.0`.
- [X] T027 [P] Add `## [1.27.0] - <date>` to the top of `spectra/CHANGELOG.md`, with a one-line summary and a **Changed** list. List items:
  - test-plan resolves its feature as the planning command does (`SPECIFY_INIT_DIR` root; `SPECIFY_FEATURE_DIRECTORY`, then `.specify/feature.json`; empty is unset), and announces it;
  - **the path argument is optional, and a path naming a feature other than the active one now stops**, with the two ways to switch;
  - one read-only shell read of two environment variables, and a stop if it is denied;
  - the handoff is printed only when the planning command would resolve the same directory;
  - the after-specify hook no longer passes a path;
  - `speckit.spectra.uat` still requires a path, a candidate for the same change.
- [X] T028 [P] Update the hand-written `<!-- SPECTRA:AGENT id=test-plan -->` block in `AGENTS_LIST.md` (≈`:505-597`):
  - "Hand it the path to…" → it picks up the feature specify recorded.
  - "Where it writes" → the active feature's directory.
  - Put the no-argument invocation first in the examples (`/speckit-spectra-test-plan`), then `/speckit-spectra-test-plan specs/021-signed-webhooks` as a confirmation, then the `--non-interactive` form without a path.
  - Remove any sentence saying it never reads the feature record.
  - Do not touch generated regions.
- [X] T029 [P] Update `docs/index.html`:
  - The `speckit.spectra.test-plan` card at `:601`: replace "It will not guess which spec you meant: no branch-name inference, no feature record, no picker — with no argument it asks and stops, because…" with "It finds the feature the way the planning command does and says which one it used — no branch-name inference, no picker — and stops rather than write into a feature the planner won't plan."
  - The example at `:604`: becomes `/speckit-spectra-test-plan`.
  - Also check `README.md` and `spectra/README.md` hand-written prose for "spec path" / "requires" wording about test-plan.
- [X] T030 Add class `NoStaleProse` to `tests/test_test_plan_flow.py` (B21, B22):
  - The command front matter and the manifest's test-plan description contain neither "requires the spec path" nor "never inferred".
  - The `id=test-plan` block of `AGENTS_LIST.md` and the test-plan card in `docs/index.html` do not contain "no feature record".
  - The card's first example `<pre>` is `/speckit-spectra-test-plan` with no path.

  Run it.
- [X] T031 Run `python3 tools/build_package.py` to rebuild `docs/packages/spectra.zip` (after T007–T029).
- [X] T032 Run `python3 tools/generate_agent_docs.py --check`, `python3 -m unittest discover -s tests`, and `python3 tools/ship.py --dry-run`; all must pass. Compare the test count with T002's baseline and record it here. **Result (2026-10-25)**: 1678 tests OK (+24, all in `TP`); `--check` clean; ship dry-run passed catalog-parity, description-parity, generated-listings, zip-matches.
- [X] T033 Confirm `git diff --stat main -- spectra/commands/uat.md` is empty (B24, FR-022).
- [X] T034 Walk quickstart M1–M11 ([quickstart.md](./quickstart.md)) in a throwaway Spec Kit project with `specify extension add --dev /Users/alibahaloo/Projects/spectra/spectra`. After each run, compare test-plan's announced directory with `setup-plan.sh --json` `FEATURE_DIR` (SC-001), and check `git status` shows at most `test-plan.md` changed. Note deviations under this task.
  - **Done (2026-10-25)**: walked by the maintainer in a throwaway Spec Kit project; no deviations reported.

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (Phase 1)** → **Foundational (Phase 2, T003)** → user stories.
- **US1 (Phase 3)** depends only on T003. It is the MVP. T008a was added by `/speckit-analyze` (U1, U2); the letter suffix keeps later IDs stable.
- **US2 (Phase 4)** depends on US1's T009 (the Step 1 it extends).
- **US3 (Phase 5)** depends on T009. Its Step 13 and Step 16 edits (T019, T020) are independent of US2.
- **US4 (Phase 6)** depends on T009 (the placeholder) and T016 (the argument stop it lists).
- **Polish (Phase 7)** depends on every story. T031 depends on all edits under `spectra/`.

### Shared files (no `[P]` across these)

- `spectra/commands/test-plan.md`: T007 → T008 → T008a → T009 → T010 → T011 → T012 → T013 → T016 → T018 → T019 → T020 → T022 → T023 → T024.
- `tests/test_test_plan_flow.py`: T003 → T004 → T005 → T006 → T015 → T017 → T021 → T030.
- `spectra/extension.yml`: T014 → T025.

### Within each story

Test task first and failing → command edit → run `TP` green.

## Parallel Opportunities

- T002 alongside T001.
- T014 (manifest) alongside the US1 command edits.
- In Polish: T025, T026, T027, T028, T029 together, after T024; then T030 → T031 → T032 → T033 → T034.

```text
# After T003, one track — every story edits test-plan.md:
T004 → T005 → T006 → T007 → T008 → T008a … T013 (+ T014 in parallel) → T015 → T016 → T017 → T018 → T019 → T020 → T021 → T022 → T023
```

## Implementation Strategy

1. **MVP = Phases 1–3 (US1).** The common flow (specify → test-plan → plan) can no longer split a feature.
   Stop and check quickstart M1.
2. **Add US2 before shipping.** Without it an explicit path can still bring back the split.
3. **Add US3 and US4.** US3 keeps the approver's safeguard, and US4 gives every stop the same remedy.
4. **Polish once**, at the end: one version bump (1.27.0), one changelog entry, one zip rebuild, then
   `tools/ship.py`.
