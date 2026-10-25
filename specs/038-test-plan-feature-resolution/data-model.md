# Data Model: Test plan finds its feature the way the planner does

Nothing here is stored by Spectra. These are the facts the command reads and the states one run passes through.

## Inputs

| Input | Source | Read how | Notes |
|---|---|---|---|
| `SPECIFY_INIT_DIR` | environment | the one shell read (R2), once | empty = unset |
| `SPECIFY_FEATURE_DIRECTORY` | environment | the same read | empty = unset |
| `feature_directory` | `<root>/.specify/feature.json` | file read; re-read once before the handoff (R4) | never written |
| Argument path | `$ARGUMENTS` minus `--non-interactive` | text | optional confirmation (R3) |

## Resolution result

| Field | Value |
|---|---|
| `root` | project root: `SPECIFY_INIT_DIR`, else the nearest `.specify/` |
| `feature_dir` | project-relative feature directory |
| `spec` | `<feature_dir>/spec.md` |
| `source` | `SPECIFY_FEATURE_DIRECTORY` \| `.specify/feature.json` |
| `record_disagreed` | the feature record's value, when the variable won and the record named another directory; else none |

## Stops (all write nothing and emit no handoff)

| Stop | Fires when | Says |
|---|---|---|
| `env-unreadable` | the shell read is denied or fails | the variables couldn't be checked, so the planner's feature can't be confirmed |
| `init-dir-invalid` | `SPECIFY_INIT_DIR` is set but names no directory, or one without `.specify/` | the value and the reason; unset it |
| `no-feature` | variable unset and no `feature.json` | neither source is set; remedy block |
| `record-unusable` | `feature.json` unparseable or has no `feature_directory` | the file and the reason; remedy block |
| `dir-missing` | resolved directory missing, or has no `spec.md` | the directory, its source; remedy block |
| `argument-mismatch` | argument isn't the feature directory or its `spec.md` | argument, resolved directory, source; remedy block |
| `out-of-project` | *unchanged* | *unchanged* |
| `unusable-spec` | *unchanged usability test* | *unchanged* |

The remedy block is defined once (research R6).

## Run states

```text
read env ──fail──▶ stop(env-unreadable)
   │
resolve root ──invalid──▶ stop(init-dir-invalid)
   │
resolve feature ──▶ stop(no-feature | record-unusable | dir-missing)
   │
announce(feature_dir, source, record_disagreed)
   │
match argument ──mismatch──▶ stop(argument-mismatch)
   │
out-of-project / usability ──▶ existing stops
   │
Steps 2–15 (unchanged) ──▶ test-plan.md written (or rewrite declined / non-interactive no-rewrite)
   │
agreement check (R4) ──changed──▶ report, no handoff
   │
Step 17 handoff
```

## Announcement (first statement of every resolved run)

```text
Feature: specs/038-test-plan-feature-resolution (from .specify/feature.json)
```

With the variable set and the record disagreeing:

```text
Feature: specs/021-signed-webhooks (from SPECIFY_FEATURE_DIRECTORY; .specify/feature.json names specs/038-test-plan-feature-resolution)
```
