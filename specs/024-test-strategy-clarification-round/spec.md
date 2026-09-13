# Feature Specification: The Test Strategy Clarification Round

**Feature Branch**: `024-test-strategy-clarification-round`

**Created**: 2026-09-12

**Status**: Implemented

**Input**: Maintainer request — "right now the `test-strategy` agent is not interactive. I am considering making it
interactive so that before writing the document, it asks the users some questions, gives recommendation then goes
ahead."

## Current State (verified against 1.16.0)

`spectra/commands/test-strategy.md` runs start to finish without consulting the user on anything substantive. It stops
three times, and all three are mechanical or terminal:

| Stop | Step | What it asks |
|---|---|---|
| Artifact root | 4 | Where to write, when the default folder is published and no root is declared |
| Coverage run | 7 | Permission to execute the project's suite, so a figure can be labelled `measured` |
| Amendment gate | 12 | Approval of a constitution amendment, after the document already exists |

None of them is about the strategy. The agent derives the whole document from evidence, which is the right default and
the reason the agent is trustworthy — [020-test-strategy-agent](../020-test-strategy-agent/spec.md) hardened that into
FR-006, which forbids asking the user whether the project is greenfield or brownfield because that is "asking them for
something the agent is about to measure anyway."

Three things, however, are not measurable from the repository, and the document is weaker for guessing at them:

- **Which journeys deserve an end-to-end test.** Step 6 resolves the end-to-end *surface* from evidence — browser, HTTP,
  CLI, or none — and that part is sound. Which two or three journeys justify the most expensive lens is business
  knowledge that no manifest carries.
- **Whether an external consumer exists.** An internal HTTP handler and a published API look identical in a source
  tree. The answer flips the API contract lens between a whole section and one line of "not applicable."
- **What the organization forbids, as distinct from what the stack cannot run.** R5 refuses to name a tool whose
  prerequisites the surface lacks. It says nothing about a tool the stack *can* run and the team may not adopt — no
  container runtime in CI, a freeze on new dependencies, no network in the test environment, a compliance rule. A
  strategy built on a tool the team cannot adopt is precisely the plausible document the agent exists to avoid.

**Supersession.** This feature adds an interaction to [020-test-strategy-agent](../020-test-strategy-agent/spec.md) and
changes the session output order its `contracts/chat-output.md` fixes. That contract's ordering clause is replaced by
FR-014 below; every other clause of feature 020 stands, including FR-006 and the ban on writing the constitution.

## Clarifications

- Q: Does asking the user contradict the agent's evidence-first premise?
  → A: Only if it asks the wrong things. The governing line is **ask about judgment, intent, and constraint; never ask
  about anything you are about to measure.** FR-006's reasoning generalises: the mode, the stack, the surfaces, the
  frameworks in use, the coverage figure, and whether tests exist are all measured in Steps 1–3 or Step 7, and asking
  would invite a wrong answer to override a right one. What remains — the strategy's shape, external consumers,
  journey priority, known pain, organizational constraint — is underdetermined by any repository.

- Q: One question at a time, or all five at once?
  → A: **One at a time.** The questions are conditional on each other: whether an external consumer exists determines
  whether the contract lens exists at all, and where the weight sits changes how much the journey question matters. A
  batch forces each question to be written as if the others do not exist, which is how a project-specific interview
  becomes a generic questionnaire — the failure Principle IV exists to prevent. The round-trip cost of five turns is
  paid back by the escape hatches, not by batching.

- Q: Always five, even when the evidence settles one?
  → A: **Always five, but evidence reshapes a question rather than skipping it.** The forcing case is the journey
  question when the end-to-end surface resolves to `none`: "which journeys deserve an end-to-end test" is incoherent
  for a library with no entry point. It becomes a confirmation — *"this project has no browser, HTTP, or CLI entry
  point; confirm, or name a journey you want covered anyway?"* — and keeps its number. A fixed count makes the length
  of the commitment predictable; reshaping keeps every question answerable.

