# Feature Specification: An Engineering Methodology Agent That Feeds the Constitution

**Feature Branch**: `035-engineering-methodology-agent`

**Created**: 2026-10-24

**Status**: Implemented

**Input**: User description: "Add a new Spectra agent, `speckit.spectra.methodology`, that helps a team find,
choose and record its engineering methodology. It writes `ENGINEERING_METHODOLOGY.md` and hands its
Constitution input section to `/speckit.constitution`, so the team's methodology becomes binding through the
Constitution Check. It is a sibling of `speckit.spectra.domain-analyzer` and `speckit.spectra.test-strategy`
and follows their shape. It works on greenfield and brownfield projects, works nine lenses, treats SDD as the
fixed base with TDD, BDD/ATDD, DDD, contract-first and ADR-driven as optional overlays that enter the
constitution only as phase-bound obligations, hands testing, deployment, product technology and DDD content to
their sibling agents, and takes over the domain analyzer's Delivery & workflow lens. Its document is
onboarding-grade, modelled on a team's hand-written engineering methodology document, and ends with a Constitution input
section and a Decisions and sources section."

## Current State (verified against extension 1.23.0)

| Question | Spectra at 1.23.0 |
|---|---|
| Can a team record *how it works* (modes, branching, review, commits, AI rules) as a guardrail? | **Only partly**, through `speckit.spectra.domain-analyzer` lens 7 "Delivery & workflow", which offers at most five candidates in one question. There is no document a new engineer could onboard from. |
| Can a team declare it works test-first, behaviour-first, or domain-first? | **No.** Nothing asks, and nothing turns such a choice into an obligation that `/speckit.plan`'s Constitution Check could enforce. Spec Kit's tasks template already supports test-first ordering, but only as an option nobody is prompted to make binding. |
| Is there a guided path for a brownfield team adopting Spectra? | **For domain, testing and deployment, yes; for methodology, no.** A team's branching model, review gates and commit conventions are found only if the domain analyzer happens to propose them. |
| Is there one source per constitution clause? | **Not for workflow once this agent exists**, unless the domain analyzer stops proposing Delivery & workflow guardrails. Two sources for one clause is how a constitution contradicts itself. |

## Clarifications

### Session 2026-10-24

- Q: When a team adopts test-first (TDD) at MUST, how should "a failing test is observed before implementation" be evidenced? → A: In `tasks.md` — each implementation task names its test task, and the test task records that it was run and failed before the implementation task is ticked.
- Q: Should the agent's final report guide the team through the other constitution-feeding agents? → A: Yes — after its own `/speckit-constitution` line, the report lists sibling agents whose documents do not exist yet, in the suggested order domain-analyzer → methodology → test-strategy → deployment-strategy; each agent keeps its own handoff line, and no sibling's input is folded into this one.
- Q: What makes a project brownfield rather than greenfield? → A: Three signals — application source code beyond scaffolding; workflow configuration (CI, PR template, CODEOWNERS, CONTRIBUTING); more than 10 commits. Two or more → brownfield; none → greenfield; exactly one → mixed, so the agent states its reading and asks.
- Q: How should lens 8 treat how much AI agents may do without a human between phases? → A: Offer three named autonomy levels — every phase a human checkpoint (recommended by default); human gates at spec approval and PR review only; autonomous through to PR — citing brownfield evidence where present.
- Q: How should strictness and scope be asked when several overlays are adopted? → A: In one question (question 2) presenting a table with a proposed strictness and scope per adopted overlay; options are accept all, make all SHOULD, choose per row, and Skip; free text adjusts any row.
- Q: What happens when a hand-written `ENGINEERING_METHODOLOGY.md` already sits at the canonical path? → A: It is read as evidence of current practice and replaced only with the team's consent before the round; otherwise, and always when non-interactive, nothing is written and the document is shown in the session. No `.proposed` or other second file is written.
- Q: How does an adopted overlay count against the five-candidate cap per lens? → A: Each adopted overlay is one candidate whose statement lists its phase obligations, so lens 1 stays within FR-008's cap of five.
- Q: How is lens 8's question shaped, given the three autonomy levels exclude each other? → A: Question 9 offers the three autonomy levels plus Skip; the lens's tools and secrets candidates ride with the chosen level unless free text excludes them.
- Q: How is ground split with `deployment-strategy`, `kb-vault` and `review-pr`? → A: Lens 7 covers commit convention and changelog only; the versioning scheme, release cut and hotfix promotion belong to `deployment-strategy`, which stops proposing the branching model; `kb-vault` routes an absorbed methodology to `ENGINEERING_METHODOLOGY.md`; `review-pr` reads it as a standard, accepted guardrails only.
- Q: Which constitution section does lens 8 feed by default? → A: Additional Constraints.
- Q: What counts as "application source beyond scaffolding" for mode detection? → A: At least one source file with more than 20 non-blank lines changed in more than one commit, or at least five such files when the history has at most one commit (including no history), so a squashed import still counts and reads as mixed when no other signal is present.
- Q: What does `kb-vault` do when absorbed methodology content would update an `ENGINEERING_METHODOLOGY.md` this agent wrote? → A: It leaves the file unchanged, names `/speckit.spectra.methodology` as the way to fold the content in, and lists the absorbed source among the items it referred on; a file at that path without `command: speckit.spectra.methodology` front matter is hand-written and takes kb-vault's existing update rules.
- Q: Should the spec name a reference project for the document's shape or for SC-006? → A: No. The reference is a team's hand-written engineering methodology in general, and SC-006 is measured on any brownfield repository that keeps one at the canonical path.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Record a brownfield team's methodology and hand it to the constitution (Priority: P1)

