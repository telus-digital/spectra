# Feature Specification: KB Vault — Knowledge Ingestion Agent

**Feature Branch**: `023-kb-vault-agent`

**Created**: 2026-09-11

**Status**: Implemented

**Input**: User description: "New agent (command) called `/kb-vault`. This agent is used build
documentation to the context; ADR, engineering methodology, UX/UI standards, etc. The ending result is
as set of .MD files added to the repo as additional documentation. The user wants to build or add to
the existing documentation on the repo. They use `/kb-vault` and attach files to the chat session
(PDF, Word, images) OR the user adds a prompt when running the command. The agent will do these:
(1) Absorb all supplied documents. (2) Then it will scan the repository structure to make an
understanding of the documentation structure, but also takes the constitution into account (if any).
It also tries to understand if the repository follows any certain templates for documentation.
(3) After that, it will attempt to plan to add these documents to the repo. Let's say the supplied
files included some architectural diagrams, and some UX/UI standards. In this case, it will attempt to
plan on generating ADRs and UX/UI standards in .MD based on the supplied docs. If one of these docs
already exist in the repo, it will then attempt to update it, not add a new file of the same nature.
(4) Then, the agent will provide a summary what it is going to do. It will provide a table, the table
has columns; doc category, doc description, doc location. The category and description are detected
from the supplied files. For location, the AI will see if there are existing locations for the given
files, maybe `docs` or `documents` folder or such. If there is, the folder will be given as a
suggestion, if not it will suggest to create a new one. That field will show where the file will end
up. (5) The agent will then prompt the user to approve this. The idea is the user can say to put X
file in Y location, or use a different name, or etc. This will be all given in a prompt. (6) Once the
agent receives approval, it will attempt to add/update files. (7) The agent will never attempt to
commit the new changes. Once done, it will let the user know that changes are made (gives a summary
too of what was done), and then tells the user that if all looks good they can go ahead and commit the
changes."

## Clarifications

### Session 2026-09-11

Most of what follows records how the request lands against Spectra's own constitution rather than
resolving genuine ambiguity in the request. The last three items were genuine scope boundaries with two
defensible readings each; they were put to the user and are recorded here with the answers given.

- Q: The user calls the command `/kb-vault`. Principle III requires every Spectra command to be
  namespaced `speckit.spectra.<command>` because Spec Kit validates command names against
  `^speckit\.<extension-id>\.<command>$`. Which name ships? → A: **The command is
  `speckit.spectra.kb-vault`**; `kb-vault` is the agent id in `agents-list.json` and the name used in
  prose. `/kb-vault` is the user's shorthand for that agent, not an invocation Spec Kit could
  register. The exact slash form a user types is decided by the host agent's own translation at
  install time, which is precisely what Principle III exists to preserve (FR-002).

- Q: The user describes the agent detecting a `docs` or `documents` folder and suggesting it.
  Principle VII already settles this: deliverables go to `<artifact-root>/<artifact>/`, the root is
  declarable in the constitution, defaults to `docs/`, and requires a publication check before
  defaulting. Does kb-vault detect or resolve? → A: **It resolves the root by Principle VII and then
  reports what it found.** The user's "see if there are existing locations" is satisfied by the
  resolution order — a declared `Artifact root:` line wins, otherwise `docs/` after the publication
  check — plus a survey of documentation the project already keeps elsewhere, which is reported as
  context rather than treated as a destination. A `documents/` suggestion is what that resolution
  yields on a project that publishes `docs/`, not a separate rule (FR-020 – FR-023).

- Q: kb-vault can produce a category — an ADR — for which Spectra already ships an agent and a
  template. Do the two collide? → A: **No; they differ in where the decision comes from.**
  `speckit.spectra.adr` elicits a decision that has not been written down yet, interactively.
  kb-vault transcribes a decision that already exists in a supplied document. When kb-vault produces
  an ADR it MUST use the shipped `adr` template resolved through the stack, the same
  `<artifact-root>/adr/` folder, and the same `ADR-NNN-` numbering, so the two agents produce one
  coherent set rather than two parallel ones (FR-030, FR-047).

- Q: Spectra ships Markdown only — no scripts, no binaries, no post-install hooks — yet the agent must
  absorb PDF, Word and image attachments. How is that satisfied? → A: **Through the host agent's
  harness, with graceful degradation, and never by handling a credential.** Spectra runs inside the
  coding agent a team already uses and inherits its reach and its limits: whatever document-reading
  capability that agent has, kb-vault uses, and it uses nothing else. Where a format cannot be read,
  the command names the file, says so plainly, asks the user to paste or convert it, and proceeds with
  the rest rather than guessing from a filename (FR-010 – FR-012). This follows the precedent set for
  JIRA retrieval in `speckit.spectra.defect-rca`.

