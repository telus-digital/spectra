# Feature Specification: Safe Handoffs Between the Foundation Agents

**Feature Branch**: `036-foundation-agent-handoff`

**Created**: 2026-10-24

**Status**: Implemented

**Input**: User description: "Make the foundation agents (kb-vault, domain-analyzer, methodology, test-strategy, deployment-strategy) hand off to each other safely when Spectra is installed on a brownfield project. (1) kb-vault stops writing to the singleton documents that feed the constitution and lands such sources as ordinary category documents, referring the user to the owning agent. (2) The four constitution feeders deliberately read kb-vault-imported documents as a distinct kind of evidence — documented intent — while code, history and configuration still decide observed versus aspirational. (3) test-strategy matches the other feeders: a create goal when no constitution exists, a 'Constitution input' section with stable frozen IDs, adopted-status tracking, sibling reading, and lossless re-runs from the checkbox format; deployment-strategy is checked against the same contract and aligned. (4) Document the brownfield onboarding sequence, with a constitution run after each feeder. (5) Fix kb-vault's template-resolution list so it names every template its reserved map uses. Out of scope: changing what any agent analyses, adding new lenses or questions, or letting any agent write the constitution."

## Context

Spectra's Foundation phase has one importer and four constitution feeders:

- **kb-vault** brings knowledge that lives outside the repository — PDFs, Word files, decks, dictated
  notes — into the repository as Markdown. It invents nothing and decides nothing.
- **domain-analyzer**, **methodology**, **test-strategy**, and **deployment-strategy** each read the
  project, put candidate guardrails to the team, record what the team decided in one standing document
  (`DOMAIN_ANALYSIS.md`, `ENGINEERING_METHODOLOGY.md`, `TEST_STRATEGY.md`, `DEPLOYMENT_STRATEGY.md`), and
  hand the accepted guardrails to `/speckit-constitution`.

Today those five agents do not compose safely:

1. kb-vault's reserved map sends an imported domain analysis, methodology, test strategy, or deployment
   strategy to the very singleton file its owning agent writes. Only methodology recognises such a file
   as hand-written and asks before replacing it. domain-analyzer and test-strategy treat it as one of
   their own prior runs and silently rewrite it; kb-vault may also update a file the owning agent wrote,
   breaking its frozen IDs and its machine-read header (which `speckit.spectra.test-plan` depends on). An
   imported "guardrail proposal" could even reach a Constitution input section without the team choosing
   it. Principle VII already names each singleton's owning command; kb-vault writing them contradicts it.
2. The feeders pick up imported documents only incidentally, through a generic "documentation
   directories" read, and do not distinguish a document describing intent from code or history showing
   practice.
3. test-strategy and deployment-strategy produce a different hand-off from the other two: a checkbox
   "Proposed constitution amendment" with no stable IDs, no adoption tracking, and — when no constitution
   exists — no hand-off at all. On a brownfield project with no constitution, their policy never reaches
   the constitution.
4. Nowhere is the intended order written down — in particular that `/speckit-constitution` runs after
   **each** feeder, so each later feeder sees the constitution and proposes only what it does not yet say.
5. kb-vault's template-resolution list and its reserved map disagree about which templates kb-vault
   resolves.

## Clarifications

### Session 2026-10-24

