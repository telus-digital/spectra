# Quickstart: Validating the Deployment Strategist

How to prove the feature works. Contracts: [command-interface](./contracts/command-interface.md),
[clarification-round](./contracts/clarification-round.md),
[document-contract](./contracts/document-contract.md),
[amendment-handoff](./contracts/amendment-handoff.md).

## 1. Repository checks (maintainer)

```bash
python3 -m unittest discover -s tests
```

```bash
python3 tools/generate_agent_docs.py --check
```

```bash
python3 tools/ship.py --dry-run
```

Expected: all pass. `test_deployment_strategy_flow.py` runs; `test_doc_output_paths.py` lists
`deployment-strategy.md` as a singleton with no earlier location; the constitution names
`<artifact-root>/DEPLOYMENT_STRATEGY.md`; manifest and catalog agree on version 1.20.0 and 12 commands;
the committed zip matches `spectra/`.

## 2. Install into a throwaway project

```bash
specify extension add --dev ./spectra
```

Run in a scratch Spec Kit project per `test/README.md`.

## 3. Scenarios

| # | Setup | Run | Expect |
|---|---|---|---|
| A | service repo: Dockerfile, k8s manifests, a deploy-on-merge workflow, a migrations folder | `/speckit-spectra-deployment-strategy` | classification `service`, `brownfield`; all six lenses; current state cited before recommendations; one Mermaid diagram matching the environments table; Q1 asked as a confirmation |
| B | library repo with a publish workflow and no deploy target | same | classification `library`; environments become release channels; data & schema `not applicable` with the search cited; Q4 confirmed not applicable; no cluster, registry, or migration recommended |
| C | repo A, answer "use your defaults" at question 2 | same | questions 2–5 not asked; recorded `default_taken` |
| D | repo A | `… --non-interactive` | no questions; all five `not_asked`; amendment `not_asked` |
| E | repo A plus `./hosting-standard.md` stating "prod deploys need CAB approval" | `… ./hosting-standard.md` | Q2 a confirmation citing the document; claim marked `claimed` |
| F | repo A with no `TEST_STRATEGY.md` | default run | pipeline lens reports CI checks as `verified`, records the missing test strategy as a gap, names `speckit.spectra.test-strategy` |
| G | repo with `docs/index.html` and no declared root | default run | publication signal surfaced; `documents/` recommended; handoff line uses the chosen path |
| H | repo A, constitution with no deployment principle; approve the amendment | default run | amendment items unchecked, invariants only, no environment names; closing link + `/speckit-constitution` line; constitution byte-identical |
| I | repo A, run twice, adding a pre-release overlay between runs | default run ×2 | one file; second run pre-fills answers; recommendations marked `new`/`adopted`/`carried` |
| J | a manifest containing a token | default run | token not reproduced; file cited with "secret present" |

## 4. Done when

Every scenario matches its expectation, and section 1 passes on the branch tip.