A tech lead adopting Spectra on an existing codebase runs `speckit.spectra.methodology`. Before anything else
the agent says it detected a **brownfield** project and why (for example: 400 commits, branch history, a CI
workflow, a PR template), and whether a constitution exists — so whether the goal is to **create** or
**update** it. It reads the repository, then works nine lenses. For each lens it first reports the team's
current practice with citations, then proposes candidate guardrails tagged `observed` (the team already does
this) or `aspirational` (it does not yet). The lead answers a fixed round of questions in the session. Only
then does the agent write `<artifact-root>/ENGINEERING_METHODOLOGY.md` — a document a new engineer could
onboard from — ending with a Constitution input section holding exactly the accepted guardrails, and a
ready-to-paste `/speckit-constitution` line.

**Why this priority**: This is the feature's purpose. The user's typical run is a brownfield project being
initialised on Spectra, and the methodology only becomes binding once it reaches the constitution.

**Independent Test**: Run the agent on a repository with branch history, a CI workflow and a PR template;
answer every question; confirm no file exists until the last answer, then that the document reports current
practice per lens with citations, records every answer, and its Constitution input section holds exactly the
accepted guardrails.

**Acceptance Scenarios**:

1. **Given** a repository with commit history and workflow configuration, **When** the run starts, **Then**
   the first output names the detected mode (`brownfield`) with the evidence behind it, and states whether a
   constitution was found and whether the goal is to create or update it.
2. **Given** any lens in brownfield mode, **When** it is presented, **Then** its current practice is stated
   with at least one cited project file or git fact before any candidate is proposed.
3. **Given** a lens with nothing to propose, **When** it is presented, **Then** it says what was searched and
   why there is nothing to propose; it is never omitted.
4. **Given** any candidate guardrail, **When** it is presented or recorded, **Then** it is tagged `observed` or
   `aspirational` and, in brownfield mode, cites its evidence.
5. **Given** the round has not ended, **When** fewer than all questions are answered, **Then** no document has
   been written.
6. **Given** the round ends with at least one accepted guardrail, **When** the agent reports, **Then** it gives
   one ready-to-paste `/speckit-constitution` line worded for the goal (create or update) and does not invoke
   it.
7. **Given** some sibling documents do not exist yet, **When** the agent reports, **Then** after its own
   `/speckit-constitution` line it lists those siblings in the suggested order, and its own line carries only
   this agent's accepted guardrails.

---

### User Story 2 - Choose a methodology stack on top of SDD, as enforceable obligations (Priority: P1)

The lead's team wants to work test-first. In the methodology-stack question the agent states that spec-driven
development is the fixed base, lists the compatible overlays — at least TDD, BDD/ATDD, DDD, contract-first /
API-first, and ADR-driven — says which ones the repository already shows evidence of, and recommends a stack.
For every overlay the team adopts, the agent then asks how strict it is (MUST or SHOULD) and how wide it
reaches (which change types and which modules). Each adopted overlay is recorded as concrete obligations
attached to spec-kit phases — specify, plan, tasks, implement — never as a slogan. Adopting TDD, for example,
yields: test tasks are ordered before, and block, the implementation tasks they cover; a failing test is
observed before implementation; a bug fix starts with a failing regression test.

