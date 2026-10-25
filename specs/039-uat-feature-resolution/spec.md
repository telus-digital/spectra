# Feature Specification: UAT finds its feature the way the implement command does

**Feature Branch**: `039-uat-feature-resolution`

**Created**: 2026-10-25

**Status**: Implemented

**Input**: User description: "Make speckit.spectra.uat find its feature the same way /speckit-implement and /speckit-plan do, using the same resolution rule speckit.spectra.test-plan adopted in spec 038 (extension 1.27.0), so UAT always accepts the feature that was just implemented. (Full description: resolve the project root from SPECIFY_INIT_DIR or the nearest .specify/, the feature from SPECIFY_FEATURE_DIRECTORY then .specify/feature.json, empty is unset, read-only, one shell read before the run confirmation with a stop if denied; define the invoking project; announce the feature and repeat it in the run confirmation and the report; make the path argument an optional confirmation that stops on mismatch; one shared remedy block; keep the no-tasks.md stop; keep everything else; rewrite the governing rule, intro, never-infer section and never-table row; check the after_implement hook prompt; update descriptions, prose, card, CHANGELOG, version, package, and tests. test-plan and how UAT performs scenarios are out of scope.)"

## Context

`speckit.spectra.uat` runs after the implement command, on request. It reads a feature's `tasks.md` and
`test-plan.md`, starts the build after a run confirmation, performs the UAT scenarios it can drive, ticks
the `[UAT]` tasks it saw pass, and writes `uat-report.md` beside the spec.

Today it decides "which feature" differently from every command before it:

- **uat** takes the feature from a required path argument and is forbidden from consulting
  `.specify/feature.json`, the branch, or anything else.
- **The core commands** (`/speckit-plan`, `/speckit-tasks`, `/speckit-implement`) ignore any path. Spec
  Kit's `get_feature_paths` resolves the feature from `SPECIFY_INIT_DIR` (the project root), then
  `SPECIFY_FEATURE_DIRECTORY`, then `feature_directory` in `.specify/feature.json`, and errors if none
  yields one.

So after implement, the user must retype a path the workflow already knows, and the after-implement offer
gives uat nothing to go on. A mistyped or stale path makes uat start a build and tick `[UAT]` tasks in a
different feature's `tasks.md`. Those ticks look exactly like correct ones.

Spec 038 solved the same problem for `speckit.spectra.test-plan` (extension 1.27.0). This feature applies
that resolution rule to uat, adapted to a command that starts a build and writes ticks.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - UAT accepts the feature that was just implemented (Priority: P1)

A developer finishes `/speckit-implement`, accepts the offered UAT run (or runs it with no argument), and
confirms the build. UAT reads that feature's `tasks.md` and `test-plan.md`, and ticks and reports into that
feature only. No path is typed.

**Why this priority**: This is the defect. Every other story protects or explains this one.

**Independent Test**: In a project where `.specify/feature.json` names feature directory A, which has a
`tasks.md`, run uat with no argument. Confirm it announces A, shows A in the run confirmation, and ticks
and writes only inside A. Confirm the implement command's own resolution in the same state also yields A.

**Acceptance Scenarios**:

1. **Given** `.specify/feature.json` names a feature directory containing `tasks.md` and
   `SPECIFY_FEATURE_DIRECTORY` is not set, **When** uat runs with no argument, **Then** it accepts that
   feature, and every tick, evidence folder, and report it writes is inside that directory.
2. **Given** `SPECIFY_FEATURE_DIRECTORY` names directory B and `.specify/feature.json` names directory A,
   **When** uat runs with no argument, **Then** it resolves B — the directory the implement command would
   resolve — and says that the feature record pointed elsewhere.
3. **Given** uat is reached through the after-implement offer, **When** it runs, **Then** it resolves the
   feature by the same rule, with no path needed.

---

### User Story 2 - A mismatched path stops before anything is started (Priority: P1)

A developer passes an explicit feature path out of habit, or from a script written before this change,
and the path is not the active feature. uat refuses to start a build or tick anything, and says exactly
what each source pointed to.

**Why this priority**: An explicit path is the only remaining way to tick the wrong feature's tasks.
Without this stop, the fix is a default rather than a guarantee.

