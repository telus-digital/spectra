# Implementation Plan: Spec Persistence Model in the Methodology Agent

**Branch**: `042-spec-persistence-model` | **Date**: 2026-11-04 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/042-spec-persistence-model/spec.md`

## Summary

`speckit.spectra.methodology` gains one decision inside an existing lens. Lens 4 (Spec lifecycle &
traceability) settles how the team handles a behaviour change to an already-delivered feature: Living
Spec, Flow-Forward, Flow-Back, or Hybrid with Living Spec as the default. Question 5 switches to the
mutually-exclusive shape question 9 already uses. The accepted model is written as one constitution
guardrail that states what each Spec Kit phase does, so an agent reading only the constitution knows
whether to edit the existing spec or start a new feature directory.

The approach is prompt work plus pinned assertions. The command file is the implementation: Step 4 gains
the persistence rules for lens 4, Step 5 gains question 5's shape, Step 7 gains a fifth always-written
reference and a `persistence` front-matter key, and the re-run and non-interactive sections each gain one
rule. The template gains guidance for the persistence reference inside its existing Spec lifecycle
section, with no new heading. The canonical obligation text for each model is fixed in
[contracts/persistence-guardrail.md](contracts/persistence-guardrail.md), and the question's shape in
[contracts/question-five.md](contracts/question-five.md). Nine lenses and ten questions stay as they are.

## Technical Context

**Language/Version**: Markdown command prompt (the shipped artifact); Python 3 standard library for tests
and the repository's generator and package tools

**Primary Dependencies**: None added. Spec Kit ≥ 0.11.2 is already the floor (`requires.speckit_version`),
which covers the converge phase the guardrail names

**Storage**: Files only: the command, its template, `agents/methodology.md`, generated listings, the
package zip

**Testing**: `python3 -m unittest discover -s tests`; `python3 tools/generate_agent_docs.py --check`;
`python3 tools/ship.py --dry-run`

**Target Platform**: Any Spec Kit agent that installs the `spectra` extension (agent-agnostic prompt)

**Project Type**: Spec Kit extension: Markdown agent commands, no runtime code

**Performance Goals**: N/A. The round still holds ten questions, so the run gets no longer

**Constraints**: Nine lenses and ten questions, no renumbering; the candidate record, Constitution input
format, and frozen IDs are unchanged; the template's section list is unchanged, so
`test_sections_match_in_order` keeps passing; the zero-dependency rule applies to tests

**Scale/Scope**: One command (about 810 lines today, expected to grow by roughly 80–110), one template,
one agent source file, one test module extended

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
| --- | --- | --- |
| I. Spec-driven, user holds every phase | Feature work (materially changes what an agent asks and produces) through specify → clarify → plan, each invoked by the user; this plan stops after Phase 1 | PASS |
| II. One self-contained extension | No new folder, command, or extension; the change sits in the existing `spectra/commands/methodology.md` and its template | PASS |
| III. Agent-agnostic commands | Guardrail text names phases ("the specify phase"), not one agent's invocation syntax (research R6). No new hard-coded `/speckit-*` invocation is added to the command | PASS |
| IV. Context-aware | Brownfield recommendation comes from the project's own `specs/` history on the default branch (research R2); greenfield and empty histories say where the agent looked | PASS |
| V. Catalog and package in sync | `agents/methodology.md` manifest and body, the command, the template, `extension.yml` (1.30.0 → 1.31.0), `CHANGELOG.md`, `catalog.json`, rebuilt `spectra.zip`, and regenerated listings in one change; `--check` passes | PASS (obligation carried into tasks) |
| VI. Independent channels | Extension bumps minor; `VERSION` and `spectra_cli/` untouched; no tag | PASS |
| VII. One declared artifact root | No new deliverable or write location; the agent still writes only `<artifact-root>/ENGINEERING_METHODOLOGY.md` and never edits `specs/` (FR-028) | PASS |
| VIII. Overridable templates | The persistence reference is guidance inside the existing template section; the template stays registered and resolved through the same stack; an override that omits the section is honoured and noted, as today | PASS |
| Publishing: compatibility pinning | No new Spec Kit feature is relied on; converge is already within the pinned floor | PASS |

No violations, so Complexity Tracking is empty.

**Post-design re-check (after Phase 1)**: unchanged. The contracts add no write location, no new
template section, no new command, and no CLI surface. The `persistence` key is added to front matter the
command already owns (Step 7), and no other agent reads it.

## Project Structure

### Documentation (this feature)

```text
specs/042-spec-persistence-model/
├── spec.md
├── plan.md              # This file
├── research.md          # Phase 0: decisions R1–R9
├── data-model.md        # Phase 1: candidates, mapping, front matter, decisions
├── quickstart.md        # Phase 1: validation scenarios
├── contracts/
│   ├── question-five.md         # The shape, options, and recording of question 5
│   └── persistence-guardrail.md # Canonical per-phase obligations for each model
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 (/speckit-tasks, not created here)
```

### Source Code (repository root)

```text
agents/
└── methodology.md                 # manifest + long description: name the persistence model in lens 4

spectra/
├── commands/methodology.md        # Step 4 lens 4 rules; Step 5 question 5; Step 7 key + reference;
│                                  # Re-running; Non-interactive; inline skeleton comment
├── templates/engineering-methodology-template.md   # persistence reference guidance in Spec lifecycle
├── extension.yml                  # version 1.31.0; template description mentions the reference
│                                  # (command description: line is generated)
└── CHANGELOG.md                   # [1.31.0] entry

catalog.json                       # spectra version 1.31.0
docs/packages/spectra.zip          # rebuilt
AGENTS_LIST.md, spectra/README.md, docs/getting-started/agents.html, agents-list.json  # regenerated

tests/
└── test_methodology_flow.py       # new TheSpecPersistenceModel class, plus a pin that question 5 leaves
                                   # the four-option shape (the old "questions 3–8 and 10" wording is unpinned)
```

**Structure Decision**: No new files outside this spec directory. Every behavioural change goes into the
existing command and template. Every listing is regenerated from `agents/methodology.md`, never edited
by hand.

## Complexity Tracking

No Constitution Check violations.
