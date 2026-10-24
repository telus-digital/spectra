# Implementation Plan: An Interactive Domain Analyzer That Feeds the Constitution

**Branch**: `034-interactive-domain-analyzer` | **Date**: 2026-10-23 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/034-interactive-domain-analyzer/spec.md`

## Summary

`speckit.spectra.domain-analyzer` stops asking the SME to tick a file after the session and instead decides in
the session, on the shape `test-strategy` already uses: state the constitution's presence and the run's goal
first, read the project, work seven fixed lenses, ask eight questions one per turn (≥4 options, one
recommended, one Skip), then write `<artifact-root>/DOMAIN_ANALYSIS.md` once, with every decision recorded and
a **Constitution input** section that `/speckit-constitution` consumes through a create or amend prompt.

Most of this already exists in the working tree (written before the spec, at the maintainer's request). This
plan records the design, reconciles it against the spec, and names the one gap the clarification opened:
an unticked item in a legacy checkbox file is **undecided** (FR-020), while the working tree still reads it as
declined.

## Technical Context

**Language/Version**: Markdown command prompt; Python 3.9+ for tests

**Primary Dependencies**: none. Standard library only

**Storage**: one Markdown file per project, `<artifact-root>/DOMAIN_ANALYSIS.md`, with YAML front matter

**Testing**: `python3 -m unittest discover -s tests`; `python3 tools/generate_agent_docs.py --check`;
`python3 tools/build_package.py`; `python3 tools/ship.py --dry-run`

**Target Platform**: any Spec Kit agent, slash-command or skills mode

**Project Type**: Spec Kit extension (Markdown commands)

**Performance Goals**: a run is bounded by its round: exactly eight questions, at most five candidates per
lens, so at most 35 candidates are ever presented

**Constraints**: Markdown only; agent-agnostic (no agent-specific question tool named); one file written per
run, after the round; never writes the constitution; no network

**Scale/Scope**: one command file rewritten, one template rewritten, one test module rewritten, one assertion in
another, version sync across seven published files, one PATCH constitution amendment

## Evidence

| Claim | How it was verified |
|---|---|
| The 1.22.0 agent decides by checkbox after the session | `git show main:spectra/commands/domain-analyzer.md`, Step 4 format rules: "every candidate MUST be `- [ ]`" |
| `test-strategy` decides in the session | `spectra/commands/test-strategy.md` Step 5: five questions, one per turn, 2–4 options, one recommended |
| `DOMAIN_ANALYSIS.md` is a named singleton | `.specify/memory/constitution.md` Principle VII names `<artifact-root>/DOMAIN_ANALYSIS.md` |
| Other agents read the file by name | `review-pr.md` (T2 standards tier), `kb-vault.md` (routing table), `deployment-strategy.md` (sibling documents) |
| Principle VII mentions "an SME's ticks" | constitution lines describing the Spec Kit carve-out and legacy reads |
| Working tree implements FR-001–FR-019 and FR-021 | `tests/test_domain_analyzer_flow.py` (rewritten) passes, 1467 tests green, `ship.py --dry-run` clean |
| `review-pr` does not filter the analysis by decision | `spectra/commands/review-pr.md:277` reads `DOMAIN_ANALYSIS.md` as T2; `:641` lets a supporting-document clause reach Major; nothing names `accepted` (FR-022) |
| Working tree does not yet implement FR-020 as clarified | `spectra/commands/domain-analyzer.md` re-run rule, `spectra/README.md`, `spectra/CHANGELOG.md`, and `test_a_legacy_checkbox_file_is_read` all say unticked = declined |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | This spec/plan/tasks on branch `034-interactive-domain-analyzer`. The implementation predates the spec; tasks reconcile against it rather than rebuild it (see Complexity Tracking) |
| II. Single Self-Contained Extension | ✅ | No files added to or removed from `spectra/` |
| III. Agent-Agnostic Commands | ✅ | The round is described in prose; no agent's question tool or invocation syntax is named. `$ARGUMENTS` and one flag, as before |
| IV. Context-Aware by Default | ✅ | Strengthened: the constitution is read first and its presence sets the run's goal; sibling strategies are read so nothing contradicts them |
| V. Catalog and Package in Sync | ✅ | `extension.yml`, `catalog.json`, `CHANGELOG.md`, `agents-list.json` description, `docs/index.html`, prose in `spectra/README.md` and `AGENTS_LIST.md`, rebuilt zip, regenerated listings |
| VI. Two Versioned Channels | ✅ | Extension only, 1.22.0 → 1.23.0. Root `VERSION` untouched; no tag |
| VII. Documents Under One Declared Root | ✅ | Same singleton path and name, same declared-root resolution, publication check, non-publishing fallback, and earlier-location read |
| VIII. Overridable Templates | ✅ | Template rewritten to the new sections, still resolved through the five-layer stack; the record format, front matter, and Constitution input format stay command-owned, and the command writes Constitution input even if an override omits it |

**Amendment classification**: PATCH, 1.11.0 → 1.11.1. Principle VII's examples "a guardrail proposal an SME
ticks" and "an SME's ticks" are reworded to "decides on" and "choices". No rule changes; the singleton list is
untouched because the filename is kept.

**Extension version classification**: MINOR, 1.22.0 → 1.23.0. The command name, argument, flag, and output
path are unchanged; the interaction and the document's format change, and earlier files are still read.

**Post-design re-check**: unchanged — all ✅. The Phase 1 contract adds no file, path, or dependency.

## Project Structure

### Documentation (this feature)

```text
specs/034-interactive-domain-analyzer/
├── spec.md
├── plan.md              # this file
├── research.md          # Phase 0: R1–R8
├── data-model.md        # Phase 1: candidate, question, Constitution input, run goal
├── contracts/
│   └── domain-analyzer-behaviour.md   # the textual contract the tests pin
├── quickstart.md        # Phase 1: how to validate
├── checklists/requirements.md
└── tasks.md             # /speckit-tasks, not this command
```

### Source Code (repository root)

```text
spectra/
├── commands/domain-analyzer.md            # rewritten (FR-001–FR-021)
├── templates/domain-analysis-template.md  # rewritten sections
├── extension.yml                          # 1.23.0, command + template descriptions
├── CHANGELOG.md                           # [1.23.0]
└── README.md                              # domain-analyzer prose; commands table regenerated
catalog.json                               # version mirror
agents-list.json                           # roster description
AGENTS_LIST.md                             # prose block
docs/index.html                            # command card
docs/e-learning/module-4.html              # lab note
docs/packages/spectra.zip                  # rebuilt
.specify/memory/constitution.md            # PATCH 1.11.1
tests/test_domain_analyzer_flow.py         # rewritten
tests/test_doc_output_paths.py             # ready-prompt assertion
spectra/commands/review-pr.md              # one paragraph: accepted guardrails only (FR-022)
tests/test_review_pr_flow.py               # one test for FR-022
```

**Structure Decision**: single-command change in the existing extension layout. No new files under
`spectra/`.

## Phase 0 — Research

See [research.md](./research.md): R1 filename, R2 question unit, R3 option set, R4 skip and silence, R5
observed/aspirational, R6 testing and deployment referral, R7 handoff wording, R8 legacy checkbox files.

## Phase 1 — Design

- [data-model.md](./data-model.md) — the four entities and their allowed values and transitions.
- [contracts/domain-analyzer-behaviour.md](./contracts/domain-analyzer-behaviour.md) — 25 numbered
  behaviours, each mapped to an FR and to the test that pins it.
- [quickstart.md](./quickstart.md) — automated checks, then three manual runs in a throwaway Spec Kit project.

## Complexity Tracking

| Deviation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Implementation written before the spec (Principle I order) | The maintainer asked for the change directly, then chose to regenerate the spec with Spec Kit for consistency | Discarding working, tested code to rewrite it after the spec would produce the same files; tasks instead verify each FR against the working tree and fix the one gap (FR-020) |
