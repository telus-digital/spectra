# Contract: The Traceability Invariant

**Owned by**: `speckit.spectra.test-plan` — not by the template, and not overridable.

This is the product. Everything else in the document is context for it.

## The invariant, in both directions

**Forward.** Every acceptance criterion in the supplied specification reaches at least one test condition
— or appears as an uncovered item with a reason. Never absent from both.

**Backward.** Every test condition names the specification item it verifies, using that item's own
identifier.

A plan that satisfies one direction and not the other has failed. Forward-only produces conditions that
verify nothing anyone asked for; backward-only produces silent gaps, which is the failure mode the
document exists to prevent.

## Reference forms

In order of preference. The command never mints an identifier for a specification item, and never edits
the specification to add one.

| Form | When | Example |
|---|---|---|
| The spec's own identifier | The spec defines one | `FR-014`, `SC-003`, `NFR-002` |
| A composed story reference | An acceptance scenario, which Spec Kit numbers per story | `US2-AC1` — story 2, first acceptance scenario |
| A short verbatim quotation | The spec states the requirement in prose with no identifier | `"rejects a request with no signature"` (6–12 words, in quotation marks) |

**Why composition is needed.** Spec Kit's template numbers acceptance scenarios *within* each user story,
so `AC1` alone is ambiguous across six stories. `USn-ACn` is deterministic, so two runs on the same spec
produce the same reference. The story titles are given once in the scope section so the reference is
legible to a reader with the spec open.

## Coverage accounting

The run report states the count both ways:

```text
Traceability: 17 of 19 acceptance criteria covered by 23 conditions.
2 uncovered — 1 unresolved clarification, 1 untestable as written.
```

A plan is written even when the count is short. A plan is **not** written with the count concealed.

## Uncovered items: the four reasons, and their remedies

| Reason | Meaning | Remedy stated |
|---|---|---|
| `unresolved-clarification` | The criterion depends on a `[NEEDS CLARIFICATION]` marker still in the spec | `/speckit-clarify` |
| `untestable-as-written` | The criterion cannot be made falsifiable without a decision the spec does not contain | What decision is missing |
| `out-of-scope` | Deliberately excluded by the scope section | Who covers it, if anyone |
| `deferred` | Real, testable, and consciously not in this cycle | When, or by whom |

**The prohibition that makes this work: never invent the missing decision.** Where a requirement is
ambiguous, the command says so and produces no condition for it. A fabricated condition that resolves an
ambiguity by assumption is the worst available outcome here — it launders a guess into something a
stakeholder approves, and the guess becomes a requirement nobody agreed to.

## Absence claims

Two different statements, two different obligations.

| Statement | Requirement |
|---|---|
| "This behaviour is already covered" | Cite the test file that covers it |
| "No test covers this behaviour" | Cite the search: what terms, in what paths |

An unqualified "not covered" is never written. "No test referencing `SignatureVerifier` found under
`tests/`" is permitted; "there is no coverage for signature verification" is not — the first is a fact
about a search, the second is a claim about the system.

## Priority derivation

A condition inherits the priority of what it verifies.

| Verifies | Priority |
|---|---|
| An acceptance criterion of a P1 / P2 / P3 story | P1 / P2 / P3 |
| A functional requirement not reachable from any story | P2 |
| …that is a prohibition, safety, or data-integrity property | **P1**, regardless of story |
| A success criterion | The priority of the story it measures, else P2 |

Only **P1** conditions gate the exit criteria. Where the specification carries no priorities at all, the
command says so and derives priority from the risk table's impact axis alone.

**Why prohibitions are promoted.** A "MUST NOT" requirement usually has no user story — nobody writes a
journey about the thing that must not happen — and it is exactly the requirement whose violation is
unrecoverable. Left at P2 it would fall outside the exit criteria that gate the release.

## Level assignment

The level is the cheapest lens that can actually verify the condition, drawn from the resolved
vocabulary, and constrained by what the project can run.

| Constraint | Rule |
|---|---|
| Vocabulary | A name from the project's test strategy, else the constitution's, else `unit` · `integration` · `api-contract` · `end-to-end` · `manual` |
| Runnability | No level or tool the project's dependency manifests cannot support. No browser anywhere → no browser-driven level |
| Cheapness | Assign to the cheapest level that can verify the condition, not the most thorough |
| `manual` | Always available, even where the strategy omits it |

**Why `manual` survives an inherited vocabulary.** A strategy decides what to automate. A plan must be
able to place a condition no automated lens will ever cover — a visual check, a third-party sandbox
interaction, an accessibility walkthrough. Without `manual` those conditions would land in "explicitly
not covered", which would be false: they are covered, by a person.
