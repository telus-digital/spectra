# Quickstart: verifying uat resolves its feature like the implement command

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

All four must pass. `tests/test_uat_flow.py` pins every behaviour in
[contracts/resolution-behaviour.md](./contracts/resolution-behaviour.md).

## Manual (throwaway Spec Kit project with this extension installed from the branch)

Prerequisite: two features, `specs/001-a` and `specs/002-b`. Each has a `spec.md`, a `test-plan.md`, and a
`tasks.md` with a UAT phase holding one `agent` scenario the session can drive. `specs/003-c` has a
`spec.md` and no `tasks.md`.

| # | Setup | Run | Expect |
|---|---|---|---|
| M1 | `feature.json` → `specs/001-a`; variables unset | uat, no argument | First line announces `specs/001-a (from .specify/feature.json)`. The run confirmation names `specs/001-a`. On yes, ticks land in `specs/001-a/tasks.md`; the report's Feature row says "resolved from .specify/feature.json" |
| M2 | M1, plus `SPECIFY_FEATURE_DIRECTORY=specs/002-b` | no argument | Resolves 002-b and notes the record names 001-a; confirmation names 002-b |
| M3 | `SPECIFY_FEATURE_DIRECTORY=""`, record → 001-a | no argument | Empty treated as unset; resolves 001-a |
| M4 | record → 001-a | `specs/002-b` | Stops before reading anything; names both directories and the source; remedy block; nothing started or written |
| M5 | record → 001-a | `specs/001-a/spec.md` | Proceeds as M1 |
| M6 | record → 003-c | no argument | Stops: no `tasks.md`; remedy block; nothing written |
| M7 | delete `feature.json`; variables unset | `specs/001-a` | Stops; the argument is not used in its place; remedy block |
| M8 | `SPECIFY_INIT_DIR=/nonexistent` | no argument | Stops naming the value and reason |
| M9 | deny the shell read when the agent asks | no argument | Stops; says the variables couldn't be checked; nothing started |
| M10 | M1, and change `feature.json` to 002-b while the run waits at the run confirmation | answer yes | Ticks, evidence and report all land in 001-a; 002-b untouched |
| M11 | M1, `--non-interactive` | no argument | Announces non-interactive, then the feature; reports what it would attempt; starts and writes nothing. With `feature.json` deleted, it stops instead |
| M12 | after `/speckit-implement` on 001-a, accept the after-implement offer | — | Resolves 001-a with no path typed |
| M13 | A second Spec Kit project at `../other` with `specs/001-x` (with `tasks.md`); `SPECIFY_INIT_DIR=../other` | no argument | Resolves `../other/specs/001-x`, then the out-of-project stop fires; nothing started or written in either project |

After every stop, `git status` shows no change and `.specify/feature.json` is unchanged. After a resolved
run, changes are limited to the resolved feature's `tasks.md` `[UAT]` lines, its `uat/<run-stamp>/`, and
its `uat-report.md`.
