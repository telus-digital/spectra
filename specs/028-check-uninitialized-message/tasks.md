---

description: "Task list for the one-step 'not a Spec Kit project' remedy"
---

# Tasks: One-Step Remedy When the Folder Is Not a Spec Kit Project

**Input**: Design documents from `specs/028-check-uninitialized-message/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/not-a-project-output.md, quickstart.md

**Tests**: Required — FR-007 asks for the tests covering this state to assert the new remedy line and
the absence of a separate `specify init` instruction. Stdlib `unittest` only; run with
`python3 -m unittest discover -s tests`.

**Organization**: Tasks are grouped by user story so each can be implemented and tested on its own.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2)

## Expected output (from contracts/not-a-project-output.md)

With ANSI styling removed, the state report is exactly:

```text
✗ This is not a Spec Kit project — no .specify/ directory here or in any parent folder.
  Initialize Specify and add Spectra: spectra install
```

Line 2 starts with two spaces; `spectra install` is the only bold part; `specify init` does not appear;
exit code stays `cli.EXIT_PROJECT_STATE`.

---

## Phase 1: Setup

No setup needed — the stdlib-only CLI and test suite already exist.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: A test helper every story's exact-output assertion depends on.

- [X] T001 Add `NOT_A_PROJECT_LINES` (a tuple of the two contract lines above) and a `plain_lines(out: str) -> list[str]` helper to `tests/helpers.py`. `plain_lines` strips ANSI escapes with `re.sub(r"\x1b\[[0-9;]*m", "", out)` and returns `splitlines()` (research.md R4: `ui.USE_COLOR` is fixed at import from the real TTY, so redirected test output may still carry colour codes). Add `import re` alongside the existing imports, and match the module's docstring and comment style.

**Checkpoint**: Helper importable as `h.plain_lines` / `h.NOT_A_PROJECT_LINES`.

---

## Phase 3: User Story 1 - One command to get from nothing to a working project (Priority: P1) 🎯 MVP

**Goal**: `spectra check` in an uninitialized folder recommends only `spectra install`.

**Independent Test**: `python3 -m unittest tests.test_check` passes, and the quickstart's manual
`NO_COLOR=1 … spectra_cli.cli check` in an empty temp dir prints the two contract lines with exit 5.

### Tests for User Story 1 ⚠️

> Write these first and confirm they FAIL against the current three-line output.

- [X] T002 [US1] In `tests/test_check.py` class `States`, replace `test_not_a_spec_kit_project_names_specify_init` with `test_not_a_spec_kit_project_points_only_at_spectra_install`: run `["check"]` in `h.temp_project(is_project=False)`, assert `code == cli.EXIT_PROJECT_STATE`, assert `h.plain_lines(out)[-2:] == list(h.NOT_A_PROJECT_LINES)`, assert `"Then add Spectra" not in out` (the old third line is gone — SC-003), and assert `"specify init" not in out` (FR-003). Update the module/class docstring only if it names `specify init`.

### Implementation for User Story 1

- [X] T003 [US1] In `spectra_cli/cli.py` `_say_not_a_project()`, replace the two `ui.plain(...)` remedy lines with the single line `ui.plain("  Initialize Specify and add Spectra: " + ui.bold("spectra install"))`. Keep the `ui.fail(...)` line, the docstring's intent, and `return EXIT_PROJECT_STATE` unchanged (FR-001, FR-002, FR-005). Do not touch `_say_not_installed`, `_say_incomplete`, or `spectra_cli/install.py` (FR-006).
- [X] T004 [US1] Run `python3 -m unittest tests.test_check` — T002 now passes, and the SC-009 "four different sentences" tests in the same file still pass.

**Checkpoint**: US1 is shippable on its own — `check` shows the new advice.

---

## Phase 4: User Story 2 - Same advice from every command that hits this state (Priority: P2)

**Goal**: `version`, `update`, and `uninstall` print the identical two-line report (FR-004, SC-002).

**Independent Test**: `python3 -m unittest tests.test_version_update tests.test_uninstall` passes.

Already true by construction after T003 (all four commands call `_say_not_a_project()`); these tasks lock it in.

### Tests for User Story 2 ⚠️

- [X] T005 [P] [US2] In `tests/test_version_update.py` class `CannotAnswer`, extend `test_not_a_project_exits_five_and_says_something_different` (the `["version"]` case) to also assert `h.plain_lines(out)[-2:] == list(h.NOT_A_PROJECT_LINES)` and `"specify init" not in out`.
- [X] T006 [P] [US2] In `tests/test_version_update.py` class `BadStates`, change `test_not_a_project_exits_five_rather_than_delegating` (the `["update"]` case) to capture `out` instead of `_`, and add the same two assertions as T005. Keep `delegated.assert_not_called()` and the exit-code assertion.
- [X] T007 [P] [US2] In `tests/test_uninstall.py` class `Failures`, extend `test_not_a_spec_kit_project_exits_five` (the `["uninstall"]` case) with the same two assertions as T005. Keep `delegated.assert_not_called()`.

> T005 and T006 edit the same file — if done by one agent, do them sequentially; [P] marks independence from T007.

**Checkpoint**: All four commands are covered by exact-output tests.

---

## Phase 5: Polish & Release (CLI channel, SHIPPING.md Path B)

- [X] T008 Bump the root `VERSION` file from `6.2.1` to `6.2.2` (PATCH — wording change only; research.md R5). Do NOT change `spectra/extension.yml`, `catalog.json`, or anything under `spectra/` (Principle VI).
- [X] T009 Run the full suite: `python3 -m unittest discover -s tests` — all green.
- [X] T010 Run the manual check from `specs/028-check-uninitialized-message/quickstart.md` step 2 for `check`, `version`, `update`, and `uninstall`; confirm each prints the two contract lines and exits 5.
- [X] T011 Run `python3 tools/ship.py --dry-run` and confirm checks and tests pass.
- [X] T012 Landing (maintainer, after commit): `python3 tools/ship.py`, then `git tag 6.2.2 && git push origin 6.2.2`, then verify the Latest release per SHIPPING.md Path B. Never `git push origin main`.

---

## Dependencies & Execution Order

- **T001** (helper) blocks T002, T005–T007.
- **US1**: T002 (failing test) → T003 (fix) → T004 (verify).
- **US2**: depends on T001 and T003 for the assertions to pass; T005/T006/T007 are independent of each other at the file level (T005/T006 share a file).
- **Polish**: T008 any time after T003; T009–T011 after all tests and the bump; T012 last, after commit.

## Parallel Example

```text
After T003:
  Agent A: T005 then T006   (tests/test_version_update.py)
  Agent B: T007             (tests/test_uninstall.py)
  Agent C: T008             (VERSION)
```

## Implementation Strategy

1. **MVP**: T001 → T002 → T003 → T004. The user-visible fix is done; every command already benefits.
2. **Lock-in**: T005–T007 guard the other three commands against future divergence.
3. **Release**: T008–T012.

## Totals

- 12 tasks: Foundational 1 · US1 3 · US2 3 · Polish/Release 5
