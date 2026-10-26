# Implementation Plan: One Source of Truth for Every Agent

**Branch**: `040-agent-single-source` | **Date**: 2026-10-25 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/040-agent-single-source/spec.md`

## Summary

A new `agents/` directory holds one Markdown file per agent: a flat `key: value` header and, for the
14 shipped Spectra agents, a long description. `tools/generate_agent_docs.py` stops reading
`agents-list.json` and reads `agents/` instead. It writes `agents-list.json` whole, byte-identical to
today's file when seeded. It also writes every existing generated region, three new regions (the
shipped-agent sections of `AGENTS_LIST.md`, the per-agent sections of `spectra/README.md`, and the
sidebar and cards of `docs/getting-started/agents.html`), and the description lines in
`spectra/extension.yml` and each command file. Markdown converts to HTML through a small
standard-library renderer that accepts only the subset the prose already uses and rejects anything
else with file and line.
`--check` compares every output with what the source would produce, so a stale output and a hand edit
fail the same way. Seeding merges today's copies into the source and writes a seeding report.

## Technical Context

**Language/Version**: Python ≥ 3.9 (the repository floor; CI runs 3.9 and 3.12). No `tomllib`, no
`match`, no 3.10+ APIs.

**Primary Dependencies**: standard library only (`argparse`, `html`, `json`, `re`, `textwrap`,
`pathlib`). `spectra_cli.roster` is reused, unchanged, to validate the roster the generator builds.

**Storage**: files in the repository. Source: `agents/*.md`. Outputs: `agents-list.json`, `README.md`,
`AGENTS_LIST.md`, `spectra/README.md`, `spectra/extension.yml`, `spectra/commands/*.md`,
`docs/getting-started/agents.html`.

**Testing**: standard-library `unittest` (`python3 -m unittest discover -s tests`), which today runs 1711 tests.

**Target Platform**: maintainer machines (macOS/Linux/Windows) and GitHub Actions `ubuntu-latest`.
Outputs use `\n` line endings regardless of platform, as the generator does today.

**Project Type**: maintainer tooling (a code generator) plus static documentation. Nothing new ships
to users' machines.

**Performance Goals**: a full generate or `--check` over 55 agents finishes in well under a second, and
CI time is unchanged.

**Constraints**: the schema of `agents-list.json` is unchanged and the file is byte-identical after
seeding (installed CLIs and `docs/agents.html` read it at run time). The CI job names are unchanged
(the `main` ruleset requires them by name). The Agent reference page stays static, with no new fetch.
Generation is deterministic: two runs produce identical bytes.

**Scale/Scope**: 55 agents (14 shipped, 10 Spec Kit core, 31 planned) and 7 phases. The scope is
roughly 730 lines of `AGENTS_LIST.md` prose, 960 lines of `spectra/README.md` prose, 14 cards, and 28
description lines.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The plan is evaluated against constitution **2.0.0**. The amendment is on this branch and not yet
committed; FR-022 is satisfied by it.

| Principle | Gate | Status |
| --- | --- | --- |
| I. Spec-Driven Development | Feature runs through specify → clarify → plan; the user invokes each phase | ✅ Pass |
| II. Single Self-Contained Extension | No new extension; `spectra/` gains no files; only description lines and README prose are regenerated | ✅ Pass |
| III. Agent-Agnostic Commands | Command bodies untouched; only the front-matter `description:` line is generated | ✅ Pass |
| IV. Context-Aware by Default | No command behaviour changes | ✅ N/A |
| V. Catalog and Package in Sync | This feature *implements* 2.0.0's Principle V: `agents/` is the only source; every listed output is generated; `--check` fails on stale or hand-edited outputs. Changed shipped text carries an extension bump (1.28.0 → 1.29.0), changelog entry, `catalog.json` update, and zip rebuild in the same change | ✅ Pass |
| VI. Two Release Channels | `spectra_cli/` and `VERSION` untouched; `roster.py` unchanged; no tag | ✅ Pass |
| VII. Artifact Root | No document-producing command changes | ✅ N/A |
| VIII. Overridable Templates | No template changes | ✅ N/A |
| Zero dependencies | Parser and Markdown renderer are hand-written on the standard library | ✅ Pass |
| Branching / shipping | Lands through `tools/ship.py`; CI job names unchanged (FR-020) | ✅ Pass |

No violations. Complexity Tracking is empty.

**Post-design re-check**: still passing.
- The design adds two `tools/` modules and no shipped files.
- It keeps `agents-list.json` byte-identical (research Findings), `roster.py` unchanged, and the CI job
  names and `checks.py` registry unchanged (D7).
- It moves every agent fact into `agents/`, as Principle V 2.0.0 requires.
- Three spec refinements follow from the design (research "Spec refinements": FR-004, FR-013, SC-004).
  None conflicts with the constitution.

## Project Structure

### Documentation (this feature)

```text
specs/040-agent-single-source/
├── plan.md              # This file
├── research.md          # Phase 0: decisions and the spec refinements they imply
├── data-model.md        # Phase 1: source entities, validation, rendering map
├── quickstart.md        # Phase 1: validation scenarios
├── contracts/
│   ├── agent-source-format.md   # The source file grammar (header + body)
│   ├── generated-outputs.md     # Every output, its region, and what it contains
│   └── agents-page-markup.md    # The card/sidebar HTML the tests and CSS rely on
├── seeding-report.md    # Written during implement (FR-016)
└── tasks.md             # Phase 2 (/speckit-tasks)
```

### Source Code (repository root)

```text
agents/                              # NEW — the only source of truth
├── _phases.md                       #   7 phases, in order
├── adr.md … uat.md                  #   14 shipped Spectra agents (header + body)
├── constitution.md … converge.md    #   10 Spec Kit core agents (header only)
└── <planned-id>.md                  #   31 planned agents (header only)

tools/
├── generate_agent_docs.py           # REWRITTEN — loads agents/, renders every output
├── agent_source.py                  # NEW — header/body parser + validation (stdlib)
├── markdown_subset.py               # NEW — Markdown subset → Markdown blocks / HTML
└── checks.py                        # unchanged registry; generated-listings now covers all outputs

agents-list.json                     # becomes a generated output (byte-identical)
AGENTS_LIST.md                       # + region agents-list-shipped
spectra/README.md                    # + region spectra-readme-agents
spectra/extension.yml                # description lines generated
spectra/commands/*.md                # front-matter description line generated
docs/getting-started/agents.html     # + regions agents-page-nav, agents-page-cards
docs/getting-started/getting-started.css  # + styles for the collapsed Full reference

tests/
├── test_agent_source.py             # NEW — grammar and validation failures
├── test_markdown_subset.py          # NEW — rendering and rejection with file:line
├── test_generator.py                # REWORKED — sandbox includes agents/ and every output
└── (flow tests unchanged in what they assert)

CONTRIBUTING.md, SHIPPING.md, CLAUDE.md   # "edit agents/<id>.md, run the generator"
```

**Structure Decision**: The generator stays a single entry point, `tools/generate_agent_docs.py`, so
`checks.py`, `ship.py`, CI, and the docs that name it keep working. The parsing and Markdown code
moves into two sibling modules under `tools/` so each can be tested on its own. Nothing goes under
`spectra_cli/`, so the CLI channel is untouched (Principle VI).

## Complexity Tracking

No Constitution Check violations.
