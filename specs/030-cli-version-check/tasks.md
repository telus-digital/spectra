---

description: "Task list for 030 — Check the spectra Command's Version From Anywhere"
---

# Tasks: Check the spectra Command's Version From Anywhere

**Input**: Design documents from `specs/030-cli-version-check/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts/cli-version-command.md](contracts/cli-version-command.md),
[quickstart.md](quickstart.md)

**Tests**: Requested — FR-017 lists the outcomes the suite must cover. Stdlib `unittest` only; run with
`python3 -m unittest discover -s tests`. Mock `spectra_cli.version.check_update`,
`spectra_cli.version.classify_uninstall`, `spectra_cli.version.read_installed_version`,
`spectra_cli.version.resolve_latest`, and `ui.confirm`; never hit the network or spawn `uv`. Drive the CLI
through `cli.main(argv)` with stdout captured, as the `run()` helper and `release()` context manager in
`tests/test_cli_update.py` do, and use `helpers.plain_lines()` / `helpers.cwd()` /
`helpers.temp_project()` / `helpers.NOT_A_PROJECT_LINES` from `tests/helpers.py`.

**Organization**: Grouped by user story. US1 and US2 are both P1 and share one handler, so US2 is
verification of the isolation US1's handler must already have.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: US1–US4, from spec.md

---

## Phase 1: Setup

**Purpose**: Version bump for the CLI channel (Principle VI, research R10).

- [X] T001 Bump `VERSION` from `6.3.0` to `6.4.0` (MINOR — a command is added). Do NOT touch `spectra/extension.yml`, `catalog.json`, `agents-list.json`, or `docs/packages/spectra.zip`.

---

## Phase 2: Foundational (un-retire the subcommand)

**Purpose**: Remove the retirement path so `cli version` can dispatch to a real handler (research R6).
Blocks every user story.

- [X] T002 In `spectra_cli/cli.py`, delete `RETIRED_TOOL_SUBCOMMAND_NAMES`, `RETIRED_TOOL_SUBCOMMANDS`, `_report_retired_subcommand`, the "Retired tool subcommands" section comment, and the `for name in RETIRED_TOOL_SUBCOMMAND_NAMES` registration loop (plus its comment) in `build_parser()`. Leave `REMOVED_FLAGS` / `_report_removed_flag` (the 5.0.0 flag path) untouched.
- [X] T003 In `spectra_cli/cli.py`, add `("cli version", "Show the spectra command's version and whether a newer release exists. Works from any folder; never checks the agents.")` as the **first** row of `TOOL_COMMANDS` (before `cli update`), so the parser loop registers it and both help panels list it (contract "Help copy"). Update the `TOOL_DISPATCH` comment, which currently says `version` points at a retirement handler.
- [X] T004 In `spectra_cli/cli.py`, extract the not-updatable advice from `cmd_cli_update` into a helper `_not_updatable_hint(kind, latest)` that prints the lines for `version.NOT_INSTALLED` / `version.PIP_OR_SOURCE` (the "Source checkout: pull the latest changes. pip install: reinstall with the tool you used." hint) and `version.UNKNOWN_UV_ABSENT` (the pinned `uv tool install {version.DIST_NAME} --from '{version.git_source(latest)}' --force` command). `cmd_cli_update` calls it; its output, return codes, and lead lines must be byte-identical to today. Run `python3 -m unittest tests.test_cli_update` — it must pass with no test edits (plan "Shared hint").

**Checkpoint**: `spectra cli version` parses and dispatches; `cli update` unchanged.

---

## Phase 3: User Story 1 — Check the command's version from any folder (Priority: P1) 🎯 MVP

**Goal**: `spectra cli version` reports the installed version and latest / update-available from any
folder, naming `spectra cli update` when an update exists.

**Independent Test**: From a temp folder with no `.specify/` above it, run `cli version` with the release
mocked current and then behind; read the output (spec US1).

### Tests for User Story 1

- [X] T005 [P] [US1] Create `tests/test_cli_version.py` with module docstring (spec 030, contract path), `run(argv)`, and a `release(status, installed, latest, *, kind)` context manager modelled on `tests/test_cli_update.py` that patches `version.check_update`, `version.classify_uninstall`, `version.perform_update`, and `ui.confirm`, yielding the mocks. Base class `_InEmptyFolder` runs each test from a fresh temp dir with no `.specify/` above it.
- [X] T006 [US1] In `tests/test_cli_version.py`, add one test per outcome in `data-model.md` rows 2 and 4–8, each asserting exit `0` and the facts in `contracts/cli-version-command.md`: LATEST names `<installed>` and "latest" and does NOT contain `spectra cli update`; AHEAD names both versions, says latest, never "update"/"available"; UPDATE_AVAILABLE (`UV_MANAGED`) names both versions and `spectra cli update`; UPDATE_AVAILABLE_NOT_UV (`PIP_OR_SOURCE` and `NOT_INSTALLED`) names the pull/reinstall hint and does NOT tell the user to run `spectra cli update` as the fix; UPDATE_AVAILABLE_NO_UV (`UNKNOWN_UV_ABSENT`) prints the pinned `uv tool install` command containing `@<latest>`; UNREACHABLE (`latest_unknown`) names `<installed>`, says it could not be checked, and contains neither "latest" nor "available".
- [X] T007 [US1] In `tests/test_cli_version.py`, add: INSTALLED_UNKNOWN (`read_installed_version` → `None`, `check_update` → `update_available`) says the installed version could not be determined and does not say "available" or name `spectra cli update` (data-model row 3); `classify_uninstall` is NOT called for LATEST, AHEAD, or UNREACHABLE; `perform_update` and `ui.confirm` are never called in any outcome (FR-006); output never contains "not a Spec Kit project" or "retired"; the temp folder is still empty afterwards; `cli version --yes` behaves identically.

### Implementation for User Story 1

- [X] T008 [US1] In `spectra_cli/cli.py`, replace the `cmd_cli_version` retirement stub with the real handler under a `# cli version (the tool reports on itself)` section placed before `cmd_cli_update`. Resolution order exactly as `data-model.md`: (1) `_update_check_disabled(args)` → SKIPPED line, return `EXIT_OK` without calling `version.check_update`; (2) `check_update()` status `latest_unknown` → UNREACHABLE; (3) installed `None` → INSTALLED_UNKNOWN; (4) `up_to_date` → LATEST; (5) `ahead` → AHEAD; (6–8) `update_available` → lead line, then `version.classify_uninstall()`: `UV_MANAGED` → `"  Update it with: " + ui.bold("spectra cli update")`, else the not-uv lead line plus `_not_updatable_hint(kind, latest)`. Every path returns `EXIT_OK`. No splash, no nudge, no prompt. Docstring cites spec 030 and explains why it honours the opt-out and exits 0 when `cmd_cli_update` does neither (research R2/R3).
- [X] T009 [US1] Run `python3 -m unittest tests.test_cli_version` until green.

