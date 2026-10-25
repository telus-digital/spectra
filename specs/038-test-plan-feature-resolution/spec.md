# Feature Specification: Test plan finds its feature the way the planner does

**Feature Branch**: `038-test-plan-feature-resolution`

**Created**: 2026-10-25

**Status**: Implemented

**Input**: User description: "Make speckit.spectra.test-plan find its feature the same way /speckit-plan does, so the test plan and the plan it hands off to always end up in the same feature directory. Problem: test-plan requires an explicit spec path and is forbidden from reading .specify/feature.json or the branch. /speckit-plan ignores any path it is given. Its setup script finds the feature only from the SPECIFY_FEATURE_DIRECTORY environment variable, then .specify/feature.json, and errors if neither is set. When the two disagree, test-plan writes specs/A/test-plan.md and prints a handoff naming it, while /speckit-plan writes plan.md into specs/B. Nothing warns about this, and the 'Testing obligations' end up attached to the wrong feature. (Full description: resolve in the planner's order, stop when nothing resolves, make the path argument optional and stop on disagreement, announce the resolved feature and its source, keep every existing safeguard, emit the handoff only when the planner will plan the same directory; also rewrite the never-infer section, the after_specify hook prompt, the descriptions, CHANGELOG, version, package, and docs. speckit.spectra.uat is out of scope.)"

## Context

`speckit.spectra.test-plan` runs between `speckit.specify` and the planning command. It writes
`test-plan.md` beside a specification, then prints a ready-to-paste planning prompt that tells the planner
to carry the test plan's obligations into `plan.md`.

Today the two commands decide "which feature" by different rules:

- **The test plan** takes the specification path from its argument and is forbidden from consulting
  `.specify/feature.json`, the branch, or anything else.
- **The planning command** ignores any path in its argument. Spec Kit's setup script resolves the feature
  directory from `SPECIFY_FEATURE_DIRECTORY`, then from `feature_directory` in `.specify/feature.json`,
  and errors if neither yields one.

When the path a user hands the test plan is not the feature the planner will resolve, the test plan is
written to one feature, the handoff names it, and the planner writes `plan.md` — with the "Testing
obligations" section that cites the other feature's test plan — into a different directory. Nothing in
either command detects or reports this. The approved test plan then never reaches the tasks of the
feature it was approved for.

This feature makes the test plan resolve its feature by the planner's rule, so the two cannot disagree.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The test plan lands in the feature the planner will plan (Priority: P1)

A developer runs specify, accepts the offered test plan (or runs it with no argument), reviews the
result, and pastes the printed planning prompt. The test plan, the plan, and the "Testing obligations"
section all belong to the same feature directory, with no path typed by hand.

**Why this priority**: This is the defect. Every other story only protects or explains this one.

**Independent Test**: In a project where `.specify/feature.json` names feature directory A, run the test
plan with no argument; confirm it writes A's `test-plan.md` and that its handoff names A. Then confirm the
planning command, run with the printed prompt, resolves A.

**Acceptance Scenarios**:

1. **Given** `.specify/feature.json` names a feature directory containing `spec.md` and
   `SPECIFY_FEATURE_DIRECTORY` is not set, **When** the test plan runs with no argument, **Then** it reads
   that directory's `spec.md`, writes `test-plan.md` in that directory, and emits a handoff naming that
   file.
2. **Given** `SPECIFY_FEATURE_DIRECTORY` names directory B and `.specify/feature.json` names directory A,
   **When** the test plan runs with no argument, **Then** it resolves B — the same directory the planning
   command would — and reports that the feature record pointed elsewhere.
3. **Given** the test plan is reached through the after-specify offer, **When** it runs, **Then** it
   resolves the feature that specify just recorded, by the same rule, with no path needed.

---

### User Story 2 - A mismatched path stops the run instead of splitting the feature (Priority: P1)

A developer passes an explicit specification path out of habit, or from a script written before this
change, and the path is not the feature the planner will resolve. The test plan refuses to write and
says exactly what each source pointed to, so the developer can fix the active feature or the path.

**Why this priority**: An explicit path is the only remaining way the original defect can recur. Without
this stop, the fix is a default, not a guarantee.

**Independent Test**: With `.specify/feature.json` naming A, pass the path of B's `spec.md`; confirm the run
writes nothing, emits no handoff, and names A, B, and the source that produced A.

