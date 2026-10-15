# Contract: speckit.spectra.uat

Covers FR-050 to FR-062.

## Interface

```text
/speckit-spectra-uat <feature-dir-or-spec-path> [--env <name-or-url>] [--non-interactive]
```

- **The feature is required.** It is a `specs/<feature>/` directory, or a path to the `spec.md` inside one.
  With no feature given, uat says what to provide and **stops**.
- **The feature is never inferred.** uat never takes it from the branch, `feature.json`, modification
  times, or session history, so the same rule as test-plan applies (pinned: "never infer which feature
  was meant").
- **`--env`** names a non-local environment. Without it, uat targets a locally started build only.
- **`--non-interactive`** means nothing is started or attempted. uat reports which scenarios it would
  attempt and why, and changes nothing.

## Reads

- The feature's `tasks.md` (the UAT phase) and `test-plan.md` (the Suggested UAT scenarios).
- The strategy's UAT evidence rule.
- The constitution.
- Manifests, the README and `quickstart.md`, to find the build or start command.

Each missing input is named. With no UAT phase, uat reports "nothing to run" and writes nothing.

## Gates, in order

1. **Implementation incomplete.** Non-UAT tasks are still unchecked. uat reports the count and asks
   before going on.
2. **Run confirmation.** uat shows the exact command it will run to start the build, and the target
   environment, then asks. If declined, every agent scenario is recorded as `blocked — run declined`.

## Behaviour

- **Which scenarios it attempts.** Only open `[UAT]` tasks whose executor is `agent` or `either`, and
  only on a surface the session's tools can operate. uat states which tools it relied on.
- **How it judges a scenario.** It performs the journey as a user would, and compares the result with the
  expected outcome. It never edits code to make a scenario pass.
- **Evidence.** For every attempted scenario it saves evidence to
  `specs/<feature>/uat/<YYYYMMDD-HHMMSS>/<UATn>-<k>.<ext>`.
- **Secrets.** It masks secrets in transcripts. Where a screen capture might show a secret it saves no
  image, and records that it withheld one.
- **Marking.** uat ticks a task `[X]` and appends ` — evidence: <path>` only when it observed a pass.
  Every other outcome leaves the line unchanged.
- **Human-only scenarios.** uat lists them as `awaiting human`. So does a scenario the plan marked
  `agent` whose surface this session's tools cannot operate, with that reason given.

## Writes (exhaustive)

| Path | What |
|---|---|
| `specs/<feature>/tasks.md` | `[UAT]` lines only: the checkbox and the evidence suffix |
| `specs/<feature>/uat/<run-stamp>/…` | evidence files, new on every run |
| `specs/<feature>/uat-report.md` | rewritten each run, shaped by the template, with a cumulative run log |

Pinned: "**never modifies source, tests, test configuration, CI, the specification, the test plan, or the
constitution**".

## Report (session)

The session report covers:

- the outcome totals;
- each scenario that is not passed, with its reason;
- where the evidence and the report were written;
- the template it resolved;
- what it ran.

Then it ends with one of two next steps. If anything is still open, it says: "the open UAT tasks are for
a human — tick them in tasks.md when done". If everything passed, it points to the PR hook or command.

## Template

`uat-report-template` is registered in `provides.templates` and resolved through the four layers, with an
inline skeleton as the last resort. Its sections are:

- Identifying block
- Scenarios
- Totals
- Tools and run
- Withheld
- Run log
- Sources consulted and coverage

## Never

- Infer the feature.
- Run anything before confirmation.
- Act on an environment the user did not name.
- Make a network request beyond what the build under test makes.
- Reproduce a secret.
- Tick a scenario it did not see pass.
- Touch a task a human ticked.
- Invoke another command.
