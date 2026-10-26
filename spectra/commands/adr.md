---
description: "Create a new Architecture Decision Record from a short description, grounded in the codebase and constitution, and hand any constitution change to /speckit-constitution."
---

# Create an Architecture Decision Record

You are helping the user capture an **Architecture Decision Record (ADR)**. Your job is to
produce an ADR that is genuinely relevant to *this* project — not a generic template fill-in.
Work through the steps below in order. Do not skip the context-gathering or the clarifying
questions.

## User Input

The user's description of the decision to record:

$ARGUMENTS

If this is empty, ask the user for a one or two sentence description of the decision before
continuing.

## What this command never does

No argument, approval, or instruction in the session enables any of these.

| Never | Why |
|---|---|
| Write `.specify/memory/constitution.md` — in any run, approved or not | `/speckit-constitution` owns that file: its sync impact report, its version, its propagation into dependent templates |
| Invoke `/speckit-constitution` | A portable command cannot rely on one agent's way of calling another, and chaining takes the user out of their own governance change |
| Write any file other than the ADR — and, on supersession, the superseded ADR's status line | One decision, one record. Step 7 adds its sections to the ADR you wrote in Step 6 |
| Adopt a guardrail nobody chose | Skip, silence, and a non-interactive run all adopt nothing. Step 7 |

## Step 1 — Gather project context (do this BEFORE asking anything)

Read and internalize the relevant project context so your questions and the ADR itself are
specific to this codebase. Inspect, where present:

1. **Constitution** — `.specify/memory/constitution.md`. These are the governing principles.
   The ADR must be consistent with them (or explicitly acknowledge tension). Also read it for the
   **artifact root** — see the next item.