**Independent Test**: With `.specify/feature.json` naming A, pass B's directory. Confirm nothing is
started, read, ticked, or written, and the run names A, B, and the source of A.

**Acceptance Scenarios**:

1. **Given** the resolved feature is A, **When** the user passes directory A or A's `spec.md`, **Then** the
   run proceeds exactly as with no argument.
2. **Given** the resolved feature is A, **When** the user passes a path inside B, **Then** the run stops
   before reading anything else and before the run confirmation. It starts nothing, writes nothing, and
   reports A, B, the source A came from, and the two ways to make B the active feature.
3. **Given** no feature resolves, **When** the user passes a path to an existing feature, **Then** the run
   stops; the path never substitutes for resolution.

---

### User Story 3 - The person confirming the run sees which feature it touches (Priority: P2)

Whoever confirms the build, and whoever later reads the report, can see which feature directory was
resolved and from which source.

**Why this priority**: The old rule existed because ticks against the wrong feature are undetectable.
Resolving automatically is safe only when the resolution is visible at the moment of consent and in the
record.

**Independent Test**: Run with each source in turn. Confirm the resolved directory and its source are the
first thing said, appear again in the run confirmation, and are recorded in `uat-report.md` and in the
session report.

**Acceptance Scenarios**:

1. **Given** any successful resolution, **When** the run begins, **Then** the first thing it says is the
   resolved feature directory and its source.
2. **Given** the run confirmation is shown, **When** the user reads it, **Then** it names the feature
   directory whose `tasks.md` will be ticked, alongside the build command, the environment, and the
   scenarios.
3. **Given** a written `uat-report.md`, **When** someone opens it, **Then** its identifying block names
   the feature directory and the source it was resolved from.

---

### User Story 4 - Nothing resolves, and the run says how to fix it (Priority: P2)

A developer runs uat where no feature is active, or where the active feature has no `tasks.md`. The run
stops, starts and writes nothing, and names the remedy.

**Why this priority**: The implement command errors in the same situation. uat must not be more
permissive than the commands it follows, and must not guess.

**Independent Test**: Remove `.specify/feature.json` and unset the variable; run uat; confirm it stops with
a reason and the remedy block, and starts and writes nothing.

**Acceptance Scenarios**:

1. **Given** neither source yields a feature directory, **When** uat runs, **Then** it stops and shows
   the remedy block.
2. **Given** the resolved directory is missing, **When** uat runs, **Then** it stops, naming the directory
   and its source.
3. **Given** the resolved directory exists but has no `tasks.md`, **When** uat runs, **Then** it stops
   with the existing reason — there is nothing to accept until the tasks exist.
4. **Given** `.specify/feature.json` cannot be parsed or has no `feature_directory`, and the variable is
   not set, **When** uat runs, **Then** it stops and says why the record is unusable.

---

### Edge Cases

- **Both sources set and they disagree**: the variable wins, as it does for the implement command, and the
  run says the feature record pointed elsewhere. This is not a stop.
- **`SPECIFY_FEATURE_DIRECTORY` set to an empty string**: treated as unset.
- **A relative value**: resolved against the project root.
- **`SPECIFY_INIT_DIR` names another project**: that project's `.specify/feature.json` is read, and the
  out-of-project stop then fires, because the feature lies outside the invoking project.
- **`SPECIFY_INIT_DIR` names a missing directory, or one with no `.specify/`**: the run stops.
- **The environment read is denied or fails**: the run stops and starts nothing. It never resolves from
  the feature record alone.
- **An explicit path that names the same directory by a different spelling** (trailing slash, `./`,
  relative or absolute, the directory or its `spec.md`): a match.
- **An explicit path to another file inside the feature directory** (for example its `tasks.md`): a
  mismatch, since only the directory or its `spec.md` confirms.
- **`--env` given with no feature path**: allowed; `--env` and `--non-interactive` are parsed as today,
  and an unrecognized option never becomes a path.
- **`--non-interactive`**: the non-interactive announcement comes first, then the feature line. A feature
  that does not resolve still stops; otherwise it reports what it would attempt and writes nothing, as
  today.
- **The feature record changes during a long run** (for example, a parallel `specify`): no effect. Ticks
  and the report still go to the feature confirmed at the start (FR-017a).
