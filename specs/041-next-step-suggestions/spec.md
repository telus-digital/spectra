# Feature Specification: Consistent Next-Step Suggestions Across the SDLC

**Feature Branch**: `041-next-step-suggestions`

**Created**: 2026-10-28

**Status**: Implemented

**Input**: User description: "Make SPECTRA's 'what's next' suggestions consistent across the SDLC. Hooks cover what follows a core Spec Kit command. A closing suggestion, written into the agent's own final report, covers what follows a SPECTRA agent. Every suggestion is an offer only: nothing runs on its own, and the user always decides and acts. Part 1 — hooks in spectra/extension.yml: after_specify → test-plan (unchanged); after_clarify → test-plan (new); after_implement → converge, uat, create-pr in that order (converge new); after_converge → uat (new), with a prompt true whether or not converge appended tasks, made safe by the UAT agent's existing implementation-incomplete check. No hook is mandatory; after_specify → clarify is deliberately not added; hooks on core commands are a known undocumented dependency; requires.speckit_version rises to the first release that ships converge; the YAML comment is corrected to say list order, not priority, controls what users see. Part 2 — closing suggestions: defect-rca → specify (new, skipped when no root cause was identified); impact → specify (new, only on a 'go'); flaky-test-detector → specify (new, only for fixes declined or too large to apply); adr, brd and the four strategy agents unchanged; kb-vault keeps routing policy documents to their owning agents. Every Principle V change lands in one change, with a minor extension bump; the CLI is not touched. Out of scope: agents reading extensions.yml or emitting their own hook events, hooks on other core commands, mandatory hooks, changing what agents produce beyond their closing suggestion."

## Clarifications

### Session 2026-10-29

- Q: Impact never decides go / no-go — every run writes `status: draft` and stakeholders decide afterwards —
  so what is its closing suggestion? → A: A conditional pointer on every run: the decision is the
  stakeholders'; if they approve, the next step is `/speckit-specify`, with a ready-to-paste prompt citing
  the analysis (User Story 6, FR-016).
- Q: What exact prompt should the hook show after converge? → A: "Run UAT now? If converge just added tasks,
  finish them with implement first — UAT will tell you if any are still open." (FR-007)
- Q: Should the three new closing suggestions share one layout or follow each agent's style? → A: One shared
  layout for defect-rca, impact, and flaky-test-detector; the six existing hand-offs are not reshaped.
  (FR-011)

## Context

A SPECTRA user moves through the SDLC one command at a time, and at the end of each command they need to
know what sensibly comes next. Two mechanisms can tell them, and today they are used unevenly.

**Hooks.** Every core Spec Kit command (`specify`, `clarify`, `implement`, `converge`, …) ends by reading
`.specify/extensions.yml` and showing the entries registered under `hooks.after_<command>`. An optional
entry is shown as a prompt with the command to run; it never runs on its own. SPECTRA registers its hooks in
the `hooks:` section of `spectra/extension.yml`. Today it registers two events: `after_specify` offers the
test plan, and `after_implement` offers UAT and then a pull request. A hook's prompt is fixed text written
when the manifest was authored: it cannot react to how the run went, because Spec Kit's command templates
skip any hook that carries a `condition`.

**Closing suggestions.** SPECTRA's own agents do not read `extensions.yml`, so no hook can fire after them.
Instead, six of them (`adr`, `brd`, `domain-analyzer`, `methodology`, `test-strategy`,
`deployment-strategy`) already end with a written next step — often a ready-to-paste prompt built from what
the run found. That is strictly more useful than a hook could be, because the agent knows the outcome.

The gaps are:

- After `clarify`, nothing offers to build or refresh the test plan from the hardened spec.
- After `implement`, nothing offers `converge`, so unbuilt work can reach UAT and a pull request unnoticed.
- After `converge` reports nothing left to build, core Spec Kit points the user to review or a PR, and
  nothing offers UAT — so the UAT step the project relies on can be skipped silently.
- `defect-rca`, `impact`, and `flaky-test-detector` end without pointing at `specify`, though each can
  produce work that belongs in a spec.
