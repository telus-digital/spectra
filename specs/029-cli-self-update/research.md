# Research: Update the spectra Command From Anywhere

All decisions below are grounded in the current code (`spectra_cli/cli.py`, `spectra_cli/version.py`,
`spectra_cli/health.py`, `spectra_cli/exits.py`) and the clarified spec. No external research was
needed; nothing in Technical Context was left as NEEDS CLARIFICATION.

## R1 · Which update machinery to reuse

- **Decision**: Build `cmd_cli_update` directly on `version.check_update()` and
  `version.perform_update(tag)` — the same pair `health.get_spectra_cli_status()` /
  `health._update_spectra_cli()` and the start-of-run nudge already call.
- **Rationale**: Spec assumption — the three paths can never disagree about "newest" or about how an
  update is performed. `check_update()` already returns `up_to_date | update_available | ahead |
  latest_unknown`, which maps one-to-one onto the spec's outcomes. `perform_update()` already produces
  the manual-command and Windows fresh-shell text FR-009 requires.
- **Alternatives considered**: Calling `health.check_all()` and filtering to the CLI component —
  rejected: `check_all` needs a project state and probes the Spec Kit CLI and integrations, which
  FR-002/FR-003 forbid. Calling `health.get_spectra_cli_status()` alone — workable, but it honours
  `skip_network` (FR-011 says this command must not) and wraps the result in `ComponentStatus` for no
  gain.

## R2 · Order of checks: version first, install kind second

- **Decision**: (1) `check_update()`; stop on unknown / current / ahead. (2) Only when an update is
  available, `version.classify_uninstall()` to learn the install kind; stop if not uv-managed or uv is
  absent. (3) Show plan, confirm, `perform_update(latest)`.
- **Rationale**:
  - When nothing needs doing, the command never spawns `uv tool list` — the common case stays a single
    network call.
  - The manual command printed when uv is missing must pin a **release tag**
    (`uv tool install spectra-cli --from git+…@<tag> --force`). An untagged source would install
    `main`, which is not a release. Knowing the tag requires the version check to have run first.
  - "Already up to date" from a source checkout is still a true statement (the source tree's `VERSION`
    is compared), so checking first does not mislead.
- **Alternatives considered**: Classify first (mirroring `cmd_cli_uninstall`) — rejected for the
  untagged-manual-command problem above, and because it adds a subprocess to every no-op run.

## R3 · Exit codes

Mapped onto the published contract in `spectra_cli/exits.py`:

| Outcome | Code | Precedent |
| --- | --- | --- |
| Updated | `0` EXIT_OK | — |
| Already current, or installed is newer (`ahead`) | `0` EXIT_OK | `spectra update` "Everything is up to date." |
| Newest release could not be determined | `3` EXIT_UNREACHABLE | FR-007 |
| User answered no | `1` EXIT_DECLINED | `spectra update` |
| Non-interactive, no `--yes` | `1` EXIT_DECLINED | `spectra update` (`_confirm_updates` → "Nothing was changed.") |
| Not uv-managed (source checkout / pip) | `0` EXIT_OK | `cmd_cli_uninstall`; exits.py "abstention with a stated reason returns 0" |
| uv not on PATH | `4` EXIT_DELEGATION | `cmd_cli_uninstall` |
| `uv` ran and failed | `4` EXIT_DELEGATION | `cmd_cli_uninstall` |

- **Decision on the non-interactive case**: `1`, as `spectra update` returns, not `2` as
  `spectra cli uninstall` returns. The spec said "the same code the other confirm-gated commands use",
  but those two disagree; `spectra update` is the sibling verb a user (and a script) will compare this
  with, and refusing to act for want of consent is "declined", not a usage error. The spec edge case is
  amended to name the code.

## R4 · `--no-update-check` / `SPECTRA_NO_UPDATE_CHECK`

- **Decision**: `cmd_cli_update` ignores both. It does not call `_update_check_disabled()`.
- **Rationale**: FR-011 — the flag opts out of *unasked-for* network traffic; this command is the ask.
  The start-of-run nudge is only invoked from `cmd_install`, so it cannot fire here; no change needed.
