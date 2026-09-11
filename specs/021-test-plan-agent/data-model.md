# Phase 1 Data Model: Test Plan Agent

**Feature**: `speckit.spectra.test-plan` | **Branch**: `021-test-plan-agent` | **Date**: 2026-09-11

Nothing here is a database schema. These are the entities the command must hold in mind while it runs and
the fields it must be able to fill or explicitly mark unfillable — the difference between a prompt that
produces a plausible document and one that produces a checkable one. Every field is either derived from
something read in this run or carries its own "not available, and here is why".

---

## 1. Entities

### `ResolvedInput`

What the argument turned out to mean. Established before anything else is read.

| Field | Values | Notes |
|---|---|---|
| `raw_argument` | text | Whatever remained after flags |
| `spec_path` | project-relative path | The resolved specification |
| `resolution` | `direct-file` · `from-directory` · `unresolved` | `from-directory` is stated aloud (R1) |
| `feature_dir` | project-relative path | The specification's directory; the write target |
| `in_project` | `true` · `false` | `false` stops the run before any write (FR-022) |
| `usability` | `usable` · `rejected` | With the reason when rejected |

**Invariant.** No `ResolvedInput` is ever constructed from inference. With no argument the entity does not
exist and the run ends (FR-008).

### `SpecificationInput`

The document being planned against. Read-only, always.

| Field | Values |
|---|---|
| `title` | text |
| `requirements[]` | `{ id?, text, kind: functional · non-functional · prohibition }` |
| `stories[]` | `{ id, title, priority: P1 · P2 · P3, acceptance_criteria[] }` |
| `success_criteria[]` | `{ id?, text, measurable: true · false }` |
| `unresolved_markers[]` | text — each `[NEEDS CLARIFICATION]` found |
| `has_priorities` | `true` · `false` — false changes R8's derivation |
| `has_identifiers` | `true` · `false` — false forces R3's quotation fallback |

### `ProjectContext`

Everything else read, with its provenance. This entity is what makes Principle IV checkable.

| Field | Values | Notes |
|---|---|---|
| `constitution` | `present` · `absent` | Path when present |
| `constitution_testing_obligation` | text · `none` | Outranks the strategy (FR-013) |
| `artifact_root` | path | `declared` · `default` · `declared-unusable` (R5) |
| `strategy` | `present` · `absent` · `unreadable` | With path and reason |
| `lens_vocabulary` | list of names | Plus `source`: `strategy` · `constitution` · `default` |
| `suite` | `present` · `absent` | Test directories and runner configuration found |
| `stack_surfaces[]` | `browser` · `http` · `cli` · `library` · `none` | Gates which levels may be used (FR-037) |
| `touched_source[]` | paths | The code the specification's behaviour reaches |
| `existing_coverage[]` | `{ behaviour, test_path, confidence }` | Citation required (FR-029) |
| `coverage_searches[]` | `{ terms, paths, result }` | Citation for every absence (FR-028) |
| `read_coverage` | `{ files_read, files_present, method }` | The FR-016 statement |
| `unreadable_inputs[]` | `{ path, reason }` | Named, never silently dropped (FR-015) |

### `TestCondition`

The unit of the document and of traceability.

| Field | Values | Rule |
|---|---|---|
| `id` | `T1`, `T2`, … | Sequential within this document only |
| `condition` | one line | A thing that must be true, never a script (FR-038) |
| `verifies` | spec identifier · `USn-ACn` · quotation | From `SpecificationInput`, never minted (R3) |
| `level` | a name from `lens_vocabulary` | Must be runnable on `stack_surfaces` (FR-037) |
| `priority` | `P1` · `P2` · `P3` | Inherited per R8 |
| `already_covered` | `{ test_path }` · `null` | Citation required when set |

### `UncoveredItem`

The counterpart that makes the invariant honest. A specification item with no condition.

| Field | Values |
|---|---|
| `verifies` | the spec identifier |
| `reason` | `unresolved-clarification` · `untestable-as-written` · `out-of-scope` · `deferred` |
| `remedy` | text — `/speckit-clarify` for the first reason (FR-026) |

### `Risk`

| Field | Values | Rule |
|---|---|---|
| `risk` | one line | What could break |
| `likelihood` | `H` · `M` · `L` | Derived, per R7 |
| `impact` | `H` · `M` · `L` | Derived, per R7 |
| `response` | `deeper-coverage` · `extra-scenario` · `accept` | `accept` is first-class |
| `trigger` | text | The condition that produced the rating |

### `ExitCriterion`

| Field | Values | Rule |
|---|---|---|
| `criterion` | one line | A declarative statement, **never** a checkbox (FR-041) |
| `threshold` | text | The bar, stated numerically where the spec allows |
| `confirmed_by` | role | Who makes the call (FR-040) |

### `BuildUnderTest`

| Field | Values |
|---|---|
| `branch` | text |
| `version` | text · `not-committed` |
| `version_source` | path · `none` |
| `component` | text · `unnamed` |

**Invariant.** No field is ever inferred. `not-committed` is a correct answer; a guessed release number is
not (R11).

### `TemplateResolution`

| Field | Values |
|---|---|
| `layer` | `override` · `preset` · `extension` · `core` · `inline-skeleton` |
| `path` | path · `n/a` for the skeleton |
| `skipped[]` | `{ path, reason }` — present but empty or unreadable |
| `sections` | ordered list, as resolved |
| `omitted_sections[]` | sections the command would have filled — noted, never reinstated (FR-055) |
| `checkboxes_rendered_plain` | count — how many constructs were converted (FR-041) |

