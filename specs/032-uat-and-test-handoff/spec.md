# Feature Specification: UAT and Regression Lenses, a Tighter Test Handoff, and a UAT Runner

**Feature Branch**: `032-uat-and-test-handoff`

**Created**: 2026-10-15

**Status**: Implemented

**Input**: User description: "Tighten the test-strategy → test-plan handoff, add UAT and Regression
lenses, and add a speckit.spectra.uat command, so the SDD flow becomes /specify → /test-plan → /plan →
/tasks → /implement → (optional) UAT. […] New lenses in test-strategy […] test-plan consistency with the
strategy […] New test-plan sections: Suggested UAT scenarios and Regression scope […] Handoff fixes so
the plan uses more of the strategy than lens names and floor […] Workflow wiring without editing core
commands: an optional after_specify hook offering test-plan, and a /plan prompt that records the test
plan's obligations in plan.md […] New command speckit.spectra.uat: run only on explicit human request
after implementation […] Ship per Principle V." (full text in the session that produced this spec; every
decision in it is carried into the requirements below)

## Clarifications

### Session 2026-10-15

The decisions below were settled with the maintainer before this spec was written. They are recorded so
a later reader can tell a choice from an omission.

- Q: When a human wants the AI agent to perform UAT, what do they invoke? → A: **A new command,
  `speckit.spectra.uat`**, rather than a plain-language request. A command is where the rules that make
  agent-run UAT trustworthy can live — evidence capture, and never marking a pass that was not observed.
  A plain request would carry none of them.

- Q: What lens set does the test plan use when the project has no test strategy? → A: **The full default
  set, flagged loudly**: `unit`, `integration`, `api-contract`, `end-to-end`, `uat`, `regression`, plus
  `manual`. The plan states that no strategy exists and recommends running test-strategy. Requiring a
  strategy would block the specify → test-plan flow on any project that skipped the foundation phase.

- Q: What happens to the always-available `manual` level once UAT exists? → A: **It stays, as its own
  level**, distinct from UAT. `manual` is for a one-off human check of a single condition (a visual check,
  a third-party sandbox call). A UAT scenario is a stakeholder-facing journey judged in the user's own
  terms. They answer different questions, so neither absorbs the other.

- Q: How does the test plan reach the tasks without editing a core command? → A: **Through `plan.md`.**
  The core tasks command reads `plan.md`, `spec.md`, and the constitution, but never `test-plan.md`. The
  test plan's handoff tells the planning command to record the plan's obligations in `plan.md`, so the
  tasks command sees them. The project constitution, which the tasks and implement commands both read,
  carries the rule that keeps UAT tasks out of implementation.

- Q: How is test-plan suggested after specify? → A: **An optional `after_specify` hook**, the same
  mechanism Spectra already uses to offer `create-pr` after implement. This reverses test-plan's earlier
  "not a hook" decision. Being optional, it only *asks*. It never runs test-plan on its own.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A test plan that carries UAT scenarios and a regression scope (Priority: P1)

A developer has just written a specification and runs test-plan against it. Next to the existing test
conditions, the plan now has a **Suggested UAT scenarios** section and a **Regression scope** section.

- **UAT scenarios** come from the spec's own user stories and acceptance scenarios, and each one is
  traced to a spec identifier. Each names who can execute it — the agent, a human, or either — and says
  "agent" only where the agent can actually drive the project's surface.
- **Regression scope** lists the existing tests that touch what the feature changes and must stay
  green, each cited by file.

A stakeholder reading the plan can see how the feature will be accepted, and what must not break, before
anyone designs the implementation.

**Why this priority**: Everything downstream — the tasks, the deferred UAT phase, the UAT runner — starts
from these two sections. Without them there is nothing to hand on.

**Independent Test**: Run test-plan against a specification with prioritized user stories, in a project
with a test strategy that marks UAT and regression applicable and has existing tests. Confirm that every
UAT scenario cites a spec identifier and names an executor, that every regression entry cites a test
file, and that the document contains no checkbox.

**Acceptance Scenarios**:

1. **Given** a spec with three user stories and a strategy marking UAT applicable, **When** test-plan
   runs, **Then** the plan has a Suggested UAT scenarios section whose scenarios each cite a story or
   acceptance-scenario identifier and name an executor of `agent`, `human`, or `either`.
2. **Given** a project whose manifests show no surface the agent can drive (for example, a desktop GUI
   with no automation tooling), **When** test-plan derives UAT scenarios, **Then** none is marked
   executable by the agent, and the plan states why.
3. **Given** existing tests that import modules the feature touches, **When** test-plan runs, **Then** the
   Regression scope lists those tests by file path, and any risk-driven additions are named as such.
4. **Given** no existing test touches the feature's modules, **When** test-plan runs, **Then** the
   Regression scope states the search it ran and where, rather than an unqualified "none".

---

### User Story 2 - The test plan's obligations become tasks, and implement leaves UAT open (Priority: P1)

After test-plan finishes, the developer gets a ready-to-paste prompt for the planning command. The prompt
links the new `test-plan.md` and tells the planning command to record the plan's testing obligations in
`plan.md`. The tasks command then produces:

- test tasks at the levels the plan names, each written before the implementation it covers;
- a task that keeps the regression scope green;
- a final, labelled **UAT phase** whose tasks are marked as not executed by the implement command.

The developer runs implement. It finishes every task except the UAT ones, and reports that
implementation is done with UAT outstanding.

**Why this priority**: This is the user's core workflow. A UAT section that never becomes tasks — or UAT
tasks that implement quietly ticks off — defeats the feature.

**Independent Test**: Take a project whose constitution carries the UAT clause from User Story 3. Follow
the printed prompt through planning and tasks, then run implement. Confirm that `tasks.md` contains test
tasks matching the plan's P1 conditions and a labelled UAT phase, and that after implement every UAT task
is still unchecked.

**Acceptance Scenarios**:

1. **Given** test-plan has just written `specs/NNN-x/test-plan.md`, **When** it reports, **Then** it
   prints a ready-to-paste planning prompt that links that exact file. The prompt also states every
   obligation: P1 conditions map to tests written before their implementation, levels are followed as
   assigned, the regression scope stays green, and UAT scenarios become a final, labelled UAT phase not
   executed by implement.
2. **Given** the planning command ran with that prompt, **When** `plan.md` is read, **Then** it names the
   test plan's path and records those obligations, so a tasks command that reads only `plan.md`, the spec,
   and the constitution can act on them.
3. **Given** a `tasks.md` with a labelled UAT phase and a project constitution carrying the UAT clause,
   **When** implement completes, **Then** every UAT task is still unchecked and the completion report
   names the outstanding UAT tasks.

---

### User Story 3 - The test strategy decides UAT and regression policy (Priority: P2)

A team running test-strategy now gets six lenses instead of four. **UAT** is marked applicable or not,
with a stated executor policy and the evidence each surface needs. **Regression** names which suite is
the regression gate, where it runs, and whether a fixed defect earns a regression test. The drafted
constitution amendment gains a clause: UAT tasks are never executed or marked complete by implement, and
run only on explicit request.

**Why this priority**: The strategy is what makes the plan's lens set consistent across features. The
clause it drafts is what makes User Story 2's "implement leaves UAT open" binding rather than a hint.

**Independent Test**: Run test-strategy on a project with a browser surface and an existing CI suite.
Confirm that the document has UAT and Regression lens sections with an applicability verdict, an executor
policy, and per-surface evidence, and that the drafted amendment contains the UAT clause.

**Acceptance Scenarios**:

1. **Given** a CLI project, **When** test-strategy runs, **Then** the UAT lens names terminal-transcript
   evidence and no screenshot evidence, and the strategy names no browser tool.
2. **Given** a published library with no user-facing entry point, **When** test-strategy runs, **Then** UAT
   is either marked not applicable with a reason, or scoped to a developer-facing journey, and either way
   the reason is stated.
