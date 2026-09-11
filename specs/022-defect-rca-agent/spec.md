# Feature Specification: Defect Root Cause Analysis Agent

**Feature Branch**: `022-defect-rca-agent`

**Created**: 2026-09-11

**Status**: Implemented

**Input**: Business Requirements Document `BRD-DEFECTRCA-001 v2.0.0` — "Defect Root Cause Analysis
Agent — Structured RCA Advisor" (TELUS Digital Quality Engineering Practice / Product Team, created
2026-08-26, last updated 2026-09-11). The BRD specifies an AI advisor that guides Quality Engineering
practitioners through hypothesis-driven root cause analysis: it accepts a defect from a JIRA ticket, a
plain-language prompt, or a GitHub issue URL; reads the project constitution; searches prior RCA
documents for recurrence; analyzes source code, configuration, tests and commit history; forms and
tests hypotheses, asking the human only for what the repository cannot yield; and writes a Root Cause
Analysis Document conforming to a fixed template (BRD Appendix A) under a sequential
`nnn-defect-name` identifier. Its thirty business requirements (BR-01 – BR-30), ten success metrics
(SC-01 – SC-10), scope boundaries, constraints and output contract are carried into this
specification and cited by BR/SC id where a requirement below implements one.

## Clarifications

### Session 2026-09-11

The BRD is unusually complete, so most of what follows records how it lands against Spectra's own
constitution rather than resolving genuine ambiguity. Three items are deliberate departures from the
BRD's literal text and are called out as such.

