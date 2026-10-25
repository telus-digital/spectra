# Tasks: UAT finds its feature the way the implement command does

**Input**: [spec.md](./spec.md), [plan.md](./plan.md), [research.md](./research.md),
[data-model.md](./data-model.md), [contracts/resolution-behaviour.md](./contracts/resolution-behaviour.md),
[quickstart.md](./quickstart.md)

**Branch**: `039-uat-feature-resolution`

**Tests**: requested (FR-024, SC-005). The behaviour contract pins B1–B25 as text assertions in
standard-library `unittest`. Every test goes in `tests/test_uat_flow.py`, abbreviated `UF`, and runs with
`python3 -m unittest discover -s tests -p "test_uat_flow.py"`. It uses the `phrases()` and
`command_text()` helpers the file already defines. Add a `section(heading_start, heading_end)` helper next
to them, as `tests/test_test_plan_flow.py` does. Within each story the test task comes first, and it must
fail before the command text it pins is written.

**Format**: `- [ ] [ID] [P?] [Story] Description`. `[P]` means a different file, with no dependency on an
incomplete task.

**Writing rules for `spectra/commands/uat.md`**:
- Keep the file hard-wrapped at the width it already uses (≈105 columns).
- Keep the command agent-agnostic (Principle III): name no agent's tool, and call the core command "the
  implement command".
- Wherever the meaning is the same, copy test-plan's Step 1 wording (`spectra/commands/test-plan.md:83-200`)
  and change only "the planning command" → "the implement command", "test-plan" → "uat", and `spec.md` →
  `tasks.md` (research R1).
- Never wrap part of an asserted phrase in bold, because the flattened assertion then misses. Bold the
  whole phrase or none of it.

---

## Phase 1: Setup (verify the premise)

- [X] T001 Confirm that the Evidence rows in `specs/039-uat-feature-resolution/plan.md` still hold on this branch:
  - `spectra/commands/uat.md:27-44` (User Input), `:52-53` (never-table rows), `:60-93` (Step 1, "Never infer", out-of-project stop), `:120-127` (Step 3 gates), `:203-219` (Steps 8–9), `:244-253` (Non-interactive), `:274` (skeleton identifying block);
  - `spectra/templates/uat-report-template.md:22` (Feature row);
  - `spectra/extension.yml:133-138` (`after_implement` uat prompt names no path);
  - `tests/test_uat_flow.py:14-15` (docstring) and `:77-97` (`TheFeatureIsRequiredAndNeverInferred`);
  - `spectra/extension.yml` and `catalog.json` at `1.27.0`.

  Correct any line reference in later tasks that has moved.
- [X] T002 [P] Run `python3 -m unittest discover -s tests` and `python3 tools/generate_agent_docs.py --check` on the unchanged branch. Record the baseline pass count here. **Baseline (2026-10-25)**: 1678 tests OK; `--check` clean (55 agents, 14 prose blocks).

**Checkpoint**: the premises hold, and the suite is green before any change.

---

## Phase 2: Foundational (retire the old contract in the tests)

- [X] T003 In `tests/test_uat_flow.py`:
  - Change the docstring bullet "**It never infers the feature.** Same reason as test-plan…" to "**It resolves the feature only as the implement command does**, and says which one, because ticks against the wrong feature are undetectably wrong."
  - Add the `section()` helper.
  - Rename class `TheFeatureIsRequiredAndNeverInferred` to `FeatureIsResolvedAsTheImplementCommandDoes`, with docstring "Spec 039 FR-001–FR-011, FR-014 — resolve as the implement command does, never otherwise".
  - Delete `test_the_feature_is_required`.
  - Rewrite `test_an_empty_argument_stops` as `test_every_resolution_stop_starts_and_writes_nothing`, asserting "starts nothing and writes nothing" in the Step 1 section.
  - Rewrite `test_it_never_infers_the_feature` as `test_it_resolves_only_as_the_implement_command_does`, asserting "resolve only as the implement command does" plus each of `("branch", "modification time", "listing of `specs/`")`. `feature.json` is now a permitted source.
  - Keep `test_it_offers_no_picker` ("do not offer a list") unchanged.
  - In `test_it_stops_when_the_feature_is_outside_the_project`, change the assertion from "outside the project" to "out-of-project", as test-plan's test does (`tests/test_test_plan_flow.py:231-234`). T011 rewrites the only sentence that contains "outside the project" (I1).
  - Add the constant `STEP_1 = ("## Step 1 — Resolve the feature", "## Step 2 —")`.

  This blocks every story phase. Run `UF`: two rewritten assertions fail. "resolve only as the implement command does" passes after T011, and "starts nothing and writes nothing" after T020. Everything else passes, because the Step 1 heading already exists (I2).

