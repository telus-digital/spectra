# Data Model: UAT finds its feature the way the implement command does

Spectra stores none of this. These are the facts the command reads and the states one run passes
through.

## Inputs

| Input | Source | Read how | Notes |
|---|---|---|---|
| `SPECIFY_INIT_DIR` | environment | the one shell read (R2), once, before the run confirmation | empty = unset |
| `SPECIFY_FEATURE_DIRECTORY` | environment | the same read | empty = unset |
| `feature_directory` | `<root>/.specify/feature.json` | one file read in Step 1; never re-read (FR-017a) | never written |
| Argument path | `$ARGUMENTS` minus `--env <value>` and `--non-interactive` | text | optional confirmation (R3) |
| `--env` | `$ARGUMENTS` | text | unchanged |
| `--non-interactive` | `$ARGUMENTS` or a session declaration | text | unchanged, except for the bullet in FR-018 |

## Resolution result

| Field | Value |
|---|---|
| `root` | `SPECIFY_INIT_DIR` if non-empty, else the nearest `.specify/` |
| `invoking_project` | the nearest `.specify/` above the current directory (out-of-project stop only) |
| `feature_dir` | project-relative feature directory; contains `tasks.md` |
| `source` | `SPECIFY_FEATURE_DIRECTORY` \| `.specify/feature.json` |
| `record_disagreed` | the record's value, when the variable won and the record named another directory; otherwise none |

`feature_dir` is fixed for the whole run. Step 6's ticks, Step 5's evidence folder and Step 8's report all
go to it (FR-017a).

## Stops (each writes nothing and starts nothing)

| Stop | Fires when | Says |
|---|---|---|
| `env-unreadable` | the shell read is denied or fails | the variables could not be checked, so the active feature cannot be confirmed |
| `init-dir-invalid` | `SPECIFY_INIT_DIR` is set but names no directory, or one with no `.specify/` | its value and the reason |
| `no-feature` | the variable is unset and there is no `feature.json` | neither source is set; remedy block |
| `record-unusable` | `feature.json` is unparseable, or has an empty or missing `feature_directory` | the file and the reason; remedy block |
| `dir-missing` | the resolved directory does not exist | the directory and its source; remedy block |
| `no-tasks` | the resolved directory has no `tasks.md` | nothing to accept until the tasks exist; remedy block |
| `argument-mismatch` | the argument is neither the feature directory nor its `spec.md` | the argument, the resolved directory, the source; remedy block |
| `out-of-project` | `feature_dir` lies outside `invoking_project` | *unchanged wording, measured against the invoking project* |

The remedy block is defined once (research R5).

## Run states

```text
read env ──fail──▶ stop(env-unreadable)
   │
resolve root ──invalid──▶ stop(init-dir-invalid)
   │
resolve feature ──▶ stop(no-feature | record-unusable | dir-missing | no-tasks)
   │
announce(feature_dir, source, record_disagreed)
   │
match argument ──mismatch──▶ stop(argument-mismatch)
   │
out-of-project ──outside──▶ stop(out-of-project)
   │
Step 2 reads (unchanged) ──no UAT phase──▶ say so, write nothing
   │
Step 3: incomplete-implementation gate ──▶ run confirmation (names feature_dir)
   │                                         │
   │                                   declined ──▶ all `blocked — run declined`; report written; no ticks
   ▼
Steps 4–9 (unchanged), every write under feature_dir
```

Non-interactive: the declaration is announced before the feature line. Resolution runs as above. A stop
still stops. A resolved run then reports what it would attempt, starts nothing, and writes nothing.

## Announcement (first statement of every resolved run)

```text
Feature: specs/039-uat-feature-resolution (from .specify/feature.json)
```

With the variable set and the record disagreeing:

```text
Feature: specs/021-signed-webhooks (from SPECIFY_FEATURE_DIRECTORY; .specify/feature.json names specs/039-uat-feature-resolution)
```

## Run confirmation (Step 3), the feature line added

```text
Feature:     specs/039-uat-feature-resolution (from .specify/feature.json)
             ticks go to its tasks.md; evidence to its uat/<run-stamp>/
Start:       <exact command>
Environment: local build
Scenarios:   UAT1, UAT3
```

## Report Feature row (Step 8)

```text
| **Feature** | specs/039-uat-feature-resolution — resolved from .specify/feature.json |
```
