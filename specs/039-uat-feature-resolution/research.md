# Research: UAT finds its feature the way the implement command does

Every decision here starts from what spec 038 settled for `speckit.spectra.test-plan` (shipped in 1.27.0).
Where uat differs, the difference is stated and justified.

## R1 — Share test-plan's resolution text, adapted to uat

**Decision**: Step 1 of `uat.md` reproduces test-plan's Step 1 (`spectra/commands/test-plan.md:83-200`)
clause by clause:

1. **Environment read.** One read of `SPECIFY_INIT_DIR` and `SPECIFY_FEATURE_DIRECTORY`, in the same POSIX
   and PowerShell forms (R2). An empty value counts as unset.
2. **Project root.** If `SPECIFY_INIT_DIR` is non-empty, it must name an existing directory containing
   `.specify/`, or the run stops. Otherwise the root is the nearest directory containing `.specify/`.
3. **Invoking project.** The nearest `.specify/` above the current directory, whatever `SPECIFY_INIT_DIR`
   says. This is used only by the out-of-project stop.
4. **Feature directory.** `SPECIFY_FEATURE_DIRECTORY`, else `feature_directory` in
   `<root>/.specify/feature.json`, else a stop. A relative value resolves against the root.
5. **Feature contents.** The directory must exist and contain `tasks.md`. This replaces test-plan's
   "contains `spec.md`" and keeps uat's existing "no `tasks.md`" stop (FR-011).
6. **Read-only.** Resolution never writes `feature.json` and never creates the directory.

The wording is test-plan's wherever the two commands mean the same thing. Only these differ:
- the command named in the remedy block ("without uat writing anything");
- the core command it mirrors (the implement command, not the planning command);
- the file the directory must contain (`tasks.md`).

**Rationale**:
- Two commands that resolve one feature should say so in one wording, so one reader can check both
  against `get_feature_paths`.
- `/speckit-implement` and `/speckit-tasks` call the same `get_feature_paths` that `/speckit-plan` calls.
  Naming implement keeps the reason local, since uat follows implement.

**Alternatives considered**:
- *Extracting a shared snippet*, included by both commands. Rejected: Spec Kit commands have no include
  mechanism, and Principle II rules out a build step that would add one.
- *Requiring `spec.md` as well as `tasks.md`.* Rejected: uat reads `tasks.md` and `test-plan.md`, not
  `spec.md`. A missing `spec.md` is already reported as an input not read.

## R2 — Where the environment read sits relative to the gates

**Decision**: The read is the first action of the run, before Step 2's reads and well before Step 3's
run confirmation.

The never-table row "Start a build, a server, or any process before the run confirmation" keeps its
wording and gains one sentence. That sentence says the Step 1 read of two environment variables is a read,
not a start: it launches nothing that outlives it, touches no build, and opens no network connection.

A denied or failed read stops the run, with no fallback to `feature.json` alone (FR-007).

The two values are reused for the whole run and never read again (FR-017a).

