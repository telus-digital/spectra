# Tasks: KB Vault — Knowledge Ingestion Agent

**Input**: Design documents from `/specs/023-kb-vault-agent/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md),
[data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md)

**Tests**: Included, and not optional here. This repository enforces Principles V, VII and VIII with a
Python suite whose checks derive from per-command registries — `tests/test_doc_output_paths.py`,
`tests/test_document_templates.py`, `tests/test_roster_data.py` — so a new document agent absent from
them is unguarded. Test tasks are in Phase 11.

**Organization**: by user story, in the priority order the spec assigns. One caveat particular to this
project: the runtime deliverable is a **single Markdown file**, so most tasks add a section to
`spectra/commands/kb-vault.md` and are therefore **strictly sequential within a phase**. Genuine
parallelism appears in Phase 10 (publishing, different files) and Phase 11 (tests, different files).

**The two items to carry through**:

1. Unlike every prior document agent, this command does **not** join `CANONICAL` in
   `tests/test_doc_output_paths.py` — it has no single output folder. It joins a **new `MULTI_CATEGORY`
   registry** that T063 creates, and `DOCUMENT_COMMANDS` becomes the union of both (research **R6**).
   Membership of that union is what subjects the command to the literal-string assertions below.
2. The inline skeleton in the command file and the shipped template must declare **the same H2 sections
   in the same order** — `ShippedAndInlineStructuresAgree.test_sections_match_in_order` compares them
   directly. T009 and T010 are therefore a pair, and editing one without the other fails the suite.
3. Adding `"kb-vault.md"` to `DOCUMENT_COMMANDS` in `tests/test_document_templates.py` (T065) enrols the
   command in four more assertions: it must name every resolution layer, name the override layer first,
   carry the inline skeleton, and report the template it used. Those are prose obligations on T008,
   T010 and T037, not test-authoring work.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel — different file, no dependency on an incomplete task
- **[Story]**: the user story the task serves (US1–US7)
- Every task names its file and cites the requirements it implements

## Path Conventions

This is a Spec Kit extension, not an application. There is no `src/`.

- Runtime deliverables: `spectra/commands/kb-vault.md`, `spectra/templates/kb-document-template.md`
- Manifest and catalog: `spectra/extension.yml`, `catalog.json`
- Roster and docs: `agents-list.json`, `README.md`, `AGENTS_LIST.md`, `docs/index.html`, `spectra/README.md`
- Package: `docs/packages/spectra.zip` (built, never hand-edited)
- Tests: `tests/`

### The literal strings `DOCUMENT_COMMANDS` membership demands

Exact substring assertions in `tests/test_doc_output_paths.py` and `tests/test_document_templates.py`,
not paraphrasable. Most land in Phase 2, and every later task that edits the command file must leave
them intact.

| Must appear literally | Asserted by | Landed in |
|---|---|---|
| `Artifact root:` | `test_each_document_command_reads_the_declaration` | T005 |
| `never write it` | `test_each_document_command_refuses_to_write_the_declaration` | T005 |
| `mkdocs.yml`, `docusaurus.config`, `docs/_config.yml`, `docs/.nojekyll`, `docs/index.html`, `docs/conf.py` | `test_each_document_command_checks_for_a_published_docs_folder` | T005 |
| `documents/` | `test_each_document_command_prefers_the_non_publishing_fallback` | T005 |
| `Inline template skeleton` | `test_each_command_keeps_an_inline_last_resort` | T010 |
| `template you used` (or `which template you used`) | `test_each_command_reports_the_template_it_used` | T037 |

And three sweeps over **all** command files, which every prose task is subject to:

- **No absolute output path.** The tokens `` `/docs/ ``, ` /docs/`, `` `/brds ``, ` /brds/` fail the
  sweep. Never put a space or a backtick immediately before a leading slash on a path.
- **Every `docs/<slug>/` reference is lowercase kebab-case.** `docs/ux-ui-standards/` passes;
  `docs/UX-UI-Standards/` does not. The generic form `<artifact-root>/<category>/` is not matched by the
  sweep at all, because `<` is not alphanumeric — prefer it, and use concrete `docs/…` paths only in
  examples.
- **A legacy folder (`docs/ADR`, `brds/`) may appear only in a legacy-handling clause**, within two
  lines of one of `legacy`, `before 1.6.0`, `git mv`, `no longer`, ``not ` ``, `read-only`,
  `case-insensitiv` — and never on a line that also contains `write`, `writes`, `writing`,
  `create the file`, `Ensure the directory`, or `git add`.