**Checkpoint**: MVP — `spectra cli version` works from any folder.

---

## Phase 4: User Story 2 — Check only the command, even inside a project (Priority: P1)

**Goal**: Prove the handler never looks at the project or the other three components.

**Independent Test**: In a temp project in each state, output equals the no-project output and the tree is
unchanged (spec US2).

### Tests for User Story 2

- [X] T010 [P] [US2] In `tests/test_cli_version.py`, add class `InsideAProject`: for each of `h.temp_project()` (installed), `h.temp_project(installed_version=None)` (not installed), and `h.temp_project(incomplete=True)`, run `cli version` with the release mocked `update_available` and assert the output equals the same run from an empty folder, exit is `0` (never `EXIT_PROJECT_STATE`), and a recursive snapshot of the project's files (paths + bytes) is identical before and after.
- [X] T011 [P] [US2] In `tests/test_cli_version.py`, add a test that patches `project.classify`, `health.check_all`, `extension.delegate_update`, and `coverage` entry points used by `cmd_update` to raise `AssertionError`, then runs `cli version` in every outcome and asserts it still returns `0` — isolation by construction (FR-002/FR-003). Assert the output never mentions "Spec Kit CLI", "core agents", or "agents installed".
- [X] T012 [US2] In `tests/test_cli_version.py`, add class `OptOuts` (FR-010): with `--no-update-check` (before and after the subcommand) and separately with `SPECTRA_NO_UPDATE_CHECK=1`, patch `version.resolve_latest` and `version.check_update` and assert neither is called, the output names `<installed>` and "skipped", contains neither "latest" nor "available", and exit is `0`. Also assert `version.passive_check` is never called by `cli version` in any mode (no start-of-run nudge).