3. **Given** a CI workflow that runs the suite on push, **When** test-strategy runs, **Then** the Regression
   lens cites that workflow as the regression gate.
4. **Given** a constitution with no UAT rule, **When** the amendment is drafted, **Then** it includes the
   clause that UAT tasks are never executed or marked complete by implement and run only on explicit
   request.

---

### User Story 4 - The agent performs UAT on explicit request (Priority: P2)

Implementation is done and UAT is open. The human runs `speckit.spectra.uat` — or answers yes to its
optional after-implement offer. The command:

- reads the UAT phase in `tasks.md` and the matching scenarios in the test plan;
- performs the scenarios the agent can drive, against the project's real build;
- saves evidence — screenshots, terminal transcripts, before-and-after comparisons — under the feature's
  directory;
- marks a UAT task complete only when it observed the scenario pass, with the evidence linked.

Scenarios marked human-only, and any that failed, are left open with a report. A human may instead
perform UAT by hand and tick the tasks themself.

**Why this priority**: This is what lets the human choose between AI-run and manual UAT. It depends on
User Stories 1 and 2 existing first.

**Independent Test**: With a `tasks.md` whose UAT phase has one agent-drivable scenario that passes, one
that fails, and one marked human-only, run the uat command. Confirm that only the passing one is ticked,
with evidence linked, and that the other two are open with reasons in the report.

**Acceptance Scenarios**:

1. **Given** a passing agent-drivable scenario, **When** uat runs, **Then** its task is marked complete
   and links evidence saved under the feature's directory.
2. **Given** a scenario that fails, **When** uat runs, **Then** its task stays unchecked, the report names
   the failure with its evidence, and no source, test, or specification file is changed.
3. **Given** a scenario marked `human`, **When** uat runs, **Then** it is not attempted and is listed as
   awaiting a human.
4. **Given** uat was not explicitly invoked, **When** implement finishes, **Then** no UAT scenario is
   performed. The optional hook only asks.
5. **Given** implementation tasks are still unchecked, **When** uat is invoked, **Then** it reports that
   implementation is incomplete and asks before going on.

---

### User Story 5 - test-plan is offered right after specify (Priority: P2)

A developer finishes specify. Among the after-specify hooks they see an offer to generate a test plan for
the spec just written, and the offer tells the agent to pass the spec path that was just reported. Saying
yes runs test-plan against that spec. Saying no changes nothing.

**Why this priority**: It puts test-plan into the SDD flow at the moment it is most useful, without
changing a core command.

**Independent Test**: Install the updated extension into a throwaway project and run specify. Confirm that
the hook output offers test-plan with an instruction to pass the spec path, and that accepting it runs
test-plan with that path.

**Acceptance Scenarios**:

1. **Given** the extension is installed, **When** specify completes, **Then** an optional test-plan hook
   is listed whose prompt says to pass the spec file just reported.
2. **Given** the hook is accepted but somehow invoked with no path, **When** test-plan starts, **Then** it
   still stops and asks for a path. It never infers the spec from session history, the branch, or
   `feature.json`.

---

### User Story 6 - The test plan honours the whole strategy, not just its vocabulary (Priority: P3)

When a strategy exists, the test plan follows more of it than lens names and the coverage floor. It
honours:

- which lens owns each kind of behaviour;
- the team's stated constraints and the strategy's tool tiers;
- known risk areas, which raise risk likelihood;
- the journeys the team said justify end-to-end tests;
- the floor for the specific surface the feature touches.

Inherited policy keeps its provenance (`cited`, `convention`, or `stated`). A stale strategy is flagged.

**Why this priority**: These tighten consistency, but the core workflow works without them.

**Independent Test**: Use a strategy that lists a constraint forbidding containers in CI, a known risk
area, two prioritized journeys, and two surfaces with different floors. Run test-plan on a spec that
touches one surface. Confirm all of the following:

- no container-based tool is named;
- risks in the known area are rated at least Medium likelihood with the strategy cited;
- end-to-end and UAT scenarios favour the named journeys;
- the touched surface's floor is the one inherited;
- every inherited item carries its provenance.

