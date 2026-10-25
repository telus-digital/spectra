# Research: The ADR Agent Hands Off to the Constitution

## R1 — Where the gate runs, and how the sections reach the file

**Decision**: Keep the step order. Step 6 writes the ADR as today. Step 7 runs the constitution check,
drafts, asks once, and then **appends** the two Constitution sections to the file it just wrote in this run.
"Revise the ADR first" edits that same file and re-offers the gate.

**Rationale**: The siblings write their single document after the round because the round decides the whole
document. For an ADR the decision is settled by Steps 2–5; the gate decides only the governance tail.
Moving the write after the gate would hold back a finished ADR on a governance question, and an
interrupted session would lose it. Appending to a file the agent created in the same run writes no second
file and touches nothing the user wrote.

**Alternatives considered**: Gate before Step 6 (rejected: delays the ADR, and a non-interactive run would
still need to write it). A separate `ADR-NNN-constitution.md` (rejected: Principle VII, one artifact type per
folder and one file per decision).

## R2 — The ground split with domain-analyzer (Spec Reconciliation C1)

**Decision (confirmed by the user, clarify 2026-10-24)**: A recorded decision outranks an inference, clause by
clause.

- The ADR agent's ground is FR-010 as written: architecture-level choices — datastores, messaging and
  eventing, architecture style, service and data boundaries and ownership, layering, integration patterns —
  and conventions no sibling owns.
- domain-analyzer keeps Lens 4 for the structure the code shows. Before drafting on Lens 4 it reads every
  `<artifact-root>/adr/*.md` Constitution input and cites an accepted record that covers the clause instead
  of drafting one.
- Languages, frameworks, runtimes, and dependency policy (Lens 5) stay domain-analyzer's alone; the ADR agent
  refers them.
- **Extended by analyze remediation U1:** the same clause-by-clause rule covers every domain-analyzer lens
  except Lens 5 — so an ADR's security, data-handling, or reliability decision (mTLS between services, a
  retention mechanism, an observability stack) is cited by Lenses 2, 3, and 6 just as Lens 4 cites an
  architecture record.
- **Analyze remediation U2:** only ADRs whose status is `Proposed` or `Accepted` count; a `Superseded` or
  `Deprecated` ADR's records serve only to find the principle a supersession amends.
- Whichever agent drafts a clause first is its source. A later ADR that changes it drafts `amends:`.

**Rationale**: Each clause keeps exactly one source, which is what the sibling-ground rule protects. The
rule the siblings use for each other — cite an existing document, otherwise name the command — is applied
at clause level here because both agents legitimately produce architecture clauses: one from observation
at onboarding, the other from deliberate decisions over the project's life.

**Alternatives considered**: Narrow ADR ground to datastores, messaging, and style (rejected — see plan,
Spec Reconciliation). Move Lens 4 wholly to the ADR agent (rejected: out of scope, and it removes the
onboarding baseline a brownfield project gets from domain-analyzer).

## R3 — The record ID

**Decision**: `adr-NNN-<section-slug>-<hash>`, where `NNN` is the ADR's number, `<section-slug>` the
kebab-cased target section, and `<hash>` an 8-character hash of the normalized statement (trimmed,
lowercased, whitespace-collapsed). Computed once when drafted, frozen; a reword at the gate keeps it.

**Rationale**: Matches `ts-` / `ds-` exactly, plus the ADR number, because unlike the siblings there are many
ADR files and the ID must say which one a clause came from. That makes SC-004 (trace a clause to its ADR in
one step) true from the ID alone.

**Alternatives considered**: `adr-<section-slug>-<hash>` (rejected: two ADRs proposing the same wording would
collide).

## R4 — The two command-owned sections; no template change

**Decision**: A significant ADR gets, after every template section:

1. `## Constitution guardrails` — every drafted record, in the sibling record format, whatever its decision.
2. `## Constitution input` — the check result, the goal line, then accepted records with status not
   `adopted`, grouped by target section.

Where a resolved template already contains either heading, the agent fills it there instead of appending.
The shipped `adr-template.md` is not changed. A non-significant ADR gets neither section.

**Rationale**: Principle VIII forbids repairing a template, and an override written before 1.26.0 would not
have the headings anyway, so the command must own them regardless. Two sections because
`/speckit-constitution` is told to adopt *every* guardrail in Constitution input — a declined record there
would be adopted. Adding the headings to the shipped template would put an empty governance tail in every
non-significant ADR, which is most of them.

**Alternatives considered**: One section with a declined sub-list (rejected: the handoff prompt would adopt
it). Records inline in Consequences (rejected: a template may omit Consequences).

## R5 — Goal states

**Decision**:

| Constitution | Accepted records | Goal line | Handoff |
|---|---|---|---|
| exists | ≥ 1 | `Goal: **update** the constitution at .specify/memory/constitution.md with the guardrails below.` | one amend line |
| exists | 0 | `Goal: **update** — nothing was accepted.` | none |
| missing | any | `Goal: **pending** — no constitution exists; these records are for a later amend.` | none; point to `speckit.spectra.domain-analyzer`, and say an amend can be run from this ADR once a constitution exists |

**Rationale**: Encodes Q2 = B. `pending` is a third value the siblings never needed; it is spelled out so a
later reader (a person, or a future `/speckit-constitution` run) can tell "nothing accepted" from "accepted,
waiting for a constitution".

## R6 — A `Proposed` ADR

**Decision**: The gate and handoff run regardless of status. The Constitution input section records the
ADR's status when drafted (`ADR status at drafting: Proposed`), and the handoff adds one sentence: run the
line once the decision is accepted.

**Rationale**: Step 5 always writes `Proposed`, so gating on `Accepted` would mean the handoff never runs in
the same session. The user decides when to run the line.

## R7 — The handoff line

**Decision**: Mirrors the siblings' update wording, with the resolved path:

```text
Next: run this to update your constitution from [ADR-007-split-billing-service.md](docs/adr/ADR-007-split-billing-service.md):

/speckit-constitution Amend the constitution with every guardrail in the "Constitution input" section of docs/adr/ADR-007-split-billing-service.md, adding each under its section and applying "amends:" items as amendments to the principle they name, and cite ADR-007 as the source of each change
```

The final clause asks `/speckit-constitution` to name the ADR in its Sync Impact Report, which is what makes
SC-004 hold from the constitution side too. Followed by: nothing reaches the constitution until that command
runs.

## R8 — Version, changelog, prose

**Decision**: MINOR, 1.25.0 → 1.26.0. `[1.26.0]` in `spectra/CHANGELOG.md` under **Changed**: the ADR agent
hands off instead of editing; sibling ground; methodology's table; domain-analyzer's split. `catalog.json`
version. `extension.yml`'s ADR description gains "and hands any constitution change to
/speckit-constitution". Hand-written prose: `AGENTS_LIST.md` blocks for `adr` ("flags any constitution update
the decision implies" becomes a handoff), `domain-analyzer`, `methodology`; `docs/index.html` cards for
`adr` and `domain-analyzer`. Rebuild the zip; `generate_agent_docs.py --check` must stay green (roster
unchanged).
