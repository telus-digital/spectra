# Feature Specification: Deployment Strategist Agent

**Feature Branch**: `031-deployment-strategy`

**Created**: 2026-10-15

**Status**: Implemented

**Input**: User description: "Add a new Spectra agent, speckit.spectra.deployment-strategy (roster id
`deployment-strategy`, title "Deployment Strategist"), in the deployment-operations phase (AI-DLC:
Operation), type add-on, provider spectra. It is a read-write, document-producing command modelled on
speckit.spectra.test-strategy and speckit.spectra.domain-analyzer: it reads the project (source, CI
workflows, Dockerfiles, k8s/Helm manifests, IaC, specs, ADRs, the constitution, an existing
TEST_STRATEGY.md and DOMAIN_ANALYSIS.md) plus any document the user uploads or references in the prompt,
then writes one deployment-strategy recommendation for the project. […] Step zero, deployable
classification […] Six mandatory lenses […] Rules, mirroring test-strategy […] Clarification round […]
Output: a standing-policy singleton at <artifact-root>/DEPLOYMENT_STRATEGY.md […] Constitution handoff
[…] Repository obligations in the same change […] Do not touch the CLI channel or VERSION." (full text
in the session that produced this spec; every decision in it is carried into the requirements below)

## Clarifications

### Session 2026-10-15

The decisions below were settled with the maintainer before this spec was written. They are recorded so
a later reader can tell a choice from an omission.

- Q: Which lenses should a deployment strategy carry? → A: **Six mandatory lenses**, merged down from an
  initial eight: environments & promotion; pipeline, artifact & traceability; release & versioning; data
  & schema change; rollback & recovery; operability & configuration. Pipeline and artifact were merged
  because "which gates a build passes" and "what the build produces and how it is traced" are one
  conversation in practice; operability and configuration/IaC were merged because both answer "how do we
  know the running thing is the thing we meant, and that it is healthy". Conditional lenses — rollout
  technique, multi-region or multi-tenant, compliance and audit gates, environment cost — appear only
  where the evidence warrants them.

- Q: How deep should operability go — a monitoring policy, or concrete alert definitions? → A: **High
  level.** The document says what should be monitored and who owns it, and lists and links scheduled
  jobs and alerts that already exist. Alert definitions, thresholds, and runbook procedure are out of
  scope for the document; a user who wants to go deeper does so by continuing the conversation with the
  agent in the same session. The reference document this agent was modelled on carries months of
  accumulated runbook detail; a first run of a strategy agent producing that would be both wrong and
  unreviewable.

- Q: How is the clarification round run? → A: **Five fixed questions, one per turn, each carrying a
  recommendation and the evidence behind it** — the same interaction as `speckit.clarify` and
  `speckit.spectra.test-strategy`. The five are: target platform/hosting (when the repository does not
  show it), who approves a production deploy and how, whether a stakeholder-review or pre-release
  environment exists or is wanted, availability and RPO/RTO targets, and release cadence.

- Q: Where does the document go? → A: **`<artifact-root>/DEPLOYMENT_STRATEGY.md`**, a standing-policy
  singleton consistent with `TEST_STRATEGY.md` and `DOMAIN_ANALYSIS.md`. Principle VII says a new
  singleton must be named in the constitution by amendment and that a command must not declare itself
  one, so this change carries that amendment (constitution 1.9.0 → 1.10.0).

- Q: Does the agent end by offering to feed the strategy back into the constitution? → A: **Yes, in the
  same way as `test-strategy` and `domain-analyzer`**: it drafts the amendment, gates it, never writes the
  constitution, and ends with a link to the written file and a ready-to-paste `/speckit-constitution`
  line that references it.

- Q: What are the command name and roster title? → A: Command `speckit.spectra.deployment-strategy`,
  roster id `deployment-strategy` — matching `test-strategy` — and display title **Deployment
  Strategist**.

