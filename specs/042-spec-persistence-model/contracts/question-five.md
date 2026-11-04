# Contract: Question 5 — Spec lifecycle & traceability

This is what the command MUST make the agent do when the round reaches question 5. Tests assert this
text against `spectra/commands/methodology.md` (Step 5).

## Before the options

1. Heading: `Question 5 of 10 — Spec lifecycle & traceability`.
2. In brownfield mode, **current practice for behaviour changes**: each of the three signals (research R2)
   with its count and up to three citations, or "not found", and where the agent looked. In greenfield
   mode, or with no `specs/` history, one line: no spec history to report.
3. Lens 4's other candidates, numbered `5.1` … `5.n` (n ≤ 4), each with its statement, basis, and
   evidence, as for any lens.

## The options

Exactly five, in this order. Exactly one is marked *(recommended)*, with its reason.

| # | Label | One-line description the agent shows |
|---|---|---|
| 1 | **Living Spec** | Edit the delivered feature's `spec.md` first, then bring `plan.md` and `tasks.md` into line. Fits: the spec is the contract. Risk: losing implementation rationale when plan and tasks are regenerated. |
| 2 | **Flow-Forward** | Leave completed feature directories alone apart from one back-link line, and specify the change as a new feature that names the spec it extends or supersedes. Fits: audit trails. Risk: context spread over several directories. |
| 3 | **Flow-Back** | Record the change in whichever of spec, plan, or tasks is nearest the work, and bring the other two into line before the PR merges. Fits: small teams, fast iteration. Risk: silent drift, `spec.md` stops matching reality. |
| 4 | **Hybrid (Living Spec by default)** | Living Spec within an existing capability; Flow-Forward for a substantial new increment. Fits: most teams; the spec stays authoritative while large increments keep their own audit trail. Risk: the threshold is only as good as the mapping. Shows the proposed mapping inline: `feature` → flow-forward · `fix` → living · `refactor` → living · `hotfix` → living · `docs` → — · `spike` → — |
| 5 | **Skip** | Decide nothing about spec lifecycle now. |

**Recommended**:

- Greenfield, or brownfield with zero or several signals: **Hybrid**.
- Brownfield with exactly one signal: that signal's model.

The reason names the evidence ("3 commits edited `specs/012-*/spec.md` after delivery; no other signal").

## Recording the answer

| Reply | Model candidates | Other lens 4 candidates | Disposition |
|---|---|---|---|
| A model (1–4) | chosen `accepted`, other three `declined` | same decision as the model, unless free text excludes them | `answered` |
| Hybrid + free-text mapping change ("refactor is flow-forward") | Hybrid `accepted` with the adjusted mapping | as above | `answered` |
| Model + free-text candidate change ("Living Spec, drop 5.3") | chosen `accepted` | named ones `declined`, rest `accepted` | `answered` |
| Skip | all `skipped` | all `skipped` | `skipped` |
| "Use your defaults" (here or earlier) | recommended `accepted`, with the proposed mapping for Hybrid | `accepted` | `default_taken` |
| No answer | all `not_asked` | all `not_asked` | `not_asked` |
| A question back | none; answer it, ask question 5 again | — | does not advance |

## Re-run variant

- **Prior `persistence` set**: open with "Last run you chose **<model>**; still right?". Pre-select it
  and, for Hybrid, the prior mapping. Name any model declined last run. All five options stay
  selectable.
- **No prior key**: ask as new, recommending from the evidence.

## Non-interactive

Not asked. All four model candidates are `not_asked`, no `persistence` key, and nothing about persistence
reaches the Constitution input.

## What question 5 never does

- It never adds a question or renumbers one. Hybrid's mapping is settled inside question 5.
- It never edits `specs/`, the constitution, or any file but the methodology document.
- It never treats the TDD overlay's implement obligation as conflicting with the persistence guardrail's.
