# Feature Specification: The ADR Agent Hands Off to the Constitution

**Feature Branch**: `037-adr-constitution-handoff`

**Created**: 2026-10-24

**Status**: Implemented

**Input**: User description: "Bring the ADR agent (spectra/commands/adr.md, Step 7) in line with how test-strategy, deployment-strategy, domain-analyzer and methodology hand off to the constitution. When an ADR is significant, the agent must never write .specify/memory/constitution.md, even when the user approves. Instead it writes a Constitution input section into the ADR itself (statement in the constitution's voice, target section, evidence, and the user's recorded decision), and it prints a ready-to-paste /speckit-constitution amend prompt that references the ADR, for the user to run. It must respect sibling ground: when the decision falls in an area another agent owns (testing goes to test-strategy, environments and releases to deployment-strategy, product technology and the domain to domain-analyzer, methodology to methodology), it drafts no clause there. It names the owning agent and suggests re-running it instead, so each constitution clause keeps one source. The methodology agent's sibling-ground table should list the ADR agent as a constitution feeder too."

## Context

`speckit.spectra.adr` records one architectural decision per run as `<artifact-root>/adr/ADR-NNN-<title>.md`.
Its Step 7 already checks whether a decision is **significant** — it sets a cross-cutting standard,
contradicts, narrows or extends a principle, or establishes a convention future work must follow — and
proactively recommends a constitution change. So decisions already flow back to the constitution.

How they flow back is the problem. On the user's agreement, Step 7 **edits
`.specify/memory/constitution.md` directly**. Four other agents feed the constitution —
`domain-analyzer`, `methodology`, `test-strategy`, and `deployment-strategy` — and none of them ever
writes that file. Each drafts guardrails as records, puts them to the team at one approval step, writes
the accepted ones into a **Constitution input** section of its own document, and prints a ready-to-paste
`/speckit-constitution` line for the user to run. `/speckit-constitution` owns the constitution's version,
its MAJOR / MINOR / PATCH judgement, its Sync Impact Report, and the propagation of a change into the
templates that depend on it.

The ADR agent's direct edit therefore bypasses all of that: a constitution changed by an ADR carries no
version bump, no impact report, and no link back to the decision that caused it. And because the ADR agent
knows nothing about which agent owns which ground, an ADR such as "adopt contract tests at every service
boundary" can write a testing clause that competes with the one `test-strategy` hands off — the "one
source per clause" rule the four feeders already observe exists precisely to prevent a constitution that
contradicts itself.

This feature makes the ADR agent the fifth constitution feeder, on the same contract as the other four.

## Clarifications

### Session 2026-10-24

- Q: Domain-analyzer owns "product languages, frameworks, dependency policy", yet many architectural decisions are technology choices. What ground does the ADR agent own? → A: Architecture-level choices — datastores, messaging, architecture style, service and data boundaries, integration patterns. Domain-analyzer keeps languages, frameworks, and dependency policy. Both agents state the split (FR-010, FR-019).
- Q: When the project has no constitution, what does a significant ADR hand off? → A: No create goal. The agent still drafts and records the guardrails in the ADR, prints no `/speckit-constitution` line, points the user to the foundation agents (domain-analyzer first), and says the ADR's accepted records stay ready for a later amend (FR-015).
- Q: The domain-analyzer and the ADR agent can both write constitution rules about architecture (layering, module and service boundaries, integrations). When both could cover the same rule, which one should write it? → A: The recorded decision wins, clause by clause. The ADR agent keeps the full architecture ground; domain-analyzer still works architecture from what it observes, but first cites any accepted ADR record that covers a clause instead of drafting it. Whichever agent drafts a clause first is its source; a later ADR that changes it drafts an amendment (FR-019, FR-005, FR-006).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A significant decision reaches the constitution through `/speckit-constitution` (Priority: P1)

An architect records "every service owns its data store; no service reads another service's tables". The
ADR agent recognises this as an architectural boundary future work must follow, drafts a guardrail in the
constitution's voice, and shows it for approval. The architect approves. The agent writes the accepted
guardrail into a Constitution input section of the ADR, leaves the constitution untouched, and prints one
ready-to-paste `/speckit-constitution` line that names the ADR file. The architect runs it, reviews the
Sync Impact Report, and the constitution's version moves.