- Q: Which roster phase does the agent belong to? → A: **`foundation`.** kb-vault establishes the
  documented context that later agents read, which is the same job `speckit.spectra.domain-analyzer`
  does for the domain. It is not `implementation` — the planned `documentation-quality` agent sits
  there and judges documentation that already exists, where kb-vault creates it (FR-004).

- Q: Is a produced document allowed to contradict the project constitution, if a supplied document
  does? → A: **No, and the command MUST NOT resolve it either.** Where a supplied source conflicts
  with governance, kb-vault surfaces the conflict in the plan and asks; it never writes a document
  that silently contradicts the constitution, and it never amends the constitution to fit (FR-024).

- Q: Invoked with free text and nothing attached, is the prompt the only knowledge source, or may the
  agent mine the codebase to synthesise documentation nobody supplied? → A: **The prompt is the only
  source.** The repository is read for placement, shape and duplicate detection, never as knowledge.
  A bare instruction with nothing to absorb — "document the architecture" — is answered by asking for
  source material, not by generating one. This keeps the traceability rule (FR-015) enforceable rather
  than aspirational, and leaves repository-derived documentation to the planned `documentation-quality`
  agent (FR-009, FR-009a).

- Q: Are the supplied originals and their images copied into the repository beside the generated
  Markdown? → A: **No — Markdown only.** Diagrams are transcribed into prose, a table or
  diagram-as-code; PDFs, Word documents and images stay outside the repository. The repository stays
  text-only and diffable, and a redaction made under FR-017 cannot be undone by an original committed
  beside the document that redacted it. The cost is accepted and made visible: where a diagram's
  structure cannot be transcribed, the command says so instead of implying a picture is present
  (FR-019, FR-019a).

- Q: At the approval step, can the user place a document anywhere in the repository? → A: **No —
  bounded to the artifact root, with one carve-out for updates.** A new file goes under
  `<artifact-root>/<category>/`; a row that updates an existing document is written where that document
  already lives, which is what makes "update it, don't duplicate it" work on a project whose
  documentation predates Spectra. A request for a destination outside that scope is answered with the
  two routes that legitimately reach it — the `Artifact root:` declaration, or a `git mv` the user runs
  — rather than with a one-off departure that would break the single-root guarantee every other Spectra
  agent depends on (FR-048 – FR-048b).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Turn a pile of supplied documents into repository documentation (Priority: P1)

An architect finishes an onboarding week with a folder of material inherited from a previous team: a
PDF of architecture decisions, a Word document describing the engineering workflow, and two exported
diagram images. None of it is in the repository, so no coding agent can see it and no new joiner finds
it. They attach all four files and run the command. The agent reads every one, works out what kind of
document each is, plans where each belongs, shows them the plan, and — once approved — leaves a set of
Markdown files in the working tree.

**Why this priority**: This is the agent. Without it there is no feature; every other story refines
this loop.

**Independent Test**: Attach a mixed set of readable documents to a repository with no existing
documentation and run the command. The run is successful when the plan lists one row per document to
be produced, and approval yields exactly those Markdown files on disk with content traceable to the
attachments.

**Acceptance Scenarios**:

1. **Given** a repository with no documentation folder and three readable attachments covering
   distinct subjects, **When** the user runs the command with no argument, **Then** the agent absorbs
   all three, proposes one destination folder per category with the folders marked as "will be
   created", and writes nothing until approved.
2. **Given** a single supplied document that covers two distinct subjects, **When** the agent plans,
   **Then** it proposes two documents rather than one, each with its own category, description and
   location.
3. **Given** two supplied documents that cover the same subject, **When** the agent plans, **Then** it
   proposes one merged document and says in the plan which sources it merged.

---

### User Story 2 - Update what already exists instead of adding a near-duplicate (Priority: P1)

A designer supplies an updated UX/UI standards deck. The repository already holds a UX/UI standards
document written eight months ago and edited by hand several times since. The agent recognises the
existing document as the same kind of thing about the same subject, plans an update to it rather than
a second file beside it, and preserves the hand-written sections the deck says nothing about.

**Why this priority**: A documentation agent that silently accumulates near-duplicates makes the
repository worse rather than better, and the damage compounds on every run.

