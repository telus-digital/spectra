---
id: uat
title: UAT Runner
command: speckit.spectra.uat
provider: spectra
type: add-on
phase: testing-quality
order: 30
status: available
summary: Run the user-acceptance scenarios from your test plan on explicit request — perform what the agent can drive, save the evidence, and tick only what it saw pass.
manifest: Run user-acceptance testing for one feature, only on explicit request — read the UAT phase in its tasks.md and the Suggested UAT scenarios in its test-plan.md, start the build after your confirmation, perform the scenarios the agent can actually drive, save screenshots or transcripts as evidence beside the spec, tick only the UAT tasks it observed pass, and write uat-report.md. Finds the feature the way the implement command does — from SPECIFY_FEATURE_DIRECTORY or .specify/feature.json — names it before anything starts and in the run confirmation, and stops rather than guess. Human-only, failed, and blocked scenarios stay open with a reason. Never edits source, tests, CI, the spec, the test plan, or the constitution, never reproduces a secret, and makes no network request beyond what the build under test makes.
---

Perform a feature's user-acceptance scenarios on the real build, after
implementation, **only when you ask**. The test plan suggests the scenarios, `tasks` turns them into a
final UAT phase, and the implement command leaves that phase open. From there you choose: perform UAT
yourself and tick the tasks, or hand the feature to this command and let the agent perform the scenarios
it can drive — with screenshots, transcripts, and comparisons as evidence.

**It ticks only what it saw pass.** A tick in `tasks.md` is a claim that acceptance happened, so a
scenario is marked done only when the agent observed its outcome, and the tick carries a link to the
evidence. A `human` scenario, a failed one, and one the agent could not reach stay open with a reason. A
task a human already ticked is never touched, and a pass is never reverted.

**It starts nothing before you confirm.** It shows the exact command it would run to start the build and
waits. Decline and every scenario is reported blocked, not failed. It acts on a locally started build
unless you name an environment with `--env`, and it makes no network request beyond what the build under
test makes. `--non-interactive` starts nothing and attempts nothing.

**It changes nothing it is accepting** — not source, not tests, not configuration, not the spec, not the
test plan, not the constitution. It never edits code to make a scenario pass. Its writes are the `[UAT]`
lines in `tasks.md` it observed passing, `uat-report.md` beside the spec, and the evidence under
`specs/<feature>/uat/<run-stamp>/`, which a re-run adds to and never overwrites. A capture that might
show a secret is masked or skipped, and the report records what was withheld.

## Arguments

none needed: it finds the feature the way the implement command does
(`SPECIFY_FEATURE_DIRECTORY`, then `.specify/feature.json`) and names it before anything starts — no
branch name, no picker. A path to the feature directory or its `spec.md` only confirms it, and a
mismatch stops. `--env <name>` to act on a named environment. `--non-interactive` for CI.

## Use it when

implementation is done and you want acceptance evidence before opening a pull
request. After implement, an optional hook offers it ahead of `create-pr`, and another offers it after
converge; the hooks only ask.

## Drivability is judged in its own session.

It states which tools it relied on; a scenario marked
`agent` that this session cannot reach becomes *awaiting human* rather than a guess.

## Template

`uat-report-template.md`. Override it at
`.specify/templates/overrides/uat-report-template.md`. The report carries no checkboxes — `tasks.md` is
the tracker — and keeps a cumulative run log.

## Examples

```
/speckit-spectra-uat
/speckit-spectra-uat --env staging
/speckit-spectra-uat specs/021-signed-webhooks
```

## How it works

1. Finds the feature the way the implement command does, and names it before anything starts and again
   in the run confirmation. Where no feature resolves, it stops and says how to set one.
2. Reads the UAT phase in `tasks.md`, the scenarios in `test-plan.md`, the strategy's evidence rule, and
   the constitution.
3. Reports incomplete implementation and asks before going on, then shows the exact command it would run
   to start the build and waits for your confirmation.
4. Performs only the `agent` and `either` scenarios it can drive with the tools available in its own
   session.
5. Captures evidence — screenshots, transcripts, comparisons — under
   `specs/<feature>/uat/<YYYYMMDD-HHMMSS>/`, never overwriting an earlier run.
6. Ticks only the UAT tasks it observed pass, appending a link to the evidence, and writes
   `uat-report.md` beside the spec.

## Other environments

`--env` takes a name or a URL: pass `--env <name-or-url>` to act on an environment other than a local
build.