**Why this priority**: This is the defect being fixed. Every other story refines it.

**Independent Test**: Run the ADR agent on a project with a constitution and a decision that sets an
architectural boundary; approve the drafted guardrail; confirm the constitution file is byte-identical
after the run, the ADR contains a Constitution input section with the accepted record, and the session ends
with a single `/speckit-constitution` line referencing that ADR's path.

**Acceptance Scenarios**:

1. **Given** a significant decision and an existing constitution, **When** the user approves the drafted
   guardrail, **Then** the constitution file is not modified, the ADR carries the accepted record in its
   Constitution input section, and the agent prints a `/speckit-constitution` amend line that references the
   ADR by its actual path.
2. **Given** the same run, **When** the user insists the agent "just edit the constitution", **Then** the
   agent declines, explains that `/speckit-constitution` owns that file, and gives the line again.
3. **Given** a decision that is not significant, **When** the run completes, **Then** the ADR has no
   Constitution input section, the agent says in one line why no constitution change is warranted, and no
   `/speckit-constitution` line is printed.
4. **Given** a significant decision, **When** the user declines every drafted guardrail, **Then** the
   records are kept in the ADR as declined, the Constitution input section says nothing was accepted, and
   no `/speckit-constitution` line is printed.

---

### User Story 2 - A decision on another agent's ground is referred, not drafted (Priority: P1)

An architect records "end-to-end tests run against an ephemeral environment per pull request". The
decision is real and the ADR is written, but test levels belong to `test-strategy` and environments to
`deployment-strategy`. The ADR agent drafts no constitution clause for either. It names the owning agents,
says whether each one's document already exists, and suggests re-running them — they read ADRs as
evidence, so the decision will be considered as part of their own handoff.

**Why this priority**: Without it, making the ADR agent a feeder creates a second source for clauses the
other feeders already own — the exact contradiction the sibling-ground rule exists to prevent.

**Independent Test**: Run the ADR agent on decisions that fall wholly in each sibling's ground; confirm no
record is drafted for those parts, each owning agent is named, and the suggestion to re-run it appears.

**Acceptance Scenarios**:

1. **Given** a decision wholly within one sibling's ground, **When** Step 7 runs, **Then** no guardrail is
   drafted, the owning agent is named, and the user is told to re-run that agent.
2. **Given** a decision that spans the ADR agent's own ground and a sibling's, **When** Step 7 runs,
   **Then** the agent drafts only the part on its own ground and refers the rest to the owning agent.
3. **Given** the owning sibling's document already exists and already carries an accepted record that the
   decision contradicts, **When** Step 7 runs, **Then** the agent names that record and surfaces the
   contradiction rather than silently overriding it.

---

### User Story 3 - The methodology agent knows the ADR agent is a feeder (Priority: P2)

A team runs `methodology` after several significant ADRs have been accepted into the constitution. The
methodology agent's sibling-ground table names the ADR agent and the ground it owns, so methodology refers
architectural standards to the ADR agent rather than drafting its own clause for them, and its statement of
how many agents feed the constitution is accurate.

**Why this priority**: The methodology agent's table is the written map of who owns which clause. Leaving
the ADR agent off it keeps the map wrong, but the defect in Story 1 matters more.

**Independent Test**: Read the methodology agent's sibling-ground table; confirm it lists
`speckit.spectra.adr` with its ground and its output location, and that the feeder count matches.

**Acceptance Scenarios**:

1. **Given** the methodology agent, **When** its sibling-ground table is read, **Then** it contains a row
   for `speckit.spectra.adr` naming the ground the ADR agent owns and `<artifact-root>/adr/`.
2. **Given** the methodology agent's statement of how many agents feed the constitution, **When** it is
   read, **Then** it counts the ADR agent.
3. **Given** the methodology agent's ordered list of foundation feeders it suggests after its handoff,
   **When** it is read, **Then** the ADR agent is not added to it — ADRs are written on demand, one per
   decision, not as a foundation step.

---

### User Story 4 - A superseding ADR amends the clause its predecessor created (Priority: P3)

