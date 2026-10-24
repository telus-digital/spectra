# Feature Specification: An Interactive Domain Analyzer That Feeds the Constitution

**Feature Branch**: `034-interactive-domain-analyzer`

**Created**: 2026-10-23

**Status**: Implemented

**Input**: User description: "Make speckit.spectra.domain-analyzer interactive and consistent with how
speckit.spectra.test-strategy flows, with its output existing to feed the constitution. The typical run is a
brownfield codebase with no constitution. (1) On start, say whether a constitution was found: if so the goal is
to update it, if not to generate it. (2) Always work seven lenses, each mapped to a constitution section;
testing and deployment are referred to their own agents. (3) Every candidate cites a file and is tagged
observed or aspirational. (4) Ask in the session instead of checkboxes in the file: eight questions, one per
turn, each with at least four options, one recommended and one Skip. (5) Write the file only after all
answers, keeping the name DOMAIN_ANALYSIS.md, with a Constitution input section. (6) End by suggesting
/speckit-constitution with a create or update prompt, never invoking it. (7) Re-runs pre-fill answers, never
re-offer a declined guardrail, keep stable IDs, mark adopted items, and read the old checkbox format. The
implementation already exists in the working tree; the spec describes that behaviour."

## Current State (verified against extension 1.22.0)

| Question | `speckit.spectra.domain-analyzer` at 1.22.0 |
|---|---|
| When does the SME decide? | **After the agent has left.** Every candidate is written as an unticked checkbox, and the SME ticks the file by hand before running `/speckit-constitution`. `test-strategy` and `deployment-strategy` both decide in the session and record the answers; this agent is the odd one out. |
| What does the agent examine? | **Unfixed.** Candidates are grouped under whatever constitution sections the agent picks, so two runs on the same project can examine different things, and an empty area cannot be told from an unexamined one. |
| Does the run say what it is for? | **Not until late.** The constitution's presence is checked mid-run, so the SME is never told up front whether this analysis will create a constitution or amend one. |
| Can the SME see which guardrails the code already meets? | **No.** A rule the codebase follows and a rule it breaks look identical, though on a brownfield project only the second creates debt when ratified. |
| Can it propose testing or deployment rules? | **Yes.** Those agents hand their own amendments to the constitution, so the same clause can arrive from two sources and contradict itself. |

## Clarifications

### Session 2026-10-23

- Q: When the agent re-runs on a file from the old checkbox version, should an unticked guardrail count as declined or as undecided? → A: Undecided. Unticked items come back in their lens's question, marked "unticked in the earlier version"; ticked items are read as accepted.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Decide guardrails in the session, not in the file (Priority: P1)

An SME runs the domain analyzer on an existing codebase. The agent reads the project, then asks one question
per turn — the inferred domain first, then one per lens. Each question lists that lens's candidate guardrails
and offers at least four options, including the agent's recommendation and Skip. When the last question is
answered, the agent writes `<artifact-root>/DOMAIN_ANALYSIS.md` with every decision already recorded and the
accepted guardrails gathered into a Constitution input section.

**Why this priority**: This is the change the user asked for. Without it the agent still depends on the SME
editing a file after the session, which is where decisions get skipped or forgotten.

**Independent Test**: Run the agent on a project, answer the eight questions, and confirm no file exists until
the last answer, then that the file records each answer and the Constitution input section holds exactly the
accepted guardrails.

**Acceptance Scenarios**:

1. **Given** any run, **When** a question is asked, **Then** it offers at least four distinct options, exactly
   one marked recommended with the evidence behind it, one of them Skip, and states that a free-text answer is
   valid.
2. **Given** the round is in progress, **When** fewer than eight questions have been answered, **Then** no
   document has been written.
3. **Given** the SME says "use your defaults", **When** questions remain, **Then** the recommended option is
   taken for each remaining question, recorded as `default_taken`, and the round ends.
4. **Given** the SME skips a lens, or leaves its question unanswered, **When** the document is written, **Then**
   none of that lens's candidates appears in the Constitution input section.
