# Data Model: Safe Handoffs Between the Foundation Agents

These "entities" are Markdown documents and the records inside them. Nothing is stored anywhere else.

## Feeder singleton

One standing document per feeder, at a fixed path under the artifact root.

| Field | Values | Notes |
|---|---|---|
| path | `<root>/DOMAIN_ANALYSIS.md`, `<root>/ENGINEERING_METHODOLOGY.md`, `<root>/TEST_STRATEGY.md`, `<root>/DEPLOYMENT_STRATEGY.md` | Named in Principle VII |
| owner | `speckit.spectra.domain-analyzer`, `…methodology`, `…test-strategy`, `…deployment-strategy` | The only writer |
| `command` (front matter, first key) | `speckit.spectra.<agent>` | **New** for three feeders; methodology already writes it |
| `goal` (front matter) | `create` \| `update` | **New** for test-strategy and deployment-strategy |
| `amendment_state` (front matter) | `embedded` \| `partial` \| `absent` \| `none` \| `not_asked` | Kept in the two strategies; `none` means no constitution, so the goal is `create` |
| `constitution_input` (front matter) | integer | **New** for the two strategies: the count of accepted, not-adopted records |
| Constitution input section | see below | **Replaces** "Proposed constitution amendment" in the two strategies |

**Classification of an existing file at the path** (research R3):

```text
has command: speckit.spectra.<this agent>        → own prior run
no command:, has this agent's earlier signature  → own prior run (earlier version)
command: names another agent                     → report, write nothing
otherwise                                        → not written by this feeder: read as `claimed`;
                                                   replace only with consent; else show in session
```

## Policy source document

Written only by kb-vault, after approval.

| Field | Values | Notes |
|---|---|---|
| folder | `<root>/domain-analysis-source/` \| `<root>/engineering-methodology-source/` \| `<root>/test-strategy-source/` \| `<root>/deployment-strategy-source/` | Fixed; one kind per folder |
| filename | `NNN-<kebab-title>.md` | Number recomputed at write time across the folder |
| template | `<kind>-source-template`, else `kb-document-template` | Five-layer stack |
| Provenance section | sources by name, ingest date, redactions by kind | How feeders recognise it outside its folder |
| Gaps section | what the sources did not cover | Unchanged kb-vault rule |
| referred to | the owning command | Stated in the plan row and the report |

**Lifecycle**: created or updated by kb-vault only, under its approval gate. It is never written, moved,
or deleted by a feeder. It stays in place after the owning feeder runs.

## Evidence item

| Kind | Provenance token | Decides basis? | Decides adoption? |
|---|---|---|---|
| Code, history, configuration | citation (`verified` in deployment-strategy) | yes | no |
| A document's claim, including every policy source document | `claimed` | **no**: alone, it gives `aspirational` | no |
| Team answer | `stated` (strategies) / the round's decision | n/a | **yes**, through the round or gate |
| Convention | `convention` | n/a | no |

**Rule**: a candidate whose only evidence is `claimed` has basis `aspirational`. Where `claimed` and code
or history disagree, both are reported and code or history is current practice.

In domain-analyzer and methodology records, a `claimed` item is written inside the existing `evidence:`
line as `claimed: \`path\``. No key is added.

## Guardrail record (test-strategy, deployment-strategy)

One per drafted guardrail, accepted or not. Keys appear in this order:

| Key | Values |
|---|---|
| statement | MUST / SHOULD, in the constitution's voice; the team's wording where reworded |
| id | `ts-<section-slug>-<hash8>` \| `ds-<section-slug>-<hash8>`; computed once, then frozen |
| section | target constitution section, using the constitution's own names where it exists |
| basis | `observed` \| `aspirational` |
| decision | `accepted` \| `declined` \| `skipped` \| `not_asked` |
| status | `new` \| `amends: <principle>` \| `adopted: <principle>` |

**Decision transitions** (research R7):

```text
gate: approve                       → every shown record accepted, except those the reply names:
                                        named to decline → declined
                                        named to reword  → accepted, new statement, same id
gate: declined as a whole           → every record skipped
gate: no answer / non-interactive   → every record not_asked
re-run: declined                    → kept, never offered as new
re-run: skipped | not_asked         → offered again
re-run: accepted ∧ constitution asserts it → status adopted: <principle>  (never reverted; drift reported)
migration: - [x]                    → accepted
migration: - [ ]                    → not_asked ("unticked in the earlier version")
```

## Constitution input section

| Property | Rule |
|---|---|
| goal line | `Goal: **create** …` or `Goal: **update** …` |
| content | exactly the records with decision `accepted` and status other than `adopted: …` |
| entry keys | statement, id, placement (`add` \| `amends: <principle>`), basis |
| grouping | by target constitution section |
| empty | one sentence saying nothing was accepted; no hand-off command |
| owner | the command, not the template; written even if a template omits the section |

## Sibling read (all four feeders)

| Reader | Reads | Uses only |
|---|---|---|
| domain-analyzer | `TEST_STRATEGY.md`, `DEPLOYMENT_STRATEGY.md` | records with decision `accepted` (checked items in a checkbox-era file). **Changed** from reading them whole |
| methodology | `DOMAIN_ANALYSIS.md`, `TEST_STRATEGY.md`, `DEPLOYMENT_STRATEGY.md` | unchanged: accepted entries only |
| test-strategy | `DOMAIN_ANALYSIS.md`, `ENGINEERING_METHODOLOGY.md`, `DEPLOYMENT_STRATEGY.md` | records with decision `accepted` (checked items in a checkbox-era file) |
| deployment-strategy | `TEST_STRATEGY.md`, `DOMAIN_ANALYSIS.md`, `ENGINEERING_METHODOLOGY.md` | unchanged rule, extended to `TEST_STRATEGY.md`'s new records |

A clause a sibling's accepted record already covers is cited, not drafted.