**Checkpoint**: Isolation and opt-out behaviour proven.

---

## Phase 5: User Story 3 — Discover the command from help (Priority: P2)

**Goal**: `cli version` appears first in both Tool commands panels; retirement tests replaced.

**Independent Test**: `spectra --help` and `spectra cli` list it (spec US3).

- [X] T013 [P] [US3] In `tests/test_cli_surface.py`, delete class `RetiredToolSubcommands` entirely. In `TheToolGroup`, rename `test_update_and_uninstall_are_the_tool_commands` to `test_version_update_and_uninstall_are_the_tool_commands` asserting `["cli version", "cli update", "cli uninstall"]` with a docstring citing spec 030; update `test_every_tool_handler_takes_one_argument`'s docstring (no retirement handler remains). Rewrite `RemovedFlags.test_no_removed_flag_points_at_a_retired_command` to assert every replacement named in `cli.REMOVED_FLAGS` is a live command (a `PROJECT_COMMANDS` name or a `TOOL_COMMANDS` label) — research R9.
- [X] T014 [P] [US3] In `tests/test_cli_version.py`, add class `Help`: `spectra --help` output's Tool commands panel lists `cli version` before `cli update` before `cli uninstall`; the `cli version` description contains "any folder" and "never checks the agents"; `spectra cli` (exit `EXIT_USAGE`) lists `version`, `update`, `uninstall`; `spectra cli version --force` is a usage error (exit `2`).
- [X] T015 [US3] In `spectra_cli/cli.py`, update the module docstring: surface diagram line becomes `spectra cli version | update | uninstall`; the 6.0.0 paragraph no longer says `cli version` "remains registered so typing it names its replacement"; add a 6.4.0 paragraph saying `cli version` returned as a tool-only, read-only check from any folder, the partner to 6.3.0's `cli update`. Update `print_cli_group_help`'s docstring ("Two rows" → three). Leave the bare-`spectra` banner paragraph intact (Principle VI).

**Checkpoint**: Help and surface tests green.

---

## Phase 6: User Story 4 — Point the stuck user at the new command (Priority: P3)

**Goal**: `spectra version` outside a project adds one pointer line (clarification Q1).

**Independent Test**: `spectra version` in an empty folder shows three lines and exits 5 (spec US4).

- [X] T016 [US4] In `spectra_cli/cli.py` `cmd_version`, replace `return _say_not_a_project()` with `code = _say_not_a_project()` followed by `ui.plain("  Check just the spectra command: " + ui.bold("spectra cli version"))` and `return code`, mirroring `cmd_update`'s pattern. `cmd_check` and `cmd_uninstall` are not touched.
- [X] T017 [US4] In `tests/test_version_update.py`: in `CannotAnswer.test_not_a_project_exits_five_and_says_something_different`, change the tail assertion to `h.plain_lines(out)[-3:] == list(h.NOT_A_PROJECT_LINES) + ["  Check just the spectra command: spectra cli version"]`; in `BadStates.test_only_update_points_at_cli_update_outside_a_project`, keep the `assertNotIn("spectra cli update", out)` and update its docstring (version now has its own pointer, spec 030 FR-015); update the docstring of `Verdicts.test_the_retired_tool_command_is_no_longer_advertised` (in-project `spectra version` still does not advertise `cli version`, but it is no longer retired) and rename it `test_in_project_version_does_not_advertise_cli_version`. Confirm `tests/test_check.py` and `tests/test_uninstall.py` not-a-project assertions still pass unchanged.

