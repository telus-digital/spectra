# Feature Specification: Test Strategy Agent

**Feature Branch**: `020-test-strategy-agent`

**Created**: 2026-09-10

**Status**: Implemented

**Input**: User description: "build a new command (agent) called `test-strategy` which will be a part
of the foundation phase. We would run this as a foundational agent (similar to constitution).
Scenario A: A greenfield project: in this case the agent will first see if there's an existing
documentation such tech stack, constitution, or anything else with which it can come up with a testing
strategy that makes sense. It should cover lenses such as E2E (e.g. using Playwright), integration
testing, API contracts, unit tests. It should also consider a test coverage floor. The agent will need
to provide a summary of what suggestions it may have, and produces an md file under `docs` folder
called `TEST_STRATEGY.md` this will outline the suggested strategy. Then the AI will prompt the user
that the strategy is ready. At that point, the AI will also check if the strategy is embedded in the
constitution as well, and if not it should prompt the user saying that if you're happy with the
strategy, let me know so I can amend the constitution ensuring that this is baked into every work
session, if not, modify, or let me know what you want to change and we can go from there. Scenario B:
A brownfield project. This is when SPECTRA is installed on a repo that is already established and has
source code + docs. Similar to above, but in this case the AI will actually consider the source code
and take that into account, and go from there. The rest remains the same."

## Clarifications

### Session 2026-09-10

Two of the description's decisions collide with Spectra's own constitution, and one of them was
already litigated on the previous document agent. What follows records what this spec settles, and
what it leaves open for the user.

- Q: The description says the two scenarios are greenfield and brownfield. Are these two commands, two
  modes, or one flow? → A: **One command, one flow, automatic detection.** Greenfield and brownfield
  are not a user-selectable mode; they are a fact about the repository the agent reads. The agent
  classifies the project itself (FR-006) and the two scenarios differ only in what evidence is
  available and therefore what the strategy can assert. Asking the user which kind of project they are
  in would be asking them for something the agent is about to measure anyway, and getting the wrong
  answer would produce a strategy grounded in nothing. The document states which mode ran, because a
  reader must be able to tell a strategy proposed for code that does not exist yet from one measured
  against code that does.

- Q: The description names Playwright for E2E. Does the agent recommend Playwright? → A: **Only where
  the project has a browser surface, and never as a default.** Principle IV makes context-awareness the
  feature: recommending Playwright to a Python CLI or a published library is exactly the generic
  template fill-in the principle exists to forbid. Playwright is the illustrative example for
  browser-facing projects, and the agent picks the end-to-end approach the project's actual surface
  admits — browser driver, HTTP-level journey test, CLI process test, or a stated finding that the
  project has no end-to-end surface worth automating (FR-016, FR-017).

