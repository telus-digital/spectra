# Implementation Plan: An Engineering Methodology Agent That Feeds the Constitution

**Branch**: `035-engineering-methodology-agent` | **Date**: 2026-10-24 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/035-engineering-methodology-agent/spec.md`

## Summary

Add `speckit.spectra.methodology`, a foundation-phase agent built on the shape `domain-analyzer` already uses.
It states mode (brownfield/greenfield, from three signals) and goal (create/update the constitution) first;
reads the repository; works nine fixed lenses; asks ten fixed questions one per turn (≥4 options, one
recommended, one Skip); then writes `<artifact-root>/ENGINEERING_METHODOLOGY.md` once. That file is an
onboarding document modelled on a team's hand-written engineering methodology, and it ends with a Constitution input section and a
Decisions and sources section. The agent then hands off one `/speckit-constitution` line and names the sibling
agents not yet run.

SDD is the fixed base. Overlays (TDD, BDD/ATDD, DDD, contract-first, ADR-driven) enter the constitution only as
obligations tied to spec-kit phases, with `tasks.md` evidence for obligations met during implementation.

Three existing agents change at their edges so that no constitution clause has two sources:
- `domain-analyzer` drops its Delivery & workflow lens (7 → 6 lenses, 8 → 7 questions).
- `deployment-strategy` stops proposing the branching model (R3).
- `kb-vault` routes an absorbed methodology document to the new singleton.

`review-pr` reads the new document as a T2 standard, citing accepted guardrails only.

## Technical Context

**Language/Version**: Markdown command prompts and templates; Python 3.9+ for tests and tooling

**Primary Dependencies**: none. Standard library only (zero-dependency rule covers the whole repository)

**Storage**: one Markdown file per project, `<artifact-root>/ENGINEERING_METHODOLOGY.md`, with YAML front matter

**Testing**: `python3 -m unittest discover -s tests`; `python3 tools/generate_agent_docs.py --check`;
`python3 tools/build_package.py`; `python3 tools/ship.py --dry-run`

**Target Platform**: any Spec Kit agent, slash-command or skills mode

**Project Type**: Spec Kit extension (Markdown commands), catalog channel only

**Performance Goals**: a run is bounded by its round: ten questions and at most five candidates per lens, so at
most 45 candidates plus one overlay table are ever presented

**Constraints**: Markdown only, no scripts in the package; agent-agnostic (no agent's question tool named);
writes one file, after the round; never writes the constitution or a sibling document; no network; reads
git history read-only (`git log`, `git branch -a`)

**Scale/Scope**: one new command, one new template, one new test module. Edge changes to four commands
(`domain-analyzer`, `deployment-strategy`, `kb-vault`, `review-pr`), one template (`domain-analysis-template`)
and their tests. Version sync across the published files. One MINOR constitution amendment

## Evidence

| Claim | How it was verified |
|---|---|
| Domain analyzer lens 7 proposes branching, review, commits, versioning, docs habits | `spectra/commands/domain-analyzer.md:192` |
| Domain analyzer's fixed count is pinned by tests | `tests/test_domain_analyzer_flow.py` `LENSES` (7) and `"question 4 of 8"`; `domain-analysis-template.md:73,89` |
| **Deployment strategy already decides the branching model and versioning scheme** | `spectra/commands/deployment-strategy.md:125`, lens *Release & versioning*: "the branching model, how a release is cut, the versioning scheme, the hotfix path" |
| **KB vault routes absorbed methodology to a series folder** | `spectra/commands/kb-vault.md:267,365` — example `docs/engineering-methodology/001-branching-and-release.md`; the reserved map (`:283–292`) has no methodology row |
| Review PR reads singletons as T2 and filters domain analysis to `accepted` | `spectra/commands/review-pr.md:273–284` |
| A new singleton must be named by constitution amendment | constitution Principle VII; enforced by `tests/test_doc_output_paths.py::test_the_constitution_names_every_singleton` |
| The extension is at 1.23.0 and the constitution at 1.12.0 | `spectra/extension.yml:6`; constitution Sync Impact Report |
| Roster has a `foundation` phase holding the sibling add-ons | `agents-list.json` phases and the `domain-analyzer`, `kb-vault` entries |
| The `--non-interactive` flag is the house convention | `spectra/commands/domain-analyzer.md:36,523` |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | Spec, clarify, and plan on `035-engineering-methodology-agent`; each phase is started by the user. The scope additions in R3–R5 are surfaced for the user's review, not silently absorbed (see Spec reconciliation) |
| II. Single Self-Contained Extension | ✅ | One command file and one template added under `spectra/`; no new top-level folder; no dependency on another extension |
| III. Agent-Agnostic Commands | ✅ | `speckit.spectra.methodology`, front-matter `description`, `$ARGUMENTS`, one `--non-interactive` flag; the round is described in prose |
| IV. Context-Aware by Default | ✅ | The command's core: mode detection, current practice cited per lens, constitution and sibling documents read first |
| V. Catalog and Package in Sync | ✅ | `extension.yml`, `catalog.json` (version, command count 13 → 14), `CHANGELOG.md`, `agents-list.json`, `docs/index.html`, regenerated listings, new prose blocks in `spectra/README.md` and `AGENTS_LIST.md`, rebuilt zip |
| VI. Two Versioned Channels | ✅ | Extension only, 1.23.0 → 1.24.0. Root `VERSION` untouched; no tag |
| VII. Documents Under One Declared Root | ✅ *after amendment* | A new singleton `<artifact-root>/ENGINEERING_METHODOLOGY.md`, with declared-root resolution, publication check, and non-publishing fallback. **A command MUST NOT declare itself a singleton**, so the constitution amendment (R10) lands in the same change, run by the user through `/speckit-constitution` |
| VIII. Overridable Templates | ✅ | `spectra/templates/engineering-methodology-template.md`, registered under `provides.templates`, resolved through the five-layer stack; the command reports the template used; the record and Constitution input formats stay command-owned |

**Gate result**: PASS, conditional on the Principle VII amendment being part of the change. Tasks must sequence it
before the singleton test is updated, since `test_the_constitution_names_every_singleton` fails until then.

**Amendment classification**: MINOR, 1.12.0 → 1.13.0. A singleton is added to Principle VII's named list; no rule
changes.

**Extension version classification**: MINOR, 1.23.0 → 1.24.0. One command added. The four edge changes narrow
or extend existing behaviour; none renames or removes a command, argument, flag, or output path.

**Post-design re-check**: unchanged, all ✅. The Phase 1 contracts add no file beyond those listed under Source
Code below, and no dependency. **Re-checked after the remediation round on 2026-10-24**: Principle VII now holds
outright, with no second file in any path (R13), and Principle I holds because no task writes `spec.md`.

## Spec Reconciliation

Planning found ground the spec did not account for. Each item is decided in [research.md](./research.md).
**Accepted by the user on 2026-10-24, and folded into `spec.md` by the second clarify session**: FR-004 (lens 7),
FR-018, FR-019, SC-005, and User Story 3 scenarios 7–8 now state R3–R5. The spec and plan agree, so no task edits
`spec.md` (Principle I).

The `/speckit-analyze` remediations, also clarified into the spec, are reflected here:

| Finding | Resolution | Where |
|---|---|---|
| C1: `.proposed` file broke Principle VII | No second file. Without consent, and always when non-interactive, write nothing and show the document in the session | research R13, B35 |
| H2: overlays broke the five-per-lens cap | One candidate per overlay, its statement listing the phase obligations | research R7, data-model, B13 |
| H3: lens 8's levels exclude each other | Question 9 offers the three levels plus Skip; tools and secrets ride with the level | research R2, B11 |
| M2: lens 8's section | Additional Constraints | research R9 |
| M3: untestable source signal | More than 20 non-blank lines changed in more than one commit, or five such files when history has at most one commit (a squashed import counts) | research R6, B2 |
| L1 / L2 | Roster sentence fixed; a file `kb-vault` absorbed is read as evidence | research R1, R4 |

**Resolved (third clarify session, 2026-10-24).** FR-002's fallback now counts five qualifying files when the
history has at most one commit, so a squashed import with no CI has the source signal only and reads as mixed, as
User Story 4 scenario 3 expects. Carried into research R6, data-model.md, B2, and quickstart §3.

**Resolved (fourth clarify session, 2026-10-24).** Analyze M1: kb-vault's update path could overwrite the
agent's own file and drop its front matter. FR-019 now has kb-vault refer instead of updating when the file
carries `command: speckit.spectra.methodology`, and report the source as referred on. Carried into research R4,
B-edge E6, contracts/sibling-boundaries.md, and quickstart §3.

| # | Finding | Decision | Spec effect |
|---|---|---|---|
| R3 | `deployment-strategy` already owns the **branching model** and **versioning scheme** | Methodology owns the branching model, naming, lifecycle and merge strategy; deployment keeps release cut, **versioning scheme**, and the hotfix promotion path, and cites `ENGINEERING_METHODOLOGY.md` for the branching model | Lens 7 narrows to commit convention and changelog. Adds a `deployment-strategy` edge change alongside the domain-analyzer one |
| R4 | `kb-vault` sends an absorbed methodology to `<root>/engineering-methodology/NNN-…` | Add a reserved-map row routing it to `<root>/ENGINEERING_METHODOLOGY.md` with `engineering-methodology-template` | Adds a `kb-vault` edge change |
| R5 | FR-034 constrains readers, but no reader exists | `review-pr` adds the document as a T2 standard, accepted guardrails only, mirroring its domain-analysis rule | Adds a `review-pr` edge change |

## Project Structure

### Documentation (this feature)

```text
specs/035-engineering-methodology-agent/
├── spec.md
├── plan.md              # this file
├── research.md          # Phase 0: R1–R13
├── data-model.md        # Phase 1: mode, goal, lens, candidate, overlay, question, constitution input
├── contracts/
│   ├── methodology-behaviour.md     # numbered behaviours → FR → test
│   └── sibling-boundaries.md        # who owns what across the four constitution-feeding agents
├── quickstart.md        # Phase 1: automated checks, then manual runs
├── checklists/requirements.md
└── tasks.md             # /speckit-tasks, not this command
```

### Source Code (repository root)

```text
spectra/
├── commands/methodology.md                        # NEW
├── templates/engineering-methodology-template.md   # NEW
├── commands/domain-analyzer.md                     # lens 7 removed, 7 questions, hands on to methodology
├── templates/domain-analysis-template.md           # Delivery & workflow section removed
├── commands/deployment-strategy.md                 # Release & versioning stops proposing the branching model
├── commands/kb-vault.md                            # reserved-map row; refer, never update, the agent's own file
├── commands/review-pr.md                           # T2 row + accepted-only rule
├── extension.yml                                   # 1.24.0; command + template registered
├── CHANGELOG.md                                    # [1.24.0]
└── README.md                                       # prose block; commands table regenerated
catalog.json                                        # version, command count
agents-list.json                                    # new `methodology` entry, phase `foundation`
AGENTS_LIST.md                                      # prose block; generated regions
README.md                                           # generated agents table
docs/index.html                                     # command card
docs/packages/spectra.zip                           # rebuilt
.specify/memory/constitution.md                     # MINOR 1.13.0, via /speckit-constitution (user-run)
tests/test_methodology_flow.py                      # NEW
tests/test_domain_analyzer_flow.py                  # 6 lenses, 7 questions, hand-on to methodology
tests/test_deployment_strategy_flow.py              # branching model referred
tests/test_doc_output_paths.py                      # SINGLETON gains methodology.md
tests/test_kb_vault_flow.py                         # reserved-map row
tests/test_review_pr_flow.py                        # T2 row, accepted-only
```

**Structure Decision**: one new command and template in the existing extension layout, plus edge edits to four
commands. Nothing new outside the paths above.

## Phase 0 — Research

See [research.md](./research.md):
- R1 command and file names
- R2 the question round
- R3 the deployment-strategy boundary
- R4 kb-vault routing
- R5 review-pr as a reader
- R6 mode detection
- R7 overlay obligations and evidence
- R8 the domain-analyzer migration
- R9 section mapping
- R10 the constitution amendment
- R11 candidate IDs
- R12 the onboarding body
- R13 a hand-written file at the canonical path

## Phase 1 — Design

- [data-model.md](./data-model.md): the entities, their allowed values, and transitions.
- [contracts/methodology-behaviour.md](./contracts/methodology-behaviour.md): numbered behaviours, each mapped to
  an FR and to the test that pins it.
- [contracts/sibling-boundaries.md](./contracts/sibling-boundaries.md): the ownership table all four agents
  must agree with.
- [quickstart.md](./quickstart.md): automated checks, then manual runs in a throwaway Spec Kit project.

## Complexity Tracking

| Deviation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Edge changes to three agents the spec did not name (`deployment-strategy`, `kb-vault`, `review-pr`) | Without them the branching model has two sources, an absorbed methodology lands beside the singleton, and FR-034 has no reader to bind | Leaving them for a follow-up ships a release in which two agents propose the same clause, which is the failure User Story 3 exists to prevent |
