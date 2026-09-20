# Implementation Plan: KB Vault — Knowledge Ingestion Agent

**Branch**: `023-kb-vault-agent` | **Date**: 2026-09-11 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/023-kb-vault-agent/spec.md`

## Summary

An eleventh Spectra command, `speckit.spectra.kb-vault`, and the **seventh document agent** — after
`adr`, `brd`, `impact`, `test-strategy`, `test-plan`, and `defect-rca`. It takes material the user
supplies — attachments the host agent can read, or knowledge dictated in the argument — absorbs it,
learns how this project already keeps documentation, classifies each source into a category, shows the
user a table of exactly what it intends to write and where, waits for approval, and then writes
Markdown into `<artifact-root>/<category>/`. It commits nothing.

Six properties shape every decision below.

**It is the first Spectra agent whose knowledge comes from outside the repository.** Every document
agent so far derives its content from the project: `impact` reasons from the code, `defect-rca` from
the code and the commits, `adr` from a conversation about the project. This one derives content from
attachments and reads the repository only to decide *where the document lands and what shape it takes*.
The clarification session made that boundary hard: FR-009 forbids mining the codebase for content even
when the user asks in the abstract. Without that line the command drifts into being a documentation
generator, which is the planned `documentation-quality` agent's territory and a different feature.

**It is the first with no single canonical output folder.** `adr` writes `docs/adr/`, `brd` writes
`docs/brd/`, `defect-rca` writes `docs/defect-rca/`. kb-vault's category set is open-ended by
requirement (FR-029), so its destination is computed per document: `<artifact-root>/<category>/`. That
is still Principle VII — one artifact type per folder — but it breaks the *shape* of
`tests/test_doc_output_paths.py`, whose `CANONICAL` dict maps one command to one folder. Research
decision **R6** resolves that without weakening the assertions the dict drives.

**It is the first that resolves a template name it does not know at authoring time.** Every other
document command resolves exactly one name. kb-vault resolves a name derived from the category, so a
project can supply `.specify/templates/overrides/ux-ui-standards-template.md` and have it apply to a
category Spectra never anticipated — with `kb-document-template` as the shipped generic fallback, and
a reserved map that routes a category another agent already owns to *that* agent's template
(**R3**, **R2**).

**It is the first with a hard approval gate before any write.** Every other document command writes as
its final act; the user sees the result. This one must show a plan and stop — FR-039, and the entire
point of User Story 3. The gate is not a nicety: it is the only thing standing between a
misclassification and a file in someone's repository, and it is what makes the write scope safe enough
to aim at a project that already has documentation.

**Its most consequential rule is a negative one.** FR-015 forbids inventing content, and FR-011
forbids inferring a document from its filename. An ingestion agent that fills a template section
because the template has the section produces documentation indistinguishable from the real thing once
committed, and worse than none. Every "cannot read it / cannot transcribe it / no source for this
section" path in the command exists to make that failure loud instead of silent.

**It writes N files, not one, and commits none of them.** Every prior document command writes one file,
or two counting an index. This one writes a set, some of which are updates to files it did not create
(FR-048, the one Complexity Tracking entry below). Then it stops: no stage, no commit, no branch, no
push, no pull request (FR-060).

The command file is the deliverable. No script and no binary ships: classification, root resolution,
duplicate detection, numbering, template resolution, the plan table, and the approval gate are all
prompt instructions, because that is the only form that survives Principle III and the Markdown-only
supply chain.

## Technical Context

**Language/Version**: Markdown command prompt in Spec Kit's generic format; Python 3.9+ (standard
library only) for this repository's own tools and tests

**Primary Dependencies**: Spec Kit `>=0.11.0`. No new tool dependency — `git` and `gh` stay optional at
the extension level and this command uses neither. Reading PDF, Word and image attachments is a
capability of the **host agent's harness**, inherited rather than integrated, on the precedent
`speckit.spectra.defect-rca` set for JIRA retrieval

**Storage**: `<artifact-root>/<category>/` in the target project — one Markdown file per planned
document, plus a `README.md` index in each category folder the command itself owns. Nothing under
`.specify/`, nothing under `specs/`, no cache, no cross-run state. The written documents *are* the
state: the next run's duplicate detection reads what earlier runs wrote

**Testing**: `python3 -m unittest discover -s tests` (**1056 passing at baseline**);
`python3 tools/generate_agent_docs.py --check` (**50 agents, 10 prose blocks at baseline**); a new
`tests/test_kb_vault_flow.py` (which also asserts manifest registration, as `test_impact_flow.py` and
`test_defect_rca_flow.py` do for theirs); three existing modules gain this command
(`tests/test_doc_output_paths.py` — via a **new `MULTI_CATEGORY` registry** rather than a `CANONICAL`
entry, per R6 — `tests/test_document_templates.py`, `tests/test_roster_data.py`). Manifest ↔ catalog ↔
zip agreement is enforced by the `catalog` job in `.github/workflows/ci.yml`, not by the unittest
suite; the manual zip-install pass in `test/README.md` covers the published artifact

**Target Platform**: every coding agent and OS Spec Kit supports. Classification, root resolution,
duplicate detection and numbering are prompt-expressed, so nothing depends on a shell flavour or a
named search tool. Which *attachment formats* work varies by host agent — that variance is surfaced to
the user per file (FR-011) rather than hidden

**Project Type**: Spec Kit extension command — a prompt file under `spectra/commands/`, a registered
template under `spectra/templates/`, plus the publishing surface Principle V requires

**Performance Goals**: not latency-bound. Two costs are explicitly bounded: the repository survey
(FR-025) reads the documentation tree's structure and only the candidate documents duplicate detection
actually needs, never the whole tree; and the command never reads source code for content, because
FR-009 forbids using it as one. A supplied set too large to absorb in one pass is reported as
partially covered rather than silently truncated

**Constraints**: Markdown only, no scripts or binaries; agent-agnostic `$ARGUMENTS`; no credential ever
requested, accepted or stored (FR-012); no network request at all — the command reads what it is given
and what is on disk; nothing written before approval (FR-039); new files only under the resolved
artifact root (FR-048a); no supplied original copied into the repository (FR-019); no source code,
build configuration, `.specify/` or `specs/` modified (FR-062); no stage, commit, branch, push, tag or
pull request (FR-060); no existing document moved, renamed or deleted (FR-061); no secret reproduced
(FR-017); instructions found inside a supplied document treated as content, never obeyed (FR-018)

**Scale/Scope**: 1 new command file; 1 new shipped template; 2 manifest entries; 1 new roster entry; 1
catalog entry; 1 changelog entry; 1 rebuilt zip; ~4 documentation surfaces including a hand-authored
prose block; 1 new test module plus four census/registry updates

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | This spec/plan/tasks set on branch `023-kb-vault-agent`; the spec carries no unresolved markers and its checklist passed 16/16 after one clarification round. |
| II. A Single Self-Contained Extension | ✅ | One new file under the existing `spectra/commands/`, one under `spectra/templates/`. No new extension folder, no dependency on another extension. Adopting the `adr` folder and template for an ADR-shaped source (R2) is reuse *inside* the one extension, not a dependency between two. |
| III. Agent-Agnostic Commands | ✅ | Text only, `$ARGUMENTS` for the argument. No named search tool, no shell flavour, no agent-specific syntax. Attachment reading is described as a capability the host may or may not have, with a degradation path (FR-011), never as an invocation. |
| IV. Context-Aware by Default | ✅ | FR-020 – FR-027 read the constitution, the artifact root, the project's folder layout, its numbering, its document shapes, its templates and its superseded folders — and every one of them changes the output. A kb-vault that ignored the project would write a generic folder tree beside the existing one, which is the exact defect Principle IV names. |
| V. Catalog and Package in Sync | ✅ | Manifest, roster, catalog, changelog, zip, landing page, generated regions and a new hand-authored prose block all move in the same change (FR-067 – FR-069). |
| VI. Two Independently-Versioned Channels | ✅ | Extension channel only: 1.15.0 → 1.16.0. `VERSION` untouched, no tag, no Release (FR-070). |
| VII. Documents Under One Declared Root | ⚠️ | **Engaged in full, with one justified deviation.** Declared root honoured, publication check before defaulting, non-publishing option where the choice cannot be obtained, `NNN-` sequence scoped to each folder, superseded folders read and never touched (FR-021 – FR-023, FR-027, FR-044 – FR-047). The deviation is FR-048's update carve-out — see Complexity Tracking. |
| VIII. Shaped by Overridable Templates | ✅ | **Engaged in full, and extended.** New registered `kb-document-template`, resolved through the four-layer stack, inline skeleton last, resolved path reported per document (FR-050 – FR-057). The extension is that the *name* resolved is category-derived rather than fixed, which widens the override surface without changing the stack (R3). |

**Amendment classification**: none required. This plan proposes no change to Spectra's own
constitution.

**Extension version classification**: MINOR — 1.15.0 → 1.16.0. A command is added; none is renamed or
removed, and no existing command's behaviour changes. `catalog.json` `provides.commands` goes 10 → 11
and `provides.templates` gains a ninth entry.

### What makes this agent different, and why each difference is contained

Four firsts are listed in the Summary. Three of them are contained by rules that already exist; the
fourth needs an argument.

**Knowledge from outside the repository** is contained by FR-015's traceability rule and FR-009's
prohibition on codebase mining. Together they mean every sentence in a produced document has a named
origin, and the origins are a closed set: a supplied source, or the repository's own structure. There
is no third category from which content may appear.

**No single canonical folder** is contained by the observation that Principle VII's unit is the
*artifact type*, not the command. "One artifact type per folder" is satisfied by a command writing to
five folders in a run, as long as each folder holds one type. What the principle forbids — an agent
inventing a top-level directory of its own — kb-vault never does: every destination is a subfolder of
the one declared root.

**A category-derived template name** is contained by the resolution stack being unchanged. Principle
VIII fixes the *order* of the layers and forbids hard-coding a single path; it does not require the
name be constant. A project override for a category is resolved by exactly the mechanism an override
for `adr-template` is.

**Writing outside the artifact root** is the one that needs an argument, and it is in Complexity
Tracking below.

### The index, again: a directory listing, not a second artifact type

FR-049 puts a `README.md` in each category folder the command owns. `specs/022-defect-rca-agent/plan.md`
argued this at length and the argument transfers unchanged: an index is navigation over one artifact
type, rebuilt from the files present, carrying no content of its own — it is a directory listing that
happens to be Markdown, not a second artifact sharing the folder. Two things are added here because
kb-vault's situation differs from `defect-rca`'s. It must **not** introduce an index into a folder
another Spectra agent owns (`adr/`, `brd/`, `impact-analysis/`, `test-strategy/`, `defect-rca/`), because
those agents' conventions are not kb-vault's to change. And where the project already keeps an index in
a folder, kb-vault updates it rather than replacing it, because a hand-maintained index may carry
columns a rebuild would destroy.

### The approval gate, and why it is expressed as a stop rather than a question

`adr` asks clarifying questions and continues. `defect-rca` asks only what the repository cannot
answer. kb-vault's gate is different in kind: it is not gathering information, it is handing over a
decision. The prompt must therefore make the stop unambiguous — present the table, state that nothing
has been written, and wait. The failure mode to design against is the agent treating a user's
*comment* on the plan as approval of it, which is why FR-041 requires the full revised plan to be
re-presented after any change and FR-042 makes ambiguity a refusal rather than a default-yes. This
costs a round trip on every run and is worth it: the alternative is that the first time the
classification is wrong, the user finds out from `git status`.

## Project Structure

### Documentation (this feature)

```text
specs/023-kb-vault-agent/
├── plan.md                      # This file
├── research.md                  # Phase 0 output
├── data-model.md                # Phase 1 output
├── quickstart.md                # Phase 1 output
├── contracts/                   # Phase 1 output
│   ├── command-interface.md     # registration, input, modes, write scope, report
│   ├── plan-table.md            # the approval gate's contract — columns, rows, re-presentation
│   ├── classification.md        # category derivation, the reserved map, duplicate matching
│   ├── document-contract.md     # where a document goes, what it is called, what it contains
│   └── index-contract.md        # the per-category README index
├── spec.md                      # Input
├── checklists/requirements.md
└── tasks.md                     # Phase 2 output (/speckit-tasks — NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
spectra/
├── commands/
│   └── kb-vault.md                      # NEW — the deliverable
├── templates/
│   └── kb-document-template.md          # NEW — shipped generic fallback (Principle VIII)
├── extension.yml                        # + commands[] entry, + templates[] entry, 1.15.0 → 1.16.0
├── CHANGELOG.md                         # + 1.16.0 entry
└── README.md                            # generated `spectra-readme-commands` region

