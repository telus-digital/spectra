# Quickstart: verifying test-plan resolves its feature like the planner

## Automated

```bash
python3 -m unittest discover -s tests
```

```bash
python3 tools/generate_agent_docs.py --check
```

```bash
python3 tools/build_package.py
```

```bash
python3 tools/ship.py --dry-run
```

All four must pass. `tests/test_test_plan_flow.py` pins every behaviour in
[contracts/resolution-behaviour.md](./contracts/resolution-behaviour.md).

## Manual (throwaway Spec Kit project with this extension installed from the branch)

Prerequisite: two features, `specs/001-a` and `specs/002-b`, each with a `spec.md`.

| # | Setup | Run | Expect |
|---|---|---|---|
| M1 | `feature.json` → `specs/001-a`; variables unset | test-plan, no argument | Announces `specs/001-a (from .specify/feature.json)`; writes `specs/001-a/test-plan.md`; handoff names it. Then `setup-plan.sh --json` reports `FEATURE_DIR` …/001-a |
| M2 | M1, plus `SPECIFY_FEATURE_DIRECTORY=specs/002-b` | no argument | Resolves 002-b, notes the record named 001-a; `setup-plan.sh` agrees |
| M3 | `SPECIFY_FEATURE_DIRECTORY=""`, record → 001-a | no argument | Empty treated as unset; resolves 001-a |
| M4 | record → 001-a | `specs/002-b/spec.md` | Stops before reading; names both directories and the source; remedy block; nothing written |
| M5 | record → 001-a | `specs/001-a/` | Proceeds as M1 |
| M6 | delete `feature.json`; variables unset | no argument | Stops; remedy block; nothing written |
| M7 | `SPECIFY_INIT_DIR=/nonexistent` | no argument | Stops naming the value and reason |
| M8 | deny the shell read when the agent asks | no argument | Stops; says the variables couldn't be checked; no fallback |
| M9 | M1, and change `feature.json` to 002-b while the run is at the existence gate | answer the gate | `test-plan.md` written in 001-a; no handoff; report names the change |
| M10 | after M1, through the after-specify hook on a fresh `specify` | accept the offer | Resolves the feature specify just recorded, with no path |
| M11 | A second Spec Kit project at `../other` with `specs/001-x`; `SPECIFY_INIT_DIR=../other` | no argument | Resolves `../other/specs/001-x`, then the out-of-project stop fires; nothing written in either project |

After each run, `git status` shows at most one changed file, `test-plan.md`, and `feature.json` unchanged.
