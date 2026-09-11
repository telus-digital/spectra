# Feature Specification: Test Plan Agent

**Feature Branch**: `021-test-plan-agent`

**Created**: 2026-09-11

**Status**: Implemented

**Input**: User description: "Build a new command (agent) called `/test-plan`. It needs an argument; a
spec file, without it the AI will not continue, it will prompt the user and ask for that spec. The idea
of this is take place after `spec.md` is created by `specify`. There's no need for `specify` command to
be modified so that it becomes aware and suggests `test-plan` as `test-plan` is an add-on (optional)
agent. This agent will be mostly used for teams that follow TDD, that want to have a test plan prior to
actual implantation. The agent will look at the specs, has access to the source code, the constitution
(test strategy) and generates a test plan accordingly. The generated test plan will be next to the spec
that was fed to it. The file name will be `test-plan.md`. The template will look like attached, however,
important to note that the `test-plan.md` file will not have any checkboxes, the idea is not to track
anything here, but rather this document will be used to be shared and approved by the stakeholders. Once
done, then the file can be fed to `/plan` command as an optional input so the AI will know that it has to
plan around it and write tests for those in the tasks." — followed by an attached template example whose
section structure (title block, 1. Scope, 2. Risks, 3. Test Conditions, 4. Environment & Data,
5. Exit Criteria, and a guidance table of optional sections) is carried into FR-030 through FR-046.

## Clarifications

### Session 2026-09-11

The description is unusually complete, so most of what follows records how it lands against Spectra's
own constitution rather than resolving genuine ambiguity. Two items are narrow, deliberate deviations
and are called out as such.

- Q: The description says the test plan is written "next to the spec that was fed to it", as
  `test-plan.md`. Principle VII sends every durable Markdown deliverable to
  `<artifact-root>/<artifact>/NNN-<name>.md`. Which applies? → A: **Next to the spec, and this is the
  carve-out rather than a breach — but only partly.** Principle VII places `.specify/` and `specs/`
  outside its location rule, because a command writing there is producing input for another command
  rather than a free-standing document. That is exactly this artifact's second job: `/plan` consumes it.
  It also matches the shape of everything else in a feature directory — `spec.md`, `plan.md`,
  `tasks.md` are all read by humans *and* by commands, all unnumbered, all identified by the directory
  they sit in. A per-feature test plan filed into a global `docs/test-plan/` series would need a
  number, and that number would carry no information the feature directory does not already carry.
  Where the fit is imperfect is the first job: this document is explicitly for stakeholder approval, so
  it is a human deliverable too, and Principle VII's rationale for the carve-out speaks of context and
  not deliverables. That makes the placement a **reasoned reading of the carve-out, not a clean
  application of it**, and the plan MUST record it in Complexity Tracking rather than leave it implicit
  (FR-021, FR-021a). No artifact subfolder, no sequence number, and no artifact-root resolution or
  publication check apply — the destination is fixed by the spec's own location.

- Q: The attached template renders section 5 (Exit Criteria) as a Markdown checklist, but the
  description says the file "will not have any checkboxes". Which wins? → A: **No checkboxes anywhere,
  including section 5.** Exit criteria are written as plain declarative statements of what must hold,
  each with its threshold and the role who confirms it (FR-040). This is not cosmetic: an approved,
  circulated document that also contains live checkboxes creates a second place where progress appears
  to be tracked, and it will disagree with `tasks.md`. The plan states the bar; `tasks.md` tracks
  whether the bar was met. The prohibition covers the whole document — the command MUST NOT emit
  `- [ ]` or `- [x]` in any section, and MUST strip them from a template layer that reintroduces them
  (FR-041).

