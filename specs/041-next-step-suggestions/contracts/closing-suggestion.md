# Contract: the closing suggestion

This is one shared layout for the three agents this feature changes: `defect-rca`, `impact`, and
`flaky-test-detector` (FR-011). The six existing hand-offs and `kb-vault` are not reshaped (FR-018,
FR-019).

## Layout

When an offer is made, it is the last thing in the report:

````text
**Next step** — `<Spec Kit's specify command, in this agent's invocation syntax>`: <one line on why, from this run's outcome>

```text
<ready-to-paste prompt>
```
````

When no offer is made:

```text
**Next step** — none: <one-line reason>
```

Rules:

- The label is exactly `**Next step**`. The command is in backticks.
- **The command is named, not spelled for one agent (Principle III).** Each command file says the command
  is Spec Kit's specify command and tells the agent to render it in whatever invocation syntax it uses (for
  example `/speckit-specify` or `/speckit.specify`). This follows the instruction already in
  `spectra/commands/test-plan.md`: "Render it in whatever invocation syntax this agent uses". The rendered
  examples in this contract use `/speckit-specify` only for illustration.
- The prompt is the only content of its code block and pastes unchanged after the specify command
  (SC-004).
- The block runs nothing and asks no question. Accepting it means the user runs the command.
- A run that writes nothing because of a mode or a decline, as listed per agent below, ends as it does
  today, with no block. The no-offer form is for runs that finished their work but whose outcome does not
  warrant a spec.

## `defect-rca` — attach to Step 13, Report

| Outcome | Block |
| --- | --- |
| A hypothesis reached `validated` and the document was written | Offer. Why: "the analysis validated a cause; a spec turns its corrective actions into a tracked fix". |
| The deepest validated finding is layer 2 (immediate technical cause) | Offer, and the prompt says the cause is the immediate technical cause and names what the analysis says would be needed to go deeper. |
| No hypothesis validated | `none: no cause was validated, so there is nothing yet to specify a fix for`. |
| Exploration mode | No block, because the mode writes nothing. |
| Non-interactive mode | Same as interactive. Printing runs nothing. |

The prompt contains:

- the defect id and source reference;
- the document path;
- the validated cause in one or two sentences, with its layer;
- the corrective actions from section 5;
- a line saying the preventive actions in section 6 are out of the fix's scope unless the user adds them.

## `impact` — attach to Step 14, Report, after "Status is draft…"

| Outcome | Block |
| --- | --- |
| Any run that writes an analysis | Offer, worded conditionally. Why: "the go / no-go decision is your stakeholders'. If they approve, this is the next step". |
| Any run that writes nothing | No block. |

The prompt contains:

- the feature name;
- the analysis path;
- the impact rating and its trigger;
- the external contract changes needing human verification, if any;
- the instruction that the spec must account for the findings, risks, and open questions in that analysis.

The pointer:

- never states, implies, or predicts the decision;
- is the same whatever the rating;
- adds nothing to the document, which still carries no spec reference (FR-017).

## `flaky-test-detector` — attach to Step 9, Report (and to the Step 7 decline)

| Outcome | Block |
| --- | --- |
| Rows left open with outcome "production code", "guardrail", or "not confident" | Offer for exactly those rows. Why: "these fixes are beyond what this agent may apply". |
| Gate 2 declined | Offer for every row still open in the written analysis. Why: "you chose not to have them applied here". |
| Every row fixed | `none: every proposed fix was applied`. |
| Only rows with "not found" or "evidence gone" left open | `none: the remaining rows no longer point at a test or evidence a spec could act on`. |
| Step 10 (no suite, or nothing intermittent) | `none: nothing was proposed`. |
| Step 1b (the last run finished everything) | `none: every proposed fix was applied`. |
| Gate 1 declined | No block, because nothing was written. |

Rows the developer deleted in review are never offered.

The prompt lists one line per offered row: `FT-NNN`, the test's file and name, the proposed fix, and the
recorded reason it was not applied. It also cites `.specify/memory/flaky-test-analysis.md`.
