# Engineering Methodology: [PROJECT NAME]

<!--
  HOW TO USE THIS TEMPLATE
  - This document is produced by `speckit.spectra.methodology`, a foundation-phase agent. It reports how the
    team works today, works nine lenses, asks the team to decide each lens's candidate guardrails in the
    session, and only then writes this file. It is written for two readers: a new engineer learning how
    work moves from intent to merged code, and `/speckit-constitution`, which creates or updates the
    constitution from the Constitution input section.
  - Delete any section that genuinely does not apply — remove it entirely rather than leaving "N/A". The
    command honours what this template says: a section you delete stays deleted, and the command notes
    the omission instead of putting it back. The one exception is "Constitution input": without it the
    run has nothing to hand off, so the command writes it anyway and says so.
  - What this template CANNOT change: the YAML front matter; the candidate record (keys `id`, `lens`,
    `section`, `evidence`, `basis`, `decision`, `status`, in that order); evidence for every statement of
    current practice; the observed/aspirational basis; the obligations matrix as the closed set of phase
    obligations; the Constitution input format; an ID frozen once written; and every prior team decision
    carried forward on a re-run. Those rules live in the command, not here, because `/speckit-constitution`
    and later runs of the command read this file and depend on them.
  - Organisation-specific facts — internal URLs, ticket systems, BA tools — appear only when the team
    supplies them.
  - HTML comments like this one are guidance and are stripped from the output.
-->

## Overview

<!--
  One paragraph: whether this is a brownfield or greenfield reading and the signals behind it, whether the
  constitution is being created or updated, and the methodology stack in one sentence — spec-driven
  development plus the overlays the team adopted, with their strictness.
-->

[MODE, GOAL, AND STACK]

## Methodology stack

<!--
  Spec-driven development as the fixed base. Each overlay offered, with its evidence and whether it is
  practised. Then the obligations matrix: one row per adopted overlay, one column per spec-kit phase
  (specify, plan, tasks, implement), with strictness and scope, and the evidence a reviewer checks for
  implement-phase obligations. Process cadences, if the team uses one, are described here and never
  enter the Constitution input. Then the candidate records.
-->

[STACK, OBLIGATIONS MATRIX, AND CANDIDATE RECORDS]

## Work modes

<!--
  The mode-choice table: change type (feature, fix, refactor, docs, spike, hotfix) → mode → whether a
  spec is required. Spike rules: timebox, single owner, never merged, findings captured instead of code.
  Each lens section opens with "Current practice" (brownfield, cited) or "Starting point" (greenfield),
  then one candidate record per guardrail offered — accepted or not.
-->

[MODE-CHOICE TABLE, SPIKE RULES, AND CANDIDATE RECORDS]

## Requirements intake

<!--
  Where intent comes from — BRD, ticket, issue — who owns it, how it reaches /speckit-specify, and how
  known unknowns are triaged. The BRD format itself belongs to speckit.spectra.brd.
-->

[CURRENT PRACTICE AND CANDIDATE RECORDS]

## Spec lifecycle & traceability

<!--
  Where spec artifacts live, how they are numbered, how a spec's status is kept honest against tasks.md,
  how deferred tasks are recorded, and the chain intent → spec → tasks → code.
-->

[CURRENT PRACTICE AND CANDIDATE RECORDS]

## Branching & integration

<!--
  The branching model, a branch-naming reference (prefix per change type), branch lifecycle, and merge
  strategy. How a release is cut and versioned belongs to the deployment strategy.
-->

[BRANCH-NAMING REFERENCE AND CANDIDATE RECORDS]

## Review & merge gates

<!--
  PR expectations per change type, approvals, required checks, issue linking, and documentation updated
  in the same PR.
-->

[CURRENT PRACTICE AND CANDIDATE RECORDS]

## Change records

<!--
  A commit-prefix reference (the commit convention) and how the changelog is kept. The versioning scheme
  belongs to the deployment strategy.
-->

[COMMIT-PREFIX REFERENCE AND CANDIDATE RECORDS]

## AI collaboration

<!--
  The autonomy level the team chose for AI agents between spec-kit phases, the AI assistants and
  development-workflow tools in use, and how secrets and API keys are handled. Product languages and
  frameworks belong to the domain analysis.
-->

[AUTONOMY LEVEL, TOOLS, SECRETS, AND CANDIDATE RECORDS]

## Governance & evolution

<!--
  How this methodology and the constitution are amended: one principle per amendment, explicit
  superseding, the commit as the decision record.
-->

[CURRENT PRACTICE AND CANDIDATE RECORDS]

## Related strategies

<!--
  One line each for the domain analysis, the test strategy, and the deployment strategy: a link where the
  document exists, the command that writes it where it does not. Their ground is summarised here, never
  restated.
-->

[LINKS OR COMMANDS]

## Constitution input

<!--
  Exactly the accepted candidates not already adopted, grouped by target constitution section, in the
  format the command defines. This is what /speckit-constitution consumes.
-->

[GOAL LINE AND ACCEPTED GUARDRAILS]

## Decisions and sources

<!--
  The ten questions: what was asked, the recommended option, the answer taken, and its disposition.
  Then the inputs read, anything expected and not readable, coverage of the analysis, and on a re-run what
  changed since the previous version.
-->

[DECISIONS, INPUTS, AND COVERAGE]
