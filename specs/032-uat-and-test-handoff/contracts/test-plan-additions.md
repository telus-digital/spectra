# Contract: test-plan — consistency, new sections, honouring the strategy

Covers FR-010 to FR-037.

## Vocabulary and lens set (Step 3)

Resolution order is unchanged (strategy → constitution → default). What it resolves is now a **lens set**
with applicability, not only names.

| Strategy state | Condition levels | UAT section | Regression section | Must say |
|---|---|---|---|---|
| Has `lenses:` | its applicable condition-bearing lenses, plus `manual` | if `uat: applicable` | if `regression: applicable` | the source, by path |
| Pre-032 (no `lenses:`) | its named lenses, plus `manual` | **omitted** | **omitted** | "**this strategy predates the UAT and Regression lenses**", and to re-run test-strategy |
| No strategy | `unit`, `integration`, `api-contract`, `end-to-end`, `manual` | yes | yes | "**no test strategy exists**", and to run test-strategy |

- Pinned: "`manual` is always available" (kept) and "distinct from a UAT scenario".
- A criterion that only a ruled-out lens could verify goes to **Explicitly not covered** with reason
  `ruled out by the strategy` and remedy "re-run test-strategy". This adds a fifth reason to the
  not-covered table.

## Section: Suggested UAT scenarios

`| ID | Journey | Expected outcome | Verifies | Priority | Executor | Evidence |`

- IDs are `UAT1`…; executor is `agent | human | either`. Rules are in [data-model.md](../data-model.md).
- Pinned: "**agent only where the surface can actually be driven**".
- No checkbox, and no status column.
- **Every user story is covered (FR-026).** Each story is the subject of at least one scenario, or appears
  under Explicitly not covered with its reason. Pinned: "**every user story**".
- **The executor is judged from the surface kind and the strategy's policy (FR-021)**, not from the
  planning session's tools. Pinned: "**not from this session's tools**".

## Section: Regression scope

`| Test | Touches | Kind |`

The **Kind** column takes `existing` or `risk-driven addition`. A search line is mandatory when the table
is empty (the existing absence rule).

## Honouring the strategy

| FR | Rule | Pinned phrase |
|---|---|---|
| 030 | Ownership map wins; a departure is stated | "honour the strategy's ownership map" |
| 031 | No tool at no tier or ruled out by a stated constraint | "a tool the strategy ruled out" |
| 032 | Known risk area → likelihood ≥ Medium, strategy cited | "at least Medium" |
| 033 | Favour the Q3 journeys; say when a journey isn't one | "journeys the strategy names" |
| 034 | Per-surface floor of each touched surface | "the floor of each surface the feature touches" |
| 035 | Inherited items carry `cited`, `convention`, or `stated` | "carries the strategy's provenance" |
| 036 | Possibly-stale flag (mode drift, or newer commits on touched files). The history lookup is a read, and is skipped with a stated reason when unavailable | "possibly stale", "the history lookup is a read" |
| 037 | Step 1 says "Six outcomes" and lists six | — (asserted by row count) |

## Template

`test-plan-template.md` gains `## 4. Suggested UAT Scenarios` and `## 5. Regression Scope` after
`## 3. Test Conditions`. Environment and Exit Criteria are renumbered to 6 and 7, and the inline skeleton
matches. The exit criteria may cite "all P1 UAT scenarios passed — confirmed by <role>", as a plain
statement.
