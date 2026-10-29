# Quickstart: validating next-step suggestions

These checks prove SC-001 to SC-006. Run the automated checks first; the manual pass covers what text
assertions can't, namely what a user actually sees.

## Automated checks (repository root)

```bash
python3 tools/generate_agent_docs.py --check
```

```bash
python3 -m unittest discover -s tests
```

Expected: both pass.

`tests/test_next_step_suggestions.py` asserts:

- the `contracts/hooks.md` invariants;
- each closing-block condition in `contracts/closing-suggestion.md`, checked against the command text;
- that `kb-vault.md` names no `/speckit-constitution`.

The existing UAT test still asserts the implementation-incomplete check.

```bash
python3 tools/ship.py --dry-run
```

Expected: the checks and tests pass. Nothing is pushed.

## Manual pass (throwaway Spec Kit project, Spec Kit 1.2.4)

1. Build the package with `python3 tools/build_package.py`. In a scratch directory, run
   `specify init --here --ai claude`, then `specify extension add --dev <repo>/spectra`. Confirm that
   `.specify/extensions.yml` lists SPECTRA under `after_clarify`, under `after_implement` (converge, uat,
   create-pr, in that order) and under `after_converge`, all `optional: true`.
2. **After clarify (US3):** run `/speckit-specify` on a small feature, then `/speckit-clarify`. The hooks
   block shows the test-plan offer with the after-clarify prompt, and nothing runs.
3. **After implement (US1):** take the feature through plan, tasks and implement. The hooks block lists
   `/speckit-converge`, then `/speckit-spectra-uat`, then `/speckit-spectra-create-pr`, and none of them runs.
4. **After converge with gaps (US2, scenarios 2–3):** delete one implemented behaviour, then run
   `/speckit-converge`. It appends tasks and names implement, and the hooks block shows the UAT offer with
   the exact FR-007 prompt. Run `/speckit-spectra-uat` straight away. It reports implementation incomplete,
   gives the count of unchecked non-UAT tasks, and asks before going on. Decline.
5. **After converge with nothing left (US2, scenario 1):** run implement, then converge again. It reports
   that it converged, and the UAT offer appears before any PR is suggested.
6. **defect-rca (US4):**
   - Run a defect through to a validated cause. The report ends with the `**Next step**` block and a
     prompt citing the document path and the cause.
   - Repeat, stopping with no validated cause. The block reads `none:` with a reason.
   - In exploration mode there is no block.
7. **flaky-test-detector (US5):**
   - With a test whose fix is in production code, approve both gates. The report's block offers only that
     row.
   - Repeat and decline Gate 2. The block offers every open row.
   - Decline Gate 1. There is no block.
8. **impact (US6):** run an analysis. The report ends with the conditional pointer and a prompt citing the
   analysis path. Nothing appears under `specs/`, and the document has no spec reference.
9. **Unchanged agents (SC-005):**
   ```bash
   git diff main --stat -- spectra/commands/
   ```
   The output lists only `defect-rca.md`, `impact.md`, and `flaky-test-detector.md`, plus `test-plan.md`,
   whose regenerated `description:` line is the only change in it.

## Manual pass

Run on 2026-10-29 against Spec Kit 1.2.4, in a fresh scratch project (`specify init --here --integration
claude`, then `specify extension add --dev <repo>/spectra`).

- **Step 1 — passed.** `.specify/extensions.yml` registers SPECTRA's hooks exactly as designed:
  - `after_specify`: test-plan;
  - `after_clarify`: test-plan;
  - `after_implement`: converge (3), uat (5), create-pr (10), in that order;
  - `after_converge`: uat.

  All are `optional: true`. The core `speckit-converge` skill is present, so its `after_converge` check
  exists in this Spec Kit.
- **Step 9 — passed.** `git diff main --stat -- spectra/commands/` lists only `defect-rca.md`,
  `flaky-test-detector.md`, `impact.md`, and `test-plan.md`, whose only change is its regenerated
  `description:` line. `spectra_cli/` and `VERSION` are unchanged.
- **Steps 2–8 — not performed in the implementing session.** Each needs a live coding-agent session that
  runs Spec Kit commands (`clarify`, `implement`, `converge`, `uat`) and the three SPECTRA agents end to end
  against a real feature. That can't be driven from inside the session that's implementing this one. Their
  text-level guarantees are covered by `tests/test_next_step_suggestions.py`. What's left to see is the
  rendered hooks block and closing blocks in a real run.
