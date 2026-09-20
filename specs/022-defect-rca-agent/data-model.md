# Phase 1 — Data Model: Defect Root Cause Analysis Agent

**Feature**: `022-defect-rca-agent` | **Date**: 2026-09-11 | **Plan**: [plan.md](./plan.md)

Nothing here is a database schema. These are the things the command must hold coherently across a
multi-turn session and, for two of them, across runs — and the rules that keep them from drifting into
the failure modes the spec names. Fields are stated as the command tracks them; where a field reaches
the written document, the template section is named.

Two entities are **durable** (they survive the session, on disk): `RCA Document` and `RCA Index`.
Everything else is **session-scoped** and is rendered, never written (FR-036).

---

## Defect

The thing under analysis. One per session.

| Field | Source | Rules |
|---|---|---|
| `channel` | Detected from `$ARGUMENTS` (D1) | One of `github-issue`, `jira`, `plain`. MUST be stated before evidence gathering (FR-008). MUST fall back to `plain` when retrieval fails (FR-013). |
| `source_reference` | The argument as given | Recorded verbatim in the document header as the JIRA key, the issue URL, or `direct prompt` (FR-038a). Never normalized away. |
| `symptom` | Ticket, issue, or description | The observable failure. Drives the slug (D5) and the recurrence search (D2). MUST NOT be restated as a cause. |
| `environment` | User, or ticket | Where it happened. Unknown is a legal value and is recorded as unknown. |
| `severity` | Ticket, or user | Header field. Where unestablished, recorded as unestablished — never inferred from the symptom's tone. |
| `repository` / `commit` | The working tree | MUST be recorded (FR-018), and the deployed-version confirmation MUST be requested before hypotheses are built on the code. |
| `supplementary_material` | User, any turn | Logs, config, timelines, reproduction steps, statements (FR-010). Screened for secrets before anything from it reaches the document (FR-039e). |

**Validation.** A session cannot proceed past intake with no `symptom`. An empty `$ARGUMENTS` yields no
Defect at all — the command asks and stops, and MUST NOT infer one (FR-009).

---

## Hypothesis

The unit of the analysis. Many per session.

| Field | Rules |
|---|---|
| `statement` | A candidate cause, falsifiable. Not a question, not a restated symptom. |
| `branch` | Which MECE dimension it sits under (see *Hypothesis Tree*). |
| `layer` | 1–5 on the ladder: symptom, immediate technical cause, contributing factor, process/practice gap, systemic/organizational (FR-026). |
| `proposed_test` | How it would be settled. MUST be stated when the hypothesis is formed, not after (FR-027). |
| `status` | `open` → `supported` / `weakened` / `invalidated` / `validated`. |
| `evidence[]` | Zero or more Evidence records. |
| `settled_by` | The evidence that moved it to a terminal status. Required for `validated` and `invalidated`. |

### Legal state transitions

```text
open ──→ supported ──→ validated
 │  ╲        │  ╲
 │   ╲       ↓   ╲
 │    ╲   weakened ──→ invalidated
 │     ╲     ↑
 └──────╲────┘
         ╲
          ──→ invalidated
```

- `open` may go to any other status.
- `supported` ⇄ `weakened` — new evidence may push either way.
- `validated` and `invalidated` are terminal **for the evidence in hand**. Reopening is legal but MUST
  be explicit: state the new evidence and the status it moved to, so the reversal is visible.
- `invalidated → validated` MUST NOT happen silently, and MUST NOT happen at all without new evidence.
- A hypothesis MUST NOT reach `validated` on evidence that cannot settle it (FR-032) — an inability to
  disprove is `open`, not `supported`.

### Validation

- At least one `invalidated` hypothesis is expected in a healthy session (SC-003) and is required in the
  document's evidence table where one exists (FR-039a). Its absence is not an error, but a session that
  invalidated nothing MUST NOT have that fact hidden.
- A hypothesis at `layer` 1 or 2 MUST NOT be synthesized as the root cause; synthesis is blocked there
  and says what would be needed to go deeper (D4).

---

## Evidence

What moved a hypothesis. Attached to hypotheses; surfaces in the document's evidence table.

| Field | Rules |
|---|---|
| `finding` | What was observed. For a negative finding, what was searched for and where (FR-019). |
| `source` | Exactly one of `code`, `commit`, `config`, `test`, `user-supplied` (FR-039a). This column is what SC-006 is measured from. |
| `locator` | File, and line where the claim is about a specific behaviour (FR-019). For `user-supplied`, what the user provided and when. |
| `secret_screened` | Whether the finding passed the secret screen. A finding containing a credential is rewritten as kind-and-location before it may be recorded (FR-039e). |

**Validation.** Every claim about the code carries a `locator`. A claim of absence without a stated
search is not evidence. A `user-supplied` finding MUST NOT be relabelled as `code` because the command
later confirmed it — that would inflate SC-006; record a second Evidence instead.

---

## Hypothesis Tree

The MECE decomposition. One per session. **Session-scoped — rendered, never written** (FR-036).

| Field | Rules |
|---|---|
| `branches[]` | At least five major branches (FR-025), drawn from Code/Logic, Design/Architecture, Process/Practice, Environment/Config, Data, People/Knowledge, Organizational/Systemic, or domain-specific equivalents. |
| `branches[].nodes[]` | Sub-nodes with discovery questions (FR-035). |
| `branches[].status` | Rolled up from its hypotheses: `open`, `narrowing`, `refuted`, `confirmed`. |

**Validation.** Mutually exclusive — a hypothesis belongs to one branch. Collectively exhaustive — a
finding that fits no branch means the tree is wrong and a branch is added, rather than the finding being
filed under the nearest match.

---

## Data Gap

Something the repository cannot establish.

