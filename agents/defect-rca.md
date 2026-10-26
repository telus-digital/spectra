---
id: defect-rca
title: Defect Root Cause Analysis
command: speckit.spectra.defect-rca
provider: spectra
type: add-on
phase: testing-quality
order: 70
status: available
summary: Take a defect from a ticket, an issue, or a description down to its root cause — with evidence read from the code, not asked for.
manifest: Guide a hypothesis-driven root cause analysis of a defect from a JIRA ticket, a GitHub issue URL, or a plain description — gathering evidence from the code, surfacing any prior analysis of the same defect, and writing one advisory analysis under the project's artifact root.
---

Take a defect down to its root cause, with evidence read from the code
rather than asked for. Conventional root cause analysis is an interview: the analyst asks an engineer
what the code does, and the answer is a memory. This agent reads the implicated code, the commits that
touched it, the configuration and the tests, reports what it found with file-and-line citations, and
spends your attention only on the runtime facts nobody can grep for — the logs, the metrics, the
environment state, what the team knew at the time.

**It takes the defect however you have it.** A GitHub issue URL, a JIRA ticket reference, or a sentence
describing what went wrong. It says which channel it resolved to before doing anything else, so a misread
costs you one word. Where the GitHub CLI is missing or JIRA is unreachable it names the failure and its
specific remedy, asks you to paste the content, and carries on — and it never asks you for a token, a
password, or a key.

**It checks whether you have analyzed this defect before, at intake.** A recurrence surfaced after the
document is written is one surfaced too late to change anything. Matches are made on implicated code, on
symptom, or on root cause — never on title similarity — and the axis that fired is disclosed with the
concrete overlap, so a spurious match costs a sentence to dismiss. Each preventive action from the
earlier analysis gets a verdict of apparently completed, apparently not completed, or undeterminable, and
the first two require a citation. Undeterminable is the default, because an uncited "completed" against
an action nobody finished is precisely what makes a recurrence read as a fresh defect.

**It will not call the first plausible code path a root cause.** Every probe names its layer — symptom,
immediate technical cause, contributing factors, process gap, systemic cause — and where the deepest
validated finding is still an immediate technical cause, the run says so and names what would be needed
to go deeper. Reading the code creates a failure mode an interviewer does not have: the path it finds is
genuinely there and genuinely related, which makes stopping feel like finishing.

**The document records what was ruled out, not only what survived.** Invalidated and weakened hypotheses
appear in the evidence table with what settled them, because a table of nothing but confirmations is a
justification rather than an analysis. Where nothing could be validated, it says so and names the
evidence that would settle it rather than promoting a guess into the heading.

## Arguments

required. With none it asks what defect to analyze and stops, inferring nothing from
your branch name, your recent commits, your open issues, or your failing tests.

## Use it when

a defect is worth understanding rather than just patching: a recurrence, a
multi-cause failure, an incident that needs a written answer, or an unfamiliar codebase where tracing
the defect by hand would take an afternoon.

## Your guardrails bind it

it reads your project's constitution and names which of its principles
bear on the analysis, by heading. Those principles are often where a systemic root cause actually
lives.

## Where it writes

`docs/defect-rca/NNN-<slug>.md` and a rebuilt folder index, under your declared
artifact root if you have one. Two files, both written as the run's final act, and nothing else
anywhere. It fixes nothing, writes no test, and never touches your ticket. The filename names the
symptom rather than the cause, because the file is named before the analysis concludes.

## Examples

```
/speckit-spectra-defect-rca https://github.com/acme/orders/issues/412
/speckit-spectra-defect-rca orders intermittently return 500 under concurrent load
```

## How it works

Run it when a defect has been found — by a failing test, by QE, or in production. Hand it the defect and
it:

1. Resolves the **channel** from what you gave it — a GitHub issue URL, a JIRA ticket reference, or a
   plain description — and says which one it picked before doing anything else.
2. Reads your project: the constitution, the implicated code, the commits that touched it, the
   configuration, the tests. It says what it examined *and what it did not*.
3. Searches your **existing analyses** for this defect, and surfaces any match while the investigation
   is still open.
4. Builds a MECE hypothesis tree, tests what the repository can settle, and asks at most five questions
   per round about the things it cannot.
5. Writes one analysis to `docs/defect-rca/NNN-<slug>.md` — or wherever your declared artifact root puts
   it — plus a rebuilt folder index.

**It reads the code before it asks you anything.** Which function handles the retry, whether the timeout
is configurable, when the offending line last changed, whether a test covers that path — those are its
questions to answer, not yours. Every claim it makes about the code cites the file and line; every claim
that something is *absent* states what it searched for and where.

An evidence table of nothing but confirmations leaves a reader unable to tell what was ruled out, so they
cannot tell how much to trust what was not — which is why invalidated hypotheses stay in the document.

## The document

**The filename names the symptom, never the cause.** `order-submission-500s`, not `missing-pool-limit`.
A cause-named file is wrong exactly when the analysis turns out to be interesting — and the flat
directory stays scannable, which is what keeps the recurrence search cheap.

**Conclusions stay yours.** Beyond fixing nothing and writing no test, it changes no configuration. The
document carries an advisory status line naming a human owner, and that line is never softened or
dropped.

The document's six sections are overridable at `.specify/templates/overrides/defect-rca-template.md`.