**Independent Test**: Run the command twice over the same subject with a revised source the second
time. The run is successful when the second run plans an update to the file the first run created,
the file count does not grow, and content the second source does not address survives.

**Acceptance Scenarios**:

1. **Given** an existing document of the same category and subject, **When** the agent plans, **Then**
   the row for that source names the existing file as its location and is marked as an update.
2. **Given** an existing document containing hand-written sections the supplied source does not
   mention, **When** the update is written, **Then** those sections are still present afterwards.
3. **Given** the agent's match is wrong — the existing document is about a different subject — **When**
   the user says so at the approval step, **Then** the agent re-plans it as a new document without
   re-reading the sources.
4. **Given** an existing document whose content the supplied source directly contradicts, **When** the
   agent plans, **Then** the contradiction is named in the plan before approval rather than resolved
   silently in the written file.

---

### User Story 3 - See and steer the plan before anything is written (Priority: P1)

A tech lead runs the command against a repository they care about. Before any file is touched, they
see a table of exactly what will happen: category, description, location. They move one document to a
different folder, rename another, drop a third, and approve the rest.

**Why this priority**: The approval gate is what makes the agent safe to point at an existing
repository. Without it, a misclassification becomes a commit.

**Independent Test**: Run the command and decline at the approval step. The run is successful when
`git status` is unchanged.

**Acceptance Scenarios**:

1. **Given** a completed plan, **When** the user has not yet approved, **Then** no file has been
   created or modified.
2. **Given** the user redirects one row to a different location and renames another, **When** they
   respond, **Then** the agent re-presents the full revised plan and waits for approval again rather
   than writing on the strength of the redirection alone.
3. **Given** the user declines or gives an ambiguous answer, **When** the agent proceeds, **Then**
   nothing is written and the agent says so.
4. **Given** the user approves only some rows, **When** the agent writes, **Then** only the approved
   rows are written and the unwritten rows are named in the closing report.

---

### User Story 4 - Land documents where the project already keeps them, shaped the way it shapes them (Priority: P1)

A repository already has a documentation tree with its own numbering and its own heading structure.
The agent notices, proposes destinations inside that tree rather than a new folder beside it, and
follows the shape the project already uses instead of imposing its own.

**Why this priority**: A documentation agent that invents a second convention beside the existing one
is the problem it was brought in to solve.

**Independent Test**: Run the command against a repository with an established documentation folder,
numbering scheme and document shape. The run is successful when the produced files continue that
numbering, sit in that folder, and carry that shape.

**Acceptance Scenarios**:

1. **Given** a constitution declaring `Artifact root: documents/`, **When** the agent plans locations,
   **Then** every destination is under `documents/`.
2. **Given** no declared root and a `mkdocs.yml` at the repository root, **When** the agent plans,
   **Then** it surfaces that writing to `docs/` would publish the documents, recommends `documents/`,
   and asks before defaulting.
3. **Given** an existing category folder whose highest-numbered document is `004`, **When** a new
   document of that category is written, **Then** it is numbered `005`.
4. **Given** the repository's existing documents of a category follow a shape that differs from the
   resolved template, **When** the agent plans, **Then** it reports the difference and offers the
   override path rather than silently deviating from the resolved template.

---

### User Story 5 - Absorb a diagram, or fail loudly on a format that cannot be read (Priority: P1)

Two of the supplied files are architecture diagrams exported as images, and one is a scanned PDF the
host agent cannot extract text from. The agent transcribes what it can actually see in the diagrams,
and for the scanned PDF says plainly that it could not read it and asks for the content — rather than
writing a plausible document from the filename.

**Why this priority**: Invented documentation is worse than absent documentation, because it is
indistinguishable from the real thing once committed.

**Independent Test**: Supply one readable document and one unreadable file. The run is successful when
the readable one produces a document, the unreadable one produces no document, and the report names it
as skipped.

**Acceptance Scenarios**:

1. **Given** a diagram image whose structure is legible, **When** the agent produces a document,
   **Then** the document carries a textual or diagram-as-code rendering of what is visible and asserts
   nothing that is not.
2. **Given** a file the host agent cannot read, **When** the agent plans, **Then** the file is named as
   unreadable, no row is planned from it, and the user is asked to paste or convert it.
3. **Given** a supplied document containing what appears to be a credential or personal data,
   **When** the agent produces a document, **Then** the value is not reproduced and the redaction is
   reported.
