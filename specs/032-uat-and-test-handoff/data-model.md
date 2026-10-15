# Data Model: UAT and Regression Lenses, a Tighter Test Handoff, and a UAT Runner

These entities are document structures, not database records. Field names are what the commands write
and read.

## Lens (strategy)

| Field | Values | Notes |
|---|---|---|
| name | `Unit`, `Integration`, `API contract`, `End-to-end`, `UAT`, `Regression`, plus evidence-warranted additions | Six mandatory; none may be omitted |
| applicability | `applicable` \| `not_applicable` | With a stated reason either way |
| proves / may assume | per the lens table | UAT: acceptable to its user in their terms / assembled build only. Regression: what worked still works / existing suite is the baseline |
| scope | a surface or `all` | |
| provenance | citation \| `convention` \| `stated` (+ question number) | R1, unchanged |

**UAT-specific fields**:
- `executors`: `human` \| `agent on explicit request` \| both.
- `evidence`: one entry per surface the project has — `browser` → screenshot (optionally a
  before-and-after pair); `cli` → terminal transcript; `http` → request/response transcript; `none` → not
  applicable.

**Regression-specific fields**:
- `gate`: the named suite, plus a cited workflow, or "runs nowhere automatically".
- `defect_rule`: whether a fixed defect earns a regression test.

**Front matter (new keys)**:

```yaml
lenses:
  unit: applicable
  integration: applicable
  api-contract: not_applicable
  end-to-end: applicable
  uat: applicable
  regression: applicable
ownership:
  "pure calculation": unit
  "persistence round-trip": integration
  "signed-in journey": end-to-end
```

A strategy with no `lenses:` key is **pre-032**. test-plan treats UAT and Regression as not established
and says so (FR-012).

## Level vocabulary (plan)

The plan's levels are the strategy's applicable **condition-bearing** lenses — unit, integration,
api-contract, end-to-end, and any added lens — plus `manual`, which is always available.

UAT and Regression are **section-bearing**: they control whether the two new sections exist, and are
not levels a condition is assigned to.

With no strategy, the default lens set applies: `unit`, `integration`, `api-contract`, `end-to-end`,
`uat`, `regression`, plus `manual`.

## UAT scenario (plan)

| Field | Rule |
|---|---|
| id | `UAT1`, `UAT2`, … scoped to the document; never reused within it |
| journey | a user-visible journey in the user's terms, one or two lines; not a click script |
| expected outcome | what the user sees or gets |
| verifies | spec identifier: `FR-xxx`, `USn-ACn`, or a short verbatim quotation |
| priority | inherited from what it verifies (existing derivation) |
| executor | `agent` \| `human` \| `either`. `agent` only when the surface is drivable *and* the strategy permits it; otherwise `human`, with the reason |
| evidence | what would show it passed, from the strategy's per-surface rule |
| journey favoured | yes or no — whether it is among the strategy's Q3 journeys (FR-033) |

**Traceability**: an acceptance criterion is *reached* by a condition, a UAT scenario, or an
"explicitly not covered" entry. R1 is otherwise unchanged.

## Regression scope entry (plan)

| Field | Rule |
|---|---|
| test | project-relative path of an existing test that touches a module the feature changes |
| why | the module or identifier it touches |
| kind | `existing` \| `risk-driven addition` (with the risk it answers) |

When nothing is found, a single line names the search terms and paths searched.

## UAT task (tasks.md, written by the planner/tasks per the handoff prompt)

```text
## Phase N: User Acceptance (UAT) — not executed by the implement command

- [ ] T041 [UAT] UAT1 (US1-AC1) New user signs up and lands on the dashboard — executor: agent
- [ ] T042 [UAT] UAT2 (US2-AC2) Exported invoice matches the on-screen total — executor: human
```

After uat observes a pass:

```text
- [X] T041 [UAT] UAT1 (US1-AC1) … — executor: agent — evidence: specs/021-x/uat/20261015-142233/UAT1-1.png
```

## UAT run and outcome (uat)

| Outcome | Meaning | Task mark |
|---|---|---|
| `passed` | the expected outcome was observed, and the evidence is saved | `[X]` + evidence link |
| `failed` | it was attempted and the observed outcome differed | unchanged |
| `blocked` | it could not be attempted (the build would not start, or a credential, sandbox or hardware was missing) | unchanged |
| `awaiting human` | its executor is `human`, or the surface is not drivable | unchanged |
| `already done` | a human, or an earlier run, ticked it | untouched |

**State transitions**: `open → passed` (ticked); `open → failed | blocked | awaiting human` (stays open);
`passed` is never reverted by uat. A re-run considers only `open` tasks.

## UAT report (`specs/<feature>/uat-report.md`)

- **Identifying block**: the feature, the build under test (branch, plus a version if one is committed),
  the environment (local, or the user-named one), and the date.
- **Scenarios**: id | verifies | executor | outcome | evidence | reason.
- **Totals**: passed, failed, blocked, awaiting human, already done.
- **Tools relied on**, and what was run, with the confirmation given.
- **Withheld**: any capture masked or skipped for secrets.
- **Run log**: one line per run, cumulative across re-runs.
- **Sources consulted and coverage.**
