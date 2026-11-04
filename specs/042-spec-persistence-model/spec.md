# Feature Specification: Spec Persistence Model in the Methodology Agent

**Feature Branch**: `042-spec-persistence-model`

**Created**: 2026-11-04

**Status**: Implemented

**Input**: User description: "Extend speckit.spectra.methodology so lens 4 (Spec lifecycle & traceability) settles the team's spec persistence model: how a behaviour change to an already-delivered feature is handled, so agents working on tasks know which artifact to change and whether to create a new feature directory. Question 5 takes its own mutually-exclusive shape, like question 9, because the models exclude each other and a 'Full set' would adopt all of them. Options: Living Spec (edit the existing spec.md first, then reconcile or regenerate plan.md and tasks.md, carrying forward rationale that still matters); Flow-Forward (leave completed feature directories untouched and create a new one via /speckit-specify, which states the spec it extends or supersedes); Flow-Back (capture the change in the artifact closest to the work, then bring the others into line); Hybrid with Living Spec as the default (Living Spec within an existing capability, Flow-Forward for a substantial new increment); and Skip. The chosen model is accepted and the others declined. The other lens 4 candidates (layout, numbering, traceability) follow the chosen model unless free text excludes them. In brownfield mode, report current practice from evidence before recommending: spec.md edited after its feature merged suggests Living Spec; new specs/ directories that reference an earlier spec suggest Flow-Forward; plan.md or tasks.md changing while spec.md stays still suggests Flow-Back. Recommend what the evidence shows, and Hybrid when it is mixed or absent. In greenfield mode, recommend Hybrid. Choosing Hybrid adds a persistence column to lens 2's mode-choice table, so the threshold between Living Spec and Flow-Forward is decided per change type (feature, fix, refactor, docs, spike, hotfix), not case by case. Lens 2's question comes before lens 4's, so this column is filled once the model is chosen, without adding a question. The accepted model becomes one constitution guardrail written as per-phase obligations (specify, plan, tasks, implement, converge), not a bare model name, because core spec-kit commands do not read a model name and change their behaviour. Say what each phase does when behaviour changes, including which artifact is updated first when implementation diverges from the spec. Cross-links between specs use the wording 'extends spec NNN' / 'supersedes spec NNN', so they are not confused with lens 9's constitution amendments or with impact's superseded analyses. Record the choice in a new `persistence` front-matter key (living | flow-forward | flow-back | hybrid, absent when question 5 is skipped or not asked) and in a persistence reference section in engineering-methodology-template.md, next to the existing mode-choice and obligations references. Non-interactive mode records it as not_asked and adopts nothing. On a re-run, a prior methodology file without the key treats the model as undecided and asks; a prior answer is offered as the proposed answer. Keep nine lenses and ten questions; nothing is renumbered. Out of scope: changing how other Spectra agents (impact, test-plan, uat, review-pr) read specs under Flow-Forward, and adding any command that edits or reconciles spec artifacts."

## Clarifications

### Session 2026-11-04

- Q: When a team chooses Hybrid, what should the agent propose by default for each change type: keep the
  existing spec, or start a new feature directory? → A: `fix`, `hotfix`, `refactor` → `living`; `feature` →
  `flow-forward`; `docs`, `spike` → `—` where lens 2 says they need no spec. (FR-011)
- Q: Under Flow-Forward, may the old, completed spec get a single added line pointing to the newer spec that
  extends or replaces it? → A: Yes, as part of the model: exactly one added line, "extended by spec NNN" or
  "superseded by spec NNN", and no other edit. (FR-018)
- Q: Under Flow-Back, by what point must `spec.md`, `plan.md`, and `tasks.md` agree again after a change
  was made in just one of them? → A: Before the pull request that carries the change merges. (FR-019)
- Q: How should the four persistence models count against the limit of five candidates per lens? → A: As
  one slot, because they are alternatives for one decision, leaving up to four other lens 4 candidates.
  (FR-006)

## Context

A team using Spec Kit eventually has to change the behaviour of a feature that has already been delivered:
its `specs/NNN-feature/` directory exists, its tasks are done, and its code is merged. Spec Kit deliberately
leaves the next move to the team. Its *Spec Persistence Models* documentation describes three conventions
and asks each team to choose one and record it, preferably in the constitution:

| Model | When behaviour changes | Best fit | Main risk |
|---|---|---|---|
| **Living Spec** | Edit the existing `spec.md` first, then reconcile or regenerate `plan.md` and `tasks.md` from it | The spec is the contract | Losing implementation rationale when derived artifacts are regenerated |
| **Flow-Forward** | Leave the completed directory untouched; create a new one with `/speckit-specify` | Audit trails, traceability, features rarely revisited | Context fragmented across several directories |
| **Flow-Back** | Capture the change in the artifact closest to the work, then bring the others into line | Small teams, fast iteration | Silent drift: `spec.md` stops matching reality |

The table states Spec Kit's descriptions. This feature's Flow-Forward guardrail also allows one added
back-link line in the completed spec (FR-018).

A fourth, **Hybrid**, uses Living Spec by default and Flow-Forward for a substantial new increment. It only
works when the threshold between the two is written down rather than decided case by case.

Nothing in Spec Kit enforces the choice. `/speckit-specify` always creates a new feature directory,
`/speckit-analyze` reports inconsistencies without editing, and `/speckit-converge` only appends tasks. An
AI agent working on tasks therefore learns the team's convention from the constitution or not at all. If no
convention is written down, it will guess: it may create a parallel spec for a one-line rule change, or
silently edit a spec that the team treats as historical record.

`speckit.spectra.methodology` already decides how a team works and hands the decisions to the
constitution. Its lens 4, **Spec lifecycle & traceability**, already settles "how specs stay current". The
persistence model is the core of that question, so this feature puts the decision inside lens 4 instead of
adding a lens.

## Decisions recorded so they are not re-proposed

- **No tenth lens, no eleventh question.** The persistence model belongs to lens 4. A separate lens would
  give two sources for the same constitution clause, and would renumber every question and every count in
  the agent, its template, its listings, and its tests.
- **Question 5 changes shape; its number does not.** The four models exclude each other, so question 5
  uses the mutually-exclusive shape question 9 already uses for the AI autonomy level, not the
  Recommended set / Codify only what exists / Full set / Skip shape.
- **The guardrail is written as phase obligations, not as a model name.** Core spec-kit commands do not
  read a model name and change their behaviour. An agent reading the constitution needs to be told what to
  do at specify, plan, tasks, implement, and converge.
- **Hybrid's threshold lives in lens 2's mode-choice table.** That table already classifies every change by
  type, so adding a column puts the threshold where a reader already looks, without another question.
- **The agent still edits nothing but its own document.** It never touches `specs/`, the constitution, or
  any other file. Existing spec directories are read as evidence only.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Choose a persistence model in question 5 (Priority: P1)

A team lead runs `/speckit-spectra-methodology`. When the round reaches question 5 (Spec lifecycle &
traceability), the agent lists lens 4's candidates, then asks the team to choose one persistence model from
five options: Living Spec, Flow-Forward, Flow-Back, Hybrid (Living Spec by default), and Skip. Each option
says what happens when behaviour changes, what it fits, and its main risk. Exactly one is marked
recommended, with the reason.

**Why this priority**: This is the decision the feature exists for. Without it nothing else in the feature
has anything to record.

**Independent Test**: Run the agent in greenfield mode on an empty project, reach question 5, and confirm
that it offers exactly the five options, marks Hybrid recommended, and records the chosen model as accepted
and the other three as declined.

**Acceptance Scenarios**:

1. **Given** a greenfield project, **When** question 5 is asked, **Then** it is labelled "Question 5 of 10",
   offers the five options in the order Living Spec, Flow-Forward, Flow-Back, Hybrid, Skip, and marks Hybrid
   as recommended.
2. **Given** the team chooses Flow-Forward, **When** the round ends, **Then** the Flow-Forward candidate is
   `accepted`, the Living Spec, Flow-Back, and Hybrid candidates are `declined`, and the other lens 4
   candidates take the same decision as the model unless free text excluded them.
3. **Given** the team answers "Skip", **When** the round ends, **Then** every lens 4 candidate, including all
   four models, is `skipped`, and no persistence guardrail reaches the Constitution input section.
4. **Given** the team replies in free text ("Living Spec, but drop 5.3"), **When** the reply is recorded,
   **Then** Living Spec is accepted, 5.3 is declined, and the remaining lens 4 candidates are accepted.

---

### User Story 2 - The constitution tells an agent what to do when behaviour changes (Priority: P1)