5. **Given** the SME replies "3.1 and 3.3, reword 3.3 to SHOULD", **When** the document is written, **Then**
   3.1 and 3.3 are accepted, 3.3 carries the new wording under its original ID, and the lens's other
   candidates are declined.

---

### User Story 2 - Know the run's goal from its first line (Priority: P1)

Before any analysis output or question, the agent says whether it found a constitution and therefore whether
this run's goal is to **generate** the constitution or **update** it. The goal is recorded in the document and
decides the wording of the final handoff.

**Why this priority**: The whole analysis exists to become constitution input. Whether that input creates a
constitution or amends one changes what every candidate means, so the SME should know before answering.

**Independent Test**: Run once with no constitution and once with one, and confirm the first output and the
handoff differ accordingly.

**Acceptance Scenarios**:

1. **Given** no constitution exists, **When** the run starts, **Then** the first output says none was found and
   that the goal is to generate it from this analysis.
2. **Given** a constitution exists, **When** the run starts, **Then** the first output names it, with its
   version and principle count where stated, and says the goal is to update it.
3. **Given** a constitution file that is empty or unreadable, **When** the run starts, **Then** it is reported
   as such and treated as absent.
4. **Given** the goal is generate, **When** the run ends with accepted guardrails, **Then** the handoff is a
   ready-to-paste `/speckit-constitution` line that creates the constitution from the Constitution input
   section; **given** the goal is update, the line amends the existing constitution instead.
5. **Given** nothing was accepted, **When** the run ends, **Then** no `/speckit-constitution` line is given and
   the SME is told how to get there.

---

### User Story 3 - A fixed set of lenses, honest about the code (Priority: P1)

Every run works the same seven lenses, each feeding a constitution section: Domain & business rules; Data
sensitivity & regulation; Security & trust boundaries; Architecture & boundaries; Technology & dependency
policy; Reliability & operability; Delivery & workflow. Every candidate cites a project file and is tagged
`observed` (the code already follows it) or `aspirational` (it does not). Testing and deployment policy is
referred to `speckit.spectra.test-strategy` and `speckit.spectra.deployment-strategy`.

**Why this priority**: A fixed set lets a reader tell "found nothing" from "never looked", and the
observed/aspirational tag is the one fact a brownfield SME most needs before ratifying a rule.

**Independent Test**: Run on a project where one lens has nothing to propose and confirm that lens still
appears, says what was searched, and still gets its question.

**Acceptance Scenarios**:

1. **Given** any run, **When** the document is written, **Then** it has a section for each of the seven
   lenses.
2. **Given** a lens with no candidates, **When** its question is asked, **Then** it is a confirmation that keeps
   its number and still offers four options, one of them Skip.
3. **Given** any candidate, **When** it is presented or recorded, **Then** it cites at least one project file
   and is tagged `observed` or `aspirational`.
4. **Given** evidence about test levels, coverage, environments, or rollback, **When** lenses are worked,
   **Then** no candidate is proposed in that ground; the relevant sibling document is cited or its command is
   named.
5. **Given** the SME corrects the domain in question 1, **When** question 2 is asked, **Then** the lens
   candidates reflect the corrected domain.

---

### User Story 4 - Re-runs respect earlier decisions (Priority: P2)

On a project analysed before, the agent rewrites the same file. Each question offers the previous answer as
its proposed answer, declined guardrails are not offered again as new, guardrails keep their IDs, and accepted
guardrails that the constitution now carries are marked adopted and leave the Constitution input section.

**Why this priority**: Teams re-run after the code or constitution moves. Asking an SME to reject the same
guardrail twice, or re-adopting one already in force, erodes trust in the agent.

**Independent Test**: Run twice on the same project, adopting some guardrails via `/speckit-constitution` in
between, and confirm the second run's questions and Constitution input reflect the first run's decisions.

**Acceptance Scenarios**:

1. **Given** a prior document, **When** a question is asked, **Then** the prior answer is offered as its
   proposed answer.
