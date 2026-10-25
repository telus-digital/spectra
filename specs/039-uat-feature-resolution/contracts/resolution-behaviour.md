# Contract: how uat resolves its feature

Each behaviour below is something `spectra/commands/uat.md` must state and `tests/test_uat_flow.py` must
pin. Tests are named by class and intent; tasks fix the exact names.

| # | Behaviour | FR | Pinned by |
|---|---|---|---|
| B1 | Feature directory is `SPECIFY_FEATURE_DIRECTORY`, then `feature_directory` in `.specify/feature.json`, in that order; a set-but-empty variable counts as unset | FR-001 | `FeatureIsResolvedAsTheImplementCommandDoes`: order by text position; "empty" + "unset" |
| B2 | Root is `SPECIFY_INIT_DIR` when non-empty, else the nearest `.specify/`; invalid `SPECIFY_INIT_DIR` stops with its value and reason; relative values resolve against the root | FR-002 | same class |
| B3 | The feature's `tasks.md`, `test-plan.md` and `spec.md` are read from the resolved directory | FR-003 | same class |
| B4 | Branch name, modification times, `specs/` listing, cache, prior run and history are never consulted; no picker | FR-004 | same class (rewritten sources test; picker assertion kept) |
| B5 | Resolution never writes `feature.json` and never creates the directory | FR-005 | same class |
| B6 | Exactly one shell read of both variables, once per run, before the run confirmation; POSIX and PowerShell forms; the never-table's "start … before the run confirmation" row says this read starts nothing | FR-006 | `TheEnvironmentReadStartsNothing` (new) |
| B7 | A denied or failed read stops before anything else is read; no fallback to `feature.json` alone | FR-007 | same new class |
| B8 | Invoking project is the nearest `.specify/`, whatever `SPECIFY_INIT_DIR` says; a feature outside it trips the out-of-project stop | FR-008 | `FeatureIsResolvedAsTheImplementCommandDoes` |
| B9 | No feature, unusable record, missing directory: each stops, writes nothing, starts nothing | FR-009, FR-010 | same class |
| B10 | A directory with no `tasks.md` stops, applied to the resolved directory | FR-011 | same class |
| B11 | Argument is optional; it matches only the feature directory or its `spec.md` after normalizing; anything else stops before reading, naming the argument, resolved directory and source | FR-012 | `AnArgumentOnlyConfirms` (new) |
| B12 | An argument is never used in place of resolution | FR-013 | same new class |
| B13 | Every resolution stop shows the one remedy block; "run the specify command" only for creating a feature | FR-014 | `FeatureIsResolvedAsTheImplementCommandDoes`: the block's lines |
| B14 | First statement of a resolved run names the directory and source, and the record's value when it disagreed | FR-015 | `TheResolutionIsAnnounced` (new) |
| B15 | Step 3's run confirmation names the feature directory whose `tasks.md` will be ticked | FR-016 | same new class |
| B16 | The report's Feature row records the directory and its source; the session report names both | FR-017 | same new class |
| B17 | Ticks, evidence and report go to the feature confirmed at the start; `feature.json` is not re-read | FR-017a | `TheEnvironmentReadStartsNothing`: "reused for the whole run" + no re-read |
| B18 | `--env`, the run confirmation gate, observed-pass-only ticking, never changing a human's tick, evidence and secret masking, `tasks.md` edit scope, and every other never-table row unchanged; non-interactive bullet becomes "a feature that does not resolve still stops" | FR-018 | existing classes unchanged; `NonInteractiveStartsNothing` bullet assertion swapped |
| B19 | Governing rule, intro, never-infer section and its reasoning, and the never-table row are rewritten | FR-019 | `NoStaleProse` (new) + `FeatureIsResolvedAsTheImplementCommandDoes` |
| B20 | `after_implement` hook prompt checked; it names no path and stays | FR-020 | assertion that the prompt names no path |
| B21 | Front matter and manifest descriptions say neither "required" nor "never inferred" | FR-021 | `NoStaleProse` |
| B22 | `AGENTS_LIST.md`, `spectra/README.md` and `docs/index.html` show the no-argument form first and drop "required" | FR-022 | `NoStaleProse` |
| B23 | Version 1.28.0 in manifest and catalog; CHANGELOG `[1.28.0]` names the mismatch stop; zip rebuilt | FR-023 | existing sync checks (`tools/ship.py --dry-run`) |
| B24 | Old-contract tests rewritten, not deleted | FR-024 | `git diff` of `tests/test_uat_flow.py` |
| B25 | `test-plan.md` command and scenario/evidence/ticking behaviour untouched | FR-025 | `git diff` review; no test |