| Field | Rules |
|---|---|
| `question` | Precise, answerable, and stated with *why it matters* (D8). |
| `priority` | Ordered by how much the answer would change the hypothesis ranking (FR-029). |
| `status` | `open` → `closed` / `unobtainable`. |
| `confidence_cost` | What its remaining open costs the conclusion. Required for every gap still open at synthesis (FR-031). |

**Validation.** A gap MUST NOT be closed by the command answering it (FR-032) or by inferring a runtime
fact it never observed (FR-033). At most five open questions are put to the user per round (D8), and
reaching that cap is disclosed.

---

## Prior RCA

A document already in the corpus, matched at intake. Read-only — the command never edits one.

| Field | Rules |
|---|---|
| `id` | `NNN-<slug>`, from the filename. |
| `match_axis` | Which of symptom / implicated-code / root-cause overlap fired (D2). MUST be disclosed with the match. Title similarity MUST NOT be an axis. |
| `overlap` | The concrete thing shared — the file, the symptom shape, the mechanism. |
| `root_cause` | Quoted from the prior document's §1. |
| `preventive_actions[]` | Each with a `verdict` of `apparently-completed`, `apparently-not-completed`, or `undeterminable`, plus `citation` (required for the first two) or `reason` (required for the third) — D3. |

**Validation.** `apparently-completed` without a citation is forbidden; the verdict defaults to
`undeterminable`. A match is surfaced at intake, while the analysis is still open (FR-020) — never first
at synthesis.

---

## RCA Document — durable

The deliverable. One per run, at `<artifact-root>/defect-rca/NNN-<slug>.md`.

| Field | Template section | Rules |
|---|---|---|
| `defect_id` | Header | `NNN-<slug>`. Slug names the symptom, 3–5 words, lowercase hyphenated (D5, FR-043). |
| `source` | Header | JIRA key, issue URL, or `direct prompt` (FR-038a). |
| `repository_commit` | Header | The analyzed commit (FR-018). |
| `severity` | Header | Or recorded as unestablished. |
| `related_prior_rca` | Header | The prior id, or an explicit statement that the search ran and found nothing. MUST NOT be blank or omitted (FR-024). |
| `owner` / `date` | Header | Owner from the repository's configured Git author, offered for correction; `unassigned` where none is readable (FR-039d). Never invented. |
| `status` | Header | The advisory line. MUST NOT be softened, reworded or dropped (FR-039d). |
| `root_cause` | §1 | Answer-first, one or two sentences, at layer 3 or deeper (FR-039, D4). |
| `symptom_contrast` | §1 | Adjacent to the root cause, explicitly distinguished (FR-039). |
| `problem_statement` / `timeline` | §2 | Only events carrying causal weight. |
| `evidence[]` | §3 | Hypothesis, status, what settled it, source. Invalidated and weakened rows required where they exist (FR-039a). |
| `data_gaps` | §3 | What was unobtainable and what it costs confidence. |
| `impact` | §4 | Quantified where possible; where not, says so rather than being omitted (FR-039c). |
| `corrective_actions[]` | §5 | Action, owner, verification criterion, due. |
| `preventive_actions[]` | §6 | Same columns. A preventive action that restates a corrective one is flagged (FR-039b). |

**Validation.**

- All nine BR-06 elements present — structural, because the resolved template supplies them (SC-005).
- No guidance comment and no unfilled placeholder token survives into the file (FR-039g).
- No secret, credential, token, or item of personal data appears anywhere in it (FR-039e, SC-013).
- Where nothing was validated, `root_cause` records that, names what was ruled out, and states what
  evidence would settle it — a speculative cause MUST NOT fill the section (FR-039f).
- Written once, as the run's final act, with the number resolved at that moment (FR-043b). Never
  overwrites, amends, or replaces an existing file (FR-043a).

---

## RCA Index — durable

`<artifact-root>/defect-rca/README.md`. One row per document.

| Field | Rules |
|---|---|
| `id` | `NNN-<slug>`, linked to the file. |
| `symptom` | The observed problem, from the document. |
| `root_cause` | The validated root cause, or `none validated`. |
| `related` | The related prior RCA id, or `none`. |
| `preventive_status` | Rolled up from the document's §6 verdicts. |

**Validation.** Rebuilt from the documents actually present on every run, so a hand-added or
hand-deleted file self-corrects (FR-046). It is a **cache of the corpus and never the corpus**: a
recurrence search finding nothing in the index MUST fall back to reading the documents (FR-047).

---

## Artifact Root

Resolved per run, before anything else that touches a path.

| Field | Rules |
|---|---|
| `value` | A declared `Artifact root:` line from the constitution, matched case-insensitively; else `docs/`. |
| `determination` | `declared`, `default`, or `chosen-after-publication-signal`. Reported on completion (FR-060). |
| `publication_signal` | Which signal was found, where none was declared (FR-041). |

**Validation.** Lowercase, project-relative. A leading slash or a `..` segment makes the value unusable:
say why and fall back to the default (FR-042). Where a publication signal is found and no root is
declared, the non-publishing root is recommended, and taken outright where the choice cannot be obtained.

---

## Resolved Template

| Field | Rules |
|---|---|
| `layer` | The first readable, non-empty layer of: project override → preset → installed extension → project templates → the command's inline skeleton (FR-050). |
| `path` | Reported on completion (FR-052). |
| `sections[]` | Honoured in the template's order. The command MUST NOT add, rename, or reorder, and reports an omission rather than reinstating it (FR-051). |

**Validation.** The command never creates or edits a template file (FR-054). The rules of FR-053 — the
symptom/root-cause distinction, answer-first ordering, invalidated hypotheses, source attribution, the
advisory status line, the related-prior-RCA field, the secret prohibition — hold whichever layer
resolves. A template cannot switch a safety rule off.
