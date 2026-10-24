# Data Model: An Interactive Domain Analyzer That Feeds the Constitution

All entities live in one Markdown document, `<artifact-root>/DOMAIN_ANALYSIS.md`: run-level values in YAML front
matter, candidates and the Constitution input in the body.

## Run goal

| Field | Values | Rule |
|---|---|---|
| `constitution` | `present` · `absent` | `absent` also when the file is empty or unreadable |
| `goal` | `create` · `update` | `create` ⇔ `absent`. Stated as the run's first output (FR-001); decides the handoff (FR-016) |
| `mode` | `greenfield` · `brownfield` · `mixed` | classified from evidence, never asked |

## Candidate guardrail

| Field | Values | Rule |
|---|---|---|
| statement | MUST/SHOULD sentence with rationale | SME wording wins where they changed it |
| `id` | `da-<section-slug>-<hash>` | computed once from section + normalized statement, then frozen (FR-018) |
| lens | one of the seven | at most five candidates per lens (FR-006) |
| `section` | target constitution section | the existing constitution's names where one exists |
| `evidence` | ≥1 project-relative path, ` ; `-separated | required (FR-005) |
| `basis` | `observed` · `aspirational` | required (FR-005) |
| `confidence` | `High` · `Medium` · `Low` | |
| `decision` | `accepted` · `declined` · `skipped` · `not_asked` | set by the round |
| `status` | `new` · `amends: <principle>` · `adopted: <principle>` | `adopted` only on a re-run, only for `accepted` |

Record key order is fixed: `id`, `section`, `evidence`, `basis`, `confidence`, `decision`, `status`.

### Decision transitions

```text
(generated) ──round──▶ accepted | declined | skipped | not_asked

re-run:
  accepted   ─ stays accepted; ─▶ status adopted when the constitution now asserts it
  declined   ─ stays declined; never re-offered as new
  skipped    ─ re-offered (undecided)
  not_asked  ─ re-offered (undecided)

legacy checkbox file:
  - [x]  ─▶ accepted
  - [ ]  ─▶ not_asked (undecided), re-offered marked "unticked in the earlier version"
```

"Undecided" is not a `decision` value: it names `skipped` and `not_asked` together. A non-interactive re-run
therefore leaves an unticked legacy item `not_asked`.

### Status transitions

```text
new / amends ─▶ adopted: <principle>     (accepted only; never reverted)
adopted whose principle has since gone  ─▶ stays adopted; drift reported
```

## Question

| Field | Values | Rule |
|---|---|---|
| `n` | 1–8 | 1 = domain; 2–8 = lenses 1–7 in order |
| `ask` | quoted text | |
| `recommended` | quoted text | exactly one option per question |
| `answer` | quoted text | |
| `disposition` | `answered` · `default_taken` · `skipped` · `not_asked` | all eight always recorded |

Options per lens question: Recommended set · Codify only what exists · Full set · Skip; a coinciding option
becomes Choose individually. A decision derives from the option: Codify → observed accepted, rest declined;
free-text pick → named accepted, rest declined; Skip → all `skipped`; unanswered → all `not_asked`.

## Constitution input

Derived, never edited independently: exactly the candidates with `decision: accepted` and `status` not
`adopted: …`, grouped by `section`, each carrying `id`, `placement` (`add` · `amends: <principle>`), and
`basis`. Opens with a goal line. Empty ⇒ one sentence and no handoff command.
