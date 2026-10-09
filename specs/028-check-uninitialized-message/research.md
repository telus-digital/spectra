# Research: One-Step Remedy When the Folder Is Not a Spec Kit Project

No `NEEDS CLARIFICATION` items remained after `/speckit-clarify`. The points below are verified facts
and decisions the implementation depends on.

## R1 — Does `spectra install` really cover `specify init`?

- **Decision**: Yes; recommending `spectra install` alone is accurate.
- **Rationale**: `install.check_in_specify_project()` (`spectra_cli/install.py:143`) walks up for
  `.specify/`, and when none is found asks *"Initialize Spec Kit in this folder now?"* and runs
  `specify init --here --force`. If the user declines or it fails, `ui.die` gives the manual
  `specify init` fallback — that guidance stays (FR-006).
- **Alternatives considered**: Keeping `specify init` as an "or, manually" line — rejected; it is the
  redundancy the feature removes, and the manual path is still surfaced by `install` when needed.

## R2 — Where the message lives and who calls it

- **Decision**: Change only `_say_not_a_project()` (`spectra_cli/cli.py:369`).
- **Rationale**: It is the single source for this state, called from `cmd_check`, `cmd_version`,
  `cmd_update`, and `cmd_uninstall`. One edit satisfies FR-004 by construction; return value
  `EXIT_PROJECT_STATE` is untouched (FR-005).
- **Alternatives considered**: Per-command wording (e.g. different text for `uninstall`) — rejected by
  the spec's assumption and SC-002.

## R3 — Formatting

- **Decision**: `ui.plain("  Initialize Specify and add Spectra: " + ui.bold("spectra install"))`.
- **Rationale**: Clarified answer (two-space indent), and matches `_say_not_installed`'s
  `"  Install it with: " + ui.bold(...)` idiom. `ui.bold` is a no-op without colour, so the plain text
  is byte-identical in non-TTY / `NO_COLOR` output.

## R4 — Testing exact output despite ANSI codes

- **Decision**: Assert on output with ANSI escape sequences stripped (`re.sub(r"\x1b\[[0-9;]*m", "", out)`)
  and compare the full line list.
- **Rationale**: `ui.USE_COLOR` is computed at import from the real `sys.stdout.isatty()`, so a
  developer running tests in a terminal gets coloured output even under `redirect_stdout`. Existing
  tests sidestep this with `assertIn` on unstyled fragments; an exact two-line check (SC-003) needs the
  strip.
- **Alternatives considered**: Patching `ui.BOLD`/`ui.RESET` — more fragile (constants are bound at
  import in several places); setting `NO_COLOR` — too late, already evaluated.

## R5 — Version bump

- **Decision**: `VERSION` 6.2.1 → 6.2.2, PATCH. Extension version untouched.
- **Rationale**: User-visible output change with no change to the command surface, exit codes, or
  prerequisites (SHIPPING.md Path B: MAJOR only for those). Principle VI forbids moving the extension
  channel.

## R6 — Other references to the old text

- **Decision**: Leave `specs/007-unified-version-update/contracts/cli-surface.md` as is.
- **Rationale**: Historical design artifact for a finished feature; CLAUDE.md notes older specs
  describe past states. No README, docs page, or CONTRIBUTING text quotes the message.
