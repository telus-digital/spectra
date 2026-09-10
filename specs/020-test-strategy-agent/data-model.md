# Phase 1 — Data Model: Test Strategy Agent

The entities the command reasons about and the schema of the one file it writes. Nothing here is a
database or a serialized structure — these are the things the prompt must keep straight and the
document must record.

Field names in the tables below are the names used in the document's front matter and section content,
so the command file, the template, and the tests can all refer to the same words.

---

## 1. Project classification

Produced once per run, before anything is proposed. Determines what the strategy may assert (R1).

| Field | Values | Notes |
|---|---|---|
| `mode` | `greenfield` \| `brownfield` \| `mixed` | FR-006. `mixed` is not a hedge — it means the signals genuinely split |
| `signals` | list of `{signal, reading, evidence}` | the five signals from R1, each with the path that produced the reading |
| `dissenting` | list of signals | signals that pointed against the chosen mode; empty for a clean read (FR-008) |

**Rule.** `mode` is always stated in the document with its `signals`. A `mixed` classification with an
empty `dissenting` list is malformed.

**Rule.** `mode` changes what may be claimed, not what is covered. Every lens appears in both modes;
brownfield adds a `current` state to each (FR-018).

---

## 2. Testable surface

One or more per run (R4). A single-surface project still produces one, but the document does not
belabour it.

| Field | Values | Notes |
|---|---|---|
| `name` | derived from the path or the workspace declaration | |
| `root` | project-relative path | |
| `stack` | what the manifest says it is | evidence for every tool recommendation scoped here |
| `manifest` | project-relative path | the file that made this a separate surface |
| `declared` | `true` \| `false` | `true` where a workspace declaration named it, `false` where it was inferred |

**Rule.** Where surfaces have different baselines, each carries its own floor (FR-027). Where a
recommendation applies to one surface, its scope is stated (User Story 5, scenario 3).

---

## 3. Lens

Four are mandatory; more may be added with justification (FR-014, FR-015).

| Field | Values | Notes |
|---|---|---|
| `lens` | `unit` \| `integration` \| `api-contract` \| `end-to-end` \| a justified addition | |
| `applicability` | `applicable` \| `not-applicable` | never omitted — a lens that does not apply says so with a reason (FR-014) |
| `reason` | text | required when `not-applicable` |
| `proves` | text | what this lens is responsible for establishing on this project (FR-020, R3) |
| `boundary` | text | where it hands off to the adjacent lenses |
| `current` | present in brownfield only | what exists today, with citations (FR-018) |
| `approach` | text | the recommendation |
| `tools` | list of tool references | each carrying its evidence tier (§6) |
| `surface` | surface name, or `all` | |

**Rule.** `current` precedes `approach` in the document. A brownfield lens that proposes before
reporting is malformed (FR-018).

**State the end-to-end lens can take** (FR-017): `browser`, `http`, `cli`, `none`. `none` is a valid
and expected outcome for a library, and it is stated rather than filled with a browser driver.

---

## 4. Coverage floor

One per surface (FR-027). The most constrained entity in the model.

| Field | Values | Notes |
|---|---|---|
| `metric` | e.g. line, branch, statement | whatever the surface's tooling reports; line is the fallback (spec Assumptions) |
| `baseline` | number, or absent | absent only when `provenance` is `unavailable` |
| `provenance` | `measured` \| `reported` \| `unavailable` | R2 |
| `as_of` | date | required when `provenance` is `reported` (FR-026) |
| `floor` | number, or `conditional` | `conditional` only when `provenance` is `unavailable` (FR-023) |
| `rounding` | text | how `baseline` became `floor` (R5) |
| `target` | number | the intended long-term value |
| `ratchet` | list of `{trigger, step}` | triggers, never dates (R5, FR-024) |
| `does_not_prove` | text | FR-025 |
| `enforcement` | text | the exact configuration change the team would make — stated, never applied (FR-047) |

**Invariant.** In `brownfield` or `mixed` mode with a numeric `baseline`: `floor <= baseline`. This is
FR-022 and it is the single most important constraint in the model — a violation ships a document that
fails the project's next build.

**Invariant.** `provenance == measured` requires that the command actually ran the tool after an
explicit confirmation (R2). A figure read from a file is `reported`, always, with `as_of`.

**Invariant.** `provenance == unavailable` requires `floor == conditional` and a first-step tooling
recommendation.

---

## 5. Recommendation

The unit the document is really made of. Every actionable statement is one.