**Acceptance Scenarios**:

1. **Given** the strategy's ownership map assigns a behaviour to integration, **When** a condition
   verifies that behaviour, **Then** it is placed at integration, or the plan states why it was placed
   elsewhere.
2. **Given** a strategy whose recorded `generated` date predates the source the feature touches, or whose
   recorded mode no longer matches the repository, **When** test-plan runs, **Then** it flags the strategy
   as possibly stale and recommends a re-run.
3. **Given** a strategy item marked `convention`, **When** the plan inherits it, **Then** the plan shows
   it as `convention`, not as a project finding.

---

### Edge Cases

- **A strategy written before UAT and Regression existed.** It has neither lens. The plan treats both as
  not established by the strategy and says so loudly. It neither silently applies the defaults nor
  silently omits the sections, and it recommends re-running test-strategy.
- **A strategy that marks UAT not applicable.** The plan has no UAT scenarios. Any acceptance criterion
  that only a UAT scenario could verify goes to "explicitly not covered", with the remedy "re-run
  test-strategy".
- **A lens the strategy marks not applicable, needed by a criterion.** The criterion goes to "explicitly
  not covered", with the reason and the remedy "re-run test-strategy". It is not reassigned to a level the
  strategy did not choose.
- **No strategy at all.** The full default lens set is used (FR-013), flagged once and loudly, with a recommendation to
  run test-strategy.
- **A screenshot or transcript that would capture a secret.** The uat command withholds or masks it,
  records that it did, and never saves the secret into evidence.
- **The build won't start, or needs something the agent lacks** (credentials, a third-party sandbox,
  hardware). The scenario is recorded as blocked with the reason, left open, and never marked as passed or
  failed.
- **A `tasks.md` with no UAT phase.** uat reports that there is nothing to run and changes nothing.
- **UAT tasks a human already ticked.** uat leaves them alone and does not re-run them unless asked.
- **A uat re-run.** It retries only open tasks, keeps prior evidence, and adds new evidence rather than
  overwriting it.
- **The core implement command ticking UAT tasks anyway** — for example, in a project whose constitution
  lacks the clause. The labelled phase note is the only guard there. The test-plan handoff and uat's
  report both state that the clause makes the guard binding.
- **Several hooks after specify.** The test-plan offer sits alongside the existing agent-context and
  git-commit offers. It is optional and never mandatory.
- **Several hooks after implement.** The UAT offer is ordered before the `create-pr` offer, so UAT can run
  before a PR is opened.

## Requirements *(mandatory)*

### Functional Requirements

**Test strategy — new lenses**

- **FR-001**: The test strategy MUST carry two additional lenses, **UAT** and **Regression**, defined by
  what they prove:
  - **UAT** proves the feature is acceptable to its user in the user's own terms. It assumes nothing
    about the implementation, only an assembled build. It is executed by a human, or by the agent only on
    explicit request.
  - **Regression** proves that behaviour which already worked still works after a change. It takes the
    existing suite as the baseline, at whatever level those tests live.
- **FR-002**: Each new lens MUST be marked applicable or not applicable, with a stated reason, exactly as
  the existing four are. Neither may be omitted.
- **FR-003**: Where UAT applies, the strategy MUST state who may execute it (`human`, `agent on explicit
  request`, or both) and what counts as evidence for each surface the project has. Evidence for a surface
  the project does not have MUST NOT be named.
- **FR-004**: Where Regression applies, the strategy MUST name the suite that forms the regression gate,
  cite where it runs (for example, a CI workflow) or state that it does not run anywhere automatically,
  and state whether a fixed defect earns a regression test.
- **FR-005**: The strategy's existing rules MUST bind the new lenses unchanged: evidence or a marker,
  cited absence, no tool the stack cannot run, tool tiers, and stated coverage.
- **FR-006**: The constitution amendment the strategy drafts MUST include a clause that UAT tasks are
  never executed or marked complete by the implement command and run only on explicit request. It MUST be
  drafted only where UAT applies, and test-strategy MUST still never write the constitution itself.