- Q: What happens when the command is invoked with no argument? → A: **It stops and asks. It never
  infers the spec.** No branch-name inference, no `.specify/feature.json` lookup, no "most recently
  modified spec" heuristic, and no scanning of `specs/` (FR-007, FR-008). This is a deliberate
  departure from the spec-discovery behaviour spec 017 gave the rest of the workflow, and the reason is
  the blast radius of being wrong: a test plan generated against the wrong specification is a document
  that reads as authoritative, gets circulated to stakeholders, and is approved by people who cannot
  tell from reading it that it describes a different feature. Guessing a path is cheap to recover from
  when the output is a task list and expensive when the output is a signed-off artifact.

- Q: The description says the file "can be fed to `/plan` as an optional input". Does that require
  changing `/plan`? → A: **No. The command hands over the exact invocation and changes nothing.**
  `/speckit-plan` is a Spec Kit core command; Spectra neither owns it nor may edit it, and Principle II
  confines every Spectra capability to a command file under `spectra/commands/`. The handoff is
  therefore the same pattern `speckit.spectra.test-strategy` uses for `/speckit-constitution`: print the
  literal invocation, naming the test plan's path, for the user to run (FR-047, FR-048). No hook is
  registered on `before_plan` either — a hook would make `/plan` prompt for a test plan on every
  feature in every project that installs Spectra, which is precisely the not-opt-in behaviour the
  description rules out for `/specify`.

- Q: Is `/speckit-specify` modified to suggest this agent? → A: **No, per the description.** Nothing
  outside the new command file, its template, and the sync artifacts Principle V requires is touched.
  Discovery is the roster's job, not a prompt injected into a core command (FR-005).

- Q: The description says the agent has access to "the constitution (test strategy)". Where does the
  testing policy actually come from? → A: **From both, with a fixed precedence.** The agent reads the
  constitution under `.specify/memory/` *and*, where present, the strategy document
  `speckit.spectra.test-strategy` writes at `<artifact-root>/test-strategy/TEST_STRATEGY.md` — resolving
  a declared `Artifact root:` line to find it. A constitutional obligation outranks the strategy
  document, which outranks the agent's own judgement (FR-011 to FR-014). Where neither exists the plan
  is still produced, and says so. Where the two conflict, the conflict is reported rather than silently
  resolved.

- Q: What vocabulary does the "Level" column use? The attached template suggests
  "Unit / Integration / E2E / Manual", while `test-strategy` defines four lenses including API contract
  and no manual lens. → A: **The project's own lens names win where they exist.** With a
  `TEST_STRATEGY.md` present, the Level column uses that document's lens names verbatim, so the two
  artifacts can be read against each other. With no strategy, the default set is unit, integration, API
  contract, end-to-end, and manual (FR-035, FR-036). `Manual` is retained in both cases because a test
  plan, unlike a strategy, must be able to place a condition that no automated lens will ever cover.

- Q: What if the supplied `spec.md` still carries unresolved `[NEEDS CLARIFICATION]` markers, or
  requirements too vague to test? → A: **Produce the plan and name the gap; never invent the missing
  decision.** Each unresolved marker and each untestable requirement is listed as a requirement with no
  test condition, with the reason, and `/speckit-clarify` is named as the remedy (FR-026, FR-027). A
  fabricated test condition for an ambiguous requirement is the worst available outcome: it launders a
  guess into something a stakeholder approves.

- Q: Which roster phase does the agent belong to? → A: **`requirements-discovery`.** The phase records
  *when you run an agent*, not what topic it covers — `speckit.spectra.test-strategy` is a testing agent
  placed in `foundation` for exactly that reason. This one runs immediately after `/speckit-specify` and
  before `/speckit-plan`, alongside `clarify` and `checklist`, and the work it does — turning acceptance
  criteria into traceable conditions and getting them agreed — is requirements work (FR-006).

- Q: Does the agent write tests, edit source, or touch CI? → A: **No. One file, and nothing else.** It
  writes `test-plan.md` in the supplied spec's directory and makes no other change anywhere, including
  to the spec it read (FR-018 to FR-020). Writing the tests is `/speckit-implement`'s job against the
  tasks `/speckit-tasks` derives; the value of this agent is that the tests get agreed before they are
  written.