ADR-007 reverses ADR-002, whose guardrail was adopted into the constitution as a principle. The ADR agent
recognises that the constitution already carries the clause ADR-002 introduced and drafts ADR-007's
guardrail as an amendment to that principle, not as a second, contradictory one.

**Why this priority**: Supersession is less common than a first decision, but getting it wrong leaves two
contradictory clauses in the constitution.

**Independent Test**: With a constitution principle traceable to an earlier ADR, record a superseding ADR;
confirm its record names the principle it amends.

**Acceptance Scenarios**:

1. **Given** a constitution principle that an earlier ADR introduced, **When** a new ADR supersedes that
   ADR, **Then** the new record is marked as amending that principle by name.
2. **Given** a significant decision the constitution already states, **When** Step 7 runs, **Then** the
   agent quotes the governing clause and drafts nothing for it.

### Edge Cases

- **The user approves, then asks the agent to apply the change anyway.** The agent never writes the
  constitution, in any run, approved or not; it repeats the handoff line.
- **A non-interactive run, or no answer at the approval step.** Every drafted record is recorded as not
  asked; nothing is accepted, the Constitution input section says so, and no line is printed. Silence adopts
  nothing.
- **The resolved ADR template has no place for a Constitution input section** — including the shipped
  default and every project override written before this feature. The agent writes the section anyway, as
  the ADR's final section, and says so once; its format belongs to the command, not the template, because
  `/speckit-constitution` depends on it. A non-significant ADR still gets no section.
- **The ADR is `Proposed`, not yet accepted.** The handoff line is still given, and the agent states that the
  amendment should be run once the decision is accepted; the record shows the ADR's status at the time it was
  drafted.
- **The decision supersedes an ADR held in a legacy, read-only location.** Supersession handling is unchanged;
  the guardrail is still drafted as an amendment where the constitution carries the earlier clause.
- **The decision contradicts an existing constitution principle on the ADR agent's own ground.** The agent
  surfaces the contradiction as a finding and drafts the record as an amendment to that principle; it never
  drafts a clause that silently overrides one.
- **Step 8's commit suggestion.** It no longer lists the constitution file; it lists the ADR alone, and notes
  that the constitution change is committed after `/speckit-constitution` runs.
- **The project has no constitution.** Guardrails are still drafted, put to the user, and recorded; no line is
  printed; the user is pointed to `speckit.spectra.domain-analyzer` first, and told the ADR's accepted records
  can be amended in once a constitution exists.