**Acceptance Scenarios**:

1. **Given** the resolved feature is A, **When** the user passes a path to A's `spec.md` or to directory A,
   **Then** the run proceeds exactly as with no argument.
2. **Given** the resolved feature is A, **When** the user passes a path inside B, **Then** the run stops
   before reading the specification, writes nothing, emits no handoff, and reports A, B, the source A came
   from, and the two ways to make B the active feature (FR-023).
3. **Given** no feature resolves, **When** the user passes a path to an existing specification, **Then**
   the run stops — the path is never used as a substitute for the planner's resolution, because the
   planner would not use it either.

---

### User Story 3 - The approver can see which specification the plan was built against (Priority: P2)

Whoever approves the test plan, and whoever reads the session, can see which feature directory was
resolved and from which source, before any analysis output appears.

**Why this priority**: The old rule existed because a plan written against the wrong specification is
"undetectably wrong to whoever approves it". Resolving automatically is safe only if the resolution is
visible; this story keeps that protection under the new rule.

**Independent Test**: Run with each source in turn and confirm the resolved directory and its source are
stated at the start of the session output and in the written document's identifying block.

**Acceptance Scenarios**:

1. **Given** any successful resolution, **When** the run begins, **Then** the first thing it says is the
   resolved feature directory and its source (`SPECIFY_FEATURE_DIRECTORY` or `.specify/feature.json`).
2. **Given** a written `test-plan.md`, **When** a stakeholder opens it, **Then** its identifying block names
   the specification path and the source the feature was resolved from.

---

### User Story 4 - Nothing resolves, and the run says how to fix it (Priority: P2)

A developer runs the test plan in a project where no feature is active, or where the active feature's
directory or specification is missing. The run stops, reads and writes nothing, and names the remedy.

**Why this priority**: The planner errors in the same situation; the test plan must not be more permissive
than the command it hands off to, and must not guess.

**Independent Test**: Remove `.specify/feature.json` and unset the variable; run the test plan; confirm it
stops with a reason and a remedy and writes nothing.

**Acceptance Scenarios**:

1. **Given** neither source yields a feature directory, **When** the test plan runs, **Then** it stops,
   says neither source was set, and names the remedies: run the specify command to create a feature, or,
   for an existing feature, set `SPECIFY_FEATURE_DIRECTORY` or change `feature_directory` in
   `.specify/feature.json`.
2. **Given** the resolved directory does not exist, or exists with no `spec.md`, **When** the test plan
   runs, **Then** it stops, names the directory and its source, and writes nothing.
3. **Given** `.specify/feature.json` exists but cannot be parsed or has no `feature_directory` value,
   **When** the test plan runs and the variable is not set, **Then** it stops and says the feature record
   is unusable and why.

---

### Edge Cases

- **Both sources set and they disagree**: the variable wins, as it does for the planner, and the run says
  the feature record pointed elsewhere. This is not a stop — the planner will plan the variable's
  directory, so writing there is correct.
- **A relative value**: resolved against the project root, as the planner does.
- **`SPECIFY_FEATURE_DIRECTORY` set to an empty string**: treated as unset; the feature record is used.
- **`SPECIFY_INIT_DIR` names another project**: that project's `.specify/feature.json` is the one the
  planner reads, so it is the one test-plan reads; the existing out-of-project stop then applies if the
  resolved directory lies outside the invoking project.
- **`SPECIFY_INIT_DIR` names a missing directory or one with no `.specify/`**: the run stops, as the
  planner's setup errors.
- **A resolved directory outside the invoking project**: the existing out-of-project stop applies, unchanged.
- **The resolved `spec.md` fails the usability test** (for example, a stub left by an interrupted specify
  run): the existing usability stop applies, unchanged.
- **An explicit path that resolves to the same directory by a different spelling** (trailing slash,
  relative vs. absolute, the directory vs. its `spec.md`): treated as a match, not a disagreement.
- **The feature record changes between resolution and the write** (for example, a parallel session runs
  specify): the handoff is emitted only if the directory written to is still the one the planner will
  resolve; otherwise the run reports the change and emits no handoff.
- **An existing `test-plan.md` in the resolved directory**: the existing ask-before-rewrite rule and the
  non-interactive no-rewrite rule apply, unchanged.
- **An unrecognized flag**: still reported and ignored; it never becomes a path.
- **The variable cannot be read** (the shell read is denied or fails): the run stops and writes nothing,
  rather than resolving from the feature record alone and risking the mismatch this feature removes.

