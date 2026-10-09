# Research: `spectra cli version`

Spec: [spec.md](spec.md). No `NEEDS CLARIFICATION` remained after `/speckit-clarify`; these are the
design decisions the plan rests on, each grounded in the code as it stands at CLI 6.3.0.

## R1 — Reuse `version.check_update()` unchanged

- **Decision**: The handler calls `version.check_update()` and branches on its `status`
  (`up_to_date` / `update_available` / `ahead` / `latest_unknown`). No change to `version.py`.
- **Rationale**: FR-011 requires the same release source and comparison as `spectra cli update`,
  `spectra version`, and the start-of-run nudge. `check_update()` is already the single function behind
  `cmd_cli_update` and `passive_check()`; `health.py`'s `spectra` row reads the same resolver. Calling it
  directly makes disagreement impossible by construction.
- **Alternatives**: Calling `passive_check()` — rejected: it collapses every non-update outcome to
  `None`, losing the distinction between "latest", "ahead", and "could not check" that FR-004/FR-008 need.

## R2 — Honour the update-check opt-outs (clarified)

- **Decision**: When `_update_check_disabled(args)` is true, the handler makes no network call: it prints
  the installed version and says the check was skipped. Exit 0.
- **Rationale**: Clarification Q3. Matches `spectra version`, whose `_skip_network()` is the same helper.
  This deliberately differs from `cmd_cli_update`, which ignores the opt-out because it cannot do its job
  offline; a version check can still answer half the question.
- **Alternatives**: Ignore the opt-out like `cli update` — rejected in clarification.

## R3 — Exit 0 for every delivered answer (clarified)

- **Decision**: `EXIT_OK` for latest, ahead, update available, unreachable, skipped, and installed-unknown.
  The handler has no non-zero path of its own; argparse usage errors stay `EXIT_USAGE`.
- **Rationale**: Clarification Q2; mirrors `cmd_version`'s documented rule ("the command was asked a
  question and answered it"). `EXIT_UNREACHABLE` is for commands asked to *act* (`cli update`).

## R4 — Classify the install only when an update exists

- **Decision**: Call `version.classify_uninstall()` only on `update_available`, then choose the next-step
  line: `UV_MANAGED` → `spectra cli update`; `NOT_INSTALLED` / `PIP_OR_SOURCE` → the same "pull / reinstall"
  hint `cmd_cli_update` prints; `UNKNOWN_UV_ABSENT` → the same pinned manual `uv tool install …` command.
- **Rationale**: FR-007 / SC-002 — the advice must work for this install. `classify_uninstall()` may spawn
  `uv tool list`; ordering it after the version check (as `cmd_cli_update` does, its R2) keeps the common
  "latest" path free of subprocesses. The hint strings are factored into one small helper shared with
  `cmd_cli_update`, so the two commands can never give different advice for the same install.
- **Alternatives**: Always print `spectra cli update` — rejected: for a pip/source install that command
  only says it cannot help, so `cli version` would point at a dead end.

## R5 — Installed version unknown

- **Decision**: If `read_installed_version()` returns `None`, say the installed version could not be
  determined, name the newest release if it was resolved, and make no up-to-date / out-of-date claim.
- **Rationale**: `compare_versions()` sorts an unknown below any real version, so `check_update()` would
  report `update_available` — a claim the spec forbids (edge case, SC-004). In practice this path is rare
  because `read_installed_version()` falls back to the committed `VERSION` file, but it is cheap to guard.

## R6 — Un-retire, and delete the retirement machinery

- **Decision**: `cli version` moves into `TOOL_COMMANDS` (first row). With nothing left retired,
  `RETIRED_TOOL_SUBCOMMANDS`, `RETIRED_TOOL_SUBCOMMAND_NAMES`, `_report_retired_subcommand`, and the
  parser's retired-registration loop are removed rather than left as empty scaffolding.
- **Rationale**: Dead code paths with empty tables are a trap for the next reader; the 5.0.0 removed-flag
  mechanism (`REMOVED_FLAGS`) is a separate, still-live path and is untouched. If a subcommand is retired
  again later, the pattern is in git history and in spec 029's plan.
- **Alternatives**: Keep the machinery with empty tables — rejected as above.

## R7 — No splash, no nudge

- **Decision**: The handler prints no banner and never calls `_start_of_run_update_nudge`.
- **Rationale**: FR-010 forbids the nudge; it would also duplicate the answer. `cmd_cli_update` sets the
  precedent of no splash for tool commands. Bare `spectra` keeps its `cli vX.Y.Z` banner untouched
  (Principle VI MUST).

## R8 — CI step that asserts retirement must be rewritten

- **Decision**: `.github/workflows/ci.yml` step "The retired cli subcommand names its replacement; the tool
  commands survive" currently *fails* if `spectra cli version` succeeds. It becomes a step asserting that
  `spectra cli version` (with `SPECTRA_NO_UPDATE_CHECK=1`, so it is offline and deterministic) exits 0
  from an empty non-project directory, prints the committed `VERSION`, never says "not a Spec Kit project"
  or "retired", writes nothing, and that `spectra cli` advertises `version`, `update`, and `uninstall`.
- **Rationale**: Without this the change cannot ship — `main` is gated on CI. Only the **step** name
  changes; the **job** name (`CLI installs and runs`), which the ruleset matches literally (SHIPPING.md),
  is untouched, so `tests/test_ci_contract.py` and the ruleset are unaffected.
- **Bonus**: the offline `cli version` output becomes a second, more direct witness to the
  installed-vs-`VERSION` parity the banner check already enforces. The banner check stays — Principle VI
  makes the banner line a MUST independently of this command.

## R9 — Removed `--version` flag message: unchanged

- **Decision**: `REMOVED_FLAGS["--version"]` keeps naming only `spectra version`.
- **Rationale**: Out of the spec's scope; the 5.0.0 messages are covered by their own tests and CI step.
  Noted for the user as a possible follow-up, since `--version` historically reported the tool itself and
  `REMOVED_FLAGS` already supports a two-replacement form (`--uninstall`).
- **Consequence**: `test_no_removed_flag_points_at_a_retired_command` loses its premise (`cli version` is
  no longer retired) and is deleted or rewritten to assert the replacement named is a live command.

## R10 — Version bump

- **Decision**: `VERSION` 6.3.0 → 6.4.0 (MINOR — a command is added). CLI channel only (Principle VI).