- **FR-007**: The strategy MUST record its lens-ownership map in a form the test plan can read: which lens
  owns which kind of behaviour.

**Test plan — consistency with the strategy**

- **FR-010**: The test plan MUST make available exactly the lenses the strategy marks applicable, plus
  `manual`. A lens the strategy marks not applicable MUST NOT be assigned to any condition or scenario.
  Two kinds of lens are distinguished:
  - **Condition levels** — unit, integration, api-contract, end-to-end, any lens the evidence added, and
    `manual` — are what a test condition is assigned to.
  - **UAT and Regression are section-bearing.** They decide whether the Suggested UAT scenarios and
    Regression scope sections exist, and are never a condition's level.
- **FR-011**: An acceptance criterion that only a lens ruled out by the strategy could verify MUST be
  listed under "explicitly not covered", with the reason and the remedy "re-run test-strategy".
- **FR-012**: When the strategy predates the UAT and Regression lenses — it carries neither — the plan
  MUST state this prominently in the document and the report, and MUST recommend re-running
  test-strategy. It MUST NOT silently add or silently drop those sections.
- **FR-013**: With no strategy document, the plan MUST use the default **lens set** (`unit`,
  `integration`, `api-contract`, `end-to-end`, `uat`, `regression`). Its condition levels are therefore
  `unit`, `integration`, `api-contract`, `end-to-end` and `manual`, and both sections are present. The
  plan MUST state once and prominently that no strategy exists, and MUST recommend running test-strategy.
- **FR-014**: `manual` MUST stay available as its own level for one-off human checks of a single
  condition, distinct from UAT scenarios.

**Test plan — new sections**

- **FR-020**: Where UAT is available, the plan MUST include a **Suggested UAT scenarios** section. Each
  scenario MUST:
  - be derived from the spec's user stories or acceptance scenarios;
  - be traced to a spec identifier in the existing forms (`FR-xxx`, `USn-ACn`, or a short verbatim
    quotation);
  - be written as a user-visible journey with an expected outcome;
  - name an executor of `agent`, `human`, or `either`.
- **FR-021**: test-plan MUST mark a UAT scenario executable by the agent only when two things hold: the
  project's manifests show a surface of a kind an agent can drive (`browser`, `cli`, or `http`), and the
  strategy's UAT executor policy permits it. Otherwise the scenario MUST be `human`, with the reason
  stated. test-plan MUST NOT judge this from its own session's tools, because uat runs in a later session
  whose tools may differ. That judgment belongs to uat (FR-054).
- **FR-022**: Each UAT scenario MUST state the evidence that would show it passed, taken from the
  strategy's per-surface evidence rule where one exists.
- **FR-023**: UAT scenarios MUST inherit priority from what they verify, by the plan's existing priority
  derivation.
- **FR-024**: Where Regression is available, the plan MUST include a **Regression scope** section that
  lists the existing tests found to touch the feature's modules, each cited by file. Risk-driven
  additions MUST be labelled as such. Where none is found, it MUST state the search performed and where,
  rather than an unqualified claim of absence.
- **FR-025**: The new sections MUST carry no checkbox and no status field, consistent with the plan's
  existing rules. Both sections MUST be declared in the shipped test-plan template and remain overridable.
- **FR-026**: Where UAT is available, **every user story** in the specification MUST either be the
  subject of at least one UAT scenario, or be listed under "explicitly not covered" with its reason. A
  story fully verified by automated conditions still gets a scenario, because UAT judges the journey, not
  the parts.

**Test plan — honouring the whole strategy**

- **FR-030**: When choosing a condition's level, the plan MUST honour the strategy's lens-ownership map.
  Where it departs from the map, it MUST state why.
- **FR-031**: The plan MUST NOT name a tool the strategy places at no tier or rules out through a stated
  team constraint.
- **FR-032**: Risk areas the strategy records as having broken before, or as feared, MUST raise the
  likelihood rating of any risk in that area to at least Medium, with the strategy cited as the trigger.