- **Implementation incomplete in the resolved feature**: the existing gate applies to that feature's
  `tasks.md`, unchanged.

## Requirements *(mandatory)*

### Functional Requirements

**Resolution**

- **FR-001**: uat MUST resolve the feature directory from exactly two sources, in this order:
  `SPECIFY_FEATURE_DIRECTORY`, then `feature_directory` in `.specify/feature.json`. A variable that is set
  but empty MUST be treated as unset.
- **FR-002**: uat MUST determine the project root as the implement command does: `SPECIFY_INIT_DIR` when
  set and non-empty, otherwise the nearest directory containing `.specify/`. `.specify/feature.json` and
  relative feature directories MUST come from that root. A `SPECIFY_INIT_DIR` that names no existing
  directory, or one without `.specify/`, MUST stop the run with its value and the reason.
- **FR-003**: The feature MUST be the resolved directory; its `tasks.md`, `test-plan.md`, and `spec.md` are
  read from there.
- **FR-004**: uat MUST NOT consult the branch name, file modification times, the listing of `specs/`, a
  cache, a prior run, or session history to choose a feature, and MUST NOT offer a picker.
- **FR-005**: Resolution MUST be read-only: uat MUST NOT write `.specify/feature.json` or create the
  feature directory.
- **FR-006**: uat MAY run exactly one read-only shell read, once per run, of the values of
  `SPECIFY_INIT_DIR` and `SPECIFY_FEATURE_DIRECTORY`, given in POSIX and PowerShell forms. The values
  MUST be reused for the whole run. The read happens before the run confirmation and MUST be stated, in
  the never-table, as a read that starts no build, server, or process, so "start nothing before the run
  confirmation" still holds. It MUST be recorded among the sources consulted.
- **FR-007**: If the read is denied or fails, uat MUST stop before reading anything else, start nothing,
  write nothing, and say that the variables could not be checked. It MUST NOT fall back to
  `.specify/feature.json` alone.
- **FR-008**: The invoking project MUST be defined as the nearest directory containing `.specify/` above
  the current directory, regardless of `SPECIFY_INIT_DIR`. A resolved feature directory outside it MUST
  trip the existing out-of-project stop.

**Stops**

- **FR-009**: When neither source yields a feature directory, uat MUST stop before reading anything else,
  start nothing, write nothing, and show the remedy block.
- **FR-010**: When the resolved directory is missing, or `.specify/feature.json` is unparseable or lacks a
  value, uat MUST stop, name the directory or file and the reason, and show the remedy block.
- **FR-011**: The existing stop for a feature directory with no `tasks.md` MUST stay, applied to the
  resolved directory.
- **FR-012**: The feature path argument MUST be optional. When given, it MUST be compared to the resolved
  directory after normalizing spelling. It matches when it is the feature directory or its `spec.md`. On
  any other path, or when no feature resolves, uat MUST stop before reading anything else and before the
  run confirmation, start nothing, write nothing, and report the argument's path, the resolved directory,
  and its source, with the remedy block.
- **FR-013**: uat MUST NOT use an explicit path in place of resolution under any circumstances.
- **FR-014**: Every stop that concerns which feature is active MUST show one shared remedy block: set
  `SPECIFY_FEATURE_DIRECTORY` for the current session, or change `feature_directory` in
  `.specify/feature.json` to switch for good. "Run the specify command" MUST be offered only as the way to
  create a feature.

**Visibility**

- **FR-015**: On every successful resolution, the first statement of the run MUST name the resolved
  directory and its source, and, when the two sources disagreed, what the feature record named. Under
  `--non-interactive`, the non-interactive announcement comes first and this line immediately after it.
- **FR-016**: The run confirmation (Step 3) MUST name the feature directory whose `tasks.md` will be
  ticked, alongside what it already shows.
- **FR-017**: `uat-report.md`'s identifying block MUST record the feature directory and its source, and
  the session report MUST include the source.
- **FR-017a**: Ticks, evidence, and the report MUST go to the feature announced and confirmed at the start
  of the run. uat MUST NOT re-read `.specify/feature.json` later in the run; a change to it after the run
  confirmation does not redirect or cancel any write.

**Preserved behaviour**

