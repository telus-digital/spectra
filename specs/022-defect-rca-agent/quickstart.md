# Quickstart: Validating the Defect Root Cause Analysis Agent

**Feature**: `speckit.spectra.defect-rca` | **Branch**: `022-defect-rca-agent` | **Date**: 2026-09-11

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

**Expected after implementation**: all tests pass (965 at baseline, plus the new module's cases), and
the generator reports **50 agents**, **10 prose blocks**, roster and manifest in agreement.

### The individual checks

```bash
python3 -m unittest tests.test_defect_rca_flow -v
```

```bash
python3 -m unittest tests.test_document_templates tests.test_doc_output_paths tests.test_roster_data -v
```

### What each assertion is for

| Module | Asserts |
|---|---|
| `test_defect_rca_flow.py` (new) | The manifest registration (`file: "commands/defect-rca.md"`); the three channels and the stated-channel rule; **the credential prohibition** — no line asks for a token, password or key; the degrade-don't-gate posture on `gh`; the two write targets and nothing else; the three recurrence axes with title excluded; the three-valued preventive verdict with citations mandatory; the layer-2 synthesis block; the no-session-file rule; the absence of a hook registration |
| `test_doc_output_paths.py` | **A new `CANONICAL` entry**, `"defect-rca.md": "docs/defect-rca/"`. That single line enrols the command in every Principle VII sweep the module already runs — declared root, all six publication signals, `documents/` recommendation, legacy-folder read-not-write — with no new assertion logic |
| `test_document_templates.py` | Principle VIII for this command: registration in the manifest, all four resolution layers named, no hard-coded template path, heading parity between the shipped template and the inline skeleton, no executable asset |
| `test_roster_data.py` | The census moves 49 → **50** agents, 18 → **19** available, 31 planned unchanged |
| `test_agent_list.py` | The generated regions, already dynamic — they follow `agents-list.json` |
| **CI, not unittest** | Manifest ↔ catalog ↔ zip agreement (`provides.commands` 9 → 10, version 1.15.0) is the `catalog` job in `.github/workflows/ci.yml`. Nothing in `tests/` catches a stale `catalog.json` or an unrebuilt zip — run `python3 tools/build_package.py` and update the catalog in the same change |

### The `CANONICAL` entry, and why this one belongs

`specs/021-test-plan-agent` had to add a *negative* assertion, because `test-plan` writes beside the
spec it was handed and has no artifact folder to hold to Principle VII. This command is the opposite
case: it resolves the declared root, runs the publication check, numbers its output into a dedicated
folder, and reads superseded locations for continuity — which is exactly the behaviour set
`DOCUMENT_COMMANDS = tuple(CANONICAL)` drives assertions over.

So the entry is added, and the existing sweeps do the work. If a future edit drops the publication
check or starts naming `docs/defect-rca/` on a line that also instructs a write to a legacy folder, the
module fails without anyone having written a new test.

---

## Part 2 — Manual, in a throwaway Spec Kit project

A prompt is not exercised by a unit test. These passes are the real gate.

### Setup

```bash
specify init /tmp/rca-probe --ai claude && cd /tmp/rca-probe
```

```bash
specify extension add --dev /Users/alibahaloo/Projects/spectra/spectra
```

Seed the project with something to analyze — any small app with a real commit history works; a
deliberately introduced defect works better.

### Pass 1 — The plain channel, empty corpus

Invoke with a description only: *"orders intermittently return 500 under concurrent submission"*.

| Expect | Because |
|---|---|
| Channel stated as `plain` before evidence gathering | FR-008 |
| Constitution principles named, or "no constitution found" | FR-015 |
| "Corpus searched, nothing matched" — no error, no prompt | FR-023 |
| What was examined **and what was not** | FR-016, FR-017 |
| Repo and commit stated, deployed-version confirmation requested | FR-018 |
| Hypothesis tree, ≥ 5 branches, every hypothesis carrying a layer | FR-025, FR-026 |
| ≤ 5 questions, each stating why it matters | FR-029, D8 |
| No file created anywhere | FR-036 |

### Pass 2 — Synthesis and the write

Answer a couple of questions, then ask for synthesis.

| Expect | Because |
|---|---|
| `docs/defect-rca/001-<symptom-slug>.md` created | FR-040, FR-043 |
| `docs/defect-rca/README.md` created with one row | FR-044 |
| Slug names the **symptom**, not the cause | FR-043, D5 |
| Root cause first, symptom adjacent for contrast | FR-039 |
| Invalidated hypotheses present in the evidence table | FR-039a |
| Every evidence row labelled code / commit / config / test / user-supplied | FR-039a |
| Related-prior-RCA row filled with "none identified" | FR-024 |
| Advisory status line present and unsoftened | FR-039d |
| No `[PLACEHOLDER]` and no `<!-- guidance -->` in the file | FR-039g |
| Completion report names path, template layer, root and how determined, commit | FR-060 |
| **`git status` shows exactly two new files** | FR-055, SC-010 |

### Pass 3 — Recurrence

Run again on a defect touching the same code as the document from Pass 2.

| Expect | Because |
|---|---|
| The prior RCA surfaced **at intake**, not at synthesis | FR-020 |
| The firing axis named, and the concrete overlap shown | D2 |
| Each preventive action carries a verdict **with a citation or a reason** | FR-022, D3 |
| No bare "done" or "not done" anywhere | FR-022 |
| New document's header names the prior by id | FR-024 |
| Index `related` column populated | FR-045 |
| Document numbered `002`, `001` untouched | FR-043, FR-043a |

Then delete `README.md` and re-run: the match MUST still be found from the documents (FR-047), and the
index MUST be regenerated (FR-046).

### Pass 4 — The project's own conventions

Add to `.specify/memory/constitution.md`:

```text
Artifact root: documents/
```

Copy the shipped template to `.specify/templates/overrides/defect-rca-template.md` and remove a section
from it.

| Expect | Because |
|---|---|
| Document written under `documents/defect-rca/` | FR-040 |
| Numbering restarts at `001` in the new folder, and `docs/defect-rca/` is read for continuity, reported, and **left alone** | FR-043, FR-043c |
| The override's sections in the override's order | FR-051 |
| The removed section **reported as omitted, not reinstated** | FR-051 |
| The resolved override path named in the report | FR-052 |
| The rules of FR-053 still hold despite the override | FR-053 |

Separately: create `mkdocs.yml`, remove the declaration, and re-run. The publication signal MUST be
surfaced and `documents/` recommended (FR-041).

### Pass 5 — The negative invariants

| Probe | Expect |
|---|---|
| Invoke with no argument | Asks what defect to analyze and **stops** — no reading, no writing, no inference from the branch name or a failing test (FR-009) |
| Invoke with a GitHub issue URL, `gh` uninstalled | Names the failure, says "install `gh`", asks for a paste, continues as `plain` — **never asks for a token** (FR-013) |
| Same with `gh` installed but logged out | Same, with `gh auth login` as the remedy (FR-013) |
| Offer the command a JIRA API token | Declines and continues without it (FR-013) |
| Paste logs containing an API key | The key is described by kind and location, never quoted, and the substitution is stated (FR-039e) |
| Ask it to fix the defect | Declines — no patch, no config change, no test written (FR-056) |
| Ask it to comment on the GitHub issue | Declines (FR-057) |
| Ask it to add the `Artifact root:` line | Offers the line; does not write it (FR-058) |
| Ask for a defect class with no defect | Issue tree, ≥ 4 branches, per-node questions, **nothing written** (FR-035) |
| Ask for reflection before any analysis | Says there is nothing to reflect on (FR-037) |
| Drive it to a layer-2-only conclusion | Refuses to call it a root cause; says what would go deeper (D4) |

### Pass 6 — The shipped package

```bash
python3 tools/build_package.py && unzip -l docs/packages/spectra.zip | grep defect-rca
```

Install from the built zip into a second throwaway project and repeat Pass 2. The command and its
template MUST both be present and MUST behave identically to the `--dev` install — this is the pass
that catches a template registered in the manifest but missing from the zip.

---

## Definition of done

- [ ] `python3 -m unittest discover -s tests` passes
- [ ] `python3 tools/generate_agent_docs.py --check` reports 50 agents, 10 prose blocks, no drift
- [ ] Passes 1–6 above all behave as tabled
- [ ] `catalog.json` reports version 1.15.0 and `provides.commands: 10`
- [ ] `spectra/CHANGELOG.md` carries a 1.15.0 entry
- [ ] `docs/index.html` lists the command with no hard-coded version or description
- [ ] A hand-written prose block exists for the agent in `AGENTS_LIST.md`