**Checkpoint**: the old contract is gone from the tests; the new one is pinned story by story.

---

## Phase 3: User Story 1 — UAT accepts the feature that was just implemented (Priority: P1) 🎯 MVP

**Goal**: with no argument, uat resolves the feature in this order: `SPECIFY_INIT_DIR` gives the root,
then `SPECIFY_FEATURE_DIRECTORY`, then `feature_directory` in `.specify/feature.json`. It reads that
directory's `tasks.md` and `test-plan.md`, and ticks and reports only inside it (FR-001–FR-008, FR-017a,
FR-018, FR-019; research R1, R2).

**Independent Test**: quickstart M1, M2, M3, M10, M12.

### Tests for User Story 1

- [X] T004 [US1] Add to `FeatureIsResolvedAsTheImplementCommandDoes` in `tests/test_uat_flow.py`:
  - **Order (B1, B2)**: in the flattened Step 1 section, the first occurrences of `specify_init_dir`, `specify_feature_directory` and `.specify/feature.json` appear in that order. The section also contains `nearest directory` and `.specify/`.
  - **Empty (B1)**: the section contains "set but empty" and "unset".
  - **Reads from the directory (B3)**: it contains "`tasks.md` in the feature directory".
  - **Read-only (B5)**: it contains "never writes `.specify/feature.json`" and "never creates the feature directory".
  - **Invoking project (B8)**: it contains "the invoking project is the nearest directory containing `.specify/`" and "regardless of `specify_init_dir`". "### The out-of-project stop" contains "the invoking project (step 1)".
  - **Governing rule (B19)**: "## The one rule that governs everything" contains "resolved exactly as the implement command resolves it".
  - **Intro (B19)**: the text before "## The one rule" no longer contains "someone hands you a feature".
- [X] T005 [US1] Add class `TheEnvironmentReadStartsNothing` to `tests/test_uat_flow.py` (B6, B7, B17). Its tests:
  - The Step 1 section contains "exactly one shell read", "once per run", both variable names, "posix" and "powershell".
  - The never-table's "start a build, a server, or any process before the run confirmation" row contains "the one shell read in step 1" and "starts nothing".
  - The Step 1 section contains "reused for the whole run" and "never read `.specify/feature.json` again".
  - The Step 1 section contains "record the read as an input".
- [X] T006 [US1] In `NonInteractiveStartsNothing`, add `test_a_feature_that_does_not_resolve_still_stops`. It asserts that the command contains "a feature that does not resolve still stops" and no longer contains "a missing feature still stops" (B18). Keep `test_non_interactive_starts_and_attempts_nothing` unchanged. Run `UF`; T004–T006 fail.

### Implementation for User Story 1

- [X] T007 [US1] In `spectra/commands/uat.md`, rewrite "## User Input":
  - "A **required** path to the feature, then optionally an environment and one flag" → "Optionally a path confirming the feature, an environment, and one flag".
  - Replace the paragraph "**The feature is required, and it is the only required input.** …" with: "**With no argument, the feature is resolved as Step 1 describes** — the same way the implement command finds it. **A path, if you give one, only confirms the feature Step 1 resolved; it never chooses one** (see "An argument only confirms" in Step 1)."
  - Delete the "**If no feature was supplied** … Read nothing, start nothing, write nothing." paragraph.
  - Keep the `--env` and `--non-interactive` paragraphs. Keep the rule that an unrecognized option is reported and ignored and never becomes part of the path.