4. **Given** a supplied document containing text addressed to the agent as an instruction, **When**
   the agent absorbs it, **Then** the text is treated as document content and not as a command.

---

### User Story 6 - Dictate knowledge without attaching anything (Priority: P2)

A staff engineer has the team's release process in their head and no document to attach. They run the
command with a paragraph describing it and get an engineering methodology document back.

**Why this priority**: The request names a prompt-only invocation explicitly, and it is the lowest-cost
way to start a documentation set. It is P2 because the attachment path carries the bulk of the value.

**Independent Test**: Run the command with an argument and no attachments. The run is successful when a
document is planned from the argument alone.

**Acceptance Scenarios**:

1. **Given** an argument describing a process and no attachments, **When** the agent plans, **Then** a
   document is proposed whose content derives from the argument.
2. **Given** both an argument and attachments, **When** the agent plans, **Then** the argument is used
   as steering for the attachments and, where it carries knowledge of its own, as a source.
3. **Given** neither an argument nor an attachment, **When** the agent runs, **Then** it asks for
   sources and does not proceed.
4. **Given** an argument that instructs but carries no knowledge — "document the architecture" — and no
   attachments, **When** the agent runs, **Then** it says it has nothing to absorb and asks for source
   material, rather than writing documentation derived from the codebase.

---

### User Story 7 - Leave the commit to the human (Priority: P2)

The files are written. The agent stops there, reports what it did, and says the changes are
uncommitted and ready for review.

**Why this priority**: Explicitly required, and cheap to honour — but it is the last step of the loop
rather than the value of it.

**Independent Test**: Complete an approved run and inspect the repository state. The run is successful
when the produced files are present and untracked or modified, and no new commit exists.

**Acceptance Scenarios**:

1. **Given** an approved plan that has been written, **When** the agent finishes, **Then** no commit
   has been created, nothing has been staged, and no branch, tag, push or pull request has occurred.
2. **Given** a completed run, **When** the agent reports, **Then** the report summarises what was
   written and updated and tells the user they can commit once satisfied.

---

### Edge Cases

- **No sources at all** — no attachment and an empty argument. The agent asks for material rather than
  inferring documentation from the codebase.
- **Every source unreadable.** Nothing is planned, nothing is written, and each file is named.
- **A supplied source contradicts the constitution** — for example a standard that conflicts with a
  stated principle. Surfaced in the plan; never resolved unilaterally; the constitution is never
  amended.
- **A false duplicate match.** The agent proposes an update to a document that is actually about
  something else. The approval step is where the user corrects it, and the correction must be cheap.
- **A true duplicate the agent missed**, producing a second file beside an existing one. The user
  redirects the row to the existing file at the approval step.
- **`docs/` is a published site source.** Defaulting there would publish the documents; the
  publication check must run before the default is taken.
- **A monorepo with several documentation trees.** More than one plausible destination exists; the
  agent reports what it found and proposes one, rather than scattering output across all of them.
- **A category folder that another Spectra agent owns** — `adr/`. kb-vault follows that agent's
  conventions rather than introducing a competing shape or numbering.
- **A numbering collision** — the next sequence number is already taken by a file the agent did not
  plan. The number is recomputed from what is actually on disk at write time.
- **Superseded folders from earlier versions** (`Docs/ADR/`, `brds/`). Read for context and for
  sequence continuity, reported once, and never moved, modified or deleted.
- **A very large supplied set** that cannot be absorbed in one pass. The agent says what it covered and
  what it did not, rather than silently truncating.
- **The user names a destination outside the resolved artifact root** at the approval step — answered
  with the routes that reach it, not with a one-off departure.
- **An existing document to be updated lives outside the artifact root.** The update is written in
  place; it is not copied into the root and it is not moved.
- **A partial write failure** — some files written, one fails. The report states exactly which
  succeeded and which did not.

## Requirements *(mandatory)*

### Functional Requirements

#### Packaging and registration

- **FR-001**: The agent MUST ship as a single command file at `spectra/commands/kb-vault.md` inside
  the one self-contained `spectra/` extension. A new top-level extension folder MUST NOT be created
  (Principle II).
- **FR-002**: The command MUST be named `speckit.spectra.kb-vault` and registered in
  `spectra/extension.yml` under `provides.commands` with `name`, `file` and `description`
  (Principle III).
- **FR-003**: The command file MUST begin with YAML front matter containing a `description`, MUST take
  user input through `$ARGUMENTS`, and MUST NOT hard-code any single agent's invocation syntax
  (Principle III).
