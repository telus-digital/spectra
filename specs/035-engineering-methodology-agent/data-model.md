# Data Model: Engineering Methodology Agent

The agent's data lives in one Markdown file, `<artifact-root>/ENGINEERING_METHODOLOGY.md`: YAML front matter plus
records in the body. These are the entities and the values each field may take.

## Run mode

| Field | Values | Rule |
|---|---|---|
| `mode` | `brownfield` \| `greenfield` | ≥2 signals → brownfield; 0 → greenfield; 1 → mixed, team decides (FR-002) |
| `signals` | subset of `source`, `workflow-config`, `commits>10` | each found signal cited in the first output; `source` = a file of more than 20 non-blank lines changed in more than one commit, or at least five such files when the history has at most one commit (including no history) |
| `mode_basis` | `detected` \| `confirmed` \| `corrected` | `confirmed` or `corrected` only after a mixed reading |

## Run goal

| Field | Values | Rule |
|---|---|---|
| `goal` | `create` \| `update` | `create` when `.specify/memory/constitution.md` is absent, empty, or unreadable |
| `constitution_version` | string or absent | reported in the first output when stated |

## Lens

Nine fixed lenses, ordered: `methodology-stack`, `work-modes`, `requirements-intake`, `spec-lifecycle`,
`branching-integration`, `review-merge-gates`, `change-records`, `ai-collaboration`, `governance-evolution`.

| Field | Values | Rule |
|---|---|---|
| `target_section` | constitution section name | project's own names, else the R9 defaults |
| `current_practice` | prose + citations | brownfield: required, cited; greenfield: "no practice to report" |
| `referred` | list of `{ground, owner, document?}` | sibling-owned ground touched by evidence (FR-018) |
| `candidates` | 0–5 Candidate guardrails | empty → "nothing to propose" with what was searched |

## Candidate guardrail

| Field | Values | Rule |
|---|---|---|
| `id` | `em-<lens-slug>-<hash>` or carried-over `da-…` | frozen at first computation (R11) |
| `lens` | one Lens | — |
| `statement` | one rule, MUST/SHOULD wording | a free-text reword keeps the ID |
| `evidence` | paths or git facts | required in brownfield mode |
| `basis` | `observed` \| `aspirational` | greenfield → always `aspirational` |
| `decision` | `accepted` \| `declined` \| `skipped` \| `not_asked` | only `accepted` is binding (FR-034) |
| `status` | `new` \| `amends: <principle>` \| `adopted: <principle>` | `adopted` is never reverted |
| `origin` | `methodology` \| `domain-analyzer` | `domain-analyzer` for records carried over from lens 7 (R8) |

**Transitions** (`status`): `new` → `adopted` when the constitution asserts it on a later run. `amends:` →
`adopted` likewise. `adopted` → `adopted` always, and a principle later removed is reported as drift.

**Transitions** (`decision`, across runs): the prior decision is the prefilled answer. `declined` stays declined
unless the team explicitly accepts it again. `not_asked` is offered again.

## Methodology overlay

| Field | Values | Rule |
|---|---|---|
| `id` | `em-overlay-<name>` | frozen |
| `name` | `tdd` \| `bdd` \| `ddd` \| `contract-first` \| `adr-driven` \| team-named | a team-named overlay needs ≥1 stated obligation |
| `practised` | `yes` \| `partial` \| `no`, with evidence | brownfield only |
| `adopted` | bool | from question 1 |
| `strictness` | `MUST` \| `SHOULD` | from question 2 |
| `scope.change_types` | subset of `feature`, `fix`, `refactor`, `docs`, `spike`, `hotfix` | from question 2 |
| `scope.modules` | paths or `all` | optional |
| `scope.code` | `new-and-changed` \| `all` | `new-and-changed` by default when `practised` ≠ `yes` (FR-015) |
| `obligations` | `{phase, obligation, evidence?}` rows | cells of the R7 matrix only; `evidence` required for implement-phase rows |
| `precedence` | ordered overlay names | required when two obligations conflict at one phase (FR-017) |

An adopted overlay produces **one** Candidate guardrail in lens `methodology-stack`, `id: em-overlay-<name>`,
whose statement renders its obligation rows as one MUST/SHOULD clause per phase, sharing the overlay's strictness
and scope. Lens 1 therefore holds at most five candidates (FR-008, FR-014).

## Autonomy level (lens 8)

One candidate whose statement is exactly one of: `human-checkpoint-every-phase` (default recommendation) |
`human-gates-spec-and-pr` | `autonomous-to-pr` (FR-011a). Question 9 picks the level; the lens's tools and
secrets candidates take the same decision as the level unless free text excludes them, and Skip leaves every lens 8
candidate `skipped`.

## Question

| Field | Values |
|---|---|
| `number` | 1–10 |
| `asks` | stack \| overlay strictness & scope \| lens 2–9 |
| `recommended` | option label + evidence |
| `prefilled` | prior answer, on re-run |
| `answer` | option label or free text |
| `disposition` | `answered` \| `default_taken` \| `skipped` \| `not_asked` |

## Constitution input

Exactly the candidates with `decision: accepted` and `status` not `adopted`, grouped by `target_section`, each
carrying `id`, `placement` (`add` \| `amends: …`), and `basis`. Opened by one line naming the `goal`. Empty means one
sentence and no `/speckit-constitution` line (FR-031).

## Front matter (command-owned)

```yaml
---
command: speckit.spectra.methodology
version: <extension version>
mode: brownfield
signals: [source, workflow-config, commits>10]
goal: update
constitution_version: 1.4.0
autonomy: human-checkpoint-every-phase
overlays:
  - {id: em-overlay-tdd, strictness: MUST, change_types: [feature, fix], code: new-and-changed}
template: .specify/extensions/spectra/templates/engineering-methodology-template.md
---
```