---

## Phase 1: Setup

**Purpose**: the file exists, declares what it takes, and states its limit.

- [X] T001 Create `spectra/commands/kb-vault.md` with YAML front matter carrying a `description`, and an H1 stating the command absorbs supplied documents and lands them as repository Markdown (FR-001, FR-003, Principle III)
- [X] T002 Add the "User Input" section to `spectra/commands/kb-vault.md` taking `$ARGUMENTS`, plus the five-row input-state table from [contracts/command-interface.md](./contracts/command-interface.md) (FR-006 – FR-008, FR-009a)
- [X] T003 Add the "What this command never does" table to `spectra/commands/kb-vault.md` — no credential, no network request, no write before approval, no copied original, no commit or stage, no move or delete, no edit of source, `.specify/` or `specs/` (FR-012, FR-017 – FR-019, FR-060 – FR-063)
- [X] T004 Add the "What this command writes" section to `spectra/commands/kb-vault.md` naming exactly three write locations — a created document under `<artifact-root>/<category>/`, an updated document at its existing path, and a category index — and stating that all of them happen after approval and nowhere else (FR-044, FR-048, FR-049, FR-058)

**Checkpoint**: the file exists, declares its input surface, and states its limit.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: the resolution machinery, the template asset, and the safety rules every story depends on.

**⚠️ CRITICAL**: no user story work can begin until this phase is complete. T005 alone carries five of
the six literal-string assertions.

- [X] T005 Add the artifact-root resolution step to `spectra/commands/kb-vault.md`: the case-insensitive `Artifact root:` line wins, a leading-slash or `..` value is rejected with a stated reason, otherwise `docs/` **after** checking `mkdocs.yml`, `docusaurus.config.*`, `docs/_config.yml`, `docs/.nojekyll`, `docs/index.html`, `docs/conf.py` and a Pages configuration; on a signal, recommend `documents/` and ask; where no answer is obtainable, take the non-publishing option; offer the declaration line and state that you **never write it** (FR-021 – FR-023, Principle VII)
- [X] T006 Add the repository-survey step to `spectra/commands/kb-vault.md` — folder layout, filename and numbering conventions, front matter, heading shapes, existing indexes, project-kept templates — and state that the survey decides placement and shape only, never content (FR-025, FR-026, FR-009, Principle IV)
- [X] T007 Add the superseded-folder clause to `spectra/commands/kb-vault.md`: read `Docs/ADR/` and `brds/` case-insensitively for context and numbering continuity, report once, and leave them alone with a `git mv` offered — observing the legacy-context and write-instruction rules under Path Conventions (FR-027, FR-061)
- [X] T008 Add the template-resolution step to `spectra/commands/kb-vault.md` naming all four layers in order — `.specify/templates/overrides/`, `.specify/presets/`, `.specify/extensions/spectra/templates/`, `.specify/templates/` — resolving `<category>-template` and falling back to `kb-document-template`, with the reserved category resolving that agent's template instead (FR-050 – FR-053, research R3)
- [X] T009 Create `spectra/templates/kb-document-template.md` — a deliberately broad knowledge-document shape with H2 sections covering purpose and scope, the substance, decisions or rules recorded, open questions and gaps, and provenance; guidance comments included, no executable content (FR-051, Principle VIII)
- [X] T010 Add the `Inline template skeleton` section to `spectra/commands/kb-vault.md` as a fenced block whose H2 sections match T009's **exactly, in order** — `ShippedAndInlineStructuresAgree` compares them directly (Principle VIII)
- [X] T011 Add the reading-and-degrading step to `spectra/commands/kb-vault.md`: attempt every source, report readability per file, name an unreadable one and ask for its content, continue with the rest, and never infer content from a filename, extension or size (FR-010, FR-011, research R7)
- [X] T012 Add the data-not-instructions rule to `spectra/commands/kb-vault.md`: text inside a supplied source addressed to the agent is document content, transcribed where relevant and never obeyed — including claims of authority, urgency or prior authorisation, and including a named destination or repository action (FR-018, research R10)
- [X] T013 Add the secrets rule to `spectra/commands/kb-vault.md`: a credential, token, key or personal data found in a source is never reproduced; the redaction is reported by kind and the value appears nowhere in the output (FR-017)
- [X] T014 Add the write-scope enforcement rule to `spectra/commands/kb-vault.md`, enforced **at plan construction**: a destination the scope forbids never reaches the table; say why, name the destination that will be used, and offer the `Artifact root:` line and the `git mv` — and state that the write step trusts the approved table and resolves no path of its own (FR-048a, FR-048b, research R11)

