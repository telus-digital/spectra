# Implementation Plan: Check the spectra Command's Version From Anywhere

**Branch**: `030-cli-version-check` | **Date**: 2026-10-08 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/030-cli-version-check/spec.md`

## Summary

Reinstate `spectra cli version`, retired in 6.0.0, as a read-only, location-independent report on the
`spectra` command alone: its installed version, and whether a newer release exists — naming
`spectra cli update` when one does. The new `cmd_cli_version` in `spectra_cli/cli.py` replaces the
retirement stub and reuses `version.check_update()` (the same resolver `cli update`, `spectra version`,
and the nudge use) and, only when an update exists, `version.classify_uninstall()` so the next step it
names actually works for this install. It honours `--no-update-check` (offline report) and exits 0 for
every answer, like `spectra version`. With nothing left retired, the retirement machinery is deleted.
`spectra version` outside a project gains one pointer line. A CI step that asserts `cli version` is
retired is rewritten. CLI channel only: `VERSION` 6.3.0 → 6.4.0.

## Technical Context

**Language/Version**: Python 3.9+ (stdlib only — the `spectra_cli/` package; CI runs 3.9 and 3.12)

**Primary Dependencies**: None (zero-dependency constraint). May spawn `uv tool list` via the existing
`classify_uninstall()`, only on the update-available path.

**Storage**: N/A

**Testing**: stdlib `unittest` — `python3 -m unittest discover -s tests`; network and `uv` mocked via
`unittest.mock` on `spectra_cli.version`

**Target Platform**: macOS / Linux / Windows terminals; `uv tool` install (pip/source handled)

**Project Type**: CLI

**Performance Goals**: The "latest" path makes one release lookup and spawns nothing; the opted-out path
makes no network request at all.

**Constraints**: Must not read or write the working directory or classify a project; output identical
with and without ANSI styling; never prompts; exit-code contract in `spectra_cli/exits.py` unchanged.

**Scale/Scope**: One handler (~40 lines) replacing a stub, one small shared hint helper, deletions of the
retirement scaffolding, one extra line in `cmd_version`, one new test module, edits to two existing test
modules, one CI step, README + landing-page copy.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Applies? | Status |
| --- | --- | --- |
| I. Spec-driven development | Yes | ✅ specify → clarify (3 Qs) → plan → tasks → implement on `030-cli-version-check`. |
| II. Single self-contained extension | No — `spectra/` untouched | ✅ |
| III. Agent-agnostic commands | No — no command files touched | ✅ |
| IV. Context-aware by default | No — no agent behaviour changes | ✅ |
| V. Catalog and package in sync | No — nothing under `spectra/` changes; `extension.yml`, `CHANGELOG.md`, `agents-list.json`, `catalog.json`, `spectra.zip` stay put. `docs/index.html` edited for CLI copy only. | ✅ |
| VI. Independent release channels | Yes — CLI channel only | ✅ `VERSION` 6.3.0 → 6.4.0 (MINOR: command added). Extension/catalog MUST NOT bump. Release resolution still via `/releases/latest`, so tags stay CLI-only. **Bare `spectra`'s `cli vX.Y.Z` banner is untouched** — the MUST stands; the CI banner check, release smoke test, and clean-room check keep using it. `cli version` becomes an additional out-of-project witness, not a replacement. |
| VII / VIII. Artifact root, templates | No — no document deliverables | ✅ |
| Landing on `main` | Yes | ✅ `python3 tools/ship.py`, then tag `6.4.0` (SHIPPING.md Path B). Never `git push origin main`. The CI change edits a **step** in job `CLI installs and runs`; the job name the ruleset matches is unchanged (research R8). |

**Result**: PASS. No violations; Complexity Tracking not needed.

**Post-design re-check**: PASS — Phase 1 touches only `spectra_cli/cli.py`, `tests/`,
`.github/workflows/ci.yml` (one step body), `VERSION`, `README.md`, `docs/index.html`, and this spec
directory. No new module, no new dependency, no change to `version.py`. Principle VI's prose ("`spectra
version` … cannot answer 'what version is this command?' from an arbitrary directory") remains true and
needs no amendment; it could optionally gain a mention of `cli version` later.

## Project Structure

### Documentation (this feature)

```text
specs/030-cli-version-check/
├── plan.md              # This file
├── research.md          # Phase 0 — decisions R1–R10
├── data-model.md        # Phase 1 — inputs and the outcome resolution table
├── quickstart.md        # Phase 1 — validation guide
├── contracts/
│   └── cli-version-command.md   # invocation, output per outcome, exit codes, help copy
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 (/speckit-tasks — not created here)
```

### Source Code (repository root)

```text
spectra_cli/
└── cli.py               # module docstring (6.4.0 paragraph; surface diagram `cli version | update | uninstall`);
                         # TOOL_COMMANDS gains "cli version" (first);
                         # DELETE RETIRED_TOOL_SUBCOMMAND_NAMES, RETIRED_TOOL_SUBCOMMANDS,
                         #        _report_retired_subcommand, the parser's retired loop;
                         # cmd_cli_version replaces the stub (outcome table in data-model.md);
                         # _not_updatable_hint(kind, latest) shared by cmd_cli_version and cmd_cli_update;
                         # TOOL_DISPATCH comment; cmd_version pointer line after _say_not_a_project()