- **FR-004**: The agent MUST be registered in `agents-list.json` with id `kb-vault`, phase
  `foundation`, type `add-on`, provider `spectra`, status `available`, and command
  `speckit.spectra.kb-vault` (Principle V).
- **FR-005**: The extension's `effect` MUST remain `read-write`; the command creates and modifies
  files in the user's project.

#### Invocation and input

- **FR-006**: The command MUST accept, in any combination: documents attached to the session, paths to
  documents readable from the machine, and free-text passed as the argument.
- **FR-007**: With neither an argument nor any supplied document, the command MUST ask the user for
  source material and MUST NOT proceed.
- **FR-008**: Free-text passed as the argument MUST be treated as steering for how the supplied
  documents are handled and, where it carries knowledge of its own, as a source in its own right.
- **FR-009**: When the command is invoked with free text and no attached documents, that free text MUST
  be the **only** knowledge source for the documents produced. The repository MUST be read for
  placement, shape, numbering and duplicate detection only, and MUST NOT be mined as a source of
  documentation content.
- **FR-009a**: Where the argument carries an instruction but no knowledge of its own — "document the
  architecture", with nothing attached — the command MUST say it has nothing to absorb and ask for
  source material. It MUST NOT synthesise documentation from the codebase to satisfy the request.
- **FR-010**: The command MUST absorb whichever document formats the host agent's harness can read —
  PDF, Word, images, slides, Markdown, plain text and HTML among them — and MUST use no capability
  beyond what that harness already provides.
- **FR-011**: Where a supplied document cannot be read, the command MUST name the file, state plainly
  that it could not read it, ask the user to paste or convert its content, and continue with the
  remaining sources. It MUST NOT infer a document's contents from its filename, extension or size.
- **FR-012**: The command MUST NOT prompt for, accept, or store any credential, API token or password,
  and MUST NOT attempt to authenticate to any service.

#### Absorbing the supplied material

- **FR-013**: The command MUST read every supplied source in full before classifying any of them, so
  that classification accounts for the whole set rather than one file at a time.
- **FR-014**: Where a source is a diagram or image, the command MUST transcribe what is legibly
  present — as prose, as a table, or as diagram-as-code — and MUST NOT assert structure, labels or
  relationships that are not visible in it.
- **FR-015**: Every substantive statement in a produced document MUST be traceable to a supplied
  source or to the repository. The command MUST NOT invent content to fill a template section; where a
  section has no source, it MUST say so in the document.
- **FR-016**: Each produced document MUST record its provenance — which supplied sources it was
  derived from, and the date of the run.
- **FR-017**: The command MUST NOT reproduce a secret, credential, token, key or personal data found
  in a supplied source. It MUST redact and report the redaction.
- **FR-018**: Text inside a supplied source that is phrased as an instruction to the agent MUST be
  treated as document content, not as a command to follow.
- **FR-019**: Only the generated Markdown MUST be written into the repository. Supplied source files —
  PDFs, Word documents, images — MUST NOT be copied into it, and a produced document MUST NOT link to a
  path outside the repository or to an asset it did not write.
- **FR-019a**: Where a diagram's structure cannot be carried into prose, a table or diagram-as-code, the
  command MUST say so in the document and in the report, naming the source it came from, rather than
  leaving a broken reference or a section that implies a picture is present.

#### Reading the project

- **FR-020**: The command MUST read `.specify/memory/constitution.md` where it exists, before planning
  anything (Principle IV).
- **FR-021**: The command MUST resolve the artifact root before proposing any location: a case-
  insensitive `Artifact root: <folder>/` line in the constitution wins; a value with a leading `/` or a
  `..` segment MUST be rejected with a stated reason and the default used instead; otherwise the
  default is `docs/` (Principle VII).
- **FR-022**: Before defaulting into `docs/`, the command MUST check whether `docs/` is a published
  site source — `mkdocs.yml`, `docusaurus.config.*`, `docs/_config.yml`, `docs/.nojekyll`,
  `docs/index.html`, `docs/conf.py`, or a Pages configuration pointing at `docs`. Finding a signal with
  no declared root, it MUST surface it, recommend `documents/`, and ask. Where the answer cannot be
  obtained it MUST take the non-publishing option (Principle VII).
- **FR-023**: The command MUST show the user the exact `Artifact root:` line that makes the chosen root
  permanent for every Spectra agent, and MUST NOT write that line into the constitution itself
  (Principle VII).