- [X] T008 [US1] In the never-table of `spectra/commands/uat.md`:
  - Change the "Infer which feature was meant" row to "Choose a feature by any rule but the implement command's". Keep its reason, and add: "The implement command just built one feature; acceptance belongs to that one".
  - Append to the "Start a build, a server, or any process before the run confirmation" row's reason: "The one shell read in Step 1 — the values of two environment variables — starts nothing: it launches no build, server, or process and opens no connection; it is a read, not a start" (R2).
- [X] T009 [US1] Rewrite the quoted rule under "## The one rule that governs everything" in `spectra/commands/uat.md` to:
  > **Perform only the scenarios a human asked you to perform, on a build you were allowed to start, in the
  > feature resolved exactly as the implement command resolves it — and mark a UAT task done only when you
  > observed it pass, with the evidence linked.**

  Keep "Every rule that follows narrows that sentence. None widens it." unchanged.

  In the intro, change "Someone hands you a feature. You read the acceptance scenarios…" to "You resolve the feature the implement command just built, and read the acceptance scenarios…". The rest of the paragraph stays as it is.
- [X] T010 [US1] Replace "## Step 1 — Resolve the feature", its five-row table, and "Resolve the input before you read anything else." in `spectra/commands/uat.md`. The new section keeps the same heading and is written as research R1 and R2 describe:
  - Open with: "Resolve the feature before you read anything else, by the rule Spec Kit's implement command uses — its `get_feature_paths` — and by no other. The implement command just built this feature; ticks belong in its `tasks.md` and nowhere else."
  - (1) **The environment read.** One shell read, once per run, of `SPECIFY_INIT_DIR` and `SPECIFY_FEATURE_DIRECTORY`, in the POSIX and PowerShell forms from 038's R2 (copy from `test-plan.md` Step 1). It happens before the run confirmation and starts nothing. A set but empty variable is unset. The values are reused for the whole run. Add the sentence "Record the read as an input." T020a writes the two places it is recorded: Step 2, and the report's **Sources consulted and coverage**.
  - (2) **Project root.** `SPECIFY_INIT_DIR` when set; otherwise the nearest directory containing `.specify/`.
  - (3) **The invoking project** is the nearest directory containing `.specify/`, walking up from the current directory, regardless of `SPECIFY_INIT_DIR`.
  - (4) **The feature directory.** `SPECIFY_FEATURE_DIRECTORY` when it is set; otherwise `feature_directory` in `<root>/.specify/feature.json`. A relative value resolves against the project root.
  - (5) **What you accept against** is `tasks.md` in the feature directory, with its `test-plan.md` beside it.
  - Add the sentence: resolution is read-only. It **never writes `.specify/feature.json`** and **never creates the feature directory**.
  - Add: "**Reached through the after-implement offer or not, the feature is resolved identically.**"
  - Add: "**The feature is fixed for the run.** Ticks, evidence, and the report go to the feature announced here and named in the run confirmation. You never read `.specify/feature.json` again, so a change to it during the run redirects nothing" (FR-017a).
  - Leave a placeholder line "Stops: see the table below." for US4.
- [X] T011 [US1] In `spectra/commands/uat.md`, replace "### Never infer which feature was meant" with "### Resolve only as the implement command does":
  - It MUST NOT consult the branch name, file modification times, the listing of `specs/`, a cache, a prior run, or session history. Keep "do not offer a list of the features you can see — a picker is the same failure with one more keystroke".
  - Rewrite the reasoning paragraph, keeping its opening "the reason belongs here so whoever edits this next reads it first". Each tick is a claim that a person's acceptance criterion was met, and ticks against the wrong feature look exactly like the right ones. So uat takes the feature from the same record the implement command used, says which one before anything starts, and repeats it in the run confirmation. A person consenting to the run can see whose `tasks.md` will change (FR-019).
  - Keep the heading "### The out-of-project stop" exactly as it is; T003's test pins "out-of-project". In its text, change "the project you were invoked in" to "the invoking project (Step 1)". Replace "Your write destination comes from your input, so the input is where the scope is checked." with "Your write destination comes from Step 1, so that is where the scope is checked."
- [X] T012 [US1] In "## Non-interactive mode" of `spectra/commands/uat.md`, replace "A missing feature still stops." with "A feature that does not resolve still stops." Leave the rest of the paragraph unchanged (FR-018). Run `UF`; T004–T006 pass.