- Q: When a project ships more than one deployable, are the five questions asked once for the project
  or once per deployable? → A: **Once per project.** Each question names where deployables differ, and
  the user may answer per deployable in free text; the announced count stays five.

- Q: Does the drafted constitution amendment carry the whole strategy, or only its durable invariants?
  → A: **Only durable invariants** — rules such as same-artifact promotion, explicit production approval,
  no floating tags, backward-compatible migrations, and app rollback ≠ database rollback. Environment
  names, platform specifics, and cadence stay in `DEPLOYMENT_STRATEGY.md`, which the amendment
  references.

- Q: What does the agent do about gating checks when no `TEST_STRATEGY.md` exists? → A: **Continue.**
  It reports the checks CI actually runs, as verified with citations, makes no recommendation about
  which tests should exist, records the missing test strategy as a gap, and names
  `speckit.spectra.test-strategy` as the next step.

- Q: Does the document include a promotion-flow diagram, and in what format? → A: **One Mermaid
  diagram** in the environments & promotion lens, built only from environments and gates the document
  itself states.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get a deployment strategy grounded in what the project already does (Priority: P1)

A team lead on an established project runs the Deployment Strategist with no arguments. The agent reads
the repository — CI workflows, container and orchestration manifests, infrastructure-as-code, specs,
ADRs, the constitution, and any existing test strategy and domain analysis — classifies what the project
ships, reports what the deployment practice is today across six lenses, and recommends what it should
become. Every claim names where it came from. The team lead reads one document that both describes the
current practice accurately and proposes a credible next state.

**Why this priority**: This is the agent's reason to exist. Without an evidence-grounded document there
is nothing to hand to the constitution and nothing a team can act on.

**Independent Test**: Run the agent on a project with a CI workflow, a container build, and deployment
manifests. Confirm that the document lists each lens, reports current state with project-relative
citations before each recommendation, and that no lens is silently missing.

**Acceptance Scenarios**:

1. **Given** a project whose CI deploys a container image on merge to its default branch, **When** the
   agent runs, **Then** the pipeline lens reports that behaviour with a citation to the workflow file
   before making any recommendation.
2. **Given** a project with no database, **When** the agent runs, **Then** the data & schema change lens
   appears and states "not applicable" with a one-line reason and the search that established the
   absence.
3. **Given** a project with an existing `TEST_STRATEGY.md`, **When** the agent addresses which checks gate
   a merge, **Then** it cites that document for which tests exist and decides only where in the pipeline
   they gate.
4. **Given** a project, **When** the document is written, **Then** it states what portion of the
   repository the agent read and what it could not see.

---

### User Story 2 - Answer the five questions the repository cannot settle (Priority: P1)

After reading and classifying, the agent announces a round of five questions and asks them one at a
time. Each question is numbered, offers two to four labelled options with one marked as recommended, and
says why — citing a project path, or stating plainly that the recommendation is a convention with
nothing in this project behind it. The user answers, skips, types a free-text answer, or says "use your
defaults" to accept every remaining recommendation.

**Why this priority**: Approval authority, availability targets, and release cadence cannot be read from
any source tree. A strategy that guesses them is a plausible document nobody can trust.

**Independent Test**: Run the agent interactively and confirm exactly one question arrives per turn,
numbered "N of 5", with a marked recommendation and its evidence; then run again answering "use your
defaults" at question 2 and confirm questions 2–5 take their recommendations without being asked.

**Acceptance Scenarios**:

1. **Given** a project whose manifests name the hosting platform, **When** question 1 is reached, **Then**
   it is asked as a confirmation of the detected platform, keeps its number, and cites the evidence.
2. **Given** the user replies with a question instead of an answer, **When** the agent responds, **Then**
   it answers and asks the same question again without advancing.
3. **Given** `--non-interactive`, **When** the agent runs, **Then** it asks nothing, takes every
   recommendation, and records all five as `not_asked`.
4. **Given** any run, **When** the document is written, **Then** all five questions are recorded with the
   recommendation, the answer taken, and a disposition of `answered`, `default_taken`, or `not_asked`.