**Checkpoint**: root resolution, the survey, template resolution, the shipped template, degradation, the
injection posture, redaction and the write-scope boundary are all in place.

---

## Phase 3: User Story 1 — Turn a pile of supplied documents into repository documentation (Priority: P1) 🎯 MVP

**Goal**: attachments in, Markdown out, with a table in between.

**Independent Test**: attach a mixed set of readable documents to a repository with no documentation.
One row per document to be produced; approval yields exactly those files, with content traceable to the
attachments.

- [X] T015 [US1] Add the absorption step to `spectra/commands/kb-vault.md`: read every supplied source **in full** before classifying any of them, so classification accounts for the whole set (FR-013)
- [X] T016 [US1] Add the classification step to `spectra/commands/kb-vault.md`: derive a lowercase kebab-case category from the source's **content**, never its filename; the set is open-ended; one source may yield several documents and several sources may merge into one (FR-028, FR-029, FR-031)
- [X] T017 [US1] Add the reserved-map table to `spectra/commands/kb-vault.md` routing an architecture decision, business requirements document, impact analysis, test strategy and defect RCA to that agent's folder, naming convention and template (FR-030, research R2, [contracts/classification.md](./contracts/classification.md))
- [X] T018 [US1] Add the placement-construction step to `spectra/commands/kb-vault.md` producing, per planned document, a category, a description from source content, a concrete project-relative location including filename, a create-or-update action, its sources, its template and its notes (FR-035 – FR-037, [data-model.md](./data-model.md))
- [X] T019 [US1] Add the plan-table rendering to `spectra/commands/kb-vault.md` — the four columns and the beneath-table notes (unreadable sources, merges, splits, contradictions, constitution conflicts, superseded folder, matches as judgements, the `Artifact root:` offer) per [contracts/plan-table.md](./contracts/plan-table.md) (FR-035, FR-038)
- [X] T020 [US1] Add the write step to `spectra/commands/kb-vault.md`: create each approved document from its resolved template, following its sections in its order without adding, renaming or reordering, and stripping guidance comments and `[PLACEHOLDER]` tokens (FR-054, FR-055)
- [X] T021 [US1] Add the provenance requirement to `spectra/commands/kb-vault.md`: every produced document names the sources it derives from and the run date, and names no redacted value (FR-016)
- [X] T022 [US1] Add the traceability rule to `spectra/commands/kb-vault.md`: every substantive statement traces to a supplied source or to the repository's structure, and a section with no source says so rather than being filled (FR-015)

**Checkpoint**: a set of readable attachments produces a plan table and, on approval, a set of correctly
shaped documents with provenance.

---

## Phase 4: User Story 2 — Update what already exists instead of adding a near-duplicate (Priority: P1)

**Goal**: the second run over the same subject grows no file count.

**Independent Test**: run twice over the same subject with a revised source. The second run plans an
update to the first run's file, the count does not grow, and hand-written content survives.

