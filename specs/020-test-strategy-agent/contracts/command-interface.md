# Contract — Command Interface

**Command**: `speckit.spectra.test-strategy` · **File**: `spectra/commands/test-strategy.md` ·
**Effect**: read-write

The command's public surface. Anything not listed here is not part of the contract.

## Name and invocation

| | |
|---|---|
| Manifest name | `speckit.spectra.test-strategy` |
| Namespace rule | `speckit.<extension-id>.<command>`, so the middle segment is `spectra` (Principle III) |
| Argument form | Generic `$ARGUMENTS` — never an agent's invocation syntax |
| Trigger | Differs per agent; the extension's README and the agent's command list show the exact form |
| Phase | Foundation. Runs alongside `constitution` and `domain-analyzer`, before any feature work |

## Arguments

| Argument | Required | Meaning |
|---|---|---|
| Focus hint | **No** | Free text weighting the analysis — a lens, a surface, a concern. Never narrows the four mandatory lenses (FR-004) |

**The command runs with no arguments** (FR-004). That is the expected invocation.

**Not accepted, by design**: a repository URL, a credential, a token, or any instruction to fetch or
clone (FR-050). Offered one, the command explains it reads only the current project and makes no
network request.

## Effect and write scope

| | |
|---|---|
| Files written | **Exactly one**: `<artifact-root>/test-strategy/TEST_STRATEGY.md` (FR-037, FR-042, FR-048) |
| Files modified | none other than that one, rewritten in place on a re-run |
| Files never written | `.specify/memory/constitution.md` — in **any** run, approved or not (FR-032) |
| Files never modified | source, test files, test framework config, coverage config, CI workflow definitions (FR-047) |
| Commands invoked | none. `/speckit-constitution` is named as something the **user** runs (R7) |
| Network | none (FR-050) |
| Processes run | none by default. The project's coverage tool may be run **only** after an explicit confirmation naming the command (R2) |

**The write happens once, at the end.** Everything before it is reading, analysing, and asking.

## Refusals and degradations

| Condition | Behaviour |
|---|---|
| Repository empty or near-empty | Produce **no** strategy. Name what was looked for and not found, and what would make a run useful (Edge Cases) |
| No project-wide text search available | Continue on what can be traversed, state the limitation, report reduced coverage (FR-013) |
| Declared artifact root unusable — absolute, or containing `..` | Say why, fall back to the default (FR-042, Edge Cases) |
| `docs/` shows a publication signal and no root is declared | Surface it, recommend `documents/`, let the user choose; take the non-publishing option where the choice cannot be obtained (FR-042) |
| Coverage tooling absent | `provenance: unavailable`, floor conditional, tooling recommended as step one (FR-023) |
| Coverage report present but stale | Use it, label it `reported`, state its date (FR-026) |
| Tests present but not executing | Report as distinct from tests-absent (Edge Cases) |
| No constitution | Report nothing to amend, name the command that creates one, create nothing (FR-030) |
| Existing principle conflicts with a recommendation | Surface as a finding; draft no amendment that silently overrides it (FR-033) |
| Resolved template omits the proposed-amendment section | Note the omission, give the text in the session, still offer the handoff (FR-036) |
| Strategy document not writable, or root cannot be created | Report the failure, output the strategy in the session, write nowhere else (Edge Cases) |
| Non-interactive session | Announce once, write the document, draft the amendment, take no approval (FR-034) |
| User directs a change contradicting the evidence | Make the change; record the disagreement in the document (FR-046) |

**The command never fails a run over an input it can describe.** The only stop is a repository with
nothing to read.

## What it does not do

- No per-test findings, no diagnosis of individual failing or flaky tests, no test files opened for
  repair (FR-049) — that is `flaky-test-detector`'s scope.
- No coverage gap analysis per file and no automation backlog — those are the roadmap's `test-coverage`
  and `test-automation` agents, which execute *against* this strategy (spec Clarifications).
- No configuration applied. Enforcement changes are stated for the team to make (FR-047).
- No constitution created (FR-030) and none amended (FR-032).
