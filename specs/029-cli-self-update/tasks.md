---

description: "Task list for 029 — Update the spectra Command From Anywhere"
---

# Tasks: Update the spectra Command From Anywhere

**Input**: Design documents from `specs/029-cli-self-update/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts/cli-update-command.md](contracts/cli-update-command.md),
[quickstart.md](quickstart.md)

**Tests**: Requested — FR-018 lists the outcomes the suite must cover. Stdlib `unittest` only; run with
`python3 -m unittest discover -s tests`. Mock `spectra_cli.version.check_update`,
`spectra_cli.version.classify_uninstall`, `spectra_cli.version.perform_update`, and `sys.stdin.isatty`;
never hit the network or spawn `uv`. Drive the CLI through `cli.main(argv)` with stdout captured, as
the `run()` helper in `tests/test_cli_surface.py` does, and use `helpers.plain_lines()` /
`helpers.cwd()` / `helpers.temp_project()` from `tests/helpers.py`.

**Organization**: Grouped by user story. US1 and US2 are both P1 and share one handler, so US2 is
purely verification of the isolation US1's handler must already have.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: US1–US4, from spec.md

---

## Phase 1: Setup

**Purpose**: Version bump for the CLI channel (Principle VI, research R9).

- [X] T001 Bump `VERSION` from `6.2.2` to `6.3.0` (MINOR — a command is added). Do NOT touch `spectra/extension.yml`, `catalog.json`, `agents-list.json`, or `docs/packages/spectra.zip`.

---

## Phase 2: Foundational (un-retire the subcommand)

**Purpose**: Move `cli update` from the retired list to the live surface so the parser, both help panels,
and dispatch all reach a real handler. Blocks every story.

- [X] T002 In `spectra_cli/cli.py`, set `RETIRED_TOOL_SUBCOMMAND_NAMES = ("version",)` and `RETIRED_TOOL_SUBCOMMANDS = {"version": "spectra version"}`; update the comment block above `RETIRED_TOOL_SUBCOMMANDS` and the module docstring so they say only `cli version` is retired and that `cli update` was reinstated in 6.3.0 to update the command alone, from any folder (`spectra update` remains the whole-stack update). Update the surface sketch in the docstring to `spectra cli update | uninstall   the spectra command`.
- [X] T003 In `spectra_cli/cli.py`, add `("cli update", "Update the spectra command itself to the newest release. Works from any folder; never touches the agents in your projects.")` as the **first** entry of `TOOL_COMMANDS`, before `cli uninstall` (FR-012). `build_parser()`'s existing `TOOL_COMMANDS` loop registers it — no parser change. Confirm `--force` is still registered only on the `update` project subcommand.
- [X] T004 In `spectra_cli/cli.py`, replace the retirement stub `cmd_cli_update` with a placeholder that the US1 tasks fill in, and keep `TOOL_DISPATCH["update"] = cmd_cli_update`; update the comment above `TOOL_DISPATCH` so it says only `version` points at a retirement handler.

**Checkpoint**: `spectra cli update` parses and dispatches to the new handler; `spectra cli version` still prints its retirement message and exits 2.

---

## Phase 3: User Story 1 — Update the command from a folder that is not a Spec Kit project (P1) 🎯 MVP

**Goal**: `spectra cli update` finds the newest release, confirms, updates via uv, and reports — from any folder.

**Independent Test**: In a temp dir with no `.specify/` anywhere above it, run `cli update` with an older installed version mocked; accept; output names old → new and exit is 0. Never "This is not a Spec Kit project".

### Tests for User Story 1

- [X] T005 [P] [US1] Create `tests/test_cli_update.py` with a module docstring citing spec 029, a `run(argv)` helper like `tests/test_cli_surface.py`'s, and a fixture helper that patches `version.check_update` to return `{"status": …, "installed": …, "latest": …}`, `version.classify_uninstall` to return a kind, `version.perform_update`, and `sys.stdin.isatty`. All tests run inside `helpers.cwd(tempdir)` for an empty temp dir.
- [X] T006 [US1] In `tests/test_cli_update.py`, test the updated path per [contracts/cli-update-command.md](contracts/cli-update-command.md) "Update available, uv-managed": with `--yes` (both `["cli", "update", "--yes"]` and `["--yes", "cli", "update"]`) `perform_update` is called once with `latest`, output contains `<installed> → <latest>` and "takes effect the next time you run spectra", exit `cli.EXIT_OK`; and on an interactive TTY answering yes (patch `ui.confirm` → True) the same.
- [X] T007 [US1] In `tests/test_cli_update.py`, test "already current": status `up_to_date` and status `ahead` each print "The spectra command is up to date (<installed>)", never call `classify_uninstall`, `perform_update`, or `ui.confirm`, and exit `cli.EXIT_OK` (FR-006; no downgrade offered).
- [X] T008 [US1] In `tests/test_cli_update.py`, test "unreachable": status `latest_unknown` prints "Could not check for a newer spectra command" and "Nothing was changed", output does NOT contain "up to date", nothing else is called, exit `cli.EXIT_UNREACHABLE` (FR-007, SC-005).
- [X] T009 [US1] In `tests/test_cli_update.py`, test confirmation: TTY + `ui.confirm` → False prints "Nothing was changed.", no `perform_update`, exit `cli.EXIT_DECLINED`; non-TTY without `--yes` prints "Re-run with --yes", calls neither `ui.confirm` nor `perform_update`, exit `cli.EXIT_DECLINED` (FR-004, FR-005; research R3).
- [X] T010 [US1] In `tests/test_cli_update.py`, test install kinds when an update is available: `NOT_INSTALLED` and `PIP_OR_SOURCE` print "not installed as a uv tool, so it cannot update itself", never prompt or call `perform_update`, exit `cli.EXIT_OK`; `UNKNOWN_UV_ABSENT` prints "uv was not found on PATH" and a manual `uv tool install spectra-cli --from '…@<latest>' --force` line containing the tag, exit `cli.EXIT_DELEGATION` (FR-008, FR-009).
- [X] T011 [US1] In `tests/test_cli_update.py`, test failure: `perform_update` raises `version.UpdateError("uv exited with code 1; your current version is unchanged. …")` → output contains "Update failed" and "unchanged", does NOT contain "Updated the spectra command", exit `cli.EXIT_DELEGATION` (FR-009, SC-005).
- [X] T012 [US1] In `tests/test_cli_update.py`, test FR-011: with `--no-update-check`, and separately with `SPECTRA_NO_UPDATE_CHECK=1` in `os.environ` (via `mock.patch.dict`), `check_update` is still called and the up-to-date line still prints. Also assert `["cli", "update", "--force"]` exits `cli.EXIT_USAGE`.
- [X] T013 [US1] In `tests/test_cli_update.py`, test the not-a-project folder: output never contains "not a Spec Kit project" or "spectra install" (US1-AS2).

### Implementation for User Story 1

- [X] T014 [US1] Implement `cmd_cli_update(args)` in `spectra_cli/cli.py`, placed just above `cmd_cli_uninstall` under a `# cli update (the tool updates itself)` section banner, following the state machine in [data-model.md](data-model.md) and the exact copy in [contracts/cli-update-command.md](contracts/cli-update-command.md): (1) `result = version.check_update()`; `latest_unknown` → `ui.fail(...)` + "Nothing was changed…" → `EXIT_UNREACHABLE`; `up_to_date`/`ahead` → `ui.ok(f"The spectra command is up to date ({installed}).")` → `EXIT_OK`. (2) `ui.info` the "A new version … is available (you have …)" line. (3) `kind = version.classify_uninstall()`; `NOT_INSTALLED`/`PIP_OR_SOURCE` → info + dim guidance → `EXIT_OK`; `UNKNOWN_UV_ABSENT` → `ui.fail` + manual command built from `version.DIST_NAME` and `version.git_source(latest)` → `EXIT_DELEGATION`. (4) Print "This updates the spectra command only. Your projects and their agents are not touched."; if `args.yes` proceed; elif not `sys.stdin.isatty()` print "Re-run with --yes…" → `EXIT_DECLINED`; elif not `ui.confirm("Update the spectra command now?", default_yes=False)` → `ui.info("Nothing was changed.")` → `EXIT_DECLINED`. (5) `version.perform_update(latest)`; on `version.UpdateError as e` → `ui.fail(f"Update failed: {e}")` → `EXIT_DELEGATION`; else `ui.ok(f"Updated the spectra command: {installed} → {latest}.")` + "The new version takes effect the next time you run spectra." → `EXIT_OK`. Use `getattr(args, "yes", False)`. Do NOT call `_update_check_disabled`, `project.*`, `health.*`, `extension.*`, or `coverage.*`. Docstring states the isolation contract and cites spec 029.