- Q: Does the generated document carry the attached template's "Add only if you need it" table? → A:
  **No — that is authoring guidance, and guidance is stripped.** The table ships in the template so a
  team editing an override can see the intent, and the command decides which optional sections the
  feature actually warrants, adds those, and states which it added and why (FR-044, FR-045). Emitting a
  table that tells a stakeholder when to add a section they are not being asked to write is noise in a
  document whose whole purpose is to be read and approved.

- Q: What happens on a re-run where `test-plan.md` already exists? → A: **Read it, then rewrite it in
  place on explicit confirmation.** There is one current test plan per feature, as there is one
  `spec.md`; version history is Git's job. The existing file is an input — a condition a previous run
  recorded as explicitly not covered is a decision, and silently dropping it would erase it (FR-050,
  FR-051).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Agree the tests before writing any code (Priority: P1)

A team practising TDD has just finished `/speckit-specify` for a new feature. Before anyone plans the
implementation, they want a test plan they can put in front of a product owner and a QA lead: what will
be verified, what deliberately will not be, where the risk sits, and what "done" means. They run the
agent with the path to their new `spec.md` and get one document next to it.

**Why this priority**: This is the agent. Without it there is nothing to review before implementation
starts, which is the entire premise.

**Independent Test**: Run the command against a feature directory containing only `spec.md`. Verify that
`test-plan.md` appears beside it, that it contains the scope, risk, condition, environment, and exit
sections, that every acceptance criterion in the spec appears in at least one test condition, and that
the file contains no checkbox anywhere.

**Acceptance Scenarios**:

1. **Given** a feature directory with a complete `spec.md` and no `test-plan.md`, **When** the agent is
   run with that spec's path, **Then** `test-plan.md` is written in that same directory and no other file
   in the project is created or modified.
2. **Given** a spec with acceptance criteria and numbered requirements, **When** the plan is generated,
   **Then** every acceptance criterion is referenced by at least one test condition, and every test
   condition names the requirement or criterion it verifies.
3. **Given** any generated plan, **When** the file is read, **Then** it contains no `- [ ]` or `- [x]`
   construct in any section, including exit criteria.
4. **Given** a generated plan, **When** a reader looks for what will not be tested, **Then** the
   out-of-scope statement and the explicitly-not-covered list are both present and non-empty, each item
   carrying a reason.

---

### User Story 2 - Inherit the project's testing policy instead of inventing one (Priority: P1)

A project has already run `speckit.spectra.test-strategy` and amended its constitution with the
resulting policy: named lenses, a coverage floor, and the tools its stack can actually run. The team
expects a test plan that uses that vocabulary and respects that floor, not a generic plan that
recommends a browser driver to a command-line tool.

**Why this priority**: Principle IV makes context-awareness the feature rather than a nicety. A test plan
that contradicts the project's own declared strategy is worse than no plan, because it forces a reviewer
to adjudicate between two documents that both claim authority.

**Independent Test**: Run the command in a project carrying both a constitutional testing obligation and
a `TEST_STRATEGY.md`. Verify the Level column uses the strategy's lens names, that no tool appears that
the project's manifests cannot run, and that the plan cites where each inherited constraint came from.

**Acceptance Scenarios**:

1. **Given** a project with `TEST_STRATEGY.md` present, **When** the plan is generated, **Then** the
   Level column uses that document's lens names and the plan records that it was consulted, by path.
2. **Given** a constitutional testing obligation that conflicts with the strategy document, **When** the
   plan is generated, **Then** the constitution is followed and the conflict is reported rather than
   silently resolved.
3. **Given** a project with neither a constitution nor a strategy document, **When** the plan is
   generated, **Then** it is still produced, the default lens set is used, and the absence is stated.
4. **Given** a project whose dependency manifests contain no browser, **When** the plan is generated,
   **Then** no condition is assigned to a browser-driven level and no browser tool is named.

---

### User Story 3 - Refuse to guess which spec was meant (Priority: P1)

