# Data Model: Spec Persistence Model in the Methodology Agent

Every entity below lives in the agent's prompt and in the one document it writes,
`<artifact-root>/ENGINEERING_METHODOLOGY.md`. Nothing is stored anywhere else.

## Persistence model candidate

One lens 4 candidate per model, four in all, using the existing candidate record (Step 7). Key order is
unchanged.

| Field | Value |
|---|---|
| statement | The model's guardrail text from [contracts/persistence-guardrail.md](contracts/persistence-guardrail.md), MUST, with the shared preamble; for Hybrid, with the accepted mapping |
| id | `em-spec-lifecycle-traceability-<hash>`, computed once from lens + normalized statement, then frozen |
| lens | Spec lifecycle & traceability |
| section | Development Workflow, or the project's equivalent |
| evidence | Brownfield: the signal's count and up to three citations (research R2). Greenfield: "default: Hybrid" for Hybrid; "offered alternative" for the others |
| basis | `observed` when its signal was found; otherwise `aspirational` |
| decision | `accepted` \| `declined` \| `skipped` \| `not_asked` |
| status | `new` \| `amends: <Principle>` \| `adopted: <Principle>` |
| origin | `methodology` |

**Validation**

- At most one of the four is `accepted`. Accepting one declines the other three in the same answer.
- Skip sets all four to `skipped`, a non-interactive run to `not_asked`, and "use your defaults" accepts
  the recommended one (question disposition `default_taken`).
- The four count as **one** slot against the five-candidate cap (FR-006).
- A reworded statement keeps its ID.

**State transitions** (per run, then across runs)

```text
generated ──(round)──► accepted | declined | skipped | not_asked
accepted ──(re-run finds the constitution asserts it)──► status adopted: <Principle>   (never reverted)
declined ──(re-run)──► offered as a selectable option, not as a new candidate; named as "declined last run"
skipped / not_asked ──(re-run)──► undecided, offered again
```

## Persistence mapping (Hybrid only)

A map from change type to persistence value.

| Key | Allowed values | Proposed default (FR-011) |
|---|---|---|
| `feature` | `living` \| `flow-forward` \| `—` | `flow-forward` |
| `fix` | same | `living` |
| `refactor` | same | `living` |
| `hotfix` | same | `living` |
| `docs` | same | `—` if the mode-choice table says no spec, else `living` |
| `spike` | same | `—` if the mode-choice table says no spec, else `living` |

**Validation**

- All six keys are present once Hybrid is accepted.
- `—` is valid only for a type the accepted mode-choice table marks "spec required: no". When question 3
  adopted no table, `—` is replaced by `living`, and the document notes it.
- The mapping is carried in the Hybrid statement (always) and mirrored as the mode-choice table's
  **Persistence** column (when the table exists). Re-runs read it back from the statement (research R4).

## Front matter: `persistence`

Added to the command-owned YAML front matter, after `autonomy`.

| Value | When |
|---|---|
| `living` \| `flow-forward` \| `flow-back` \| `hybrid` | The matching candidate is `accepted` |
| *(key absent)* | Question 5 skipped, unanswered, or not asked (non-interactive), or a prior file from before this feature |

`clarification.asked` and `answered` keep counting out of ten.

## Question 5 record (Decisions and sources)

The same record every question has: the question, the recommended option with its evidence, the answer
taken, and its disposition (`answered` | `default_taken` | `skipped` | `not_asked`). For Hybrid, the
answer records the accepted mapping, including any free-text adjustment.

## Persistence reference (document body)

Written in the Spec lifecycle & traceability section on every run.

- **A model accepted**: the model's name, one line on when it applies (delivered = merged to the default
  branch), and a table with one row per phase (specify, plan, tasks, implement, converge) → obligation.
  For Hybrid, the mapping, or a pointer to the mode-choice table's Persistence column.
- **No model accepted**: one sentence saying no spec persistence model was chosen and that question 5
  was skipped, unanswered, or not asked.

## Relationships

```text
Question 5 answer ──decides──► 4 persistence model candidates (1 accepted max)
                   └─decides──► other lens 4 candidates (follow the model unless excluded)
Hybrid accepted ──carries──► persistence mapping ──mirrored in──► mode-choice table Persistence column
accepted candidate ──listed in──► Constitution input (unless adopted) ──consumed by──► /speckit-constitution
accepted candidate ──sets──► front matter `persistence`
```