**Rationale**: Resolution must happen before anything else can be read, because every later input path
hangs off the feature directory. Framing the read inside the row it might seem to break leaves that row's
promise intact. This is the same answer 038 gave to its "runs nothing" row (038's C1).

**Alternatives considered**: putting the read after the run confirmation. Rejected: the confirmation has to
name the feature (FR-016), so the feature has to be known first.

## R3 — Matching an explicit argument

**Decision**: As 038's R3, unchanged:
- Take the argument, after `--env <value>` and `--non-interactive` are removed.
- Resolve it against the project root.
- Normalize it: drop a trailing slash, drop `./` segments, and treat relative and absolute forms as equal.
- It matches when it equals the feature directory or `<feature-dir>/spec.md`.

Any other path, including `<feature-dir>/tasks.md`, is a mismatch. A mismatch stops before Step 2 reads
anything. The stop names the argument, the resolved directory, the source, and the remedy block. When no
feature resolves, the argument is never used in its place (FR-013).

**Rationale**: Accepting `spec.md` keeps every old invocation that named the active feature working, in
both of the forms uat used to accept. Accepting `tasks.md` would be a new form, and nothing asks for one.

**Ordering with `--env`**: options are removed first, exactly as uat does today. An unrecognized option is
still reported and ignored, and it still never becomes part of the path.

## R4 — Recording the source

**Decision**: The resolution is stated in four places, with the same facts each time:

| Where | What it says |
|---|---|
| Announcement, first statement of a resolved run | `Feature: <dir> (from <source>)`, plus the record's value when the variable won and the record disagreed |
| Step 3 run confirmation | The feature directory whose `tasks.md` will be ticked and whose `uat/` folder will receive evidence, next to the command, environment and scenarios |
| Step 8, the report's Feature row | `<dir>` — resolved from `<source>` |
| Step 9, the session report | A **Feature** line, before Totals |

**No template change.** `uat-report-template.md:22` already has a Feature row whose placeholder is the
project-relative path. Step 8 says what fills it: the path followed by "resolved from …".

The inline skeleton's identifying-block comment becomes
`feature (and where it was resolved from) | build under test | environment | date`.

**Rationale**: This is Principle VIII as 038's R5 applied it. The command owns what fills a row, so an
override that keeps a Feature row still gets the source, and the shipped template stays byte-identical.

## R5 — Stops and the remedy block

**Decision**: The same remedy block as test-plan, with the command name changed:

```text
To choose the feature without uat writing anything:
  · for this session — set SPECIFY_FEATURE_DIRECTORY=<feature-dir>
  · for good         — set "feature_directory" in .specify/feature.json to <feature-dir>
To create a new feature, run the specify command.
```

The Step 1 outcome table has these rows:

| Outcome | Stop |
|---|---|
| Environment read denied or failed | stop; the variables could not be checked; no remedy block, since the remedy is to allow the read |
| `SPECIFY_INIT_DIR` invalid | stop with its value and the reason; the remedy is to unset or correct it |
| Neither source set | stop + remedy block |
| `feature.json` unparseable, or no `feature_directory` | stop + remedy block |
| Resolved directory missing | stop + remedy block |
| Resolved directory has no `tasks.md` | stop: nothing to accept until the tasks exist (existing wording) + remedy block |
| Argument does not match | stop + remedy block |
| Resolved | announce, then go on |

Every stop writes nothing and starts nothing. No evidence folder is created and the report is not
written. That second point differs from a declined run confirmation, which still writes the report.

**uat has no degrade list**, unlike test-plan. Nothing is added: every resolution failure is a stop, not a
degrade.

## R6 — The `after_implement` hook prompt

**Decision**: Leave it as it is. `spectra/extension.yml:133-138` reads "Run UAT now? The agent performs the
scenarios it can drive and leaves the rest for a human." It names no path and passes no variable, so it
already works with resolution and needs no change. Test-plan's hook prompt had to change only because it
passed `SPEC_FILE`.

The manifest description (`extension.yml`, uat entry) does change: it drops "The feature path is required
and never inferred", as the front matter does (FR-021).

## R7 — Version, CHANGELOG, and tests

**Version**: MINOR, 1.27.0 → 1.28.0, for the same reason as 038's R7.

**CHANGELOG `[1.28.0]`**:
- A **Changed** item: uat resolves its feature as the implement command does, and an argument only
  confirms.
- It says plainly that **a path naming a feature other than the active one now stops**, and gives the
  remedy, for anyone who scripted the old form.
- A second item names the one environment read and says it happens before the run confirmation and starts
  nothing.
- 1.27.0 said uat was a candidate for this change. 1.28.0 closes that.

**Tests** (`tests/test_uat_flow.py`):
- The module docstring drops "It never infers the feature."
- `TheFeatureIsRequiredAndNeverInferred` becomes `FeatureIsResolvedAsTheImplementCommandDoes`, mirroring
  038's `FeatureIsResolvedAsThePlannerDoes`. It checks:
  - the order of `SPECIFY_INIT_DIR`, the variable and the record;
  - empty counts as unset;
  - read-only;
  - the forbidden sources and no picker;
  - each stop, including no `tasks.md`;
  - the remedy block;
  - the out-of-project stop against the invoking project.
- New classes:
  - `AnArgumentOnlyConfirms`;
  - `TheResolutionIsAnnounced` (announcement, Step 3 confirmation, Step 8 Feature row, Step 9);
  - `TheEnvironmentReadStartsNothing` (the never-table sentence, read before the confirmation, one read
    reused, no re-read of `feature.json`);
  - `NoStaleProse` (no "required" or "never inferred" in the front matter, manifest, `AGENTS_LIST.md`,
    `spectra/README.md` or `docs/index.html`; the no-argument form first).
- `NonInteractiveStartsNothing` keeps "start nothing and attempt nothing", and swaps "A missing feature
  still stops" for "a feature that does not resolve still stops".
- Every other class stays as it is (FR-018).

The old-contract assertions that keep their meaning in the new contract are rewritten, not deleted:
- "read nothing, start nothing, write nothing" now applies to every resolution stop.
- "do not offer a list" stays.
- "outside the project" stays.
