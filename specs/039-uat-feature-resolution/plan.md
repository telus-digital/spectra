# Implementation Plan: UAT finds its feature the way the implement command does

**Branch**: `039-uat-feature-resolution` | **Date**: 2026-10-25 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/039-uat-feature-resolution/spec.md`

## Summary

`speckit.spectra.uat` stops taking its feature from a required argument and resolves it by Spec Kit's
`get_feature_paths` rule, the rule `speckit.spectra.test-plan` adopted in spec 038 (1.27.0). No agent is
added. How UAT performs scenarios, captures evidence, ticks tasks, and writes its report is unchanged.

1. **Step 1 is rewritten** with the same resolution text test-plan uses, adapted to uat:
   - One shell read of `SPECIFY_INIT_DIR` and `SPECIFY_FEATURE_DIRECTORY`.
   - The project root, the invoking project, the feature directory (variable, then record), read-only.
   - An eight-outcome table — seven stops, including the existing "no `tasks.md`" stop, plus the resolved
     row — and one remedy block.
2. **The argument becomes an optional confirmation**: the feature directory or its `spec.md`, else a stop
   before anything is read or started.
3. **The resolution is announced first**, repeated in the run confirmation (Step 3), and recorded in the
   report's Feature row (Step 8) and the session report (Step 9).
4. **The never-table changes in two rows.** "Infer which feature was meant" becomes "Choose a feature by
   any rule but the implement command's". "Start a build … before the run confirmation" gains a sentence
   saying the one environment read starts nothing.
5. **The governing rule, intro, and reasoning are rewritten.** Non-interactive's "A missing feature still
   stops" becomes "A feature that does not resolve still stops".
6. **Surfaces**: front matter and manifest description, `AGENTS_LIST.md` and `spectra/README.md` prose,
   the `docs/index.html` card, CHANGELOG, version, zip, and `tests/test_uat_flow.py`. The `after_implement`
   prompt already names no path and stays as is (research R6).

The extension goes from 1.27.0 to 1.28.0. No constitution amendment is needed.

## Technical Context

**Language/Version**: Markdown command prompts; Python 3.9+ for tests and tooling

**Primary Dependencies**: none. Standard library only

**Storage**: reads `.specify/feature.json` and two environment variables; writes only what uat already
writes (`[UAT]` lines in `tasks.md`, `uat/<run-stamp>/`, `uat-report.md`)

**Testing**:
- `python3 -m unittest discover -s tests`
- `python3 tools/generate_agent_docs.py --check`
- `python3 tools/build_package.py`
- `python3 tools/ship.py --dry-run`

**Target Platform**: any Spec Kit agent, slash-command or skills mode, POSIX or PowerShell shell

**Project Type**: Spec Kit extension (Markdown commands), catalog channel only

**Performance Goals**: no change; one added shell read per run

**Constraints**:
- Markdown only; no script ships.
- Agent-agnostic; no agent tool named.
- Resolution writes nothing and starts nothing.
- The resolution wording matches `spectra/commands/test-plan.md` Step 1 wherever the two commands mean the
  same thing (research R1).
- No network access beyond what the build under test makes.

**Scale/Scope**:
- One command edited in places: `uat.md`. That covers the front matter, intro, governing rule, User
  Input, never-table, Step 1 and its sub-sections, and Steps 3, 8 and 9. It also covers Non-interactive,
  the inline skeleton, and a new degrade row if the command has a degrade list (it has none, see R5).
- No template change (R4).
- Manifest description; CHANGELOG; catalog version; prose and card; zip.
- `tests/test_uat_flow.py`: the old-contract class is rewritten, and new classes are added.

## Evidence

| Claim | How it was verified |
|---|---|
| uat requires a path and forbids `feature.json` | `spectra/commands/uat.md:27-44`, `:64-87` |
| Step 1's table accepts a `specs/` directory with `tasks.md`, or a `spec.md` path | `uat.md:68-74` |
| The "no `tasks.md`" stop | `uat.md:73` |
| Out-of-project stop says "your write destination comes from your input" | `uat.md:89-93` |
| The run confirmation shows the command, environment, and scenarios | `uat.md:124-127` |
| The report's identifying block has a Feature row | `spectra/templates/uat-report-template.md:22`; skeleton `uat.md:274` |
| Non-interactive says "A missing feature still stops" | `uat.md:244-253` |
| The `after_implement` prompt names no path | `spectra/extension.yml:133-138` |
| Tests pin the old contract | `tests/test_uat_flow.py:77-97` (`TheFeatureIsRequiredAndNeverInferred`), and its docstring `:14-15` |
| Prose and card say "required, never inferred" | `AGENTS_LIST.md` `id=uat` block (`:657`+); `spectra/README.md:945`+; `docs/index.html:609-611` |
| test-plan's resolution text, to mirror | `spectra/commands/test-plan.md` Step 1 (shipped in `bf3cf19`) |
| The extension is at 1.27.0 | `spectra/extension.yml:6`; `catalog.json:13` |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | The user ran specify, clarify, and plan on `039-uat-feature-resolution` and answered the one question. No task edits `spec.md` |
| II. Single Self-Contained Extension | ✅ | Only existing files change. No new command, script, or dependency |
| III. Agent-Agnostic Commands | ✅ | The read is described by its result, in POSIX and PowerShell forms. No agent tool named |
| IV. Context-Aware by Default | ✅ | Strengthened: uat reads the feature record the rest of Spec Kit reads |
| V. Catalog and Package in Sync | ✅ | `extension.yml` 1.28.0 and description, `catalog.json` version, `CHANGELOG.md`, rebuilt zip, `docs/index.html` card, `AGENTS_LIST.md` and `spectra/README.md` prose. Roster unchanged; `--check` only |
| VI. Two Versioned Channels | ✅ | Extension only. `VERSION` untouched; no tag |
| VII. Documents Under One Declared Root | ✅ | Output stays in the feature directory, as today |
| VIII. Overridable Templates | ✅ | No template change. The resolution source is command-owned content of the Feature row (R4) |

**Gate result**: PASS.

**Extension version classification**: MINOR, 1.27.0 → 1.28.0. The argument becomes optional and a stop is
added. No command is renamed or removed (the same call as 038).

**Post-design re-check**: unchanged, all ✅.

## Spec Reconciliation

None needed. The two readings 038 had to settle are already explicit in this spec:
- FR-006 frames the environment read as one that starts nothing (038's C1).
- FR-018 names the non-interactive bullet that changes (038's C2).

## Project Structure

### Documentation (this feature)

```text
specs/039-uat-feature-resolution/
├── spec.md
├── plan.md              # this file
├── research.md          # Phase 0: R1–R7
├── data-model.md        # Phase 1: inputs, resolution result, stops, announcement, confirmation
├── contracts/
│   └── resolution-behaviour.md   # numbered behaviours → FR → test
├── quickstart.md
├── checklists/requirements.md
└── tasks.md             # /speckit-tasks
```

### Source Code (repository root)

```text
spectra/
├── commands/uat.md              # front matter; intro; governing rule; User Input; never-table (2 rows);
│                                #   Step 1 + sub-sections rewritten; Steps 3, 8, 9; Non-interactive; skeleton
├── extension.yml                # 1.28.0; uat description
├── CHANGELOG.md                 # [1.28.0]
catalog.json                     # version 1.28.0
AGENTS_LIST.md                   # uat prose and examples
spectra/README.md                # uat section and usage
docs/index.html                  # uat card and example
docs/packages/spectra.zip        # rebuilt
tests/test_uat_flow.py           # old-contract class rewritten; new classes
```

**Structure Decision**: only existing files change.

## Phase 0 — Research

See [research.md](./research.md): R1 shared wording with test-plan, R2 where the read sits relative to the
gates, R3 matching an argument, R4 recording the source, R5 stops and remedy, R6 the hook prompt, R7
version, CHANGELOG, and tests.

## Phase 1 — Design

- [data-model.md](./data-model.md)
- [contracts/resolution-behaviour.md](./contracts/resolution-behaviour.md)
- [quickstart.md](./quickstart.md)

## Complexity Tracking

No constitution violations. Nothing to justify.
