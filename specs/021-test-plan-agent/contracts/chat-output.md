# Contract: What the User Sees

**Surface**: the session. Everything here is said aloud, not written to a file.

## The two gates

### Gate 2 — out of project (no answer taken)

Fires before anything is read. Not a confirmation; a stop.

```text
The specification at ../other-repo/specs/003-x/spec.md resolves outside this project.
A test plan is written beside its specification, and this command writes only inside the
project it was invoked in. Nothing was written.
```

### Gate 1 — an existing plan (answer required)

Fires **after** the derivation, so the question carries information.

```text
A test plan already exists at specs/021-test-plan-agent/test-plan.md (last changed 2026-09-04).
Rewriting it would:
  · add 4 conditions and remove 1 (US3-AC2 no longer appears in the spec)
  · carry forward 2 explicitly-not-covered decisions
  · leave the risk table unchanged
Rewrite it? [y/N]
```

Declined → nothing is written, and the run says so. A confirmation request with no information attached
is one a user learns to answer reflexively, which is the same as having no gate.

## The missing-argument response

```text
This command needs a specification to plan against, and it will not guess which one.

Supply the path to a spec.md, or to the feature directory containing it:
  <the planning command> specs/021-test-plan-agent/spec.md

Nothing was read and nothing was written.
```

It does **not** list the contents of `specs/`. Offering a picker is a second-order version of the same
problem: it still asks the user to choose from a list the command assembled, and one wrong keystroke
produces the same wrongly-grounded, signed document.

## The run report

Emitted after a successful write. Six things, in this order:

```text
Wrote specs/021-test-plan-agent/test-plan.md  (created)

Traceability   17 of 19 acceptance criteria covered by 23 conditions
               2 uncovered — 1 unresolved clarification, 1 untestable as written
Levels         unit · integration · api-contract · manual
               from docs/test-strategy/TEST_STRATEGY.md
Template       .specify/extensions/spectra/templates/test-plan-template.md
               1 checkbox construct rendered as a plain statement
Read           23 of 61 source files under src/auth and tests/auth, selected by
               the identifiers the spec names
Not read       docs/test-strategy/TEST_STRATEGY.md — not present; default lens set used
Added          Rollback / migration testing — the spec implies a schema change

Next:
  /speckit-plan Plan this feature against the approved test plan at
  specs/021-test-plan-agent/test-plan.md. Every P1 test condition in it must map to a
  task that writes the test before the implementation it covers.
```

### What the report must always state

| Element | Requirement |
|---|---|
| The written path and whether it was created or rewritten | FR-049 |
| Acceptance criteria covered out of those found | FR-049 |
| The resolved lens vocabulary and where it came from | FR-035, FR-036 |
| The resolved template layer, by path | FR-049, FR-054 |
| Any checkbox constructs converted | FR-041 |
| What portion of the relevant code and tests was read, and by what method | FR-016 |
| Every input expected and not readable, by name and reason | FR-015 |
| Which optional sections were added and why | FR-045 |
| The handoff | FR-047 |

## Degrading loudly

Every reduction in what the command could do is said at the moment it happens, with the reason. There is
no silent narrowing.

| Situation | Said |
|---|---|
| No constitution | "No constitution found; no testing obligation to inherit" |
| No strategy document | "Not present at the resolved location; default lens set used" |
| A declared artifact root that is unusable | The value, why it was rejected, and that the default was used for the lookup |
| A template layer present but empty | The path, and that the next layer was taken |
| No repository-wide text search available | That existing-coverage detection was reduced, and how |
| A specification with no identifiers | That the `Verifies` column uses verbatim quotations |
| A specification with no priorities | That priority was derived from impact alone |

## What is never said

| Never | Instead |
|---|---|
| A secret value, whole or partial | Its kind and where it is configured, and that the value was withheld |
| "There is no coverage for X" | "No test referencing X found under `<paths>`" |
| A guessed version for "build under test" | The branch, and that no version is committed |
| A claim that the plan is approved | The document is for approval; nothing in the run grants it |