**Why this priority**: This is the user's ultimate goal — that a team's chosen methodologies become part of the
constitution in a form the Constitution Check can enforce, so AI agents actually work test-first (or
behaviour-first, or contract-first) rather than being told to.

**Independent Test**: Run the agent, adopt TDD at MUST for features and fixes, and confirm the document's
methodology → phase obligations matrix and the Constitution input section each state TDD's obligations per
phase with that strictness and that scope.

**Acceptance Scenarios**:

1. **Given** any run, **When** the methodology stack is presented, **Then** SDD is stated as the base and is not
   offered as optional, and at least TDD, BDD/ATDD, DDD, contract-first/API-first and ADR-driven are offered as
   overlays.
2. **Given** brownfield evidence for an overlay (test commits preceding or accompanying code, `.feature` files or
   BDD dependencies, a glossary or context-aligned module layout, contracts committed ahead of handlers, an
   `adr/` directory), **When** the overlay is offered, **Then** the evidence is cited and the overlay is marked
   as already practised.
3. **Given** an overlay is adopted, **When** it is recorded, **Then** it carries a strictness (MUST or SHOULD), a
   scope (change types and, where given, modules), and at least one obligation tied to a named spec-kit phase;
   an implementation-time obligation states its evidence in `tasks.md` (the test task records its failing run
   before the implementation task it blocks is ticked).
4. **Given** an overlay is adopted that the code does not yet follow (e.g. TDD on a codebase with little test
   coverage), **When** its default scope is proposed, **Then** it is scoped to new and changed code and tagged
   `aspirational`, never claimed for the existing codebase.
5. **Given** the team names a process cadence (Scrum, Kanban, Shape Up), **When** the document is written,
   **Then** the cadence may appear in the human-facing body but never in the Constitution input section.
6. **Given** two adopted overlays whose obligations would conflict at the same phase, **When** they are
   recorded, **Then** the conflict is reported and the team is asked which takes precedence before the
   document is written.

---

### User Story 3 - Stay inside its own ground, and take over the domain analyzer's workflow lens (Priority: P1)

The agent works only its nine lenses. Where evidence touches ground a sibling agent owns, it cites that
sibling's document if it exists, or names the command that writes it, and proposes nothing there: test levels,
coverage floors, UAT and the ratchet go to `speckit.spectra.test-strategy`; environments, promotion,
rollback, the versioning scheme, release cut and hotfix promotion go to `speckit.spectra.deployment-strategy`; product languages, frameworks and dependency policy go
to `speckit.spectra.domain-analyzer`; DDD content — bounded contexts, invariants, glossary terms — goes to
`speckit.spectra.domain-analyzer`, while this agent records only the commitment to work domain-first. In the
same change, `speckit.spectra.domain-analyzer` stops proposing Delivery & workflow guardrails and hands that
ground to this agent; `speckit.spectra.deployment-strategy` stops proposing the branching model;
`speckit.spectra.kb-vault` routes an absorbed methodology to the same file; and `speckit.spectra.review-pr`
reads it as a standard.

**Why this priority**: The constitution receives input from four agents. If two of them propose the same
clause, the constitution can contradict itself, and the Constitution Check becomes unreliable.

**Independent Test**: Run this agent on a repository with a coverage configuration and a deployment workflow,
then run the domain analyzer on the same repository; confirm neither produces a candidate in the other's
ground, and that each cites or names the sibling that owns it.

**Acceptance Scenarios**:

1. **Given** evidence of coverage thresholds, test levels, environments or rollback, **When** lenses are
   worked, **Then** no candidate is proposed in that ground and the owning sibling's document or command is
   named.
2. **Given** TDD is adopted, **When** its obligations are recorded, **Then** they govern *when* tests are
   written relative to code, and say nothing about test levels or coverage floors, which are referred to
   `speckit.spectra.test-strategy`.
3. **Given** DDD is adopted, **When** it is recorded, **Then** the obligations reference the domain's
   ubiquitous language and contexts without defining them, and the domain analysis is cited or its command
   named.
4. **Given** the AI collaboration lens, **When** tools are recorded, **Then** only AI assistants and
   development-workflow tooling are covered, never the product's languages or frameworks.
5. **Given** the updated domain analyzer runs, **When** its lenses are worked, **Then** it has no Delivery &
   workflow lens and no question for it, and it names `speckit.spectra.methodology` for that ground.
6. **Given** a `DOMAIN_ANALYSIS.md` written by an earlier version with Delivery & workflow decisions, **When**
   either agent re-runs, **Then** those prior decisions are preserved as a record, never deleted, and this
   agent reads them as prior answers for the matching lenses.