**Checkpoint**: T005–T013 pass. MVP shippable.

---

## Phase 4: User Story 2 — Update only the command, even inside a project (P1)

**Goal**: Prove the handler is isolated from every project and every other component.

**Independent Test**: Inside a `helpers.temp_project()` with Spectra installed, run `cli update --yes`; only `perform_update` is invoked and the project tree is byte-identical.

- [X] T015 [US2] In `tests/test_cli_update.py`, add an isolation test: patch `project.classify`, `health.check_all`, `health.apply_updates`, `extension.delegate_update`, and `coverage` entry points (whatever `cmd_update` calls) with `side_effect=AssertionError`; run `["cli", "update", "--yes"]` with an update available inside `helpers.temp_project()`; assert exit `cli.EXIT_OK` and `perform_update` called once (FR-002, FR-003).
- [X] T016 [US2] In `tests/test_cli_update.py`, add a tree-unchanged test: snapshot `(relative path, bytes)` for every file under a `helpers.temp_project()` root, run `["cli", "update", "--yes"]` from inside it, re-snapshot, assert equal (SC-002). Also assert the output names no other component (no "Spec Kit CLI", "Core agents", "Spectra agents") (US2-AS3).

**Checkpoint**: Isolation is enforced by tests, not just by reading the handler.