- [X] T023 [US2] Add the duplicate-detection step to `spectra/commands/kb-vault.md` as two staged reads — candidate folders from the survey, shortlist by filename and heading, then read the shortlist — bounded by the documentation tree rather than the repository, and naming no search tool (FR-032, research R5)
- [X] T024 [US2] Add the three match axes to `spectra/commands/kb-vault.md` — category, subject, scope — and state that title similarity alone is never a match (FR-032, [contracts/classification.md](./contracts/classification.md))
- [X] T025 [US2] Add the update-row rule to `spectra/commands/kb-vault.md`: a match produces an `Update` row whose location is the matched file's existing path, wherever that is, including outside the artifact root (FR-033, FR-048)
- [X] T026 [US2] Add the update-write rules to `spectra/commands/kb-vault.md`: content the sources do not address survives, nothing is removed that the plan did not show being removed, the file is not renamed, renumbered or moved, and the existing document's own shape is followed where it differs from the resolved template (FR-059, FR-061)
- [X] T027 [US2] Add the contradiction and judgement clauses to `spectra/commands/kb-vault.md`: a source contradicting the document it would update is named in the plan rather than resolved silently, and a match is stated as a judgement the user can correct at the gate in one sentence without re-absorption (FR-034)

**Checkpoint**: a revised source updates the existing document in place, preserving what it does not
address, and a wrong match costs one sentence to correct.

---

## Phase 5: User Story 3 — See and steer the plan before anything is written (Priority: P1)

**Goal**: the gate is unambiguous, and declining costs nothing.

**Independent Test**: run the command and decline. `git status` is unchanged.

- [X] T028 [US3] Add the gate to `spectra/commands/kb-vault.md` after the table and its notes: an explicit statement that **nothing has been written yet**, a single question asking for approval, and a stop (FR-039)
- [X] T029 [US3] Add the approval semantics to `spectra/commands/kb-vault.md`: approval is affirmative; a question, a comment, a partial reaction or an ambiguous response is not approval, and where it is unclear nothing is written and the command says so (FR-042, research R4)
- [X] T030 [US3] Add the redirection surface to `spectra/commands/kb-vault.md` — the user may change a row's category, filename, category folder, action, and update target, or drop it; they may not send a **new** file outside the resolved artifact root (FR-040, FR-048a)
- [X] T031 [US3] Add the re-presentation rule to `spectra/commands/kb-vault.md`: any change produces the **full revised table** and a fresh question, and re-planning must not cost the user another absorption pass (FR-041)
- [X] T032 [US3] Add the subset rule to `spectra/commands/kb-vault.md`: approval of some rows writes only those rows, and the rest are named in the report (FR-043)

**Checkpoint**: the plan can be declined, corrected, partially approved, and re-presented, and nothing
is written except on an affirmative answer.

---

## Phase 6: User Story 4 — Land documents where the project keeps them, shaped the way it shapes them (Priority: P1)

**Goal**: continue the project's conventions rather than opening a second set.

**Independent Test**: run against a repository with an established folder, numbering scheme and document
shape. Produced files continue all three.

- [X] T033 [US4] Add the destination-assembly step to `spectra/commands/kb-vault.md`: `<artifact-root>/<category>/`, one category per folder, folder created on demand, all paths lowercase and project-relative (FR-044, FR-047)
- [X] T034 [US4] Add the numbering rule to `spectra/commands/kb-vault.md`: zero-padded three digits scoped to the folder, starting at `001`, one greater than the highest found across the destination and any superseded folder matched case-insensitively, computed **at write time** rather than plan time (FR-045, FR-046, research R9)
- [X] T035 [US4] Add the convention-precedence rule to `spectra/commands/kb-vault.md`: where the destination folder has an established naming convention — the reserved map's, or the project's own — it wins over the `NNN-` default (FR-045)
- [X] T036 [US4] Add the house-shape reporting rule to `spectra/commands/kb-vault.md`: where the project's existing documents of a category differ in shape from the resolved template, report the difference and offer the override path; never silently deviate from the resolved template (FR-056)
- [X] T037 [US4] Add the template-reporting rule to `spectra/commands/kb-vault.md`: name the resolved template's **full path** for each produced document, phrased so the literal `template you used` appears — `test_each_command_reports_the_template_it_used` asserts it (FR-057)
- [X] T038 [US4] Add the index step to `spectra/commands/kb-vault.md` per [contracts/index-contract.md](./contracts/index-contract.md): maintain `<artifact-root>/<category>/README.md` only for folders the command owns, never introduce one into a reserved-map folder, update rather than replace an index the project already keeps, and rebuild rows from the documents present (FR-049, research R8)