7. **Given** the updated deployment strategist runs, **When** it works its release lens, **Then** it proposes
   nothing on the branching model and cites `ENGINEERING_METHODOLOGY.md` or names `speckit.spectra.methodology`.
8. **Given** a pull request is reviewed in a project with an `ENGINEERING_METHODOLOGY.md`, **When**
   `speckit.spectra.review-pr` cites it, **Then** only guardrails whose decision is `accepted` are raised.
9. **Given** an `ENGINEERING_METHODOLOGY.md` written by this agent, **When** `speckit.spectra.kb-vault` absorbs
   a methodology source, **Then** the file is left unchanged, `/speckit.spectra.methodology` is named as the
   way to fold the content in, and the source is listed among the items kb-vault referred on.

---

### User Story 4 - Shape a methodology for a greenfield project (Priority: P2)

A team starting a new project runs the agent. It detects **greenfield** — no meaningful history, no workflow
configuration — and says so. Since there is no current practice to report, each lens becomes a short
interview: the agent proposes sensible defaults (for example trunk-based development with short-lived
branches, squash merges, Conventional Commits, one approval per PR), every candidate tagged `aspirational`,
and the team accepts, adjusts or skips them in the same fixed round.

**Why this priority**: The user wants both. Greenfield is less common for a team initialising Spectra, but
it is where a methodology is cheapest to set.

**Independent Test**: Run the agent in an empty repository and confirm the mode is reported as greenfield,
every lens offers defaults, and the document is produced with every candidate tagged `aspirational`.

**Acceptance Scenarios**:

1. **Given** a repository with no source code beyond scaffolding, no workflow configuration and at most 10
   commits, **When** the run starts, **Then** the first output names the mode `greenfield` and the signals it
   checked.
2. **Given** greenfield mode, **When** a lens is presented, **Then** it states that there is no current
   practice to report and offers default candidates instead, each tagged `aspirational`.
3. **Given** a repository showing exactly one of the three signals (e.g. source code imported with squashed
   history and no workflow configuration),
   **When** the mode is detected, **Then** the agent states its reading and the alternative and lets the team
   correct it before lenses are presented.

---

### User Story 5 - Re-run safely and run non-interactively (Priority: P2)

The team re-runs the agent months later. It rewrites the same `ENGINEERING_METHODOLOGY.md`. Every question
offers the previous answer as its proposed answer, declined guardrails are not offered again as new,
guardrails keep their IDs, and accepted guardrails the constitution now carries are marked adopted and leave
the Constitution input section. In a non-interactive run — declared by flag or by the user, never inferred —
no question is asked, the document records every candidate as `not_asked`, and nothing is handed to the
constitution.

**Why this priority**: Methodologies evolve, and teams re-run after changing. Re-proposing a declined rule, or
handing an adopted rule back to the constitution, erodes trust. Non-interactive mode serves CI and scripted
setup.

**Independent Test**: Run twice, adopting some guardrails through `/speckit-constitution` in between; confirm
the second run's prefilled answers, declined suppressions and adopted markings. Run once non-interactively and
confirm no question was asked and the Constitution input section is empty.

**Acceptance Scenarios**:

1. **Given** a prior document, **When** a question is asked, **Then** the prior answer is offered as its
   proposed answer.
2. **Given** a candidate declined last run, **When** the same guardrail is regenerated, **Then** it is not
   offered as new and the question says how many were declined before.
3. **Given** an accepted candidate the constitution now asserts, **When** the re-run completes, **Then** it is
   marked `adopted: <principle>` and is absent from the Constitution input section.
4. **Given** a non-interactive run, **When** it completes, **Then** no question was asked, every candidate is
   `not_asked`, the Constitution input section says nothing was accepted, and no `/speckit-constitution` line is
   given.

---

### Edge Cases

- **A reply that is not an answer** (a question back, a request to explain an overlay): the agent answers it and
  asks the same question again; the round does not advance.
- **"Use your defaults"**: the recommended option is taken for every remaining question and recorded as
  `default_taken`; those candidates are accepted like any other answer.
- **An unanswered or skipped question**: adopts nothing; this governs the constitution, so silence is not
  consent.
- **No overlay adopted**: the strictness-and-scope question becomes a confirmation that keeps its number; the
  obligations matrix shows SDD alone.
- **An overlay's evidence is contradictory** (e.g. `.feature` files exist but none run in CI): it is reported as
  partially practised, and the candidate is `aspirational` for the part not yet true.