**Checkpoint**: US1 complete. Quickstart M1–M3, M10 and M12 would pass.

---

## Phase 4: User Story 2 — A mismatched path stops before anything is started (Priority: P1)

**Goal**: an argument only confirms. After normalizing, it must be the feature directory or its `spec.md`;
otherwise the run stops before anything is read or started (FR-012, FR-013; research R3).

**Independent Test**: quickstart M4, M5, M7.

### Tests for User Story 2

- [X] T013 [US2] Add class `AnArgumentOnlyConfirms` to `tests/test_uat_flow.py` (B11, B12). The Step 1 section contains:
  - "the feature directory or its `spec.md`"
  - "trailing slash"
  - "any other path" and "stop before reading anything else"
  - "the argument's path, the resolved directory, and its source"
  - "an argument is never used in place of"
  - "after `--env` and `--non-interactive` are removed"
  - "when no feature resolves", together with "names the argument's path and the reason" (U2)

  Also add `test_options_never_become_the_path` (C1): the "## User Input" section contains "`--env <name-or-url>`" and "never silently becomes part of the path". It passes today (`uat.md:44`). It is a regression guard so that T007 keeps that sentence.

  Run `UF`; the Step 1 assertions fail, and the C1 guard passes.

### Implementation for User Story 2

- [X] T014 [US2] In Step 1 of `spectra/commands/uat.md`, add "### An argument only confirms" after the resolution list. Copy test-plan's sub-section, adapted as research R3 says:
  - The argument is what remains after `--env` and `--non-interactive` are removed.
  - Resolve it against the project root and normalize it: drop a trailing slash and any `./` segments, and compare relative and absolute forms alike.
  - It matches when it is the feature directory or its `spec.md`. Any other path, including the directory's `tasks.md`, is a mismatch.
  - On a mismatch, stop before reading anything else and before the run confirmation. Start nothing, write nothing, and report the argument's path, the resolved directory, and its source, then the remedy block.
  - An argument is never used in place of resolution, including when no feature resolves. In that case the stop is the resolution stop that fired (no feature, unusable record, or missing directory). It names the argument's path and the reason in place of a resolved directory and source, and shows the remedy block (U2, FR-012).

  Run `UF`; T013 passes.

**Checkpoint**: US1 and US2 close the defect. Quickstart M4, M5 and M7 would pass.

---

## Phase 5: User Story 3 — The person confirming the run sees which feature it touches (Priority: P2)