After the run, the team runs the ready-to-paste `/speckit-constitution` command. Later, an AI agent is
asked to change how an already-delivered feature behaves. It reads the constitution and finds a single
persistence guardrail that says, phase by phase, whether to edit the existing spec or create a new feature
directory, how plan and tasks are brought into line, which artifact is updated first if implementation
diverges from the spec, and how converge is run.

**Why this priority**: Recording a model name helps nobody. The value is an agent that acts correctly
without asking, so this is co-equal with the choice itself.

**Independent Test**: For each of the four models, accept it, read only the generated Constitution input
entry, and confirm that the entry answers the five phase questions (specify, plan, tasks, implement,
converge) without referring to the model's name or to any outside document.

**Acceptance Scenarios**:

1. **Given** Living Spec is accepted, **When** the Constitution input section is written, **Then** it holds
   one persistence guardrail stating that a behaviour change to a delivered feature edits that feature's
   `spec.md` first, that `plan.md` and `tasks.md` are reconciled or regenerated from it while carrying
   forward rationale that still applies, that a divergence found during implement updates `spec.md` before
   the code proceeds, and that converge runs against the revised directory.
2. **Given** Flow-Forward is accepted, **When** the guardrail is written, **Then** it states that completed
   feature directories are not edited except for one added back-link line, that the change goes into a new
   directory created by `/speckit-specify`, that the new `spec.md` names the spec it builds on with the
   wording "extends spec NNN" or "supersedes spec NNN", and that the earlier `spec.md` gains the matching
   line "extended by spec NNN" or "superseded by spec NNN".
3. **Given** Flow-Back is accepted, **When** the guardrail is written, **Then** it states which artifact may
   take the change first, and that `spec.md`, `plan.md`, and `tasks.md` must agree again before the pull
   request carrying the change merges.
4. **Given** Hybrid is accepted, **When** the guardrail is written, **Then** it states Living Spec as the
   default, Flow-Forward for the change types the mode-choice table marks `flow-forward`, and the rule that
   decides between them.

---

### User Story 3 - Brownfield evidence drives the recommendation (Priority: P2)

A team brings an existing Spec Kit project onto Spectra. Before question 5, lens 4 reports how the team
handles behaviour changes today, citing the history it found, and the recommended option in question 5
follows that evidence.

**Why this priority**: Every brownfield lens reports current practice before proposing (R1). Recommending a
model that contradicts the team's history would push them to codify something they do not do.

**Independent Test**: Prepare three fixture histories, one per signal, run the agent on each, and confirm
the reported practice, its citations, and the recommended option.

**Acceptance Scenarios**:

1. **Given** a history in which a `spec.md` was edited after its feature merged, **When** lens 4 reports
   current practice, **Then** it cites those commits and recommends Living Spec.
2. **Given** spec directories whose `spec.md` names an earlier spec it extends or supersedes, **When** lens 4
   reports, **Then** it cites those files and recommends Flow-Forward.
3. **Given** commits that change `plan.md` or `tasks.md` of a delivered feature while its `spec.md` does
   not change, **When** lens 4 reports, **Then** it cites those commits and recommends Flow-Back.
4. **Given** signals for more than one model, or none at all, **When** lens 4 reports, **Then** it says
   which signals it found (or that it found none, and where it looked) and recommends Hybrid.

---

### User Story 4 - Hybrid's threshold is decided per change type (Priority: P2)

A team chooses Hybrid. Question 5's Hybrid option already shows the proposed persistence for each change
type. The written methodology's mode-choice table gains a persistence column, so a reader looking up
"fix" sees both whether it needs a spec and whether it edits the existing spec or starts a new one.

**Why this priority**: Without a written threshold, Hybrid collapses into "decide each time", which is the
drift the constitution entry is meant to prevent.

**Independent Test**: Choose Hybrid with and without free-text adjustments, and confirm that the
mode-choice table has a persistence column for all six change types matching the accepted mapping.

**Acceptance Scenarios**:

1. **Given** question 3 has already settled the mode-choice table, **When** question 5 offers Hybrid,
   **Then** the option shows the proposed persistence for each of `feature`, `fix`, `refactor`, `docs`,
   `spike`, and `hotfix`, and choosing it accepts that mapping without a further question.
2. **Given** the team replies "Hybrid, but refactor is flow-forward", **When** the document is written,
   **Then** the column shows `flow-forward` for refactor and the proposed values elsewhere.
3. **Given** any model other than Hybrid is chosen, **When** the document is written, **Then** the
   mode-choice table has no persistence column.

---

### User Story 5 - Re-runs and non-interactive runs stay consistent (Priority: P3)

