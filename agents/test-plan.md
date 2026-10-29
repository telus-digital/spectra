---
id: test-plan
title: Test Plan
command: speckit.spectra.test-plan
provider: spectra
type: add-on
phase: requirements-discovery
order: 40
status: available
summary: Turn a specification into a test plan stakeholders can approve — traceable conditions, stated exclusions, and a real exit bar — before the implementation is designed.
manifest: Turn one specification into a stakeholder-facing test plan written beside it as test-plan.md — scope, risks, traceable test conditions, suggested UAT scenarios, regression scope, environment, and exit criteria — grounded in the project's own testing policy and its existing suite. It uses exactly the lenses the test strategy chose; a lens the strategy rules out is unavailable, and it says so loudly when the strategy predates UAT and regression or does not exist. It finds the feature the way the planning command does — SPECIFY_FEATURE_DIRECTORY, then .specify/feature.json — and says which one it used; a path argument only confirms it, and a mismatch stops, so the test plan and the plan always share a directory. Every acceptance criterion reaches a condition or a UAT scenario or is reported as uncovered, every user story gets a UAT scenario or a reason, and an ambiguous requirement gets a stated gap rather than an invented condition. Carries no checkbox in any section — it is approved, not tracked — and is offered by an optional hook after specify or clarify. It ends with a ready-to-paste planning prompt that writes the plan's testing obligations into plan.md, so the tasks include the tests and a final UAT phase the implement command does not execute. Writes one file, runs nothing, and makes no network request.
---

Get the tests **agreed before anyone writes them**. Run it after
`specify` and it picks up the feature `specify` recorded — the same one `plan` will plan — then reads its
specification, your constitution, your test strategy, your existing suite,
and the source the feature touches, then writes one `test-plan.md` **beside the spec**: scope with real
exclusions, a risk table that is a decision rather than an inventory, traceable test conditions,
suggested UAT scenarios, a regression scope, environment and data, and an exit bar someone can make a
go/no-go call from. It runs between `specify` and `plan`, and it is built for teams who want the test set
settled before the implementation is designed.

The document has two audiences and that shapes everything. A stakeholder reads it and approves it; the
planning command reads it and designs around it. So it states intent, not progress — and it produces no
tasks, writes no test code, and tracks nothing.

What makes it worth more than an hour with a whiteboard is **traceability that runs both ways**. Every
acceptance criterion in your spec reaches a test condition, a UAT scenario, or the uncovered list with a
reason — never none of them. Every condition names what it verifies using your spec's own identifiers
(`FR-014`, `SC-003`, or the composed `US2-AC1` for an acceptance scenario), so a reviewer can check
coverage in either direction without opening the code. The run tells you the count.

What it refuses to do is as important as what it does:

- **It finds the feature exactly as `plan` does, and no other way.** `SPECIFY_FEATURE_DIRECTORY` if set,
  otherwise `.specify/feature.json` — the record `specify` writes — so the test plan and `plan.md` always
  land in the same directory. No branch-name inference, no most-recently-modified heuristic, no picker.
  It says which feature it resolved and from where before doing anything else, and records it in the
  document, because a plan built against the wrong spec reads as authoritative to whoever approves it.
  If nothing resolves, it stops and tells you how to choose a feature. It runs one read-only shell
  command to see those two environment variables, and stops if that is refused rather than guess.
- **It never invents the missing decision.** Where a requirement is too ambiguous to test, it says so and
  writes no condition for it. A plausible-looking condition would be worse than the gap, because it
  launders a guess into something a stakeholder approves — and the guess becomes a requirement nobody
  agreed to.
- **It carries no checkboxes — exit criteria included.** It is approved, not tracked. A circulated document
  with live checkboxes creates a second apparent source of truth about progress, and it will disagree with
  `tasks.md`. If a template override puts checkboxes back, they are rendered as plain statements: your
  section is kept, only the construct goes.
- **It runs nothing.** Existing coverage is established by reading test source, never by executing the
  suite or a coverage tool. A coverage claim cites the test file; an absence claim cites the search — "no
  test referencing `SignatureVerifier` found under `tests/`" is allowed, "there is no coverage for
  signature verification" is not.
- **It inherits rather than invents.** Level names come from your `TEST_STRATEGY.md` **verbatim** where you
  have one — not normalized, not mapped — so the two documents read against each other. A declared coverage
  floor is carried into the exit criteria and attributed, never adjusted. And no level or tool is assigned
  that your dependency manifests cannot support, so a command-line tool never gets handed a browser driver.
