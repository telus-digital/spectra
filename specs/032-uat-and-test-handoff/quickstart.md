# Quickstart: validating spec 032 end to end

The command files are prompts, so `unittest` proves only that the rules are still in the text. This
manual pass proves that the flow works in a real project.

## Automated checks (run first)

```bash
python3 -m unittest discover -s tests
python3 tools/generate_agent_docs.py --check
python3 tools/build_package.py && git diff --stat docs/packages/spectra.zip
python3 tools/ship.py --dry-run
```

**Expected**: all tests pass and `--check` is clean. The zip only changes when `spectra/` does.

## Throwaway project

Set up a project with a browser surface so that agent UAT is reachable. A minimal web app with one page
and one form is enough.

```bash
specify init uat-demo --here
specify extension add --dev /Users/alibahaloo/Projects/spectra/spectra
```

**Expected**:
- `.specify/extensions.yml` lists `speckit.spectra.test-plan` under `after_specify`, with
  `optional: true`.
- It lists `speckit.spectra.uat` before `speckit.spectra.create-pr` under `after_implement`.

## Scenarios

1. **Strategy with the new lenses**
   - Run `/speckit-spectra-test-strategy` and take the defaults.
   - **Expected**: `docs/TEST_STRATEGY.md` has six lens sections, front matter with `lenses:` and
     `ownership:`, and a UAT evidence rule naming screenshots. It names no evidence for surfaces the app
     lacks. The amendment draft carries the UAT clause.
   - Apply the amendment with `/speckit-constitution`.
2. **Specify → test-plan offer** (US5)
   - Run `/speckit-specify` for a two-story feature.
   - **Expected**: the hooks block offers test-plan and tells the agent to pass `SPEC_FILE`. Accepting
     it runs test-plan against that path.
3. **Test plan** (US1, US6)
   - **Expected**:
     - `specs/001-…/test-plan.md` has Suggested UAT Scenarios, with each `UATn` citing `USn-ACn` and
       naming an executor.
     - It has a Regression Scope that cites existing tests, or the search performed.
     - It contains no checkbox.
     - It ends with the printed planning prompt, linking the file and stating the four obligations.
4. **Plan → tasks** (US2)
   - Paste the planning prompt, then run `/speckit-tasks`.
   - **Expected**:
     - `plan.md` has a Testing obligations section naming the test plan.
     - `tasks.md` has test tasks for every P1 condition before their implementation tasks.
     - It ends with a "User Acceptance (UAT) — not executed by the implement command" phase, with one
       `[UAT] UATn` task per scenario.
5. **Implement leaves UAT open** (US2, SC-003)
   - Run `/speckit-implement`.
   - **Expected**: every non-UAT task is `[X]`, every `[UAT]` task is still `[ ]`, and the report names
     the open UAT tasks. The after-implement hooks offer uat first, then create-pr.
6. **Agent UAT** (US4, SC-004)
   - Make one scenario fail deliberately (change the expected text in the test plan and task), mark
     another `human`, then run `/speckit-spectra-uat specs/001-…`.
   - **Expected**:
     - uat shows its start command and waits for confirmation before running it.
     - The passing scenario is ticked, with an evidence link under `specs/001-…/uat/<stamp>/`.
     - The failing scenario stays open, with evidence and a reason.
     - The human scenario is `awaiting human`.
     - `uat-report.md` exists, and no source file changed (`git status`).
7. **Re-run**
   - Run uat again.
   - **Expected**: only open tasks are retried, a new run-stamp folder is added, the report's run log has
     two lines, and the earlier evidence is still present.
8. **Consistency** (SC-005)
   - Mark UAT `not_applicable` in the strategy's front matter, then re-run test-plan.
   - **Expected**: there is no UAT section. Criteria that only UAT could verify appear as "ruled out by
     the strategy — re-run test-strategy".
9. **Pre-032 strategy**
   - Delete the `lenses:` key and re-run test-plan.
   - **Expected**: it states loudly that the strategy predates the UAT and Regression lenses, and both
     sections are omitted.
10. **No strategy**
    - Delete `docs/TEST_STRATEGY.md` and re-run.
    - **Expected**: it states loudly that no test strategy exists, uses the default set, and includes both
      sections.

## Contracts referenced

[strategy-lenses](contracts/strategy-lenses.md) ·
[test-plan-additions](contracts/test-plan-additions.md) ·
[workflow-wiring](contracts/workflow-wiring.md) · [uat-command](contracts/uat-command.md)
