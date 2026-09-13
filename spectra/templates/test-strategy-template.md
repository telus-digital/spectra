# Test Strategy: [PROJECT NAME]

<!--
  HOW TO USE THIS TEMPLATE
  - This document is produced by `speckit.spectra.test-strategy`, a foundation-phase agent. It states
    how this project tests itself and what floor it holds, so every later work session inherits one
    answer instead of re-deciding.
  - Fill every [PLACEHOLDER]. Delete any section that genuinely does not apply — remove it entirely
    rather than leaving "N/A". The command honours what this template says: a section you delete stays
    deleted, and the command notes the omission instead of putting it back.
  - What this template CANNOT change: every recommendation carries a citation, a convention marker, or
    a stated marker naming the question it came from; an answer the user gave is never written up as
    evidence and never moves a measured figure; a brownfield floor never exceeds the measured baseline;
    a baseline is always labelled measured / reported / unavailable; no tool is named that this stack
    cannot run; and coverage of the analysis is always stated. Those rules live in the command, not
    here.
  - The document's YAML front matter is written by the command, not by this template, and it has to
    parse. Overriding the body is supported; reshaping the header is not.
  - HTML comments like this one are guidance and are stripped from the output.
-->

## Classification and evidence

<!--
  greenfield | brownfield | mixed, with the signals that produced it and any signal that pointed the
  other way. A reader must be able to tell a strategy proposed for code that does not exist yet from
  one measured against code that does.
-->

**Mode**: [GREENFIELD / BROWNFIELD / MIXED]

| Signal | Reading | Evidence |
|---|---|---|
| [signal] | [what it indicated] | [path] |

**Signals pointing the other way**: [list, or "none"]

## Testable surfaces

<!--
  One row per part of the repository with its own toolchain and therefore its own testing answers. A
  single-stack project has exactly one and does not belabour it.
-->

| Surface | Root | Stack | Manifest | Declared or inferred |
|---|---|---|---|---|
| [name] | [path] | [stack] | [path] | [declared / inferred] |

## Unit testing

<!--
  Applicable with an approach, or not applicable with a reason. In brownfield, state what exists today
  — with citations — before proposing anything.
-->

**Applicability**: [APPLICABLE / NOT APPLICABLE — reason]

**Proves**: [what this lens is responsible for establishing here]

**Boundary**: [where it hands off to the adjacent lenses]

**Today**: [brownfield only — what exists, cited]

**Recommended approach**: [approach]

**Tools**: [tool — tier and evidence]

## Integration testing

**Applicability**: [APPLICABLE / NOT APPLICABLE — reason]

**Proves**: [what this lens is responsible for establishing here]

**Boundary**: [where it hands off to the adjacent lenses]

**Today**: [brownfield only — what exists, cited]

**Recommended approach**: [approach]

**Tools**: [tool — tier and evidence]

## API contract testing

**Applicability**: [APPLICABLE / NOT APPLICABLE — reason]

**Proves**: [what this lens is responsible for establishing here]

**Boundary**: [where it hands off to the adjacent lenses]

**Today**: [brownfield only — what exists, cited]

**Recommended approach**: [approach]

**Tools**: [tool — tier and evidence]

## End-to-end testing

<!--
  The surface is browser, http, cli, or none. "None" is a valid and expected outcome for a library, and
  is better than a browser driver this project cannot run.
-->

**Surface**: [BROWSER / HTTP / CLI / NONE]

**Applicability**: [APPLICABLE / NOT APPLICABLE — reason]

**Proves**: [what this lens is responsible for establishing here]

**Boundary**: [where it hands off to the adjacent lenses]

**Today**: [brownfield only — what exists, cited]

**Recommended approach**: [approach]

**Tools**: [tool — tier and evidence]

## Coverage floor

<!--
  One block per surface where surfaces have different baselines. The floor is a floor, not a target,
  and it must be one this project can hold on its next build.
-->

**Surface**: [name, or "all"]

**Metric**: [line / branch / statement — whatever this surface's tooling reports]

**Baseline**: [figure, or "none"] — **[MEASURED / REPORTED as of DATE / UNAVAILABLE]**

**Floor**: [figure, or "conditional on the tooling below"]

**How the floor was derived**: [rounding applied to the baseline]

**Target**: [long-term figure]

**Ratchet**:

| Trigger | Step |
|---|---|
| [condition that can be checked from the repository] | [increase] |

**What this floor does not prove**: [statement]

**To enforce it**: [the exact configuration change — stated here, applied by the team]

## Recommendations summary

<!--
  Every actionable statement in one table, so a reader can see the whole plan without re-reading the
  lenses. Each carries its evidence, is marked as a convention, or is marked as stated by the team —
  one of the three, never none.
-->

| # | Lens | Surface | Recommendation | Evidence | Scope |
|---|---|---|---|---|---|
| 1 | [lens] | [surface] | [statement] | [path, or "convention", or "stated: Q<n>"] | [surface-specific / repository-wide] |

## Proposed constitution amendment

<!--
  Drafted here; applied by `/speckit-constitution`. Nothing in this section has been written to the
  constitution — this command never writes that file.
-->

**Already in the constitution?**: [EMBEDDED / PARTIAL / ABSENT / NO CONSTITUTION]

**Governing clause today**: [quoted text, where one exists]

**Conflict found**: [where an existing principle contradicts a recommendation above, or "none"]

**Approval**: [APPROVED / DECLINED / NOT ASKED]

**Proposed text**:

```markdown
- [ ] [statement in the constitution's voice, MUST/SHOULD, with a brief rationale]
      section: [target section]
      status: [add | amends: <principle name>]
```

**To apply it**: [the command the user runs, referencing this document]

## Sources consulted and coverage of analysis

<!--
  What was read, what was not, and what the analysis could not see. A reader must be able to tell
  "checked and found nothing" from "did not check".
-->

**Read**: [count] of [count] files present — [selection method]

**Could not see**: [what was out of reach, and why]

**Inputs consulted**:

| Input | Read? | Note |
|---|---|---|
| [path] | read / unreadable / missing | [reason where not read] |

**Inputs from the user**:

<!--
  What was asked, what was recommended, and what came back. The user's answers are a source consulted,
  which is why they are recorded here rather than in a section of their own. A reader must be able to
  tell an answer the team gave from a figure this analysis measured — so does every row that a
  recommendation elsewhere cites as "stated".
-->

| # | Question | Recommended | Answer | Disposition |
|---|---|---|---|---|
| [n] | [what was asked] | [the answer proposed] | [the answer taken] | answered / default taken / not asked |

**Tool verification**: no recommendation in this document was checked against a package registry; this
analysis made no network request.