**Goal**: the resolution is announced first, repeated in the run confirmation, and recorded in the report
and the session report (FR-015–FR-017; research R4; data-model "Announcement", "Run confirmation", "Report
Feature row").

**Independent Test**: quickstart M1, M2, M11.

### Tests for User Story 3

- [X] T015 [US3] Add class `TheResolutionIsAnnounced` to `tests/test_uat_flow.py` (B14–B16):
  - Step 1 contains "the first thing you say", the example `Feature: specs/` and "(from .specify/feature.json)".
  - Step 1 contains the disagreeing form "; .specify/feature.json names".
  - Step 1 contains "the non-interactive announcement comes first". "## Non-interactive mode" contains "before the feature line in step 1".
  - The Step 3 section contains "the feature directory whose `tasks.md` will be ticked".
  - The Step 8 section contains "resolved from".
  - The Step 9 section contains "**feature**" and "the source it was resolved from".
  - The inline skeleton's identifying-block comment contains "where it was resolved from".
  - `TEMPLATE` (`uat-report-template.md`) is unchanged: it still contains "| **Feature** | [project-relative path to the feature directory] |".

  Run `UF`; it fails.

### Implementation for User Story 3

- [X] T016 [US3] In Step 1 of `spectra/commands/uat.md`, add after resolution: "**Announce it before reading anything else** — the first thing you say", with the two example lines from data-model.md "Announcement". Add: "Under `--non-interactive`, the non-interactive announcement comes first and this line immediately after it." In "## Non-interactive mode", change "**Announce it once, up front.**" to "**Announce it once, up front** — before the feature line in Step 1."
- [X] T017 [US3] In "## Step 3 — The gates" of `spectra/commands/uat.md`, change the run confirmation sentence to: "Show the feature directory whose `tasks.md` will be ticked and whose `uat/` folder will receive evidence, and the source it was resolved from; the exact command you will run to start the build; the environment it targets; and the scenarios you intend to attempt." Leave the rest of the gate unchanged.
- [X] T018 [US3] In "## Step 8 — Write the report" of `spectra/commands/uat.md`, add: "Fill the identifying block's **Feature** with the project-relative feature directory followed by "resolved from `SPECIFY_FEATURE_DIRECTORY`" or "resolved from `.specify/feature.json`", and, when the two disagreed, what the record named." The template is not changed (R4).

  In "## Step 9 — Report in the session", add a first bullet: "**Feature** — the feature directory and the source it was resolved from."

  In the inline skeleton, change the comment `feature | build under test | environment | date` to `feature (and where it was resolved from) | build under test | environment | date`. Run `UF`; T015 passes.

**Checkpoint**: US3 complete.

---

## Phase 6: User Story 4 — Nothing resolves, and the run says how to fix it (Priority: P2)

**Goal**: every resolution stop starts nothing, writes nothing, and shows the one remedy block (FR-007,
FR-009–FR-011, FR-014; research R5; data-model "Stops").

**Independent Test**: quickstart M6, M7, M8, M9, M13.

### Tests for User Story 4

- [X] T019 [US4] Add to `FeatureIsResolvedAsTheImplementCommandDoes` in `tests/test_uat_flow.py` (B2, B7, B9, B10, B13):
  - Step 1 contains a table whose rows name each stop. Assert each phrase: "the shell read is denied or fails", "names no existing directory", "neither source", "cannot be parsed", "does not exist", "has no `tasks.md`".
  - The text contains "never fall back to `.specify/feature.json` alone".
  - The remedy block appears: "to choose the feature without uat writing anything", "for this session" with `set SPECIFY_FEATURE_DIRECTORY=`, "for good" with `"feature_directory" in .specify/feature.json`, and "to create a new feature, run the specify command".
  - Add `test_step_one_counts_its_own_outcomes`, modelled on test-plan's. It slices from "## Step 1 — Resolve the feature" to "### An argument only confirms", reads the "<N> outcomes:" word, and checks it against the table's row count.

  Run `UF`; it fails.

### Implementation for User Story 4

- [X] T020 [US4] Replace the placeholder from T010 in `spectra/commands/uat.md` with "Eight outcomes:" and a `| Input | What you do |` table of exactly eight rows (research R5):
  - resolved, with no argument or a matching one → announce and continue;
  - the shell read is denied or fails → stop; say the variables could not be checked; never fall back to `.specify/feature.json` alone;
  - `SPECIFY_INIT_DIR` names no existing directory, or one with no `.specify/` → stop with its value and the reason, and say to unset or correct it;
  - neither source set → stop, remedy block;
  - `.specify/feature.json` cannot be parsed or has no `feature_directory` → stop, remedy block;
  - the feature directory does not exist → stop, naming it and its source, remedy block;
  - the feature directory has no `tasks.md` → report that there is nothing to accept until the tasks exist; stop, remedy block;
  - an argument that does not match → stop (US2), remedy block.

  Follow the table with: "Every stop **starts nothing and writes nothing** — no evidence folder, no report." Then add the remedy block once, verbatim from research R5, introduced by "The remedy block, used by every stop that concerns which feature is active:". Run `UF`; T019 passes, and so do T003's rewritten tests.
- [X] T020a [US4] Record the environment read among the sources consulted (FR-006, U1). This task was added by `/speckit-analyze`; the letter suffix keeps later IDs stable.
  - **Test first**: add `test_the_environment_read_is_recorded_as_a_source` to `TheEnvironmentReadStartsNothing` in `tests/test_uat_flow.py`. It asserts that the "## Step 2 —" section contains "the environment read" and that the inline skeleton's "Sources consulted and coverage" comment contains "environment read". Run `UF`; it fails.
  - **Command**: in "## Step 2 — Read what you will accept against" of `spectra/commands/uat.md`, add a sentence just before the numbered list: "Record **the environment read** from Step 1 as an input — which of `SPECIFY_INIT_DIR` and `SPECIFY_FEATURE_DIRECTORY` was set, and never more than the resolved directory." In the inline skeleton, change the comment on "## Sources consulted and coverage" from "read; could not read; nothing modified beyond tasks.md UAT lines" to "read; environment read; could not read; nothing modified beyond tasks.md UAT lines".
  - Run `UF`; it passes.

**Checkpoint**: all four stories complete.

---

## Phase 7: Polish & Cross-Cutting Concerns (release surfaces, Principle V)

- [X] T021 In the front matter `description` of `spectra/commands/uat.md`, replace "The feature path is required and never inferred." with "Finds the feature the way the implement command does — from SPECIFY_FEATURE_DIRECTORY or .specify/feature.json — names it before anything starts and in the run confirmation, and stops rather than guess."
- [X] T022 [P] In `spectra/extension.yml`:
  - Set `version` to `1.28.0`.
  - In the `speckit.spectra.uat` description, replace the required/never-inferred wording with the same sentence as T021.
  - Leave the `after_implement` uat prompt unchanged (R6, FR-020).
- [X] T023 [P] Set the `spectra` entry's `version` in `catalog.json` to `1.28.0`.
- [X] T024 [P] Add `## [1.28.0] - 2026-10-25` to the top of `spectra/CHANGELOG.md`, with a one-line summary and a **Changed** list (R7). List items:
  - uat resolves its feature as the implement command does (root from `SPECIFY_INIT_DIR`; then `SPECIFY_FEATURE_DIRECTORY`, then `.specify/feature.json`; empty is unset), announces it, and names it in the run confirmation and the report;
  - **the path argument is optional, and a path naming a feature other than the active one now stops**, with the two ways to switch;
  - one read-only shell read of two environment variables, before the run confirmation; it starts nothing, and a denied read stops;
  - the after-implement offer now needs no path. This closes the candidate noted in 1.27.0.
- [X] T025 [P] Update the hand-written `<!-- SPECTRA:AGENT id=uat -->` block in `AGENTS_LIST.md` (≈`:657`+):
  - The "Arguments" item becomes: optional; the feature is found the way the implement command finds it, and a path only confirms it.
  - Examples, no-argument form first: `/speckit-spectra-uat`, then `/speckit-spectra-uat --env staging`, then `/speckit-spectra-uat specs/021-signed-webhooks` as a confirmation.
  - Remove "required" and "never inferred".
  - Do not touch generated regions.
- [X] T026 [P] Update the uat section of `spectra/README.md` (≈`:945`+):
  - The usage example becomes `/speckit-spectra-uat`.
  - Replace "The feature is required." with one sentence on resolution and confirmation.
  - Check the root `README.md` for hand-written uat prose saying "required", and fix any it has.
- [X] T027 [P] Update `docs/index.html`:
  - The uat card args at `:609`: replace "the feature directory (<b>required</b> — never inferred)" with "optional — the feature is found the way the implement command finds it; a path only confirms it".
  - The example at `:611` becomes `/speckit-spectra-uat`.
  - *Recorded by convergence (T034)*: the uat step in `docs/getting-started/spectra.html:230` also showed a path (`/speckit-spectra-uat specs/001-signup`). It now reads `/speckit-spectra-uat` and says no path is needed. Kept, because it is a hand-written page describing the uat command (FR-022).
- [X] T028 Add class `NoStaleProse` to `tests/test_uat_flow.py` (B19–B22):
  - The command front matter and the manifest's uat description contain neither "required" nor "never inferred".
  - The command contains neither "never infer which feature was meant" nor "the feature is required".
  - The exact stale strings are gone (A1). Flatten each file's text before checking:
    - the `id=uat` block of `AGENTS_LIST.md` does not contain "**required**, and never inferred";
    - the uat section of `spectra/README.md` does not contain "The feature is required.";
    - the uat card in `docs/index.html` does not contain "<b>required</b> — never inferred".
  - The card's first example is `/speckit-spectra-uat` with no path.
  - The `after_implement` uat prompt in `hooks_block()` contains no `specs/` and no `SPEC_FILE` (B20).

  Run it.
- [X] T029 Run `python3 tools/build_package.py` to rebuild `docs/packages/spectra.zip`. Run it after T007–T027.
- [X] T030 Run `python3 tools/generate_agent_docs.py --check`, `python3 -m unittest discover -s tests` and `python3 tools/ship.py --dry-run`; all must pass. Compare the test count with T002's baseline and record it here. **Result (2026-10-25)**: 1711 tests OK (+33, all in `UF`); `--check` clean; ship dry-run passed catalog-parity, description-parity, generated-listings, zip-matches.
- [X] T031 Confirm `git diff --stat main -- spectra/commands/test-plan.md spectra/templates/uat-report-template.md VERSION` is empty (B25, FR-023, FR-025). Review `git diff main -- spectra/commands/uat.md` for edits in Steps 4–7. There should be none, apart from Step 2's environment-read sentence from T020a (FR-018, FR-025). **Result**: the three paths are unchanged; `uat.md` hunks fall only in the front matter, intro, governing rule, User Input, never-table, Steps 1, 2, 3, 8 and 9, Non-interactive, and the skeleton.
- [X] T032 Walk quickstart M1–M13 ([quickstart.md](./quickstart.md)) in a throwaway Spec Kit project with `specify extension add --dev /Users/alibahaloo/Projects/spectra/spectra`. After each run:
  - compare uat's announced directory with `check-prerequisites.sh --json --paths-only` `FEATURE_DIR` (SC-001);
  - check that `git status` shows changes only inside the resolved feature, and none after a stop (SC-003).

  Note any deviations under this task.
  - **Done (2026-10-25)**: walked by the maintainer in a throwaway Spec Kit project; no deviations reported.

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (Phase 1)** → **Foundational (Phase 2, T003)** → user stories.
- **US1 (Phase 3)** depends only on T003. It is the MVP.
- **US2 (Phase 4)** depends on US1's T010, the Step 1 it extends.
- **US3 (Phase 5)** depends on T010. Its Step 3, 8 and 9 edits (T017, T018) are independent of US2.
- **US4 (Phase 6)** depends on T010 (the placeholder) and T014 (the argument stop it lists). T020a was added by `/speckit-analyze` (U1); the letter suffix keeps later IDs stable.
- **Polish (Phase 7)** depends on every story. T029 depends on all edits under `spectra/`.

### Shared files (no `[P]` across these)

- `spectra/commands/uat.md`: T007 → T008 → T009 → T010 → T011 → T012 → T014 → T016 → T017 → T018 → T020 → T020a → T021.
- `tests/test_uat_flow.py`: T003 → T004 → T005 → T006 → T013 → T015 → T019 → T020a → T028.
- `spectra/extension.yml`: T022 only.

### Within each story

Write the test task first and see it fail, then make the command edit, then run `UF` to green.

## Parallel Opportunities

- T002 alongside T001.
- In Polish: T022, T023, T024, T025, T026 and T027 together, after T021. Then T028 → T029 → T030 → T031 → T032.

```text
# After T003, one track — every story edits uat.md:
T004 → T005 → T006 → T007 … T012 → T013 → T014 → T015 → T016 → T017 → T018 → T019 → T020 → T020a
```

## Implementation Strategy

1. **MVP = Phases 1–3 (US1).** The implement → UAT flow ticks the feature just built, with no path.
   Check quickstart M1.
2. **Add US2 before shipping.** Without it, an explicit path can still tick the wrong feature.
3. **Add US3 and US4.** US3 makes the feature visible at the moment of consent. US4 gives every stop the
   same remedy.
4. **Polish once, at the end**: one version bump (1.28.0), one changelog entry, and one zip rebuild. Then
   land it with `tools/ship.py`.

---

## Phase 8: Convergence

- [X] T033 In "## Step 8 — Write the report" of `spectra/commands/uat.md`, change "Rewrite it on every run" to "Rewrite the report on every run". The new **Feature** paragraph now comes before that sentence, so "it" reads as the Feature row rather than the report per FR-018 (partial)
- [X] T034 Review the edit to `docs/getting-started/spectra.html` (the uat step now reads `/speckit-spectra-uat` with no path). No task named that page. Keep it as part of FR-022's intent, and record it under T027, or revert it per FR-022 (unrequested)