- **It honours the whole strategy, not just its lens names.** A lens the strategy ruled out is unavailable
  here: a criterion that needs it goes to the uncovered list with the remedy "re-run test-strategy". It
  follows the strategy's ownership map when choosing a level, never names a tool the strategy ruled out,
  raises the likelihood of a risk in an area the strategy says has broken before, picks the floor of the
  surface the feature actually touches, and carries each inherited rule's provenance — cited, convention,
  or stated. A strategy that predates the UAT and Regression lenses, or looks stale against the repository,
  is flagged loudly. With no strategy at all it uses the full default set and says so, recommending
  `test-strategy`. `manual` stays available for a one-off human check, distinct from a UAT scenario.
- **UAT scenarios and regression scope.** Every user story gets at least one UAT scenario, traced to its
  acceptance criteria and given an executor — `agent`, `human`, or `either`, with `agent` only where the
  surface can actually be driven. The regression scope lists the existing tests that touch the feature's
  modules and must stay green, plus the additions its risks call for.

## Arguments

none needed. A path to the feature directory or its `spec.md` is accepted only as a
confirmation: if it names a different feature than the active one, the run stops and writes nothing.
`--non-interactive` for CI.

## Use it when

a spec is finished, your team works test-first, and you want the test set reviewed and
agreed before the implementation is planned. Skip it when nobody outside the implementing team needs to
see the test set; it is an add-on. After `specify` or `clarify`, an optional hook offers it — the hook
only asks, and the run picks up the feature `specify` recorded.

## Where it writes

`test-plan.md` in the active feature's directory, beside its `spec.md`. No sequence number, no
artifact subfolder, no `Artifact root:` resolution for the output. A test plan is *about one feature*, so
its identity is that feature's directory, exactly as `spec.md` and `plan.md` beside it carry no number.
It reads your declared artifact root for one purpose only — finding `TEST_STRATEGY.md`.

## Feeding it to the planner is one copy-paste.

The run ends with a ready-to-copy planning prompt that
links the written path and asks `plan` to record a *Testing obligations* section in `plan.md` — because
that is what `tasks` reads. P1 conditions become test tasks written before their implementation, the
regression scope stays green, and the UAT scenarios become a final phase titled "User Acceptance (UAT) —
not executed by the implement command". No core command is modified, so `plan` behaves exactly as it does
today for anyone who never installs this agent.

## Re-runs ask first.

The usual trigger is a `clarify` session changing the spec. It reads the existing
plan, tells you what would change before you answer, and carries forward every *explicitly not covered*
decision — or says it removed one. Declining leaves the file byte-identical. One file, rewritten in
place; Git carries the history.

## Priorities come from your spec.

A condition inherits the priority of the story it verifies, and only
P1 conditions gate the exit criteria. The one override: a prohibition, safety, or data-integrity property
is promoted to P1 whatever the story says, because a "MUST NOT" requirement rarely has a user story and
is exactly the one whose violation is unrecoverable.

## Template

`test-plan-template.md`, a seven-section structure. Override it at
`.specify/templates/overrides/test-plan-template.md` to reshape or drop sections; the override is
committed, team-wide, and survives extension updates. Each run reports which template it used. The
traceability invariant, the no-checkbox rule, the cited-absence rule, the priority derivation, and the
coverage statement stay with the command — a template shapes the document, not the standards.

## What it does not do

It does not write tests, generate tasks, modify your spec, touch test or CI configuration, edit the
constitution, commit, or make a network request. It writes exactly one file.

## Examples

```
/speckit-spectra-test-plan
/speckit-spectra-test-plan specs/021-signed-webhooks
/speckit-spectra-test-plan --non-interactive
```

## How it works

1. Resolves the feature exactly as `plan` does and says which one it picked and from where.
2. Reads your project — the spec in full, the constitution, your test strategy, existing tests and runner
   configuration, dependency manifests, CI definitions, and the source the feature touches.
3. Resolves the lens set from your own `TEST_STRATEGY.md` where you have one.
4. Turns every acceptance criterion into a test condition or a UAT scenario — or reports it as uncovered,
   with a reason. A requirement too ambiguous to test is reported as a gap naming what is missing.
5. Derives the risk table from stated triggers and the strategy's known risk areas, and condition
   priority from your spec's own story priorities.
6. Suggests UAT scenarios and a regression scope.
7. Writes one `test-plan.md` beside the spec, reports the count — criteria covered out of criteria
   found — then prints the planning prompt that consumes it.

The final UAT phase in `tasks.md` is one a human ticks, or that `speckit.spectra.uat` performs on
request.

## Unattended runs

Pass `--non-interactive` in CI: it will create a plan that does not exist, but never rewrite one that
does.