- **An existing constitution already states a methodology rule**: the matching candidate is suppressed, or
  marked `amends: <principle>` when it would change it.
- **The team's practice contradicts its written docs** (CONTRIBUTING.md says squash-merge; history shows merge
  commits): both are reported, the history is treated as current practice, and the question asks which to
  codify.
- **The default `docs/` folder is published** (Pages, MkDocs, Docusaurus signals): the team chooses the folder
  before the round; where no choice can be obtained, the non-publishing folder is used.
- **A project template override omits the Constitution input section**: the section is written anyway and the
  omission reported, since without it nothing can be handed off.
- **The file cannot be written**: the failure is reported and the document is shown in the session instead.
- **A hand-written methodology already sits at the canonical path** (e.g. a team's own `docs/ENGINEERING_METHODOLOGY.md`,
  or one `speckit.spectra.kb-vault` absorbed): it is read as evidence of current practice; it is replaced only
  with the team's consent before the round; otherwise, and always when non-interactive, nothing is written and
  the document is shown in the session.
- **`speckit.spectra.kb-vault` absorbs a methodology source while this agent's file exists**: kb-vault does not
  update the file; it names `/speckit.spectra.methodology` and reports the source as referred on, so the
  command-owned front matter and frozen IDs survive (FR-019, FR-025).
- **A sibling document exists but contradicts a methodology candidate** (e.g. the test strategy exempts fixes
  from tests while TDD at MUST covers fixes): the conflict is reported; this agent does not edit the sibling.
- **Lens 9 overlaps the project's existing constitution Governance section**: the existing section's rules are
  reported as current practice; nothing is proposed that it already asserts.

## Requirements *(mandatory)*

### Functional Requirements

**Run setup**

- **FR-001**: The agent MUST state, as its first output, the detected mode (`brownfield` or `greenfield`) with
  the evidence behind it, and whether a constitution was found and therefore whether the goal is to **create**
  or **update** it.
- **FR-002**: The agent MUST detect mode from three signals: (a) application source beyond scaffolding — at
  least one source file with more than 20 non-blank lines changed in more than one commit, or at least five such
  files when the history has at most one commit (including no history), so a squashed import still counts; (b) workflow configuration — CI workflows, a PR template, CODEOWNERS, or CONTRIBUTING, (c) more than 10
  commits. Two or more signals mean `brownfield`; none means `greenfield`; exactly one is a mixed reading, for
  which the agent MUST state its reading and the alternative and MUST accept the team's answer before
  presenting lenses. The first output MUST name which signals were found.
- **FR-003**: The agent MUST read the project before proposing anything — including, where present, commit
  history and branch names, PR and issue templates, CODEOWNERS, CI workflows, commit-lint, changelog and
  release configuration, CONTRIBUTING.md, existing spec artifacts, the constitution, and sibling documents
  (`TEST_STRATEGY.md`, `DOMAIN_ANALYSIS.md`, `DEPLOYMENT_STRATEGY.md`).

**Lenses**

- **FR-004**: The agent MUST work all nine lenses on every run — Methodology stack; Work modes &
  classification; Requirements intake; Spec lifecycle & traceability; Branching & integration; Review & merge
  gates; Change records; AI collaboration rules; Governance & evolution — and MUST NOT omit one. A lens with
  nothing to propose MUST say what was searched and why. Lens 7 (Change records) covers the commit convention
  and the changelog only; the versioning scheme is referred (FR-018).
- **FR-005**: Each lens MUST map to a constitution section, using the existing constitution's section names
  where one exists and Spec Kit's default headings otherwise.
- **FR-006**: In brownfield mode, each lens MUST report current practice with citations before proposing
  candidates; in greenfield mode, each lens MUST say there is no practice to report and offer default
  candidates.
- **FR-007**: Every candidate MUST be tagged `observed` or `aspirational`, and in brownfield mode MUST cite at
  least one project file or git fact.
- **FR-008**: The agent MUST propose at most five candidates per lens.
- **FR-009**: When a constitution exists, the agent MUST suppress candidates it already asserts and MUST mark
  candidates that would change a principle as `amends: <principle>`.
- **FR-010**: Lens 2 MUST classify change types — at least feature, fix, refactor, docs, spike, and hotfix —
  by whether a spec is required, and MUST cover spike rules (timebox, never merged, findings captured instead
  of code).
- **FR-011**: Lens 3 MUST cover where intent originates, who owns it, how it reaches `/speckit-specify`, and how
  known unknowns are triaged, and MUST refer the BRD's format to `speckit.spectra.brd`.
