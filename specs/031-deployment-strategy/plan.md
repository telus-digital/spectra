# Implementation Plan: Deployment Strategist Agent

**Branch**: `031-deployment-strategy` | **Date**: 2026-10-15 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/031-deployment-strategy/spec.md`

## Summary

A twelfth Spectra command, `speckit.spectra.deployment-strategy`, and the **third standing-policy
singleton**, after `test-strategy` and `domain-analyzer`. It reads the project and any documents the user
supplies, classifies what ships, works six mandatory lenses — environments & promotion; pipeline,
artifact & traceability; release & versioning; data & schema change; rollback & recovery; operability &
configuration — asks five judgement calls one at a time, and writes one recommendation to
`<artifact-root>/DEPLOYMENT_STRATEGY.md`. It then checks the constitution, drafts an amendment carrying
only durable invariants, gates it, and hands off to `/speckit-constitution` with a ready-to-paste line.
It never writes the constitution.

Four properties shape the design.

**It is a copy of a proven shape, not a new one.** `test-strategy` already solved root resolution, the
publication check, the one-question-per-turn round, parseable front matter, re-runs, non-interactive
mode, and the amendment gate. Every one of those is carried over in the same words where the behaviour
is the same, so a reader who knows one agent knows the other, and the test suite can assert the shared
rules the same way. What is new is only what is about deployment: the deployable classification, the six
lenses, the four-way provenance, the open-questions section, the Mermaid diagram, and the
invariants-only amendment.

**Classification comes before every lens.** The reference document assumes a running service on a
cluster. Applied unconditionally, that shape recommends `kubectl rollout undo` to a library. Research
R1 and R3 make "what ships" a step-zero fact read from evidence, and every lens's meaning is resolved
against it — release channels instead of environments, publish instead of deploy, yank-or-supersede
instead of rollback.

**Its honesty rule has four provenances, not three.** `test-strategy` distinguishes citation,
convention, and stated. Deployment policy routinely lives in documents outside the repository — a
client's hosting standard, a platform team's runbook — so a citation to a document is split from a
citation to what the repository actually does (R5). A README saying "we deploy with blue-green" is
*claimed in docs*; a workflow that does it is *verified*.

**It runs nothing, ever.** `test-strategy` has one gated exception — a coverage run. This agent has
none: nothing about a deployment strategy is measured by executing the project, and the only executions
that would tell it anything (a deploy, a `kubectl` query) touch shared infrastructure.

The command file is the deliverable, with a registered template beside it. No script and no binary
ships. This change also amends this repository's constitution, because Principle VII says a new
singleton is named there by amendment and a command may not declare itself one.

## Technical Context

**Language/Version**: Markdown command prompt in Spec Kit's generic format; Python 3.9+ (standard
library only) for this repository's tools and tests

**Primary Dependencies**: Spec Kit `>=0.11.0`. No runtime tool dependency, no `git`/`gh` gate, no
network request (FR-049)

**Storage**: the target project's `<artifact-root>/DEPLOYMENT_STRATEGY.md` — one file, rewritten in
place. Nothing under `.specify/`, no cache, no cross-run state beyond the document

**Testing**: `python3 -m unittest discover -s tests` (1263 passing at baseline);
`python3 tools/generate_agent_docs.py --check`; a new `tests/test_deployment_strategy_flow.py`; existing
modules gain the command: `test_doc_output_paths.py` (`SINGLETON`, with no earlier location),
`test_document_templates.py`, `test_roster_data.py`

**Target Platform**: every coding agent and OS Spec Kit supports; classification and reading are prompt
instructions

**Project Type**: Spec Kit extension command — a prompt under `spectra/commands/`, a registered template
under `spectra/templates/`, plus the publishing surface Principle V requires

**Performance Goals**: not latency-bound. The round is capped at five questions and the session report
at a terminal-readable per-lens summary

**Constraints**: Markdown only; `$ARGUMENTS`; no network; never writes the constitution (FR-047); never
edits source, CI, manifests, or IaC (FR-049); exactly one file per run (FR-034); never reproduces a
secret (FR-007); operability stays high level (FR-019)

**Scale/Scope**: 1 command file; 1 template; 2 manifest entries; 1 roster entry; 1 catalog update; 1
changelog entry; 1 constitution amendment; 1 rebuilt zip; landing page, prose block, CONTRIBUTING, the
kb-vault reserved map, and the e-learning customization table; 1 new test module plus three registry
updates

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | This spec/plan/tasks set on branch `031-deployment-strategy`; four clarifications recorded in the spec before planning. |
| II. A Single Self-Contained Extension | ✅ | One new file under `spectra/commands/`, one under `spectra/templates/`. No new extension, no dependency on another. |
| III. Agent-Agnostic Commands | ✅ | Text only, `$ARGUMENTS` for the hint, references, and `--non-interactive`. `/speckit-constitution` is a command the user runs, never one this command invokes. |
| IV. Context-Aware by Default | ✅ | FR-004 to FR-007 read the constitution, specs, ADRs, CI, container and orchestration files, IaC, migrations, release config, and the sibling singletons; FR-008 to FR-011 make the classification change what every lens may assert. |
| V. Catalog and Package in Sync | ✅ | Manifest, roster, catalog, changelog, zip, landing page, generated regions, and a hand-written prose block move together (FR-052). |
| VI. Two Independently-Versioned Channels | ✅ | Extension only: 1.19.0 → 1.20.0. `spectra_cli/` and `VERSION` untouched (FR-054). |
| VII. Documents Under One Declared Root | ✅ | **Engaged, no deviation.** Declared root, publication check, non-publishing fallback, lowercase project-relative paths. The singleton form is legitimate only once the constitution names it, so this change amends Principle VII (FR-051) rather than arguing a deviation. No earlier location exists, so the read-report-leave-alone rule has nothing to act on. |
| VIII. Shaped by Overridable Templates | ✅ | **Engaged.** New registered `deployment-strategy-template`, four-layer stack, inline skeleton last, resolved path reported; the rules live in the command (FR-036 to FR-038). |

**Amendment classification**: **required**, MINOR — 1.9.0 → 1.10.0. Principle VII gains a third named
singleton; no principle is added, removed, or redefined. The amendment and its sync impact report land
in this change, before the command that relies on it ships.

**Extension version classification**: MINOR — 1.19.0 → 1.20.0. A command and a template are added; no
command is renamed or removed. `catalog.json` `provides.commands` goes 11 → 12. `kb-vault`'s reserved map
gains a row so an ingested deployment strategy lands at the singleton path — an additive change to its
behaviour, inside the same MINOR.

### Does "producing a document is not a licence to edit governance" forbid the handoff?

No, for the same reason it does not forbid `test-strategy`'s: Principle VII's own text carves out "the
one constitution change a Spectra command may propose is one that is *about* the decision it just
recorded, and even that requires explicit approval". The command proposes, gates on approval, records
the draft in its own document, and hands off; the constitution file is never written. Research R8
narrows what it may propose further — durable invariants only — so the proposal is about the decision
and not a transcription of its environment-specific detail.

**Post-design re-check (after Phase 1)**: unchanged — all ✅. The contracts add no write target, no
runtime dependency, and no network path; the data model is document-only.

## Project Structure

### Documentation (this feature)

```text
specs/031-deployment-strategy/
├── plan.md              # This file
├── research.md          # Phase 0 decisions
├── data-model.md        # Phase 1: the document's entities and front matter
├── quickstart.md        # Phase 1: validation scenarios
├── contracts/
│   ├── command-interface.md     # arguments, flags, never-list, session flow
│   ├── clarification-round.md   # the five questions, confirmations, dispositions
│   ├── document-contract.md     # path, front matter, sections, provenance, diagram
│   └── amendment-handoff.md     # constitution states, invariant catalogue, gate, handoff line
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 (/speckit-tasks)
```

### Source Code (repository root)

```text
spectra/
├── commands/
│   ├── deployment-strategy.md        # NEW — the command
│   └── kb-vault.md                   # reserved map gains DEPLOYMENT_STRATEGY.md
├── templates/
│   └── deployment-strategy-template.md   # NEW — registered, overridable
├── extension.yml                     # command + template registered; 1.19.0 → 1.20.0
└── CHANGELOG.md                      # 1.20.0 entry

.specify/memory/constitution.md       # Principle VII names the third singleton; 1.9.0 → 1.10.0
agents-list.json                      # deployment-strategy roster entry
catalog.json                          # version, command count, tags
docs/index.html                       # command card
docs/packages/spectra.zip             # rebuilt
docs/e-learning/customization.html    # template table row
AGENTS_LIST.md                        # SPECTRA:AGENT prose block + regenerated regions
README.md, spectra/README.md          # regenerated regions
CONTRIBUTING.md                       # singleton list

tests/
├── test_deployment_strategy_flow.py  # NEW
├── test_doc_output_paths.py          # SINGLETON entry, earlier location optional
├── test_document_templates.py        # command → template mapping
└── test_roster_data.py               # shipped-agent census
```

**Structure Decision**: the existing single-extension layout. The command mirrors `test-strategy.md`'s
section order (one rule, input, never-list, rules, definitions, numbered steps, re-run, non-interactive,
limitations, inline skeleton) so the two read as siblings.

## Complexity Tracking

No Constitution Check violations. Nothing to justify.
