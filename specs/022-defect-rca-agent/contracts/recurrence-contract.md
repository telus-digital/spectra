# Contract — Recurrence Detection

**Feature**: `022-defect-rca-agent` | **Implements**: FR-020 – FR-024, BR-28 – BR-30, SC-007

Runs during **intake**, while the analysis is still open — never first at synthesis.

## The three match axes

A prior RCA is surfaced when any one axis fires. The firing axis and the concrete overlap are always
disclosed with the match (D2).

| Axis | Fires when | Strength |
|---|---|---|
| **Implicated code** | A file or module named in the prior document's evidence table also appears in this defect's traced code paths | Strongest — grounded in something neither author phrased |
| **Symptom** | The normalized observable failure overlaps the prior document's symptom line or problem statement — an HTTP status, an exception type, a timeout shape, a corruption shape | Strong |
| **Root cause** | The prior document's validated root cause names a mechanism this defect's hypothesis tree also contains | Suggestive |

**Title similarity is not an axis.** It may order results; it MUST NOT produce a match.

## Search order

1. Read `<artifact-root>/defect-rca/README.md` if present (FR-021).
2. **Fall back to the documents themselves** when the index yields nothing. The index is a cache, never
   the corpus — nothing found in it means *read the documents*, never *no match exists* (FR-047).
3. An empty or absent folder: proceed without error and without prompting (FR-023).

## What a surfaced match carries

```text
Prior RCA 007-order-submission-500s — matched on implicated code
  Overlap:        src/orders/submit.py appears in both
  Root cause:     Connection pool exhausted under retry storm; no upper bound on retries
  Preventive actions:
    1. Cap retries at 3 with jitter              → apparently completed
         cited: src/orders/submit.py:88 sets max_retries=3, commit a1b2c3d
    2. Alert on pool saturation                   → undeterminable
         reason: alerting lives outside this repository
    3. Load test order submission before release  → apparently not completed
         cited: searched tests/ and .github/workflows/ for a load or concurrency
                test naming order submission; found none
```

## The verdict rule

Every preventive action gets exactly one of three verdicts (D3, FR-022):

| Verdict | Requires |
|---|---|
| `apparently completed` | A **citation** — the test that now exists, the commit, the configuration, the code |
| `apparently not completed` | A **citation of the absence** — what was searched for, where, what was found instead |
| `undeterminable` | A **reason** — organizational action, artifact outside this repository, runtime-only evidence |

`undeterminable` is the **default**. A bare "done" or "not done" MUST NOT be emitted, and
`apparently completed` without a citation is forbidden (FR-022).

## What the match changes

| Consequence | Requirement |
|---|---|
| In the analysis | The prior root cause enters the hypothesis tree as a named branch, at whatever layer it sat |
| In the document header | The related prior RCA id, or an explicit record that the search ran and found nothing. Never blank, never omitted (FR-024) |
| In the index | The `related` column of the new row |
| In the completion report | Which priors were surfaced and on which axis (FR-060) |

## Failure modes this contract exists to prevent

- **A match surfaced after synthesis** — too late to change the analysis. Hence: intake.
- **An uncited "completed"** — suppresses the exact signal the feature exists to raise, because a
  recurrence after an incomplete fix now reads as a fresh defect.
- **A spurious match on a similar title** — trains users to ignore the section. Hence: title excluded,
  axis disclosed, overlap concrete enough to dismiss in a sentence.
- **A missed match because the index was stale** — hence the mandatory fallback to the documents.