A team re-runs the agent months later. The model it chose last time is offered as question 5's proposed
answer. A team whose earlier methodology file predates this feature is asked the question as new.

**Why this priority**: Re-run and non-interactive behaviour already have rules in the agent. This story
makes sure the new decision obeys them; it adds no new value on its own.

**Independent Test**: Re-run against a methodology file with `persistence: living`, against one with no
`persistence` key, and with `--non-interactive`, and compare the results with the acceptance scenarios.

**Acceptance Scenarios**:

1. **Given** a prior file with `persistence: hybrid`, **When** question 5 is asked, **Then** it opens with
   "last run you chose Hybrid; still right?", and the prior per-type mapping is the proposed mapping.
2. **Given** a prior file written before this feature, with no `persistence` key, **When** the agent
   re-runs, **Then** the model is undecided and question 5 offers all five options, recommending from the
   evidence.
3. **Given** `--non-interactive`, **When** the document is written, **Then** question 5 is `not_asked`, all
   four model candidates are `not_asked`, the front matter has no `persistence` key, and nothing about
   persistence reaches the Constitution input section.

---

### Edge Cases

- **A brand-new capability.** Under every model, a feature that did not exist before gets a new feature
  directory. The persistence model only decides what happens to a feature that has already been delivered,
  and the guardrail says so, so that no agent reads Living Spec as "never create a directory".
- **The feature in progress.** Every model allows editing the spec of a feature whose work is not yet
  merged. The persistence rules start applying once a feature is delivered, and the guardrail defines
  delivered as merged to the default branch.
- **An existing constitution already states a convention.** When the goal is update and a ratified
  principle already asserts the same model, the matching candidate is suppressed. When a principle asserts
  a different one, the chosen model's candidate is `amends: <Principle>`, following the existing rules for
  an existing constitution.
- **Question 3 was skipped but Hybrid is chosen.** There is no accepted mode-choice table to extend. The
  per-type mapping then appears only in the persistence guardrail statement, where it is always written,
  and the document says why.
- **"Use your defaults" before question 5.** The recommended model and, for Hybrid, the proposed mapping
  are taken and recorded as `default_taken`.
- **A brownfield project with no `specs/` directory.** Lens 4 reports that no spec history was found, and
  where it looked, and recommends Hybrid as in greenfield mode.
- **The five-candidate cap.** Four model candidates plus lens 4's other candidates would exceed the cap of
  five per lens. The four models count as one slot, because they are alternatives for one decision and at
  most one can be accepted, leaving up to four other lens 4 candidates.
- **A prior run declined a model.** A declined model is not offered as a new candidate on a re-run, but it
  remains selectable as an option in question 5, as declined autonomy levels do in question 9. The question
  mentions which models were declined last run.
- **An overlay obligation at the same phase.** TDD's implement obligation and the persistence guardrail's
  implement obligation govern different things: when tests are written versus which artifact changes
  first. They are not reported as a conflict.

## Requirements *(mandatory)*

### Functional Requirements

**The question**

- **FR-001**: Lens 4 MUST settle the team's spec persistence model as part of what it already settles. The
  agent MUST still work nine lenses and ask ten questions, and no question MUST be renumbered.
- **FR-002**: Question 5 MUST list lens 4's other candidates first, numbered within the lens, and then offer
  exactly five labelled options in this order: **Living Spec**, **Flow-Forward**, **Flow-Back**, **Hybrid
  (Living Spec by default)**, **Skip**. Each of the first four MUST state, in one or two lines, what happens
  when behaviour changes, what it fits, and its main risk.
- **FR-003**: Exactly one option MUST be marked recommended, with the evidence or reason behind the mark.
- **FR-004**: The chosen model's candidate MUST be recorded `accepted` and the other three model candidates
  `declined`. Lens 4's other candidates MUST take the same decision as the model unless free text excludes
  them. Skip MUST leave every lens 4 candidate `skipped`.
- **FR-005**: Free text MUST remain a valid answer, including a model choice combined with adjustments to
  other lens 4 candidates or to Hybrid's per-type mapping.
- **FR-006**: The four model candidates MUST count as one slot against the cap of five candidates per lens.

**The recommendation**

- **FR-007**: In brownfield mode, lens 4 MUST report current practice for behaviour changes to delivered
  features before question 5, citing what it found. It MUST read three signals:
  - a `spec.md` changed in a commit after its feature merged (Living Spec);
  - a `spec.md` that names an earlier spec it extends or supersedes (Flow-Forward);
  - a delivered feature's `plan.md` or `tasks.md` changed while its `spec.md` did not (Flow-Back).
