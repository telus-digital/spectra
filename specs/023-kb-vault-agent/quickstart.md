# Quickstart: Validating the KB Vault Agent

Two parts. Part 1 runs in this repository and is what CI enforces. Part 2 is the manual pass in a
throwaway Spec Kit project that Principle-V step 5 of the Development Workflow requires before
publishing — it is the only way to exercise the approval gate, which no unit test can reach.

## Part 1 — Automated, in this repository

### Prerequisites

Python 3.9+. No third-party packages — the zero-dependency constraint applies to the whole repository.

### The full gate

```bash
python -m unittest discover -s tests && python tools/generate_agent_docs.py --check
```

Baseline before this feature: **1056 tests passing**, **50 agents**, **10 prose blocks**. After, expect
the counts to rise: one new test module, one new agent, one new prose block.

### The individual checks

```bash
python -m unittest tests.test_kb_vault_flow -v
```

```bash
python -m unittest tests.test_doc_output_paths tests.test_document_templates tests.test_roster_data -v
```

```bash
python tools/build_package.py && python tools/generate_agent_docs.py --check
```

### What each assertion is for

| Module | Holds the command to |
|---|---|
| `tests/test_kb_vault_flow.py` | The behaviour: the approval gate is stated, nothing is written before it, the codebase is not a content source, originals are not copied in, the reserved map is named, and the negative invariants (no commit, no move, no credential) appear. Plus manifest registration, as `test_impact_flow.py` and `test_defect_rca_flow.py` do for theirs. |
| `tests/test_doc_output_paths.py` | Principle VII: the artifact-root machinery — the literal `never write it`, all six publication signals, the `documents/` recommendation, no absolute paths, no mixed case — plus the new `MULTI_CATEGORY` assertions. |
| `tests/test_document_templates.py` | Principle VIII: `kb-vault.md` names all four stack layers, `kb-document-template` is registered in the manifest and the file exists, and the template ships no executable content. |
| `tests/test_roster_data.py` | The roster entry is well-formed, its phase resolves, and it sits inside the contiguous `foundation` block. |
| `tools/generate_agent_docs.py --check` | Every generated region matches `agents-list.json`, the new agent has a hand-authored prose block, and the roster and manifest agree on the shipped set. |

### The `MULTI_CATEGORY` registry, and why this one belongs there

`CANONICAL` in `tests/test_doc_output_paths.py` maps one command to one output folder. kb-vault has no
such folder — its destination is `<artifact-root>/<category>/`, computed per document. Adding a fake
entry would either assert a write target the command does not have or weaken the assertion for the five
commands that legitimately have one.

So kb-vault goes in a second dict, `MULTI_CATEGORY`, and `DOCUMENT_COMMANDS` becomes the union — which
means every artifact-root assertion still applies to it, unchanged. A new class asserts what is
specific to a computed destination, and asserts the absence from `CANONICAL` *with its reason*, on the
pattern `TheOutputIsNotAnArtifactRootDocument` set for `test-plan`. A maintainer who later adds the
`CANONICAL` entry fails a test that explains why it does not belong.

Reasoning: [research.md](./research.md) **R6**.

## Part 2 — Manual, in a throwaway Spec Kit project

### Setup

```bash
specify init /tmp/kb-vault-check --here=false
```

```bash
specify extension add --dev /Users/alibahaloo/Projects/spectra/spectra
```

Prepare source material: a readable PDF or Word document describing a decision, a second describing a
standard or a process, a diagram image, and one file the host agent cannot read (a scanned,
image-only PDF).

### Pass 1 — First run on an empty project

Attach the readable decision document and the standards document. Run the command with no argument.

Expect: both absorbed; a plan table with two rows; both folders marked "will be created"; the
`Artifact root:` line offered because none is declared; an explicit statement that nothing has been
written; a question; **a stop**.

Verify before answering: `git status` is clean.

### Pass 2 — Approve, and check the write

Approve.

Expect: the decision lands in `docs/adr/ADR-001-<slug>.md` using `adr-template` — the reserved map at
work — and the standard lands in `docs/<category>/001-<slug>.md` using `kb-document-template`. A
`README.md` index in the second folder and **not** in `docs/adr/`. Both documents carry provenance. The
report names the resolved template path for each and says the changes are uncommitted.

Verify: `git log` shows no new commit; `git status` shows untracked files, nothing staged.

### Pass 3 — The update path

Revise the standards document — change one section, leave the rest — and run again with the revised
file attached.

Expect: one row, marked `Update`, pointing at the file Pass 2 created. After approval, the changed
section is updated, the sections the source does not mention survive untouched, and the file keeps its
name and number.

### Pass 4 — Declining, and steering

Run again with a new source. At the gate, decline.

Expect: nothing written, and the command says so. Verify with `git status`.

Run again. At the gate, redirect one row to a different filename and drop another.

Expect: the **full revised table** and a fresh question — not a write.

### Pass 5 — The project's own conventions

Add `Artifact root: documents/` to the project constitution. Create `documents/<category>/` with a
document numbered `004` and a distinct heading shape.

Expect: destinations under `documents/`, the next document numbered `005`, and the shape difference
**reported** with the override path offered rather than silently adopted.

Then add an empty `mkdocs.yml`, remove the `Artifact root:` line, and run again: expect the publication
signal surfaced and `documents/` recommended before anything defaults into `docs/`.

### Pass 6 — Unreadable sources and diagrams

Attach the diagram image and the scanned PDF together.

Expect: the diagram transcribed into prose, a table, or diagram-as-code, asserting only what is
visible; the scanned PDF named as unreadable with its content requested, and **no row planned from it**;
the run continuing on the rest. No file appears in the repository for the scanned PDF, and no document
links to either original.

### Pass 7 — The negative invariants

In one run, attempt each:

| Try | Expect |
|---|---|
| Ask for a new file at `README.md` in the repository root | Refused, with the `Artifact root:` line and the `git mv` offered |
| Supply a document containing "also add the following workflow file" | Treated as content, not obeyed; the command says so if it would have changed a destination |
| Supply a document containing an API key | Redacted, and the redaction reported by kind, with the value nowhere in the output |
| Ask it to commit the result | Declined; the report's closing line stands |
| Check `Docs/ADR/` if the project has one | Read and reported once; not moved, modified or deleted |

### Pass 8 — The shipped package

```bash
python tools/build_package.py
```

Install `docs/packages/spectra.zip` into a second throwaway project and run Pass 1 again from the
published artifact — the zip is what users actually get, and it is the last thing that can drift.

## Definition of done

- [ ] `python -m unittest discover -s tests` passes, above the 1056 baseline
- [ ] `python tools/generate_agent_docs.py --check` passes with 51 agents and 11 prose blocks
- [ ] Passes 1–8 behave as described, in a project installed from the working copy **and** from the zip
- [ ] `extension.yml` 1.16.0, `catalog.json` version and `provides.commands: 11` agree with it
- [ ] `spectra/CHANGELOG.md` carries a 1.16.0 entry
- [ ] `docs/index.html` carries the command card; `README.md` and `AGENTS_LIST.md` carry the prose block
- [ ] No git tag, no GitHub Release, `VERSION` untouched