- **FR-011a**: Lens 8 MUST offer agent autonomy as exactly one of three named levels: **every phase a human
  checkpoint** (a person starts each spec-kit phase; agents never run one phase into the next), **human gates
  at spec approval and PR review** (agents may run plan → tasks → implement unattended), or **autonomous to
  PR** (a person reviews only the pull request). The first is the default recommendation; brownfield evidence
  of current practice (e.g. agent-authored commits spanning several phases) MUST be cited where present. The
  accepted level enters the Constitution input as one testable clause. Lens 8 also covers the AI assistants
  and development-workflow tools in use and secret/API-key handling. Lens 8's question (question 9) MUST offer
  the three levels as three of its options, the default one marked recommended, plus Skip; the lens's tools and
  secrets candidates are listed above the options and are accepted with whichever level is chosen unless the
  reply excludes them in free text. Skip adopts nothing from the lens.

**Methodology stack**

- **FR-012**: The agent MUST present spec-driven development as the fixed base and MUST NOT offer it as
  optional.
- **FR-013**: The agent MUST offer at least TDD, BDD/ATDD, DDD, contract-first/API-first and ADR-driven as
  overlays, MUST cite repository evidence of each one already practised, and MUST recommend a stack.
- **FR-014**: Every adopted overlay MUST be recorded with a strictness (`MUST` or `SHOULD`), a scope (change
  types and, optionally, modules), and at least one obligation tied to a named spec-kit phase (specify, plan,
  tasks, implement). An overlay that cannot be expressed as such an obligation MUST NOT enter the Constitution
  input section. Each adopted overlay is **one** candidate guardrail in lens 1, whose statement lists its
  obligations per phase, so lens 1 stays within FR-008's cap of five.