- **Alternative rejected**: Honouring the flag and printing "check skipped" — a command whose only job
  is the check would then do nothing at all, silently, in CI environments that set the variable
  globally.

## R5 · Un-retiring the subcommand in the parser and dispatch table

- **Decision**:
  - `TOOL_COMMANDS` becomes `[("cli update", …), ("cli uninstall", …)]` (update first, FR-012). The
    existing loop in `build_parser()` registers it, so no parser code changes.
  - `RETIRED_TOOL_SUBCOMMAND_NAMES = ("version",)` and `RETIRED_TOOL_SUBCOMMANDS = {"version": …}`.
  - `TOOL_DISPATCH["update"]` points at the new `cmd_cli_update`; the retirement stub of the same name
    is replaced.
  - Module docstring and the comment block above the retired handlers are rewritten so they no longer
    claim `cli update` is retired.
- **Rationale**: The table-driven surface means help, parser, and dispatch all follow from the two
  lists; `cli version` keeps its named-replacement behaviour (FR-014).

## R6 · Help copy

- **Decision**:
  - `--help` row: `cli update` — "Update the spectra command itself to the newest release. Works from
    any folder; never touches the agents in your projects."
  - `spectra cli` intro (FR-013): "Manage the spectra command itself. These work from any folder. To
    check or update your whole stack — Spec Kit, the core agents, and your agents too — use
    `spectra version` and `spectra update` (see `spectra --help`)."
- **Rationale**: Each sentence answers one of the spec's acceptance checks (US3-AS2): what it updates,
  where it works, what it leaves alone. The group intro no longer implies the tool can only be updated
  from the top level.

## R7 · Pointer line from `spectra update` outside a project (FR-016)

- **Decision**: `cmd_update` keeps calling `_say_not_a_project()` and then prints one extra line
  before returning its code:
  `  Update just the spectra command: spectra cli update` — two-space indent and `Label: command`
  shape, matching the remedy line above it. `_say_not_a_project()` itself is unchanged, so `check`,
  `version`, and `uninstall` keep feature 028's exact two-line output.
- **Rationale**: Smallest change; the shared helper stays the single source of the shared lines.
- **Alternative rejected**: A `hint=` parameter on `_say_not_a_project()` — an argument used by one
  caller is indirection without reuse.

## R8 · The removed `--update` flag's message

- **Decision**: Unchanged — it keeps naming `spectra update` only.
- **Rationale**: `--update` was always the whole-stack update by the 6.0.0 reading; adding a second
  candidate is a separate surface change the spec did not ask for. The test
  `test_no_removed_flag_points_at_a_retired_command` stays green as-is (its output still contains no
  `spectra cli update`); its `cli update` assertion is dropped because that command is no longer
  retired, so the assertion's stated reason would be false.

## R9 · Versioning and documentation (Principle VI)

- **Decision**: CLI channel only. `VERSION` 6.2.2 → **6.3.0** (MINOR: a command is added to the
  surface; nothing existing breaks — `cli update` previously only printed a retirement error and
  exited 2). `spectra/extension.yml`, `catalog.json`, `docs/packages/spectra.zip`, and
  `agents-list.json` MUST NOT change.
- **Docs touched** (FR-017):
  - `README.md` — the "Managing the tool itself" block (~L397) gains `spectra cli update`; the
    "Changed in 6.0.0" note gains a "Changed in 6.3.0" note above it; the Two release channels table's
    "You update it with" cell for the CLI names `spectra cli update` as the from-anywhere option.
  - `docs/index.html` — the "Keep the whole stack current" step adds `spectra cli update` and a
    "Changed in 6.3.0" sentence; the 6.0.0 sentence is reworded so it no longer reads as current.
- **Rationale**: Bare `spectra`'s `cli vX.Y.Z` banner is untouched, so the CI/release/clean-room
  checks Principle VI names keep working.