### `OptionalSection`

| Field | Values |
|---|---|
| `name` | from R12's table |
| `trigger_found` | text — the evidence |
| `added` | `true` · `false` |

### `TestPlan`

The output. One per feature directory.

| Field | Values |
|---|---|
| `path` | `<feature_dir>/test-plan.md` — fixed |
| `mode` | `created` · `rewritten` · `not-written` |
| `carried_forward[]` | not-covered decisions preserved from a prior plan (FR-051) |
| `dropped[]` | prior decisions deliberately removed — stated in the report |

---

## 2. Document schema

The written document, in the order the shipped template fixes. An override may reorder or drop; the
command follows what it resolved and notes omissions (FR-055).

```text
# Test Plan — <feature name>

<identifying block>            Spec · Build under test · Author / Date        FR-030
## 1. Scope                    In scope; out of scope with an owner each      FR-031
## 2. Risks                    2–5 rows, derived ratings, response each       FR-032, FR-033
## 3. Test Conditions          the table, then "Explicitly not covered"       FR-034, FR-039
## 4. Environment & Data       environment · test data · prerequisites        FR-040
## 5. Exit Criteria            declarative statements, no checkboxes          FR-040, FR-041
<optional sections>            only those whose trigger fired                 FR-045
<sources consulted>            what was read, what was not, coverage          FR-015, FR-016
```

**What the document never contains**, in any section, from any template layer:

| Forbidden | Requirement |
|---|---|
| `- [ ]` or `- [x]` | FR-041 |
| A status, progress, or completion field | FR-042 |
| An unfilled `[PLACEHOLDER]` token or guidance comment | FR-043 |
| The optional-section guidance list | FR-044 |
| A secret value, whole or partial | FR-020b |
| An unqualified claim of absence | FR-028 |
| A level or tool the stack cannot run | FR-037 |

---

## 3. Run states

```text
                    ┌─────────────────┐
                    │  argument read  │
                    └────────┬────────┘
            empty ───────────┤
                             │
              ┌──────────────▼──────────────┐
              │ ASK-AND-STOP · nothing read │  FR-007 to FR-009
              └─────────────────────────────┘

          path supplied
                             │
              ┌──────────────▼──────────────┐
              │        resolve input        │  R1
              └──────┬───────────────┬──────┘
        unresolvable │               │ resolved
                     ▼               │
         ┌──────────────────┐        │
         │ REPORT-AND-STOP  │        │
         └──────────────────┘        │
                                     ▼
                     ┌───────────────────────────────┐
                     │ GATE 2 — in project?  FR-022  │
                     └────────┬──────────────┬───────┘
                        no    │              │ yes
                              ▼              │
                  ┌──────────────────┐       │
                  │ REPORT-AND-STOP  │       │
                  └──────────────────┘       │
                                             ▼
                             ┌───────────────────────────────┐
                             │ read context · resolve lenses │
                             │ resolve template · derive     │
                             └───────────────┬───────────────┘
                                             ▼
                     ┌───────────────────────────────────────┐
                     │ GATE 1 — plan exists? FR-050 to FR-052│
                     └──────┬─────────────┬──────────────────┘
              exists, no    │             │ absent, or confirmed
              confirmation  ▼             ▼
                  ┌──────────────────┐   ┌──────────────────┐
                  │ REPORT, NO WRITE │   │  WRITE ONE FILE  │
                  └──────────────────┘   └────────┬─────────┘
                                                  ▼
                                         ┌──────────────────┐
                                         │ report + handoff │  FR-047, FR-049
                                         └──────────────────┘
```

**Gate ordering is deliberate.** Gate 2 fires before anything is read, because a specification outside the
project is a stop regardless of content. Gate 1 fires *after* the derivation, so the user being asked
whether to rewrite can be told what would change — a confirmation request with no information attached is
one a user learns to answer reflexively.

**Every terminal state that does not write says why.** There is no silent no-op (FR-049).

---

## 4. Validation rules, as assertions

Restated as the checks an implementation review runs against the shipped command text.

| # | Rule | Source |
|---|---|---|
| V1 | Empty argument → asks, reads nothing, writes nothing | FR-007 to FR-009 |
| V2 | No inference clause anywhere: no branch, no `feature.json`, no mtime, no `specs/` scan | FR-008 |
| V3 | Exactly one write target, `<feature_dir>/test-plan.md`, and the input spec is never modified | FR-018, FR-021 |
| V4 | Every acceptance criterion appears in `TestCondition.verifies` or in `UncoveredItem` | FR-023, FR-025 |
| V5 | Every `TestCondition.verifies` resolves to an item in `SpecificationInput` | FR-024 |
| V6 | No minted identifier for a specification item | R3 |
| V7 | No checkbox construct, from any template layer | FR-041 |
| V8 | No tracking field | FR-042 |
| V9 | Every level is in the resolved `lens_vocabulary` and runnable on `stack_surfaces` | FR-035 to FR-037 |
| V10 | Every coverage claim cites a test path; every absence cites a search | FR-028, FR-029 |
| V11 | Risk table is 2–5 rows and not uniformly H/H, or says why | FR-033 |
| V12 | The declared root is read but never written, and no publication check is performed | R5 |
| V13 | `CANONICAL` in `test_doc_output_paths.py` is not extended — pinned by a negative assertion | R5 |
| V14 | Template resolution names all four layers plus the skeleton, and reports the layer used | FR-054 |
| V15 | The report states the covered-out-of-found count and the resolved template path | FR-049 |
| V16 | The handoff is printed, never invoked; no hook is registered | FR-047, FR-048, FR-005 |
