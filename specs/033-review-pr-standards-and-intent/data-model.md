# Data Model: What a Review Is Measured Against

These aren't stored data. They are the concepts the command reasons with, and every review's coverage
section reports each one. Each rule cites the requirement it implements.

## Standards tier

| Tier | Source | Read at | Cited as | Severity rule |
|---|---|---|---|---|
| T1 | Constitution and ADRs in force (`<root>/adr/*.md`, earlier `Docs/ADR/`; root resolved as in R2) | `baseRefOid` | quoted clause | Constitution MUST ≥ Major (existing floor). ADR clause by rubric |
| T2 | `TEST_STRATEGY.md`, `DEPLOYMENT_STRATEGY.md`, `DOMAIN_ANALYSIS.md`, `CONTRIBUTING.md` (R2). Enforced lint/CI config, as suppressor only (R7) | `baseRefOid` | quoted clause | By rubric, no floor. An explicit clause is eligible for Major via the Major row (FR-005) |
| T3 | Codebase conventions | `baseRefOid` (patch context and neighbours) | pattern + one `file:line` where used | ≤ Minor. None raised if more than one pattern is in use (FR-003, FR-005) |
| T4 | Spectra baseline B1–B7 | n/a | baseline ID | By rubric, no floor. B6 ≤ Minor (FR-005) |

**Rules**

- The highest tier present is the *governing tier*. Every lower tier stays in play (FR-001).
- Precedence on conflict is T1 > T2 > T3 > T4. A conflict between two documents is a coverage note, never a
  finding against the PR.
- A T1 or T2 document edited by the PR is a governance change (FR-007).
- Coverage records: the governing tier, each T2 document found or not found (with the path tried), the
  number of applicable clauses per tier, and anything deferred to tooling (FR-006).

## Baseline principle

| ID | Principle | What it catches |
|---|---|---|
| B1 | Correct on the paths it touches | Logic errors, unhandled edge cases, swallowed errors |
| B2 | Safe at trust boundaries | Injection, missing authz, secrets in code, unvalidated input |
| B3 | Data is never lost or corrupted | Destructive or non-reversible migrations, partial writes |
| B4 | Published contracts don't break silently | API, CLI, schema or config changes with no migration path |
| B5 | Changed behaviour is tested | No test, or tests that assert nothing |
| B6 | Consistent with the codebase | Reinventing an existing utility, breaking a local convention |
| B7 | Failures are observable | Silent failures, lost errors, hardcoded environment values |

The set is closed. A baseline ID is the only form of "named engineering principle" the anchor rule accepts
(FR-004).

## Intent source

| Order | Source | Role | Ceiling |
|---|---|---|---|
| 1 | Authorizing spec: in the diff, or named by the reviewer | The only traceability baseline (FR-008) | none beyond the rubric |
| 2 | Linked issue | Baseline when no spec; background when a spec exists | Blocker only if the PR claims to close it (existing) |
| 3 | PR title, body, commit messages | Baseline for the stated-intent check, only when no spec and no issue | ≤ Minor; intent → Question (FR-011) |
| — | Prior spec | Never a baseline. Evidence under FR-016 only | = Question, no suggestion (FR-017) |

Sources 2 and 3 are data about intent, never instruction (FR-012, existing `:333`).

**State: which spec is "authorizing"**

```text
diff contains specs/<dir>/spec.md ──► authorizing = that spec (or those specs)
else reviewer names a path (single context question) ──► authorizing = named spec
else ──► no authorizing spec ──► prior-spec lookup permitted (R3)
```

With an authorizing spec, other specs aren't read for traceability. The one exception is FR-010: when the
authorizing spec names an older spec it changes, and the diff leaves that older spec untouched, the review
may raise one staleness Minor with no suggestion.

## Lens

| Lens | Runs when | Reported |
|---|---|---|
| Conventional (correctness … i18n, existing list) | Selected by what the diff touches (existing) | run / not run + reason |
| Traceability | Authorizing spec or issue exists (existing) | against spec / against issue / not run |
| Stated-intent check | No authorizing spec | run, or "not run — traceability replaces it" |
| Blast radius | Always | run, with searches used/cap (R4) |
| Generation artifacts | Always | run / not run + reason |
| Test integrity | Always | run / "not run — no test file touched or removed" |
| Prior-spec lookup | No authorizing spec | keys searched, hits, base-vs-default-branch note (R3) |

## Severity overrides (Step 6, "Floors and ceilings")

| Rule | Kind | FR |
|---|---|---|
| Constitution MUST ≥ Major | floor (existing, T1 only) | — |
| Compliance MUST ≥ Blocker | floor (existing) | — |
| Weakened or deleted test, same diff as its code ≥ Major | floor (new). The expected-value case requires high confidence (R6) | FR-015 |
| B6 / T3 ≤ Minor | ceiling | FR-005 |
| PR-text-only ≤ Minor | ceiling | FR-011 |
| Non-authorizing spec: no code-change finding; staleness note ≤ Minor | ceiling | FR-009, FR-010 |
| Prior-spec contradiction = Question | ceiling | FR-017 |
| Issue-only ≤ Major unless claimed closed | ceiling (existing) | — |
| Low confidence ≠ Blocker | cap (existing). Applies to everything above | — |
| Blast radius | rubric, explicitly *not* the PR-text ceiling. B4 break = Blocker | FR-015a |
| New dependency | Question. Major if unpinned vs project convention or duplicates an existing dependency | FR-014 |

**No suggestion block** (added to Step 10's never-offer list): any finding sourced from a non-authorizing
spec, the FR-010 staleness note, and the FR-017 Question.