**Checkpoint**: a project's declared root, folder layout, numbering, conventions and template override
are all honoured, and every divergence is reported rather than absorbed.

---

## Phase 7: User Story 5 — Absorb a diagram, or fail loudly on a format that cannot be read (Priority: P1)

**Goal**: nothing invented, and every gap visible.

**Independent Test**: supply one readable document and one unreadable file. The readable one produces a
document, the unreadable one produces none, and the report names it as skipped.

- [X] T039 [US5] Add the diagram-transcription rule to `spectra/commands/kb-vault.md`: carry what is legibly present into prose, a table or diagram-as-code, asserting no structure, label or relationship that is not visible (FR-014)
- [X] T040 [US5] Add the untranscribable-diagram rule to `spectra/commands/kb-vault.md`: say so in the document and in the report, naming the source, rather than leaving a broken reference or a section that implies a picture is present (FR-019a)
- [X] T041 [US5] Add the unreadable-source handling to `spectra/commands/kb-vault.md`: name the file, state the failure, ask for the content, plan **no row** from it, and continue with the remaining sources (FR-011)
- [X] T042 [US5] Add the no-originals rule to `spectra/commands/kb-vault.md`: supplied PDFs, Word documents and images are never copied into the repository, and no produced document links to an asset the command did not write or to a path outside the repository (FR-019)

**Checkpoint**: a diagram is transcribed or declared, an unreadable file is named rather than invented
from, and no original lands in the repository.

---

## Phase 8: User Story 6 — Dictate knowledge without attaching anything (Priority: P2)

**Goal**: a paragraph is enough to start, and a bare instruction is not.

**Independent Test**: run with an argument and no attachments. A document is planned from the argument
alone.

- [X] T043 [US6] Add the argument-handling rule to `spectra/commands/kb-vault.md`: the argument is steering for the attachments, and a source in its own right where it carries knowledge (FR-008)
- [X] T044 [US6] Add the argument-only rule to `spectra/commands/kb-vault.md`: with no attachments the argument is the **only** knowledge source, and the repository is read for placement, shape, numbering and duplicate detection only — never mined for documentation content (FR-009)
- [X] T045 [US6] Add the nothing-to-absorb refusal to `spectra/commands/kb-vault.md`: an argument that instructs but carries no knowledge, or no input at all, is answered by asking for source material and stopping — never by synthesising documentation from the codebase (FR-007, FR-009a)

**Checkpoint**: dictated knowledge produces a document; "document the architecture" produces a request
for material.

---

## Phase 9: User Story 7 — Leave the commit to the human (Priority: P2)

**Goal**: the run ends with a report and an uncommitted working tree.

**Independent Test**: complete an approved run. Produced files are present and untracked or modified;
no new commit exists.

- [X] T046 [US7] Add the completion report to `spectra/commands/kb-vault.md` carrying all eight elements from [contracts/command-interface.md](./contracts/command-interface.md) — files created and updated, template path per document, redactions by kind, skipped sources, declined rows, unresolved conflicts, partial-write detail, and the uncommitted-changes statement (FR-064)
- [X] T047 [US7] Add the commit handoff to `spectra/commands/kb-vault.md`: state that the changes are uncommitted and that the user may commit once satisfied, and restate that the command itself never stages, commits, branches, pushes, tags or opens a pull request (FR-060, FR-065)
- [X] T048 [US7] Add the partial-outcome rules to `spectra/commands/kb-vault.md`: where some writes succeeded and others failed, state exactly which; where a written filename differs from the planned one because the sequence moved, say so (FR-066, research R9)