---

### User Story 3 - Decide whether the strategy becomes policy (Priority: P1)

After the document is written and summarised, the agent checks whether the project's constitution
already carries a deployment or release policy. Where it does not, or only partly does, the agent drafts
the amendment in the constitution's voice, shows it, and offers three paths: approve, modify the strategy
first, or talk it through. On approval it records the draft in the document and ends with a link to the
written file and a ready-to-paste `/speckit-constitution` line. It never edits the constitution.

**Why this priority**: A strategy that is not policy is advice every later session can ignore. The
handoff is what makes it binding, and keeping the constitution edit with the constitution command is what
keeps it safe.

**Independent Test**: Run the agent on a project whose constitution has no deployment obligations;
approve the amendment; confirm the document carries the unchecked amendment items, the closing message
contains a link to the actual path written and the one-line `/speckit-constitution` command, and the
constitution file is byte-identical to before.

**Acceptance Scenarios**:

1. **Given** a constitution that already mandates deployment gates covering the strategy's core claims,
   **When** the check runs, **Then** the agent quotes the governing clause, drafts nothing, and offers no
   gate.
2. **Given** a constitution that contradicts a recommendation, **When** the check runs, **Then** the
   contradiction is surfaced as its own finding and no amendment silently overrides the existing
   principle.
3. **Given** no constitution, **When** the check runs, **Then** the agent says there is nothing to amend,
   names `/speckit-constitution` as the way to create one, and offers no gate.
4. **Given** a declared artifact root of `documents/`, **When** the handoff line is printed, **Then** it
   references `documents/DEPLOYMENT_STRATEGY.md`, not the default path.

---

### User Story 4 - Supply documents the repository does not contain (Priority: P2)

A consultant has a client's hosting standard as a PDF and an ops runbook as a Markdown file outside the
repository. They reference both in the prompt. The agent reads them as inputs, cites them as **claimed
in docs**, and uses them to settle questions it would otherwise have asked — without treating a claim in
a document as a fact about the repository.

**Why this priority**: Deployment policy often lives with a client or a platform team, not in the
repository. Without this the agent asks questions the user has already answered on paper.

**Independent Test**: Reference a local document stating the production approval rule; confirm question 2
is turned into a confirmation citing that document, and the recommendation is marked as claimed-in-docs
rather than verified.

**Acceptance Scenarios**:

1. **Given** a referenced local document, **When** the agent reads it, **Then** it is listed among the
   inputs consulted and every claim drawn from it carries the claimed-in-docs provenance.
2. **Given** a referenced URL, **When** the agent encounters it, **Then** it does not fetch it, says so,
   and asks the user to supply the content locally if it matters.
3. **Given** a referenced document that cannot be read, **When** the agent continues, **Then** it names
   the document and the reason in the inputs it could not read.

---

### User Story 5 - Re-run when the project changes (Priority: P2)

Months later the project has added a pre-release environment and a migration job. The team re-runs the
agent. It reads the prior document, pre-fills the five questions from the answers recorded last time
("last run you said this; still true?"), marks each recommendation `new`, `adopted`, or `carried`, states
what changed, and rewrites the same file in place.

**Why this priority**: A standing policy that cannot be refreshed decays into a historical artefact.

**Independent Test**: Run twice on the same project, changing one manifest between runs; confirm one file
exists, the second run's questions open with the prior answers, and the changed area is marked.

**Acceptance Scenarios**:

1. **Given** a prior `DEPLOYMENT_STRATEGY.md`, **When** the agent re-runs, **Then** no second strategy
   file is created.
2. **Given** a recommendation the project has since implemented, **When** the agent re-runs, **Then** it
   is reported as `adopted` rather than proposed again.

---

### User Story 6 - Run it on something that is not a web service (Priority: P3)