- Q: The BRD hard-codes the output folder as `docs/defect-rca/` in fifteen places (BR-22, BR-24,
  BR-25, BR-28, Section 15). Principle VII makes the artifact root **declarable** — `docs/` is only
  the default — and requires a publication check before defaulting into it. Which applies? → A:
  **Principle VII applies; this is a departure from the BRD's literal path.** Output goes to
  `<artifact-root>/defect-rca/`, resolving an `Artifact root:` line in the project's constitution
  first, and checking for the documentation-publication signal (`mkdocs.yml`, `docusaurus.config.*`,
  `docs/_config.yml`, `docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, a Pages configuration
  pointing at `docs`) before defaulting. The BRD's `docs/defect-rca/` is what that resolution yields
  on a project that declares nothing and publishes nothing — the common case, not a different rule.
  The departure matters in one direction only: on a project that publishes `docs/`, writing there
  would serve a document containing production defect detail, stack traces and customer-impact
  figures to the public web, which is precisely the harm Principle VII's publication check exists to
  prevent and which the BRD's own sensitive-data risk names. Where the choice cannot be obtained the
  non-publishing root is taken (FR-040 – FR-042).

- Q: BRD Appendix A declares itself "binding under BR-23" and embeds the RCA document structure in
  the requirements document. Principle VIII requires every durable Markdown deliverable to take its
  shape from a **registered, overridable** template asset resolved through Spec Kit's stack. Which
  wins? → A: **Both, in layers.** Appendix A becomes the shipped default template at
  `spectra/templates/defect-rca-template.md`, registered in `spectra/extension.yml` under
  `provides.templates`, and is resolved through the stack so a project override at
  `.specify/templates/overrides/defect-rca-template.md` replaces it wholesale (FR-048 – FR-052).
  Appendix A is therefore binding as *Spectra's* default and not as an unconditional output contract:
  a team that overrides it gets its own sections, in its own order, and the agent honours them rather
  than repairing them. What stays with the command — and survives any override — is the set of rules
  the command owns: symptom-versus-root-cause distinction, answer-first ordering, the requirement to
  record invalidated hypotheses, the evidence-source attribution, the advisory status line, and the
  prohibition on reproducing a secret (FR-053).

- Q: The BRD requires JIRA ticket retrieval as a P1 MUST (BR-15, BR-16) but Spectra ships Markdown
  only — no scripts, no binaries, no post-install hooks — and there is no universally available JIRA
  CLI to depend on the way `gh` is depended on for GitHub. How is the channel satisfied? → A:
  **Through the host agent's harness, with graceful degradation, and never by handling a
  credential.** Spectra runs inside the coding agent a team already uses and inherits its reach and
  its limits: whatever JIRA access that agent already has — an MCP connector, a configured CLI, an
  internal service — the command uses, and it uses nothing else. Where no such access exists, or
  retrieval fails, the command says so plainly, asks the user to paste the ticket content, and
  proceeds treating the reference as a plain-language description (BR-18). It MUST NOT prompt for,
  accept, or store a JIRA credential, API token, or password, and MUST NOT attempt to authenticate
  (FR-011 – FR-013). The same degradation path covers `gh` being absent or unauthenticated.

- Q: The BRD leaves open whether a generated index (`docs/defect-rca/README.md`) should be
  maintained, calling it "a readability question rather than a functional gap". → A: **Yes, an index
  is maintained** — and it is a functional matter, not only a readability one. The BRD's own risk
  register names prior-RCA search degrading as the corpus grows, and the mitigation it proposes is a
  cheap flat-file scan. An index row carrying the defect id, the symptom, the validated root cause,
  the related prior RCA and the preventive-action status turns that scan into one file read instead
  of N, and is what makes the recurrence check under BR-28/BR-29 stay reliable past a few dozen
  documents. It also matches the shipped house pattern: `speckit.spectra.impact` maintains exactly
  such an index at `<artifact-root>/impact-analysis/README.md`. The index is rebuilt from the
  documents present, so a hand-deleted or hand-added file self-corrects (FR-044 – FR-047).

- Q: BRD SC-05 sets RCA document completeness at ≥ 85% of the nine BR-06 elements. Should the spec
  carry that bar? → A: **No — the bar here is 100%, and the reason is structural.** In the BRD,
  completeness was a behavioural target because the sections were described in prose. Here the
  document's shape comes from a resolved template the command MUST honour without omitting sections,
  so a missing element is a defect in the command rather than a miss in a distribution. The
  judgement-based metrics — analysis depth, root-cause level, hypothesis discipline — keep the BRD's
  percentages, because those measure the quality of reasoning and not the presence of a heading
  (SC-005, SC-001 – SC-004).

- Q: Which roster phase does the agent belong to? → A: **`testing-quality`.** The phase records *when
  you run an agent*, not what topic it covers. This one runs when a defect has been found — by a
  failing test, by QE, or in production — which places it alongside `flaky-test-detector` rather than
  in `deployment-operations`, where the planned `incident-responder` already covers live incident
  handling. An RCA is the post-hoc analysis of a defect, not the response to an outage.

- Q: BR-14 says the user SHOULD be able to "edit, annotate, and export the hypothesis tree, question
  list, and session notes alongside the RCA Document". Does that mean a second written artifact? →
  A: **No. Working artifacts are rendered in the session and never written to disk.** Principle VII
  gives each artifact *type* its own subfolder, so a written hypothesis tree would need one of its
  own, and the BRD itself excludes these from the output contract and from the RCA folder. The
  command renders them in full during the conversation — where they are already editable and
  copyable — and writes exactly the RCA document and the index row (FR-036, FR-037). "Export" is
  satisfied by rendering, not by a file.

- Q: What happens in a session that cannot take answers — a non-interactive or automated run — given
  the analysis loop is human-in-the-loop by design (BR-04)? → A: **Proceed on repository evidence
  alone, write the document, and record every unanswered question as an open data gap with the
  confidence consequence stated.** A document that names what it could not establish is useful; a
  refusal is not. What the command MUST NOT do is answer its own questions, infer a runtime fact it
  never observed, or present a hypothesis as validated on repository evidence that cannot settle it
  (FR-031 – FR-033).

- Q: The Appendix A header carries "Author / Date" and "Status — Advisory, conclusions owned by [QE
  name]". Where does a human name come from? → A: **From the repository's configured Git author,
  offered for correction, and never invented.** Where no name can be read, the field records that the
  owner is unassigned and the command says so, rather than filling it with a plausible name. The
  status line is never softened, dropped, or reworded — it is what makes the document advisory
  (BR-09, FR-027).

- Q: Does the command modify `/speckit-specify`, `/speckit-implement`, or register a hook so the
  workflow suggests it? → A: **No.** Nothing outside the new command file, its template, and the
  sync artifacts Principle V requires is touched. A hook would make every project that installs
  Spectra prompt for an RCA on flows where no defect exists; discovery is the roster's job.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start the analysis with the evidence already gathered (Priority: P1)

A QE engineer has a defect — a JIRA ticket, a GitHub issue, or just a description of what went wrong.
They invoke the command with it and, instead of being handed a questionnaire, they get back what the
repository already knows: the code paths implicated, the recent commits that touched them, the
configuration and tests involved, which constitution principles bear on the analysis, a MECE
hypothesis tree of where the cause could live, and a short prioritized list of the things only a human
can supply.

**Why this priority**: This is the step that converts an hour of manual code archaeology into a
minute, and it is the precondition for every other story. Without it the agent is a questionnaire.

**Independent Test**: Invoke the command against a repository with a seeded defect description and
confirm it returns a hypothesis tree, a summary of the code and commits it examined, and a question
list — with no prior RCA corpus, no constitution, and no ticket system reachable.

**Acceptance Scenarios**:

1. **Given** a GitHub issue URL and a working, authenticated `gh`, **When** intake runs, **Then** the
   issue body and its comments are retrieved without the user pasting anything.
2. **Given** a JIRA ticket reference and JIRA access available through the host agent, **When** intake
   runs, **Then** the ticket content is retrieved and used.
3. **Given** a JIRA reference or GitHub URL that cannot be retrieved, **When** intake runs, **Then**
   the command states why, asks for the content to be pasted, and continues treating the reference as
   a plain-language description — without prompting for any credential.
4. **Given** a plain-language description and no ticket at all, **When** intake runs, **Then** the
   command proceeds on the description alone.
5. **Given** a project constitution exists, **When** intake completes, **Then** the command names the
   principles that bear on this analysis and cites them by heading.
6. **Given** a defect description such as "API returns 500 under concurrent load", **When** intake
   completes, **Then** the output carries a hypothesis tree of at least five branches, a statement of
   which code, configuration, tests and commits were examined, and a prioritized question list.
7. **Given** intake output, **When** the user reads it, **Then** every conclusion is framed as
   advisory and every claim about the code cites the file it came from.

---

### User Story 2 - Catch the defect we have already fixed once (Priority: P1)

The same defect has surfaced before. Six months ago someone wrote an RCA for it, prescribed a
preventive action, and the action was never finished. The engineer starting today's analysis is told
that at intake — while the investigation is still open — rather than discovering it after writing a
second document that reaches the same conclusion.

**Why this priority**: Recurrence is the failure mode the whole artifact corpus exists to detect, and
a match surfaced after synthesis is a match surfaced too late to change the analysis.

**Independent Test**: Seed the RCA folder with a prior document, run intake on a defect with
overlapping symptoms, and confirm the prior document is surfaced with its root cause, its preventive
actions, and an assessment of whether those actions appear to have landed.

**Acceptance Scenarios**:

1. **Given** a prior RCA whose symptoms, root cause, or implicated code overlap today's defect,
   **When** intake completes, **Then** it is surfaced with its identifier, its validated root cause,
   and its prescribed preventive actions.
2. **Given** a surfaced prior RCA, **When** the command assesses its preventive actions, **Then** each
   is reported as apparently completed, apparently not completed, or undeterminable — with the
   evidence cited for the first two and the reason given for the third.
3. **Given** an empty or absent RCA folder, **When** intake completes, **Then** the command proceeds
   without error and without prompting.
4. **Given** a prior RCA that proved related, **When** the new document is written, **Then** it names
   that prior RCA by identifier in its header.
5. **Given** no prior RCA matched, **When** the new document is written, **Then** the related-RCA
   field records that the search ran and found nothing, rather than being left blank or omitted.

---

### User Story 3 - Test hypotheses against the code instead of interrogating the human (Priority: P1)

The engineer supplies the runtime logs. The agent does not then ask them which function handles the
retry, whether the timeout is configurable, or when the offending line was last changed — it reads
that itself, reports what it found, and spends its questions on the things the repository genuinely
cannot answer. Hypotheses move between open, supported, weakened and invalidated as evidence lands,
and the analysis keeps peeling back past the first plausible code path.

**Why this priority**: An agent that asks the human for what it could read is slower than no agent,
and an agent that stops at the first plausible code path produces the shallow diagnosis the BRD exists
to eliminate.

**Independent Test**: Pose a hypothesis that the source can settle and confirm the command
investigates and reports rather than asking; then state a surface symptom and confirm the command
proposes a deeper probe and names the analysis layer it is on.

**Acceptance Scenarios**:

1. **Given** a hypothesis testable against source, **When** the loop runs, **Then** the command
   investigates it and reports the finding with its file and line, rather than asking the user.
2. **Given** a surface-level symptom, **When** the loop runs, **Then** the command proposes a deeper
   probe and states the current layer on the symptom → immediate cause → contributing factors →
   process gap → systemic cause ladder.
3. **Given** several rounds of answers, **When** the user continues, **Then** the command maintains a
   running view of validated, supported, weakened, invalidated and open hypotheses with the remaining
   data gaps.
4. **Given** a hypothesis the repository cannot settle, **When** the loop runs, **Then** it is named
   as unresolvable from the repository and the specific evidence needed is requested.
5. **Given** the loop is active, **When** the command asks a question, **Then** the questions are
   prioritized by what would most change the analysis, not listed exhaustively.

---

### User Story 4 - Leave a document the next person can act on (Priority: P1)

The analysis has converged. The engineer asks for synthesis and gets a document that leads with the
validated root cause, states the symptom next to it so nobody confuses the two, shows the hypotheses
that were killed as well as the one that survived, quantifies the impact, and separates the fix for
this instance from the change that stops it happening again — each with an owner and a way to tell it
worked.

**Why this priority**: The document is the durable output. Everything before it is a conversation that
ends when the terminal closes.

**Independent Test**: Run synthesis against a set of validated and invalidated hypotheses and confirm
the written file carries all nine required elements, leads with the root cause, and lands at the next
unused sequence number.

**Acceptance Scenarios**:

1. **Given** validated hypotheses and supporting evidence, **When** synthesis runs, **Then** the
   document carries all nine elements: problem statement, timeline, validated root cause stated
   answer-first, supporting evidence, impact, corrective actions, preventive actions, ownership, and
   verification criteria.
2. **Given** synthesis output, **When** the document is read, **Then** the root cause and the
   presenting symptom appear adjacently and are explicitly distinguished.
3. **Given** hypotheses that were invalidated during analysis, **When** the document is written,
   **Then** they appear in the evidence table with their status and what settled them.
4. **Given** each item of evidence, **When** the document is written, **Then** its source is
   attributed as code, commit, configuration, test, or user-supplied.
5. **Given** corrective and preventive action sections, **When** the document is written, **Then**
   they are distinct — a preventive action that merely restates the corrective one is flagged as a
   sign the analysis did not reach a root cause.
6. **Given** impact that cannot be quantified, **When** the document is written, **Then** the section
   says so rather than being omitted.
7. **Given** the folder already contains documents, **When** the file is written, **Then** its number
   is one greater than the highest present and no existing file is touched.

---

### User Story 5 - Explore a defect class before a defect exists (Priority: P1)

An engineer wants to work through a whole class of failure — intermittent failures, performance
degradation, data integrity — rather than a single ticket. The command lays out the issue tree or
fishbone for that class, supplies discovery questions at each node, helps rank branches by likelihood
and impact, and records which nodes were confirmed, refuted, or left open. Nothing is written to disk.

**Why this priority**: The BRD prices this as P1 and it is the mode that builds the practitioner's
mental model; it is also the only mode that is useful with no defect in hand.

**Independent Test**: Request exploration of a named defect class and confirm a MECE tree of at least
four major branches with sub-nodes and per-node discovery questions comes back, and that no file is
created.

**Acceptance Scenarios**:

1. **Given** a named or described defect class, **When** exploration starts, **Then** a MECE tree of
   at least four major branches with sub-nodes and per-node discovery questions is presented.
2. **Given** the tree, **When** the user navigates a branch, **Then** tailored discovery questions for
   that node are supplied and the branch's likelihood and impact are discussed.
3. **Given** an exploration session, **When** it ends, **Then** no file has been created or modified
   anywhere in the project.
4. **Given** an exploration that turns into a real defect, **When** the user says so, **Then** the
   command carries the confirmed and refuted nodes into intake rather than starting over.

---

### User Story 6 - Write where the project says, in the shape the project says (Priority: P1)

A team that has declared `Artifact root: documents/` in its constitution, and dropped its own RCA
template into `.specify/templates/overrides/`, gets its document in its folder with its sections in
its order — and is told which template layer was used, so an override that failed to apply is visible
immediately rather than discovered in review.

**Why this priority**: Constitutional. Principles VII and VIII are binding on every document-producing
agent, and an agent that honours them only by default is an agent whose team conventions silently do
not apply.

**Independent Test**: Declare a non-default artifact root and supply a template override, run
synthesis, and confirm the file lands under the declared root with the override's sections and that
the run names the resolved template path.

**Acceptance Scenarios**:

1. **Given** an `Artifact root:` declaration in the constitution, **When** the document is written,
   **Then** it lands under that root, matched case-insensitively.
2. **Given** no declaration and a documentation-publication signal in `docs/`, **When** the root is
   resolved, **Then** the command surfaces the signal, recommends the non-publishing root, and takes
   the non-publishing option where the choice cannot be obtained.
3. **Given** a template override, **When** the document is written, **Then** its sections and order
   are the override's, unchanged, and the run names the resolved path.
4. **Given** an override that omits a section the command would otherwise fill, **When** the document
   is written, **Then** the omission is reported and the section is not reinstated.
5. **Given** a superseded folder from an earlier convention, **When** numbering is resolved, **Then**
   it is read for continuity and reported, and nothing in it is moved, renamed, or deleted.

---

### User Story 7 - Coach the practitioner, not just the defect (Priority: P2)

After the document is written, the engineer asks how they did. They get specific feedback on how deep
the analysis went, whether hypotheses were genuinely tested or merely asserted, whether data gaps were
closed or quietly dropped, and whether the conclusions lead with the answer — with at least one
concrete thing to do differently next time.

**Why this priority**: Real value, but it depends on a completed analysis and delivers nothing on its
own. The BRD prices it P2.

**Independent Test**: Complete an analysis, request reflection, and confirm feedback is returned
against all four dimensions with at least one concrete improvement.

**Acceptance Scenarios**:

1. **Given** a completed analysis, **When** reflection is requested, **Then** feedback covers analysis
   depth, hypothesis discipline, data-gap closure, and answer-first structure.
2. **Given** reflection output, **When** it is read, **Then** it contains at least one concrete,
   specific improvement rather than generic encouragement.
3. **Given** reflection is requested before any analysis has run, **When** the command responds,
   **Then** it says there is nothing to reflect on rather than inventing an assessment.

### Edge Cases

- **No defect supplied.** The command asks what defect to analyze. It MUST NOT infer one from the
  branch name, recent commits, an open issue, or a failing test.
- **A ticket reference that does not resolve** — wrong project key, deleted issue, private repository,
  `gh` absent or unauthenticated, no JIRA access. Stated plainly with the specific remedy, then
  degraded to plain-language mode. Never a credential prompt.
- **The repository does not match where the defect happened** — wrong branch, undeployed change. The
  analyzed commit is recorded in the document and the user is asked to confirm the deployed version
  early, before hypotheses are built on code that was never running.
- **A codebase too large to scan exhaustively.** Scanned from the symptom outward, with an explicit
  statement of which areas were examined and which were not, so the gap is visible rather than
  implied.
- **Every hypothesis is invalidated.** The document is written recording that no root cause was
  validated, what was ruled out, and what evidence would be needed — not a speculative cause promoted
  to fill the section.
- **The defect's root cause lies outside this repository** — another service, another repo, a vendor.
  Named as out of reach, with what was established locally, rather than forced into a local
  explanation.
- **A declared artifact root that is unusable** — absolute, or escaping the project. Reported, and the
  default used instead, rather than guessed at.
- **The RCA folder contains a file whose name does not match the convention.** Read for context,
  ignored for numbering, reported once, and left alone.
- **A sequence-number collision from parallel branches.** Never resolved by overwriting; the file is
  written at the next free number and the collision resolves at merge like any other file conflict.
- **User-supplied logs containing secrets or personal data.** Never reproduced verbatim in a document
  that will be committed; described by kind and location instead.
- **Reflection or synthesis requested with no analysis behind it.** Refused with an explanation, not
  fabricated.

## Requirements *(mandatory)*

### Functional Requirements

#### Packaging and registration

- **FR-001**: The capability MUST ship as a single command file under `spectra/commands/`, registered
  in the single `spectra/extension.yml`. No new top-level extension folder MUST be created.
- **FR-002**: The command MUST be named `speckit.spectra.defect-rca` and MUST begin with YAML front
  matter carrying a `description`.
- **FR-003**: The command MUST be agent-agnostic, taking its input through `$ARGUMENTS`, and MUST NOT
  hard-code any single agent's invocation syntax or depend on a Bash helper from Spec Kit's script
  tree.
- **FR-004**: The command's effect is read-write: it writes the RCA document and the folder index, and
  nothing else.
- **FR-005**: No existing command file MUST be modified and no hook MUST be registered in
  `spectra/extension.yml` as part of this feature.
- **FR-006**: The agent MUST be registered in `agents-list.json` in the `testing-quality` phase, and
  its hand-written prose block MUST be added, anchored by its stable id.

#### Invocation and input

- **FR-007**: The command MUST accept a defect through three channels: a JIRA ticket reference or URL,
  a plain-language description, and a GitHub issue URL (BR-15).
- **FR-008**: The command MUST detect which channel was supplied from the argument's form and MUST
  state which channel it resolved to before gathering evidence.
- **FR-009**: With empty input the command MUST ask what defect to analyze and stop. It MUST NOT infer
  the defect from the branch name, recent commits, open issues, failing tests, or any other heuristic,
  and MUST NOT read source code or write anything before a defect is supplied.
- **FR-010**: The command MUST accept supplementary user-supplied material — logs, configuration,
  timelines, reproduction steps, stakeholder statements — in any channel and at any point in the
  session (BR-17).
- **FR-011**: Given a GitHub issue URL the command MUST retrieve the issue body and its comments using
  the `gh` CLI (BR-16). It MUST verify `gh` is present and authenticated before relying on it, and
  MUST give the distinct remedy for each failure — install versus `gh auth login`.
- **FR-012**: Given a JIRA reference the command MUST retrieve the ticket through whatever JIRA access
  the host agent already provides, and MUST use nothing else.
- **FR-013**: Where a ticket or issue cannot be retrieved the command MUST say so with the reason, ask
  the user to paste the content, and proceed treating the reference as a plain-language description
  (BR-18). It MUST NOT prompt for, accept, transmit, or store any credential, API token, or password,
  and MUST NOT attempt to authenticate on the user's behalf.
- **FR-014**: The command MUST make no network request other than the ticket and issue retrieval named
  above, and MUST NOT accept a repository URL to clone.

#### Reading the project

- **FR-015**: The command MUST discover and read the project constitution where one exists and MUST
  state, by heading, which of its principles bear on this analysis (BR-19).
- **FR-016**: The command MUST scan and analyze the source code, configuration, tests, and commit
  history relevant to the reported symptoms, and MUST report what it examined (BR-20).
- **FR-017**: The scan MUST be scoped outward from the defect's symptoms rather than run
  exhaustively, and the command MUST state which areas of the codebase it examined and which it did
  not, so the coverage gap is visible.
- **FR-018**: The command MUST record the repository and the exact commit it analyzed, and MUST ask
  the user to confirm the deployed version before hypotheses are built on code that may never have
  been running.
- **FR-019**: Every claim the command makes about the code MUST cite the file, and where the claim is
  about a specific behaviour, the line. A claim that something is absent MUST state what was searched
  for and where.

#### Recurrence

- **FR-020**: During intake the command MUST search the RCA folder for prior documents whose symptoms,
  validated root cause, or implicated code overlap the reported defect, and MUST surface every match
  with its identifier, root cause, and prescribed preventive actions (BR-28).
- **FR-021**: The search MUST be driven by symptoms and implicated code, not by title alone, and MUST
  use the folder index where one is present and the documents themselves where it is not.
- **FR-022**: For each surfaced prior RCA the command MUST report whether its preventive actions
  appear completed, not completed, or undeterminable — citing the evidence for the first two and the
  reason for the third (BR-29). It MUST NOT assert completion without a citation.
- **FR-023**: An empty or absent RCA folder MUST be handled without error and without prompting.
- **FR-024**: Any prior RCA identified as related MUST be recorded in the new document's header by
  identifier; where none matched, the header MUST record that the search ran and found nothing
  (BR-30). The field MUST NOT be left blank or omitted.

#### The analysis loop

- **FR-025**: The command MUST generate a MECE hypothesis tree covering Code/Logic,
  Design/Architecture, Process/Practice, Environment/Configuration, Data, People/Knowledge, and
  Organizational/Systemic dimensions, or the domain-specific equivalents the project warrants, with at
  least five major branches (BR-01).
- **FR-026**: The command MUST guide analysis through layered questioning — symptom, immediate
  technical cause, contributing factors, process and practice gaps, systemic and organizational root
  cause — and MUST state which layer the current probe is on (BR-02).
- **FR-027**: The command MUST form explicit hypotheses, propose how each would be tested, track each
  as open, supported, weakened, invalidated or validated, and refine the remaining branches as
  evidence lands (BR-03). All outputs MUST be framed as advisory with the human retaining ownership of
  conclusions, communication, and actions (BR-09).
- **FR-028**: The command MUST test a hypothesis against the repository itself wherever the evidence
  is obtainable there, and MUST NOT ask the user for anything it can read (BR-21).
- **FR-029**: The command MUST identify what it cannot obtain from the repository and MUST ask precise
  questions prioritized by what would most change the analysis, not an exhaustive list (BR-04).
- **FR-030**: The loop MUST continue until root causes are validated or further evidence is
  unobtainable, and the command MUST NOT conclude at the first plausible code path.
- **FR-031**: In a session that cannot take answers, the command MUST proceed on repository evidence
  alone and write the document, recording every unanswered question as an open data gap with its
  effect on confidence stated.
- **FR-032**: The command MUST NOT answer its own questions, and MUST NOT present a hypothesis as
  validated on evidence that cannot settle it.
- **FR-033**: The command MUST NOT infer a runtime fact — a log line, a metric, an environment state,
  a timestamp — that it did not observe or receive.
- **FR-034**: The command MUST coach quantification of impact — severity, frequency, cost, risk,
  customer and business effect — wherever data exists or can be elicited (BR-08), and SHOULD coach
  peel-back questioning, hypothesis-validation phrasing, triangulation, and magic-wand framing where
  they help (BR-11).
- **FR-035**: The command MUST offer issue tree and fishbone structures for common defect classes with
  discovery questions at each node, navigable branch by branch, with at least four major branches
  (BR-05). Exploration alone MUST write nothing. It SHOULD map the McKinsey 7-Step process explicitly
  when structured problem-solving support is requested (BR-13).
- **FR-036**: The hypothesis tree, question list, issue trees, and session notes MUST be rendered in
  full in the session and MUST NOT be written to disk (BR-14).
- **FR-037**: After an analysis the command SHOULD offer reflection covering analysis depth,
  hypothesis discipline, data-gap closure, and answer-first structure, with at least one concrete
  improvement (BR-12). Requested with no analysis behind it, it MUST say so rather than assess.

#### The document

- **FR-038**: The document MUST contain all nine required elements: problem statement, timeline and
  context, validated root cause, supporting evidence, impact assessment, corrective actions,
  preventive actions, suggested ownership, and verification criteria (BR-06).
- **FR-038a**: The document MUST open with an identity block recording the defect id, the source
  reference — JIRA key, GitHub issue URL, or "direct prompt" (BR-26) — the repository and commit
  analyzed, the severity, the related prior RCA, the owner and date, and the advisory status line.
  Where a field cannot be established it MUST record that fact rather than be omitted or invented.
- **FR-039**: Conclusions MUST be structured answer-first — the validated root cause before the
  supporting argument and evidence (BR-07) — and the presenting symptom MUST appear adjacent to it,
  explicitly distinguished (BR-27).
- **FR-039a**: The evidence section MUST record invalidated and weakened hypotheses alongside
  validated ones, and MUST attribute every item of evidence to its source: code, commit,
  configuration, test, or user-supplied.
- **FR-039b**: Corrective and preventive actions MUST be carried in separate sections, each row
  naming an owner and a verification criterion. Where a preventive action only restates a corrective
  one, the command MUST say so, as a sign the analysis has not reached a root cause.
- **FR-039c**: Where impact cannot be quantified the section MUST say so rather than be omitted.
- **FR-039d**: The advisory status line MUST be present and MUST NOT be softened, reworded, or
  dropped. The owner MUST be taken from the repository's configured Git author and offered for
  correction; where no name is readable the field MUST record that the owner is unassigned.
- **FR-039e**: The command MUST NOT reproduce a secret, credential, token, or item of personal data in
  the document. Where user-supplied material contains one, it MUST be described by kind and location
  instead, and the substitution MUST be stated in the session.
- **FR-039f**: Where no root cause could be validated, the document MUST record that, name what was
  ruled out, and state what evidence would settle it. A speculative cause MUST NOT be promoted to fill
  the section.
- **FR-039g**: Guidance comments and unfilled placeholder tokens MUST be stripped from the written
  document, whichever template layer they came from.

#### Where it is written

- **FR-040**: The document MUST be written into `<artifact-root>/defect-rca/` in the project,
  honouring an `Artifact root:` line declared in the constitution and matched case-insensitively. The
  path MUST be lowercase and project-relative, and the folder MUST be created on demand.
- **FR-041**: Where no root is declared, the command MUST check for the documentation-publication
  signal before defaulting to `docs/` — `mkdocs.yml`, `docusaurus.config.*`, `docs/_config.yml`,
  `docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, or a Pages configuration pointing at `docs`.
  Finding one, it MUST surface it, recommend the non-publishing root, and take the non-publishing
  option where the choice cannot be obtained.
- **FR-042**: A declared root that is unusable — absolute, or escaping the project — MUST be reported
  and the default used, never guessed at.
- **FR-043**: The filename MUST be `NNN-<slug>.md`, where `NNN` is a zero-padded three-digit sequence
  scoped to that folder and `<slug>` is a lowercase hyphenated name of roughly three to five words
  describing the *observed problem*, not the suspected cause (BR-24). The sequence MUST be one greater
  than the highest number already present — not a count of files — MUST start at `001` in an empty
  folder, and MUST be independent of the `specs/` sequence (BR-25).
- **FR-043a**: The command MUST NOT overwrite, replace, or amend an existing document. A file whose
  name does not match the convention MUST be read for context, ignored for numbering, reported once,
  and left alone.
- **FR-043b**: The document and its index row MUST be written together as the run's final act, and the
  sequence number resolved at that moment. A run that stops before that point MUST leave the folder
  exactly as it found it — no partial document, no number consumed.
- **FR-043c**: A folder from a superseded convention MUST be read for context and for numbering
  continuity, reported once with the canonical folder named, and offered as a move the user can run.
  The command MUST NOT move, rename, modify, or delete anything there.

#### The index

- **FR-044**: The command MUST maintain an index at `<artifact-root>/defect-rca/README.md` listing
  every RCA document in the folder.
- **FR-045**: Each row MUST carry the identifier, the observed symptom, the validated root cause, the
  related prior RCA where one exists, and the preventive-action status.
- **FR-046**: The index MUST be rebuilt from the documents actually present, so a hand-added or
  hand-deleted file self-corrects on the next run.
- **FR-047**: The index MUST be treated as a cache of the corpus and never as the corpus itself: a
  recurrence search that finds nothing in the index MUST fall back to the documents.

#### The template

- **FR-048**: The document's structure MUST come from a template shipped as
  `spectra/templates/defect-rca-template.md` and registered in `spectra/extension.yml` under
  `provides.templates`. It MUST NOT be embedded as a literal in the command file.
- **FR-049**: The shipped default MUST be BRD Appendix A's structure: identity block, root cause,
  problem statement and timeline, supporting evidence, impact, corrective actions, preventive actions.
- **FR-050**: The template MUST be resolved through Spec Kit's stack, highest priority first:
  `.specify/templates/overrides/defect-rca-template.md`, then
  `.specify/presets/<preset-id>/templates/defect-rca-template.md`, then
  `.specify/extensions/spectra/templates/defect-rca-template.md`, then
  `.specify/templates/defect-rca-template.md`, then the command's own inline skeleton as last resort.
  The first readable, non-empty layer MUST be taken, and no single path MUST be hard-coded.
- **FR-051**: The resolved template's sections and order MUST be honoured. The command MUST NOT add,
  rename, or reorder them, and where a section the command would ordinarily fill is absent, MUST
  report the omission rather than reinstate it.
- **FR-052**: The command MUST report which template layer it resolved, naming the path.
- **FR-053**: The rules the command owns MUST hold whichever layer is resolved: the
  symptom-versus-root-cause distinction, answer-first ordering, the recording of invalidated
  hypotheses, evidence-source attribution, the advisory status line, the related-prior-RCA field, and
  the prohibition on reproducing a secret.
- **FR-054**: The command MUST NOT create or edit any template file, and MUST name the override path
  as the supported customization point — never the installed copy under `.specify/extensions/`.

#### Write scope

- **FR-055**: The command MUST treat the repository as read-only except for
  `<artifact-root>/defect-rca/`, where it writes exactly the RCA document and the index (BR-22).
- **FR-056**: The command MUST NOT generate, apply, or execute a code fix, patch, or configuration
  change, and MUST NOT write, modify, or generate test code (BRD Section 5.2).
- **FR-057**: The command MUST NOT write back to JIRA or GitHub, create an issue, comment, or
  transition a ticket.
- **FR-058**: The command MUST NOT edit the constitution, create a branch, stage, or commit. Where a
  constitution line would help — an `Artifact root:` declaration — it MUST offer the exact line for the
  user to add.
- **FR-059**: The command MUST require no external knowledge base, document repository, or retrieval
  integration, operating on methodology within model knowledge plus artifacts in the project (BR-10).
  Methodology MUST be applied faithfully without reproducing substantial portions of the copyrighted
  texts that describe it.

#### Reporting

- **FR-060**: On completion the command MUST report the path written, the template layer resolved, the
  artifact root used and how it was determined, the commit analyzed, which prior RCAs were surfaced,
  and what it could not examine.

#### Catalog and package sync

- **FR-061**: `extension.version` in `spectra/extension.yml` MUST be bumped as a MINOR release, with a
  matching `spectra/CHANGELOG.md` entry.
- **FR-062**: The `spectra` entry in `catalog.json` MUST be updated so its version, command count, and
  description match the manifest and the rebuilt package.
- **FR-063**: `docs/packages/spectra.zip` MUST be rebuilt with `tools/build_package.py` so the
  published package carries the new command and template.
- **FR-064**: `docs/index.html` MUST list the new command without hard-coding any value another
  artifact defines.
- **FR-065**: Every generated agent listing MUST be regenerated with `tools/generate_agent_docs.py`,
  and `tools/generate_agent_docs.py --check` MUST pass.
- **FR-066**: The repository's standard-library `unittest` suite MUST cover the agent's invariants, and
  `python -m unittest discover -s tests` MUST pass.

### Key Entities

- **Defect**: What is being analyzed. Arrives through one of three channels, carries a symptom, an
  environment, and optionally a severity and a timeline. Identified in the corpus by its RCA id.
- **Hypothesis**: A candidate cause with a proposed test, a status (open, supported, weakened,
  invalidated, validated), the evidence that moved it, and that evidence's source.
- **Hypothesis tree**: The MECE decomposition of where the cause could live. Session-only; never
  written.
- **Data gap**: Something the repository cannot establish. Carries the question asked, whether it was
  closed, and what its being open costs the conclusion's confidence.
- **RCA document**: The durable deliverable. `NNN-<slug>.md` under `<artifact-root>/defect-rca/`,
  shaped by the resolved template, carrying the nine required elements and the identity header.
- **Prior RCA**: An existing document in the corpus matched at intake by symptom, root cause, or
  implicated code, contributing its preventive actions and their apparent status.
- **RCA index**: `README.md` in the same folder; one row per document, rebuilt from what is present,
  a cache of the corpus rather than the corpus.
- **Artifact root**: The project's declared or defaulted root for durable deliverables, resolved per
  run, under which `defect-rca/` sits.
- **Resolved template**: The first readable, non-empty layer of the template stack, whose sections and
  order the document takes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Guided investigations reach an average of at least 4 analysis layers, targeting 4–5
  (BRD SC-01).
- **SC-002**: At least 80% of completed sessions produce a validated root cause at the process,
  design, or systemic level rather than a restated technical symptom (BRD SC-02).
- **SC-003**: At least 90% of sessions record explicit hypothesis formation and testing, including at
  least one invalidated hypothesis (BRD SC-03).
- **SC-004**: At least 75% of sessions beginning with material data gaps close them or mark them
  explicitly unobtainable before synthesis (BRD SC-04).
- **SC-005**: Every generated document contains all nine required elements and leads with the root
  cause — 100%, because the resolved template makes both structural (tightens BRD SC-05 and SC-06).
- **SC-006**: At least 60% of hypotheses testable against source are settled by the command's own
  repository analysis rather than by asking the user (BRD SC-07).
- **SC-007**: Where a prior RCA exists for a substantially similar defect, it is surfaced at intake in
  at least 80% of cases (BRD SC-10).
- **SC-008**: At least 70% of preventive actions originating from these analyses are judged actionable
  and relevant on periodic qualitative review by practice leadership (BRD SC-09).
- **SC-009**: Within six months of regular use, pilot users show measurable improvement on
  analysis-depth and data-gap metrics against their own baseline (BRD SC-08).
- **SC-010**: Across every run, no file outside `<artifact-root>/defect-rca/` is created, modified, or
  deleted, and no existing document in that folder is overwritten — zero exceptions.
- **SC-011**: Every run reports the path written, the template layer resolved, the artifact root and
  how it was determined, and the commit analyzed — 100%.
- **SC-012**: A project that declares an artifact root and supplies a template override gets its
  document in its folder with its sections in its order — 100% of such runs.
- **SC-013**: No generated document contains a secret, credential, token, or item of personal data
  carried over from user-supplied material — zero occurrences.
- **SC-014**: A QE engineer with no prior exposure to the command can go from a defect reference to a
  written RCA document in a single session without consulting external documentation.

## Assumptions

- Users are Quality Engineering professionals with foundational testing and defect-class knowledge;
  the agent coaches structured analysis methodology rather than teaching technical fundamentals.
- The agent runs inside a host coding agent with read access to the repository containing the code
  under investigation, and inherits that agent's permission model, approvals, and audit trail. It
  grants itself nothing and asks for no exemption.
- `gh` is installed and authenticated where the GitHub issue channel is used; JIRA access, where used,
  already exists in the host agent's environment. Neither is required for the command to function.
- The human supplies the runtime evidence the repository cannot — logs, metrics, environment state —
  and answers the command's questions, or accepts the recorded gaps where they cannot.
- Where a project constitution exists it is the authoritative statement of that project's principles;
  where none exists the agent proceeds on methodology alone.
- Sessions run in English or another language the underlying model supports.
- Final root-cause conclusions, stakeholder communication, and action ownership remain the
  responsibility of the human QE professional; the agent is a coach and structuring aid.
- The RCA corpus is small enough that a full scan of the folder remains practical. The index exists to
  push that ceiling higher; when a corpus outgrows a full scan, the search mechanism is revisited
  rather than silently degraded.
- Sensitive production and client information is handled under applicable data-protection and
  confidentiality policy; repo-native output keeps the artifact inside the access controls the
  repository already has.
- Monorepo and multi-repository defects — where the cause lies outside the repository the agent can
  read — are out of scope for this release and are reported as out of reach rather than forced into a
  local explanation.
