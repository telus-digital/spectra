# Contract: Who Owns Which Constitution Clause

Four agents hand input to `/speckit-constitution`. A clause must have exactly one source, so each agent proposes
only in its own rows below. Where it touches someone else's row, it cites that agent's document if it exists, or
names the agent's command if not. Every one of the four command files must agree with this table, and the tests
check that the referrals exist on both sides.

| Ground | Owner | Others refer |
|---|---|---|
| Methodology stack: SDD base, overlays, phase obligations | `methodology` | — |
| Work modes: change types, spec required, spikes | `methodology` | — |
| Requirements intake | `methodology` (BRD format → `brd`) | — |
| Spec lifecycle & traceability | `methodology` | — |
| Branching model, branch naming, lifecycle, merge strategy | `methodology` | `deployment-strategy` (**changed**: no longer proposes the branching model), `domain-analyzer` (**changed**: lens 7 removed) |
| Review & merge gates: PR expectations, approvals, issue linking, docs-in-same-PR | `methodology` | `domain-analyzer` (**changed**) |
| Commit convention, changelog | `methodology` | `domain-analyzer` (**changed**) |
| AI collaboration: autonomy level, AI/dev-workflow tools, secret handling for those tools | `methodology` | — |
| Governance & amendment process | `methodology` | `domain-analyzer` (**changed**) |
| Versioning scheme, how a release is cut, hotfix promotion | `deployment-strategy` | `methodology` |
| Environments, promotion, rollback, operability | `deployment-strategy` | `methodology`, `domain-analyzer` |
| Which checks gate where in the pipeline | `deployment-strategy` | `methodology` (review gates cite it for required checks) |
| Test levels, coverage floor and ratchet, UAT | `test-strategy` | `methodology` (TDD governs *when* tests are written only) |
| Domain invariants, bounded contexts, glossary | `domain-analyzer` | `methodology` (DDD records the commitment only) |
| Product languages, frameworks, dependency policy | `domain-analyzer` | `methodology` |
| Security, data sensitivity, architecture, reliability | `domain-analyzer` | — |

## Readers

| Reader | Reads | Binding entries |
|---|---|---|
| `review-pr` (T2) | `<root>/ENGINEERING_METHODOLOGY.md` | `decision: accepted` only (**new**) |
| `kb-vault` reserved map | routes an absorbed methodology to `<root>/ENGINEERING_METHODOLOGY.md`; when that file has `command: speckit.spectra.methodology` front matter, refers the source to the command instead of updating | — (**new**) |
| `deployment-strategy` sibling read | `ENGINEERING_METHODOLOGY.md` for the branching model | `decision: accepted` only (**new**) |
| `methodology` sibling read | `DOMAIN_ANALYSIS.md`, `TEST_STRATEGY.md`, `DEPLOYMENT_STRATEGY.md` | accepted entries; carried-over lens-7 records as prior answers |

## Suggested order (FR-031a)

`domain-analyzer` → `methodology` → `test-strategy` → `deployment-strategy`. The report lists only siblings whose
document does not exist.
