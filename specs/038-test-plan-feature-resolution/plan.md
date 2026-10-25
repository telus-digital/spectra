# Implementation Plan: Test plan finds its feature the way the planner does

**Branch**: `038-test-plan-feature-resolution` | **Date**: 2026-10-25 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/038-test-plan-feature-resolution/spec.md`

## Summary

`speckit.spectra.test-plan` stops taking its specification from the argument and resolves the feature by
the rule Spec Kit's `get_feature_paths` uses, so `test-plan.md` and the `plan.md` it hands off to always
share a directory. No agent is added. Traceability, lenses, UAT, regression scope, the existence gate,
non-interactive mode, and the Step 17 prompt are unchanged.

1. **Step 1 is rewritten as "Resolve the feature."** One read-only shell read returns `SPECIFY_INIT_DIR` and
   `SPECIFY_FEATURE_DIRECTORY`. The project root is the first if set, otherwise the nearest `.specify/`. The
   feature directory is the second if set, otherwise `feature_directory` from that root's
   `.specify/feature.json`, otherwise a stop. Empty counts as unset. The spec is `<dir>/spec.md`.
2. **The argument becomes an optional confirmation.** It must name the resolved directory or its `spec.md`.
   Anything else stops before the spec is read.
3. **The resolution is announced first** and recorded in the identifying block (Step 13) and the report
   (Step 16).
4. **The handoff is gated on agreement.** Before Step 17 prints, the run re-reads only `feature.json` (when
   the variable was unset) and confirms that the planner would still resolve the directory written to.
5. **"Never infer" becomes "resolve only as the planner does."** The never-table row, the section, and its
   reasoning are rewritten. The "runs nothing" row names the one environment read.
6. **The surfaces move with it.** The front matter, the manifest description and `after_specify` prompt,
   `AGENTS_LIST.md` prose and examples, the `docs/index.html` card, and the CHANGELOG are updated. The
   package is rebuilt and the existing tests are rewritten to the new contract.

The extension goes from 1.26.0 to 1.27.0. No constitution amendment is needed.

## Technical Context

**Language/Version**: Markdown command prompts; Python 3.9+ for tests and tooling

**Primary Dependencies**: none. Standard library only; the zero-dependency rule covers the whole repository

**Storage**: reads `.specify/feature.json` and two environment variables in the consumer's project; writes
only `<feature-dir>/test-plan.md`, as today

**Testing**:
- `python3 -m unittest discover -s tests`
- `python3 tools/generate_agent_docs.py --check`
- `python3 tools/build_package.py`
- `python3 tools/ship.py --dry-run`

**Target Platform**: any Spec Kit agent, in slash-command or skills mode, with a POSIX or PowerShell shell

**Project Type**: Spec Kit extension (Markdown commands), catalog channel only

**Performance Goals**: no change. One added shell read per run

**Constraints**:
- Markdown only; no script ships in the package (research R2).
- Agent-agnostic: the read is described by what it returns, with a POSIX and a PowerShell form; no agent
  tool is named.
- Resolution never writes `feature.json` and never creates a directory (FR-004).
- The resolution must track upstream `get_feature_paths` in the Spec Kit version Spectra tests against.
- No network access.

**Scale/Scope**:
- One command rewritten in places: `test-plan.md` (front matter, User Input, never-table, Step 1, the never-infer
  section, Step 3's closing sentence, Steps 13, 15, 16, 17, Non-interactive).
- No template change (research R5).
- Manifest description and hook prompt; CHANGELOG; catalog version; `AGENTS_LIST.md` and `docs/index.html`
  prose; the rebuilt zip.
- `tests/test_test_plan_flow.py` rewritten where it pins the old contract, plus a new resolution class.

## Evidence

| Claim | How it was verified |
|---|---|
| The planner resolves root from `SPECIFY_INIT_DIR`, else the nearest `.specify/` | `.specify/scripts/bash/common.sh:56-73` |
| `SPECIFY_INIT_DIR` that is missing or has no `.specify/` is an error | `common.sh:38-52` |
| Feature dir: non-empty `SPECIFY_FEATURE_DIRECTORY`, else `feature.json`, else error; relative values joined to the root | `common.sh:187-215` |
| The planner persists the variable into `feature.json` and runs `mkdir -p` | `common.sh:196-200`; `setup-plan.sh:36` |
| `setup-plan.sh` accepts no path argument | `setup-plan.sh:8-24` |
| The command currently requires a path and forbids `feature.json` | `spectra/commands/test-plan.md:25-38`, `:84-125` |
| It already classes git lookups as reads, not runs | `test-plan.md:223-227` |
| Non-interactive says "an empty argument still stops" | `test-plan.md:814` |
| The handoff is withheld when "no path was supplied" | `test-plan.md:781` |
| The hook prompt tells the agent to pass `SPEC_FILE` | `spectra/extension.yml:129` |
| Tests pin the old contract | `tests/test_test_plan_flow.py:109-165`, `:325-332`, `:576-599` |
| The card and the prose say "no feature record" and show path-only examples | `docs/index.html:601-604`; `AGENTS_LIST.md:505-597` |
| `catalog.json` carries a version, not command descriptions | `catalog.json:9-13` |
| The extension is at 1.26.0 | `spectra/extension.yml:6`; `catalog.json:13` |
| Renaming or removing a command is the only stated MAJOR trigger for the extension | `.specify/memory/constitution.md:393-396` |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | The user ran specify, clarify, and plan on `038-test-plan-feature-resolution` and answered every question. The two spec readings planning had to settle (Spec Reconciliation C1, C2) were accepted by the user. No task edits `spec.md` |
| II. Single Self-Contained Extension | ✅ | Only existing files under `spectra/` change. No new command, folder, script, or dependency |
| III. Agent-Agnostic Commands | ✅ | The read is described by its result, with POSIX and PowerShell forms (R2). No agent tool named |
| IV. Context-Aware by Default | ✅ | Strengthened: the command reads the same feature record the rest of Spec Kit reads |
| V. Catalog and Package in Sync | ✅ | `extension.yml` 1.27.0 and the new description and hook prompt, `catalog.json` version, `CHANGELOG.md`, rebuilt zip, `docs/index.html` card, `AGENTS_LIST.md` prose. The roster's description does not mention the path, so it is unchanged and generated regions need only `--check` |
| VI. Two Versioned Channels | ✅ | Extension only. Root `VERSION` untouched; no tag |
| VII. Documents Under One Declared Root | ✅ | Output stays beside the spec, as today; no artifact root is resolved for it |
| VIII. Overridable Templates | ✅ | No template change. The resolution source is command-owned content of the identifying block (R5) |

**Gate result**: PASS.

**Extension version classification**: MINOR, 1.26.0 → 1.27.0. The argument becomes optional and a new stop is
added; no command is renamed or removed. The CHANGELOG calls out that a path naming a non-active feature
now stops (R7).

**Post-design re-check**: unchanged, all ✅. The contract adds no file beyond those under Source Code.

## Spec Reconciliation

Places where the spec, read literally, meets text or files that already exist. Each has a reading that
changes no requirement. **Accepted by the user (2026-10-25)**: C1 and C2 stand as written below, and
`spec.md` is unchanged. C3 was added from `/speckit-analyze` (I2) and is a statement of fact, not a choice.

| # | Finding | Proposed reading | Spec effect |
|---|---|---|---|
| C1 | **FR-005 calls the environment read "the only exception" to "runs nothing."** The command already performs read-only git lookups (branch for the identifying block, history for the stale-strategy check) and classes them as "a read, not a run" (`test-plan.md:223-227`) | The environment read joins that class and is named in the never-table row as **the only command run to resolve the feature**. The git reads keep their existing status. "Nothing is executed" keeps meaning no build, test, install, or script | None if accepted; FR-005's "only exception" is read as "only exception this feature adds" |
| C2 | **FR-015 preserves non-interactive mode, but that section says "an empty argument still stops."** FR-008 makes the argument optional, so that bullet contradicts the spec | The bullet becomes "a feature that does not resolve still stops". The create-but-never-rewrite asymmetry and the declaration rules are unchanged | None; FR-008 supersedes the one bullet |
| C3 | **FR-018 asks for the command's description to be updated in `catalog.json`.** The catalog carries a version, not per-command descriptions (`catalog.json:9-13`) | FR-018 is met by the front matter and `extension.yml`; `catalog.json` gets only the 1.27.0 version (T026) | None |

## Project Structure

### Documentation (this feature)

```text
specs/038-test-plan-feature-resolution/
├── spec.md
├── plan.md              # this file
├── research.md          # Phase 0: R1–R8
├── data-model.md        # Phase 1: inputs, resolution result, stops, announcement
├── contracts/
│   └── resolution-behaviour.md   # numbered behaviours → FR → test
├── quickstart.md        # automated checks, then manual runs
├── checklists/requirements.md
└── tasks.md             # /speckit-tasks, not this command
```

### Source Code (repository root)

```text
spectra/
├── commands/test-plan.md        # front matter; User Input; never-table; Step 1 + never-infer rewritten;
│                                #   Steps 3 (closing sentence), 13, 15, 16, 17; Non-interactive bullet
├── extension.yml                # 1.27.0; test-plan description; after_specify prompt
├── CHANGELOG.md                 # [1.27.0]
catalog.json                     # version 1.27.0
AGENTS_LIST.md                   # test-plan prose and examples
docs/index.html                  # test-plan card and example
docs/packages/spectra.zip        # rebuilt
tests/test_test_plan_flow.py     # old-contract classes rewritten; new FeatureIsResolvedAsThePlannerDoes
```

**Structure Decision**: only existing files change.

## Phase 0 — Research

See [research.md](./research.md):
- R1: following the planner's rule, step by step
- R2: how the one environment read is done, agent- and shell-agnostically
- R3: matching an explicit argument
- R4: the end-of-run agreement check
- R5: where the resolution source is recorded
- R6: what the remedies say
- R7: version and CHANGELOG
- R8: tests, and the UAT candidate

## Phase 1 — Design

- [data-model.md](./data-model.md): the inputs, the resolution result, the stops, and the announcement.
- [contracts/resolution-behaviour.md](./contracts/resolution-behaviour.md): numbered behaviours, each mapped
  to an FR and the test that pins it.
- [quickstart.md](./quickstart.md): automated checks, then manual runs in a throwaway Spec Kit project.

## Complexity Tracking

No constitution violations. Nothing to justify.