- **FR-014a**: An obligation whose fulfilment happens during implementation (e.g. TDD's failing test before
  code, BDD's scenario runs before its step code) MUST name its evidence in `tasks.md`: the implementation task
  names the test task it depends on, and that test task records that it was run and failed before the
  implementation task is ticked. The generated obligation text MUST state this evidence so the Constitution
  Check and PR review can verify it.
- **FR-015**: An adopted overlay the code does not yet follow MUST be tagged `aspirational` and, by default,
  scoped to new and changed code.
- **FR-016**: Process cadences (Scrum, Kanban, Shape Up, and similar) MUST NOT enter the Constitution input
  section; they MAY appear in the document body.
- **FR-017**: Where two adopted overlays impose conflicting obligations at the same phase, the agent MUST report
  the conflict and obtain a precedence before writing the document.

**Boundaries**

- **FR-018**: The agent MUST NOT propose guardrails on test levels, coverage floors, UAT or the coverage ratchet
  (owned by `speckit.spectra.test-strategy`); on environments, promotion or rollback, or on the versioning
  scheme, how a release is cut, and the hotfix promotion path (owned by `speckit.spectra.deployment-strategy`); on product languages, frameworks or dependency policy (owned by
  `speckit.spectra.domain-analyzer`); or on DDD content — bounded contexts, invariants, glossary terms (owned by
  `speckit.spectra.domain-analyzer`). Where such ground is touched, it MUST cite the sibling's document if it
  exists or name the command that writes it.
- **FR-019**: `speckit.spectra.domain-analyzer` MUST stop working a Delivery & workflow lens and MUST name
  `speckit.spectra.methodology` for that ground; its question round MUST shrink accordingly and stay a fixed,
  announced count. In the same change, `speckit.spectra.deployment-strategy` MUST stop proposing the branching
  model and MUST cite `ENGINEERING_METHODOLOGY.md` for it, or name `speckit.spectra.methodology` where it does
  not exist; `speckit.spectra.kb-vault` MUST route an absorbed engineering methodology to
  `<artifact-root>/ENGINEERING_METHODOLOGY.md`, and where that file carries `command: speckit.spectra.methodology`
  front matter MUST NOT update it: it leaves the file unchanged, names `/speckit.spectra.methodology` as the way
  to fold the content in, and lists the absorbed source among the items it referred on in its report (a file
  at that path without that front matter is hand-written and takes kb-vault's existing update rules); and `speckit.spectra.review-pr` MUST read that file as a
  standard, citing accepted guardrails only (FR-034).
- **FR-020**: Delivery & workflow decisions already recorded in an existing `DOMAIN_ANALYSIS.md` MUST be
  preserved there as a record by the domain analyzer, and MUST be read by this agent as prior answers for the
  matching lenses.

**Clarification round**

- **FR-021**: The agent MUST ask a fixed, announced number of questions, one per turn, numbered within the
  total, after announcing the round once with its ways out (answer several at once, use your defaults, skip).
- **FR-021a**: Strictness and scope for all adopted overlays MUST be asked in a single question (question 2),
  presenting a table with one row per adopted overlay and a proposed strictness and scope for each. Its four
  options MUST be **Accept all as proposed** (recommended), **Make every overlay SHOULD**, **Choose per row**, and
  **Skip**; free text MAY adjust any row. Skip leaves every adopted overlay out of the Constitution input. With no
  overlay adopted, the question becomes a confirmation (FR-023).
- **FR-022**: Every question MUST offer at least four distinct labelled options, exactly one marked recommended
  with its evidence, and one of them Skip; free text MUST always be accepted.
- **FR-023**: A question with nothing to choose MUST become a confirmation that keeps its number and its four
  options.
- **FR-024**: Skip, an unanswered question, and a non-interactive run MUST adopt nothing; "use your defaults"
  MUST take the recommended option for every remaining question.

**The document**

- **FR-025**: The agent MUST write exactly one file, `<artifact-root>/ENGINEERING_METHODOLOGY.md` (default
  `docs/ENGINEERING_METHODOLOGY.md`), only after the round ends, and MUST rewrite it in place on re-runs. Where
  that path holds a file without this agent's front matter (a hand-written methodology), the agent MUST read it
  as evidence of current practice and MUST obtain the team's consent before the round to replace it; without
  consent, and always in a non-interactive run, it MUST write nothing and show the document in the session. It
  MUST NOT write a second file (no `.proposed` copy or similar).
- **FR-026**: The document MUST be readable as onboarding material: at least a mode-choice table (change type →
  mode → spec required), a branch-naming reference, a commit-convention reference, the methodology → phase
  obligations matrix, and a short section per lens — with sibling-owned ground summarised in one line and
  linked rather than restated.
- **FR-027**: The document MUST record every candidate offered with its ID, lens, target section, evidence,
  basis, decision (`accepted`, `declined`, `skipped`, `not_asked`) and status (`new`, `amends:`, `adopted:`).
- **FR-028**: The document MUST contain a Constitution input section in the same command-owned format the
  domain analyzer uses, holding exactly the accepted candidates not already adopted, grouped by target section,
  naming the goal and each guardrail's placement.
- **FR-029**: The document MUST end with a Decisions and sources section recording every question with the
  recommended option, the answer and its disposition, and every input read.
- **FR-030**: The document's structure MUST come from an overridable `engineering-methodology-template` shipped
  under `spectra/templates/`, registered in the manifest, and resolved through the same override chain as its
  siblings; the agent MUST report which template it used. The record format and the Constitution input format
  MUST stay owned by the agent.

**Handoff and limits**

- **FR-031**: The agent MUST end with one ready-to-paste `/speckit-constitution` line worded for the goal, or
  with none when nothing was accepted.
- **FR-031a**: After the handoff line, the report MUST list each sibling agent whose document does not exist yet
  (`speckit.spectra.domain-analyzer`, `speckit.spectra.test-strategy`, `speckit.spectra.deployment-strategy`), in
  the suggested order domain-analyzer → methodology → test-strategy → deployment-strategy, and MUST NOT fold any
  sibling document's input into its own `/speckit-constitution` line.
- **FR-032**: The agent MUST NOT write or edit the constitution, invoke `/speckit-constitution` or any other
  spec-kit phase, modify any file other than its own document, or make a network request.
- **FR-033**: The agent MUST NOT report as current practice anything the evidence does not show.
- **FR-034**: Any agent that reads `ENGINEERING_METHODOLOGY.md` as a standard MUST treat only guardrails whose
  decision is `accepted` as binding.

**Re-runs and non-interactive mode**

- **FR-035**: A candidate's ID MUST be computed once and frozen; re-runs MUST match prior candidates by recorded
  ID or by same intent within the same lens.
- **FR-036**: Re-runs MUST pre-fill each question with the prior answer, MUST NOT re-offer a declined candidate
  as new, MUST NOT delete any prior candidate, and MUST mark accepted candidates the constitution now asserts
  as adopted without ever reverting an adopted status.
- **FR-037**: Non-interactive mode MUST be declared, by flag or by the user, never inferred; it MUST ask no
  question, record every candidate as `not_asked`, and give no `/speckit-constitution` line.

**Packaging and governance**

- **FR-038**: The change MUST ship with updates to `spectra/extension.yml`, `spectra/CHANGELOG.md`,
  `agents-list.json`, `catalog.json`, `docs/packages/spectra.zip`, `docs/index.html`, the regenerated agent
  listings, and a hand-written per-agent prose block, so the generated-listings check passes. The CLI's
  `VERSION` MUST NOT change.
- **FR-039**: Because a new singleton deliverable must be named in the constitution by amendment,
  `ENGINEERING_METHODOLOGY.md` MUST be added to Principle VII's list of singletons in the same feature, through
  `/speckit-constitution` run by the user.

### Key Entities

- **Run mode**: `brownfield` or `greenfield`, with the evidence that decided it.
- **Run goal**: `create` or `update`, decided by whether a constitution exists.
- **Lens**: one of nine areas of methodology, each mapped to a constitution section, each with a
  current-practice statement (brownfield) and up to five candidates.
- **Candidate guardrail**: one proposed rule — statement, frozen ID, lens, target section, evidence, basis
  (`observed`/`aspirational`), decision, status.
- **Methodology overlay**: one methodology adopted on top of SDD — name, strictness, scope, and its obligations
  per spec-kit phase; the rows of the methodology → phase obligations matrix. Recorded as one candidate
  guardrail in lens 1.
- **Question**: one of the fixed round — what was asked, the recommended option, the answer, the disposition
  (`answered`, `default_taken`, `skipped`, `not_asked`).
- **Constitution input**: the accepted, not-yet-adopted guardrails grouped by section, with the run's goal —
  what `/speckit-constitution` consumes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A team completes a run, from first output to handoff, without opening the document to make any
  decision.
- **SC-002**: In 100% of runs where at least one guardrail is accepted, the run ends with a single
  `/speckit-constitution` line that creates or updates the constitution from the Constitution input section.
- **SC-003**: Every adopted overlay in the Constitution input section names at least one spec-kit phase and the
  obligation at that phase; zero overlays enter it as a bare label.
- **SC-004**: Run on a brownfield repository, 100% of lenses report current practice with at least one citation
  or say what was searched; zero claims of current practice lack evidence.
- **SC-005**: Run together on the same repository, this agent and the domain analyzer produce zero candidates
  in each other's ground, this agent produces zero candidates in test-strategy or deployment-strategy ground,
  and the deployment strategist produces zero candidates on the branching model.
- **SC-006**: Applied to a brownfield repository that already keeps a hand-written `ENGINEERING_METHODOLOGY.md`,
  the produced document covers intake, work modes, spikes, branching, review, commits, AI tooling, and
  constitution amendment, with coverage and environment content only linked to their sibling documents, and the
  existing file is read as evidence.
- **SC-007**: On a re-run with no change to the project or constitution, zero previously declined guardrails are
  offered as new and zero adopted guardrails appear in the Constitution input section.
- **SC-008**: The repository's test suite and the generated-listings check pass with the change in place.

## Assumptions

- The command is `speckit.spectra.methodology`; the document is the singleton
  `<artifact-root>/ENGINEERING_METHODOLOGY.md`, following Principle VII's rule for standing-policy artifacts.
- The round has a fixed count of **ten** questions so it can be announced honestly: (1) methodology stack, (2)
  strictness and scope of each adopted overlay (a confirmation when none is adopted), then (3)–(10) one per
  lens 2–9. Mode is stated and corrected before the round, not counted in it.
- An unanswered question adopts nothing, matching the domain analyzer rather than test-strategy, because the
  answers become governance.
- Lens questions use the domain analyzer's four-option shape (Recommended set, Codify only what exists, Full
  set, Skip, with Choose individually replacing a duplicate), except question 9, which offers the three autonomy
  levels plus Skip (FR-011a).
- Default target sections: lens 1 → Core Principles; lenses 2–7 → Development Workflow; lens 8 → Additional
  Constraints; lens 9 → Governance — overridden by the project's own section names.
- The domain analyzer's change is a narrowing: its command name, output path and arguments are unchanged; its
  question count drops from eight to seven.
- The extension takes a MINOR bump (1.23.0 → 1.24.0): one command added, none renamed or removed. The constitution
  amendment naming the new singleton is a MINOR amendment, run by the user through `/speckit-constitution`.
- A team's hand-written engineering methodology — onboarding material covering intake, work modes,
  branching, review, and commits — is the reference for the document's shape, not a template to copy; organisation-specific content (internal URLs, tool names) appears only when the team supplies it.