2. **The artifact root** — where this project keeps generated documents. Resolve it before you look for
   anything else, because every path below hangs off it:
   - **Declared root wins.** If the constitution contains a line reading `Artifact root: <folder>/`
     (match case-insensitively), use that folder. It MUST be project-relative — reject a value with a
     leading `/` or a `..` segment, say why, and fall back to the default.
   - **Otherwise the default is `docs/`** — but check first whether `docs/` is a **published site
     source** in this project. Signals: `mkdocs.yml`, `docusaurus.config.*`, `docs/_config.yml`,
     `docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, or a GitHub Pages configuration pointing at
     `docs` (Pages' only non-root branch source is `/docs`).
   - **If you find a signal and no declared root**, raise it with the user before writing: writing to
     `docs/adr/` would publish the ADR on their site or add it to a generated documentation build.
     Recommend `documents/` and ask which they want. This question is about *where to write*, not about
     the decision, so it does not count against the five in Step 2. If you cannot get an answer, use
     `documents/` and say so — a file in the wrong private folder is one `git mv` away, a published one
     cannot be recalled from caches or forks.
   - **Offer the declaration; never write it.** Whatever root is chosen, show the user the line that
     makes it permanent for every Spectra agent, and let them add it themselves:

     ```text
     Artifact root: documents/
     ```

     Until that line exists you will ask again on the next run. Do **not** edit
     `.specify/memory/constitution.md` for this — the only constitution input you may draft is the one
     in Step 7, about the decision itself, handed to `/speckit-constitution`.
   - From here on, `<artifact-root>/adr/` is this project's ADR folder — `docs/adr/` unless the root was
     declared or changed above.
3. **Existing ADRs** — every `*.md` file under `<artifact-root>/adr/`. Use these to:
   - understand decisions already made and the conventions/numbering in use,
   - avoid duplicating or silently contradicting a prior ADR,
   - detect if this new decision **supersedes** an existing one.

   **Also check the locations earlier runs used.** Extension versions before 1.6.0 wrote ADRs to
   `Docs/ADR/` — compare case-insensitively, since on macOS `Docs/ADR/` may already resolve to
   `docs/ADR/`. And if the root was declared as something other than `docs/`, check `docs/adr/` too.
   Read any you find, for exactly the same purposes and for the numbering in Step 3. Treat them as
   **read-only**: you never move, rename, modify, or delete anything in them.
4. **Specifications and plans** — anything under `specs/` (spec.md, plan.md, research.md,
   data-model.md, contracts/, tasks.md) relevant to the area being decided.
5. **Source code** — locate and skim the parts of the codebase the decision actually touches
   (relevant modules, configs, dependency manifests like package.json / pyproject.toml /
   go.mod, infrastructure files). Ground your understanding in what exists today.

Summarize for yourself what the decision affects and where it sits relative to existing
decisions. Do not show this raw dump to the user unless it helps frame a question.

## Step 2 — Ask clarifying questions (maximum 5)

Ask the user **up to 5** clarifying questions, and no more. Fewer is better — only ask what
you genuinely cannot determine from Step 1.

- Each question must be specific to this project and informed by the context you gathered
  (reference the actual modules, prior ADRs, or constitution principles involved).
- Skip anything the description or the codebase already answers.
- Prioritize questions that change the *substance* of the decision: alternatives considered,
  constraints, scope/boundaries, migration impact, and reversibility.
- Present the questions, then wait for the user's answers before drafting. If the user
  declines to answer some, proceed with reasonable, clearly-stated assumptions.

## Step 3 — Determine the ADR number and location

- Ensure the directory `<artifact-root>/adr/` exists at the project root; create it if it does not. With
  the default root that is `docs/adr/`. The path is **project-relative and lowercase** — not `Docs/ADR/`,
  not `/docs/adr/`.
- Scan `<artifact-root>/adr/` for existing files named `ADR-NNN-*.md` and find the highest `NNN`.
- If Step 1 found ADRs in an earlier location (`Docs/ADR/`, or `docs/adr/` when the root is declared
  elsewhere), scan those the same way and take the **highest `NNN` across every folder**, so the decision
  log keeps one continuous sequence across the move.
- The new number is that value + 1, zero-padded to **three digits** (e.g. `001`, `002`, `017`).
  If no ADRs exist anywhere, start at `001`.

## Step 4 — Resolve the ADR template

The ADR's **structure** comes from a template, not from this file. Resolve `adr-template.md` through the
project's template stack and take the **first readable, non-empty** hit:

1. `.specify/templates/overrides/adr-template.md` — the project's own override. It wins outright.
2. `.specify/presets/<preset-id>/templates/adr-template.md` — any installed preset (in registry priority
   order, if a `.specify/presets/.registry` says so).
3. `.specify/extensions/spectra/templates/adr-template.md` — the template shipped with this extension.
4. `.specify/templates/adr-template.md` — a core template, if the project keeps one there.
5. The **inline skeleton** at the end of this command — last resort only, for a project with no `.specify/`
   at all.

Rules:

- **Do not stop at the first file that exists — stop at the first one you can actually use.** If a layer's
  file is present but empty or unreadable, say so in one line and continue down the list.
- **Report which template you used**, by path, when you report the result in Step 6. An override that
  silently failed to apply looks exactly like one that worked, and the first clue would otherwise be a
  wrongly-shaped ADR.
- **Never edit a template.** They are input.

## Step 5 — Draft the ADR

Follow the resolved template's sections **exactly** — same sections, same order, same headings. Do not add,
rename, or reorder them.

Filling rules:

- **NNN** — the zero-padded number from Step 3. **Title** — short and descriptive, in title case.
- **Date** — today's date in `YYYY-MM-DD` format.
- **Status** — `Proposed` for a new ADR. Keep only the chosen value on the line (e.g. `**Status:** Proposed`)
  and delete the alternatives.
- **Context** — ground it in the real problem, referencing the relevant code, specs, and prior ADRs you
  found. Capture the user's answers from Step 2.
- **Decision** — state the concrete decision clearly and unambiguously.
- **Consequences** — be honest about both the benefits and the trade-offs.
- **Delete every guidance comment and `[PLACEHOLDER]` token.** None may survive into the finished ADR.
- **Honour the template; do not repair it.** If the resolved template omits a section this command would
  ordinarily fill — no Consequences, say — follow the template as authored and mention the omission once
  when you report. Do not reinstate it. A project's override is a decision, not a suggestion. Equally, if
  the template adds sections (Alternatives Considered, Compliance Impact, Drivers), fill them from what you
  gathered in Steps 1–2; where you genuinely have nothing, say so in the section rather than inventing
  content.
- If this decision supersedes an existing ADR, say so in Context, and after writing the new
  file, update the superseded ADR's status line to `Superseded` (referencing the new number).
  **Exception:** if the superseded ADR lives in one of the earlier locations from Step 1 (a legacy
  `Docs/ADR/`, or `docs/adr/` when the root is declared elsewhere), do not edit it there — those folders
  are read-only. Record the supersession in the new ADR's Context and tell the user which file to update
  once they move it. Either way, if the superseded decision reached the constitution, Step 7 drafts the
  matching constitution amendment.

## Step 6 — Write the file

Create the file at:

```
<artifact-root>/adr/ADR-NNN-<kebab-case-title>.md
```

which with the default root is:

```
docs/adr/ADR-NNN-<kebab-case-title>.md
```

where `<kebab-case-title>` is the title lowercased with spaces replaced by hyphens and special
characters removed (e.g. `ADR-003-adopt-postgres-for-primary-store.md`).

Show the user the path you created, the **template you used** (the path resolved in Step 4), and a short
summary of the ADR.

**If Step 1 found ADRs in an earlier location**, say so once, in one short note — and no more than once
per run:

- state where ADRs live now and that this ADR was written there,
- confirm you left the earlier folder untouched,
- offer the move as a command they can run if they want the history in one place (substitute the actual
  folders):

  ```bash
  git mv Docs/ADR/*.md docs/adr/ && rmdir Docs/ADR
  ```

Do **not** run it, and do not move the files yourself. Continuing the numbering across every folder means
nothing breaks if they never move them.

**If the template came from the shipped default** (layer 3), and only if the user seems to want a different
structure, mention once that they can copy it to `.specify/templates/overrides/adr-template.md`, edit it,
and commit — every later ADR follows their version, and the override survives extension updates. Do not
create that file yourself.

## Step 7 — Check the ADR against the constitution and hand off

Compare the decision against `.specify/memory/constitution.md` and decide whether this is a
**significant** ADR. Treat it as significant if it does any of the following:

- introduces or changes a cross-cutting standard or principle (e.g. a default tech choice,
  a security/testing/quality bar, an architectural boundary),
- contradicts, narrows, or extends an existing constitution principle,
- establishes a convention future work is expected to follow.

**If it is not significant**, say so in one line with the reason, write no Constitution section, print
no `/speckit-constitution` line, and continue to Step 8.

**If it is significant**, the recommendation must come from you — do not wait to be asked. Work through
the rest of this step.

### The constitution check

Read `.specify/memory/constitution.md` **semantically** — a section heading, plus normative keywords such
as MUST or SHOULD, plus the subject matter. Never match on a string. Classify each guardrail the decision
would make binding:

| State | What you found | What you do |
|---|---|---|
| **embedded** | the constitution already states it | quote the governing clause; draft nothing |
| **partial** | a clause exists but omits or contradicts part of it | quote it, name the gap, draft `amends: <principle>` |
| **absent** | nothing normative covers it | draft it as `new` |
| **no constitution** | the file does not exist | draft it as `new`; the goal is `pending` |
| **sibling ground** | another feeder owns it | draft nothing on another feeder's ground; refer it (Sibling ground) |

**Where an existing principle contradicts the decision**, surface the contradiction as a finding in its
own right and draft the record as `amends:` that principle. Never draft a clause that silently overrides
one.

**When Step 5 recorded a supersession**, find the principle the superseded ADR introduced — by the
`adr-NNN-` id in its Constitution input section, or by a citation of that ADR in the constitution — and
draft the new record as `amends: <that principle>`. The constitution keeps only its latest sync impact
report and an ADR written before 1.26.0 has no Constitution input section, so this lookup can come up
empty; then draft against the principle the check matched, or as `new`. A reversed decision must never
leave two contradictory clauses behind.

### Sibling ground

Five agents feed the constitution, and each clause has one source. **Your ground** is
architecture-level choices — datastores, messaging and eventing infrastructure, architecture style (for
example monolith, modular monolith, services), service and data boundaries and ownership, layering, and
integration patterns — plus architectural decisions on security, data handling, or reliability (for
example mTLS between services, a data-retention mechanism, an observability stack), and conventions future
work must follow that no sibling owns. Ground shared with domain-analyzer is governed clause by clause.

Everything else belongs to a sibling. Draft nothing on another feeder's ground:

| Ground | Owner | Document you check |
|---|---|---|
| Test levels, coverage floor, the ratchet, UAT | `speckit.spectra.test-strategy` | `<artifact-root>/TEST_STRATEGY.md` |
| Environments, promotion, rollback, the versioning scheme, the release cut, hotfix promotion | `speckit.spectra.deployment-strategy` | `<artifact-root>/DEPLOYMENT_STRATEGY.md` |
| Languages, frameworks, runtimes, dependency policy; bounded contexts, invariants, glossary terms | `speckit.spectra.domain-analyzer` | `<artifact-root>/DOMAIN_ANALYSIS.md` |
| Methodology overlays, work modes, branching, review gates, change records | `speckit.spectra.methodology` | `<artifact-root>/ENGINEERING_METHODOLOGY.md` |

- **For each part of the decision on a sibling's ground**, name the owner, say whether its document exists
  at the artifact root, and suggest the user re-run it — every one of them reads ADRs as evidence, so the
  decision will be weighed in its own handoff. Record the referral in the `Constitution check:` line.
- **Where that document exists**, read only records whose `decision` is `accepted` (in a checkbox-era file,
  its `- [x]` items), and name any one this decision contradicts. A `declined`, `skipped`, or `not_asked`
  record never constrains you.
- **A decision naming a language, framework, or dependency rule is domain-analyzer's**, even when it is
  recorded as an ADR. A mixed decision — "adopt event sourcing on Kafka, written in Kotlin" — drafts only
  the architecture-level part and refers the rest.
- **Ground shared with domain-analyzer** — every lens of its analysis except Technology & dependency policy
  — is governed clause by clause: check the constitution and `DOMAIN_ANALYSIS.md`'s accepted records, cite
  a clause that already covers the decision, and draft `amends:` where the decision changes one. Whichever
  agent drafts a clause first is its source; domain-analyzer cites your accepted records in turn.
- **Prior ADRs** — when you read other ADRs' Constitution input sections (for supersession, or to see what
  is already decided), a `Superseded` or `Deprecated` ADR's records count only as the principle a
  supersession amends, never as a constraint.

### The draft

Draft each guardrail in the constitution's voice — declarative and testable, MUST or SHOULD, with a brief
rationale — so it needs minimal rewriting downstream. **Each drafted guardrail is a record:**

```markdown
- **<Guardrail statement — declarative and testable, MUST/SHOULD, with a brief rationale>**
  - id: `adr-NNN-<section-slug>-<hash>`
  - section: <Target constitution section>
  - basis: observed | aspirational
  - decision: accepted | declined | skipped | not_asked
  - status: new | amends: <Principle name/number> | adopted: <Principle name/number>
```

Keys appear in exactly that order. The statement is the user's wording where they changed it.

- **The ID is `adr-NNN-<section-slug>-<hash>`**: `NNN` is this ADR's number from Step 3, `<section-slug>`
  the kebab-cased target section, and `<hash>` a short (8-char) hash of the normalized statement (trimmed,
  lowercased, whitespace-collapsed). It is computed once, when first drafted, and frozen: a reword at the
  gate keeps the ID. The number is what lets anyone trace a constitution clause back to this decision.
- **`section`** uses the project constitution's own section names; Spec Kit's defaults where none exists.
- **`basis`** is `observed` where the codebase already holds the rule, `aspirational` where it does not.
- **`status`** is `adopted: …` where the constitution already carries the guardrail in substance.

### The gate

**Show every drafted record first**, with its statement, section, and basis. Then ask once. This question
does not count against the five clarifying questions of Step 2.

- **Approve it** — every shown record is `accepted`, except those the reply names: a record **named to
  decline** is `declined`; a record **named to reword** is `accepted` with the new statement and **the
  same id**.
- **Revise the ADR first** — edit the ADR you wrote in Step 6 in place, re-draft the records, and offer
  this same gate again.
- **Talk it through** — nothing is decided until one of the others is chosen.
- **Decline the whole gate** — every record is `skipped`.
- **No answer, or a non-interactive run** — every record is `not_asked`. Silence adopts nothing.

### The sections

Add two sections to the ADR you wrote in Step 6 — in this run, and to no other file:

1. `## Constitution guardrails` — every drafted record, accepted or not, so the ADR records what was
   offered as well as what was chosen.
2. `## Constitution input` — the section `/speckit-constitution` consumes. It holds exactly the records
   whose `decision` is `accepted` and whose status is not `adopted: …` — nothing else.

Fill them where the resolved template places either heading; otherwise append them after the template's
last section, in that order, and say so once when you report. The format is this command's, and a template
cannot change it. Open Constitution input with the check, the ADR's status, and the goal, then group the
records by target section:

```markdown
## Constitution input

Constitution check: <one line per state found — governing clauses quoted, contradictions and referrals named>
ADR status at drafting: Proposed
Goal: **update** the constitution at .specify/memory/constitution.md with the guardrails below.

### <Target constitution section>

- <Guardrail statement, as accepted>
  - id: `adr-NNN-<section-slug>-<hash>`
  - placement: add | amends: <Principle name/number>
  - basis: observed | aspirational
```

The goal line is exactly one of:

- `Goal: **update** the constitution at .specify/memory/constitution.md with the guardrails below.` — a
  constitution exists and at least one record was accepted.
- `Goal: **update** — nothing was accepted.` — a constitution exists and nothing was accepted. The section
  says so in that one sentence and lists nothing.
- `Goal: **pending** — no constitution exists; these records are for a later amend.` — there is no
  constitution. The accepted records are listed all the same.

### The invariant

> **You never write `.specify/memory/constitution.md`.** Not on approval. Not when the file is missing.
> Not when the user insists.

Approval authorises records in the ADR you were already writing, and nothing else. `/speckit-constitution`
owns the sync impact report, the MAJOR / MINOR / PATCH judgement, the version and amendment-date lines, and
propagating the change into dependent templates and docs. If the user asks you to apply the change
yourself, decline, say why, and give the line again.

### The handoff

When a constitution exists and at least one record was accepted, tell the user to run
`/speckit-constitution` referencing this ADR. **Do not invoke it.** Give the ADR as a link to the path you
actually wrote — resolved root, not the default — and the command as one ready-to-paste line:

```text
Next: run this to update your constitution from [ADR-007-split-billing-service.md](docs/adr/ADR-007-split-billing-service.md):

/speckit-constitution Amend the constitution with every guardrail in the "Constitution input" section of docs/adr/ADR-007-split-billing-service.md, adding each under its section and applying "amends:" items as amendments to the principle they name, and cite ADR-007 as the source of each change
```

Substitute this ADR's path and number. The closing clause — cite ADR-NNN as the source of each change —
stays in every line: it is what makes the constitution's own change record point back at this decision.

State plainly that **nothing reaches the constitution until that command runs**. If the ADR's status is
`Proposed`, add that they should run it once the decision is accepted. If nothing was accepted, say so and
give no command: a prompt that adopts nothing invites a run that can only re-touch the constitution.

**When there is no constitution**, give no command — one decision is no foundation for a whole
constitution. Point the user to the foundation agents, `speckit.spectra.domain-analyzer` first, and say
that once a constitution exists, the accepted records can be amended in from this ADR.

## Step 8 — Suggest committing the ADR (optional, do not run automatically)

Do **not** run git commands yourself. Instead, present them as an optional suggestion the user
can copy. Tailor the message and the file list to what you actually changed — the ADR, plus the
superseded ADR when Step 5 updated its status line — and use the real artifact root:

```bash
git add docs/adr/ADR-NNN-<kebab-case-title>.md
git commit -m "docs(adr): ADR-NNN <title>"
```

A constitution change is committed after `/speckit-constitution` runs, as its own change. Make clear
this step is optional and the user can adjust the branch, message, or scope as they prefer.

---

## Inline template skeleton (last resort for Step 4)

Use this **only** when no layer in Step 4 yielded a readable template — a project with no `.specify/`
directory at all. Its sections are identical to the shipped `adr-template.md`; fill it per Step 5 and delete
these guidance notes in the output.

```markdown
# ADR-NNN: [Title]

**Date:** YYYY-MM-DD

**Status:** Proposed | Accepted | Deprecated | Superseded

## Context

What is the issue or problem that motivates this decision?

## Decision

What is the change that we're proposing and/or doing?

## Consequences

What becomes easier or harder as a result of this decision?
```