- The comment above `after_implement` in `spectra/extension.yml` says Spec Kit sorts hooks by `priority`.
  Per the Spec Kit extension reference, command templates show hooks in YAML list order and do not sort, so
  the comment misdescribes what users see.

This feature closes those gaps with the rule "hooks after core commands, closing suggestions after SPECTRA
agents", and keeps every suggestion an offer.

## Decisions recorded so they are not re-proposed

- **No `after_specify` → `clarify` hook.** Core `specify` already names `/speckit-clarify` as a next step in
  its completion report; a hook would repeat it.
- **No hooks after SPECTRA agents.** Making SPECTRA agents read `extensions.yml` or emit their own events
  (an `after_spectra_<id>` event) was considered and rejected: a fixed hook prompt would duplicate, more
  weakly, the closing suggestion the agent already writes from its run's outcome.
- **`kb-vault` does not suggest `/speckit-constitution`.** It keeps routing each policy document to the
  agent that owns that ground, so no constitution clause gets two sources.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - After implement, converge is offered before UAT and a PR (Priority: P1)

A developer finishes `/speckit-implement`. Before they test or open a pull request, they are offered a
check for work the spec, plan, and tasks call for that is still unbuilt — then UAT, then a pull request, in
that order.

**Why this priority**: Unbuilt work reaching UAT or review is the most expensive gap this feature closes,
and `after_implement` is the hook every feature passes through.

**Independent Test**: Install the extension into a Spec Kit project, complete an implement run, and read the
hooks block it shows.

**Acceptance Scenarios**:

1. **Given** SPECTRA is installed, **When** `implement` completes, **Then** the hooks block offers
   `converge`, then `uat`, then `create-pr`, in that order, each as an optional offer.
2. **Given** the same project, **When** the user does not invoke any of them, **Then** none of them runs.

---

### User Story 2 - After converge, UAT is offered before a PR (Priority: P1)

A developer runs `/speckit-converge`. Whether it found nothing left or appended new tasks, they are offered
UAT before a pull request. If they accept it while appended tasks are still open, the UAT agent warns them
before anything is started.

**Why this priority**: Without it, a converged feature is pointed straight at a PR and UAT is skipped.

**Independent Test**: Run converge once on a finished feature and once on a feature with gaps; check the
offer in both, then run UAT immediately after the second.

**Acceptance Scenarios**:

1. **Given** converge reports that nothing remains, **When** it completes, **Then** UAT is offered, and the
   prompt reads correctly for that outcome.
2. **Given** converge appended tasks, **When** it completes, **Then** UAT is offered with a prompt that tells
   the user to finish appended tasks with implement first, and converge's own next step (implement) is
   unchanged.
3. **Given** converge just appended tasks and they are unchecked, **When** the user runs UAT anyway,
   **Then** the UAT agent reports that implementation is incomplete, gives the count of unchecked tasks
   outside the UAT phase, and asks before going on.

---

### User Story 3 - After clarify, the test plan is offered (Priority: P2)

A developer clarifies a spec. They are offered a test plan built from the clarified spec, for the feature
the clarify run worked on, with no path to type.

**Why this priority**: Clarification changes acceptance criteria; a test plan built before it is stale.

**Independent Test**: Run clarify on a feature and read the hooks block.

**Acceptance Scenarios**:

1. **Given** SPECTRA is installed, **When** `clarify` completes, **Then** the test plan is offered as an
   optional hook whose prompt says no path is needed.
2. **Given** a test plan already exists for that feature, **When** the user accepts the offer, **Then** the
   test-plan agent handles the existing plan exactly as it does today.

---

### User Story 4 - After a root cause analysis, specifying the fix is offered (Priority: P2)

A developer finishes `/speckit-spectra-defect-rca` with a validated cause. The report ends by offering
`/speckit-specify` with a ready-to-paste prompt that cites the RCA document and its root cause.

**Why this priority**: An advisory RCA that names a cause is the natural input to a fix spec, and today the
user has to compose that prompt by hand.

**Independent Test**: Run defect-rca to a validated cause, and separately to no validated cause; read the
final report of each.

**Acceptance Scenarios**:

1. **Given** the analysis validated a root cause, **When** the document is written, **Then** the report
   offers `/speckit-specify` with a ready-to-paste prompt citing the document's path and the cause.
2. **Given** the deepest validated finding is only the immediate technical cause, **When** the offer is made,
   **Then** the prompt says so rather than presenting it as the systemic root cause.
3. **Given** no cause was validated, **When** the run ends, **Then** no specify offer is made and the report
   says why.

---

### User Story 5 - After flaky-test detection, specifying unapplied fixes is offered (Priority: P3)

A developer runs `/speckit-spectra-flaky-test-detector`, and some fixes are not applied — they declined to
have them worked, or the agent could not apply them within its scope. The report offers `/speckit-specify`
for exactly those, with a ready-to-paste prompt listing each test and its proposed fix.

**Why this priority**: Useful but narrower: most flaky-test fixes are applied by the agent itself.

**Independent Test**: Run the agent through Gate 2 with one row whose remedy lies in production code, and
separately with every fix applied; read both reports.

**Acceptance Scenarios**:

1. **Given** a row was left open because its remedy is in production code, a guardrail forbids the remedy,
   or the agent was not confident in the fix, **When** the run reports, **Then** it offers
   `/speckit-specify` listing those rows' tests and proposed fixes.
2. **Given** the developer declined Gate 2, **When** the run ends, **Then** the offer lists every row still
   open in the written analysis.
3. **Given** every fix was applied, or nothing was proposed, **When** the run ends, **Then** no offer is made
   and the report says why.

---

### User Story 6 - After an impact analysis, the path to a spec is named (Priority: P3)

A BA finishes `/speckit-spectra-impact`. The analysis is a draft for stakeholders, who make the go / no-go
decision outside the session.

Because impact never decides go / no-go — every run writes `status: draft`, and the stakeholders' answer
is recorded by hand afterwards — its closing suggestion is a conditional pointer: the decision is the
stakeholders', and if they approve, the next step is `/speckit-specify`, with a ready-to-paste prompt citing
the analysis.

**Why this priority**: The decision belongs to stakeholders; the suggestion only shortens the path once
they have made it.

**Independent Test**: Run impact and read the final report.

**Acceptance Scenarios**:

1. **Given** an analysis is written, **When** the report ends, **Then** it says the decision belongs to the
   stakeholders, makes no claim about what they will decide, and says that if they approve, the next step is
   `/speckit-specify`, with a ready-to-paste prompt citing the analysis's path.
2. **Given** any impact run, **When** it completes, **Then** nothing is written under `specs/` and the
   analysis records no spec reference.

---

### Edge Cases

- **Another extension hooks the same event** (for example the git extension's `after_implement` commit):
  SPECTRA controls only the order of its own entries; their position relative to another extension's is
  Spec Kit's to decide.
- **A user disables one SPECTRA hook by hand** (`enabled: false` in `.specify/extensions.yml`): it is
  skipped. A later extension update re-registers SPECTRA's hooks as enabled; that is Spec Kit behaviour and
  is stated, not changed, by this feature.
- **The project runs a Spec Kit older than the first release with `converge`**: the raised minimum version
  stops the extension being installed there, rather than registering a hook for a command that does not
  exist.
- **Clarify is run several times**: the test plan is offered after each run; the test-plan agent's existing
  behaviour toward an existing plan applies.
- **defect-rca in exploration mode** writes nothing, so it makes no specify offer. **In non-interactive
  mode** the offer is still printed; it runs nothing.
- **flaky-test-detector declined at Gate 1** writes nothing, so it makes no offer. **Rows the developer
  deleted** in review are not offered: deleting a row means they chose not to fix it. **Rows left open
  because the test can no longer be found or its evidence has gone** are not offered: there is nothing
  sound to specify.
- **A Spec Kit release stops honouring hooks that target core commands**: the `after_implement` →
  `converge` offer would stop appearing; no other SPECTRA behaviour depends on it.

## Requirements *(mandatory)*

### Functional Requirements

**Hooks**

- **FR-001**: The `hooks:` section of `spectra/extension.yml` MUST contain exactly these entries, and no
  others:
  1. `after_specify` → `speckit.spectra.test-plan` (unchanged);
  2. `after_clarify` → `speckit.spectra.test-plan`;
  3. `after_implement` → `speckit.converge`, `speckit.spectra.uat`, `speckit.spectra.create-pr`, in that
     list order;
  4. `after_converge` → `speckit.spectra.uat`.
- **FR-002**: Every SPECTRA hook MUST be `optional: true` and MUST carry no `condition`.
- **FR-003**: The order users see MUST come from each event's list order. Each entry's `priority` MUST agree
  with that order but MUST NOT be what produces it.
- **FR-004**: The comment above `after_implement` MUST state that list order, not `priority`, controls the
  order users see.
- **FR-005**: The `after_clarify` prompt MUST offer to build or refresh the test plan from the clarified
  spec and MUST say that no path is needed, because the test plan resolves the feature itself.
- **FR-006**: The `after_implement` → `converge` prompt MUST offer to check the codebase against the spec,
  plan, and tasks for work that is still unbuilt.
- **FR-007**: The `after_converge` → `uat` prompt MUST read correctly whether converge appended tasks or
  found nothing remaining. It MUST read exactly: "Run UAT now? If converge just added tasks, finish them
  with implement first — UAT will tell you if any are still open."
- **FR-008**: The UAT agent's existing implementation-incomplete check (it counts unchecked tasks outside the
  UAT phase, reports the count, and asks before going on) MUST be kept unchanged.