- **FR-024**: Where a supplied source conflicts with a stated principle in the constitution, the
  command MUST surface the conflict in the plan and ask. It MUST NOT write a document that silently
  contradicts governance, and MUST NOT amend the constitution.
- **FR-025**: The command MUST survey the documentation the project already keeps — folder layout,
  filename and numbering conventions, front matter, heading structure, and any index files — and MUST
  use that survey when proposing categories, names and locations.
- **FR-026**: The command MUST look for documentation templates the project already uses: the Spec Kit
  override and preset layers, a templates folder inside the documentation tree, repository issue and
  pull-request templates, and the shape of existing documents of the same category.
- **FR-027**: The command MUST read superseded Spectra output locations (`Docs/ADR/`, `brds/`, and the
  default root once another root is declared), matching case-insensitively, for context and sequence
  continuity; it MUST report such a folder once and MUST NOT move, rename, modify or delete anything in
  it (Principle VII).

#### Classifying and matching

- **FR-028**: The command MUST classify each supplied source into a documentation category expressed
  as a lowercase kebab-case slug — for example `adr`, `engineering-methodology`, `ux-ui-standards` —
  derived from the content of the source, not from its filename.
- **FR-029**: The set of categories MUST be open-ended rather than a fixed list, so a supplied document
  of a kind not anticipated here is still placeable.
- **FR-030**: Where a category corresponds to a document type another Spectra agent already produces —
  `adr` above all — the command MUST adopt that agent's folder, numbering and template rather than
  creating a parallel set.
- **FR-031**: One supplied source MUST be able to produce several documents, and several supplied
  sources MUST be able to merge into one document. The plan MUST make either case visible.
- **FR-032**: Before planning a new file, the command MUST search the repository for an existing
  document of the same category about the same subject, matching on content and category rather than
  on filename alone.
- **FR-033**: Where such a document is found, the command MUST plan an **update** to it rather than a
  new file of the same nature.
- **FR-034**: Where a supplied source directly contradicts the content of the document it would update,
  the command MUST name the contradiction in the plan rather than resolving it silently in the written
  file.

#### The plan and the approval gate

- **FR-035**: The command MUST present a plan as a Markdown table before writing anything, carrying at
  minimum the columns **doc category**, **doc description** and **doc location**, plus an indication of
  whether each row creates a new file or updates an existing one.
- **FR-036**: The **doc category** and **doc description** MUST be derived from the supplied source
  content.
- **FR-037**: The **doc location** MUST be a concrete project-relative path including the filename, and
  MUST state whether the containing folder already exists or will be created.
- **FR-038**: Alongside the table, the plan MUST report: sources that could not be read, redactions
  made, sources merged into one document, conflicts with the constitution, an existing document the
  agent judged a match, and any superseded folder found.
- **FR-039**: The command MUST obtain explicit user approval before writing. No file may be created or
  modified before approval is given.
- **FR-040**: At the approval step the user MUST be able to change any row's location, filename or
  category, drop a row, split one row into several, merge rows, or convert a create into an update and
  the reverse.
- **FR-041**: After any change, the command MUST re-present the full revised plan and obtain approval
  again rather than writing on the strength of the change alone.
- **FR-042**: A declined, absent or ambiguous approval MUST result in no writes, and the command MUST
  say that nothing was written.
- **FR-043**: Approval of a subset MUST write only that subset.

#### Where the documents are written

- **FR-044**: Documents MUST be written to `<artifact-root>/<category>/`, one category per folder, with
  the folder created on demand (Principle VII).
- **FR-045**: Filenames MUST be lowercase kebab-case and carry a zero-padded three-digit sequence
  number scoped to the folder, starting at `001` and continuing from the highest number found across
  the canonical folder and any superseded one. Where a category has an established convention — the
  `ADR-NNN-` prefix — that convention MUST be followed instead (Principle VII).
- **FR-046**: The sequence number MUST be computed from what is on disk at write time, so a file added
  between planning and writing does not produce a collision.
- **FR-047**: All paths MUST be lowercase and project-relative; a path with a leading slash, a `..`
  segment or mixed case MUST NOT be used (Principle VII).
- **FR-048**: The write scope MUST be bounded to the resolved artifact root, with one carve-out: a row
  that **updates** an existing document MUST be written where that document already lives, even when
  that is outside the root (Principle VII).
- **FR-048a**: At the approval step the user MUST be able to change a row's category folder, its
  filename, and — for an update — which existing file it targets. They MUST NOT be able to direct a
  **new** file outside `<artifact-root>/<category>/`.