A developer types the command with nothing after it. Rather than picking a spec from the current branch
or the most recent directory, the agent stops and asks which specification to plan against.

**Why this priority**: The document gets circulated and approved. A plan generated against the wrong spec
is authoritative-looking and undetectably wrong to the people asked to sign it.

**Independent Test**: Invoke with empty input and verify that nothing is read beyond what is needed to
ask the question, that no file is written, and that the response names what to supply. Repeat with a path
that does not exist, and with a path to a directory rather than a file.

**Acceptance Scenarios**:

1. **Given** no argument, **When** the command runs, **Then** it asks for a spec path, writes nothing,
   and does not analyze the project.
2. **Given** a path that does not exist or cannot be read, **When** the command runs, **Then** it reports
   the path and the reason and stops without writing.
3. **Given** a path to a feature directory that contains a `spec.md`, **When** the command runs, **Then**
   it resolves the `spec.md` inside it, states the resolution, and continues.
4. **Given** a readable file that is not a specification, **When** the command runs, **Then** it says why
   it is not usable as one and stops.
5. **Given** a non-interactive session with no argument, **When** the command runs, **Then** it reports
   that the required input is missing and exits without writing.

---

### User Story 4 - Hand the agreed plan to the planner (Priority: P2)

The plan has been reviewed and approved. The team now wants `/speckit-plan` to design around it so the
tasks include the tests it names.

**Why this priority**: The handoff is what makes the document part of the workflow rather than a
deliverable that stops at approval. It is P2 because it is one line of output, not a mechanism.

**Independent Test**: Complete a run and verify the closing output contains a literal, copyable
`/speckit-plan` invocation naming the written `test-plan.md` path, and that `/speckit-plan` itself is
unmodified.

**Acceptance Scenarios**:

1. **Given** a completed run, **When** the agent reports, **Then** it emits the exact `/speckit-plan`
   invocation that passes the written plan's path as input.
2. **Given** a completed run, **When** the project is inspected, **Then** no core Spec Kit command file
   and no hook registration has been changed or added.

---

### User Story 5 - Re-run after the spec changes (Priority: P2)

`/speckit-clarify` resolved three open questions and the spec now says something different. The team
re-runs the agent on the same spec.

**Why this priority**: A plan that cannot be refreshed goes stale on first contact with clarification,
and a team that has to hand-merge it will stop using the agent.

**Independent Test**: Generate a plan, edit the spec, re-run, and verify the existing plan was read, that
rewriting required confirmation, and that a previously recorded not-covered decision is either carried
forward or reported as dropped.

**Acceptance Scenarios**:

1. **Given** an existing `test-plan.md`, **When** the agent runs on the same spec, **Then** it reads the
   existing plan and asks for confirmation before rewriting it.
2. **Given** confirmation is declined, **When** the run ends, **Then** the existing file is unchanged and
   nothing else is written.
3. **Given** the existing plan recorded a condition as explicitly not covered, **When** the plan is
   rewritten, **Then** that decision is carried forward or its removal is stated.

---

### User Story 6 - Plan for a feature in a codebase that already exists (Priority: P3)

The feature touches existing modules. The team wants the plan to reflect what is already covered, so
they are not asked to approve re-testing ground the suite already holds.

**Why this priority**: It sharpens the output but the plan is useful without it, and a greenfield feature
has no prior coverage to read.

**Independent Test**: Run against a spec for a change to an existing, tested module and verify that
conditions already covered by the suite are identified as such with a cited test path, and that gaps are
cited by what was searched for.

**Acceptance Scenarios**:

1. **Given** a spec touching code with existing tests, **When** the plan is generated, **Then**
   conditions the suite already covers are marked as such, citing the test file.
2. **Given** a behaviour with no test found, **When** the plan states that gap, **Then** it cites what was
   searched for and where, rather than asserting absence unqualified.

---

### Edge Cases