- **FR-009**: `requires.speckit_version` MUST be raised to the first Spec Kit release that ships the
  `converge` command and its `after_converge` event. If planning cannot establish that release, it MUST be
  recorded as an open question, never guessed.
- **FR-010**: The dependency on Spec Kit honouring a hook that targets a core command (`speckit.converge`),
  which works in current Spec Kit but is not described in its extension reference, MUST be recorded where
  maintainers will find it — beside the hook in `spectra/extension.yml` and in the changelog entry.

**Closing suggestions**

- **FR-011**: Every closing suggestion this feature adds MUST be part of the agent's final report and MUST
  run nothing. The three agents MUST use one shared layout: a "Next step" label, the command, one line on
  why, and the ready-to-paste prompt in a code block — or, where no offer is made, the label followed by the
  one-line reason. The command MUST be named as Spec Kit's specify command and rendered in the running
  agent's own invocation syntax, never hard-coded in one agent's form (Principle III). The six existing
  hand-offs (FR-018) are not reshaped to match.
- **FR-012**: `defect-rca` MUST, after writing a document whose analysis validated a cause, offer
  `/speckit-specify` with a ready-to-paste prompt citing the document's path and the validated cause. Where
  the deepest validated finding is the immediate technical cause rather than a deeper layer, the prompt
  MUST say so.
- **FR-013**: `defect-rca` MUST make no specify offer, and MUST say why, when no cause was validated. It MUST
  make none in exploration mode, which writes nothing.
- **FR-014**: `flaky-test-detector` MUST offer `/speckit-specify` only for rows left open because the remedy
  is in production code, a guardrail forbids the remedy, or the agent was not confident in the fix — and,
  when the developer declined Gate 2, for every row still open. The prompt MUST list each such row's test
  and proposed fix.
- **FR-015**: `flaky-test-detector` MUST make no specify offer, and MUST say why, when every fix was applied
  or nothing was proposed. When Gate 1 is declined it MUST print no closing block, because nothing was
  written and the agent already says so. Rows the developer deleted and rows whose test or evidence is gone
  MUST NOT be offered.
- **FR-016**: `impact` MUST end its report by saying the go / no-go decision belongs to the stakeholders, and
  MUST NOT state, set, or infer that decision. It MUST then say that, if the stakeholders approve, the next
  step is `/speckit-specify`, with a ready-to-paste prompt citing the analysis's path. The pointer is
  conditional in wording and appears on every run that writes an analysis, whatever its impact rating.
- **FR-017**: `impact` MUST continue to write nothing under `specs/` and to record no spec reference; a
  suggestion is a pointer only.
