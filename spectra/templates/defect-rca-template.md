<!--
  Defect Root Cause Analysis — section structure for speckit.spectra.defect-rca.

  Override this file for your whole team at .specify/templates/overrides/defect-rca-template.md.
  Do not edit the installed copy under .specify/extensions/ — a version bump discards it.

  This file declares SECTIONS AND ORDER ONLY. The rules that make the document honest stay with the
  command and survive any override: answer-first ordering, the symptom/root-cause distinction, the
  recording of invalidated hypotheses, evidence-source attribution, the advisory status line, the
  related-prior-RCA field, and the prohibition on reproducing a secret.

  Every comment in this file is authoring guidance. None of it reaches the written document.
-->

# Root Cause Analysis — [DEFECT TITLE]

| | |
|---|---|
| **Defect ID** | [nnn-defect-name] |
| **Source** | [JIRA key / GitHub issue URL / direct prompt] |
| **Repository / commit** | [repo @ commit analyzed] |
| **Severity** | [Sev-1 / P1 / etc., or "not established"] |
| **Related prior RCA** | [nnn-defect-name, or "none identified — corpus searched"] |
| **Author / Date** | [owner] / [YYYY-MM-DD] |
| **Status** | Advisory — conclusions owned by [owner] |

<!--
  The status line is not decoration: it is what makes this document advisory rather than a directive.
  The commit reference is what lets a reader tell whether the code analyzed is the code that ran.
  The related-RCA row must be filled either way, so that "none identified" records that the search ran
  rather than that it was skipped.
-->

---

## 1. Root Cause

> **[The validated root cause, one or two sentences. Answer first.]**

**Symptom, for contrast:** [the technical symptom this is not]

<!--
  Nothing above this section but identity. Stating the root cause and the symptom adjacently is the
  cheapest available proof that the analysis did not stop at the first plausible code path.
-->

---

## 2. Problem Statement & Timeline

[Two or three sentences: what happened, to whom, in what environment.]

| Time | Event |
|---|---|
| [timestamp] | [what happened or was changed] |
| [timestamp] | [detection] |
| [timestamp] | [mitigation] |

<!-- Only events carrying causal weight. This is not an incident log. -->

---

## 3. Supporting Evidence

| Hypothesis | Status | Evidence | Source |
|---|---|---|---|
| [hypothesis] | Validated / Supported / Weakened / Invalidated / Unresolved | [what settled it, with file and line] | Code / Commit / Config / Test / User-supplied |

**Data gaps:** [what could not be established, and what that costs the conclusion's confidence]

<!--
  Invalidated hypotheses belong here. Recording only what was confirmed produces justification rather
  than analysis. The Source column is what makes "the repository answered this" checkable.
-->

---

## 4. Impact

- **Severity / scope:** [who and what was affected]
- **Frequency:** [occurrences, duration]
- **Quantified where possible:** [cost, SLA breach, customers affected, risk exposure]

<!-- Where impact cannot be quantified, say so. Do not omit the section. -->

---

## 5. Corrective Actions — fix this instance

| Action | Owner | Verification criteria | Due |
|---|---|---|---|
| [action] | [role or name] | [how we will know it worked] | [date] |

---

## 6. Preventive Actions — stop recurrence

| Action | Owner | Verification criteria | Due |
|---|---|---|---|
| [systemic action] | [role or name] | [how we will know it worked] | [date] |

<!--
  Sections 5 and 6 stay separate. A symptom-only fix is the primary failure mode this document exists
  to prevent: if section 6 restates section 5, the analysis did not reach a root cause.
  Ownership and verification criteria are required, and are carried as columns here rather than as
  sections of their own.
-->