- Q: How is a user's answer distinguished from evidence?
  → A: With a third provenance marker, `stated`. R1 admits exactly two today — a cited project path, or `convention`
  for an unevidenced default. An answer is neither. Without the third marker an answer either launders into a fake
  citation or is mislabelled a convention, and R1 stops meaning anything. The document's promise is that a reader can
  tell measured from conventional, and now from asked-for.

- Q: Can an answer override a measurement?
  → A: **No**, and this needs its own rule because it is the obvious way the feature could corrupt the document. R3 is
  absolute: a user asking for a 90% floor against a 31% baseline does not move the floor. Answers shape judgment;
  they never move a measured or reported figure.

- Q: Does the round need an approval gate before the document is written?
  → A: No. The document is a singleton rewritten in place with Git carrying the history, and the amendment gate already
  offers "modify the strategy first." A second gate would add a failure path and a second divergence in non-interactive
  mode for a file that costs nothing to rewrite.

- Q: FR-028 of feature 020 says the agent summarises "before asking the user anything". Is that violated?
  → A: No — that requirement is scoped to the amendment gate, which is the only question feature 020 contemplated. The
  clarification round asks its questions before there are any recommendations to summarise. They are different
  interactions, and the command's wording is sharpened to say so.

- Q: Why does the coverage-run confirmation move?
  → A: So its answer is available to the five that follow. "Where should the weight sit" is a different question at 31%
  than at 78%. Moving it also collapses two separate interruptions into one round, which is the difference between a
  document that stops the user twice and one that stops them once.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The strategy reflects a decision the repository could not make (Priority: P1)

A maintainer runs the agent on a service. The repository shows a test directory, a coverage config, and an HTTP
framework, so the agent can measure the mode, the surfaces, and the baseline. It cannot tell whether the service's
endpoints are consumed by another team, whether the team wants weight on units or on integration, or that CI has no
container runtime. It asks those five things, one at a time, each with its own recommendation and the evidence behind
it, and writes a strategy that reflects the answers.

**Why this priority**: this is the feature. Everything else is the discipline that keeps it from degrading the
document.

**Independent Test**: run the command on a repository with a measurable baseline, answer all five questions, and verify
that each answer changed a named section of the document and is recorded with `stated` provenance.

**Acceptance Scenarios**:

1. **Given** an interactive session, **When** the round begins, **Then** a single announcement states the number of
   questions and the three ways out, and no question has yet been asked.
2. **Given** the round is running, **When** each question appears, **Then** it is numbered within the fixed total,
   offers between two and four labelled options, marks one as recommended, and states the project evidence behind the
   mark.
3. **Given** a question is answered, **When** the next appears, **Then** it is informed by the previous answers rather
   than written as if they did not exist.
4. **Given** all five are answered, **When** the document is read, **Then** every recommendation that rests on an answer
   carries `stated` provenance and is traceable to the question that produced it.
5. **Given** the run completes, **When** the working tree is inspected, **Then** the only change is the strategy
   document.

### User Story 2 - Declining costs nothing (Priority: P1)

A maintainer wants the document, not the interview. They say "use your defaults" at the first question, or answer
nothing at all. The agent proceeds on its own recommendations and produces the document it would have produced before
this feature existed.

**Why this priority**: it is what makes the feature safe to add. If declining is not free, an interactive agent is a
worse agent for everyone who was happy with the previous one.

**Independent Test**: run the command twice on the same repository — once declining every question, once with the flag
— and verify the two documents differ only in how the questions are recorded.

**Acceptance Scenarios**:

1. **Given** any point in the round, **When** the user asks to proceed with defaults, **Then** every remaining question
   takes its recommended answer and the round ends immediately.
2. **Given** the user abandons the round part-way, **When** the document is written, **Then** the answered questions are
   recorded as answered and the rest as not asked with the default taken.
3. **Given** a session that cannot take an answer, **When** the run starts, **Then** it says so once, asks nothing, and
   records all five as not asked.
