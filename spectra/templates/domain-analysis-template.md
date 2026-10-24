# Domain Analysis: [PROJECT NAME]

<!--
  HOW TO USE THIS TEMPLATE
  - This document is produced by `speckit.spectra.domain-analyzer`, a foundation-phase agent. It infers
    the project's business domain, works six lenses, asks an SME to decide each lens's candidate
    guardrails in the session, and only then writes this file. Its purpose is to be the input
    `/speckit-constitution` creates or updates the constitution from.
  - Delete any section that genuinely does not apply — remove it entirely rather than leaving "N/A". The
    command honours what this template says: a section you delete stays deleted, and the command notes
    the omission instead of putting it back. The one exception is "Constitution input": without it the
    run has nothing to hand off, so the command writes it anyway and says so.
  - What this template CANNOT change: the YAML front matter; the candidate record (keys `id`, `section`,
    `evidence`, `basis`, `confidence`, `decision`, `status`, in that order); at least one file path of
    evidence per candidate; the Constitution input format; an ID frozen once written; and every prior
    SME decision carried forward on a re-run. Those rules live in the command, not here, because
    `/speckit-constitution` and later runs of the command read this file and depend on them.
  - HTML comments like this one are guidance and are stripped from the output.
-->

## Constitution status and goal

<!--
  Whether `.specify/memory/constitution.md` exists, its version and principle count if so, and the goal
  that follows: create the constitution from this analysis, or update it.
-->

[CONSTITUTION STATUS AND GOAL]

## Inferred domain

<!--
  One paragraph: what the system is and what it handles, then the evidence basis — which artifacts led
  there — and the alternative reading considered. Say whether the SME confirmed or corrected it. Say so
  plainly when the project is sparse. Add the advisory-only compliance add-on note here when the domain
  is regulated.
-->

[DOMAIN SUMMARY, EVIDENCE BASIS, AND CONFIRMATION]

## Domain & business rules

<!--
  Each lens section opens with current practice, cited, then one candidate record per guardrail offered —
  accepted or not. A lens with nothing to propose says what was searched and where.
-->

[CURRENT PRACTICE AND CANDIDATE RECORDS]

## Data sensitivity & regulation

[CURRENT PRACTICE AND CANDIDATE RECORDS]

## Security & trust boundaries

[CURRENT PRACTICE AND CANDIDATE RECORDS]

## Architecture & boundaries

[CURRENT PRACTICE AND CANDIDATE RECORDS]

## Technology & dependency policy

[CURRENT PRACTICE AND CANDIDATE RECORDS]

## Reliability & operability

<!-- Testing and deployment policy is referred to speckit.spectra.test-strategy and
     speckit.spectra.deployment-strategy, and workflow — branching, review, commit conventions,
     governance — to speckit.spectra.methodology, not proposed here. -->

[CURRENT PRACTICE AND CANDIDATE RECORDS]

## Constitution input

<!--
  Exactly the accepted candidates not already adopted, grouped by target constitution section, in the
  format the command defines. This is what /speckit-constitution consumes.
-->

[GOAL LINE AND ACCEPTED GUARDRAILS]

## Decisions and sources

<!--
  The seven questions: what was asked, the recommended option, the answer taken, and its disposition.
  Then the inputs read, anything expected and not readable, coverage of the analysis, and on a re-run what
  changed since the previous version — including any Delivery & workflow records from an earlier version,
  kept under "Handed on to speckit.spectra.methodology".
-->

[DECISIONS, INPUTS, AND COVERAGE]
