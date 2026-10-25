# Contract: how test-plan resolves its feature

Each behaviour is something `spectra/commands/test-plan.md` must state and `tests/test_test_plan_flow.py` must
pin. Tests are named by class and intent; tasks fix the exact names.

| # | Behaviour | FR | Pinned by |
|---|---|---|---|
| B1 | Root is `SPECIFY_INIT_DIR` when non-empty, else the nearest `.specify/`; `feature.json` and relative paths come from that root | FR-001a | `FeatureIsResolvedAsThePlannerDoes`: names `SPECIFY_INIT_DIR` and the nearest `.specify/` |
| B2 | Feature directory is `SPECIFY_FEATURE_DIRECTORY`, then `feature_directory` in `.specify/feature.json`, in that order | FR-001 | same class: order asserted by text position |
| B3 | A set-but-empty variable counts as unset | FR-001 | same class: "empty" + "unset" |
| B4 | The spec is `<feature-dir>/spec.md` | FR-002 | same class |
| B5 | Branch name, modification times, `specs/` listing, cache, prior run, and history are never consulted to choose a feature; no picker | FR-003 | rewritten inference-sources test; picker test kept |
| B6 | Resolution never writes `feature.json` and never creates the directory | FR-004 | same class |
| B7 | Exactly one shell read, of both variables, once per run; named in the never-table as the only command run to resolve the feature; POSIX and PowerShell forms given | FR-005, C1 | same class + `ItRunsNothing` gains one assertion |
| B8 | A failed or denied read stops; no fallback to `feature.json` alone | FR-005 | same class |
| B9 | Invalid `SPECIFY_INIT_DIR` stops with the value and reason | FR-001a | same class |
| B10 | No feature, unusable record, missing directory or `spec.md`: each stops, writes nothing, names the remedy block | FR-006, FR-007, FR-023 | same class: each stop + the remedy block's two lines |
| B11 | Argument is optional; it must equal the feature directory or its `spec.md`; else stop, naming argument, resolved directory, source | FR-008 | `AnArgumentOnlyConfirms` (new) |
| B12 | An argument is never used in place of resolution | FR-009 | same new class |
| B13 | First statement names the resolved directory and source, and the record's value when it disagreed | FR-010 | `TheResolutionIsAnnounced` (new) |
| B14 | Step 13's Spec fact records the source | FR-011 | same new class |
| B15 | Step 16 reports the source next to the written path | FR-012 | same new class |
| B16 | Step 17 content unchanged | FR-013 | existing `TheHandoffIsPrintedNeverWired` tests unchanged |
| B17 | Handoff only after the agreement check passes; the check reuses the env values and re-reads only `feature.json` | FR-014 | `TheHandoffIsPrintedNeverWired` gains one test |
| B18 | Out-of-project stop, usability test, one-file write, existence gate, non-interactive asymmetry, R1–R6 unchanged | FR-015 | existing classes unchanged; non-interactive empty-argument bullet replaced (C2) |
| B19 | The never-infer section and table row state the new rule and its reason | FR-016 | rewritten `test_it_refuses_to_infer_the_specification` |
| B20 | Hook prompt no longer passes `SPEC_FILE`; says the feature specify just recorded is used | FR-017 | rewritten manifest hook test |
| B21 | Front matter and manifest descriptions say neither "requires the spec path" nor "never inferred" | FR-018 | new assertion over both descriptions |
| B22 | `AGENTS_LIST.md` and `docs/index.html` show the no-argument form first and drop "no feature record" | FR-019 | new assertion over both files |
| B23 | Version 1.27.0 in manifest and catalog; CHANGELOG `[1.27.0]` names the mismatch stop; zip rebuilt | FR-020 | existing sync checks (`tools/ship.py --dry-run`) |
| B24 | `uat.md` unchanged | FR-022 | `git diff` review; no test |