- **FR-008**: In brownfield mode, the recommendation MUST be the model whose signal the evidence shows. When
  signals for more than one model appear, or none appear, the recommendation MUST be Hybrid, and the report
  MUST name the signals found or the places searched.
- **FR-009**: In greenfield mode, the recommendation MUST be Hybrid.

**Hybrid's threshold**

- **FR-010**: The Hybrid option MUST show a proposed persistence value for each of the six change types
  (`feature`, `fix`, `refactor`, `docs`, `spike`, `hotfix`). Each value MUST be `living` or `flow-forward`,
  or `—` where the accepted mode-choice table says that change type needs no spec. When question 3 adopted
  no mode-choice table, `—` is not available and such a value becomes `living`. Choosing Hybrid MUST
  accept the mapping as shown, and free text MAY adjust any value. No additional question MUST be asked.
- **FR-011**: The proposed mapping MUST follow the Hybrid rule: a change within an existing capability is
  `living`; a substantial new increment on a delivered feature (a new user journey, a redesign, or a change
  the team would review as its own unit) is `flow-forward`. Unless brownfield evidence points elsewhere,
  the proposed mapping MUST be: `fix`, `hotfix`, and `refactor` → `living`; `feature` → `flow-forward`;
  `docs` and `spike` → `—` where the accepted mode-choice table says they need no spec, and `living`
  otherwise.
- **FR-012**: When Hybrid is accepted, the written mode-choice table MUST gain a persistence column holding
  the accepted mapping. When any other model is accepted, or question 5 is skipped, the table MUST have no
  persistence column.
- **FR-013**: When Hybrid is accepted, the accepted mapping MUST always be written into the persistence
  guardrail statement itself, because the constitution receives the guardrail and not the mode-choice table
  (SC-003). The mode-choice table's persistence column (FR-012) mirrors it. When question 3 adopted no
  mode-choice table, the statement is the only place the mapping appears, and the document MUST say why.

**The guardrail**

- **FR-014**: An accepted model MUST produce exactly one persistence guardrail in the Constitution input
  section, targeting the section lens 4 already feeds (Development Workflow by default, or the project's own
  equivalent).
- **FR-015**: The guardrail statement MUST state the obligation at each of the five phases — specify, plan,
  tasks, implement, converge — for a behaviour change to a delivered feature, and MUST be understandable
  without knowing the model's name.
- **FR-016**: The guardrail MUST state which artifact is updated first when implementation diverges from
  the spec.
- **FR-017**: The guardrail MUST state that a new capability always gets a new feature directory, and that
  the persistence rules apply only once a feature is delivered (merged to the default branch).
- **FR-018**: Under Flow-Forward, and under Hybrid for `flow-forward` changes, the guardrail MUST require the
  new `spec.md` to name the spec it builds on with the exact wording "extends spec NNN" or
  "supersedes spec NNN", and MUST require the earlier `spec.md` to gain exactly one matching line,
  "extended by spec NNN" or "superseded by spec NNN". That line MUST be the only edit the guardrail allows
  to a completed feature directory.
- **FR-019**: Under Flow-Back, the guardrail MUST state that `spec.md`, `plan.md`, and `tasks.md` agree
  again before the pull request that carries the change merges.
- **FR-020**: The candidate record and the Constitution input entry MUST keep the format the agent already
  uses: a frozen, content-derived ID in lens 4's namespace, a basis of `observed` or `aspirational`, a
  decision, and a status, including suppression or `amends:` against an existing constitution.

**The written document**

- **FR-021**: The document's front matter MUST carry a `persistence` key whose value is `living`,
  `flow-forward`, `flow-back`, or `hybrid`, and MUST omit the key when question 5 was skipped or not asked.
- **FR-022**: `engineering-methodology-template.md` MUST include a persistence reference in the Spec
  lifecycle & traceability section, and the agent MUST always write it when a model is accepted. It MUST
  name the accepted model and show its five phase obligations as a short table, next to the existing
  mode-choice, branch-naming, commit-prefix, and obligations references. With no model accepted, it MUST
  be one sentence saying no persistence model was chosen.
- **FR-023**: The Decisions and sources section MUST carry question 5 like every other question: the
  question, the recommended option and its evidence, the answer taken, and its disposition.