**Checkpoint**: all seven stories are independently exercisable from the command file.

---

## Phase 10: Publishing Surface (Principle V)

**Purpose**: what a consumer actually installs. Different files, so genuinely parallel — except the
three edits to `extension.yml`, which are sequential with each other.

- [X] T049 Add the `speckit.spectra.kb-vault` entry to `provides.commands` in `spectra/extension.yml` with `name`, `file` and `description` per [contracts/command-interface.md](./contracts/command-interface.md) (FR-002)
- [X] T050 Add the `kb-document-template` entry to `provides.templates` in `spectra/extension.yml` with `name`, `file` and `description` (FR-051)
- [X] T051 Bump `extension.version` in `spectra/extension.yml` from `1.15.0` to `1.16.0` (FR-067, Principle VI)
- [X] T052 [P] Add the `1.16.0` entry to `spectra/CHANGELOG.md` describing the added command and template (FR-067)
- [X] T053 [P] Add the `kb-vault` entry to `agents-list.json`, **inserted inside the existing `foundation` block after `domain-analyzer`** — appending at the end fails `test_agents_are_contiguous_by_phase_in_declared_phase_order` (FR-004, research R1)
- [X] T054 [P] Update the `spectra` entry in `catalog.json`: `version` to `1.16.0`, `provides.commands` from 10 to 11, and add the tags this agent introduces (FR-068)
- [X] T055 [P] Add the hand-authored command card for `speckit.spectra.kb-vault` to `docs/index.html`, in the style of the existing cards — name, description, example invocation (FR-069)
- [X] T056 Run `python tools/generate_agent_docs.py` to rewrite the generated regions in `README.md`, `AGENTS_LIST.md` and `spectra/README.md` — never hand-edit them (FR-069)
- [X] T057 Hand-author the per-agent prose block for `kb-vault` in `README.md` and `AGENTS_LIST.md`, anchored by `<!-- SPECTRA:AGENT id=kb-vault -->`; `--check` fails without it (FR-069)
- [X] T058 Run `python tools/build_package.py` to rebuild `docs/packages/spectra.zip` with a single top-level `spectra/` folder (FR-068)

**Checkpoint**: a consumer running `spectra install` would get the command, and every published surface
agrees with the manifest.

---

## Phase 11: Validation

**Purpose**: the guards. Tasks within a file are sequential; different files are parallel.