- **FR-033**: When assigning end-to-end conditions and UAT scenarios, the plan MUST favour the journeys
  the strategy records as worth end-to-end coverage, and MUST say when a journey it covers is not among
  them.
- **FR-034**: Where the strategy declares per-surface floors, the plan MUST inherit the floor of each
  surface the feature touches, and name the surface.
- **FR-035**: Every item the plan inherits from the strategy MUST carry the strategy's provenance for it
  (`cited`, `convention`, or `stated`).
- **FR-036**: The plan MUST flag the strategy as possibly stale, and recommend a re-run, when either of
  these holds: its recorded mode no longer matches the repository's evident state, or the source the
  feature touches has changed since the strategy's recorded generation date by evidence the plan can read.
- **FR-037**: The outcome count in test-plan's spec-resolution step MUST match the outcomes it lists.

**Workflow wiring**

- **FR-040**: The extension MUST register an **optional** `after_specify` hook offering test-plan. The
  hook's prompt MUST tell the agent to pass the spec file path that specify just reported.
- **FR-041**: test-plan MUST keep refusing to infer the specification. Being reached through the hook
  MUST NOT relax that rule, and a hook invocation with no path MUST stop exactly as an empty invocation
  does.
- **FR-042**: test-plan's stated rationale about hooks MUST be rewritten to match: it is offered through
  an optional hook and still never runs on its own.
- **FR-043**: After writing, test-plan MUST print a ready-to-paste planning prompt that links the written
  `test-plan.md` and instructs the planning command to record these obligations in `plan.md`:
  - every P1 condition maps to a test task written before the implementation it covers;
  - conditions are tested at their assigned levels;
  - the regression scope is kept green;
  - UAT scenarios become tasks in a final, labelled UAT phase marked as not executed by the implement
    command.
- **FR-044**: No Spec Kit core command file or core template may be edited by this change, or by any
  command it ships.

**The UAT runner — `speckit.spectra.uat`**

- **FR-050**: A new command, `speckit.spectra.uat`, MUST perform UAT for one feature only when explicitly
  invoked. It MUST also be offered through an optional `after_implement` hook ordered before the existing
  `create-pr` offer.
- **FR-051**: It MUST take the feature to act on as an explicit input and MUST NOT infer it, consistent
  with test-plan.
- **FR-052**: It MUST read the UAT phase of the feature's `tasks.md` and the matching scenarios in its
  `test-plan.md`. Where either is missing it MUST say so. With no UAT phase it MUST change nothing.
- **FR-053**: Where implementation tasks are still unchecked, it MUST report this and ask before going on.
- **FR-054**: It MUST attempt only scenarios marked `agent` or `either`, and only on a surface that the
  tools available in **its own** session can operate. It MUST state which tools it relied on. Where the
  plan marked a scenario `agent` but this session cannot drive its surface, the scenario is
  `awaiting human` with that reason. Scenarios marked `human` MUST be listed as awaiting a human and left open.
- **FR-055**: Before starting the project's build or any process, it MUST state what it will run and get
  confirmation. By default it MUST run against a locally started build. It MUST NOT act against any other
  environment unless the user names that environment in the invocation.
- **FR-056**: It MUST save evidence for every scenario it attempts — screenshots, transcripts, or
  comparisons, as the surface admits — under the feature's directory in `specs/`.
- **FR-057**: It MUST mark a UAT task complete only when it observed the scenario's expected outcome, and
  MUST link the evidence from that task. A failed, blocked, or unattempted scenario MUST stay unchecked.
- **FR-058**: It MUST NOT reproduce a secret in any evidence or report. Where captured output would
  contain one, it MUST withhold or mask it and record that it did.
- **FR-059**: It MUST NOT modify source, tests, test configuration, CI, the specification, the test plan,
  or the constitution. The only edits it makes to `tasks.md` are completion marks and evidence links on
  UAT tasks.
- **FR-060**: It MUST write a UAT report for the run under the feature's directory, shaped by a new
  registered, overridable template. The report lists each scenario's outcome (`passed`, `failed`,
  `blocked`, or `awaiting human`), its evidence, and its reason.