## Requirements *(mandatory)*

### Functional Requirements

**Resolution**

- **FR-001**: The test plan MUST resolve the feature directory from exactly two sources, in this order:
  the `SPECIFY_FEATURE_DIRECTORY` environment variable, then the `feature_directory` value in
  `.specify/feature.json` — the same sources, in the same order, as Spec Kit's planning setup. A variable
  that is set but empty MUST be treated as unset, as the planner treats it.
- **FR-001a**: The test plan MUST determine the project root the way the planner does: the
  `SPECIFY_INIT_DIR` environment variable when it is set and non-empty, otherwise the nearest directory
  containing `.specify/`. The `.specify/feature.json` that is read, and the root a relative feature
  directory resolves against, MUST both come from that project root. When `SPECIFY_INIT_DIR` is set but
  names no existing directory, or a directory without `.specify/`, the test plan MUST stop and say so,
  as the planner errors.
- **FR-002**: The specification read MUST be `spec.md` in the resolved directory.
- **FR-003**: The test plan MUST NOT consult the branch name, file modification times, the contents or
  listing of `specs/`, a cache, a prior run, or session history to resolve or choose a feature, and MUST
  NOT offer a picker.
- **FR-004**: Resolution MUST be read-only: the test plan MUST NOT create, update, or normalize
  `.specify/feature.json`, and MUST NOT create the feature directory.
- **FR-005**: The test plan MAY run exactly one command, once per run: a read-only shell read of the
  values of `SPECIFY_INIT_DIR` and `SPECIFY_FEATURE_DIRECTORY`. This MUST be stated in the command as the
  only exception to its "runs nothing" guarantee, MUST NOT modify any file or environment state, and MUST
  be reported in the run's sources. The values it returns MUST be used for the whole run, including the
  check in FR-014; no later step reads them again. If the read cannot be performed, the test plan MUST
  stop before reading the specification, write nothing, emit no handoff, and say that the variables could
  not be checked, so the planner's feature cannot be confirmed. It MUST NOT fall back to
  `.specify/feature.json` alone.

**Stops**

- **FR-006**: When neither source yields a feature directory, the test plan MUST stop before reading
  anything else, write nothing, and name the remedies in FR-023.
- **FR-007**: When the resolved directory is missing, has no `spec.md`, or `.specify/feature.json` is
  unparseable or lacks a value, the test plan MUST stop, name the directory or file and the reason, and
  write nothing.
- **FR-008**: The specification path argument MUST be optional. When supplied, the test plan MUST compare
  it to the resolved feature directory after normalizing spelling; on a match it proceeds, and on a
  mismatch — or when no feature resolves — it MUST stop before reading the specification, write nothing,
  emit no handoff, and report the argument's directory, the resolved directory, and the source.
- **FR-009**: The test plan MUST NOT use an explicit path in place of the planner's resolution under any
  circumstances.
- **FR-023**: Every stop that concerns which feature is active (FR-006, FR-007, FR-008) MUST name how to
  switch the active feature without test-plan writing anything: set `SPECIFY_FEATURE_DIRECTORY` for the
  current session, or change `feature_directory` in `.specify/feature.json` to switch for good. "Run the
  specify command" MUST be offered only as the way to create a feature, never as the way to select an
  existing one.

**Visibility**

- **FR-010**: On every successful resolution, the first statement of the run MUST name the resolved
  directory and its source. When both sources were set and disagreed, it MUST also name the directory the
  feature record pointed to.
- **FR-011**: The written test plan's identifying block MUST record the specification path and the source
  the feature was resolved from.
- **FR-012**: The run report MUST include the resolution source alongside the written path.

**Handoff**

- **FR-013**: The Step 17 planning prompt MUST keep its current content and clauses.
- **FR-014**: The handoff MUST be emitted only when a file was written and the directory written to is
  still the directory the planner will resolve at the end of the run; otherwise the run MUST say why no
  handoff was emitted. This check MUST reuse the variable values read once under FR-005 and re-read only
  `.specify/feature.json`, which is the one source that can change during a run.

**Preserved behaviour**

