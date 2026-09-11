# Contract — The RCA Index

**Feature**: `022-defect-rca-agent` | **Artifact**: `<artifact-root>/defect-rca/README.md`
**Implements**: FR-044 – FR-047

## Status: a cache, not the corpus

The index holds no analysis, states no conclusion of its own, and is **rebuilt from the documents
actually present** on every run that writes (FR-046). Deleting it loses nothing. A document added or
removed by hand self-corrects on the next run.

This is what keeps it inside Principle VII's "exactly one artifact type per folder": a directory listing
is not a second artifact type. `speckit.spectra.impact` ships the same thing at
`<artifact-root>/impact-analysis/README.md`.

**The consequence that matters**: a recurrence search finding nothing in the index MUST fall back to
reading the documents (FR-047). The index makes the common case cheap; it never decides that a match
does not exist.

## Shape

```markdown
# Defect root cause analyses

Written by `speckit.spectra.defect-rca`. One row per analysis, rebuilt on each run.
Conclusions are advisory and owned by the named author of each document.

| ID | Symptom | Root cause | Related | Preventive actions |
|---|---|---|---|---|
| [001-order-submission-500s](./001-order-submission-500s.md) | Intermittent HTTP 500s on order submission under load | Connection pool exhausted under retry storm; no upper bound on retries | none | 1 completed, 1 open, 1 undeterminable |
| [002-duplicate-invoice-emails](./002-duplicate-invoice-emails.md) | Customers received the same invoice email twice | Idempotency key derived from a timestamp with second precision | none | 2 open |
| [003-order-submission-timeouts](./003-order-submission-timeouts.md) | Order submission times out at p99 | none validated — evidence ran out at the load balancer | [001](./001-order-submission-500s.md) | 1 open |
```

## Column rules

| Column | Rule |
|---|---|
| `ID` | `NNN-<slug>`, linked to the file |
| `Symptom` | The observed problem, from the document's §1 contrast line or §2 |
| `Root cause` | The validated root cause, or `none validated — <where the evidence ran out>` |
| `Related` | The related prior RCA id, linked, or `none` |
| `Preventive actions` | Rolled up from §6 — counts by verdict, not the action text |

## Invariants

- Rebuilt, never appended to blindly: a run reads the folder, regenerates every row, and writes the
  whole file (FR-046).
- Written together with the document, as the run's final act (FR-043b). An abandoned run leaves the
  index untouched.
- A file in the folder that does not match `NNN-<slug>.md` is reported once and gets no row.
- The index carries no secret, because it carries nothing the documents do not (FR-039e).
- The index is never the sole basis for concluding a defect is new (FR-047).