A maintainer of a published library and a CLI tool runs the agent. It classifies the deployables from
evidence — a package published to a registry, a CLI distributed as a tool — and each lens adapts:
"environments" becomes release channels, "deploy" becomes "publish", rollback becomes yank-or-supersede.
Nothing recommends a cluster, a container registry, or a database migration the project does not have.

**Why this priority**: Most of the reference shape assumes a running service. Without classification
the agent would recommend Kubernetes rollbacks to a library.

**Independent Test**: Run the agent on a library-only repository; confirm the classification is
`library/package`, no lens recommends infrastructure absent from the evidence, and inapplicable lenses
state why.

**Acceptance Scenarios**:

1. **Given** a monorepo with a web service and a published package, **When** the agent classifies,
   **Then** each deployable gets its own lens treatment and shared sections cover only what genuinely
   applies to both.
2. **Given** a mobile app, **When** the environments & promotion lens runs, **Then** store review is
   recorded as a promotion gate the team does not control.

---

### Edge Cases

- **No CI, no manifests, nothing deployable yet (greenfield).** The agent classifies from declared intent
  (specs, README, constitution); recommendations are marked `convention`; the document says plainly it is
  a strategy for code that does not exist yet.
- **Evidence contradicts an answer** (the user says "no database", the repository carries migrations).
  The answer shapes judgement where it is legitimately the user's call; the contradiction is recorded in
  the document; no measured fact is overwritten by an answer.
- **The default `docs/` root is published** (GitHub Pages, MkDocs, Docusaurus signals) with no declared
  root. The agent surfaces it, recommends `documents/`, and lets the user choose; where no choice can be
  obtained it takes the non-publishing option.
- **The target file cannot be written.** The agent reports the failure, outputs the strategy in the
  session, writes nowhere else, and does not proceed to the amendment gate.
- **A secret appears in a manifest or referenced document.** The agent never reproduces it; it cites the
  file and states that a secret is present.
- **The user asks mid-session to go deeper** on one lens (alert definitions, a runbook). The agent
  answers in the session; the standing document stays high level unless the user explicitly asks for the
  detail to be added.
- **The resolved template omits a section** the agent would fill. The agent notes the omission rather
  than reinstating the section.
- **A reply that is not an answer** during the clarification round. The agent answers it and repeats the
  same question; it does not advance or count it as a skip.
- **Session non-interactivity is not declared.** The agent asks; it never infers non-interactive mode
  from the environment.

## Requirements *(mandatory)*

### Functional Requirements

#### Identity and registration

- **FR-001**: The command MUST be named `speckit.spectra.deployment-strategy`, live at
  `spectra/commands/deployment-strategy.md`, begin with YAML front matter carrying a `description`, use
  `$ARGUMENTS` for input, and be registered in `spectra/extension.yml` `provides.commands`.
- **FR-002**: The agent MUST be registered in `agents-list.json` with id `deployment-strategy`, title
  "Deployment Strategist", phase `deployment-operations`, type `add-on`, provider `spectra`, status
  `available`, and command `speckit.spectra.deployment-strategy`.
- **FR-003**: The command MUST require no arguments. Optional input is a focus hint, references to
  local documents, and the single flag `--non-interactive`. An unrecognised flag MUST be reported and
  ignored, never folded into the hint. A hint weights the analysis but MUST NOT cause any mandatory lens
  to be dropped.

#### Reading context

- **FR-004**: Before proposing anything, the agent MUST read, where present: the constitution; specs;
  ADRs; README and contributing documentation; CI workflow definitions; container build files;
  orchestration manifests (Kubernetes, Helm, Compose, serverless configuration); infrastructure-as-code;
  database migration tooling; dependency manifests; release configuration; and any existing
  `TEST_STRATEGY.md` and `DOMAIN_ANALYSIS.md` at the resolved artifact root.
- **FR-005**: The agent MUST read local documents the user references or uploads, record each as an
  input, and attribute claims drawn from them as **claimed in docs**. It MUST NOT fetch a URL; it states
  that it did not and asks for local content where it matters.
