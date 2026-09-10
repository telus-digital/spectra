# Contract — The Strategy Document

What the command writes, where, and how its shape is resolved.

## Location

```text
<artifact-root>/test-strategy/TEST_STRATEGY.md
```

| Rule | Source |
|---|---|
| `<artifact-root>` is the project's declared root, read case-insensitively from `Artifact root:` in the constitution | Principle VII |
| An absolute root, or one containing `..`, is refused with a stated reason and the default is used | Principle VII, FR-042 |
| Default is `docs/`, **after** the publication check | Principle VII, FR-042 |
| Publication signals: `mkdocs.yml`, `docusaurus.config.*`, `docs/_config.yml`, `docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, a Pages configuration pointing at `docs` | Principle VII |
| A signal firing with no declared root: surface it, recommend `documents/`, let the user choose | Principle VII |
| Choice unobtainable: take the non-publishing option | Principle VII |
| The command states the declaration line and **never writes it** | Principle VII |
| Dedicated subfolder, holding exactly one artifact type | Principle VII |
| **No sequence number** | FR-042a — the deviation, argued in [plan.md](../plan.md) |

**One file. Ever.** A re-run rewrites this path in place. No second file, no `NNN`, no supersede
marker, no index (FR-037, FR-048).

**Spectra's own repository trips the publication check** — `docs/index.html` is present and `main`
`/docs` is served by Pages — so a self-hosted run must surface the choice. That makes the check
verifiable here rather than only in a fixture.

## Template resolution

First readable, non-empty layer wins (FR-039, Principle VIII):

1. `.specify/templates/overrides/test-strategy-template.md`
2. `.specify/presets/<preset-id>/templates/test-strategy-template.md`
3. `.specify/extensions/spectra/templates/test-strategy-template.md`
4. `.specify/templates/test-strategy-template.md`
5. The command's own inline skeleton

**No single path is hard-coded** (FR-039). **The resolved path is reported in the session** (FR-041).
Guidance comments and `[PLACEHOLDER]` tokens are stripped whichever layer supplied the template.

## Sections

The shipped template declares, in order:

| # | Section | May an override drop it? | What the command does if dropped |
|---|---|---|---|
| 1 | Classification and evidence | yes | notes the omission; still reports the mode in the session |
| 2 | Testable surfaces | yes | notes the omission |
| 3 | Unit testing | yes | notes the omission |
| 4 | Integration testing | yes | notes the omission |
| 5 | API contract testing | yes | notes the omission |
| 6 | End-to-end testing | yes | notes the omission |
| 7 | Coverage floor | yes | notes the omission; still states the floor and its baseline in the session |
| 8 | Recommendations summary | yes | notes the omission |
| 9 | Proposed constitution amendment | yes | gives the amendment text in the session and still offers the handoff (FR-036) |
| 10 | Sources consulted and coverage of analysis | yes | notes the omission; still reports coverage in the session |

**Honour, do not repair** (Principle VIII, FR-040). Sections are not added, renamed, or reordered. A
dropped section is noted, never reinstated.

**Heading parity is enforced.** `test_document_templates.py` extracts the H2 list from the shipped
template and from the fenced block under the command's `## Inline template skeleton` heading, strips
trailing `<!-- … -->` annotations, and asserts the two lists are equal **and in the same order**. The
command file must therefore carry an `Inline template skeleton` section whose fenced block declares
exactly the ten headings above, in order. This is verified in the repository, not in a scratch project.


## What the template does NOT govern

The honesty rules stay with the command, exactly as `review-pr` keeps its revision anchor and `impact`
keeps its citation rule out of their templates:

- the evidence-or-convention marker on every recommendation (FR-043);
- the searched-and-not-found form for an absence claim (FR-044);
- `floor <= baseline` in brownfield (FR-022);
- the `measured` / `reported` / `unavailable` provenance labels (FR-023, FR-026);
- the tool-tier rule and its no-network caveat (FR-016, R9);
- the greenfield / brownfield / mixed declaration (FR-045);
- the coverage-of-analysis statement (FR-013).

An override that removes "Sources consulted" removes the section. It cannot make the command stop
knowing what it did not read, and the command still reports coverage in the session.

## Front matter

Written by the command, not the template: `mode`, `generated` (with time of day), `surfaces`,
`template` (resolved path), `coverage_of_analysis`, `amendment`. See
[data-model.md](../data-model.md) §8.