**Re-runs and non-interactive runs**

- **FR-024**: On a re-run, a prior `persistence` value MUST be offered as question 5's proposed answer, and a
  prior Hybrid mapping as the proposed mapping.
- **FR-025**: A prior document with no `persistence` key MUST be treated as undecided: question 5 is asked
  with all five options and recommends from the evidence.
- **FR-026**: A declined model MUST NOT be offered as a new candidate on a re-run, but MUST remain selectable
  as an option, and question 5 MUST say which models were declined last run.
- **FR-027**: In non-interactive mode, question 5 and all four model candidates MUST be `not_asked`, the
  `persistence` key MUST be absent, and nothing about persistence MUST reach the Constitution input
  section.

**Boundaries and shipping**

- **FR-028**: The agent MUST NOT modify any file under `specs/`, the constitution, or any file other than its
  own methodology document.
- **FR-029**: The cross-link wording of FR-018 MUST always name a spec ("… spec NNN"), so it cannot be read
  as lens 9's "superseding" of constitution principles or as `speckit.spectra.impact`'s superseded
  analyses.
- **FR-030**: The change MUST land as one Principle V change: the agent's source in `agents/methodology.md`,
  the command, the template, regenerated listings, the extension's version bump and changelog entry, the
  catalog entry, the rebuilt package, and tests that cover the new behaviour.

### Key Entities

- **Persistence model**: The team's convention for a behaviour change to a delivered feature. One of Living
  Spec, Flow-Forward, Flow-Back, or Hybrid. Recorded as one lens 4 candidate per model, of which at most one
  is accepted.
- **Persistence guardrail**: The accepted model's candidate, written as five phase obligations. It is what
  reaches the constitution.
- **Persistence mapping**: Hybrid only. Change type → `living`, `flow-forward`, or `—`. Always written
  inside the guardrail statement, and mirrored as a column of the mode-choice table when one was adopted.
- **`persistence` front-matter key**: The machine-readable record of the accepted model, read by later runs.
- **Spec cross-link**: A pair of lines: one in the new `spec.md` naming the earlier spec it extends or
  supersedes, and one back-link added to the earlier `spec.md` naming the new one.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In 100% of interactive runs, the round still holds exactly ten questions, numbered "of 10",
  and question 5 offers exactly five options with exactly one recommended.
- **SC-002**: In 100% of runs that accept a model, the Constitution input section holds exactly one
  persistence guardrail, and it states an obligation for all five phases.
- **SC-003**: Given only the constitution entry, a reader can answer "edit the existing spec, or create a new
  feature directory?" for each of the six change types, for all four models, with no reference to any other
  document: 24 of 24 combinations answerable.
- **SC-004**: For each of the three brownfield fixture histories (one signal each), the recommended option
  matches the signal in 3 of 3 cases; for a mixed or empty history, Hybrid is recommended.
- **SC-005**: In non-interactive runs and skipped question 5 runs, zero persistence guardrails reach the
  Constitution input section and the `persistence` key is absent.
- **SC-006**: On a re-run, zero declined models are offered as new candidates, and the previously chosen
  model is the proposed answer in 100% of re-runs where one was recorded.
- **SC-007**: The repository's generator check and test suite pass with the change, and no file outside the
  methodology agent's command, source, template, generated listings, release metadata, package, and tests
  changes.

## Assumptions

- **Hybrid's proposed per-type mapping** is settled in FR-011. Two readings behind it: a `refactor` is
  `living` because a behaviour-preserving change leaves the spec as it is, and a `hotfix` is `living` with
  the spec reconciled after the fix ships, as the guardrail's implement obligation states. The team adjusts
  any value in free text.
- **"Delivered" means merged to the default branch.** This is the moment a feature's directory stops being
  a work area under Flow-Forward, and the moment from which brownfield signals count edits as "after
  merge".
- **Spec Kit version.** The obligations name `/speckit-converge`; projects on a Spec Kit release without it
  still get a valid guardrail for the other four phases. The extension's existing `requires.speckit_version`
  already covers converge.
- **This repository.** Spectra's own `specs/` history follows Flow-Forward. This feature changes what the
  agent offers other teams; it does not change Spectra's constitution.
- **Out of scope.** How `speckit.spectra.impact`, `test-plan`, `uat`, and `review-pr` read specs under
  Flow-Forward (for example, following "supersedes spec NNN" chains to find current behaviour), and any
  command that edits or reconciles spec artifacts.