- **FR-006**: The agent MUST record every input consulted and, by name and reason, every expected input
  it could not read.
- **FR-007**: The agent MUST NOT reproduce a secret found in any input; it cites the location and states
  that a secret is present.

#### Classifying what ships

- **FR-008**: Before applying any lens, the agent MUST classify each deployable from evidence as one of:
  running service, static site/SPA, library/package, CLI/desktop tool, mobile app, or infra-only. It
  MUST NOT ask the user for this classification.
- **FR-009**: Where a project declares workspaces or carries several independently built deployables,
  each MUST receive its own classification and lens treatment; a single-deployable project MUST say so
  once and not read like a monorepo.
- **FR-010**: The agent MUST also classify the project greenfield, brownfield, or mixed from deployment
  practice evidence (CI that deploys, manifests, release configuration) and report the deciding and
  dissenting signals.
- **FR-011**: Every lens MUST adapt its meaning to the classification — for a library "deploy" means
  "publish to a registry" and environments become release channels; for a mobile app, store review is
  recorded as a promotion gate the team does not control.

#### The lenses

- **FR-012**: The document MUST address six mandatory lenses: (1) environments & promotion; (2) pipeline,
  artifact & traceability; (3) release & versioning; (4) data & schema change; (5) rollback & recovery;
  (6) operability & configuration. Each MUST be marked **applicable** or **not applicable** with a
  one-line reason. No lens may be omitted.
- **FR-013**: In brownfield or mixed mode, each applicable lens MUST report current state, with
  citations, before any recommendation.
- **FR-014**: Environments & promotion MUST state, per environment, what it proves, its audience, how it
  is deployed, and the gate that moves a release into it. It MUST include exactly one Mermaid
  promotion-flow diagram, from source branch through each environment to production (or the release
  channels a non-service deployable has), drawing only environments and gates the lens itself states;
  a node or gate with no row in the lens is a defect. Where the lens is not applicable, no diagram is
  drawn.
- **FR-015**: Pipeline, artifact & traceability MUST cover pre-merge and on-merge checks, whether the
  same artifact is promoted unchanged between environments, whether tags are immutable (never a floating
  tag such as `latest` as a deployment identifier), and traceability from a running artifact to its
  commit. Provenance and SBOM MUST be recommended only where the evidence warrants. Which tests exist
  MUST be cited from `TEST_STRATEGY.md` when present; this lens decides only where they gate. When no
  `TEST_STRATEGY.md` exists, the agent MUST NOT stop and MUST NOT recommend which tests should exist: it
  reports the checks CI runs today as verified, records the missing test strategy as a gap, and names
  `speckit.spectra.test-strategy` as the next step.
- **FR-016**: Release & versioning MUST cover the branching model, how a release is cut, the versioning
  scheme, and the hotfix path.
- **FR-017**: Data & schema change MUST cover how migrations run and in what order relative to the
  application, backward compatibility, and MUST state explicitly that rolling back the application does
  not roll back the database.
- **FR-018**: Rollback & recovery MUST give the application rollback approach with short, concrete
  commands where the platform is known; state disaster-recovery targets (RPO/RTO) as answered or as open
  questions; and distinguish what has been drilled from what is assumed.
- **FR-019**: Operability & configuration MUST stay high level: health checks and smoke tests, what
  should be monitored and who owns detection and alerting, scheduled or background workloads, how
  configuration and secrets enter each environment, what is managed as code versus set up out of band,
  and how drift is caught. Existing scheduled jobs and alerts MUST be listed and linked, not redefined.
  Alert definitions, thresholds, and runbook procedure MUST NOT be generated into the document unless the
  user explicitly asks for them in the session.
- **FR-020**: Conditional lenses — rollout technique, multi-region or multi-tenant, compliance and audit
  gates, environment cost — MUST appear only where the evidence warrants them, each with that evidence.

#### Provenance and honesty rules