tests/
├── test_cli_version.py  # NEW — every data-model outcome, cwd/project isolation, opt-outs make no
│                        #       network call, never prompts/updates, --force rejected, help rows
├── test_cli_surface.py  # DELETE RetiredToolSubcommands; tool-command order → version, update, uninstall;
│                        # rewrite test_no_removed_flag_points_at_a_retired_command (R9)
├── test_cli_update.py   # still green after the hint helper is factored out (no expectation changes)
└── test_version_update.py  # `spectra version` not-a-project: three lines incl. pointer;
                            # docstring of test_the_retired_tool_command_is_no_longer_advertised
tests/test_check.py         # (unchanged) `check` keeps exactly two lines — guards FR-015's scope

.github/workflows/ci.yml # rewrite step "The retired cli subcommand names its replacement…" (R8)
VERSION                  # 6.3.0 → 6.4.0
README.md                # tool-commands block, "Changed in 6.4.0" note, fix the 6.0.0 note, channels table
docs/index.html          # tool-commands snippet + 6.4.0 note; fix "cli update returned in 6.3.0" aside
```

**Structure Decision**: Single existing package. The handler sits next to `cmd_cli_update` and
`cmd_cli_uninstall` in `cli.py` and calls existing `version.py` functions; ~40 lines does not warrant a
module.

## Implementation Notes

- **Isolation (FR-002/FR-003)**: `cmd_cli_version` never calls `project.classify()`, `health.*`,
  `extension.*`, or `coverage.*`. Tests patch `project.classify` and `health.check_all` to raise and run
  from a temp dir containing `.specify/`, asserting identical output and no file changes.
- **Opt-out (FR-010)**: `if _update_check_disabled(args)` is the first branch; a test asserts
  `version.resolve_latest` / `check_update` are not called.
- **Order matters** (data-model): opted-out → unreachable → installed-unknown → compare. Do not call
  `classify_uninstall()` before knowing an update exists.
- **Shared hint**: extracting the not-uv / no-uv strings from `cmd_cli_update` into one helper is a pure
  refactor; `test_cli_update.py` must pass unchanged — that is the proof.
- **Pointer (FR-015)**: in `cmd_version`, mirror `cmd_update`'s pattern at `cli.py` around line 1084:
  `code = _say_not_a_project(); ui.plain("  Check just the spectra command: " + ui.bold("spectra cli version"))`.
- **CI**: the rewritten step runs with `SPECTRA_NO_UPDATE_CHECK=1` so it is deterministic and offline,
  and greps for the committed `VERSION` in the output.

## Complexity Tracking

No constitution violations to justify.