- [X] T059 Create `tests/test_kb_vault_flow.py` asserting manifest registration — the command is in `provides.commands` with the right file, and `kb-document-template` is in `provides.templates` with the right file — on the pattern of `tests/test_defect_rca_flow.py`
- [X] T060 Add gate assertions to `tests/test_kb_vault_flow.py`: the command states that nothing has been written before approval, requires an affirmative answer, re-presents the full table on any change, and supports subset approval (FR-039 – FR-043)
- [X] T061 Add negative-invariant assertions to `tests/test_kb_vault_flow.py`: no commit or stage, no move or delete, no credential, no copied original, no codebase mining as a content source, and supplied text treated as data (FR-009, FR-012, FR-018, FR-019, FR-060, FR-061)
- [X] T062 Add classification assertions to `tests/test_kb_vault_flow.py`: the reserved-map folders are named, category derivation is from content not filename, and the index is excluded from reserved-map folders (FR-028, FR-030, FR-049)
- [X] T063 Add the `MULTI_CATEGORY` registry to `tests/test_doc_output_paths.py` mapping `"kb-vault.md"` to `"<artifact-root>/<category>/"`, and make `DOCUMENT_COMMANDS` the union of `CANONICAL` and it, with a comment stating why the split exists (research R6)
- [X] T064 Add a class to `tests/test_doc_output_paths.py` asserting the deliberate absence from `CANONICAL` **with its reason**, that the command ships, and that it names the `<artifact-root>/<category>/` form and the reserved-map folders — on the pattern of `TheOutputIsNotAnArtifactRootDocument`
- [X] T065 [P] Add `"kb-vault.md": "kb-document-template"` to `DOCUMENT_COMMANDS` in `tests/test_document_templates.py`, which enrols the command in the four-layer and inline-skeleton-parity assertions
- [X] T066 [P] Update the census expectations in `tests/test_roster_data.py` for the new agent, and confirm the `foundation` block stays contiguous
- [X] T067 Run `python -m unittest discover -s tests` and fix every failure; the baseline before this feature was 1056 passing
- [X] T068 Run `python tools/generate_agent_docs.py --check`; expect 51 agents and 11 prose blocks, up from 50 and 10
- [X] T069 Execute [quickstart.md](./quickstart.md) Part 2 passes 1–7 in a throwaway Spec Kit project installed with `specify extension add --dev`, observing the gate, the update path, the decline, the project's own conventions, the unreadable source and the negative invariants
  - **Mechanically verified.** A throwaway project was created with `specify init`, the working copy
    installed with `specify extension add --dev`, and the translation verified: the command surfaces as
    `.claude/skills/speckit-spectra-kb-vault`, keeps `$ARGUMENTS`, and carries all six asserted literals.
    Against a fixture project the resolution mechanics were confirmed end to end — a case-insensitively
    declared `Artifact root: documents/` parses, `mkdocs.yml` is found as a publication signal, an
    existing `004-` document yields `005`, a legacy `Docs/ADR/` folder is readable case-insensitively,
    and both template-stack layers resolve to real paths.
  - **Deferred to real use**: the behavioural passes — observing the agent stop at the gate, decline,
    update in place, correct a wrong match, or transcribe a diagram. Those require an agent session
    running inside the throwaway project with documents attached, which cannot be driven from the
    Spectra repository. Accepted by the maintainer on 2026-09-11: the rules they would exercise are
    each asserted as prose invariants in `tests/test_kb_vault_flow.py`, and the first real run is the
    cheaper place to observe them.
- [X] T070 Execute [quickstart.md](./quickstart.md) Part 2 pass 8 — install `docs/packages/spectra.zip` into a second throwaway project and repeat pass 1 from the published artifact

**Checkpoint**: the rules are asserted in the suite, and an agent has been observed following them in
both the working copy and the shipped zip.

---

## Phase 12: Publish (Constitution Development Workflow step 6)

- [X] T071 Verify the CLI channel is untouched: root `VERSION` unchanged, no git tag created, no GitHub Release drafted (FR-070, Principle VI)
- [X] T072 Commit the `spectra/` folder, `specs/023-kb-vault-agent/`, `agents-list.json`, `catalog.json`, `docs/`, `README.md` and `AGENTS_LIST.md` on branch `023-kb-vault-agent`
- [X] T073 Open the pull request for `023-kb-vault-agent` and merge to `main` once the `catalog` job and the test suite in `.github/workflows/ci.yml` pass; the catalog and package are live immediately at their raw links

---

## Dependencies & Execution Order

### Phase dependencies

- **Phase 1 (Setup)**: no dependencies.
- **Phase 2 (Foundational)**: depends on Phase 1. **Blocks every user story** — T005's root resolution,
  T008's template resolution and T014's write-scope boundary are read by every later step.
- **Phases 3–9 (User Stories)**: depend on Phase 2. Within the command file they are sequential in
  practice; the story boundaries mark independently testable increments, not independently editable
  files.
- **Phase 10 (Publishing)**: depends on the command file and template being complete (T001–T048, T009).
- **Phase 11 (Validation)**: depends on Phase 10 — the registry tasks assert the manifest entries.
- **Phase 12 (Publish)**: depends on Phase 11 passing.

### Story dependencies