- **FR-021**: Every claim and recommendation MUST carry exactly one provenance: **verified** (a
  project-relative citation), **claimed in docs** (a citation to a document, in or outside the
  repository), **stated** (a clarification answer, naming its question), or **convention** (no project
  evidence).
- **FR-022**: Every claim of absence MUST name what was searched for and where.
- **FR-023**: An answer MUST NOT overwrite a fact read from the repository. Where they conflict, the
  agent applies the answer where it is legitimately the user's decision and records the disagreement in
  the document.
- **FR-024**: The document MUST contain an **Open questions / confirmation items** section listing what
  only the client or ops owner can answer — for example cloud project or account identifiers, cluster
  names, domains and TLS, who is paged, availability targets left unanswered. The agent MUST NOT invent
  values for these.
- **FR-025**: The document MUST state the agent's coverage of the analysis: what it read out of what is
  present, and what it could not see.

#### The clarification round

- **FR-026**: After reading and classifying and before writing, the agent MUST run a round of exactly
  five questions: (1) target platform/hosting; (2) who approves a production deploy, and how; (3) whether
  a stakeholder-review or pre-release environment exists or is wanted; (4) availability and RPO/RTO
  targets; (5) release cadence. The round is asked once per project, never once per deployable; where
  deployables need different answers, the question names the difference and accepts a per-deployable
  free-text answer, and the recorded answer keeps that per-deployable split.