- **The spec is outside a Spec Kit project**, or `.specify/` does not exist. The plan is produced from
  the spec and any readable source, and the missing context is stated.
- **The spec path is inside a different repository or above the project root.** The agent reads it in
  place if readable, and writes the plan beside it only if that directory is inside the project it was
  invoked in; otherwise it reports the conflict and stops rather than writing outside the project.
- **The spec has no acceptance criteria at all** — only prose. The agent derives conditions from the
  requirements it can find, and states that the traceability column has nothing to anchor to.
- **The spec's requirements are all non-functional** (performance, accessibility, security budgets). The
  optional non-functional section is added and the plan says so.
- **A template layer resolves but is empty or unreadable.** The agent says so in one line and continues
  down the resolution stack.
- **A template override reintroduces checkboxes**, or drops a mandatory section. Checkboxes are stripped;
  a dropped section is noted as omitted and not reinstated.
- **The same spec is planned twice concurrently.** Last write wins; no locking is attempted. The
  confirmation gate is what makes this visible.
- **The project's declared `Artifact root:` is unusable** (leading slash, `..`). It only affects where
  `TEST_STRATEGY.md` is looked for; the agent says the value is unusable, falls back to the default, and
  the plan's own destination is unaffected.
- **The spec describes a documentation-only or configuration-only change** with no testable behaviour.
  The agent says so plainly and produces a plan whose condition table is deliberately near-empty rather
  than padding it.
- **A requirement would require a secret to test.** The agent names the credential's kind and where it
  is configured, and never reproduces its value.

## Requirements *(mandatory)*

### Functional Requirements

#### Identity and registration

- **FR-001**: The capability MUST ship as a single command file under `spectra/commands/`, registered in
  `spectra/extension.yml` under `provides.commands`, inside the one self-contained `spectra/` extension.
- **FR-002**: The command MUST be named `speckit.spectra.test-plan` and MUST begin with YAML front matter
  containing a `description`.
- **FR-003**: The command MUST be agent-agnostic, taking its input through `$ARGUMENTS` and hard-coding
  no single agent's invocation syntax.
- **FR-004**: The command's effect MUST be declared consistently with what it does: it writes exactly one
  file inside the project.
- **FR-005**: No existing command file MUST be modified, and no new hook MUST be registered, in
  `spectra/extension.yml` or anywhere else. Specifically, `/speckit-specify` and `/speckit-plan` MUST
  remain unaware of this agent.
- **FR-006**: The agent MUST be registered in `agents-list.json` in the `requirements-discovery` phase
  with `provider: spectra`, `type: add-on`, `status: available`, and `command: speckit.spectra.test-plan`.

#### The required argument

- **FR-007**: The command MUST require a specification path. With empty input it MUST ask the user for
  that path and stop.
- **FR-008**: With empty input the agent MUST NOT infer the specification by any means — not from the
  current Git branch, not from `.specify/feature.json`, not from modification times, and not by scanning
  `specs/`.
- **FR-009**: With empty input the agent MUST NOT read source code, analyze the project, or write any
  file.
- **FR-010**: The command MUST accept either a path to a specification file or a path to a directory
  containing one, resolving the latter to the `spec.md` inside it and stating the resolution. A path that
  is missing, unreadable, ambiguous, or not usable as a specification MUST be reported by name with the
  reason, and the run MUST stop without writing.

#### Context the agent reads

- **FR-011**: Before writing anything the agent MUST read the supplied specification in full, and MUST
  read, where present: `.specify/memory/constitution.md`, the project's test strategy document, existing
  test directories and test framework configuration, dependency manifests, CI workflow definitions, and
  the source code the specification's behaviour touches.
- **FR-012**: The agent MUST look for the test strategy document at `<artifact-root>/test-strategy/`,
  resolving a constitutional `Artifact root:` declaration (matched case-insensitively) and defaulting to
  `docs/`. An unusable declared value MUST be reported and the default used.
- **FR-013**: Where the constitution carries a testing obligation and the strategy document carries a
  different one, the constitution MUST prevail and the conflict MUST be reported in the document.
