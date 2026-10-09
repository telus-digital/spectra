# Implementation Plan: Update the spectra Command From Anywhere

**Branch**: `029-cli-self-update` | **Date**: 2026-10-08 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/029-cli-self-update/spec.md`

## Summary

Reinstate `spectra cli update`, retired in 6.0.0, with a narrower meaning: update **only** the `spectra`
command, from any folder, without classifying the project or touching any other component. The new
`cmd_cli_update` in `spectra_cli/cli.py` reuses `version.check_update()` and `version.perform_update()`
— the same pair `spectra update` and the start-of-run nudge use — and `version.classify_uninstall()` to
refuse cleanly when it is not a uv tool. It confirms like `spectra update` (prompt, `--yes`, refuse when
non-interactive). Moving the row from the retired list into `TOOL_COMMANDS` puts it in both help
panels. `spectra update` outside a project gains one pointer line. CLI channel only: `VERSION`
6.2.2 → 6.3.0.

## Technical Context

**Language/Version**: Python 3.9+ (stdlib only — the `spectra_cli/` package; CI runs 3.9 and 3.12)

**Primary Dependencies**: None (zero-dependency constraint). Delegates to `uv` at run time, as today.

**Storage**: N/A

**Testing**: stdlib `unittest` — `python3 -m unittest discover -s tests`; network and `uv` mocked via
`unittest.mock` on `spectra_cli.version`

**Target Platform**: macOS / Linux / Windows terminals; `uv tool` install

**Project Type**: CLI

**Performance Goals**: The no-op path ("already up to date") makes one release lookup and spawns no
subprocess (research R2).

**Constraints**: Must not read or write the working directory; output identical with and without ANSI
styling (`NO_COLOR`, non-TTY); existing exit-code contract in `spectra_cli/exits.py`.

**Scale/Scope**: One new handler (~50 lines), list/dict edits in `cli.py`, one extra line in
`cmd_update`, one new test module, edits to one existing test module, README + landing page copy.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Applies? | Status |
| --- | --- | --- |
| I. Spec-driven development | Yes | ✅ spec → clarify → plan → tasks → implement on `029-cli-self-update`. |
| II. Single self-contained extension | No — `spectra/` untouched | ✅ |
| III. Agent-agnostic commands | No — no command files touched | ✅ |
| IV. Context-aware by default | No — no agent behaviour changes | ✅ |
| V. Catalog and package in sync | No — nothing under `spectra/` changes, so `extension.yml`, `CHANGELOG.md`, `agents-list.json`, `catalog.json`, `spectra.zip` stay put. `docs/index.html` is edited only for CLI copy. | ✅ |
| VI. Independent release channels | Yes — CLI channel only | ✅ `VERSION` 6.2.2 → 6.3.0 (MINOR: command added). Extension/catalog MUST NOT bump. The command reuses `/releases/latest` resolution, so tags remain CLI-only. Bare `spectra`'s `cli vX.Y.Z` banner is untouched, so the CI / release smoke / clean-room checks keep working — and `spectra cli update` now also works in the clean-room state where `spectra version` correctly refuses. |
| VII / VIII. Artifact root, templates | No — no document deliverables | ✅ |
| Landing on `main` | Yes | ✅ `python3 tools/ship.py`, then tag `6.3.0` (SHIPPING.md Path B). Never `git push origin main`. |

**Result**: PASS. No violations; Complexity Tracking not needed.

**Post-design re-check**: PASS — Phase 1 touches only `spectra_cli/cli.py`, `tests/`, `VERSION`,
`README.md`, `docs/index.html`, and this spec directory. No new module, no new dependency, no change
to `version.py`'s public functions.

## Project Structure

### Documentation (this feature)

```text
specs/029-cli-self-update/
├── plan.md              # This file
├── research.md          # Phase 0 — decisions R1–R9
├── data-model.md        # Phase 1 — inputs and the outcome state machine
├── quickstart.md        # Phase 1 — validation guide
├── contracts/
│   └── cli-update-command.md   # invocation, output per outcome, exit codes, help copy
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 (/speckit-tasks — not created here)
```

### Source Code (repository root)

```text
spectra_cli/
└── cli.py               # module docstring; TOOL_COMMANDS gains "cli update" (first);
                         # RETIRED_TOOL_SUBCOMMAND_NAMES / RETIRED_TOOL_SUBCOMMANDS → version only;
                         # new cmd_cli_update (replaces the retirement stub);
                         # print_cli_group_help intro; cmd_update pointer line after _say_not_a_project()

tests/
├── test_cli_update.py   # NEW — every outcome in the contract, cwd-independence, no project reads,
│                        #       --no-update-check ignored, --force rejected, help rows
└── test_cli_surface.py  # RetiredToolSubcommands → `version` only; drop the stale `cli update`
                         # assertion in test_no_removed_flag_points_at_a_retired_command

tests/test_version_update.py  # `spectra update` not-a-project: three lines incl. pointer
tests/test_check.py           # (unchanged) `check` keeps the exact two lines — guards FR-016's scope

VERSION                  # 6.2.2 → 6.3.0
README.md                # tool-commands block, "Changed in 6.3.0" note, release-channels table
docs/index.html          # "Keep the whole stack current" step: add `spectra cli update` + 6.3.0 note
```

**Structure Decision**: Single existing package. The handler lives in `cli.py` next to
`cmd_cli_uninstall`, its only sibling tool command, and calls existing functions in `version.py`; no
new module is warranted for ~50 lines.

## Implementation Notes

- **Isolation (FR-002/FR-003)**: `cmd_cli_update` never calls `project.classify()`, `health.*`,
  `extension.*`, or `coverage.*`. A test patches `project.classify` and `health.check_all` to raise and
  asserts the command still succeeds, and runs it from a temp dir containing a `.specify/` to show it
  is not consulted.
- **Ignoring `--no-update-check` (FR-011)**: the handler simply never calls `_update_check_disabled`.
  The flag remains parseable because `_add_shared` attaches it to every subcommand.
- **Exit codes**: see research R3 / data-model state machine.
- **Retirement tests**: `test_neither_performs_its_old_action` and
  `test_neither_reaches_the_network_or_spawns_a_subprocess` keep running for `cli version` only.

## Complexity Tracking

No constitution violations to justify.