- **A decision mixes an architecture-level choice with a language or framework** ("adopt event sourcing on
  Kafka, written in Kotlin"). The agent drafts for the architecture-level part only and refers the language
  part to `speckit.spectra.domain-analyzer`.
- **domain-analyzer runs after an ADR's guardrail was accepted.** Where the ADR's accepted record covers an
  architecture clause, domain-analyzer cites it and drafts nothing for that clause; it still drafts
  architecture clauses no accepted ADR record covers. A declined or not-asked ADR record never constrains it.
- **An ADR records a security or reliability decision.** The ADR agent drafts it; domain-analyzer's Security &
  trust boundaries or Reliability & operability lens later cites that accepted record instead of drafting the
  same clause.
- **An accepted guardrail's ADR was later superseded.** domain-analyzer ignores it; the superseding ADR's
  record, drafted as `amends:`, is what counts.
- **The artifact root is declared elsewhere.** The handoff line and link use the resolved root, never the
  default.

## Requirements *(mandatory)*

### Functional Requirements

**The invariant**

- **FR-001**: The ADR agent MUST NOT write `.specify/memory/constitution.md` in any run — not on approval,
  not when the file is missing, not when the user insists. Its list of things it never does MUST say so and
  give the reason: `/speckit-constitution` owns that file's version, impact report, and propagation.
- **FR-002**: The ADR agent MUST NOT invoke `/speckit-constitution`. It prints the command; the user runs it.

**Drafting**

- **FR-003**: When a decision is significant (Step 7's existing test), the agent MUST draft each guardrail
  the decision would make binding, on its own ground only (FR-008), in the constitution's voice: declarative
  and testable, MUST or SHOULD, with a brief rationale.
- **FR-004**: Each drafted guardrail MUST be a record carrying, in a fixed order: the statement, a stable
  id, the target constitution section, its basis (observed where the codebase already holds the rule,
  aspirational where it does not), the user's decision, and its status (new, amending a named principle, or
  already adopted). The record format MUST match the one the other four feeders use, with an id prefix
  that identifies the ADR agent.
- **FR-005**: The agent MUST read the constitution semantically before drafting. Where the constitution
  already states the guardrail, it MUST quote the governing clause and draft nothing for it. Where a
  principle contradicts the decision, it MUST surface the contradiction and draft an amendment to that
  principle, never a clause that silently overrides it.
- **FR-006**: Where the decision supersedes an ADR whose guardrail the constitution already carries, the new
  record MUST be drafted as amending that principle.

**The approval step**

- **FR-007**: The agent MUST show every drafted record and ask once, with the same choices the sibling
  feeders offer: approve all (individual records may be named to decline or reword, keeping their id),
  revise the ADR first, talk it through, decline all, or no answer. Declined-all records MUST be recorded as
  skipped; no answer or a non-interactive run MUST record them as not asked.

**Sibling ground**

- **FR-008**: The agent MUST NOT draft a guardrail on ground another feeder owns:
  - test levels, coverage floor, the ratchet, UAT → `speckit.spectra.test-strategy`;
  - environments, promotion, rollback, the versioning scheme, the release cut, hotfix promotion →
    `speckit.spectra.deployment-strategy`;
  - product languages, frameworks, dependency policy, bounded contexts, invariants, glossary terms →
    `speckit.spectra.domain-analyzer`;
  - methodology overlays, work modes, branching, review gates, change records → `speckit.spectra.methodology`.
- **FR-009**: For each part of a decision that falls on a sibling's ground, the agent MUST name the owning
  agent, say whether that agent's document exists at the artifact root, and suggest re-running it. Where that
  document exists, it MUST read its accepted records only and surface any one the decision contradicts. When
  the ADR agent reads prior ADRs' Constitution input sections (FR-005, FR-006), a `Superseded` or `Deprecated`
  ADR's records count only as the principle a supersession amends, never as a constraint.
- **FR-010**: The ADR agent's own ground MUST be stated in the command: **architecture-level choices** —
  datastores, messaging and eventing infrastructure, architecture style (for example monolith, modular
  monolith, services), service and data boundaries and ownership, layering, and integration patterns — plus
  architectural decisions on security, data handling, or reliability (for example mTLS between services, a
  data-retention mechanism, an observability stack), and conventions future work must follow that no sibling
  owns. Ground shared with domain-analyzer is governed clause by clause (FR-019). A decision naming a language, a framework, or a
  dependency rule is domain-analyzer's ground, even when it is recorded as an ADR.

**The Constitution input section and handoff**

- **FR-011**: When at least one record was drafted, the ADR MUST carry a Constitution input section holding
  exactly the records whose decision is accepted and whose status is not already adopted. It MUST open with
  the result of the constitution check and one line naming the goal, then group records by target section,
  each with its id, placement (add, or amends a named principle), and basis. If nothing was accepted, it MUST
  say so in one sentence.
- **FR-012**: The drafted records, accepted or not, MUST also be kept in the ADR, so the file records what
  was offered as well as what was chosen.
- **FR-013**: The Constitution input section's format belongs to the command. Where the resolved template
  does not place it, the agent MUST write it as the ADR's final section and say so once. A non-significant
  ADR MUST carry no such section.
- **FR-014**: When the Constitution input section is non-empty, the agent MUST print one ready-to-paste
  `/speckit-constitution` line that references the ADR by its actual resolved path, worded for the goal, and
  state plainly that nothing reaches the constitution until that command runs. When it is empty, the agent
  MUST print no line.
- **FR-015**: When the project has no constitution, the agent MUST NOT hand off a create goal. It MUST still
  run the approval step and record the guardrails in the ADR; the Constitution input section MUST open by
  saying no constitution exists and that its records are for a later amend. The agent MUST print no
  `/speckit-constitution` line, MUST point the user to the foundation agents with
  `speckit.spectra.domain-analyzer` first, and MUST say that once a constitution exists, the ADR's accepted
  records can be amended in from this file.
- **FR-016**: Step 8's optional commit suggestion MUST list only the ADR (and any superseded ADR it updated),
  never the constitution.

**Methodology agent**

- **FR-017**: The methodology agent's sibling-ground table MUST list `speckit.spectra.adr` with the ground
  defined in FR-010 and its output location `<artifact-root>/adr/`.
- **FR-018**: Every statement in the methodology agent of how many agents feed the constitution MUST count
  the ADR agent. Its ordered list of foundation feeders suggested after its handoff MUST NOT include the ADR
  agent.

**Domain-analyzer**

- **FR-019**: The domain-analyzer agent MUST state the same split from its side: its technology ground is
  product languages, frameworks, and dependency policy, and architecture-level choices (FR-010) belong to
  `speckit.spectra.adr`. Every lens except Technology & dependency policy MUST keep working what the code
  shows, but before drafting a clause it MUST read the Constitution input sections of the ADRs under
  `<artifact-root>/adr/` — accepted records only, and only from ADRs whose status is `Proposed` or
  `Accepted`; an ADR marked `Superseded` or `Deprecated` never constrains it — and cite an accepted record
  that covers a clause instead of drafting that clause. A clause no accepted ADR record covers MAY be drafted from observation. Whichever
  agent drafts a clause first is its source; a later ADR that changes it drafts an amendment (FR-005,
  FR-006), never a second clause.

**Unchanged**

- **FR-020**: Everything else the ADR agent does — context gathering, the five-question limit, numbering,
  template resolution, the artifact-root rules, supersession, and the significance test itself — MUST be
  unchanged.

### Key Entities

- **Guardrail record**: one drafted constitution clause inside an ADR — statement, frozen id, target section,
  basis, the user's decision, and status. Kept whether accepted or not.
- **Constitution input section**: the part of an ADR that `/speckit-constitution` consumes — only accepted,
  not-yet-adopted records, plus the constitution-check result and the goal.
- **Sibling ground**: the division of constitution subject matter among the five feeders, so each clause has
  exactly one source. domain-analyzer's ground, except Technology & dependency policy, is shared with the ADR
  agent — the ADR agent works it from recorded decisions, domain-analyzer from observation — and there the
  rule applies clause by clause: an accepted ADR record is cited, never re-drafted.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In every ADR run — approved, declined, insisted, non-interactive, or with no constitution — the
  constitution file is unchanged afterwards (0 writes across all scenarios in this specification).
- **SC-002**: 100% of significant ADRs with at least one accepted record, on a project that has a
  constitution, end with exactly one `/speckit-constitution` line that names that ADR's path; 0% of runs with
  nothing accepted, or with no constitution, print one.
- **SC-003**: For each of the four sibling grounds, an ADR whose decision lies wholly on that ground drafts 0
  records and names the owning agent.
- **SC-004**: A constitution amendment that came from an ADR can be traced back to that ADR from the
  constitution's change record in one step, because the handoff line names the ADR.
- **SC-005**: The methodology agent's sibling-ground table and feeder count agree with the five agents that
  hand off to `/speckit-constitution`.

## Assumptions

- The ADR agent writes a Constitution input section only for a significant ADR; ADRs are numerous and most
  will never touch the constitution, so an empty section in every ADR would be noise.
- The shipped ADR template is not required to change: the command owns the section's format and appends it
  when the template has no place for it (FR-013), the same rule `domain-analyzer` already follows.
- A `Proposed` ADR may still hand off; the user decides when to run the line, and the agent advises running it
  once the decision is accepted.
- The sibling feeders already read ADRs as evidence (`test-strategy`, `deployment-strategy`, `domain-analyzer`,
  and `methodology` all list ADRs among their inputs), so "re-run the owning agent" is a real route for a
  decision on their ground. Changing how they weigh ADRs is out of scope.
- Only the methodology agent's sibling-ground table and domain-analyzer's statement of its technology ground
  (FR-019) are updated. Test-strategy and deployment-strategy cite sibling ground in their own words; aligning
  their lists is out of scope unless the plan finds one that would contradict FR-008.
- The ADR agent is not added to any foundation onboarding sequence; it remains an on-demand agent.
- Out of scope: changing what makes a decision significant, the ADR's numbering or location, or letting any
  agent write the constitution.
