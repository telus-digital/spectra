# Quickstart: Validating the Test Plan Agent

**Feature**: `speckit.spectra.test-plan` | **Branch**: `021-test-plan-agent` | **Date**: 2026-09-11

How to prove this works. Two halves: the automated checks that run in this repository, and the manual
passes that exercise the command inside a real Spec Kit project — because a prompt file's behaviour is
only observable when an agent runs it.

---

## Part 1 — Automated, in this repository

### Prerequisites

Python 3.9+. No dependencies — standard library only, by constitution.

### The full gate

```bash
python3 -m unittest discover -s tests && python3 tools/generate_agent_docs.py --check
```

**Expected after implementation**: all tests pass (884 at baseline, plus the new module's cases), and the
generator reports **49 agents**, **9 prose blocks**, roster and manifest in agreement.

### The individual checks

```bash
python3 -m unittest tests.test_test_plan_flow -v
```

```bash
python3 -m unittest tests.test_document_templates tests.test_doc_output_paths tests.test_roster_data -v
```

### What each assertion is for

| Module | Asserts |
|---|---|
| `test_test_plan_flow.py` (new) | The argument gate and the inference prohibition; the single write target; the no-checkbox rule over the template and the inline skeleton; the traceability language; the never-runs-anything posture; the printed-not-invoked handoff; the absence of a hook registration |
| `test_document_templates.py` | Principle VIII for this command: registration in the manifest, all four resolution layers named, no hard-coded template path, heading parity between the shipped template and the inline skeleton, no executable asset |
| `test_doc_output_paths.py` | The five sweeps that apply to every command file; **plus a new negative assertion** that `test-plan.md` is deliberately absent from `CANONICAL`, with the reason |
| `test_roster_data.py` | The census: 49 agents, 18 available, 31 planned |
| `test_extension.py`, `test_agent_list.py` | Manifest ↔ catalog agreement and the generated regions, both already dynamic |

### The negative assertion, and why it exists

`CANONICAL` in `test_doc_output_paths.py` maps each artifact-root document command to its folder, and
`DOCUMENT_COMMANDS = tuple(CANONICAL)` drives assertions that the command says `never write it`, names all
six publication signals, and recommends `documents/`. Every one of those describes a command that
*writes* into the artifact root. This command does not — it writes beside the spec it was handed, and
reads the declared root only to find the strategy document.

So the entry is not added. Since "deliberately absent" and "someone forgot" look identical in a dict, the
new assertion pins the omission and carries the reason in its failure message. A future maintainer adding
this command to `CANONICAL` fails a test that explains why the entry does not belong.

---

## Part 2 — Manual, in a throwaway Spec Kit project

### Setup

```bash
specify init tp-check --ai claude && cd tp-check
```

Set `SPECTRA_REPO` to your checkout of this repository before running these.

```bash
specify extension add --dev "$SPECTRA_REPO/spectra"
```

Then create a feature to plan against:

```bash
mkdir -p specs/001-signed-webhooks
```

Write a `spec.md` in it with numbered requirements, three prioritized user stories with acceptance
scenarios, and — deliberately — one `[NEEDS CLARIFICATION]` marker and one requirement phrased too vaguely
to test.

### Pass 1 — The argument gate (the most important one)

Run the command with **no argument**.

| Check | Expected |
|---|---|
| Does it ask for a path? | Yes, naming what to supply |
| Does it list `specs/`? | **No** — offering a picker is the same failure with extra steps |
| Does it mention the branch, `.specify/feature.json`, or a most-recent file? | **No** |
| Did it read any source code? | **No** |
| Was anything written? | **No** |

Then repeat with: a path that does not exist; a path to `README.md`; a path to the feature *directory*;
and a path to a directory with no `spec.md`. Each should stop with the reason, except the directory
containing `spec.md`, which should resolve and say so.

### Pass 2 — Traceability in both directions

Run against the spec. Then check by hand:

```bash
grep -oE '\*\*(FR|SC)-[0-9]+\*\*' specs/001-signed-webhooks/spec.md | sort -u
```

| Check | Expected |
|---|---|
| Every acceptance criterion reachable from a condition or from *Explicitly not covered* | Yes — no criterion absent from both |
| Every condition's `Verifies` resolves to a real spec item | Yes |
| Any identifier the command invented | **None** — `USn-ACn` composition and verbatim quotations only |
| The `[NEEDS CLARIFICATION]` requirement | Listed uncovered, `/speckit-clarify` named as the remedy |
| The vague requirement | Listed uncovered as untestable, with the missing decision named — **not** given a fabricated condition |
| The report's count | States covered-out-of-found |

### Pass 3 — No checkboxes anywhere

```bash
grep -nE '^\s*[-*] \[[ xX]\]' specs/001-signed-webhooks/test-plan.md
```

**Expected: no output.** Then the harder case — copy the shipped template to
`.specify/templates/overrides/test-plan-template.md`, reintroduce a checklist in the exit criteria, and
re-run.

| Check | Expected |
|---|---|
| Checkboxes in the output | **None** — rendered as plain statements |
| The exit criteria section | Still present; not dropped over the override |
| The run report | States how many constructs were converted, and that the override layer was used |

### Pass 4 — Inheriting the project's lens vocabulary

Run `speckit.spectra.test-strategy` in the same project so `docs/test-strategy/TEST_STRATEGY.md` exists,
then re-run the test plan.

| Check | Expected |
|---|---|
| The `Level` column | Uses the strategy's lens names, verbatim — not normalized or title-cased |
| The report | Names the strategy by path as the vocabulary's source |
| A conflicting constitutional obligation | Constitution wins; the divergence is reported |
| With the strategy deleted | Default set used, absence stated, run still succeeds |

### Pass 5 — No unrunnable level (the plausibility failure)

Do this in a project with **no browser anywhere** in its manifests — a Python CLI is ideal.

| Check | Expected |
|---|---|
| Any condition at a browser-driven level | **None** |
| Any browser tool named | **None** |
| The end-to-end lens | Resolved to the project's real surface, or stated as having none |

This is the failure `test-strategy` exists to avoid, reappearing one phase later. A test plan that assigns
a CLI tool's conditions to a browser driver is the same defect with a different filename.

### Pass 6 — Risks are a decision, not an inventory

| Check | Expected |
|---|---|
| Row count | Between 2 and 5 |
| Every row rated H/H | **No** — or an explicit statement of why the derivation produced that |
| At least one `accept` where the rating does not justify effort | Present |
| Each rating | Traceable to a stated trigger |

### Pass 7 — Existing coverage, read not run

Add a real test for one of the spec's behaviours, then re-run.

| Check | Expected |
|---|---|
| That condition | Marked already covered, citing the test file |
| An uncovered behaviour | States what was searched for and where — never bare "not covered" |
| Was the suite executed? | **No.** No test output, no coverage run, no install |

### Pass 8 — Re-run, and the preservation rule

Edit the spec (resolve the clarification, add a requirement), then re-run.

| Check | Expected |
|---|---|
| Was the existing plan read? | Yes |
| Was confirmation asked before rewriting? | Yes — and the request states what would change |
| Declining | Leaves the file byte-identical; nothing else written |
| Accepting | Carries forward the prior *explicitly not covered* decisions, or states their removal |
| With `--non-interactive` and a plan present | Reports what exists and what would change; **writes nothing** |
| With `--non-interactive` and no plan | Creates it |

### Pass 9 — The handoff

| Check | Expected |
|---|---|
| A copyable `/speckit-plan` invocation naming the written path | Present |
| Did the command invoke it? | **No** |
| `.specify/extensions.yml` | No `before_plan` entry added |
| Core command files | Unmodified |

### Pass 10 — Write scope

```bash
git status --porcelain
```

**Expected: exactly one changed path** — `specs/001-signed-webhooks/test-plan.md`. Not the spec, not the
constitution, not a test file, not CI, not `.specify/`.

Then the out-of-project case: point the command at a spec in a sibling repository.

| Check | Expected |
|---|---|
| Was anything written? | **No** — the conflict is reported and the run stops |
| Did it relocate the output into this project instead? | **No** |

### Pass 11 — The published package

```bash
cd $(mktemp -d) && specify init zip-check --ai claude && cd zip-check
```

```bash
specify extension add --catalog https://raw.githubusercontent.com/telus-digital/spectra/main/catalog.json spectra
```

| Check | Expected |
|---|---|
| The command is installed and invocable | Yes |
| `.specify/extensions/spectra/templates/test-plan-template.md` | Present |
| Catalog version | 1.14.0, `provides.commands: 9` |
| The landing page lists the command | Yes, reading version and roster from the artifacts that define them |

---

## The four failures most worth hunting

Ranked by how plausible the broken output looks.

1. **An empty invocation that analyzes the project anyway.** The command reads the repository, then asks
   for the spec. Harmless-looking, and it means the inference prohibition is a suggestion rather than a
   gate — the next edit makes it pick a spec.
2. **An acceptance criterion that reaches no condition and no uncovered list.** The document reads as
   complete. This is the defect the whole feature exists to prevent, and it is invisible without the
   count in the report.
3. **A fabricated condition for the vague requirement.** Strictly worse than a gap, because it looks like
   coverage and a stakeholder signs it. Pass 2 is the only thing that catches it.
4. **A checkbox surviving an override.** Turns an approval document into a competing tracker that will
   disagree with `tasks.md`, and it only appears on projects that customize — the ones least likely to
   report it.
