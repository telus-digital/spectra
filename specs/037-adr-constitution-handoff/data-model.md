# Data Model: The ADR Agent Hands Off to the Constitution

All entities are Markdown written by `speckit.spectra.adr` into the ADR it created in the same run. Formats
are command-owned: a template can place the sections, never change them (research R4).

## Constitution check result

Computed in Step 7, per guardrail candidate, by reading `.specify/memory/constitution.md` semantically
(section heading + normative keyword + subject), never by string match.

| State | Meaning | Effect |
|---|---|---|
| `embedded` | the constitution already states it | quote the governing clause; draft nothing |
| `partial` | a clause exists but omits or contradicts part of it | quote it, name the gap; draft `amends: <principle>` |
| `absent` | nothing normative covers it | draft `new` |
| `no constitution` | the file does not exist | draft `new`; goal `pending` (R5) |
| `sibling ground` | it falls on another feeder's ground | draft nothing; refer (see Referral) |

## Guardrail record

One per drafted clause, in `## Constitution guardrails`, accepted or not. Keys in exactly this order:

```markdown
- **<Statement — declarative and testable, MUST/SHOULD, with a brief rationale>**
  - id: `adr-NNN-<section-slug>-<hash>`
  - section: <Target constitution section>
  - basis: observed | aspirational
  - decision: accepted | declined | skipped | not_asked
  - status: new | amends: <Principle name/number> | adopted: <Principle name/number>
```

| Field | Rule |
|---|---|
| id | R3. Frozen at drafting; a reword keeps it |
| section | the project constitution's own section names; Spec Kit's defaults where none exists |
| basis | `observed` if the codebase already holds the rule, else `aspirational` |
| decision | set by the gate only (transitions below) |
| status | `adopted` when the constitution already carries it verbatim in substance; `amends` on `partial` or supersession (FR-006) |

### Decision transitions (the gate, asked once)

| User's answer | Result |
|---|---|
| Approve | every shown record `accepted`; named-to-decline → `declined`; named-to-reword → `accepted`, new statement, same id |
| Revise the ADR first | ADR edited in place; records re-drafted; gate offered again |
| Talk it through | no change until another answer |
| Decline all | every record `skipped` |
| No answer / non-interactive | every record `not_asked` |

## Constitution input section

`## Constitution input`. Holds **exactly** records with `decision: accepted` and status not `adopted`.

```markdown
## Constitution input

Constitution check: <one line per candidate state, quoting governing clauses; contradictions named>
ADR status at drafting: Proposed
Goal: **update** the constitution at `.specify/memory/constitution.md` with the guardrails below.

### <Target constitution section>

- <Statement, as accepted>
  - id: `adr-NNN-<section-slug>-<hash>`
  - placement: add | amends: <Principle name/number>
  - basis: observed | aspirational
```

Goal line values: `update` (records listed), `update — nothing was accepted` (one sentence, no records),
`pending — no constitution exists; these records are for a later amend` (records listed). See research R5.

## Referral

Not written as a record. Reported in the session, and once in the Constitution input section's check line:

| Ground | Owner | Document checked |
|---|---|---|
| Test levels, coverage floor, ratchet, UAT | `speckit.spectra.test-strategy` | `<root>/TEST_STRATEGY.md` |
| Environments, promotion, rollback, versioning scheme, release cut, hotfix promotion | `speckit.spectra.deployment-strategy` | `<root>/DEPLOYMENT_STRATEGY.md` |
| Languages, frameworks, runtimes, dependency policy; bounded contexts, invariants, glossary | `speckit.spectra.domain-analyzer` | `<root>/DOMAIN_ANALYSIS.md` |
| Methodology overlays, work modes, branching, review gates, change records | `speckit.spectra.methodology` | `<root>/ENGINEERING_METHODOLOGY.md` |

Where the document exists, only its `accepted` records are read; a contradicted one is named.

## Where each section goes

| Situation | Constitution guardrails | Constitution input |
|---|---|---|
| Not significant | absent | absent |
| Significant, template has the heading | filled in place | filled in place |
| Significant, template lacks it | appended after the last template section, noted once | appended after guardrails, noted once |
| ADR written before 1.26.0 | absent; never treated as missing | absent |