- **FR-061**: It MUST leave UAT tasks a human already ticked untouched. A re-run MUST retry only open
  tasks and MUST add evidence rather than overwrite earlier evidence.
- **FR-062**: It MUST make no network request beyond what the project's own build under test makes. The
  only exception is an environment the user explicitly named per FR-055.

**Shipping**

- **FR-070**: The change MUST meet Principle V in the same change:
  - a catalog-channel version bump with a matching changelog entry;
  - the new command registered in the manifest and the roster;
  - the catalog, package, landing page, and generated agent listings regenerated;
  - a hand-written prose block for the new agent.
- **FR-071**: The CLI channel and its `VERSION` MUST NOT change.

### Key Entities

- **Lens**: a kind of testing, defined by what it proves and what it may assume. The set grows from four
  to six (adding UAT and Regression); `manual` remains a plan-only level.
- **Lens-ownership map**: the strategy's statement of which lens owns which kind of behaviour, read by the
  plan.
- **UAT scenario**: a user-visible journey with an expected outcome. It carries a spec identifier, a
  priority, an executor (`agent`, `human`, or `either`), and the evidence that would show it passed.
- **Regression scope**: the existing tests, cited by file, that must stay green for a feature, plus
  labelled risk-driven additions.
- **UAT phase**: the final, labelled phase in `tasks.md` holding one task per UAT scenario, marked as not
  executed by implement.
- **UAT evidence**: screenshots, transcripts, or comparisons saved per attempted scenario under the
  feature's directory.
- **UAT report**: the record of one uat run — each scenario's outcome, its evidence, and its reason.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In a project whose strategy marks UAT applicable, 100% of the user stories in a spec are
  either represented by at least one UAT scenario, or listed as explicitly not covered with a reason.
- **SC-002**: Following the printed planning prompt, then running tasks, yields a `tasks.md` in which
  every P1 test condition maps to a task and every UAT scenario maps to a task in the UAT phase. The target
  is 100% traceability, checkable by count.
- **SC-003**: After implement completes in a project carrying the constitution clause, 0 UAT tasks are
  marked complete.
- **SC-004**: After a uat run, every UAT task marked complete links evidence, and 0 tasks for failed,
  blocked, or human-only scenarios are marked complete.
- **SC-005**: Across test plans generated for a project, no plan assigns a lens the project's strategy
  marks not applicable: 0 violations.
- **SC-006**: A developer goes from a finished specification to a running test-plan in one reply to the
  after-specify offer, without typing the spec path by hand.
- **SC-007**: No evidence file or report produced by uat contains a secret value: 0 occurrences.

## Assumptions

- The new agent's roster entry is id `uat`, titled "UAT Runner", in the testing-quality phase, type
  add-on, provider spectra. The title can be reworded later without breaking anything, since prose is
  keyed to the id.
- UAT evidence and the UAT report live under the feature's own `specs/<feature>/` directory, beside the
  test plan. This is the same reasoning spec 021 argued for writing `test-plan.md` beside the spec.
  Because two commands now write per-feature deliverables there, this change amends Principle VII to
  state that carve-out explicitly (plan, research R4) instead of re-arguing it case by case.
- Whether the agent can "drive" a surface is judged at two points:
  - **test-plan** judges by the kind of surface the manifests show and by the strategy's executor policy
    (FR-021);
  - **uat** judges by the tools its own session actually has, and states which it relied on (FR-054).

  The two sessions may differ, so neither borrows the other's judgment.
- By default UAT runs against a locally started build. Running against a deployed or shared environment
  happens only when the user names it.
- Existing strategy documents are not migrated. A re-run of test-strategy produces the new lenses, and
  test-plan flags older strategies until then.
- The core implement command reads the project constitution, so a constitution clause is a binding guard
  on UAT tasks. The labelled-phase note in `tasks.md` is the fallback where the clause is absent.
- This is a minor catalog-channel release: one command added, two changed, and no command renamed or
  removed.
