# Data Model: Consistent Next-Step Suggestions Across the SDLC

Nothing is stored. The two entities are text that SPECTRA ships, plus the run outcomes that select a
closing block.

## Hook entry

An entry in `spectra/extension.yml` under `hooks.<event>`. Spec Kit copies it into a project's
`.specify/extensions.yml` at install.

| Field | Rule |
| --- | --- |
| event | One of `after_specify`, `after_clarify`, `after_implement`, `after_converge` |
| command | A dotted command id. A `speckit.spectra.*` command, or `speckit.converge` (core; see research R2) |
| optional | Always `true` |
| priority | An integer ≥ 1. It strictly increases with list position within an event that has several entries. It doesn't control what users see |
| prompt | Fixed text, true for every outcome of the command that triggers it. Names no path |
| description | One line saying when and why the offer appears |
| condition | Never present |
| list position | Sets the order users see |

Lifecycle: written by the maintainer in the manifest. Installing the extension registers it with
`enabled: true`. A user may set `enabled: false` by hand, and a later extension update re-registers it as
enabled. That is Spec Kit behaviour, recorded and not changed here.

## Closing suggestion

The final block of a SPECTRA agent's session report. It's written fresh on each run, never saved to a file.

| Field | Rule |
| --- | --- |
| label | `**Next step**` |
| command | Spec Kit's specify command for the three agents in scope, rendered in the running agent's invocation syntax (Principle III) |
| why | One line, taken from this run's outcome |
| prompt | Ready to paste, built from the run's own artifacts (document path, cause, rows) |
| no-offer reason | Replaces command, why and prompt when the outcome doesn't warrant an offer |

## Outcome states that select a block

```text
defect-rca:      validated(layer ≥ 3) ─► offer
                 validated(layer 2)   ─► offer, labelled immediate technical cause
                 none validated       ─► none + reason
                 exploration          ─► no block

impact:          analysis written     ─► conditional offer (every rating)
                 nothing written      ─► no block

flaky-test-detector:
                 Gate 1 declined      ─► no block
                 Gate 2 declined      ─► offer (all open rows)
                 worked: open rows ∈ {production code, guardrail, not confident} ─► offer (those rows)
                 worked: all fixed, or only {not found, evidence gone} open     ─► none + reason
                 Step 10 / Step 1b    ─► none + reason
```