- Q: The description says the agent produces `docs/TEST_STRATEGY.md`. Principle VII makes the artifact
  root **declarable** (`Artifact root: documents/`) with `docs/` only the default, and requires a
  publication check before defaulting into `docs/`. Which applies? → A: **Principle VII applies to the
  root.** Output resolves a declared root first, checks for the publication signal (`mkdocs.yml`,
  `docusaurus.config.*`, `docs/_config.yml`, `docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, or a
  Pages configuration pointing at `docs`) before defaulting, and takes the non-publishing option when
  the choice cannot be obtained (FR-041). This is not hypothetical for Spectra itself: this repository
  serves `main` `/docs` over GitHub Pages and carries `docs/index.html`, so a run here trips the check
  on the first try. What Principle VII *also* requires — a `<artifact>/` subfolder and an `NNN-` sequence
  number — is settled separately below, because a strategy is a singleton and the shipped document
  agents produce series.

- Q: Is the strategy document shaped by a registered template? → A: **Yes, in full, per Principle
  VIII.** It is a durable Markdown deliverable a human reads, so its structure ships as
  `spectra/templates/test-strategy-template.md`, declared in `provides.templates`, resolved through
  Spec Kit's four-layer stack with the command's inline skeleton as the last resort. The command
  reports the resolved path and honours the resolved template rather than repairing it (FR-035 to
  FR-038). A team that runs a different set of lenses changes one committed file and every future
  strategy follows.

- Q: Does the agent wire the coverage floor into CI, the test runner config, or a coverage tool? → A:
  **No. It recommends; it never configures.** The agent writes one document and, on explicit approval,
  one constitution amendment. It does not edit `package.json`, a coverage config, a CI workflow, or any
  test file (FR-045). Enforcement is a code change with a blast radius — a floor written into CI fails
  the next build — and the agent that proposes a policy is the wrong actor to enforce it silently. The
  document states the exact configuration change the team would make, so adopting it is a copy, not a
  research task.

- Q: What is the relationship to the roster's already-planned `test-coverage` and `test-automation`
  agents in the Testing & Quality phase? → A: **This agent decides the policy; those two would execute
  against it.** `test-strategy` runs once at foundation and answers "what should this project's testing
  look like and what floor does it hold"; a coverage analyst answers "where are we against it today"
  and an automation analyst answers "what should we automate next". This agent therefore produces no
  per-test findings, opens no test files for repair, and duplicates nothing `flaky-test-detector`
  already does (FR-046).

- Q: Can the agent run before a constitution exists? → A: **Yes, and it says what that costs.** The
  constitution is the strongest single input but it is not a precondition — a greenfield project may
  have nothing but a README and a dependency manifest. Where it is absent the agent produces the
  strategy from whatever evidence exists, and at the amendment step reports that there is no
  constitution to amend and names `/speckit-constitution` as the way to create one (FR-030).

- Q: What happens when the session cannot take an answer — a piped or non-interactive run? → A:
  **Write the document, skip the amendment, say so once.** The document is the deliverable and needs no
  approval; the constitution amendment requires explicit approval that a non-interactive session cannot
  give, and Principle VII's carve-out is conditioned on that approval. The run states up front that it
  detected a non-interactive session, writes the strategy, and reports the amendment as offered-but-not-
  applied with the exact text a human can apply later (FR-034).

- Q: Principle VII also requires an `<artifact>/` subfolder and an `NNN-` sequence number. A test
  strategy is a singleton, not a decision log — does it get a number? → A: **No. One file,
  `<artifact-root>/test-strategy/TEST_STRATEGY.md`, rewritten in place.** The subfolder and the
  declarable root are kept; the sequence number is not. A strategy is a living policy of the same kind
  as the constitution — there is exactly one current answer, and anything that links to it needs a
  stable path. Numbering exists so that `ADR-004` can supersede `ADR-002` without either losing its
  identity, which is a property of a decision log and not of a standing policy. Version history is
  Git's job here, not the filename's. This is a deliberate, narrow deviation from Principle VII —
  numbering only, with the root, the subfolder, the one-artifact-type rule, and the publication check
  all honoured — and the plan MUST carry it in Complexity Tracking rather than leave it implicit
  (FR-042, FR-042a).

- Q: Once the user approves the amendment, who writes it into the constitution? → A: **Not this agent.
  `/speckit-constitution` does.** The agent detects the gap, drafts the exact amendment in the
  constitution's voice, shows it, takes the approval, records it in the strategy document, and hands
  off — naming the invocation that applies it. It never edits `.specify/memory/constitution.md`, in any
  run, approved or not (FR-032, FR-032a). This is the `domain-analyzer` precedent, and the reason is
  that the amendment procedure is more than an append: it needs a sync impact report, a MAJOR / MINOR /
  PATCH judgement, and dependent templates and docs updated in the same change. A second command
  re-implementing that is a second thing to keep correct, and the failure mode is a constitution that
  is subtly malformed rather than one that is obviously broken. It costs the user one more command, and
  buys a single owner for every constitution edit.

  One consequence follows and is worth stating: because the approved amendment is recorded *in the
  strategy document*, the proposed-amendment section belongs to the registered template. A team whose
  override drops that section gets the amendment text in the session and a note that the section was
  omitted, per the honour-don't-repair rule — not a reinstated section (FR-036).

No questions remain open. Every marker raised during validation is settled above.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get a testing strategy before there is code to test (Priority: P1)

A tech lead has just stood up a repository. There is a README, a dependency manifest, maybe a
constitution and a plan — and no meaningful source. They run the agent. It reads what exists, works out
what the project is going to be, and proposes a testing strategy across the lenses that project will
actually need: unit, integration, API contract, end-to-end, and a coverage floor. It summarises the
proposal in the session, then writes it to a single Markdown document. Nothing about the strategy is
generic: every recommendation names the evidence behind it, and where there is no evidence it says the
recommendation is a convention rather than a finding.

**Why this priority**: this is the MVP and the reason a foundation-phase agent exists. Testing
decisions made after the code is written are migrations; made before, they are free. A greenfield
project is where a strategy has the most leverage and the least evidence, so the whole question is
whether the agent can be specific without inventing.

**Independent Test**: run the command in a repository containing only a README, a dependency manifest,
and a constitution, then verify the document names a concrete approach for every applicable lens, that
every recommendation carries either a cited evidence source or an explicit convention marker, and that
no tool is recommended that the declared stack cannot run.

**Acceptance Scenarios**:

1. **Given** a repository with documentation and dependency manifests but no substantial source,
   **When** the agent runs, **Then** it classifies the project as greenfield, states that classification
   in the document, and names the evidence that produced it.
2. **Given** the greenfield classification, **When** the document is read, **Then** it covers unit,
   integration, API contract, and end-to-end testing, plus a coverage floor, treating each as either
   applicable-with-an-approach or not-applicable-with-a-reason.
3. **Given** any recommendation in the document, **When** it is read, **Then** it either cites the
   project evidence it rests on or is explicitly marked as a convention-based default with no project
   evidence.
4. **Given** a declared stack with no browser surface, **When** the end-to-end lens is read, **Then** it
   does not recommend a browser driver, and names the end-to-end surface the project actually has or
   states that it has none.
5. **Given** the run completes, **When** the session output is read, **Then** a summary of the
   recommendations appears in the session before the user is asked anything.
6. **Given** the run finished, **When** the working tree is inspected, **Then** the only change is the
   new strategy document.

---

### User Story 2 - Get a strategy that starts from what the code already does (Priority: P1)

Spectra is installed on an eight-year-old service. The agent reads the source, not just the docs: which
test frameworks are actually wired up, which directories carry tests and which carry none, whether
coverage is measured at all and what it currently reports, what the CI workflow runs, and where the
untested surface is. The strategy it writes opens with what is true today and proposes a path from
there — a coverage floor set at or below the measured baseline with a stated ratchet, not an aspiration
that would fail the next build.

**Why this priority**: brownfield is the common case for an agent installed into an existing repository,
and it is where a generic strategy does the most damage. A document that ignores the 340 tests already
passing is not a strategy, it is a rewrite proposal. This story and Story 1 are the same deliverable
grounded in different evidence, so both are P1.

**Independent Test**: run the command in a repository with existing tests and a partially configured
coverage tool, then verify the document reports the current state per lens with file-path evidence,
that the proposed floor does not exceed the measured baseline, and that the ratchet has stated steps.

**Acceptance Scenarios**:

1. **Given** a repository with source code and existing tests, **When** the agent runs, **Then** it
   classifies the project as brownfield and the document reports the current testing state per lens
   before proposing anything.
2. **Given** existing test tooling, **When** the recommendations are read, **Then** they build on the
   frameworks already in use, and any proposal to replace one states the reason and the migration cost
   rather than simply naming a preferred tool.
3. **Given** a coverage figure the agent could measure or read from a committed report, **When** the
   floor is proposed, **Then** the floor is at or below that figure and the document states the
   measured baseline it came from.
4. **Given** coverage that cannot be measured because no tooling is configured, **When** the floor is
   proposed, **Then** the document says so, recommends the tooling as the first step, and makes the
   floor conditional on it rather than asserting a number.
5. **Given** a proposed floor below the intended long-term target, **When** the coverage section is
   read, **Then** it states a ratchet with concrete steps and the trigger for each increase.
6. **Given** an untested area the agent identified, **When** it appears in the document, **Then** it
   cites a path, and where the claim is that something is missing it cites what was searched and where.
7. **Given** the run completes, **When** the document's coverage-of-analysis statement is read, **Then**
   it says what portion of the repository was read and what it could not see.

---

### User Story 3 - Decide whether the strategy becomes policy (Priority: P1)

The document is written and the summary is on screen. The agent then checks whether this strategy is
already reflected in the project's constitution. Where it is not, it says so and offers the choice
plainly: approve it, and the agent drafts the exact amendment that would bake the strategy into every
future work session and hands it to `/speckit-constitution` to apply; change something first; or talk
through what is wrong with it. The agent itself never writes to the constitution — approved or not.

**Why this priority**: this is what makes it a *foundation* agent rather than a document generator. A
strategy that lives only in `TEST_STRATEGY.md` is advice; a strategy in the constitution is checked by
the Constitution Check gate on every plan. The user's description makes this the point of the whole
command, and it is the one place the agent reaches toward governance, so its gate has to be exact.

**Independent Test**: run the command in a project whose constitution has no testing principle, verify
the agent reports the absence and offers the three options, decline once and confirm nothing changed,
then approve and confirm the amendment text is recorded in the document and handed off — with the
constitution file itself byte-identical either way.

**Acceptance Scenarios**:

1. **Given** the document has been written, **When** the agent reports completion, **Then** it states
   where the document was written, which template shaped it, and summarises the recommendations before
   asking anything.
2. **Given** a constitution exists, **When** the agent checks it, **Then** it reports whether the
   strategy is already embedded, quoting the governing clause where it is.
3. **Given** the strategy is not embedded, **When** the agent prompts, **Then** it offers approving the
   amendment, modifying the strategy first, or discussing the changes — and it shows the exact
   amendment text before the user chooses.
4. **Given** the amendment text is shown, **When** it is read, **Then** it is written in the
   constitution's voice, names the section it targets, and states whether it adds a new principle or
   amends an existing one.
5. **Given** the user approves, **When** the run finishes, **Then** the amendment text is recorded in
   the strategy document and the agent names the `/speckit-constitution` invocation that applies it.
6. **Given** any run at all — approved, declined, or unanswered — **When** the working tree is
   inspected, **Then** `.specify/memory/constitution.md` is byte-identical to how the run found it.
7. **Given** the constitution already contains a testing principle that conflicts with a
   recommendation, **When** the agent reports, **Then** it surfaces the conflict as a finding and does
   not draft an amendment that silently overrides the existing principle.
8. **Given** no constitution exists, **When** the agent reaches the amendment step, **Then** it says
   there is nothing to amend and names the command that creates one, without creating one itself.
9. **Given** the user asks for a change to the strategy, **When** the agent revises, **Then** the
   document is updated in place, a fresh summary is given, and the same approval gate is offered again.

---

### User Story 4 - Re-run it when the project changes (Priority: P2)

A year in, the service has grown a second surface and the original strategy is stale. The tech lead
runs the agent again. It finds the existing strategy, treats it as the starting point rather than
noise, and reports what has changed since — lenses that were not applicable and now are, a baseline
that has moved, recommendations the project has since adopted or abandoned.

**Why this priority**: a foundation document that cannot be revisited becomes wrong quietly. It is not
MVP — the first run delivers the value — but a strategy nobody can refresh is a strategy nobody trusts
after the second quarter.

**Independent Test**: run the agent twice with a change to the project in between, and verify the
second run reports the prior strategy as an input, names what changed, and does not silently discard a
recommendation the team had adopted.

**Acceptance Scenarios**:

1. **Given** a strategy document already exists, **When** the agent runs, **Then** it reads it and
   records it as an input rather than ignoring it.
2. **Given** a prior recommendation the project has since implemented, **When** the new strategy is
   written, **Then** it is reported as adopted rather than re-proposed as new.
3. **Given** the coverage baseline has moved since the prior run, **When** the floor is proposed,
   **Then** the document states both figures and whether the ratchet advanced.
4. **Given** a prior strategy document exists, **When** the run finishes, **Then** that same file has
   been rewritten in place, no second strategy file has been created, and the run states what changed
   since the prior version.

---

### User Story 5 - Run it on a project with more than one stack (Priority: P3)

A monorepo holds a TypeScript front end, a Python service, and a shared library. One coverage floor and
one end-to-end recommendation cannot be right for all three. The agent identifies the distinct testable
surfaces and gives each its own lens treatment inside one document, with a shared section for what
genuinely applies repository-wide.

**Why this priority**: monorepos are common enough that a single-stack assumption produces a visibly
wrong document, but a single-stack project is still the majority case and gets full value without this.

**Independent Test**: run the agent in a repository with two distinct stacks and verify each surface
gets its own approach and floor, and that a recommendation is not applied across a surface it does not
fit.

**Acceptance Scenarios**:

1. **Given** a repository with multiple distinct testable surfaces, **When** the agent runs, **Then**
   the document treats each surface separately where the lenses differ.
2. **Given** distinct surfaces with different baselines, **When** floors are proposed, **Then** each
   surface carries its own floor rather than one repository-wide number.
3. **Given** a recommendation that applies to only one surface, **When** the document is read, **Then**
   its scope is stated and it is not presented as repository-wide policy.

---

### Edge Cases

- **The repository is empty or near-empty.** No manifests, no README, no constitution. The agent
  produces no strategy rather than a generic one, says exactly what it looked for and did not find, and
  names what would make a run useful.
- **`docs/` is published.** The project serves `docs/` over GitHub Pages, MkDocs, or Docusaurus. The
  publication check fires before the default is taken; where the choice cannot be obtained, the
  non-publishing location wins. Spectra's own repository is in this state.
- **The declared artifact root is unusable** — absolute, or containing `..`. The agent says so and
  falls back to the default rather than guessing or writing outside the project.
- **A constitution exists but has no testing content at all.** Not an error: this is the ordinary case
  the amendment step is built for.
- **A constitution's testing principle contradicts the evidence** — it mandates 90% coverage in a
  repository measuring 31%. The gap is a finding in its own right; the agent reports it rather than
  proposing a strategy that pretends the principle is being met.
- **Tests exist but do not run** — a framework is configured, the suite is broken or excluded from CI.
  The agent reports tests-present-but-not-executing as distinct from tests-absent, because the remedies
  are different.
- **A coverage report is committed but stale.** The figure is used with its date stated, and it is
  labelled as read-from-a-report rather than measured.
- **The agent cannot search the repository's full text.** Coverage of the analysis degrades loudly: the
  document states the reduced coverage rather than silently narrowing what it examined.
- **A template override drops the proposed-amendment section.** The agent notes the omission and gives
  the amendment text in the session rather than reinstating the section — the template is honoured, not
  repaired, and the handoff still happens.
- **The strategy document exists but is not writable**, or the artifact root cannot be created. The
  agent reports the failure and outputs the strategy in the session rather than writing it elsewhere.
- **The session is non-interactive.** The document is written, the amendment is drafted in text and
  left unapproved, and both facts are stated.
- **The user asks for a change that contradicts the evidence** — dropping integration tests on a service
  whose logic is mostly at the boundaries. The change is made as instructed and the disagreement is
  recorded in the document rather than argued in the session.

## Requirements *(mandatory)*

### Functional Requirements

#### Identity and registration

- **FR-001**: The capability MUST ship as a single command file under `spectra/commands/`, registered
  in `spectra/extension.yml` under `provides.commands`, in the one self-contained `spectra/` extension.
- **FR-002**: The command MUST be named `speckit.spectra.test-strategy` and MUST begin with YAML front
  matter containing a `description`.
- **FR-003**: The command MUST be agent-agnostic, taking user input through `$ARGUMENTS` and hard-coding
  no single agent's invocation syntax.
- **FR-004**: The command MUST run with no arguments. Supplied arguments MUST be treated as a focus hint
  that weights the analysis without narrowing the mandatory lenses.
- **FR-005**: The agent MUST be registered in `agents-list.json` in the `foundation` phase with
  `provider: spectra` and `type: add-on`, and every generated listing MUST be regenerated from it.

#### Classifying the project

- **FR-006**: The agent MUST classify the project as greenfield or brownfield from evidence it reads,
  MUST NOT ask the user which it is, and MUST state the classification and its evidence in the document.
- **FR-007**: Classification MUST rest on the presence and volume of source and tests, not on repository
  age or commit count.
- **FR-008**: Where the evidence is mixed — substantial source with no tests, or scaffolding only — the
  agent MUST state which signals pointed each way rather than presenting a clean classification.

#### Reading context

- **FR-009**: Before proposing anything, the agent MUST read, where present: the constitution under
  `.specify/memory/`, specifications under `specs/`, `README*`, `CONTRIBUTING*`, documentation
  directories, dependency manifests, test framework and coverage configuration, CI workflow definitions,
  and existing test directories.
- **FR-010**: In brownfield mode the agent MUST additionally read source code to establish what is
  tested and what is not, and MUST NOT derive the current state from documentation alone.
- **FR-011**: The agent MUST record every input it consulted, and MUST record by name and reason any
  input it expected and could not read.
- **FR-012**: Where a prior strategy document exists, the agent MUST read it and treat it as an input.
- **FR-013**: The agent MUST state what portion of the repository it read and what it could not see.
  Where its search capability is reduced, it MUST say so rather than narrowing silently.

#### The lenses

- **FR-014**: The strategy MUST cover, at minimum, unit testing, integration testing, API contract
  testing, and end-to-end testing, and MUST treat each as either applicable — with a named approach — or
  not applicable, with a stated reason.
- **FR-015**: The agent MUST add any further lens the project's evidence warrants, and MUST justify each
  addition from that evidence.
- **FR-016**: Every tool the agent names MUST be one the project's actual stack can run. The agent MUST
  NOT recommend a tool whose prerequisites the project does not have.
- **FR-017**: The end-to-end lens MUST be matched to the project's real surface — browser, HTTP, CLI, or
  none — and MUST NOT default to a browser driver.
- **FR-018**: In brownfield mode each lens MUST report the current state with cited evidence before it
  proposes a change.
- **FR-019**: A recommendation to replace an existing tool MUST state the reason and the migration cost.
- **FR-020**: The document MUST state what each lens is responsible for proving and where its boundary
  with the adjacent lenses lies, so a team can tell which lens a given behaviour belongs to.

#### The coverage floor

- **FR-021**: The strategy MUST propose a coverage floor, MUST state the metric it is measured in, and
  MUST state how it would be measured on this project.
- **FR-022**: In brownfield mode the proposed floor MUST NOT exceed the measured or reported baseline,
  and the document MUST state the baseline it came from.
- **FR-023**: Where coverage cannot be measured, the agent MUST say so, MUST recommend the tooling that
  would make it measurable, and MUST make the floor conditional rather than asserting a number.
- **FR-024**: Where the floor is below the intended target, the document MUST state a ratchet with
  concrete steps and the trigger for each increase.
- **FR-025**: The document MUST state what the floor does and does not prove, so it is not read as a
  quality guarantee.
- **FR-026**: A coverage figure read from a committed report MUST be labelled as such and carry the
  report's date; only a figure the agent produced by running measurement may be called measured.
- **FR-027**: Where the project has distinct testable surfaces with different baselines, each surface
  MUST carry its own floor.

#### Reporting and the approval gate

- **FR-028**: After writing the document, the agent MUST summarise its recommendations in the session,
  and MUST state where the document was written and which template shaped it, before asking the user
  anything.
- **FR-029**: The agent MUST determine whether the strategy is already embedded in the constitution, and
  MUST report the result, quoting the governing clause where one exists.
- **FR-030**: Where no constitution exists, the agent MUST report that there is nothing to amend and
  name the command that creates one. It MUST NOT create a constitution.
- **FR-031**: Where the strategy is not embedded, the agent MUST offer three paths — approve the
  amendment, modify the strategy first, or discuss the changes — and MUST show the exact amendment text
  before the user chooses.
- **FR-032**: The agent MUST NOT write to `.specify/memory/constitution.md` under any circumstance.
  Approval authorises drafting and handoff, never a direct edit, and every run MUST leave the
  constitution byte-identical to how it found it.
- **FR-032a**: On approval the agent MUST record the amendment text in the strategy document's
  proposed-amendment section and MUST name the `/speckit-constitution` invocation that applies it.
  Satisfying the project's amendment procedure — the sync impact report, the version bump, and the
  dependent templates and docs updated in the same change — is that command's responsibility, not this
  agent's.
- **FR-032b**: The drafted amendment MUST be written in the constitution's voice, MUST name the section
  it targets, and MUST state whether it adds a new principle or amends an existing one, so the handoff
  is actionable without re-deriving it.
- **FR-033**: Where an existing constitution principle conflicts with a recommendation, the agent MUST
  surface the conflict and MUST NOT draft an amendment that silently overrides it.
- **FR-034**: In a non-interactive session the agent MUST detect the condition, state it once, write the
  document, and report the amendment as drafted-but-not-approved with its exact text, taking no
  approval it was not given.
- **FR-035**: Where the user asks for changes, the agent MUST revise the document in place,
  re-summarise, and re-offer the same approval gate.
- **FR-036**: Where the resolved template omits the proposed-amendment section, the agent MUST note the
  omission and give the amendment text in the session rather than reinstating the section, and the
  handoff MUST still be offered.

#### The document

- **FR-037**: The agent MUST write exactly one Markdown strategy document per run. A re-run MUST rewrite
  that same file in place, MUST NOT create a second strategy file, and MUST state what changed since the
  version it replaced.
- **FR-038**: The document's structure MUST come from a template shipped under `spectra/templates/` as
  `test-strategy-template.md`, registered in `spectra/extension.yml` under `provides.templates`.
- **FR-039**: The template MUST be resolved through Spec Kit's stack — project overrides, then preset,
  then extension, then core templates, then the command's inline skeleton — taking the first readable,
  non-empty layer. The command MUST NOT hard-code a single template path.
- **FR-040**: The agent MUST honour the resolved template's sections and their order, MUST NOT add,
  rename, or reorder them, and MUST note rather than reinstate a section the template omits.
- **FR-041**: The agent MUST report the resolved template path in the session.
- **FR-042**: The document MUST be written to `<artifact-root>/test-strategy/TEST_STRATEGY.md`. The
  agent MUST resolve a declared artifact root where one is declared, MUST perform the publication check
  before defaulting into `docs/`, MUST take the non-publishing option where the choice cannot be
  obtained, and MUST fall back to the default with a stated reason where a declared root is unusable.
- **FR-042a**: The filename MUST carry no sequence number. This is a deliberate deviation from Principle
  VII's numbering rule on the grounds that a strategy is a standing policy with exactly one current
  version, and the plan MUST record it in Complexity Tracking. Every other part of Principle VII — the
  declarable root, the dedicated subfolder, one artifact type per subfolder, and the publication check —
  MUST be honoured.
- **FR-043**: Every recommendation MUST either cite the project evidence it rests on or be explicitly
  marked as a convention-based default with no project evidence.
- **FR-044**: A finding that something is absent MUST cite what was searched and where, rather than
  being omitted for lack of a citable line.
- **FR-045**: The document MUST state which mode ran — greenfield or brownfield — and what evidence
  produced that classification.
- **FR-046**: Where the user directs a change that contradicts the evidence, the document MUST record
  the disagreement alongside the change.

#### Scope boundaries

- **FR-047**: The agent MUST NOT modify source code, test files, test framework configuration, coverage
  configuration, or CI workflow definitions. Where it recommends such a change it MUST state the exact
  change for the team to apply.
- **FR-048**: The strategy document is the only file the agent writes, in every run.
- **FR-049**: The agent MUST NOT produce per-test findings, diagnose individual failing or flaky tests,
  or open test files for repair.
- **FR-050**: The agent MUST make no network request and MUST accept no repository URL.

#### Publishing obligations

- **FR-051**: The change MUST bump `extension.version` in `spectra/extension.yml`, mirror it in
  `catalog.json` along with the command count, and add a matching `spectra/CHANGELOG.md` entry.
- **FR-052**: The change MUST rebuild `docs/packages/spectra.zip`, update `docs/index.html`, regenerate
  every structured agent listing from `agents-list.json`, and add the hand-written per-agent prose block
  the new agent requires.
- **FR-053**: The change MUST NOT bump the CLI's `VERSION`, create a Git tag, or publish a GitHub
  Release.

### Key Entities

- **Project classification** — greenfield or brownfield, with the signals that produced it and any
  signals that pointed the other way. Determines what the strategy may assert.
- **Testable surface** — a distinct part of the repository with its own stack and its own testing needs.
  A single-stack project has one; a monorepo has several. Each carries its own lens treatment and floor.
- **Lens** — one testing concern (unit, integration, API contract, end-to-end, or a project-warranted
  addition), holding an applicability verdict, a current state where one exists, a recommended approach,
  the tools that approach implies, and the evidence behind it.
- **Coverage floor** — a metric, a proposed value, the baseline it was derived from, how that baseline
  was obtained, the ratchet steps toward the target, and a statement of what the floor does not prove.
- **Recommendation** — a single proposed change, carrying its lens, its scope, its evidence citation or
  convention marker, and its adoption state on a re-run.
- **Strategy document** — the durable Markdown deliverable, shaped by the resolved template, holding the
  classification, the surfaces, the lenses, the floor, the coverage-of-analysis statement, and the
  inputs consulted.
- **Constitution amendment draft** — the exact proposed text in the constitution's voice, the section it
  targets, whether it adds or amends a principle, whether the strategy is already embedded, any conflict
  found with an existing principle, its approval state, and the handoff invocation that would apply it.
  Drafted and recorded by this agent; applied by another.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A team can go from installing Spectra to having a written, project-specific testing
  strategy in a single command invocation with no arguments.
- **SC-002**: Every recommendation in a produced document is traceable: a reader can open the cited
  evidence and find it, or see that the recommendation is marked as a convention with no project
  evidence. Zero unmarked, unevidenced recommendations.
- **SC-003**: In a brownfield project, the proposed coverage floor never exceeds the baseline the
  document reports, so adopting the floor as written does not fail the project's next build.
- **SC-004**: No document recommends a tool the project's stack cannot run, across a sample of at least
  four projects of different stacks including one with no browser surface.
- **SC-005**: The constitution is byte-identical after every run of the agent, including runs where the
  user approved the amendment.
- **SC-006**: A reader can tell, from the document alone, which mode ran, how much of the repository was
  examined, and what the analysis could not see.
- **SC-007**: A team that overrides the template gets a document in their own structure without editing
  anything inside the extension tree.
- **SC-008**: Re-running the agent on an unchanged project reports the prior strategy as an input,
  re-proposes nothing the project has already adopted, and leaves exactly one strategy file on disk.
- **SC-009**: A user who approves the amendment can apply it by running one named command against the
  strategy document, with no part of the amendment text re-derived by hand.

## Assumptions

- The agent runs inside a Spec Kit project with Spectra installed; the constitution, specs, and templates
  are read from their standard locations.
- Greenfield and brownfield are ends of a spectrum rather than a binary; the classification is a
  reported judgement with its evidence, not a guarantee, and a mixed project is described as mixed.
- The agent has read access to the repository and whatever full-text search the host agent provides. It
  does not require ripgrep or any other named tool, and it degrades loudly where search is unavailable.
- Running the project's test suite or coverage tool is permitted but not assumed. Where the agent cannot
  execute measurement it reads committed reports and configuration, labels the figure accordingly, and
  says a baseline was not measured.
- Coverage floors are expressed in whatever metric the project's tooling reports; line coverage is the
  fallback where nothing is configured, because it is the metric every mainstream tool produces.
- Playwright is treated as an illustrative example for browser-facing projects, not a default. The
  description named it as an example and the constitution's context-awareness principle forbids
  applying it blind.
- The `test-coverage` and `test-automation` agents already on the roadmap will execute against this
  strategy rather than restate it; this spec claims no part of their scope.
- `/speckit-constitution` is available to apply an approved amendment and owns the amendment procedure —
  the documented change, the version bump, and the dependent artifacts updated together. This agent
  depends on it for the final step but does not invoke it automatically; the user runs it.
- Git, not the filename, carries the strategy's version history. The singleton is rewritten in place and
  prior versions are recoverable from the repository.
- This work bumps the catalog channel only. The `spectra` CLI is untouched.