- **FR-018**: The closing hand-offs of `adr`, `brd`, `domain-analyzer`, `methodology`, `test-strategy`, and
  `deployment-strategy` MUST be unchanged. `adr` MUST still offer `/speckit-constitution` only when the
  decision changes the constitution.
- **FR-019**: `kb-vault` MUST keep routing each policy document to the agent that owns it and MUST NOT
  suggest `/speckit-constitution` directly.

**Across the change**

- **FR-020**: No agent or hook added or changed by this feature MAY invoke another agent or command; every
  next step waits for the user.
- **FR-021**: Wherever an agent's description or SPECTRA's documentation says which hook offers an agent —
  including the test-plan and uat descriptions in `agents/`, and the Getting Started walkthrough — it MUST
  be updated to match. Generated listings MUST be changed only by editing `agents/` and regenerating.
- **FR-022**: The change MUST land as one change with every Principle V artifact in sync: the affected
  `agents/<id>.md`, `spectra/commands/<id>.md`, `spectra/extension.yml` with a minor version bump,
  `spectra/CHANGELOG.md`, `catalog.json`, and `docs/packages/spectra.zip`, with the generated outputs
  regenerated and the generator's check passing.
- **FR-023**: The `spectra` CLI (`spectra_cli/` and the root `VERSION`) MUST NOT be touched or bumped.

### Key Entities

- **Hook entry**: one optional offer registered under an `after_<command>` event — target command, prompt,
  description, priority, list position. Fixed when the manifest is written.
- **Closing suggestion**: the next-step block at the end of a SPECTRA agent's report — next command, reason,
  ready-to-paste prompt — written from that run's outcome; where the outcome does not warrant an offer, the
  block states the reason instead. For the three agents this feature changes, it has one shared layout
  (FR-011).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After each of `specify`, `clarify`, `implement`, and `converge`, the user sees exactly the
  SPECTRA offers listed in FR-001 for that command, in that order — 4 events, 6 offers — and zero of them
  run without the user invoking them.
- **SC-002**: In 100% of converge runs, UAT is offered before a PR is suggested by any SPECTRA hook; in 100%
  of UAT runs started while non-UAT tasks are unchecked, the user is told the count and asked before
  anything starts.
- **SC-003**: Each of `defect-rca` and `flaky-test-detector` makes its specify offer in every run that meets
  its condition and in no run that does not. Every run that finished its work without an offer states why;
  runs that wrote nothing (defect-rca exploration mode, a flaky-test-detector Gate 1 decline, an impact run
  that wrote no analysis) print no closing block. `impact` ends every
  run that writes an analysis with the conditional pointer, and no run states or implies a go / no-go.
- **SC-004**: A user accepting a specify offer from `defect-rca`, `flaky-test-detector`, or `impact` can paste the given
  prompt unchanged and start `/speckit-specify` with no further composition.
- **SC-005**: The final reports of `adr`, `brd`, `domain-analyzer`, `methodology`, `test-strategy`,
  `deployment-strategy`, and `kb-vault` are unchanged by this feature.
- **SC-006**: No published description or page states a hook arrangement other than the one in FR-001, and
  the generated-docs check and the test suite pass.

## Assumptions

- **"Declined" in flaky-test-detector** means the developer declined Gate 2, or a row the agent left open
  for a reason a spec could act on (remedy in production code, a guardrail, low confidence). Rows the
  developer deleted are a choice not to fix and are not offered.
- **A defect-rca "root cause identified"** means at least one hypothesis reached `validated`. A run whose
  deepest validated finding is the immediate technical cause still offers specify, labelled as such, since a
  fix for that cause is legitimate work.
- **The test-plan agent already resolves the feature** after clarify the same way it does after specify
  (`SPECIFY_FEATURE_DIRECTORY`, then `.specify/feature.json`), so the `after_clarify` offer needs no path.
- **Raising `requires.speckit_version`** is acceptable: users on an older Spec Kit are already unable to run
  `converge`, and the after-converge offer is meaningless without it.
- **Hook order across extensions**, and the re-enabling of hand-disabled hooks on update, are Spec Kit
  behaviour outside SPECTRA's control and are not changed here.
- **Dependency**: Spec Kit continues to show an extension's hook that targets a core command, as it does in
  the current release.