| Field | Values | Notes |
|---|---|---|
| `lens` | lens name, or `cross-cutting` | |
| `surface` | surface name, or `all` | |
| `statement` | text | |
| `evidence` | citation, or `convention` | FR-043 — never empty |
| `citation` | project-relative path, optionally with a line | required when `evidence` is a citation |
| `searched` | text | required when the statement asserts an absence (FR-044) |
| `adoption` | `new` \| `adopted` \| `carried` | re-run only (FR-012, User Story 4) |
| `replaces_tool` | text | when present, requires a reason and a migration cost (FR-019) |
| `user_directed` | `true` \| `false` | `true` where the user asked for it; if it contradicts the evidence the disagreement is recorded (FR-046) |

**Rule.** `evidence: convention` is not a defect — it is the honest state for most greenfield
recommendations. What is a defect is a recommendation with neither a citation nor the marker.

---

## 6. Tool reference

Every tool named anywhere in the document (R9, FR-016).

| Field | Values | Notes |
|---|---|---|
| `name` | text | |
| `tier` | `present` \| `ecosystem-standard` \| `unverified` | R9's three tiers |
| `evidence` | manifest path, or stack evidence, or absent | absent only at `unverified` |
| `caveat` | text | required at `unverified`: cannot confirm current state, no network |

**Invariant.** A tool whose prerequisites the surface does not have MUST NOT appear at any tier
(FR-016). This is what makes `browser driver on a CLI project` unreachable rather than merely
discouraged.

---

## 7. Constitution amendment draft

Drafted by this command, applied by another (FR-032, FR-032a, R6, R7).

| Field | Values | Notes |
|---|---|---|
| `embedded` | `embedded` \| `partial` \| `absent` | R6's three states |
| `governing_clause` | quoted text | required when `embedded` or `partial` (FR-029) |
| `conflict` | text | where an existing principle contradicts a recommendation (FR-033) |
| `statement` | text in the constitution's voice | FR-032b |
| `section` | target section name | FR-032b |
| `status` | `add` \| `amends: <principle>` | mirrors `domain-analyzer`'s handoff shape (R7) |
| `approval` | `approved` \| `declined` \| `not-asked` | `not-asked` in a non-interactive run (FR-034) |
| `handoff` | text | the `/speckit-constitution` invocation the **user** runs |

**Lifecycle**, and where it deliberately stops:

```text
absent|partial  →  drafted  →  shown  →  approved  →  recorded in document  →  ┃ handed off
                                      ↘  declined  →  nothing recorded         ┃
                                      ↘  not-asked →  recorded as unapproved   ┃
                                                                     this command ends here
```

**Invariant.** No transition in this lifecycle writes `.specify/memory/constitution.md`. There is no
state in which this command has permission to (FR-032). `approved` authorises a paragraph in a
document the command was already writing, and nothing else.

**Invariant.** `embedded == embedded` produces no draft. There is nothing to add.

---

## 8. The strategy document

The single file, rewritten in place (FR-037, FR-042).

**Target**: `<artifact-root>/test-strategy/TEST_STRATEGY.md`, root resolved per R8.

**No sequence number** (FR-042a) — the deliberate Principle VII deviation, argued in
[plan.md](./plan.md) Complexity Tracking. Everything else about the location follows the principle.

**Front matter** (the command's fields; the template governs body sections, not these):

| Field | Notes |
|---|---|
| `mode` | §1 |
| `generated` | timestamp including time of day |
| `surfaces` | names from §2 |
| `template` | resolved template path (FR-041) |
| `coverage_of_analysis` | what was read out of what is present, and what could not be seen (FR-013) |
| `amendment` | `embedded` \| `approved` \| `declined` \| `not-asked` — from §7 |

**Body sections** come from the resolved template (FR-038 to FR-040). The shipped template declares, in
order: classification and evidence; surfaces; the four lenses; the coverage floor; recommendations
summary; the proposed constitution amendment; sources consulted and coverage of analysis. An override
may drop any of them, and the command notes the omission rather than reinstating it — including the
amendment section, which falls back to the session (FR-036).

**Re-run semantics** (FR-037, User Story 4): the file is rewritten in place. No second file, no
numbering, no supersede marker. The prior version is read first and becomes an input; recommendations
it contained that the project has since implemented are marked `adoption: adopted` rather than
re-proposed; and the run states what changed. History lives in Git (spec Assumptions).

---

## What this model deliberately has no entity for

- **A findings list.** This is not `impact` and not `flaky-test-detector`. There are no per-test
  findings and no defect records (FR-049).
- **An index.** One file, so nothing to index (contrast `impact`'s folder index).
- **A status lifecycle on the document.** A strategy is current or it is replaced; there is no draft /
  approved / superseded progression, because there is only ever one file.
- **Cross-run state.** Nothing under `.specify/`. The prior document is the only memory (FR-012).