- **FR-014**: Where neither a constitution nor a strategy document exists, the plan MUST still be
  produced and the absence MUST be stated.
- **FR-015**: The agent MUST record every input it consulted, by path, and MUST record by name and reason
  any input it expected and could not read.
- **FR-016**: The agent MUST state what portion of the relevant code and tests it read and what it could
  not see, so a reader can distinguish a checked absence from an unchecked one.
- **FR-017**: The agent MUST NOT ask the user for anything the specification or the repository already
  answers.

#### What the agent never does

- **FR-018**: The agent MUST write exactly one file per run — the test plan — and MUST NOT create,
  modify, or delete any other file, including the specification it read.
- **FR-019**: The agent MUST NOT edit the constitution, create a branch, stage, or commit.
- **FR-020**: The agent MUST NOT write, modify, or generate test code; MUST NOT modify test framework,
  coverage, or CI configuration; and MUST NOT run, build, or install anything.
- **FR-020a**: The agent MUST make no network request and MUST NOT accept a repository URL, credential,
  or token.
- **FR-020b**: The agent MUST NOT reproduce a secret value in the document or in the session. Where a
  test condition depends on one, it MUST name the credential's kind and where it is configured, and state
  that the value was withheld.

#### Output location

- **FR-021**: The plan MUST be written as `test-plan.md` in the same directory as the specification
  supplied to the command. It MUST NOT be numbered, MUST NOT be placed in an artifact subfolder, and MUST
  NOT be subject to artifact-root resolution or the publication check.
- **FR-021a**: Because the document is also a stakeholder deliverable, this placement MUST be recorded in
  the plan's Complexity Tracking as a reasoned narrow reading of Principle VII's Spec Kit carve-out, with
  its justification, rather than passed over as automatically compliant.
- **FR-022**: Where the resolved specification lies outside the project the command was invoked in, the
  agent MUST report the conflict and stop rather than write outside that project.

#### Traceability, the core invariant

- **FR-023**: Every acceptance criterion in the supplied specification MUST be referenced by at least one
  test condition.
- **FR-024**: Every test condition MUST name the requirement, acceptance criterion, or success criterion
  it verifies, using that item's own identifier where the specification provides one.
- **FR-025**: The agent MUST report any acceptance criterion it could not cover, with the reason, rather
  than omitting it silently.
- **FR-026**: Each unresolved `[NEEDS CLARIFICATION]` marker in the specification MUST be listed as a
  requirement carrying no test condition, with `/speckit-clarify` named as the remedy.
- **FR-027**: Where a requirement is too ambiguous to test, the agent MUST say so and MUST NOT invent a
  test condition that resolves the ambiguity by assumption.
- **FR-028**: A statement that something is not covered by the existing suite MUST cite what was searched
  for and where. An unqualified claim of absence MUST NOT be made.
- **FR-029**: A claim that a behaviour is already covered MUST cite the test file that covers it.

#### Document structure

- **FR-030**: The document MUST open with an identifying block giving the specification it plans against
  (as a path or link), the build under test, and the author and date.
- **FR-031**: The document MUST carry a scope section stating both what is in scope and what is
  deliberately out of scope, each out-of-scope item naming who covers it if anyone.
- **FR-032**: The document MUST carry a risk section as a table of risk, likelihood, impact, and the
  testing response to it.
- **FR-033**: The risk section MUST be prioritized: the agent MUST NOT rate every row at the highest
  likelihood and impact, and MUST keep the section short enough to be a decision rather than an
  inventory.
- **FR-034**: The document MUST carry a test conditions table whose rows each have an identifier, the
  condition in one line, what it verifies, its level, and its priority.
- **FR-035**: Where a test strategy document exists, the level vocabulary MUST be that document's lens
  names, used verbatim.
- **FR-036**: Where no test strategy exists, the level vocabulary MUST be unit, integration, API
  contract, end-to-end, and manual.