- Q: When test-strategy or deployment-strategy shows its drafted constitution rules for approval, should the team accept or reject them all at once, or decide each rule separately? → A: One approval step accepts every rule shown; free text may decline or reword individual rules, which are recorded as declined (or accepted with the team's wording).
- Q: Should this feature also change review-pr so it treats only accepted constitution rules in TEST_STRATEGY.md and DEPLOYMENT_STRATEGY.md as review standards? → A: Yes, in scope — review-pr applies the same accepted-only rule it already uses for DOMAIN_ANALYSIS.md and ENGINEERING_METHODOLOGY.md.
- Q: When kb-vault imports a document about one of the four policies, which folder should it go in? → A: One folder per policy with a `-source` suffix: `domain-analysis-source/`, `engineering-methodology-source/`, `test-strategy-source/`, `deployment-strategy-source/`.
- Q: How should each of the four agents mark its standing document as its own? → A: All four write `command: speckit.spectra.<agent>` in the document header; files from earlier versions, which lack the key, are recognised by the header fields those versions already wrote.
- Q: Since kb-vault will no longer write any of the four policy documents, which templates should its template list name? → A: Exactly the templates its remaining reserved map uses (adr, brd, impact-analysis, defect-rca) and no policy-agent template; imported policy sources resolve `<kind>-source-template`, then `kb-document-template`.
- Q: Should the body of TEST_STRATEGY.md and DEPLOYMENT_STRATEGY.md still count as review-pr standards, or only the accepted rules? → A: Accepted rules only; body sections are context and never a finding source, as for the domain analysis and methodology.
- Q: When an agent cites an imported document, should it label the citation with the word `claimed`, the word deployment-strategy already uses for "what a document says"? → A: Yes — `claimed` in all four feeders (FR-007).
- Q: When review-pr finds an earlier-format strategy document in which no drafted rule was ever approved, what should it do? → A: Draw no standards from it, and say so plainly in the review, naming the remedy (re-run the strategy agent and accept guardrails) (FR-020a, Edge Cases).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Importing outside documents never clobbers a decision record (Priority: P1)

A team installing Spectra on an existing codebase has an old test-strategy PDF and a Word document
describing its engineering workflow. They hand both to kb-vault. kb-vault lands each as an ordinary,
numbered, provenance-carrying source document under the artifact root, tells them which agent turns it
into the project's standing policy, and never touches `TEST_STRATEGY.md`, `ENGINEERING_METHODOLOGY.md`,
`DOMAIN_ANALYSIS.md`, or `DEPLOYMENT_STRATEGY.md`. When they later run the owning agents, the imported
documents are still there, unchanged.

**Why this priority**: This is the defect that can silently destroy a team's recorded decisions or
smuggle unchosen guardrails toward the constitution. Everything else builds on the singletons being owned
by exactly one agent each.

**Independent Test**: On a project with and without existing singletons, supply kb-vault one source of
each of the four policy kinds; confirm the plan table proposes only category documents plus referrals,
that no singleton is created or modified after approval, and that the report names the owning command
for each.

**Acceptance Scenarios**:

1. **Given** no `TEST_STRATEGY.md` exists, **When** the user supplies a test-strategy document to
   kb-vault and approves the plan, **Then** kb-vault writes `<artifact-root>/test-strategy-source/NNN-<title>.md`
   with its Provenance and Gaps sections, creates no `TEST_STRATEGY.md`, and its report tells the user to
   run `speckit.spectra.test-strategy` to turn it into the project's strategy.
2. **Given** a `DOMAIN_ANALYSIS.md` written by domain-analyzer exists, **When** the user supplies a
   document kb-vault classifies as a domain analysis, **Then** the plan shows no update row for
   `DOMAIN_ANALYSIS.md`, shows a create row for a domain-analysis source document, and refers the user to
   `speckit.spectra.domain-analyzer`; after approval `DOMAIN_ANALYSIS.md` is byte-for-byte unchanged.
3. **Given** a hand-written `DEPLOYMENT_STRATEGY.md` exists that no Spectra agent wrote, **When** the user
   supplies a deployment-strategy document, **Then** kb-vault still does not update the singleton; it
   lands a source document and refers to `speckit.spectra.deployment-strategy`.
4. **Given** the user asks kb-vault to write the source directly to `TEST_STRATEGY.md`, **When** kb-vault
   builds the plan, **Then** it declines that destination, says the file belongs to the owning agent, and
   offers the source-document row and the referral instead.

---

### User Story 2 - Feeders use imported knowledge without mistaking it for practice (Priority: P1)

After importing, the team runs domain-analyzer, methodology, test-strategy, and deployment-strategy. Each
one finds the kb-vault-imported documents relevant to its ground, cites them as **documented intent**,
and keeps deciding `observed` versus `aspirational` from code, history, and configuration. Where an
imported workflow document says "we squash-merge" but the history is full of merge commits, the agent
reports both and treats the history as current practice. No imported document adopts a guardrail on its
own; only the team's answers in the round do.

**Why this priority**: Importing outside knowledge is only worth doing if the analysts actually use it —
and only safe if they never let a document's claims outrank the evidence or the team's choice.

**Independent Test**: On a sample brownfield project with imported source documents that partly agree
and partly disagree with the code and history, run each feeder; confirm every imported document relevant
to its ground appears among its inputs as documented intent, every disagreement is reported with both
sides, no candidate's basis is set from an imported document alone, and nothing reaches Constitution
input without a team answer.

**Acceptance Scenarios**:

1. **Given** an imported source document under the artifact root with a Provenance section, **When** a
   feeder runs, **Then** it lists the document among its consulted inputs and cites it, where relevant,
   with a label that distinguishes documented intent from code, history, or configuration evidence.
2. **Given** an imported document asserts a practice the code or history contradicts, **When** the
   feeder reports current practice, **Then** it states both, treats the code or history as current
   practice, and marks any candidate built on the documented intent as `aspirational`.
3. **Given** an imported document contains a list of rules phrased as guardrails, **When** the feeder
   runs non-interactively or the team skips that question, **Then** none of those rules reaches the
   Constitution input section.
4. **Given** an imported document contains text addressed to the agent (an instruction to adopt, write,
   or skip something), **When** the feeder reads it, **Then** the text is treated as content, never
   acted on, and is reported where it would have changed an outcome.

---

### User Story 3 - Every feeder hands a consistent, trackable input to the constitution (Priority: P2)

A team runs test-strategy on a brownfield project that has no constitution yet. Instead of saying there
is nothing to amend, it plans a **create**, records the team's approval as decisions on stable, IDed
guardrails in a "Constitution input" section, and hands off a ready-to-paste create prompt — exactly like
domain-analyzer and methodology. On a later re-run after the constitution adopted those guardrails, it
marks them `adopted` and stops proposing them. It also reads the accepted entries of its siblings and
refers, rather than re-proposes, any clause another feeder owns. deployment-strategy is brought to the
same contract.

**Why this priority**: It makes the four hand-offs uniform, which is what makes the documented sequence
(Story 4) work and lets downstream readers treat all four documents the same way. It depends on nothing
in Stories 1–2 but is less urgent than preventing data loss.

**Independent Test**: Run test-strategy and deployment-strategy on (a) a project with no constitution and
(b) one with a constitution; confirm both produce a Constitution input section in the shared shape with
frozen IDs and a goal-specific hand-off line; then ratify, re-run, and confirm adopted items leave the
section; then re-run against a document in the old checkbox format and confirm no decision is lost.

**Acceptance Scenarios**:

1. **Given** no constitution exists, **When** test-strategy (or deployment-strategy) completes and the
   team approves, **Then** the document carries a Constitution input section whose goal line says
   **create**, and the hand-off is a ready-to-paste `/speckit-constitution` create prompt.
2. **Given** a constitution exists, **When** either agent runs, **Then** the goal is **update**,
   candidates the constitution already asserts are suppressed, amending candidates are marked
   `amends: <principle>`, and the hand-off is an amend prompt.
3. **Given** each Constitution input entry carries an ID computed once from its first wording, **When**
   the team rewords it on a later run, **Then** the ID is unchanged.
4. **Given** a prior run's accepted guardrail has since been ratified, **When** the agent re-runs,
   **Then** that entry is marked `adopted: <principle>` and no longer appears in Constitution input; if
   the principle later drifts, the drift is reported and the item is not silently re-proposed.
5. **Given** a `TEST_STRATEGY.md` or `DEPLOYMENT_STRATEGY.md` from an earlier version with a checkbox
   amendment, **When** the agent re-runs, **Then** checked items are carried forward as accepted,
   unchecked items as undecided, every statement is kept, and the report says the file was migrated.
6. **Given** methodology has an accepted TDD obligation that a fix starts with a failing regression test,
   **When** test-strategy drafts its regression policy, **Then** it cites that accepted entry rather than
   drafting a second clause for the same obligation.
7. **Given** the team declines the approval gate or the run is non-interactive, **Then** nothing is
   accepted, the Constitution input section says so, and no hand-off command is given.

---

### User Story 4 - A newcomer can follow the brownfield onboarding sequence (Priority: P3)

Someone installing Spectra on an existing codebase opens the README or the landing page and finds one
ordered sequence: kb-vault (optional, to import outside knowledge), then domain-analyzer →
`/speckit-constitution` (create) → methodology → `/speckit-constitution` (amend) → test-strategy →
`/speckit-constitution` (amend) → deployment-strategy → `/speckit-constitution` (amend). It explains why
the constitution runs after each feeder, and recommends declaring the `Artifact root:` line in the first
constitution run so later agents stop asking.

**Why this priority**: The behavioural fixes in Stories 1–3 are what make the sequence safe; this story
makes it discoverable. It is valuable but changes no agent behaviour.

**Independent Test**: A reader with no prior Spectra knowledge, given only `README.md`,
`spectra/README.md`, or the landing page, can state the order, say why the constitution runs between
feeders, and say where the `Artifact root:` line goes.

**Acceptance Scenarios**:

1. **Given** the three documentation surfaces, **When** a reader looks for how to start on an existing
   codebase, **Then** each surface presents the same ordered sequence and the same explanation.
2. **Given** the sequence, **When** a reader asks why not run all four feeders first and the constitution
   once, **Then** the documentation answers it: each later feeder detects the constitution, switches to
   update, and drops what is already ratified.

---

### User Story 5 - kb-vault resolves the template its reserved map promises (Priority: P3)

A maintainer reading kb-vault's instructions finds a template-resolution list that matches its reserved
map exactly: every template the map uses is listed, and no feeder template — which kb-vault no longer
resolves once it stops writing the singletons — is listed. A project that wants imported policy sources
shaped differently overrides `<kind>-source-template` or `kb-document-template`.

**Why this priority**: A small, self-contained correctness fix to kb-vault's own instructions.

**Independent Test**: Compare the template names in kb-vault's resolution list with the templates its
reserved map references; they match exactly.

**Acceptance Scenarios**:

1. **Given** kb-vault's reserved map and its resolution list, **When** they are compared, **Then** every
   template the map names appears in the list and the list names none the map does not use.

---

### Edge Cases

- **A singleton written by an earlier version of its owning command** carries no new ownership marker.
  The owning command must still recognise it as its own prior run, not as a hand-written file.
- **A singleton that kb-vault wrote under an earlier Spectra version** exists in a project. The owning
  command must treat it as a hand-written document — documented-intent evidence — and replace it only with
  the team's consent, as methodology already does; it must not misread it as a prior run and inherit
  decisions it never recorded.
- **One supplied source covers both a policy kind and something else** (a deck with a test strategy and UX
  standards): kb-vault splits it — a policy source document plus a referral, and an ordinary category
  document for the rest.
- **Several sources describe the same policy**: kb-vault merges them into one source document and refers
  once.
- **A policy source already imported earlier** matches an existing source document: kb-vault updates that
  source document under its normal update rules (it is kb-vault's own file), and still refers.
- **An imported document lives outside the artifact root** (for example a legacy folder): feeders read it
  only if it is documentation they already read today; the documented-intent label applies to anything
  recognisable as kb-vault output by its Provenance section.
- **The team declines to replace a hand-written singleton** in a feeder run: the feeder writes nothing and
  shows its document in the session, as methodology already does.
- **Two feeders' accepted entries overlap** despite sibling reading (for example an older document
  predates this change): the later feeder reports the overlap and refers to the earlier entry rather than
  adding a second source.
- **The publication check fires** (the default `docs/` folder is a published site): the onboarding
  documentation's `Artifact root:` advice must still steer to a non-publishing root.
- **review-pr, test-plan, and uat read the changed documents**: they must keep working on documents in
  both the new and the earlier format, and review-pr must treat only accepted Constitution input entries
  of the two strategies as standards.
- **An earlier-format strategy whose amendment was never approved** (no checked item) gives review-pr no
  standard from that document. review-pr says so plainly rather than treating the file as unreadable; the
  remedy is to re-run the strategy agent and accept guardrails.

## Requirements *(mandatory)*

### Functional Requirements

**kb-vault and the singletons**

- **FR-001**: kb-vault MUST NOT create, update, or propose writing any of `DOMAIN_ANALYSIS.md`,
  `ENGINEERING_METHODOLOGY.md`, `TEST_STRATEGY.md`, or `DEPLOYMENT_STRATEGY.md`, whoever wrote the
  existing file and whatever the user asks.
- **FR-002**: A source kb-vault classifies as one of those four policy kinds MUST be planned as an
  ordinary category document under the artifact root, in exactly one of four fixed per-kind source
  folders — `<artifact-root>/domain-analysis-source/`, `<artifact-root>/engineering-methodology-source/`,
  `<artifact-root>/test-strategy-source/`, `<artifact-root>/deployment-strategy-source/` — named
  `NNN-<kebab-title>.md` and numbered as a series, shaped by its `<category>-template` override or
  else `kb-document-template`, and carrying kb-vault's Provenance and Gaps sections.
- **FR-003**: For every such row, kb-vault's plan and its report MUST name the owning agent's command as
  the way to turn the source into the project's standing document.
- **FR-004**: When a user directs a policy source at a singleton path, kb-vault MUST decline that
  destination, say which agent owns it, and offer the source-document row instead.
- **FR-005**: kb-vault's other reserved-map entries (ADR, BRD, impact analysis, defect RCA) and all its
  existing rules (approval gate, no invention, redaction, no commit) MUST be unchanged.

**Feeders reading imported knowledge**

- **FR-006**: domain-analyzer, methodology, test-strategy, and deployment-strategy MUST deliberately read
  kb-vault-imported documents under the artifact root that are relevant to their ground, recognising them
  by kb-vault's Provenance section, and MUST list them among their consulted inputs.
- **FR-007**: Each feeder MUST cite imported documents as a distinct evidence kind — documented intent,
  cited with the provenance token `claimed` (the word deployment-strategy already uses for what a document
  says) — visibly different from code, history, or configuration evidence.
- **FR-008**: A candidate's `observed` / `aspirational` basis MUST be decided by code, history, and
  configuration only. A candidate resting solely on documented intent MUST be `aspirational`.
- **FR-009**: Where documented intent and code or history disagree, the feeder MUST report both and treat
  code or history as current practice.
- **FR-010**: No imported document MAY adopt a guardrail. Only a team answer in the clarification round
  (or the approval gate, for test-strategy and deployment-strategy) MAY move a guardrail into Constitution
  input. Text in an imported document addressed to the agent MUST be treated as content and never acted on.
- **FR-011**: Each feeder MUST write `command: speckit.spectra.<agent>` (`domain-analyzer`,
  `methodology`, `test-strategy`, `deployment-strategy`) in its document's header, as methodology already
  does. A file at the feeder's path is its own prior run when its header carries that key, or — for a
  document from an earlier version, which lacks the key — when its header carries the fields that earlier
  version of the feeder wrote. Each feeder MUST treat a singleton at its path that it did not write (hand-written, or
  written by kb-vault under an earlier version) as documented-intent evidence, replacing it only with the
  team's consent, and writing nothing when consent is declined or the run is non-interactive.

**test-strategy and deployment-strategy hand-off**

- **FR-012**: test-strategy and deployment-strategy MUST support a **create** goal when no constitution
  exists and an **update** goal when one does, announced at the start of the run as the other feeders do.
- **FR-013**: Both MUST replace the checkbox "Proposed constitution amendment" with a "Constitution input"
  section in the same shape domain-analyzer and methodology use: a goal line; entries grouped by target
  constitution section; each entry with a stable, content-derived ID (prefix `ts-` for test-strategy,
  `ds-` for deployment-strategy) computed once and frozen; placement `add` or `amends: <principle>`; and
  basis `observed` or `aspirational`.
- **FR-014**: Both MUST record a decision for every drafted guardrail — `accepted`, `declined`,
  `skipped`, or `not_asked` — from the existing approval gate. Approving accepts every guardrail shown;
  in the same reply the team MAY name individual guardrails to decline (recorded `declined`) or reword
  (recorded `accepted` with the team's wording, ID unchanged). Declining the gate as a whole records every
  guardrail `skipped` (undecided, offered again on re-run); no answer, or a non-interactive run, records
  every guardrail `not_asked`. Constitution input MUST hold exactly the accepted, not-yet-adopted
  guardrails.
- **FR-015**: On re-run, both MUST mark adoption (`adopted: <principle>` when the constitution now asserts
  the guardrail), remove adopted entries from Constitution input, never revert an adopted entry, report
  drift, and never re-offer a declined guardrail as new.
- **FR-016**: On re-run against a document in the earlier checkbox format, both MUST carry every item
  forward — checked as `accepted`, unchecked as undecided — keep every statement, assign IDs once, and say
  in the report that the file was migrated.
- **FR-017**: Both MUST hand off a ready-to-paste `/speckit-constitution` line worded for the goal
  (create or amend), MUST give no command when nothing was accepted, and MUST NOT invoke
  `/speckit-constitution` or write the constitution.
- **FR-018**: test-strategy MUST read the accepted entries of `DOMAIN_ANALYSIS.md`,
  `ENGINEERING_METHODOLOGY.md`, and `DEPLOYMENT_STRATEGY.md`, and MUST cite rather than re-draft any clause
  another feeder owns; deployment-strategy's existing sibling reading MUST be kept and checked against the
  same rule.
- **FR-019**: Everything else both agents guarantee MUST be unchanged: their lenses, their questions, the
  coverage-floor and baseline rules, the UAT clause, the machine-read header fields that test-plan and
  uat consume, and their non-interactive behaviour (which records nothing as accepted).

**Downstream readers**

- **FR-020**: review-pr, test-plan, and uat MUST continue to read `TEST_STRATEGY.md` and
  `DEPLOYMENT_STRATEGY.md` correctly in both the new and the earlier format.
- **FR-020a**: review-pr MUST be changed in this feature so that, from `TEST_STRATEGY.md` and
  `DEPLOYMENT_STRATEGY.md`, it cites as standards only guardrail entries whose decision is `accepted` —
  the Constitution input section, or an `accepted` record elsewhere in the document — exactly as it
  already does for `DOMAIN_ANALYSIS.md` and `ENGINEERING_METHODOLOGY.md`. A `declined`, `skipped`, or
  `not_asked` entry MUST never be a finding source, and neither MUST any body section describing a
  recommendation (coverage floor, lens approach, regression gate, environments) that is not itself an
  accepted record — such sections are context only. In a document in the earlier checkbox format, only
  checked items count as accepted; a document with no checked item contributes no standard, and review-pr
  MUST say so in its output and name the remedy rather than staying silent or treating the file as
  unreadable.

**Documentation and kb-vault template list**

- **FR-021**: `README.md`, `spectra/README.md`, and `docs/index.html` MUST each present the brownfield
  onboarding sequence — kb-vault (optional) → domain-analyzer → `/speckit-constitution` (create) →
  methodology → `/speckit-constitution` (amend) → test-strategy → `/speckit-constitution` (amend) →
  deployment-strategy → `/speckit-constitution` (amend) — consistently across all three.
- **FR-022**: That documentation MUST explain that each feeder hands off its own constitution run and why
  running it after each feeder matters, and MUST recommend declaring the `Artifact root:` line in the first
  constitution run (respecting the publication check).
- **FR-023**: The sequence documentation MUST respect the repository's rule that structured agent listings
  are generated from the roster and prose is hand-written.
- **FR-024**: kb-vault's template-resolution list MUST name exactly the templates its reserved map uses —
  `adr-template`, `brd-template`, `impact-analysis-template`, `defect-rca-template` — and MUST name none
  of the four feeder templates (`domain-analysis-template`, `engineering-methodology-template`,
  `test-strategy-template`, `deployment-strategy-template`), which kb-vault no longer resolves.

**Release discipline**

- **FR-025**: The change MUST ship as one extension release, with the version, changelog, catalog, package,
  and landing page kept in sync, and with every agent description that states a changed behaviour updated
  to match. The CLI channel MUST NOT be bumped.

### Key Entities

- **Constitution feeder singleton**: one of the four standing documents, each owned by exactly one
  agent; carries the team's decisions and a Constitution input section; rewritten in place by its owner.
- **Policy source document**: a kb-vault-written, numbered, provenance-carrying Markdown document holding
  imported knowledge about one policy kind; permanent; read by the owning feeder as documented intent.
- **Constitution input entry**: an accepted, not-yet-adopted guardrail with a frozen ID, target section,
  placement, and basis; the unit every feeder hands to `/speckit-constitution`.
- **Guardrail decision**: `accepted`, `declined`, `skipped`, or `not_asked`, plus an adoption status of
  `new`, `amends: <principle>`, or `adopted: <principle>`.
- **Evidence kind**: code, history, configuration (which decide basis) versus documented intent (which
  informs but never decides basis or adoption).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Across kb-vault runs supplying each of the four policy kinds, on projects with and without
  existing singletons (at least 8 cases), zero singletons are created or modified and every run names the
  owning command.
- **SC-002**: Running all four feeders after an import, zero imported source documents are modified or
  removed.
- **SC-003**: Each of the four feeders produces a goal-correct, ready-to-paste constitution hand-off in
  both the no-constitution and the existing-constitution case — 8 of 8.
- **SC-004**: Following the documented sequence end to end on a sample brownfield project, no clause in
  the resulting constitution has two source entries across the four feeders.
- **SC-005**: Re-running test-strategy and deployment-strategy on documents in the earlier checkbox format
  loses zero recorded decisions and zero guardrail statements.
- **SC-006**: No guardrail reaches any Constitution input section from an imported document without a
  recorded team decision — zero occurrences across the walkthrough, including non-interactive runs.
- **SC-007**: A reader given only one of the three documentation surfaces can state the onboarding order
  and why the constitution runs between feeders, and the three surfaces present the same order.
- **SC-008**: Every existing Spectra check and test passes, and review-pr, test-plan, and uat behave the
  same on documents in the earlier format as before the change.
- **SC-009**: Reviewing a pull request against strategy documents that contain declined, skipped, and
  not-asked guardrails, review-pr raises zero findings sourced from any non-accepted entry.

## Assumptions

- The four `-source` folders (FR-002) each hold one artifact type, as Principle VII requires, and do not
  collide with the pre-1.19.0 legacy `test-strategy/` location.
- test-strategy and deployment-strategy keep their existing approval gate as the place decisions are made;
  no new questions or lenses are added (out of scope). Per-guardrail control comes through free text in
  the approval reply (see Clarifications and FR-014).
- An earlier-version prior run is recognisable from the header fields that version wrote (for example
  `generated:`, `template:`, `clarification:`), so upgrading never triggers a spurious consent question.
  A kb-vault-written singleton from an earlier version lacks those command-owned fields and is therefore
  read as hand-written.
- Unchecked items in an earlier checkbox amendment are treated as undecided, not declined, following
  domain-analyzer's precedent, because an unticked box cannot distinguish "rejected" from "never reviewed".
- Constitution feeders still never write the constitution and never invoke another phase; each hand-off
  remains a command the user runs.
- Because kb-vault no longer lands imported policies at the singleton paths, an imported policy is not a
  review-pr standard until its owning feeder has run and the team has accepted guardrails. This is
  intended: review standards come from team decisions, not from imported text. For the same reason,
  review-pr stops treating the strategy documents' body as standards (FR-020a); a recommendation the team
  wants enforced in review becomes an accepted guardrail.
- This is a Spectra extension change only (Markdown, templates, catalog, package, docs); the `spectra`
  CLI is not affected.
