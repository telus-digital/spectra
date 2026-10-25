# Deployment Strategy: [PROJECT NAME]

<!--
  HOW TO USE THIS TEMPLATE
  - This document is produced by `speckit.spectra.deployment-strategy`. It states how this project gets
    from a merged change to something running or published — environments, gates, releases, schema
    changes, rollback, and operability — so every later work session inherits one answer.
  - Fill every [PLACEHOLDER]. Delete any section that genuinely does not apply — remove it entirely
    rather than leaving "N/A". The command honours what this template says: a section you delete stays
    deleted, and the command notes the omission instead of putting it back.
  - What this template CANNOT change: every claim carries its provenance (verified, claimed, stated, or
    convention); an absence names what was searched; values only the client or ops owner can supply are
    listed as open questions, not filled in; operability stays at the level of policy and ownership; a
    secret found in an input is cited, not copied; and the promotion diagram shows only what the
    environments table states. Those rules live in the command, not here.
  - The document's YAML front matter is written by the command, not by this template, and it has to
    parse. Overriding the body is supported; reshaping the header is not.
  - HTML comments like this one are guidance and are stripped from the output.
-->

## Classification and evidence

<!--
  What ships, read from evidence: one row per deployable. Then greenfield | brownfield | mixed, judged
  from deployment practice, with the signals that decided it and any that pointed the other way. A
  single-deployable project has one row and says so once.
-->

| Deployable | Root | Class | Deciding evidence |
|---|---|---|---|
| [name] | [path] | [service / static-site / library / cli-desktop / mobile / infra] | [path] |

**Mode**: [GREENFIELD / BROWNFIELD / MIXED]

**Signals pointing the other way**: [list, or "none"]

## Environments & promotion

<!--
  Applicable with an approach, or not applicable with a reason. In brownfield, today's state first,
  with provenance. For a library or CLI these rows are release channels; for mobile, store tracks.
  The diagram below draws only the rows in this table.
-->

**Applicability**: [APPLICABLE / NOT APPLICABLE — reason]

| Environment | Proves | Audience | Deploy method | Gate in | Provenance |
|---|---|---|---|---|---|
| [name] | [what it establishes] | [who uses it] | [automatic / manual / tag] | [what must be true to enter] | [verified / claimed / stated / convention] |

```mermaid
flowchart LR
  [PROMOTION FLOW]
```

**Recommendation**: [what should change, with provenance and the exact change where possible]

## Pipeline, artifact & traceability

<!--
  Pre-merge and on-merge checks and where each gates; build once and promote the same artifact;
  immutable identifiers; traceability from a running or published artifact back to its commit;
  provenance and SBOM only where warranted. Which tests exist is the test strategy's call — cite it.
-->

**Applicability**: [APPLICABLE / NOT APPLICABLE — reason]

**Today**: [current state, with provenance]

**Recommendation**: [with provenance]

## Release & versioning

<!--
  Branching model, how a release is cut, the versioning scheme, and the hotfix path.
-->

**Applicability**: [APPLICABLE / NOT APPLICABLE — reason]

**Today**: [current state, with provenance]

**Recommendation**: [with provenance]

## Data & schema change

<!--
  How migrations run and in what order relative to the application, backward compatibility, and the
  statement that an application rollback leaves the schema where it is.
-->

**Applicability**: [APPLICABLE / NOT APPLICABLE — reason]

**Today**: [current state, with provenance]

**Recommendation**: [with provenance]

## Rollback & recovery

<!--
  The application rollback path, with short commands where the platform is known. Recovery targets as
  answered or as open questions. Each recovery claim marked drilled or assumed.
-->

**Applicability**: [APPLICABLE / NOT APPLICABLE — reason]

**Today**: [current state, with provenance]

| Recovery claim | Target | Drilled or assumed | Provenance |
|---|---|---|---|
| [claim] | [target or "open question"] | [drilled — date / assumed] | [provenance] |

**Recommendation**: [with provenance]

## Operability & configuration

<!--
  Health checks and smoke tests; what should be monitored and who owns detection and alerting;
  scheduled and background workloads; how configuration and secrets reach each environment; what is
  managed as code and what is set up by hand; how drift is caught. Existing jobs and alerts are listed
  and linked, not redefined.
-->

**Applicability**: [APPLICABLE / NOT APPLICABLE — reason]

**Today**: [current state, with provenance]

| Existing job or alert | Where it is defined | Owner |
|---|---|---|
| [name] | [path] | [role or "open question"] |

**Recommendation**: [with provenance]

## Conditional lenses

<!--
  Rollout technique, multi-region or multi-tenant, compliance and audit gates, environment cost — each
  only with the evidence that warrants it. Otherwise one line saying none were warranted.
-->

[CONDITIONAL LENSES, or "None warranted by the evidence."]

## Open questions / confirmation items

<!--
  What only the client, the ops owner, or a platform team can answer. Never a guessed value.
-->

| Item | Who answers | Blocks |
|---|---|---|
| [item] | [role] | [lens or recommendation] |

## Recommendations summary

| # | Lens | Deployable | Recommendation | Provenance | Re-run mark |
|---|---|---|---|---|---|
| [n] | [lens] | [deployable or "all"] | [recommendation] | [provenance] | [new / adopted / carried] |

## Constitution input

<!--
  The section /speckit-constitution consumes. Its format is owned by the command, and this template
  cannot change it: the command writes it here, or before the sources section if an override drops it.
  It opens with the constitution check — its state, the governing clause where one exists, and any
  conflict found — then one goal line — create the constitution, or update it — then lists, grouped by target
  constitution section, exactly the guardrails the team accepted and the constitution has not yet
  adopted, each with its frozen `ds-` id, its placement (add, or amends: <principle>), and its basis
  (observed or aspirational). The full record of every drafted guardrail — statement, id, section,
  basis, decision, status — sits with its lens in the body, accepted or not. Nothing here has been
  written to the constitution; this command never writes that file.
-->

**Already in the constitution?**: [EMBEDDED / PARTIAL / ABSENT / NO CONSTITUTION]

**Governing clause today**: [quoted text, where one exists]

**Conflict found**: [where an existing principle contradicts a recommendation above, or "none"]

Goal: [**create** the constitution at `.specify/memory/constitution.md` / **update** the constitution] from the guardrails below.

### [Target constitution section]

- [Guardrail statement, as accepted]
  - id: `ds-[section-slug]-[hash]`
  - placement: [add | amends: <principle name>]
  - basis: [observed | aspirational]

**To apply it**: [the /speckit-constitution line for the goal, referencing DEPLOYMENT_STRATEGY.md — or, when nothing was accepted, one sentence saying so and no command]

## Sources consulted and coverage of analysis

<!--
  What was read out of what is present; what could not be seen and why; every input, from the
  repository and from referenced documents; the five clarification answers; the no-network and
  no-execution statements; the known limitations.
-->

**Coverage**: [n of m files opened; what was not examined]

**Inputs consulted**: [list]

**Could not read**: [list with reasons, or "none"]

| # | Question | Recommended | Answer taken | Disposition |
|---|---|---|---|---|
| [n] | [question] | [recommendation] | [answer] | [answered / default_taken / not_asked] |

**Known limitations**: [LIMITATIONS]