---

## Phase 5: User Story 3 — Discover the command from help (P2)

**Goal**: Both help surfaces list `cli update`, with copy that says what it does, where, and what it leaves alone.

**Independent Test**: `spectra --help` and `spectra cli` show the `cli update` / `update` row first in the Tool commands panel.

- [X] T017 [US3] In `spectra_cli/cli.py`, rewrite `print_cli_group_help()`'s intro (and its docstring) to the contract text: "Manage the spectra command itself. These work from any folder. To check or update your whole stack — Spec Kit, the core agents, and your agents too — use `spectra version` and `spectra update` (see `spectra --help`)." wrapped across `ui.plain` lines at the file's existing width (FR-013).
- [X] T018 [P] [US3] In `tests/test_cli_update.py`, add help tests: `--help` output (via `helpers.plain_lines`) contains a `cli update` line before the `cli uninstall` line, within the "Tool commands — act on the spectra command itself" panel; the `cli update` description contains "any folder" and "never touches the agents"; `["cli"]` output lists `update` before `uninstall` and contains "work from any folder" (FR-012, FR-013, US3).
- [X] T019 [P] [US3] In `tests/test_cli_surface.py`, update `RetiredToolSubcommands`: class docstring says only `cli version` remains retired (`cli update` reinstated in 6.3.0); `RETIRED = {"version": "spectra version"}`; `test_neither_performs_its_old_action` and `test_neither_reaches_the_network_or_spawns_a_subprocess` run `["cli", "version"]` only (rename to `test_it_does_not_…`); `test_they_are_absent_from_the_advertised_tool_commands` asserts only `cli version` is absent and add an assertion that `cli update` IS advertised. In `RemovedFlags.test_no_removed_flag_points_at_a_retired_command`, drop the `spectra cli update` assertion (research R8) and update the docstring of `test_each_removed_flag_names_a_live_replacement` so it no longer says the tool-scoped pair was retired.

**Checkpoint**: Help and the retired-command tests agree with the new surface.

---

## Phase 6: User Story 4 — Point the stuck user at the new command (P3)

**Goal**: `spectra update` outside a project adds one pointer line; other commands keep 028's two lines.

**Independent Test**: In an empty temp dir, `spectra update` prints three lines and exits 5; `spectra check` prints two.

- [X] T020 [US4] In `spectra_cli/cli.py` `cmd_update`, replace `return _say_not_a_project()` with: call `_say_not_a_project()`, then `ui.plain("  Update just the spectra command: " + ui.bold("spectra cli update"))`, then return the code `_say_not_a_project()` returned. Leave `_say_not_a_project()` itself unchanged (research R7, FR-016).
- [X] T021 [US4] In `tests/test_version_update.py`, extend (or add beside) `test_not_a_project_exits_five_and_says_something_different` for the `update` path: in a non-project temp dir, `helpers.plain_lines(out)` for `["update"]` equals exactly the three lines in the contract's "spectra update outside a Spec Kit project" section, exit `cli.EXIT_PROJECT_STATE`; and for `["version"]` the output does NOT contain "spectra cli update" (FR-016 scope). Confirm `tests/test_check.py` and `tests/test_uninstall.py` exact-two-line tests still pass unchanged.