- **FR-027**: The agent MUST announce the round once — its length and every way out ("use your
  defaults", skipping a question, answering several at once).
- **FR-028**: The agent MUST ask one question per turn and wait. Each question MUST be numbered "N of 5",
  offer two to four labelled options with exactly one marked recommended, give the evidence behind the
  recommendation (a project path or document, or "convention, nothing in this project"), and state that
  free text is valid.
- **FR-029**: Where the evidence already settles a question, the agent MUST turn it into a confirmation
  and keep its number; it MUST NOT skip or renumber.
- **FR-030**: "Use your defaults" MUST take every remaining recommendation and end the round; an
  unanswered question MUST take its recommendation and be recorded; a reply that is not an answer MUST be
  answered and the same question asked again.
- **FR-031**: The agent MUST NOT ask anything the repository answers — the deployable classification,
  the stack, whether CI or manifests exist.
- **FR-032**: Non-interactive mode MUST be entered only when declared (`--non-interactive`, or the user
  stating no answer can be given), never inferred. In it the agent asks nothing, takes every
  recommendation, records all five as `not_asked`, takes the non-publishing option on any root question,
  and records the amendment as not asked.
- **FR-033**: On a re-run, the agent MUST pre-fill each question from the prior document's recorded
  answer and offer it for confirmation; a question previously recorded `not_asked` is asked normally.

#### The document

- **FR-034**: The agent MUST write exactly one file, to `<artifact-root>/DEPLOYMENT_STRATEGY.md`, as the
  final write of the run. No subfolder, no sequence number.
- **FR-035**: The artifact root MUST be resolved as the other singleton agents resolve it: a declared
  `Artifact root:` line in the constitution (project-relative, no leading slash, no `..`; an unusable
  value is reported and the default used); else a publication check on `docs/` (`mkdocs.yml`,
  `docusaurus.config.*`, `docs/_config.yml`, `docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, or a
  Pages configuration) that, on a hit, surfaces it, recommends `documents/`, and lets the user choose,
  taking the non-publishing option when no choice can be obtained; else `docs/`. The agent MAY offer the
  declaration line and MUST NOT write it.
- **FR-036**: The document's structure MUST come from a template named `deployment-strategy-template`,
  shipped at `spectra/templates/deployment-strategy-template.md`, registered in `provides.templates`,
  and resolved through the stack: project override → preset → installed extension copy → core templates
  → the command's inline skeleton as last resort. The first readable, non-empty layer wins.
- **FR-037**: The agent MUST honour the resolved template — its sections, in its order — and MUST NOT
  add, rename, or reorder sections; where a section it would fill is missing it notes the omission. Guidance
  comments and placeholder tokens MUST be stripped. The template used MUST be reported by path.
- **FR-038**: The provenance rules, the never-guess rule for open questions, the high-level operability
  boundary, and the no-secret rule MUST live in the command, not the template, so an override cannot
  remove them.
- **FR-039**: The document MUST begin with YAML front matter that parses: every free-text value quoted,
  no key holding both a scalar and a collection, and enumerated values spelled exactly. It MUST carry at
  least the mode, the deployables, the generation timestamp, the resolved template, the run number,
  coverage of analysis, the amendment state, and the full clarification record (each question's ask,
  recommendation, answer, and disposition).
- **FR-040**: The clarification record MUST appear in the body as well as the front matter.
- **FR-041**: If the file cannot be written, the agent MUST report the failure, output the strategy in
  the session, write nowhere else, and MUST NOT proceed to the amendment gate.
- **FR-042**: On a re-run the agent MUST rewrite the same file in place, read the prior document as an
  input, mark each recommendation `new`, `adopted`, or `carried`, and state what changed.

#### Report, constitution check, and handoff

- **FR-043**: After writing, the agent MUST report in the session, in order: where the document was
  written; which template was used; coverage of the analysis; the classification with its deciding
  signals; and a per-lens summary short enough to read in a terminal. It MUST NOT paste the document.
- **FR-044**: The agent MUST then check the constitution semantically — section headings, normative
  keywords, and subject matter, never a bare keyword match — and report one of **embedded**, **partial**,
  **absent**, or **no constitution**, quoting any governing clause.
- **FR-045**: Where the state is partial or absent, the agent MUST draft the amendment in the
  constitution's voice (declarative, MUST/SHOULD, brief rationale) as unchecked checkbox items carrying a
  target section and an add-or-amends marker, show it, and offer three paths:
  approve, modify the strategy first, or talk it through. The draft MUST carry only durable invariants
  the strategy establishes — rules that stay true when an environment, platform, or cadence changes —
  and MUST reference `DEPLOYMENT_STRATEGY.md` for the specifics rather than restating them; environment
  names, platform identifiers, and cadences MUST NOT appear as constitutional obligations. Approval records the draft in the document's proposed-amendment
  section; declined or unanswered records nothing.
- **FR-046**: A contradiction between an existing constitution principle and a recommendation MUST be
  surfaced as its own finding; no draft may silently override an existing principle.
- **FR-047**: The agent MUST NOT write `.specify/memory/constitution.md` in any run, approved or not, and
  MUST NOT create a constitution.
- **FR-048**: The agent MUST end by giving a link to the path it actually wrote and one ready-to-paste
  line of the form `/speckit-constitution Adopt the checked items in the "Proposed constitution
  amendment" section of <resolved-path>/DEPLOYMENT_STRATEGY.md`. It MUST NOT invoke the constitution
  command itself.

#### Scope boundaries

- **FR-049**: The agent MUST NOT modify source, CI workflows, manifests, infrastructure-as-code, or
  configuration; MUST NOT run any command, build, or deployment; MUST NOT make a network request; and
  MUST NOT accept a credential or token. It recommends; the team applies, and each recommendation states
  the exact change where it can.
- **FR-050**: The agent decides deployment policy, not tactics: which tests exist belongs to
  `speckit.spectra.test-strategy`; alert implementation, IaC misconfiguration scanning, and incident
  handling belong to other agents. The document says so in a known-limitations statement.

#### Repository obligations (this change)

- **FR-051**: This repository's constitution Principle VII MUST be amended to name
  `<artifact-root>/DEPLOYMENT_STRATEGY.md` (`speckit.spectra.deployment-strategy`) as the third shipped
  singleton, as a MINOR bump (1.9.0 → 1.10.0) with a sync impact report.
- **FR-052**: The catalog channel MUST be released as extension version 1.20.0: `spectra/extension.yml`
  version and registrations, a matching `spectra/CHANGELOG.md` entry, the `spectra` entry in
  `catalog.json` (version, description where needed, command count, tags), a rebuilt
  `docs/packages/spectra.zip`, an updated `docs/index.html`, a hand-written `SPECTRA:AGENT` prose block,
  and regenerated agent listings that pass `tools/generate_agent_docs.py --check`.
- **FR-053**: The change MUST add standard-library `unittest` coverage asserting the command's
  registration, its singleton output path, its template registration and resolution stack, the six
  lenses, the five-question round, the never-write-the-constitution rule, and the handoff line.
- **FR-054**: The change MUST NOT modify the CLI channel: no change to `spectra_cli/` or the root
  `VERSION` file.

### Key Entities

- **Deployable**: something the project ships independently — its classification (service, static
  site, library, CLI/desktop, mobile, infra-only), its root, and the evidence for it.
- **Lens finding**: per deployable and lens — applicability and reason, current state with citations,
  recommendation, provenance, and on a re-run its `new`/`adopted`/`carried` mark.
- **Clarification record**: five entries, each with the question, the recommended answer, the answer
  taken, and a disposition of `answered`, `default_taken`, or `not_asked`.
- **Open question**: an item only the client or ops owner can answer, with who should answer it and what
  it blocks.
- **Proposed amendment**: unchecked checkbox items in the constitution's voice, with target section,
  add-or-amends marker, the embedded state, any conflict, and the approval outcome.
- **Deployment strategy document**: the single file at `<artifact-root>/DEPLOYMENT_STRATEGY.md` holding
  all of the above under parseable front matter.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In 100% of runs, the document addresses all six mandatory lenses, each marked applicable or
  not applicable with a reason.
- **SC-002**: In 100% of runs, every recommendation carries exactly one of the four provenances; a
  reviewer sampling any ten recommendations can trace each to a file, a document, an answer, or a stated
  convention.
- **SC-003**: The clarification round never presents more than one question per turn and never more than
  five questions; a user who says "use your defaults" at any point receives no further question.
- **SC-004**: Across runs on a library-only or CLI-only project, zero recommendations name
  infrastructure (clusters, container registries, database migrations) absent from that project's
  evidence.
- **SC-005**: The constitution file is unchanged by every run, including runs where the amendment is
  approved.
- **SC-006**: Every run that writes a document ends with a link to the actual path written and a
  `/speckit-constitution` line the user can paste without editing.
- **SC-007**: A re-run on an unchanged project produces one file, not two, and the user can confirm all
  five prior answers in five replies or one ("use your defaults").
- **SC-008**: Every open item that depends on client or ops knowledge appears in the open questions
  section rather than as an invented value; a reviewer finds zero fabricated identifiers.
- **SC-009**: The repository's `generate_agent_docs.py --check`, the version and command-count agreement
  between manifest and catalog, the package drift check, and the full unit test suite all pass after the
  change.

## Assumptions

- The agent runs inside a Spec Kit project with Spectra installed; it can read files and, ideally,
  search the repository. Without repository-wide search it continues on what it can traverse and reports
  the reduced coverage.
- The reference deployment strategy the maintainer uses on another project is a guide to the document's
  shape and depth, not a template to reproduce; its runbook-level sections (scheduled-job internals,
  alert tables) are deliberately out of the default document.
- Uploaded documents in formats the host agent can read (Markdown, text, PDF, Word) are read through the
  host's own capabilities; Spectra ships no parser.
- The agent is typically run once a project has a shape to deploy, but works on greenfield projects by
  falling back to declared intent and conventions.
- Existing singleton behaviour from `test-strategy` and `domain-analyzer` — root resolution, publication
  check, earlier-location handling, front-matter rules — is the model, and the new command mirrors it
  rather than inventing variants. There is no earlier location for this document, so no migration path is
  needed.
- Planned roster agents in the same phase (Observability Readiness, Infrastructure-as-Code Analysis,
  Incident Responder) remain planned and unaffected; this agent does not absorb their scope.