- **FR-037**: A condition MUST be assigned to the cheapest level that can actually verify it, and no
  level or tool MUST be named that the project's stack cannot run.
- **FR-038**: Conditions MUST be stated as things that must be true, not as test scripts or step
  sequences.
- **FR-039**: The test conditions section MUST be followed by an explicit statement of conditions
  consciously not covered, each with its reason.
- **FR-040**: The document MUST carry an environment and data section covering where tests run and what
  is stubbed versus real, the test data and how it is reset, and the prerequisites; and an exit criteria
  section stating what must hold for a go decision, each criterion with its threshold and the role who
  confirms it.
- **FR-041**: The document MUST contain no checkbox construct in any section. Where a resolved template
  layer contains one, it MUST be rendered as a plain statement instead.
- **FR-042**: The document MUST NOT contain any tracking construct that duplicates `tasks.md` — no status
  column, no progress field, no completion marker.
- **FR-043**: The agent MUST strip every guidance comment and unfilled placeholder token from the written
  document, whichever template layer it came from.
- **FR-044**: The template MUST carry a guidance list of sections to add only when the situation warrants
  them, and that guidance MUST NOT appear in the written document.
- **FR-045**: The agent MUST decide which of those optional sections the feature actually warrants, add
  those, and state which it added and why.
- **FR-046**: Where the specification describes no testable behaviour, the agent MUST say so and produce
  a deliberately sparse condition table rather than padding it.

#### Handoff and reporting

- **FR-047**: On completion the agent MUST emit the literal `/speckit-plan` invocation that passes the
  written plan's path as an optional input, ready to copy.
- **FR-048**: The agent MUST NOT itself invoke `/speckit-plan` or any other command.
- **FR-049**: On completion the agent MUST report the written path, the template layer it resolved by
  path, the number of acceptance criteria covered out of those found, and anything it could not read.

#### Re-running

- **FR-050**: Where a `test-plan.md` already exists beside the specification, the agent MUST read it and
  treat it as an input.
- **FR-051**: The agent MUST obtain explicit confirmation before rewriting an existing plan, MUST leave
  the file untouched if confirmation is declined, and MUST carry forward or explicitly report the removal
  of any previously recorded not-covered decision.
- **FR-052**: In a session that cannot take an answer, the agent MUST NOT rewrite an existing plan; it
  MUST report that a plan exists and what it would have changed.

#### The template

- **FR-053**: The document's structure MUST come from a template shipped as
  `spectra/templates/test-plan-template.md` and registered in `spectra/extension.yml` under
  `provides.templates` with a name, file, and description.
- **FR-054**: The template MUST be resolved through Spec Kit's stack, highest priority first: the
  project's override under `.specify/templates/overrides/`, then an installed preset, then the
  extension's own copy under `.specify/extensions/spectra/templates/`, then `.specify/templates/`, then
  the command's inline skeleton as the last resort. The first readable, non-empty layer MUST be used and
  its path MUST be reported.
- **FR-055**: The agent MUST honour the resolved template's sections and order, MUST NOT add, rename, or
  reorder them, and MUST note rather than reinstate a section the template omits.
- **FR-056**: The rules the command owns — the traceability invariant, the no-checkbox rule, the
  cited-absence rule, the secret prohibition, and the coverage statement — MUST remain in the command and
  MUST NOT be overridable by a template.
- **FR-057**: The agent MUST NOT create or edit any template file, and MUST name the override path as the
  supported customization route.

#### Catalog and package sync

- **FR-058**: `extension.version` in `spectra/extension.yml` MUST be bumped as a MINOR release for the
  added command, with a matching `spectra/CHANGELOG.md` entry under that version.
- **FR-059**: The `spectra` entry in `catalog.json` MUST be updated so its version, command count, and
  tags agree with the manifest.
- **FR-060**: `docs/packages/spectra.zip` MUST be rebuilt with `tools/build_package.py` so the published
  package contains the new command and template.