**Checkpoint**: All four stories complete.

---

## Phase 7: Polish & Cross-Cutting

- [X] T022 [P] Update `README.md`: in the "Managing the **tool itself**" block (~L397) change the lead-in (no longer "down to one verb") and add `spectra cli update   # update the spectra command itself, from any folder` above `spectra cli uninstall`; add a `> **Changed in 6.3.0.**` note above the 6.0.0 note explaining `spectra cli update` is back with a narrower meaning (the command only, from anywhere; `spectra update` still covers the whole stack); reword the 6.0.0 note so it does not read as current ("were retired" → "were retired; `cli update` returned in 6.3.0"); in the "Two release channels" table, CLI column "You update it with" → `spectra update`, or `spectra cli update` from any folder (`spectra cli uninstall` to remove it) (FR-017).
- [X] T023 [P] Update `docs/index.html` "Keep the whole stack current" step: add `<pre><code>spectra cli update      # update just the command, from any folder</code></pre>` above the `spectra cli uninstall` line, and prepend a "Changed in 6.3.0: …" sentence to the `.os` changelog span; reword the 6.0.0 sentence to note `cli update` returned in 6.3.0 (FR-017).
- [X] T024 Run `python3 -m unittest discover -s tests` and `python3 tools/generate_agent_docs.py --check`; fix any failure.
- [X] T025 Run the manual checks in [quickstart.md](quickstart.md) §2–§4 from a temp dir and confirm output matches the contract.
- [X] T026 Run `python3 tools/ship.py --dry-run`; confirm `VERSION` is `6.3.0` and `spectra/extension.yml`, `catalog.json`, `docs/packages/spectra.zip` are unchanged (`git diff --stat main`).

---

## Dependencies & Execution Order

- **Phase 1 (T001)**: independent; can run any time before T026.
- **Phase 2 (T002–T004)**: all in `spectra_cli/cli.py`, sequential; blocks every story.
- **US1 (T005–T014)**: T005 first (creates the test file); T006–T013 extend that file sequentially; T014 (implementation) can be written alongside and must land for them to pass.
- **US2 (T015–T016)**: depends on T014. No production change.
- **US3 (T017–T019)**: T017 depends on Phase 2 only. T018 depends on T005 (same file as US1 tests, so sequence it after T013). T019 is a different file → [P].
- **US4 (T020–T021)**: depends on Phase 2 only; independent of US1–US3.
- **Polish**: T022/T023 [P] any time after Phase 2; T024–T026 last.

### Story dependency graph

```text
T001 ─────────────────────────────────────────────┐
T002 → T003 → T004 ─┬─ US1 (T005…T014) ─ US2 (T015, T016)
                    ├─ US3 (T017, T019 ∥; T018 after T013)
                    ├─ US4 (T020 → T021)
                    └─ T022 ∥ T023 ──────────────────┴─ T024 → T025 → T026
```

## Parallel Opportunities

- After Phase 2: T019 (`tests/test_cli_surface.py`), T021 (`tests/test_version_update.py`), T022 (`README.md`), and T023 (`docs/index.html`) touch distinct files and can proceed together while US1 is built.
- Within US1, T005 can be drafted while T014 is implemented.

```text
# Example: once T004 lands
Task: "T019 update RetiredToolSubcommands in tests/test_cli_surface.py"
Task: "T022 README tool-commands block + 6.3.0 note"
Task: "T023 docs/index.html stack-current step"
Task: "T005 create tests/test_cli_update.py scaffold"
```

## Implementation Strategy

### MVP (US1 only)

Phase 1 → Phase 2 → US1. At that point `spectra cli update` works from any folder, is listed in
`--help` (via T003), and every outcome is tested. Shippable on its own.

### Incremental delivery

1. MVP as above.
2. US2 — lock the isolation contract in with tests.
3. US3 — `spectra cli` group copy and retired-command test cleanup.
4. US4 — pointer line from `spectra update`.
5. Polish — docs, full suite, quickstart, `ship.py --dry-run`. Then land with `python3 tools/ship.py`
   and tag `6.3.0` (SHIPPING.md Path B). Never `git push origin main`.
