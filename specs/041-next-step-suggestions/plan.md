# Implementation Plan: Consistent Next-Step Suggestions Across the SDLC

**Branch**: `041-next-step-suggestions` | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/041-next-step-suggestions/spec.md`

## Summary

SPECTRA suggests a next step at the end of every SDLC command, and never runs one. After a core Spec Kit
command, the suggestion is a hook:

- `after_clarify` gains a test-plan offer;
- `after_implement` gains a converge offer ahead of UAT and a PR;
- a new `after_converge` event offers UAT before a PR.

The hooks keep a fixed order, set by their position in the list. After a SPECTRA agent, the suggestion is a
closing block in the agent's own report, written from how the run turned out. `defect-rca`, `impact`, and
`flaky-test-detector` each gain one, in a shared layout and only under the conditions the spec sets. The
other seven agents' endings are untouched.

Two research findings shape the change:

- Spec Kit 0.11.2 is the first release with `converge`, so it becomes the floor.
- Spec Kit currently accepts a hook that targets a core command, but doesn't document it. That dependency is
  recorded beside the entry.

## Technical Context

**Language/Version**: Markdown command prompts and YAML (the extension); Python 3 standard library (tools and tests)

**Primary Dependencies**: Spec Kit `>=0.11.2` (raised from `>=0.11.0`, research R1); no new dependency

**Storage**: N/A — files in the repository only

**Testing**: standard-library `unittest` (`python3 -m unittest discover -s tests`), `tools/generate_agent_docs.py --check`, and the manual install pass in `quickstart.md`

**Target Platform**: any Spec Kit project, any supported coding agent (agent-neutral commands)

**Project Type**: Spec Kit extension (catalog channel) — no CLI change

**Performance Goals**: N/A — prompt text; the closing block adds at most a few lines to a report

**Constraints**: nothing runs without the user; no `optional: false`, no `condition`; no agent reads `extensions.yml`; no new deliverable location or template; the CLI (`spectra_cli/`, `VERSION`) is untouched

**Scale/Scope**: 1 manifest (4 hook events, 6 entries); 3 command bodies gain a closing block; 2 agent sources and 1 hand-written page reworded; 1 new test module and 2 adjusted ones; version bump to 1.30.0

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
| --- | --- | --- |
| I. Spec-driven, user holds every phase | Feature work through specify → clarify → plan, each invoked by the user; this plan stops here | PASS |
| II. One self-contained extension | No new folder or extension. Hooking `speckit.converge` targets Spec Kit core, not another extension, so SPECTRA still depends on no other extension | PASS |
| III. Agent-agnostic commands | Hook commands use dotted ids, which Spec Kit renders per agent. Closing blocks name Spec Kit's specify command and tell the agent to render it in its own invocation syntax, as `test-plan.md` already does for the planning command. No literal `/speckit-specify` is hard-coded (contracts/closing-suggestion.md). Some existing hand-offs (`adr`, `test-strategy`) hard-code `/speckit-constitution`; they are out of this feature's scope (FR-018) and are not a precedent for new text | PASS |
| IV. Context-aware | Each closing block is built from the run's own outcome (validated cause, analysis path, open rows and their reasons) | PASS |
| V. Catalog and package in sync | `agents/`, command files, `extension.yml` (1.30.0), `CHANGELOG.md`, `catalog.json`, and `spectra.zip` in one change; generator re-run; `--check` passes | PASS (obligation carried into tasks) |
| VI. Independent channels | Extension bumps minor; `VERSION` and `spectra_cli/` untouched; no tag | PASS |
| VII. One declared artifact root | No new deliverable and no new write location; `impact` still writes nothing under `specs/` | PASS |
| VIII. Overridable templates | The closing block is session guidance, like the existing ready-to-paste prompts, not a document deliverable (research R5); no template changes | PASS |
| Publishing: compatibility pinning | Floor raised to the first release that has what the manifest now uses; exercised on the installed 1.2.4 in the quickstart pass | PASS |

**Post-design re-check (after Phase 1)**: unchanged. The contracts add no write location, no template, no
mandatory hook, and no CLI surface.

## Project Structure

### Documentation (this feature)

```text
specs/041-next-step-suggestions/
├── spec.md
├── plan.md                         # this file
├── research.md                     # Phase 0
├── data-model.md                   # Phase 1
├── quickstart.md                   # Phase 1
├── contracts/
│   ├── hooks.md                    # the exact hooks: section
│   └── closing-suggestion.md       # the shared closing block and each agent's conditions
├── checklists/requirements.md
└── tasks.md                        # Phase 2 (/speckit-tasks, not created here)
```

### Source Code (repository root)

```text
spectra/
├── extension.yml                   # hooks: section (contracts/hooks.md), requires floor, version 1.30.0
├── CHANGELOG.md                    # [1.30.0] entry
└── commands/
    ├── defect-rca.md               # Step 13 closing block
    ├── impact.md                   # Step 14 closing block; "never does" row clarified
    └── flaky-test-detector.md      # Step 7 decline path, Step 9, Step 10 closing block