- **FR-015**: These existing behaviours MUST be unchanged: the out-of-project stop; the specification
  usability test; writing exactly one file, `test-plan.md`, beside the specification; ask-before-rewrite;
  non-interactive mode (including that it never rewrites an existing plan); the `--non-interactive` flag
  and the handling of unrecognized flags; R1–R6; and every entry in "What this command never does" other
  than the one this feature replaces.
- **FR-016**: The "Never infer which specification was meant" section and the corresponding "never" table
  row MUST be rewritten to state the new rule — resolve only by the planner's sources, never by any other
  — and its reasoning: the test plan and the planner must agree on the feature, and visibility of the
  resolution is what protects the approver.

**Surfaces that describe the command**

- **FR-017**: The after-specify hook prompt in the extension manifest MUST no longer tell the agent to pass
  the spec file path, and MUST describe the test plan as using the feature specify just recorded.
- **FR-018**: The command's description MUST be updated wherever it is declared — the command file's
  front matter, the extension manifest, the roster, and the catalog — so none says the path is required or
  never inferred.
- **FR-019**: Hand-written documentation that says the path is required, or shows a path as the only way
  to invoke the command, MUST be updated; examples MUST show the no-argument form first.
- **FR-020**: The change MUST ship as an extension release: a version bump, a CHANGELOG entry that names
  the behaviour change for anyone who scripted the old required-path form, and a rebuilt package, all in
  the same change. The CLI channel MUST NOT be touched.
- **FR-021**: The repository's tests that assert the old contract (required path, never reading
  `.specify/feature.json`, the hook prompt passing the path) MUST be updated to assert the new one.

**Out of scope**

- **FR-022**: `speckit.spectra.uat` MUST NOT change. Its own required, never-inferred feature path MUST be
  recorded as a candidate for the same change.

### Key Entities

- **Feature directory**: the directory for one feature (for example, `specs/038-…`) that holds its
  `spec.md`, `test-plan.md`, and `plan.md`.
- **Resolution source**: where the feature directory came from — the environment variable or the feature
  record — stated in every successful run.
- **Feature record**: `.specify/feature.json`, written by specify and read by the planner; read, never
  written, by the test plan.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In every successful run, the directory the test plan writes to equals the directory the
  planning command resolves in the same project state — 0 mismatches across every combination of the two
  sources being set, unset, and disagreeing.
- **SC-002**: A developer following specify → test plan → plan types no path at any step.
- **SC-003**: Every run that could have split a feature across two directories (mismatched explicit path,
  record changed mid-run) ends with nothing written or no handoff, and names both directories — 100% of
  such cases.
- **SC-004**: In 100% of successful runs, a reader of the session or of the written document can name the
  resolved directory and its source without looking anywhere else.
- **SC-005**: Every behaviour listed in FR-015 is still asserted by the repository's tests after the change,
  and the full test suite and the documentation check pass.

## Clarifications

### Session 2026-10-25

- Q: How does test-plan read `SPECIFY_FEATURE_DIRECTORY` without breaking "runs nothing"? → A: One read-only shell read of the variable is allowed, stated as the only exception to "runs nothing".
- Q: If the variable cannot be read, stop or fall back to `.specify/feature.json`? → A: Stop and write nothing; never fall back.
- Q: Which remedy does a feature-selection stop name? → A: Both — set `SPECIFY_FEATURE_DIRECTORY` for the session, or change `feature_directory` in `.specify/feature.json` for good; "run specify" only to create a feature.
- Q: Which planner rules did the first draft miss? → A: `SPECIFY_INIT_DIR` as the project-root override; a set-but-empty variable counts as unset; both variables are read once per run, and the end-of-run check re-reads only `.specify/feature.json`.

## Assumptions

- The planner's resolution rule is the one in the Spec Kit version Spectra currently tests against
  (project root from `SPECIFY_INIT_DIR` or the nearest `.specify/`; then the feature environment
  variable, then the feature record, then error). If Spec Kit changes it, the test plan follows
  in a later change; this feature does not track upstream automatically.
- The branch name plays no part in resolution, because it plays none in the planner's.
- An explicit path is kept as a confirmation, not removed outright, so existing scripts and habits get a
  clear stop rather than a silently ignored argument.
- Relaxing "never infer" is acceptable because the source is the same one the planner uses and the
  resolution is announced; this is the user's decision and is recorded in the rewritten section's reasoning.
- The change is to the extension only (the agent's command file, manifest, roster, catalog, docs, package,
  and tests); the `spectra` CLI is unaffected.
