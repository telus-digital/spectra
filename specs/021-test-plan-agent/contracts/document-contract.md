# Contract: The Test Plan Document

**Produced by**: `speckit.spectra.test-plan` | **Template**: `test-plan-template`

## Write target

```text
<directory of the resolved specification>/test-plan.md
```

Fixed by the input. Not numbered, not placed in an artifact subfolder, not subject to artifact-root
resolution or a publication check.

**The in-project guard replaces the write-scope protection the artifact root would have given.** The
resolved specification's directory MUST lie inside the project the command was invoked in. Otherwise the
run reports the conflict and stops — it does not write outside the project, and it does not relocate the
output into the project instead.

**Why here and not under the artifact root.** Constitution Principle VII places `specs/` outside its
location rule. This document is consumed by `/speckit-plan`, which is the relationship that carve-out
describes, and its identity is the feature directory — exactly as `spec.md`, `plan.md`, and `tasks.md`
carry no sequence number because the directory already supplies one. The full argument, including the
part where the fit is imperfect because the document is *also* a stakeholder deliverable, is in
[plan.md](../plan.md) under Complexity Tracking.

## Section order

As resolved from the template. The shipped template's order:

| # | Section | Contents |
|---|---|---|
| — | Identifying block | Spec (path or link) · Build under test · Author / Date |
| 1 | Scope | In scope; out of scope, each out-of-scope item naming who covers it if anyone |
| 2 | Risks | 2–5 rows: risk, likelihood, impact, testing response |
| 3 | Test Conditions | The table; then **Explicitly not covered**, each with a reason |
| 4 | Environment & Data | Where tests run and what is stubbed; test data and its reset; prerequisites |
| 5 | Exit Criteria | Declarative statements, each with a threshold and the role who confirms it |
| — | Optional sections | Only those whose trigger fired, named as added and why |
| — | Sources consulted | What was read, what could not be, and the coverage statement |

## The no-checkbox rule

The document MUST contain no `- [ ]` and no `- [x]`, in any section, from any template layer.

This is the **one** place the command overrides a template's content rather than merely declining to
extend it. A checkbox found in a resolved layer is rendered as a plain statement and the conversion is
counted in the run report. The command does not refuse the override and does not drop the section.

**Why the command owns this and not the template.** Principle VIII puts the rules that make output
trustworthy in the command. An approval document containing live checkboxes creates a second apparent
source of truth about progress, and it will disagree with `tasks.md`. A template asking for checkboxes is
asking for a tracker; `tasks.md` already is one.

## What the document never contains

| Forbidden | Requirement |
|---|---|
| A checkbox construct | FR-041 |
| A status, progress, or completion field | FR-042 |
| An unfilled placeholder token or a guidance comment | FR-043 |
| The optional-section guidance list from the template | FR-044 |
| A minted identifier for a specification item | R3 |
| A secret value, whole or partial | FR-020b |
| An unqualified claim of absence | FR-028 |
| A level or tool the project's stack cannot run | FR-037 |
| A test script or step sequence in the condition column | FR-038 |

## Template resolution

Highest priority first. Take the first layer that is readable **and** non-empty:

1. `.specify/templates/overrides/test-plan-template.md`
2. `.specify/presets/<preset-id>/templates/test-plan-template.md`
3. `.specify/extensions/spectra/templates/test-plan-template.md`
4. `.specify/templates/test-plan-template.md`
5. The command's own inline skeleton — last resort, for a project with no `.specify/` at all

A layer that is present but empty or unreadable is reported in one line and skipped. The resolved layer's
path is reported. No template path is hard-coded, no template file is ever written, and the override path
is named once as the supported customization route.

## What an override may and may not do

| May | Result |
|---|---|
| Drop a section — including the risk table or the exit criteria | The section goes; the command notes the omission and does not reinstate it |
| Reorder sections | Followed as resolved |
| Rename a section | Followed as resolved |
| Add a section | Filled if the command has content for it; otherwise noted as unfilled and removed |
| Change the level column's example values | Ignored — the vocabulary comes from the project's strategy, not the template |

| May not | Result |
|---|---|
| Reintroduce a checkbox | Rendered as a plain statement |
| Remove the traceability obligation | The invariant lives in the command; dropping the `Verifies` column removes the column, and the covered-out-of-found count still appears in the session report |
| Remove the coverage statement | Dropping *Sources consulted* removes the section; the command still states coverage in the session |
| Make the command claim absence without a search, name an unrunnable tool, or print a secret | Not template-governed |
