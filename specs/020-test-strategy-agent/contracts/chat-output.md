# Contract — What the User Sees

The session output, in order. The document is the deliverable; this is how the user learns what is in
it and decides what happens next.

## Order is part of the contract

```text
1. Non-interactive announcement          (only when detected — FR-034)
2. Coverage-run confirmation             (only when a coverage run is possible — R2)
3. Root / publication choice             (only when a signal fires and no root is declared — FR-042)
4. The document is written
5. Run report: where, which template, coverage of analysis
6. Summary of recommendations
7. Constitution check result
8. The amendment gate                    (only when not already embedded)
```

**Steps 5 and 6 come before step 8.** FR-028 requires the summary and the location before the user is
asked anything about the constitution. A gate offered before the user knows what they are approving is
not a gate.

## Step 2 — the coverage-run confirmation

One question. It names the exact command it would run, warns that it executes the project's test
suite, and is declinable (R2). Declined, unanswered, or non-interactive: the run continues on
`reported` or `unavailable`, and the document says which.

## Step 5 — the run report

| Line | Source |
|---|---|
| The document path written | FR-028 |
| The resolved template path | FR-041 |
| Coverage of analysis — what was read out of what is present, what could not be seen | FR-013 |
| Reduced search capability, where applicable | FR-013 |
| Mode: greenfield, brownfield, or mixed, with the deciding signals | FR-045 |

## Step 6 — the summary

The recommendations, per lens, short enough to read in the terminal (FR-028). It states the coverage
floor, its baseline, and the baseline's provenance, because those are the numbers a reader will argue
with and they should not have to open the file to find them.

## Step 7 — the constitution check

One of four (R6, FR-029, FR-030):

- **embedded** — quote the governing clause. No gate follows.
- **partial** — quote what exists, name the gap, proceed to the gate.
- **absent** — say so, proceed to the gate.
- **no constitution** — say there is nothing to amend, name `/speckit-constitution`, stop. No gate.

A conflict between an existing principle and a recommendation is surfaced here as a finding, whichever
state applies (FR-033).

## Step 8 — the gate

The amendment text in full, then the three paths (FR-031): approve, modify, discuss. See
[amendment-handoff.md](./amendment-handoff.md).

**Nothing is asked before the document exists.** If the run cannot write the document, it reports the
failure and outputs the strategy in the session instead of proceeding to a gate about a document that
was never written.

## Tone rules

- **Do not dump the analysis.** The session gets the summary; the document gets the detail.
- **State degradations once, plainly**, where they happen — not collected into a postscript.
- **Never claim a run did something it did not.** "Coverage read from `coverage.xml`, dated 2026-01-14"
  and "coverage measured just now" are different sentences and the wrong one is a lie about evidence.