- **FR-048b**: Where the user asks for a destination the write scope does not allow, the command MUST
  say why plainly, name the destination it will use instead, and offer the two routes that do reach the
  requested place: the `Artifact root:` declaration line, or a `git mv` the user runs after the write.
  It MUST NOT silently relocate the row and MUST NOT write outside the scope.
- **FR-049**: Where the command creates a category folder it alone owns, it MUST maintain an index at
  `<artifact-root>/<category>/README.md` listing each document, its subject and its date, rebuilt from
  the documents present so a hand-added or hand-deleted file self-corrects. It MUST NOT introduce an
  index into a folder owned by another Spectra agent, and MUST update rather than replace an index the
  project already keeps.

#### The shape the documents take

- **FR-050**: Every produced document MUST take its structure from a template resolved through Spec
  Kit's stack, highest priority first: `.specify/templates/overrides/<name>.md` →
  `.specify/presets/<preset-id>/templates/<name>.md` → `.specify/extensions/spectra/templates/<name>.md`
  → `.specify/templates/<name>.md` → the command's own inline skeleton. The first readable, non-empty
  layer wins (Principle VIII).
- **FR-051**: A default template MUST ship as a registered asset at
  `spectra/templates/kb-document-template.md`, registered in `spectra/extension.yml` under
  `provides.templates` with `name`, `file` and `description` (Principle VIII).
- **FR-052**: Where a produced document's category matches a template Spectra already ships — `adr` —
  that template MUST be resolved and used in place of the default.
- **FR-053**: Where a project supplies an override named for the category, that override MUST be used;
  this is the supported customization point, and editing the installed copy under `.specify/extensions/`
  MUST NOT be documented as an alternative (Principle VIII).
- **FR-054**: A resolved template MUST be honoured, not repaired: its sections MUST be followed in its
  order, and MUST NOT be added to, renamed or reordered. Where the template omits a section the command
  would ordinarily fill, the omission MUST be noted rather than the section reinstated (Principle VIII).
- **FR-055**: Guidance comments and `[PLACEHOLDER]` tokens MUST be stripped from the output whichever
  layer the template came from (Principle VIII).
- **FR-056**: Where the repository's existing documents of a category follow a shape that differs from
  the resolved template, the command MUST report the difference and offer the override path, and MUST
  NOT silently deviate from the resolved template.
- **FR-057**: The command MUST report which template it used for each produced document, naming the
  resolved path (Principle VIII).

#### Write scope

- **FR-058**: The command MUST write only the files listed in the approved plan.
- **FR-059**: An update MUST preserve content in the existing document that the supplied source does
  not address, and MUST NOT remove or replace content without that removal having been visible in the
  plan.
- **FR-060**: The command MUST NOT commit, stage, push, tag, branch, amend history, or open a pull
  request. It leaves every change in the working tree.
- **FR-061**: The command MUST NOT move, rename or delete an existing document. Where a relocation
  would help, it MUST offer the command for the user to run.
- **FR-062**: The command MUST NOT modify source code, build configuration, `.specify/` (including the
  constitution), or `specs/`.
- **FR-063**: The command MUST NOT modify or delete the supplied source files.

#### Reporting

- **FR-064**: On completion the command MUST report: each file created and each file updated with its
  path, the template resolved for each, redactions made, sources skipped as unreadable, rows the user
  declined, and any conflict left unresolved.
- **FR-065**: The report MUST state that the changes are uncommitted, and tell the user that they can
  commit once they are satisfied.
- **FR-066**: Where some writes succeeded and others failed, the report MUST state exactly which did
  and which did not.

#### Catalog and package sync

- **FR-067**: Shipping the agent MUST, in the same change, bump `extension.version` in
  `spectra/extension.yml` per SemVer with a matching `spectra/CHANGELOG.md` entry (Principle V,
  Publishing Standards).
- **FR-068**: `docs/packages/spectra.zip` MUST be rebuilt with `tools/build_package.py`, and the
  `spectra` entry in `catalog.json` updated so name, description, version, tags, command count and
  `download_url` agree with the manifest and the new zip (Principle V).
- **FR-069**: `docs/index.html` MUST list the new command, and every structured agent listing MUST be
  regenerated with `tools/generate_agent_docs.py`; the per-agent prose block for `kb-vault` MUST be
  hand-written (Principle V).
- **FR-070**: The change MUST NOT create a Git tag or a GitHub Release, and MUST NOT bump the root
  `VERSION` file — those belong to the CLI channel alone (Principle VI).