- **FR-061**: `docs/index.html` MUST list the new command without hard-coding any value another artifact
  already defines.
- **FR-062**: Every generated agent listing MUST be regenerated with `tools/generate_agent_docs.py`, and
  the hand-written per-agent prose block the new agent requires MUST be authored.
- **FR-063**: The repository's `unittest` suite MUST cover the agent's invariants, and
  `tools/generate_agent_docs.py --check` MUST pass.

### Key Entities

- **Test plan**: One Markdown document per feature, living beside its specification as `test-plan.md`.
  Carries scope, risks, test conditions, environment and data, and exit criteria. Read by stakeholders
  for approval and by `/speckit-plan` as input. Holds no tracking state.
- **Test condition**: One row of the conditions table — an identifier, a one-line statement of what must
  be true, the specification item it verifies, the level it lives at, and its priority. The unit of
  traceability.
- **Level**: The lens a condition is verified at. Inherited from the project's test strategy where one
  exists, otherwise unit, integration, API contract, end-to-end, or manual.
- **Specification**: The input. A `spec.md` supplied by path, or a directory resolved to the one inside
  it. Read, never written.
- **Test strategy**: The project-wide policy produced by `speckit.spectra.test-strategy`, read as an
  input. Supplies lens names, the coverage floor, and the tools the stack can run.
- **Constitution**: `.specify/memory/constitution.md`. Supplies any binding testing obligation and the
  artifact root used to locate the strategy. Read, never written.
- **Template**: `test-plan-template.md`, resolved through Spec Kit's layered stack, shaping the
  document's sections. Read, never written.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A team can go from a finished specification to a test plan ready to circulate in a single
  command invocation, with no manual authoring step in between.
- **SC-002**: 100% of the acceptance criteria in the supplied specification are either referenced by a
  test condition or listed as uncovered with a reason — never silently absent.
- **SC-003**: Every test condition traces to a named item in the specification, so a reviewer can check
  coverage in both directions without reading the code.
- **SC-004**: A generated plan contains zero checkboxes and zero tracking fields, in every section, on
  every run.
- **SC-005**: Invoked with no argument, the command writes nothing, reads no source code, and asks for
  the specification — in 100% of runs.
- **SC-006**: In a project with a declared testing policy, every level name and every tool named in the
  plan comes from that policy or from the project's own manifests, with no exception.
- **SC-007**: A stakeholder with no access to the codebase can read the plan and answer what will be
  verified, what will not, and what "done" means, without asking a follow-up question.
- **SC-008**: A reader can tell, for every absence claim in the document, whether it was checked or not
  checked.
- **SC-009**: The plan feeds `/speckit-plan` by copying one printed invocation, with no edit to any core
  Spec Kit command or hook.
- **SC-010**: Re-running on a changed specification never destroys a prior not-covered decision without
  stating it.

## Assumptions

- The stated section structure follows the attached template example, adapted on two points the
  description settles: checkboxes are removed throughout, and the authoring-guidance table of optional
  sections stays in the template rather than the output.
- The command is invoked by its namespaced name; the description's `/test-plan` is shorthand. Principle
  III fixes the name as `speckit.spectra.test-plan`, and each agent renders its own invocation syntax.
- "The constitution (test strategy)" in the description means both the constitution and the document
  `speckit.spectra.test-strategy` writes; neither is a precondition for a useful run.
- The agent is optional and discovered through the roster. Nothing prompts for it, and a project that
  never installs it is unaffected.
- The extension version bump is MINOR: a command is added, none renamed or removed. The `spectra` CLI
  channel does not move.
- Stakeholder approval happens outside the document — in a review, a PR, or a meeting. The plan records
  the bar, not who cleared it.
- A `Manual` level remains available even where a test strategy omits it, because a test plan must be
  able to place a condition no automated lens will cover.
- Reading the specification creates no obligation to keep the plan in sync with it. A stale plan is
  refreshed by re-running the command, not by a watcher.