**Checkpoint**: All four stories complete.

---

## Phase 7: Polish & Cross-Cutting

- [X] T018 Rewrite the step "The retired cli subcommand names its replacement; the tool commands survive" in `.github/workflows/ci.yml` (job `CLI installs and runs` — do NOT rename the job) as "`spectra cli version` reports the committed version outside a Spec Kit project": with `SPECTRA_NO_UPDATE_CHECK: '1'`, run `spectra cli version` from a fresh `mktemp -d` capturing to a file; fail if exit is non-zero, if the output lacks the contents of `VERSION`, if it contains `not a Spec Kit project` or `retired`, or if the directory is non-empty afterwards; then keep the `spectra cli` group check, now requiring `version`, `update`, and `uninstall` and dropping the "still advertises 'cli version'" failure. Update the step comment. Also update the comment on "The command runs and reports the committed version" step that says `cli version` "was retired in 6.0.0" / "is gone". Run `python3 -m unittest tests.test_ci_contract`.
- [X] T019 [P] In `README.md`: tool-commands block (≈line 398) becomes three verbs, adding `spectra cli version    # show the spectra command's version, from any folder` first, and "takes two verbs" → "three"; add a `> **Changed in 6.4.0.**` note above the 6.3.0 one explaining `cli version` is back as a tool-only check that names `spectra cli update` when newer; fix the 6.0.0 note so it no longer says `cli version` "is still retired"; add a "You check it with" row to the release-channels table (≈line 519): `spectra cli version` from any folder, or `spectra version` in a project | `spectra version`.
- [X] T020 [P] In `docs/index.html` (≈line 521): add `<pre><code>spectra cli version     # check just the command, from any folder</code></pre>` before the `cli update` line; prepend a "Changed in 6.4.0" sentence to the `.os` aside; fix the 6.0.0 sentence's parenthetical to say both returned (`cli update` in 6.3.0, `cli version` in 6.4.0).
- [X] T021 Grep the repo (excluding `specs/0[0-2]*`) for `cli version` and `retired` and fix any remaining claim that `spectra cli version` is retired — including `CONTRIBUTING.md`, `SHIPPING.md`, and `spectra_cli/*.py` comments.
- [X] T022 Run `python3 -m unittest discover -s tests` and `python3 tools/generate_agent_docs.py --check`; then `python3 tools/ship.py --dry-run`. All must pass.
- [X] T023 Walk [quickstart.md](quickstart.md) steps 1, 2, 4, 5, 6 against the working copy (`python3 -m spectra_cli.cli …` or a local `uv tool install --from . spectra-cli --force`) and confirm each expected outcome; mark spec Status `Implemented`.

---

## Dependencies & Execution Order

- **T001** independent.
- **T002 → T003 → T004** (same file, sequential). Block all stories.
- **US1**: T005 ∥ (T002–T004 done) → T006 → T007 → T008 → T009.
- **US2**: needs T008. T010 ∥ T011, then T012 (same file as T010/T011 — run after them if editing serially).
- **US3**: needs T003. T013 ∥ T014 (different files), then T015.
- **US4**: independent of US1–US3 code-wise (only `cmd_version`); T016 → T017.
- **Polish**: T018 needs T008 (CI asserts the new behaviour). T019 ∥ T020. T021 after T015/T019/T020. T022 after everything. T023 last.

### Parallel examples

```text
# After Phase 2:
T005 (tests/test_cli_version.py scaffold)  ∥  T013 (tests/test_cli_surface.py)  ∥  T016 (cmd_version pointer)

# Polish:
T019 (README.md)  ∥  T020 (docs/index.html)
```

## Implementation Strategy

**MVP** = Phases 1–3 (T001–T009): the command exists and answers correctly from any folder. US2 adds the
proof of isolation, US3 the discoverability and stale-test cleanup, US4 the pointer. Phase 7's CI rewrite
(T018) is mandatory before shipping — without it `main` rejects the push (research R8). Ship with
`python3 tools/ship.py`, then tag `6.4.0` per SHIPPING.md Path B.