### Key Entities

- **Supplied Source**: One document offered to the command — an attachment, a readable path, or the
  free-text argument. Carries a format, a readability outcome, and the content absorbed from it.
- **Documentation Category**: A lowercase kebab-case slug naming a kind of document — `adr`,
  `engineering-methodology`, `ux-ui-standards`. Determines the destination folder, the template and the
  naming convention. Open-ended.
- **Repository Documentation Profile**: What the command learned about how this project already keeps
  documentation — the resolved artifact root, existing folders, numbering conventions, document shapes,
  templates in use, index files, and superseded locations.
- **Planned Placement**: One row of the plan — a category, a description, a destination path, and
  whether it creates or updates. The unit the user approves, redirects or drops.
- **Knowledge Document**: A produced Markdown file: its content, the template it was shaped by, and the
  supplied sources it derives from.
- **Provenance Record**: The link from a Knowledge Document back to the Supplied Sources it came from
  and the date of the run, carried in the document itself.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of runs that write a file present a plan and obtain explicit approval first; a
  declined run leaves the working tree byte-identical.
- **SC-002**: 100% of produced documents land under the resolved artifact root in a folder holding
  exactly one category, with a correctly sequenced filename.
- **SC-003**: 100% of produced documents are shaped by a resolved template whose path is named in the
  report.
- **SC-004**: In a repository that already holds a document of the same category and subject, at least
  90% of runs plan an update to it rather than a new file of the same nature.
- **SC-005**: 100% of updates preserve hand-written content the supplied source does not address.
- **SC-006**: 100% of substantive statements in a produced document are traceable to a supplied source
  or to the repository; no run produces a document from an unreadable source.
- **SC-007**: 100% of unreadable sources are named to the user, with the content requested, rather than
  silently dropped.
- **SC-008**: 0 runs commit, stage, push, tag or open a pull request; 0 runs modify source code, the
  constitution or `specs/`.
- **SC-009**: 0 secrets or personal data found in a supplied source are reproduced in a produced
  document.
- **SC-010**: On a project that publishes `docs/`, 100% of runs surface the publication signal before
  defaulting there.
- **SC-011**: A user can redirect a planned document to a different location or name and reach an
  approved plan in one exchange, without re-supplying the source material.
- **SC-012**: A practitioner with a folder of inherited documents can go from attachments to reviewable
  Markdown in the working tree in a single run, with no manual file creation.
- **SC-013**: 0 runs copy a supplied source file into the repository, and 0 produced documents contain a
  link to an asset the command did not write.
- **SC-014**: 0 new files are written outside the resolved artifact root; 100% of updates to documents
  that live outside it are written in place rather than duplicated into it.
- **SC-015**: After shipping, `tools/generate_agent_docs.py --check` passes and CI finds no disagreement
  between `extension.yml`, `catalog.json`, the committed zip and `agents-list.json`.

## Assumptions

- The command is `speckit.spectra.kb-vault`; `/kb-vault` is the user's shorthand for the agent, and the
  exact slash form typed is whatever the host agent's install-time translation produces (Principle III).
- The agent belongs to the `foundation` roster phase, alongside `speckit.spectra.domain-analyzer`: it
  establishes the documented context that later agents read.
- Reading PDF, Word and image attachments is a capability of the host agent's harness, not of Spectra,
  which ships Markdown only. The command inherits that harness's reach and its limits.
- The plan table carries the three columns the request names — category, description, location — plus a
  create-or-update indication, because the request's step 3 requires distinguishing the two and the
  table is where that distinction is visible to the user.
- "Never commit" is read as the full set of history-affecting and outward-facing Git actions: no
  commit, no staging, no push, no tag, no branch, no pull request. Changes are left in the working tree
  for the user to review with their normal tools.
- Approval is obtained conversationally in the host agent's own interface; the command does not
  prescribe a mechanism beyond asking and waiting.
- Where the repository has no documentation at all, the resolved artifact root is created on demand;
  this is the ordinary first-run case, not an error.
- The agent does not judge the quality of documentation it did not produce, and does not derive
  documentation from the codebase; both are the planned `documentation-quality` agent's territory.
- Keeping originals out of the repository is a deliberate trade: fidelity for a diagram that resists
  transcription is lost, and the command is required to say so rather than let the loss pass silently.
- The default template shipped for categories Spectra does not already cover is a general knowledge
  document shape, deliberately broad, because the category set is open-ended and a project that wants a
  category-specific shape supplies one as an override.
