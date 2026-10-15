# Contract: Command Interface

**Command**: `speckit.spectra.deployment-strategy` — file `spectra/commands/deployment-strategy.md`

## Invocation

```text
/speckit-spectra-deployment-strategy [focus hint] [document references…] [--non-interactive]
```

| Input | Required | Behaviour |
|---|---|---|
| (none) | — | analyse the whole project |
| focus hint | no | weights the analysis; never drops a mandatory lens |
| local document references | no | read as inputs; claims are `claimed` (FR-005) |
| URL | no | never fetched; reported, local copy requested (FR-005) |
| `--non-interactive` | no | the only flag; removed before the hint is read (FR-032) |
| any other `--flag` | — | reported and ignored; never folded into the hint (FR-003) |

## Session flow

1. Read the project and referenced documents (FR-004 to FR-007).
2. Classify deployables and mode (FR-008 to FR-011) — never asked.
3. Resolve the artifact root (FR-035); a publication-signal choice, where needed, is asked here.
4. Clarification round — five questions, one per turn ([clarification-round.md](./clarification-round.md)).
5. Resolve the template (FR-036).
6. Work the six lenses and any conditional lenses (FR-012 to FR-020).
7. Write the one file (FR-034); on failure, output in session and stop (FR-041).
8. Report (FR-043).
9. Constitution check, amendment gate, handoff ([amendment-handoff.md](./amendment-handoff.md)).

## Front-matter `description`

Must state: what it reads; that it classifies what ships; the six lenses; five questions asked one at a
time with a recommendation and evidence; the output path `<artifact-root>/DEPLOYMENT_STRATEGY.md`; the
constitution handoff; and that it never edits the constitution, never edits source/CI/manifests/IaC,
runs nothing, and makes no network request.

## Never-list (no argument or approval enables any of these)

| Never | Requirement |
|---|---|
| write `.specify/memory/constitution.md`, in any run | FR-047 |
| create a constitution | FR-047 |
| modify source, CI workflows, manifests, IaC, or configuration | FR-049 |
| write more than one file | FR-034 |
| run any command, build, deploy, or query against infrastructure | FR-049 |
| make a network request, fetch a URL, accept a credential or token | FR-005, FR-049 |
| reproduce a secret | FR-007 |
| invent a value only the client or ops owner can supply | FR-024 |
| ask what the repository answers | FR-031 |
| let an answer overwrite a fact read from the repository | FR-023 |
| invoke `/speckit-constitution` | FR-048 |
| generate alert definitions or runbook procedure without an explicit request | FR-019 |

## Session report (Step 8), in order

1. Path written (resolved root). 2. Template used, by path. 3. Coverage of the analysis. 4. Deployables,
classes, mode, with deciding signals. 5. Per-lens summary, terminal-length, including the open-question
count. The document is not pasted.
