# Phase 1 — Quickstart: Proving the Test Strategy Agent Works

How to validate the command before publishing. Repository checks run here; behaviour checks run in a
throwaway Spec Kit project with the working copy installed.

## Prerequisites

```bash
python3 -m unittest discover -s tests
```

```bash
python3 tools/generate_agent_docs.py --check
```

Baseline before this feature: **828 tests passing**, generator reporting 47 agents and 7 prose blocks.
After: 48 agents, 17 available, 8 prose blocks, and the new flow module.

Install the working copy into a scratch project to exercise the command:

```bash
specify extension add --dev /Users/alibahaloo/Projects/spectra/spectra
```

---

## A. Repository checks — run in this repo

### A1. The publishing surface agrees with itself

```bash
python3 tools/generate_agent_docs.py --check && python3 -m unittest discover -s tests
```

**Expect**: generator reports 48 agents, 8 prose blocks, roster and manifest agreeing; suite green.
`--check` fails loudly if the roster ships an agent with no prose block, which is the step easiest to
forget.

### A2. The catalog and the manifest agree

```bash
grep -n 'version:' spectra/extension.yml | head -1 && grep -n '"version"\|"commands"' catalog.json
```

**Expect**: `1.13.0` in both, `"commands": 8`. CI fails the merge on a mismatch, so catch it here.

### A3. The zip is the committed one

```bash
python3 tools/build_package.py && git diff --stat docs/packages/spectra.zip
```

**Expect**: no diff. A dirty zip after a rebuild means the committed package drifted from `spectra/`.

### A4. The constitutional enforcement modules picked the command up

```bash
python3 -m unittest tests.test_doc_output_paths tests.test_document_templates -v 2>&1 | grep -i "test.strategy\|OK\|FAILED"
```

**Expect**: the new command appears in the parameterised subtests and passes. This is what proves the
declared-root, publication-check, `never write it`, and four-layer-resolution obligations are enforced
rather than merely written.

---

## B. Behaviour checks — run in a scratch project

### B1. Greenfield — a strategy with no code to read (User Story 1)

Scratch project: a `README.md`, one dependency manifest, a constitution. No source, no tests.

Run the command with no arguments.

**Expect**:
- mode reported as `greenfield`, with the deciding signals;
- all four lenses present, each `applicable` with an approach or `not-applicable` with a reason;
- a coverage floor framed as hold-from-the-first-commit, marked `convention`;
- every recommendation carrying a citation **or** the convention marker — count them, expect zero
  bare ones;
- the summary printed **before** any question about the constitution;
- exactly one new file in the working tree.

### B2. Brownfield — the floor never exceeds the baseline (User Story 2)

Scratch project: real source, a configured test framework, a committed coverage report showing a low
figure — 31% is a good choice because it is well under any conventional target.

**Expect**:
- mode `brownfield`;
- each lens reporting `current` **before** `approach`, with citations;
- baseline `31%`, provenance `reported`, with the report's date;
- **floor ≤ 31%** — this is the single most important assertion in the whole pass. A floor of 80%
  here is the failure the design exists to prevent;
- a ratchet with triggers, no dates;
- the exact enforcement configuration stated and **not applied** — diff the coverage config and the
  CI workflow and expect no change.

### B3. No coverage tooling at all

Same, with the coverage report and coverage config removed.

**Expect**: provenance `unavailable`, floor `conditional`, tooling recommended as step one, and **no
number asserted**.

### B4. No browser, no browser driver (FR-017)

Scratch project: a Python CLI, or a published library. Nothing browser-related in any manifest.

**Expect**: the end-to-end lens resolves to `cli`, `http`, or `none` — and the word Playwright does not
appear. This is the generic-template-fill-in failure, and it is the one a reader spots instantly.

### B5. The constitution is never written (User Story 3)

Scratch project with a constitution that has no testing principle.

```bash
shasum .specify/memory/constitution.md
```

Run the command. Decline the amendment. Re-hash.

**Expect**: identical hash.

Run again and **approve**. Re-hash.

**Expect**: **still identical**. The amendment text is in the strategy document's proposed-amendment
section, and the session names the `/speckit-constitution` invocation. This is the invariant the whole
Q2 decision rests on — approval changes the document, never the constitution.

### B6. Already embedded, and partially embedded

Add a constitution principle mandating testing with a coverage floor. Run.

**Expect**: state `embedded`, the clause quoted, **no gate offered**.

Now weaken the principle so it mandates testing but says nothing about a floor. Run.

**Expect**: state `partial`, the existing clause quoted, and a draft scoped to the gap rather than a
wholesale replacement.

Now set the principle to 90% in a repository measuring 31%. Run.

**Expect**: the contradiction surfaced as a finding, and **no** amendment that silently overrides it
(FR-033).

### B7. Re-run rewrites in place (User Story 4)

Run twice, changing something between runs.

**Expect**: one file, same path, no `NNN`, no second document, no index. The prior strategy is named as
an input, an implemented recommendation is marked adopted rather than re-proposed, and the run states
what changed.

### B8. The declared root and the publication check

Add `Artifact root: documents/` to the constitution. Run.

**Expect**: `documents/test-strategy/TEST_STRATEGY.md`.

Remove the declaration and add `docs/index.html`. Run.

**Expect**: the publication signal surfaced, `documents/` recommended, the choice offered — and the
non-publishing option taken if no answer is given.

**Then run it in this repository**, which has `docs/index.html` and Pages on `main` `/docs`. The check
must fire here too; a run that silently writes `docs/test-strategy/` is a bug.

### B9. The template override wins, and an omission is honoured

```bash
mkdir -p .specify/templates/overrides
```

Copy the shipped template there, delete the "Coverage floor" section, run.

**Expect**: the override's path reported in the session; no coverage-floor section in the document;
the omission noted; the floor still stated **in the session**.

Now delete the "Proposed constitution amendment" section instead.

**Expect**: the amendment text in the session and the handoff still offered (FR-036).

### B10. Non-interactive

Run with no terminal able to answer.

**Expect**: the condition announced once; the document written; no coverage run attempted; the
amendment drafted and recorded as `not-asked`; no approval inferred.

### B11. The empty repository

Run in a directory with essentially nothing in it.

**Expect**: **no strategy document**. A statement of what was looked for, what was not found, and what
would make a run useful. A generic strategy here is the failure.

---

## C. The manual publish pass

Follow `test/README.md` to install the built zip into a clean Spec Kit project and confirm the command
is registered, invocable, and shows the new entry on the landing page. Principle V is only satisfied
when the zip, the catalog, and the page all agree with `spectra/`.
