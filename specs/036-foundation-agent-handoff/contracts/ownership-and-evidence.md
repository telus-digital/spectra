# Contract: Ownership, Recognition, and Evidence

All six commands this feature touches must agree with this table. A row that one command's text
contradicts is a defect.

## Who writes what

| File or folder | Writer | Everyone else |
|---|---|---|
| `<root>/DOMAIN_ANALYSIS.md` | `speckit.spectra.domain-analyzer` | read only |
| `<root>/ENGINEERING_METHODOLOGY.md` | `speckit.spectra.methodology` | read only |
| `<root>/TEST_STRATEGY.md` | `speckit.spectra.test-strategy` | read only |
| `<root>/DEPLOYMENT_STRATEGY.md` | `speckit.spectra.deployment-strategy` | read only |
| `<root>/domain-analysis-source/NNN-*.md` | `speckit.spectra.kb-vault` | read only, cited `claimed` |
| `<root>/engineering-methodology-source/NNN-*.md` | `speckit.spectra.kb-vault` | read only, cited `claimed` |
| `<root>/test-strategy-source/NNN-*.md` | `speckit.spectra.kb-vault` | read only, cited `claimed` |
| `<root>/deployment-strategy-source/NNN-*.md` | `speckit.spectra.kb-vault` | read only, cited `claimed` |
| `.specify/memory/constitution.md` | `/speckit-constitution`, run by the user | read only, for all six |

kb-vault's write scope no longer includes any singleton. No feeder's write scope includes any `-source`
folder.

## How a file at a singleton path is recognised

| Header | Classified as | The feeder does |
|---|---|---|
| `command: speckit.spectra.<this agent>` | own prior run | re-run rules: carry, match by ID, mark adoption |
| no `command:`, this agent's earlier-version signature | own prior run, earlier version | the same, and the file gains `command:` on rewrite |
| `command:` naming another agent | misplaced | report it; write nothing |
| anything else | not written by this feeder | read as `claimed`; ask consent before the round (not counted); no consent or non-interactive → write nothing, show the document in the session |

Earlier-version signatures: see research R3.

## How imported knowledge is read

| Feeder | Reads by path | Also reads | Label |
|---|---|---|---|
| domain-analyzer | `<root>/domain-analysis-source/` | any kb-vault document under the root, by its Provenance section, where it touches domain ground | `claimed` |
| methodology | `<root>/engineering-methodology-source/` | the same, for workflow ground | `claimed` |
| test-strategy | `<root>/test-strategy-source/` | the same, for testing ground | `claimed` |
| deployment-strategy | `<root>/deployment-strategy-source/` | the same, for deployment ground | `claimed` (existing provenance) |

`claimed` never sets basis to `observed`, never moves a measured figure, and never adopts a guardrail.

## What each feeder hands to the constitution

| Feeder | Section | ID prefix | Hand-off line names |
|---|---|---|---|
| domain-analyzer | Constitution input | `da-` | `"Constitution input" section of <path>/DOMAIN_ANALYSIS.md` |
| methodology | Constitution input | `em-` | `… ENGINEERING_METHODOLOGY.md` |
| test-strategy | Constitution input | `ts-` | `… TEST_STRATEGY.md` |
| deployment-strategy | Constitution input | `ds-` | `… DEPLOYMENT_STRATEGY.md` |

Each hand-off is worded for its goal (create or amend). It is omitted when nothing is accepted, and is
never invoked by the agent.

## What review-pr treats as a standard

| Document | Standards are |
|---|---|
| `DOMAIN_ANALYSIS.md`, `ENGINEERING_METHODOLOGY.md` | unchanged: accepted records only |
| `TEST_STRATEGY.md`, `DEPLOYMENT_STRATEGY.md` | **new**: records with decision `accepted` (Constitution input, or an accepted record elsewhere in the document); in a checkbox-era file, `- [x]` items only. As for the other two, a body section describing a recommendation is not a finding source (clarification Q2, option A) |
| `-source` documents | never. They are not at a path review-pr reads |