2. **Given** a candidate declined last run, **When** the same guardrail is regenerated (same ID or same intent
   in the same section), **Then** it is not offered as new, and the question mentions how many were declined.
3. **Given** an accepted candidate the constitution now asserts, **When** the re-run completes, **Then** its
   status is `adopted: <principle>` and it is absent from the Constitution input section.
4. **Given** an adopted item whose principle was later removed, **When** re-run, **Then** the status stays
   adopted and the drift is reported.
5. **Given** a document in the earlier checkbox format, **When** re-run, **Then** ticked items are read as
   accepted, unticked items are read as undecided (`not_asked`) and offered again in their lens's question marked
   "unticked in the earlier version", IDs and wording are kept, and the file is rewritten in the new format.

---

### Edge Cases

- **Non-interactive run** (declared by flag or by the user, never inferred): no question is asked, every
  candidate is recorded `not_asked`, the Constitution input section is empty, and no `/speckit-constitution`
  line is given.
- **A reply that is not an answer** (a question back, a request to explain): the agent answers it and asks the
  same question again; the round does not advance.
- **Two lens options would take the same candidates** (the recommendation is the observed set, or the lens has
  one candidate): the duplicate becomes "Choose individually", so four options always mean four things.
- **Greenfield project**: nearly every candidate is `aspirational`; that is reported, not hidden.
- **Regulated domain**: an advisory-only note recommends the matching compliance add-on; nothing is enabled.
- **The default `docs/` folder is published**: the SME chooses the folder before the round, outside the eight
  questions; where no choice can be obtained, the non-publishing folder is used.
- **A project template override omits the Constitution input section**: the section is written anyway and the
  omission reported, since without it nothing can be handed off.
- **The file cannot be written**: the failure is reported and the document is shown in the session instead.
- **A prior candidate's evidence file is gone**: the candidate is kept and the missing evidence reported.
- **A PR review reads the analysis**: `speckit.spectra.review-pr` cites only accepted guardrails from it; a
  guardrail the SME declined is never raised as a finding.
- **The pre-1.19.0 location `.specify/memory/domain-analysis.md` exists**: it is read for prior decisions,
  reported once with a removal command, and never modified.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The agent MUST state, as its first output, whether a constitution was found and whether the
  run's goal is therefore to generate or update it.
- **FR-002**: The agent MUST work all seven lenses on every run and MUST NOT omit one; a lens with nothing to
  propose MUST say what was searched and where.
- **FR-003**: Each lens MUST map to a constitution section, using the existing constitution's section names
  where one exists.
- **FR-004**: The agent MUST NOT propose testing or deployment policy, and MUST refer that ground to
  `speckit.spectra.test-strategy` and `speckit.spectra.deployment-strategy`.
- **FR-005**: Every candidate MUST cite at least one project file and MUST be tagged `observed` or
  `aspirational`.
- **FR-006**: The agent MUST propose at most five candidates per lens.
- **FR-007**: When a constitution exists, the agent MUST suppress candidates it already asserts and MUST mark
  candidates that would change a principle as `amends: <principle>`.
- **FR-008**: The agent MUST ask exactly eight questions — the domain, then one per lens — one per turn,
  numbered within the total, after announcing the round once with its ways out.
- **FR-009**: Every question MUST offer at least four distinct labelled options, exactly one marked
  recommended with its evidence, and one of them Skip; free text MUST always be accepted.
- **FR-010**: A lens question's options MUST be Recommended set, Codify only what exists, Full set, and Skip,
  with a coinciding option replaced by Choose individually.
- **FR-011**: A question with nothing to choose MUST become a confirmation that keeps its number and its four
  options.
- **FR-012**: Skip, an unanswered question, and a non-interactive run MUST adopt nothing; "use your defaults"
  MUST take the recommended option for every remaining question.
- **FR-013**: The agent MUST write exactly one file, to `<artifact-root>/DOMAIN_ANALYSIS.md` (default
  `docs/DOMAIN_ANALYSIS.md`), and only after the round ends.
