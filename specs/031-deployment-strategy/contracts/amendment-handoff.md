# Contract: Constitution Check, Amendment Gate, Handoff

Runs only after the document is written and the report is given (FR-043, FR-044).

## Check (semantic, never a bare keyword match)

| State | Found | Action |
|---|---|---|
| `embedded` | normative deployment/release obligations covering the strategy's invariants | quote the clause; draft nothing; no gate |
| `partial` | some obligations; gaps or contradictions | quote; name the gap; draft scoped to it |
| `absent` | none | draft new items |
| `no constitution` | file missing | say so; name `/speckit-constitution` to create one; create nothing; no gate |

A contradiction with an existing principle is a separate finding; no draft silently overrides it
(FR-046).

## Draft

Durable invariants only (research R8). Format:

```markdown
- [ ] <statement in the constitution's voice, MUST/SHOULD, brief rationale>
      section: <target section>
      status: add | amends: <principle name>
```

Always unchecked. Includes, where the strategy supports it, the item that makes `DEPLOYMENT_STRATEGY.md`
the reference for environment-specific detail. Never names environments, platforms, identifiers,
cadences, or targets as obligations.

## Gate

Show the exact text, then offer: **approve** (record in the document's proposed-amendment section) ·
**modify the strategy first** (revise in place, re-summarise, re-offer) · **talk it through** (nothing
recorded yet). Declined or unanswered: nothing recorded. Non-interactive: recorded as `not_asked`.

## Invariant

The command never writes `.specify/memory/constitution.md` — not on approval, not on re-run, not when
missing, not when the user insists (FR-047).

## Handoff (closing lines)

```text
Next: review the proposed amendment in [DEPLOYMENT_STRATEGY.md](<resolved-root>/DEPLOYMENT_STRATEGY.md), then run:

/speckit-constitution Adopt the checked items in the "Proposed constitution amendment" section of <resolved-root>/DEPLOYMENT_STRATEGY.md
```

The link and the command use the path actually written. The command is printed, never invoked
(FR-048).