4. **Given** a run in which nothing was answered, **When** the document is compared to one produced before this feature,
   **Then** the recommendations are the same.

### User Story 3 - An answer cannot launder itself into evidence (Priority: P2)

A maintainer answers that the coverage floor should be 90%. The measured baseline is 31%. The agent holds the floor at
the baseline, records the disagreement, and does not present the user's preference as a finding about the repository.

**Why this priority**: the failure mode this whole agent exists to prevent is a document that reads well and cannot be
trusted. A user's opinion rendered as evidence is exactly that.

**Independent Test**: answer a question in a way that contradicts a measured figure and verify the figure is unchanged,
the disagreement is recorded, and the answer is marked `stated` rather than cited.

**Acceptance Scenarios**:

1. **Given** an answer that would raise the floor above the baseline, **When** the floor is derived, **Then** it remains
   at or below the baseline and the disagreement is recorded in the document.
2. **Given** any recommendation resting on an answer, **When** its provenance is read, **Then** it is `stated` — never a
   path, never `convention`.
3. **Given** the recorded answers, **When** the document is read, **Then** the question, the recommendation, the answer,
   and its disposition are all recoverable.

### Edge Cases

- **The user asks a question instead of answering one** — it is answered, then the same question is re-asked. The round
  does not advance, and an off-topic reply is not a declination.
- **The user answers several questions at once** — accepted. The announcement offers it, and a maintainer who already
  knows their answers should not be made to spend five turns.
- **An answer fits none of the options** — accepted as free text. The options are scaffolding, not a closed menu.
- **The end-to-end surface resolves to `none`** — the journey question becomes a confirmation rather than being dropped.
- **A published manifest already settles the external-consumer question** — it is presented as a confirmation, for the
  same reason.
- **The project has no coverage tooling to run** — there is no coverage confirmation to ask, the baseline is
  `unavailable`, and the five proceed unchanged.
- **A re-run on a project already analysed** — the prior document's recorded answers pre-fill each question, so the
  round confirms rather than re-interrogates.
- **An unrecognised flag is supplied** — reported and ignored. It never silently becomes part of the focus hint.

## Requirements *(mandatory)*

### The round

- **FR-001**: The command MUST ask a fixed set of five clarifying questions before the document is written, covering the
  strategy's shape, external consumers, end-to-end journey priority, known failure history, and organizational
  constraints the repository does not express.
- **FR-002**: The command MUST state the rule that governs what may be asked — judgment, intent, and constraint only —
  and MUST name the facts it may never ask about, being the mode, the stack, the surfaces, the frameworks in use, the
  coverage figure, and whether tests exist.
- **FR-003**: Each question MUST be asked on its own, MUST be numbered within the fixed total, MUST offer between two
  and four labelled options with exactly one marked as recommended, and MUST state the project evidence behind that
  mark or label it as a convention.
- **FR-004**: The command MUST state that the options are not exhaustive and that free text is a valid answer.
- **FR-005**: Before the first question, the command MUST announce the number of questions and MUST name three ways out:
  answering several at once, taking the recommendations wholesale, and declining.
- **FR-006**: Where evidence settles a question, the command MUST present it as a confirmation rather than an open
  choice, and MUST NOT drop it or renumber the remainder.
- **FR-007**: The coverage-run confirmation MUST be asked as part of this round and before the five, so the baseline it
  establishes is available to them. Its existing conditions are unchanged: it names the exact command, warns that the
  suite will execute, and is declinable.
- **FR-008**: The round MUST occur after the artifact root is resolved and before the document's template is resolved,
  so every question can name real paths in this project.

### What an answer may and may not do

- **FR-009**: The command MUST recognise a third provenance, `stated`, for a recommendation that rests on a user's
  answer, alongside a cited project path and the existing `convention` marker.
- **FR-010**: An answer MUST NOT change a measured or reported figure. The coverage floor MUST remain at or below the
  baseline regardless of what any answer requests.
