# Quickstart: Validating the spec persistence model

## Prerequisites

- Spec Kit ≥ 0.11.2 (`specify --version`), the working copy of this repository, and `python3`.
- A throwaway project per scenario, installed from the working copy:

```bash
specify init --here --ai claude && specify extension add --dev /path/to/spectra/spectra
```

## Static checks (run first)

```bash
python3 tools/generate_agent_docs.py --check
```

```bash
python3 -m unittest discover -s tests
```

```bash
python3 tools/ship.py --dry-run
```

Expected: all pass. The new `TheSpecPersistenceModel` assertions in `tests/test_methodology_flow.py` pin
the rules in [contracts/question-five.md](contracts/question-five.md) and
[contracts/persistence-guardrail.md](contracts/persistence-guardrail.md).

## Scenario 1 — Greenfield, Hybrid recommended (US1, US4)

1. In an empty project, run `/speckit-spectra-methodology`. Answer questions 1–4 with their
   recommendations.
2. At question 5: confirm it reads "Question 5 of 10", lists lens 4 candidates, and offers exactly five
   options with **Hybrid** recommended and the mapping shown inline.
3. Reply `Hybrid, but refactor is flow-forward`, then finish the round.

Expected in `docs/ENGINEERING_METHODOLOGY.md`:

- front matter `persistence: hybrid`;
- the mode-choice table has a Persistence column with `refactor` → flow-forward and the others as
  proposed;
- the Spec lifecycle section has the persistence reference table;
- the Constitution input holds one persistence guardrail containing the preamble, both models'
  obligations, the decision rule, and the mapping;
- Living Spec, Flow-Forward, and Flow-Back records are `declined`.

## Scenario 2 — Each model's guardrail stands alone (US2, SC-003)

For each of Living Spec, Flow-Forward, Flow-Back (and Hybrid from Scenario 1), re-run choosing it. From
the Constitution input entry alone, answer "edit the existing spec, or create a new directory?" for
`feature`, `fix`, `refactor`, `docs`, `spike`, and `hotfix`. Expected: 24 of 24 answerable, no phase
missing, and no agent-specific invocation syntax in the text.

## Scenario 3 — Brownfield signals (US3, SC-004)

Build three fixture repositories with a default branch and one delivered `specs/001-a/`:

| Fixture | History after delivery | Expected recommendation |
|---|---|---|
| living | one commit editing `specs/001-a/spec.md` | Living Spec, citing the commit |
| forward | `specs/002-b/spec.md` containing "extends spec 001" | Flow-Forward, citing the file |
| back | one commit editing `specs/001-a/tasks.md` only | Flow-Back, citing the commit |
| mixed | both the living and forward histories | Hybrid, naming both signals |

## Scenario 4 — Skip, defaults, non-interactive, re-run (US5, SC-005, SC-006)

- Answer **Skip** at question 5. Expected: no `persistence` key, every lens 4 record `skipped`, and the
  persistence reference is one sentence.
- Run with `--non-interactive`. Expected: question 5 `not_asked`, no key, nothing about persistence in the
  Constitution input.
- Re-run on the Scenario 1 output. Expected: question 5 opens "Last run you chose **Hybrid**; still
  right?" with the prior mapping, names the three declined models, and creates no new IDs.
- Delete the `persistence` key from a copy and re-run. Expected: asked as new.

## Scenario 5 — Nothing else changed

```bash
git diff --stat main -- . ':!specs/042-spec-persistence-model'
```

Expected: only the files listed in [plan.md](plan.md) under Source Code, including regenerated outputs and
the rebuilt zip. Nothing under `spectra_cli/`, no `VERSION` change, and no other command file.

## Results

**2026-11-04**

| Check | Result |
|---|---|
| Static checks: generator `--check`, full unittest suite (1840 tests), `ship.py --dry-run` | Pass |
| Install: `specify init --integration claude` then `specify extension add --dev` on Spec Kit 1.2.4 | Pass. Installs 1.31.0, and the rendered `speckit-spectra-methodology` skill holds the question 5 and persistence-guardrail text |
| Scenario 5: nothing else changed | Pass. Only the plan's Source Code files changed; `spectra_cli/` and `VERSION` untouched |
| Scenarios 1–4: interactive runs of the agent | Pass. Walked through by hand by the maintainer, as reported on 2026-11-04 |
