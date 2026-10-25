# Research: Test plan finds its feature the way the planner does

## R1 — Following the planner's rule, step by step

**Decision**: Step 1 reproduces `get_feature_paths` (`common.sh:163-215`) and `get_repo_root`
(`common.sh:56-73`) in prose, in their order:

1. **Project root.** If `SPECIFY_INIT_DIR` is non-empty: it must name an existing directory containing
   `.specify/`, or stop. A relative value resolves against the current directory, as `resolve_specify_init_dir`
   does. Otherwise the root is the nearest directory, walking up from the current one, that contains `.specify/`.
2. **Feature directory.** If `SPECIFY_FEATURE_DIRECTORY` is non-empty, use it. Otherwise, if
   `<root>/.specify/feature.json` exists, use its `feature_directory`; unparseable or empty is a stop.
   Otherwise stop. A relative value resolves against the root.
3. **Specification.** `<feature-dir>/spec.md`. A missing directory or file is a stop. The planner would
   `mkdir -p` here, and test-plan does not create anything (FR-004).
4. **Out-of-project stop** and the **usability test** then run unchanged, on that file.

**Rationale**: Prose that follows the script's order clause by clause is checkable against it. Writing the
rule as "do what the planner does" without the steps would leave each agent to guess.

**Alternatives considered**:
- *Calling `check-prerequisites.sh --json --paths-only`* (the planner's own read-only resolution). This is exact
  by construction, but it runs a script outside the extension, depends on its output format and on a
  bash/PowerShell choice, and was not the option the user chose (Q1).
- *Reading only `feature.json`* was rejected in Q1: it misses the variable.

## R2 — How the one environment read is done

**Decision**: The command describes the read by what it returns, "the values of `SPECIFY_INIT_DIR` and
`SPECIFY_FEATURE_DIRECTORY`, empty where unset", and gives two forms:

```text
POSIX:      printf 'SPECIFY_INIT_DIR=%s\nSPECIFY_FEATURE_DIRECTORY=%s\n' "${SPECIFY_INIT_DIR-}" "${SPECIFY_FEATURE_DIRECTORY-}"
PowerShell: "SPECIFY_INIT_DIR=$env:SPECIFY_INIT_DIR"; "SPECIFY_FEATURE_DIRECTORY=$env:SPECIFY_FEATURE_DIRECTORY"
```

It runs once, before anything else is read. A denied or failed read is a stop (Q2). The values are not
echoed into the document. They are paths, not secrets, but only the resolved directory and its source are
recorded.

**Rationale**: Principle III bars an agent's syntax, not a shell's; Spec Kit itself ships both a bash and a
PowerShell script set. Labelled lines make "empty" unambiguous, and an empty value is treated as unset
(FR-001).

**Alternatives considered**: `env | grep SPECIFY_`. Rejected because it can't distinguish "unset" from
"absent from output", and it prints every `SPECIFY_*` variable, not just the two.

## R3 — Matching an explicit argument

**Decision**: After resolution, an argument (with the flag removed) is resolved against the project root and
normalized: trailing slash dropped, `./` segments removed. It **matches** when it equals the feature
directory or `<feature-dir>/spec.md`. Any other path, including another file inside the feature directory,
is a **mismatch**, because the planner reads `spec.md` and nothing else. On a mismatch the run stops with
the argument's path, the resolved directory, the source, and the two remedies (R6). With no feature
resolved, an argument does not help: the run stops at resolution (FR-009).

**Rationale**: A confirmation that accepts some other file would bring back a split: a test plan built from a
document the planner never reads.

**Alternatives considered**: resolving symlinks or comparing inode identity. Rejected because it needs a
command, and a project-relative textual match covers every realistic spelling.

## R4 — The end-of-run agreement check

**Decision**: Just before Step 17 prints, the run re-establishes the planner's answer from the values it read
in R2, without reading them again (FR-005). If `SPECIFY_FEATURE_DIRECTORY` was non-empty, that answer cannot
have changed, so the check passes trivially. Otherwise the run re-reads `<root>/.specify/feature.json`. If it
now names a different directory, or is gone, no handoff is printed, and the report says what it now names.
The written `test-plan.md` stays, since it is correct for its own feature.

**Rationale**: `feature.json` is the only source that can change during a run (a parallel `specify`). The
check is a file read, not a command, so it doesn't exceed the one-command budget.

## R5 — Where the resolution source is recorded

**Decision**: Step 13's **Spec** fact becomes: the project-relative spec path, followed by "resolved from
`SPECIFY_FEATURE_DIRECTORY`" or "resolved from `.specify/feature.json`". When both were set and disagreed, a
second clause names what the feature record held. The announcement (first statement of the run) and the
report (Step 16, next to the written path) carry the same facts. No template changes: the template's
identifying block is a comment ("spec path | build under test | author / date"), and Step 13 already owns
what fills it.

**Rationale**: Principle VIII keeps the rule in the command. An override that reshapes the block still gets
the source, because Step 13 writes it.

## R6 — What the remedies say

**Decision**: One remedy block, used by every resolution stop (FR-023):

```text
To choose the feature without test-plan writing anything:
  · for this session — set SPECIFY_FEATURE_DIRECTORY=<feature-dir>
  · for good         — set "feature_directory" in .specify/feature.json to <feature-dir>
To create a new feature, run the specify command.
```

A `SPECIFY_INIT_DIR` stop instead says the variable's value and why it was rejected (missing directory, or no
`.specify/`), and names unsetting it as the remedy.

**Rationale**: One wording, so the tests pin one string and the user sees the same advice at every stop.

## R7 — Version and CHANGELOG

**Decision**: MINOR, 1.26.0 → 1.27.0. The constitution makes only a command rename or removal MAJOR
(`constitution.md:393-396`), and this change makes an argument optional. The `[1.27.0]` entry has a
**Changed** item that says plainly: **a path naming a feature other than the active one now stops**, with the
remedy. That's for anyone who scripted the old form. A second item notes the one environment read.

## R8 — Tests, and the UAT candidate

**Decision**: In `tests/test_test_plan_flow.py`:
- `TheSpecificationArgumentIsRequired` becomes `FeatureIsResolvedAsThePlannerDoes`. It asserts the order (init
  dir, variable, record), empty-as-unset, read-only (never writes the record, never creates the directory),
  the forbidden sources (branch, modification time, `specs/` listing, history), no picker, the stops, and
  the remedy block.
- `test_step_one_counts_its_own_outcomes` keeps its guard against the table and the prose disagreeing, and
  points at the new Step 1 heading and table.
- `test_the_hook_does_not_relax_the_never_infer_rule` asserts that resolution is identical whether or not
  the hook was used.
- `test_the_manifest_offers_it_after_specify_optionally` asserts the prompt no longer passes `SPEC_FILE`.
- New assertions: argument match and mismatch, the announcement, Step 13's source clause, the agreement check
  before Step 17, the environment read named in the never-table, and the non-interactive bullet (C2).
- `ItRunsNothing` keeps its phrases.

`speckit.spectra.uat` keeps its required path (FR-022). The CHANGELOG entry records it as a candidate for
the same change. `uat.md` is not touched.
