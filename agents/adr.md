---
id: adr
title: Architecture Decision Records (ADR)
command: speckit.spectra.adr
provider: spectra
type: add-on
phase: architecture-design
order: 20
status: available
summary: Capture a context-aware Architecture Decision Record grounded in the codebase, prior ADRs, and the constitution.
manifest: Create a new Architecture Decision Record from a short description, grounded in the codebase and constitution, and hand any constitution change to /speckit-constitution.
---

Create a context-aware Architecture Decision Record grounded in your codebase,
prior ADRs, and the project constitution. It gathers project context, asks up to five clarifying
questions, and writes the ADR under `docs/adr/` — or the artifact root your constitution declares. When the
decision is significant, it drafts the constitution guardrails it implies, on its own ground —
architecture-level choices — and refers testing, deployment, languages and frameworks, and workflow to
the agent that owns them. You decide each guardrail; the ADR records the outcome in a Constitution input
section and hands you a ready-to-paste `/speckit-constitution` line that cites it. It never edits the
constitution.

## Arguments

a one-or-two-sentence description of the decision. If omitted, the command asks you
for one before drafting.

## Use it when

you're making a significant architecture or technology choice and want it captured
and checked against the constitution as you decide.

## Where it writes

`docs/adr/` by default, or the `Artifact root:` your constitution declares. It
checks whether `docs/` is a published site source (Pages, MkDocs, Docusaurus) and asks first if it is.

## Template

`adr-template.md`. Override it at `.specify/templates/overrides/adr-template.md` to change the
sections; the override is committed, team-wide, and survives extension updates. Each run reports which
template it used.

## Examples

```
/speckit-spectra-adr We should standardize on PostgreSQL for all primary data stores
```

## Change the shape of your ADRs

The ADR's section structure comes from `adr-template.md`, shipped with the extension. To use your own — extra
sections your governance requires, or fewer than the default — copy it into your project's override slot and
edit it there:

```bash
mkdir -p .specify/templates/overrides
cp .specify/extensions/spectra/templates/adr-template.md .specify/templates/overrides/adr-template.md
```

Commit that file. Every ADR from then on follows your structure, for everyone on the team, and **the override
survives extension updates** because it lives outside the extension's own directory. The command resolves the
template in this order and uses the first one it can read:

1. `.specify/templates/overrides/adr-template.md` — yours
2. `.specify/presets/<preset-id>/templates/adr-template.md` — an installed preset
3. `.specify/extensions/spectra/templates/adr-template.md` — the shipped default
4. `.specify/templates/adr-template.md` — a core template, if you keep one there
5. a skeleton inside the command itself — only when there is no `.specify/` at all

Every run tells you which template it used, so an override that isn't being picked up is obvious. Sections you
delete stay deleted: the command follows your template and mentions what it left out rather than adding it
back. Do **not** edit the copy under `.specify/extensions/` — extension files are replaced when the extension
updates, and your edit goes with them.

## How it works

Takes a short description of a decision and then:

1. Reads your project context — the constitution (`.specify/memory/constitution.md`), existing ADRs under
   `docs/adr/`, specs under `specs/`, and the relevant source code.
2. Asks up to 5 clarifying questions, specific to your project, before drafting anything.
3. Determines the next ADR number, drafts the ADR, and writes it to `docs/adr/ADR-NNN-<title>.md` —
   `docs/adr/` is created automatically, and numbers are zero-padded to three digits.
4. Checks the decision against your constitution and, if significant, drafts the guardrails it would
   make binding. You approve, decline, or reword each. With no constitution yet, it keeps the guardrails
   for later and points you to the domain analyzer first.
5. Suggests (does not run) the optional git commands to commit the new ADR.

## Somewhere other than docs/?

One line in `.specify/memory/constitution.md` moves every Spectra document agent at once:

```text
Artifact root: documents/
```

The command reads that line and writes to `documents/adr/` instead. It offers the line but never adds it
for you.

The published-site check looks for `mkdocs.yml`, `docusaurus.config.*`, `docs/_config.yml`,
`docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, or a Pages configuration pointing at `docs` — and
asks before defaulting there, since that would publish the ADR or add it to a generated docs build.

## Upgrading from an older version?

If the project still has a `Docs/ADR/` folder from before 1.6.0, the command reads it for context and
continues its numbering, tells you once where ADRs live now, and offers a `git mv` you can run. It never
moves or edits anything in the old folder.