- **FR-011**: Where an answer contradicts the project's evidence, the command MUST make the change where it is
  legitimate and MUST record the disagreement in the document rather than silently adopting or silently discarding it.

### Recording

- **FR-012**: The document MUST record every question with its recommended answer, the answer taken, and a disposition
  of answered, default taken, or not asked.
- **FR-013**: That record MUST live inside the existing sources-and-coverage section rather than as a new top-level
  section, and MUST also appear in the document's front matter so it survives a template override that reshapes that
  section.
- **FR-014**: The session output order MUST be: the non-interactive announcement where one applies, the artifact-root
  choice where one applies, the clarification round, the document write, the summary of recommendations, and the
  amendment gate.

### Declining, and sessions that cannot answer

- **FR-015**: A request to proceed with the recommendations MUST end the round immediately, taking the recommended
  answer for every remaining question.
- **FR-016**: A question left unanswered MUST take its recommended answer and be recorded as not asked, and the run MUST
  continue rather than blocking.
- **FR-017**: A reply that does not answer the question MUST be addressed, after which the same question is asked again.
  It MUST NOT be treated as a declination and MUST NOT advance the round.
- **FR-018**: A run in which no question is answered MUST produce the same recommendations as a run of the command
  before this feature.
- **FR-019**: The command MUST accept a `--non-interactive` flag declaring that no answer can be taken. The flag MUST be
  removed before the remainder is read as the existing optional focus hint, and an unrecognised flag MUST be reported
  and ignored rather than absorbed into that hint.
- **FR-020**: In a non-interactive session the command MUST ask none of the five, MUST record each as not asked, and
  MUST otherwise write and report as normal.

### Re-running

- **FR-021**: On a re-run the command MUST read the prior document's recorded answers and MUST offer each as the
  pre-filled answer to its question, so the round confirms rather than re-interrogates.

### Boundaries and release

- **FR-022**: The round MUST NOT introduce a second document, a second write, or an approval gate before the write. The
  run still produces exactly one file.
- **FR-023**: The command MUST still never write `.specify/memory/constitution.md`, in any run, under any answer.
- **FR-024**: No named browser driver may appear in the command's text, including in any example answer.
- **FR-025**: The test suite MUST assert every clause above that lives in the command's text, including that the
  never-ask list names the measured facts and that the recorded provenance vocabulary carries all three markers.
- **FR-026**: The extension version MUST bump to `1.17.0` — a new interaction is added and every existing invocation
  still works — with manifest, catalog, changelog, and zip in sync.

## Success Criteria *(mandatory)*

- **SC-001**: A maintainer who answers all five questions gets a document in which every answer is traceable to the
  question that produced it and to the section it changed.
- **SC-002**: A maintainer who declines everything gets the document the previous version would have produced, and the
  run costs them one reply.
- **SC-003**: A reader of any produced document can tell, for every recommendation, whether it rests on something
  measured in the repository, a convention with no evidence, or something the team stated.
- **SC-004**: No answer, however stated, produces a coverage floor above the project's baseline.
- **SC-005**: A run with no terminal produces a complete document and asks nothing.
- **SC-006**: `python3 -m unittest discover -s tests`, `tools/generate_agent_docs.py --check`, and a
  `tools/build_package.py` rebuild all pass.

## Assumptions

- Command files are prompts: the enforceable surface is their text plus the tests over it. "Asks one question at a time"
  is a written instruction to the host agent, not a control flow anything can verify mechanically.
- The host agent can end a turn and wait for a reply. Every integration Spec Kit targets can, and the command names no
  agent's syntax for doing it (Principle III).
- Five is a budget, not a discovery. The questions are fixed because a variable-length interview cannot be announced
  honestly up front, and predictability is worth more here than marginal coverage.
- Recording answers in front matter as well as in the body is redundancy on purpose: Principle VIII lets a project's
  template override delete the section that holds the table, and the provenance record must survive that.
