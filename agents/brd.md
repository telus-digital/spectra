---
id: brd
title: BRD Generator
command: speckit.spectra.brd
provider: spectra
type: add-on
phase: requirements-discovery
order: 20
status: available
summary: Turn a raw business requirement, typed or in a document, into a structured, specify-ready BRD.
manifest: Transform a raw business requirement (inline text or a .docx/.pdf/.md/.txt document) into a structured, specify-ready BRD under docs/brd/ (or the project's declared artifact root), asking clarifying questions when needed, then hand off to the specify command.
---

Turn a raw business requirement into a structured, **specify-ready** BRD. It
accepts the requirement as inline text or a document (`.docx`, `.pdf`, `.md`, `.txt`), reads project
context (the shipped template, constitution, existing BRDs under `docs/brd/`, prior specs) to ground it,
asks up to five clarifying questions only when the requirement has material gaps, and writes one
`NNN-<title>.md` under `docs/brd/` — never inventing requirements (genuine unknowns become Open
Questions). It then tells you to run the specify command with the BRD; its only write is the BRD file.

## Arguments

the business requirement as text, or a path to a requirement document. When both are
given, the document is primary and the text is guidance. With no input, it asks for a requirement or
a path.

## Use it when

you have a rough business need (in your head or in a `.docx`/`.pdf`) and want a
structured, reviewable BRD to feed into `specify`, instead of pasting a loose paragraph straight in.

## Where it writes

`docs/brd/` by default. Declare `Artifact root: documents/` in the constitution to
move it, and every Spectra document agent follows. Because `docs/` is GitHub Pages' only non-root branch
source and the default source directory for MkDocs and Docusaurus, the command checks for that setup and
asks before writing a BRD somewhere it would be published.

## Template

`brd-template.md`, the 14-section structure. Override it at
`.specify/templates/overrides/brd-template.md` to add or drop sections; the override is committed, team-wide,
and survives extension updates. Each run reports which template it used.

## Examples

```
/speckit-spectra-brd Support agents need to merge duplicate customer tickets while preserving history
/speckit-spectra-brd reqs/ticket-merge-brief.docx
```

## How it works

1. Reads the requirement — inline text, or a `.docx`/`.pdf`/`.md`/`.txt` document whose text it
   extracts. Unreadable or image-only files are reported, not fabricated.
2. Reads project context — the shipped BRD template, the constitution, existing BRDs under `docs/brd/`,
   and prior specs — to ground and deconflict, without adding scope the requirement didn't state.
3. Writes one BRD to `docs/brd/NNN-<title>.md` (folder created automatically, numbered zero-padded to
   three digits, never overwriting), following the canonical template — genuine unknowns become Open
   Questions and adopted defaults become Assumptions.
4. Reports the path and tells you to run the Spec Kit **specify** command with the BRD.

Its only write is the BRD file; it never edits your spec, constitution, or source, and never invokes
`specify` itself.

## Publishing and upgrading

`Artifact root: documents/` in `.specify/memory/constitution.md` sends BRDs to `documents/brd/` instead
of `docs/brd/`. The command checks whether `docs/` is a published site source before defaulting there
and asks first if it is; a BRD carries stakeholders, revenue targets, and competitive rationale, so
publishing one by accident is the mistake worth one question. Unanswered, it picks the non-publishing
folder.

Upgrading from an older version? A `brds/` folder from before 1.6.0 is read for context and numbering,
so the next BRD continues the sequence; the command says once where BRDs live now and offers a
`git mv`. Nothing in the old folder is moved or modified.

## Change the shape of your BRDs

Same mechanism as the ADR agent, with `brd-template.md`:

```bash
mkdir -p .specify/templates/overrides
cp .specify/extensions/spectra/templates/brd-template.md .specify/templates/overrides/brd-template.md
```

Commit it, and every BRD follows your structure — the 14 shipped sections are a default, not a fixed contract.
Resolution order, the reported template path, and the survives-updates guarantee are identical to the ADR
agent's, described [above](#change-the-shape-of-your-adrs).

One caveat worth knowing: **Section 6 — User Journeys** is what the Spec Kit `specify` command leans on most
heavily. Dropping it is allowed, and the command will say it did so, but expect the resulting spec to have
thinner user stories.
