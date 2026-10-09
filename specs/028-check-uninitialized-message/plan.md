# Implementation Plan: One-Step Remedy When the Folder Is Not a Spec Kit Project

**Branch**: `028-check-uninitialized-message` | **Date**: 2026-10-08 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/028-check-uninitialized-message/spec.md`

## Summary

`_say_not_a_project()` in `spectra_cli/cli.py` prints a two-step remedy (`specify init`, then
`spectra install`) even though `spectra install` already offers to run `specify init` itself
(`install.check_in_specify_project`). Replace the two remedy lines with one,
`  Initialize Specify and add Spectra: spectra install`, indented two spaces like the sibling
project-state messages. The function is shared by `check`, `version`, `update`, and `uninstall`, so a
single edit covers all four (FR-004). Flip the one test that currently *requires* `specify init`, and
add exact-output assertions. CLI channel only: PATCH bump `VERSION` 6.2.1 → 6.2.2.

## Technical Context

**Language/Version**: Python 3 (stdlib only — the `spectra_cli/` package)

**Primary Dependencies**: None (zero-dependency constraint)

**Storage**: N/A

**Testing**: stdlib `unittest` — `python3 -m unittest discover -s tests`

**Target Platform**: macOS / Linux / Windows terminals; `uv` tool install

**Project Type**: CLI

**Performance Goals**: N/A (static message)

**Constraints**: Output must read identically with and without ANSI styling (`NO_COLOR`, non-TTY)

**Scale/Scope**: One function (3 lines), one shared call path used by 4 commands, ~3 test files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Applies? | Status |
| --- | --- | --- |
| I. Spec-driven development | Yes | ✅ This feature has spec → plan → tasks → implement. |
| II. Single self-contained extension | No — `spectra/` untouched | ✅ |
| III. Agent-agnostic commands | No — no command files touched | ✅ |
| IV. Context-aware by default | No — no agent behaviour changes | ✅ |
| V. Catalog and package in sync | No — nothing under `spectra/` changes, so no zip/catalog/roster/landing-page work | ✅ |
| VI. Independent release channels | Yes — CLI channel only | ✅ `VERSION` 6.2.1 → 6.2.2 (PATCH: user-facing text fix, no surface change). `spectra/extension.yml` and `catalog.json` MUST NOT bump. Bare-`spectra` `cli vX.Y.Z` banner unaffected. |
| VII / VIII. Artifact root, templates | No — no document deliverables | ✅ |
| Landing on `main` | Yes | ✅ Via `python3 tools/ship.py`, then tag `6.2.2` (SHIPPING.md Path B). Never `git push origin main`. |

**Result**: PASS. No violations; Complexity Tracking not needed.

**Post-design re-check**: PASS — Phase 1 introduced no new files outside `spectra_cli/`, `tests/`,
`VERSION`, and this spec directory.

## Project Structure

### Documentation (this feature)

```text
specs/028-check-uninitialized-message/
├── plan.md              # This file
├── research.md          # Phase 0
├── data-model.md        # Phase 1 (project states — no persisted data)
├── quickstart.md        # Phase 1 validation guide
├── contracts/
│   └── not-a-project-output.md   # exact output contract
└── tasks.md             # Phase 2 (/speckit-tasks — not created here)
```

### Source Code (repository root)

```text
spectra_cli/
└── cli.py               # _say_not_a_project(): replace two remedy lines with one

tests/
├── test_check.py        # flip test_not_a_spec_kit_project_names_specify_init; exact two-line assertion
├── test_version_update.py  # `version` (and `update`) give the same remedy
└── test_uninstall.py    # `uninstall` gives the same remedy

VERSION                  # 6.2.1 → 6.2.2
```

**Structure Decision**: Edit in place. No new modules; the shared helper already guarantees one
message for all four commands.

## Complexity Tracking

Not applicable — no constitution violations.
