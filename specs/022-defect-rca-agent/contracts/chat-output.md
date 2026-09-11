# Contract — Session Output

**Feature**: `022-defect-rca-agent` | **Implements**: FR-008, FR-025 – FR-037, FR-060

Most of what a user sees from this command is never written to a file. The hypothesis tree, the
statuses, the questions and the issue trees are **rendered in the session and never persisted**
(FR-036) — so this contract is as load-bearing as the document contract.

## Intake output

Emitted after evidence gathering, before any question is asked:

1. **Resolved channel**, stated (FR-008) — and the retrieval outcome where one was attempted.
2. **Constitution principles that bear on this analysis**, by heading (FR-015). Or: no constitution
   found, proceeding on methodology.
3. **Prior RCAs surfaced**, per `recurrence-contract.md`. Or: corpus searched, nothing matched.
4. **What was examined** — the code paths, the recent commits, the configuration, the tests (FR-016) —
   **and what was not** (FR-017). The second half is not optional; it is what makes the first half
   honest on a large repository.
5. **Repository and commit analyzed**, with the request to confirm the deployed version before
   hypotheses are built on this code (FR-018).
6. **The hypothesis tree** — at least five major branches with sub-nodes (FR-025).
7. **At most five questions**, ordered by what would most change the analysis, each stating *why it
   matters* (FR-029, D8).

## The hypothesis tree, rendered

```text
Hypothesis tree — 6 branches, 11 hypotheses

Code / Logic                                            [narrowing]
  H1  Retry loop has no upper bound          layer 2    supported
        code  src/orders/submit.py:88 — while not ok: retry()
  H2  Idempotency key collides under load    layer 2    invalidated
        code  src/orders/key.py:22 — key includes a UUID4, collision implausible

Design / Architecture                                   [open]
  H3  Connection pool sized for sequential traffic  layer 3  open
        test:  read config/db.yaml and compare to observed concurrency

Process / Practice                                      [open]
  H4  No load test covers concurrent submission  layer 4  open
  ...
```

Every hypothesis carries its **layer** (FR-026) and its **status** (FR-027). Every finding carries its
**source and locator** (FR-019). Nothing is asserted without one.

## Loop output, per round

- Which hypotheses moved, and on what evidence.
- The running view: validated / supported / weakened / invalidated / open, plus open data gaps
  (FR-027).
- The current ladder layer, and — where the deepest finding is still layer 2 — what would be needed to
  go deeper (D4).
- The next questions, capped at five, stakes stated.

## Question format

```text
Q1  What was the p99 latency on the order service between 14:00 and 14:30 UTC?
    Why it matters: separates H1 (retry storm) from H3 (pool sizing) — these predict
    opposite latency shapes, so one answer retires a branch.

Q2  Was the 14:07 config change deployed before or after the first failure?
    Why it matters: if after, H5 is retired outright.
```

Never asked: anything the repository answers (FR-028). Never answered by the command itself (FR-032).

## Issue-tree exploration output

At least four major branches with sub-nodes and per-node discovery questions (FR-035), branch
likelihood and impact discussed on request, confirmed / refuted / open recorded per node — and
**nothing written anywhere** (FR-035). Where the exploration turns into a real defect, the confirmed and
refuted nodes carry into intake rather than restarting.

## Synthesis output

Before the write: the document rendered for review. After the write: the completion report of
`command-interface.md` — path, template layer and path, artifact root and how it was determined, commit
analyzed, priors surfaced and their axes, what could not be examined (FR-060).

## Reflection output

Four dimensions — analysis depth, hypothesis discipline, data-gap closure, answer-first structure — with
at least one concrete improvement (FR-037). Requested with no analysis behind it: say so, do not assess.

## Refusals, and how they read

| Situation | Response |
|---|---|
| Empty `$ARGUMENTS` | Ask what defect to analyze. Stop. No inference, no reading, no writing (FR-009) |
| Retrieval failed | Name the failure and its specific remedy, ask for a paste, continue as `plain` (FR-013) |
| A credential is offered or would be needed | Decline, explain, continue without it (FR-013) |
| Deepest finding is layer 2 at synthesis | Say so, name what would go deeper, do not promote it to root cause (D4) |
| Nothing validated | Write the document recording that, what was ruled out, what would settle it (FR-039f) |
| Root cause is outside this repository | Name it as out of reach, report what was established locally |
| Secret found in user material | Describe by kind and location, state the substitution, never quote it (FR-039e) |
| Reflection with no analysis | Say there is nothing to reflect on (FR-037) |

## Non-interactive sessions

Proceed on repository evidence alone; write the document; record every unanswered question as an open
data gap with its confidence cost stated (FR-031). Do not answer own questions (FR-032), do not infer
unobserved runtime facts (FR-033). Where a root would have been chosen after a publication signal, take
the non-publishing option and say so (FR-041).
