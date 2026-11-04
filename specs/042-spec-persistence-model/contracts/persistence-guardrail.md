# Contract: The persistence guardrail

The canonical statement the agent proposes for each model. The agent MAY adapt wording to the project's
constitution voice and section names. It MUST keep every obligation below, MUST name phases rather than
any agent's invocation syntax (research R6), and MUST keep the cross-link wording exact. Tests pin the
obligations that make the entry answerable on its own (SC-003).

## Shared preamble (every model)

> **Spec persistence.** A new capability MUST get its own feature directory from the specify phase. The
> rules below apply to a behaviour change to a **delivered** feature, one whose directory has been merged
> to the default branch. Until then, its `spec.md`, `plan.md`, and `tasks.md` are a work area and MAY be
> edited freely.

## Living Spec

| Phase | Obligation |
|---|---|
| specify | The change MUST be made by editing the delivered feature's `spec.md`. No new feature directory is created for it. |
| plan | `plan.md` MUST be revised or regenerated from the edited spec. Decisions and rationale that still hold MUST be carried forward before anything is overwritten. |
| tasks | `tasks.md` MUST be revised so it describes the work the change needs. Git keeps the history of what it replaced. |
| implement | When implementation shows the spec is wrong, `spec.md` MUST be updated first, then `plan.md` and `tasks.md`, then the code continues. |
| converge | Runs against the revised feature directory. |

## Flow-Forward

| Phase | Obligation |
|---|---|
| specify | The change MUST get a new feature directory. Its `spec.md` MUST state `extends spec NNN` or `supersedes spec NNN` and which requirements change. The earlier `spec.md` MUST gain exactly one line, `extended by spec NNN` or `superseded by spec NNN`. No other edit is allowed in a completed feature directory. |
| plan | A new `plan.md` in the new directory; the earlier one is not edited. |
| tasks | A new `tasks.md` in the new directory; the earlier one is not edited. |
| implement | When implementation shows the spec is wrong, the **new** `spec.md` MUST be updated first. Completed directories are never edited. |
| converge | Runs against the new feature directory. |

## Flow-Back

| Phase | Obligation |
|---|---|
| specify | No new feature directory. The change MAY be recorded first in whichever artifact of the delivered feature is nearest the work: `tasks.md` for a task-level change, `plan.md` for a design change, `spec.md` for a requirement change. |
| plan | MAY lead the change, when the change is a design change. |
| tasks | MAY lead the change, when the change is task-level. |
| implement | A divergence MAY be recorded first in `tasks.md` or `plan.md`. `spec.md`, `plan.md`, and `tasks.md` MUST agree again **before the pull request carrying the change merges**, checked by the analyze phase reporting no inconsistency between them. |
| converge | Runs against the delivered feature directory once the three agree. |

## Hybrid (Living Spec by default)

The statement MUST contain:

1. A five-row phase table (specify, plan, tasks, implement, converge). Each row gives the Living Spec
   obligation, which is the default, and the Flow-Forward obligation, which applies to the change types the
   mapping marks `flow-forward`, each as written above.
2. The decision rule: a change within an existing capability follows Living Spec; a substantial new
   increment (a new user journey, a redesign, or a change the team would review as its own unit) follows
   Flow-Forward.
3. The accepted mapping, always (research R4), written out as `feature → …, fix → …, refactor → …, hotfix → …, docs → …,
   spike → …`. `—` means the change type needs no spec.

## Wording rules

- Cross-links are exactly `extends spec NNN`, `supersedes spec NNN`, `extended by spec NNN`,
  `superseded by spec NNN`, always naming a spec (FR-029).
- `NNN` is the spec directory's number. In a project using timestamp numbering, it is the directory's
  prefix.
- MUST/MAY as written above. The model guardrail is never offered as SHOULD (research R5).
- The persistence guardrail's implement obligation sits alongside an overlay's, for example TDD's, and
  never replaces it.