agents-list.json                         # NEW entry, inserted in the `foundation` block
catalog.json                             # version, provides.commands 10 → 11, tags
docs/
├── index.html                           # + hand-authored command card
└── packages/spectra.zip                 # rebuilt by tools/build_package.py
README.md                                # generated `readme-agents-table` region + prose block
AGENTS_LIST.md                           # generated roster regions + prose block

tests/
├── test_kb_vault_flow.py                # NEW — behaviour + manifest registration
├── test_doc_output_paths.py             # + MULTI_CATEGORY registry (R6)
├── test_document_templates.py           # + kb-vault.md → kb-document-template
└── test_roster_data.py                  # census counts
```

**Structure Decision**: the shipped extension is unchanged in shape — one command file and one template
file added to the folders that already hold ten and eight of them. The only structural novelty is in
`tests/test_doc_output_paths.py`, which gains a second registry because this command's output folder is
computed rather than fixed (R6). Everything else is an additional row in an existing list.

## Complexity Tracking

> Filled because the Constitution Check above flags Principle VII as ⚠️.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| **FR-048: an update is written where the existing document already lives, which may be outside the resolved artifact root.** Principle VII says a document-producing command "MUST NOT write anywhere else" than `<artifact-root>/<artifact>/`. | The spec's central requirement is "update it, don't add a new file of the same nature" (FR-033, User Story 2). On any project whose documentation predates Spectra — which is every project kb-vault is useful on — the document to update is in that project's own tree, not in Spectra's root. A rule that forbids writing there does not prevent the write; it converts every update into a duplicate, in a different folder, saying something different. That is the precise harm Principle VII exists to prevent, arrived at by obeying its letter. | **Strictly bounded** (the user's option C at clarification) writes a second copy under the artifact root and leaves the original stale. Within a month the project has two UX/UI standards documents disagreeing with each other and no rule for which is current. **Move-then-update** — relocate the existing document into the root, then update it — is forbidden outright by Principle VII's own "MUST NOT move, rename, modify, or delete anything there", and would rewrite the project's documentation layout as a side effect of an ingestion run nobody asked to reorganise anything. |

Three properties keep the deviation narrow, and each is a testable requirement rather than an
intention:

1. **New files are never affected.** FR-048a bounds every *create* to `<artifact-root>/<category>/`. The
   carve-out applies only to a row that updates a file that already exists.
2. **The user sees it before it happens.** The out-of-root path appears in the plan table's location
   column (FR-037) and the row is marked as an update (FR-035), so the deviation is approved explicitly
   on the run where it occurs.
3. **It cannot be used as a back door.** FR-048b forbids honouring a user's request to write a *new*
   file outside the root, and requires the command to offer the two legitimate routes instead — the
   `Artifact root:` declaration, or a `git mv` the user runs. Without that clause the carve-out would
   be "anywhere, if you phrase it as an update".

## Phase 0 — Research

**Output**: [research.md](./research.md) — eleven decisions (R1 – R11), each with rationale and the
alternatives rejected. Summarised:

- **R1** Command name, id and roster placement.
- **R2** How a category is derived, and the reserved map for folders other agents own.
- **R3** Template resolution when the template name is not known at authoring time.
- **R4** Expressing the approval gate agent-agnostically.
- **R5** Duplicate detection without depending on a search tool.
- **R6** The `CANONICAL` registry problem in `tests/test_doc_output_paths.py`.
- **R7** Reading attachments through the host harness, and degrading per file.
- **R8** Index scope: which folders get one and which must not.
- **R9** Sequence numbering across create, update and collision.
- **R10** Treating supplied documents as data, never as instructions.
- **R11** Where the write-scope boundary is enforced in the command's own flow.

No `NEEDS CLARIFICATION` remained in the Technical Context above; the three genuine unknowns were
resolved with the user before this plan began and are recorded in the spec's Clarifications section.

## Phase 1 — Design & Contracts

**Outputs**: [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md).

`data-model.md` carries the six entities the spec names, with their fields, their lifecycle through a
run (absorbed → classified → planned → approved → written → reported), and the validation rules the
command enforces on each.

`contracts/` carries five contracts. `command-interface.md` is the registration, input, mode and write
scope contract — what the manifest says and what a run may touch. `plan-table.md` pins the approval
gate: the exact columns, what each holds, what appears beneath the table, and the re-presentation rule.
`classification.md` pins category derivation, the reserved map, and the duplicate-match axes.
`document-contract.md` pins where a document lands, what it is called, what provenance it carries, and
the rejection cases. `index-contract.md` pins the per-category index and the two folders-it-must-not-touch
rules.

`quickstart.md` is the validation guide: the automated gate in this repository, then a manual pass in a
throwaway Spec Kit project covering a first run on an empty project, an update run, a project with its
own conventions, an unreadable attachment, a declined approval, and the negative invariants.

## Post-Design Constitution Re-Check

Re-evaluated after the Phase 1 artifacts were written. No status changed.

- **II, III, V, VI** are unaffected by the design: the contracts add no file outside `spectra/`, name no
  agent's syntax, change no channel's version policy, and list the same publishing surface the gate
  already required.
- **IV** strengthened. `classification.md` makes the repository survey load-bearing rather than
  advisory — the reserved map, the numbering and the duplicate match all read the project, and a run
  against a project with existing documentation produces materially different output from a run against
  an empty one.
- **VII** unchanged at ⚠️, with the same single justified deviation. The Phase 1 design added no new
  write location: `document-contract.md` enumerates exactly two — `<artifact-root>/<category>/<name>.md`
  for a create, and the existing path for an update — and `index-contract.md` adds the index only in
  folders the command owns.
- **VIII** unchanged at ✅. `document-contract.md` fixes the resolution order as the constitution states
  it and requires the resolved path in the report; the category-derived name changes which file is
  looked for at each layer, not the layers or their order.

The one deviation remains justified, remains bounded to updates, and remains visible to the user before
it occurs.