- **US1 (P1)** — the MVP. Depends only on Phase 2.
- **US2 (P1)** — depends on US1's classification step (T016) to know what category to match within.
- **US3 (P1)** — depends on US1's table (T019); the gate follows what it renders.
- **US4 (P1)** — depends on US1's placement construction (T018) and Phase 2's root resolution (T005).
- **US5 (P1)** — depends on Phase 2's degradation step (T011); independent of US2–US4.
- **US6 (P2)** — depends on Phase 2 only. The most independently deliverable of the seven.
- **US7 (P2)** — depends on every story that contributes a line to the report, so it goes last.

### Within each phase

- The command file is one file. Tasks that edit it are sequential, in the order given.
- A task that adds a literal string the suite asserts (T005, T010) must not be reworded by a later task.
- T009 and T010 are a pair: the shipped template and the inline skeleton must declare the same H2
  sections in the same order.

### Parallel opportunities

- **Phase 10**: T052, T053, T054 and T055 touch four different files and can run together. T049 → T050
  → T051 are sequential (all `extension.yml`). T056 must follow T053. T057 must follow T056. T058 must
  follow T049–T051.
- **Phase 11**: T065 and T066 are different files and can run together, and alongside T063 → T064
  (same file, sequential) and T059 → T062 (same file, sequential).
- Nothing in Phases 1–9 is parallel. Marking it so would produce conflicting edits to one Markdown file.

---

## Parallel Example: Phase 10

```bash
# After T049–T051 land the three extension.yml edits, these four are independent:
Task: "Add the 1.16.0 entry to spectra/CHANGELOG.md"
Task: "Add the kb-vault entry to agents-list.json inside the foundation block"
Task: "Update the spectra entry in catalog.json — version, provides.commands 11, tags"
Task: "Add the command card for speckit.spectra.kb-vault to docs/index.html"

# Then, in order:
python tools/generate_agent_docs.py      # T056 — needs T053
# hand-author the prose block            # T057 — needs T056
python tools/build_package.py            # T058 — needs T049–T051
```

---

## Implementation Strategy

### MVP (User Story 1 only)

1. Phase 1 — Setup (T001–T004)
2. Phase 2 — Foundational (T005–T014) — **blocking**
3. Phase 3 — User Story 1 (T015–T022)
4. **STOP and VALIDATE**: install the working copy into a throwaway project, attach two readable
   documents, and confirm a plan table is produced and approved documents land with provenance.

At that point the agent does the thing it was asked for. Everything after it is making that safe on a
repository that already has documentation.

### Incremental delivery

1. Setup + Foundational → the machinery exists
2. + US1 → attachments become documents (**MVP**)
3. + US2 → a second run updates rather than duplicates
4. + US3 → the gate is steerable and declining is free
5. + US4 → the project's own conventions are continued
6. + US5 → diagrams and unreadable formats fail honestly
7. + US6 → dictated knowledge works with nothing attached
8. + US7 → the report closes the loop and hands the commit back
9. Publishing + Validation + Publish → a consumer can install it

### The order that is not negotiable

- **T005 before anything that names a path.** Every destination hangs off the resolved root.
- **T009 with T010.** Split them across sessions and the parity assertion fails on a change neither
  task looks wrong in isolation.
- **T014 before Phase 3.** The write-scope boundary is enforced at plan construction, so the step that
  constructs placements (T018) has to already know the rule.
- **T053 before T056.** `generate_agent_docs.py` reads `agents-list.json`; running it first regenerates
  the old roster.
- **T067 and T068 before T069.** A manual pass against a command that fails its own suite tests nothing.

---

## Notes

- 73 tasks. 7 user stories. 5 parallel opportunities, all in Phases 10 and 11.
- `[P]` tasks are different files with no dependency on an incomplete task.
- The runtime deliverable is two Markdown files. No script, no binary, no post-install hook.
- Commit after each phase rather than each task; the command file is one artifact and a half-written
  section is not a useful commit.
- Stop at any checkpoint to validate the story independently.
- Avoid: rewording a literal the suite asserts, editing a generated region by hand, appending the
  roster entry outside its phase block, and bumping the root `VERSION`.