- **FR-018**: These MUST be unchanged: `--env` and its rule; `--non-interactive`, except that "a missing
  feature still stops" becomes "a feature that does not resolve still stops"; the implementation-incomplete
  gate; the run confirmation gate; observed-pass-only ticking; never changing a human's tick or reverting a
  pass; evidence handling and secret masking; the edit scope in `tasks.md`; the report's location and run
  log; and every never-table row other than the one this feature replaces.
- **FR-019**: "The one rule that governs everything", the introduction ("Someone hands you a feature"),
  the "Never infer which feature was meant" section and its reasoning, and its never-table row MUST be
  rewritten to state the new rule — resolve only as the implement command does — and why: ticks are only
  trustworthy when they land in the feature that was just implemented, and the announcement plus the
  confirmation is what lets a person see which feature that is.

**Surfaces that describe the command**

- **FR-020**: The after-implement hook prompt MUST be checked and, if needed, reworded so it reads
  correctly for a command that needs no path.
- **FR-021**: The command's description in its front matter and in the extension manifest MUST no longer
  say the feature path is required or never inferred.
- **FR-022**: Hand-written uat prose in `AGENTS_LIST.md` and `spectra/README.md`, and the uat card and
  example in the landing page, MUST describe the new rule, with the no-argument form first.
- **FR-023**: The change MUST ship as an extension release: a minor version bump, a CHANGELOG entry that
  calls out that a path naming a feature other than the active one now stops, and a rebuilt package, all
  in the same change. The CLI channel MUST NOT be touched.
- **FR-024**: The tests that pin the old contract in `tests/test_uat_flow.py` MUST be rewritten to pin the
  new one.

**Out of scope**

- **FR-025**: `speckit.spectra.test-plan` and how UAT performs scenarios, captures evidence, or ticks tasks
  MUST NOT change.

### Key Entities

- **Feature directory**: the directory for one feature, holding `spec.md`, `test-plan.md`, `tasks.md`,
  `uat-report.md`, and the `uat/` evidence folders.
- **Resolution source**: `SPECIFY_FEATURE_DIRECTORY` or `.specify/feature.json`; stated in every
  successful run, in the run confirmation, and in the report.
- **Feature record**: `.specify/feature.json`, written by specify; read, never written, by uat.
- **Invoking project**: the nearest `.specify/` above the current directory; the boundary for the
  out-of-project stop.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In every run that starts a build, the feature uat ticks and reports into equals the feature
  the implement command resolves in the same project state — 0 mismatches across every combination of
  the two variables and the feature record being set, unset, empty, and disagreeing.
- **SC-002**: A developer following implement → UAT types no path.
- **SC-003**: Every run that could have ticked the wrong feature — a mismatched path, no resolvable feature,
  an unreadable environment — starts nothing and writes nothing, 100% of the time.
- **SC-004**: In 100% of runs that reach the run confirmation, the person confirming can name the feature
  whose `tasks.md` will be ticked from the confirmation alone.
- **SC-005**: Every behaviour listed in FR-018 is still asserted by the repository's tests after the change,
  and the full test suite and the documentation check pass.

## Clarifications

### Session 2026-10-25

- Q: Before writing ticks and the report, should uat re-check that `.specify/feature.json` still names the announced feature? → A: No. Ticks, evidence, and the report go to the feature announced and confirmed at the start; no re-check.

## Assumptions

- The resolution rule is the one in the Spec Kit version Spectra tests against, identical to the one
  spec 038 adopted for test-plan; the two commands should describe it in the same words.
- **No end-of-run agreement check** (confirmed in clarification, FR-017a). test-plan re-checks the feature record before printing its handoff
  because the handoff feeds another command. uat's ticks and report are bound to the feature announced
  and confirmed at the start; a later change to the record does not make them wrong. The next step it
  prints (the pull-request command) acts on the branch, not the feature record.
- The read happens before the run confirmation, and reading two environment variables is not starting a
  process. That keeps the "start nothing before the run confirmation" guarantee intact.
- An explicit path is kept as a confirmation, not removed, so existing scripts get a clear stop rather than
  a silently ignored argument.
- The change is to the extension only: the command file, manifest, prose, landing page, CHANGELOG, package,
  and tests. The `spectra` CLI is unaffected.
