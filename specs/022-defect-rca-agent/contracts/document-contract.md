# Contract — The RCA Document

**Feature**: `022-defect-rca-agent` | **Artifact**: `<artifact-root>/defect-rca/NNN-<slug>.md`

## Where it goes

| Rule | Requirement |
|---|---|
| Folder | `<artifact-root>/defect-rca/`, created on demand, lowercase and project-relative (FR-040) |
| Declared root | An `Artifact root:` line in the constitution wins, matched case-insensitively (FR-040) |
| Default | `docs/` — **only after** checking for `mkdocs.yml`, `docusaurus.config.*`, `docs/_config.yml`, `docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, or a Pages configuration pointing at `docs` (FR-041) |
| Signal found, no declaration | Surface it, recommend the non-publishing root, take it where the choice cannot be obtained (FR-041) |
| Unusable declaration | Absolute, or containing `..` — report and use the default, never guess (FR-042) |
| Superseded folder | Read for context and numbering continuity, reported once, offered as a move the user runs. Never moved, renamed, modified or deleted by the command (FR-043c) |

## What it is called

`NNN-<slug>.md` where:

- `NNN` is zero-padded three digits, scoped to this folder, **one greater than the highest already
  present** — not a count of files — starting at `001` in an empty folder, independent of the `specs/`
  sequence (FR-043).
- `<slug>` is lowercase, hyphen-separated, three to five words, describing the **observed problem** and
  never the suspected cause (FR-043, D5).

Good: `order-submission-500s`, `duplicate-invoice-emails`, `search-index-staleness`.
Wrong: `missing-pool-limit` (names the cause), `intermittent-http-500-errors-on-order-submission-under-concurrent-load` (too long), `PROJ-1234` (not a symptom).

## When it is written

Once, as the run's final act, together with the index row, with the sequence number resolved at that
moment (FR-043b). A run that stops before that point leaves the folder exactly as it found it — no
partial document, no document marked incomplete, no number consumed.

**Never** overwrites, replaces, or amends an existing file (FR-043a). A file in the folder whose name
does not match the convention is read for context, ignored for numbering, reported once, and left alone.

## Shape

From the resolved template (FR-050). The shipped default is BRD Appendix A:

```text
# Root Cause Analysis — <Defect Title>

<identity block>                  # defect id, source, repo@commit, severity, related prior RCA, owner/date, advisory status
## 1. Root Cause                  # answer first; symptom stated adjacently for contrast
## 2. Problem Statement & Timeline
## 3. Supporting Evidence         # table: hypothesis | status | evidence | source. Plus data gaps.
## 4. Impact
## 5. Corrective Actions          # table: action | owner | verification criteria | due
## 6. Preventive Actions          # table: action | owner | verification criteria | due
```

**The template owns**: which sections exist, their order, their headings.
**The command owns** (FR-053), and these hold whichever layer resolves — including a project override:

| Rule | Requirement |
|---|---|
| Answer first | The validated root cause precedes supporting argument and evidence (FR-039) |
| Symptom contrast | Stated adjacent to the root cause, explicitly distinguished (FR-039) |
| Invalidated hypotheses | Recorded, not only the surviving one (FR-039a) |
| Source attribution | Every evidence item labelled `code` / `commit` / `config` / `test` / `user-supplied` (FR-039a) |
| Advisory status line | Present, never softened, reworded or dropped (FR-039d) |
| Related prior RCA | Filled either way — the id, or that the search ran and found nothing (FR-024) |
| No secrets | No credential, token, or item of personal data, ever (FR-039e) |

Where the resolved template omits a section the command would fill, the omission is **reported, not
repaired** (FR-051).

## Content rules

| Rule | Requirement |
|---|---|
| Nine elements | Problem statement, timeline, root cause, evidence, impact, corrective actions, preventive actions, ownership, verification criteria (FR-038) |
| Identity block | Defect id, source reference, repo@commit, severity, related prior RCA, owner/date, advisory status. A field that cannot be established records that fact rather than being omitted or invented (FR-038a) |
| Owner | The repository's configured Git author, offered for correction; `unassigned` where none is readable. Never invented (FR-039d) |
| Corrective vs preventive | Separate sections. A preventive action that restates a corrective one is flagged as a sign the analysis did not reach a root cause (FR-039b) |
| Unquantifiable impact | Said so, not omitted (FR-039c) |
| Nothing validated | Recorded, with what was ruled out and what evidence would settle it. A speculative cause MUST NOT fill the section (FR-039f) |
| Placeholders and guidance | Stripped, whichever layer they came from (FR-039g) |
| Secrets in user material | Described by kind and location; the substitution stated in the session (FR-039e) |

## Rejection cases

A document MUST NOT be written that:

- names a root cause at ladder layer 1 or 2 (D4) — say what would be needed to go deeper instead;
- marks a hypothesis validated on evidence that cannot settle it (FR-032);
- records a runtime fact the command never observed or received (FR-033);
- reproduces a credential, token, or item of personal data (FR-039e);
- overwrites anything (FR-043a).