agents/
├── test-plan.md                    # manifest + body: offered after specify or clarify
└── uat.md                          # body: offered after implement and after converge

docs/
├── getting-started/spectra.html    # hand-written walkthrough: converge → UAT offer
└── packages/spectra.zip            # rebuilt

catalog.json                        # version 1.30.0

tests/
├── test_next_step_suggestions.py   # new
├── test_test_plan_flow.py          # slice after_specify to the next event; reworded phrase
└── test_uat_flow.py                # slice after_implement to the next event; optional count >= 6

# generated by tools/generate_agent_docs.py — never hand-edited:
agents-list.json, AGENTS_LIST.md, spectra/README.md, docs/getting-started/agents.html,
description: lines in spectra/extension.yml and spectra/commands/*.md
```

**Structure Decision**: the existing single-extension layout. Every change edits a file that already exists,
except the one new test module. No agent is added or removed, so the command count (14) and the shipped set
are unchanged.

## Phase 0 — Research

[research.md](research.md) settles every unknown:

| ID | Topic | Decision |
| --- | --- | --- |
| R1 | Spec Kit floor | `>=0.11.2` |
| R2 | Hooking a core command | Allowed; dependency recorded |
| R3 | Display order | List order; priorities 3 / 5 / 10 |
| R4 | Where each closing block attaches | Attach points and conditions per agent |
| R5 | Block layout and Principle VIII | Shared two-part block; no template |
| R6 | Verification | New test module; fix two tests that mis-slice the manifest |
| R7 | Published text to reword | `agents/test-plan.md`, `agents/uat.md`, the walkthrough page |

## Phase 1 — Design

- [contracts/hooks.md](contracts/hooks.md) — the `hooks:` section exactly as it will ship, with its comments.
- [contracts/closing-suggestion.md](contracts/closing-suggestion.md) — the shared block, and for each of
  the three agents its attach point, offer condition, prompt contents, and no-offer reasons.
- [data-model.md](data-model.md) — the two entities (hook entry, closing suggestion) and the outcome states
  that select a closing block.
- [quickstart.md](quickstart.md) — the automated checks and the manual install pass that prove SC-001 to
  SC-006.

### Change notes for tasks

- **Order of work**: manifest and its tests first (US1–US3 are manifest-only), then the three command bodies
  (US4–US6), then `agents/` wording, the walkthrough page, the changelog, the version, the generator, the
  zip, and the catalog.
- **Existing tests that must change with the manifest**: see research R6. Without the slicing fix they pass
  or fail for the wrong reason once `after_clarify` and `after_converge` exist.
- **Unchanged-ness (SC-005)** is verified by diff review: `git diff` touches no file of `adr`, `brd`,
  `domain-analyzer`, `methodology`, `test-strategy`, `deployment-strategy`, or `kb-vault` beyond regenerated
  listings. The new test also asserts that `kb-vault.md` never names `/speckit-constitution`.
- **Changelog** records the core-command dependency (FR-010), the raised floor, and that the hooks are
  offers only.

## Complexity Tracking

No constitution violations to justify.
