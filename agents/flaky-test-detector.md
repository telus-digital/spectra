---
id: flaky-test-detector
title: Flaky Test Detector
command: speckit.spectra.flaky-test-detector
provider: spectra
type: add-on
phase: testing-quality
order: 60
status: available
summary: Find the tests that pass and fail on the same code, then fix the ones you approve, one at a time.
manifest: Find the tests that pass and fail on the same code by reading the test source alone — no test run, no CI history — report each with a confidence rating and a concrete fix, then, behind two explicit gates, write a resumable task list to .specify/memory/flaky-test-analysis.md and apply the fixes the developer approves.
---

Find the tests that pass and fail on the same code, then fix
the ones you approve. The usual way to catch a flaky test is to instrument CI, collect hundreds of runs,
and compute a score — pipeline work, a results store, and weeks of waiting before the first answer. This
agent needs none of that, because the causes are sitting in the source: an unconditional sleep before an
assertion, an un-awaited async call, state one test leaves behind for another, a live network call, an
unseeded random value, an assertion against the real clock. It reads your test suite and names them, on
the day you install it.

**It never runs anything** — not the suite, not a build, not an install, and not to check that a fix
worked. That last exclusion is the deliberate one: an agent that can run the tests it just edited is an
agent that can iterate until green, and iterating until green is how tests get quietly weakened.
Verification stays with you and your CI.

**A fix removes the cause.** Deleting an assertion, loosening one until it always passes, skipping the
test, marking it expected-to-fail, adding a retry, or lengthening a sleep are all forbidden as remedies —
they make the symptom disappear and leave you worse off, because now the suite lies quietly. Edits stay
inside test and test-support files; where the genuine remedy belongs in application code, the item is
left open with a note saying what would need to change and where.

**Two gates, with your review in between.** The run reports a ranked table — test, file, confidence, and
a specific fix — and stops. On your go-ahead it writes `.specify/memory/flaky-test-analysis.md`: a run
summary, one `[ ]` row per candidate, the evidence behind each, and an honest account of what it could
not examine. You delete the rows you disagree with. On a second go-ahead it works what is left, one item
at a time, ticking each `[x]` on disk as it lands — so an interrupted session leaves a file that is
exactly true rather than one that claims nothing happened. Nothing is ever committed; the working-tree
diff is your review surface.

**The list outlives the session**, which is the point of writing it down. Every run reads that file first
and branches on what it finds: unfinished work resumes without re-analysing and without discarding your
pruning, a completed list asks before it is replaced, and a file it cannot parse is never overwritten
silently. There is exactly one analysis file at any time.

## Arguments

optional. With none, it analyses the whole working tree; give it a path or a suite name
to narrow the run. Before a narrowed run replaces a broader plan, it names the pending items that would
be dropped and waits for an answer.

## Use it when

your suite has become something people re-run rather than trust, and you want a short
reviewable list of what to fix rather than a dashboard telling you it is bad.

## Confidence

High, Medium, or Low, rating the strength of the evidence rather than a failure rate.
With no run history there is no denominator, so it emits no percentage, score, or flakiness index.

## Your guardrails bind it

it reads your project's own constitution, and where a rule forbids the
only available remedy, the item is left open naming that rule instead of producing a fix your review
would reject.

## Where it writes

`.specify/memory/flaky-test-analysis.md`, and test code you approved row by row.
Never production source, never governance, never a commit.

## Examples

```
/speckit-spectra-flaky-test-detector
/speckit-spectra-flaky-test-detector api/
```

## The list is meant to outlive the session

There is exactly **one** analysis file, at `.specify/memory/flaky-test-analysis.md`, at any time. Close
your terminal mid-run and the file is still exactly true — progress is written after every single fix, not
batched at the end — so the next run picks up the remaining items without re-analysing and without
discarding the pruning you did. A completed list is never replaced without asking. A file it cannot parse
is never overwritten silently; it says what it could not read and waits. And before a run scoped to one
suite replaces a plan covering more, it names the pending items that would be dropped.

The file is yours to edit. Delete rows to exclude those tests, reword a suggested fix and it acts on your
wording, tick an item yourself and it skips it. Only structural damage — a missing `## Tasks` heading,
rows it cannot resolve — counts as unreadable.

## Confidence, and what it is not

High, Medium, or Low, rating **the strength of the evidence in your source**, not a measured failure rate.
High requires the triggering construct in the test's own body or its direct fixtures, citable by line.
With no run history there is no denominator, so the command emits no percentage, score, or flakiness
index — inventing one would be the easiest way to sound authoritative and be wrong.

Your project's constitution binds the fix it chooses. If a guardrail rules out the only available remedy —
no mocking libraries, no new test dependencies — the item is left open with that rule named, rather than
producing a change your own review would reject.

## How it works

It is the only Spectra agent that edits code you wrote.

1. Reads `.specify/memory/flaky-test-analysis.md` first, before anything else, and branches on what it
   finds.
2. Identifies your test suites from the working tree — runner configuration, test scripts in the project
   manifest, directory conventions, filename patterns — and reports each with its framework and file
   count before naming a single candidate. Several suites in several languages are fine.
3. Reads the tests for the eight signal categories: timing and async, isolation and shared state,
   unmocked external dependencies, non-determinism, brittle assertions, parallel-execution conflicts,
   environment coupling, and existing retry or known-flaky annotations.
4. Reports the ranked table and stops, asking before it writes anything.
5. On your go-ahead writes the plan, then stops again and tells you to delete the rows you disagree with.
6. On a second go-ahead works the surviving rows in file order, ticking each `[x]` on disk as it lands,
   and closes with what it fixed, what it left open and why, and every file it touched.

A fix may create a helper or a mock where it needs one, and it will say so — but it never touches
production source and never adds a new dependency.