- **FR-014**: The document MUST record every candidate offered with its ID, section, evidence, basis,
  confidence, decision (`accepted`, `declined`, `skipped`, `not_asked`), and status (`new`, `amends:`,
  `adopted:`), and MUST record all eight questions with the recommended option, the answer, and its
  disposition.
- **FR-015**: The document MUST contain a Constitution input section holding exactly the accepted candidates
  not already adopted, naming the goal and each guardrail's placement.
- **FR-016**: The agent MUST end with one ready-to-paste `/speckit-constitution` line worded for the goal, or
  with none when the Constitution input section is empty.
- **FR-017**: The agent MUST NOT write the constitution, invoke `/speckit-constitution`, modify any other file,
  or make a network request.
- **FR-018**: A candidate's ID MUST be computed once and frozen; re-runs MUST match prior candidates by
  recorded ID or by same intent within the same section.
- **FR-019**: Re-runs MUST pre-fill each question with the prior answer, MUST NOT re-offer a declined
  candidate as new, MUST NOT delete any prior candidate, and MUST mark accepted candidates the constitution now
  asserts as adopted without ever reverting an adopted status.
- **FR-020**: A document in the earlier checkbox format MUST be read as prior decisions — a ticked item is
  accepted; an unticked item is undecided — recorded as `not_asked` until a question answers it — and MUST
  be offered again in its lens's question, marked "unticked
  in the earlier version", because the old format cannot distinguish "reviewed and rejected" from "never
  reviewed" — and rewritten in the current format.
- **FR-021**: The document's structure MUST come from the overridable `domain-analysis-template`; the record
  format, front matter, and Constitution input format MUST stay owned by the agent.
- **FR-022**: Any agent that reads `DOMAIN_ANALYSIS.md` as a standard MUST treat only guardrails whose
  decision is `accepted` as binding; `declined`, `skipped`, and `not_asked` candidates are a record of what
  was offered, never a standard.

### Key Entities

- **Candidate guardrail**: one proposed rule — statement, frozen ID, lens, target section, evidence paths,
  basis (`observed`/`aspirational`), confidence, decision, status.
- **Question**: one of eight — what was asked, the recommended option, the answer taken, the disposition
  (`answered`, `default_taken`, `skipped`, `not_asked`).
- **Constitution input**: the accepted, not-yet-adopted guardrails grouped by section, with the run's goal —
  what `/speckit-constitution` consumes.
- **Run goal**: `create` or `update`, decided by whether a constitution exists.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An SME completes a run, from first output to handoff, without opening the document to make any
  decision.
- **SC-002**: A run on a project with no constitution ends with a single command that creates one, in 100% of
  runs where at least one guardrail was accepted.
- **SC-003**: Every run asks exactly eight questions (zero in non-interactive mode), and every question offers
  at least four options with exactly one recommended and one Skip.
- **SC-004**: 100% of candidates in the document cite a project file and carry an observed/aspirational tag.
- **SC-005**: On a re-run with no change to code or constitution, zero previously declined guardrails are
  offered as new and zero adopted guardrails appear in the Constitution input section.
- **SC-006**: The repository's test suite and the generated-listings check pass with the change in place.

## Assumptions

- The filename stays `DOMAIN_ANALYSIS.md`. It is already named as a singleton in the constitution's
  Principle VII and read by other agents, so renaming would add migration with no benefit.
- Constitution sections default to Spec Kit's standard constitution headings when no constitution exists.
- An unanswered question adopting nothing is deliberately stricter than `test-strategy`, where an unanswered
  question takes the recommendation: here the answer becomes governance, so silence is not consent.
- This is a minor version change to the extension (1.22.0 → 1.23.0): the command name, its arguments, and its
  output path are unchanged; only the interaction and the document format change.
- The constitution's Principle VII wording about "an SME's ticks" is updated as a wording-only (PATCH) change,
  1.11.0 → 1.11.1, since the agent no longer uses ticks.
- The implementation already exists in the working tree; planning and tasks will reconcile against it rather
  than rebuild it.
