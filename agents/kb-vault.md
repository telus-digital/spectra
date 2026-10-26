---
id: kb-vault
title: KB Vault
command: speckit.spectra.kb-vault
provider: spectra
type: add-on
phase: foundation
order: 40
status: available
summary: Absorb documents you supply — ADRs, engineering methodology, UX/UI standards — and land them in the repository as Markdown, planned and approved before anything is written.
manifest: Absorb documents the user supplies — PDFs, Word files, images, or dictated knowledge — classify them, and land them as Markdown under the project's artifact root, planned and approved before anything is written. Updates an existing document rather than duplicating it, and never commits. A domain analysis, engineering methodology, test strategy, or deployment strategy is kept as a policy source in its own <kind>-source folder and referred to the agent that owns it — kb-vault never writes the documents those agents feed the constitution.
---

Get the knowledge your team already has into the repository, where
people and coding agents can both read it. Attach the documents — a PDF of architecture decisions
inherited from a previous team, a Word file describing the engineering workflow, a deck of UX/UI
standards, a diagram exported as an image — or just describe what you know. It absorbs all of it, works
out what kind of document each source is, learns how your project already keeps documentation, and
writes Markdown.

**It shows you a table before it writes anything.** Category, description, destination, create or
update — one row per document it intends to produce, with the unreadable sources, the merges, the
contradictions and the redactions named beneath it. Then it stops. This is the one Spectra document
agent that gates on approval rather than showing you the result, because it is aimed at repositories
that already have documentation, where an unwanted *update* is not trivially undone by someone who did
not notice it happened. A comment on the plan is not approval of it; any change re-presents the whole
table; an ambiguous answer writes nothing.

**It updates what you already have rather than duplicating it.** Supply a revised standards document
and it finds the one in your repository — matching on subject and category, never on title similarity,
because `standards.md` and `ux-guidelines.md` may well be the same document while `adr-005.md` and
`adr-006.md` certainly are not. It edits that file in place, at its existing path, keeping its name and
the hand-written sections your source never mentions. The match is labelled as a judgement, so a wrong
one costs you a sentence to correct and does not cost you another pass over your attachments.

**It never invents, and it never mines your codebase.** Every substantive sentence traces to something
you supplied. A template section with no source says so instead of being filled. A file it cannot read
is named and its content requested — never guessed at from the filename, because invented documentation
is indistinguishable from the real thing once committed. A diagram is transcribed only as far as it is
legible, and where the structure will not carry it says that rather than implying a picture is present.
And "document the architecture" with nothing attached gets you a request for material, not
documentation reverse-engineered from your source code.

**It joins your existing sets instead of starting new ones.** Where a supplied document is a kind
Spectra already produces — an ADR, a BRD, an impact analysis, a defect RCA — it adopts that agent's folder, numbering and template. Without that rule, a PDF of past architecture decisions
would land in a folder of its own beside the one the ADR agent maintains: two decision records, two
numbering schemes, and no rule for which is authoritative. A domain analysis, engineering methodology,
test strategy, or deployment strategy is different: those documents feed the constitution and belong to
the agent that produces them, so kb-vault never writes them. It keeps the source as a **policy source** in
its own `<kind>-source/` folder, and the plan and report name the agent to run next, which reads it as
what the document *claims*.

## Arguments

optional. Steering for the attached documents, or the knowledge itself when you have
nothing to attach. With neither an argument nor a document it asks for material and stops.

## Use it when

onboarding a repository that has knowledge living in PDFs, decks and people's
heads; folding an acquired or inherited project's documentation into the tree; or writing down a
process you have never written down.

## Your guardrails bind it

it reads your constitution before planning, honours your declared
artifact root, and where a supplied document conflicts with a stated principle it surfaces the
conflict and asks rather than writing the contradiction. It never amends the constitution to fit.

## Where it writes

`<artifact-root>/<category>/` per document, plus a rebuilt index in each
category folder it owns. New files never leave that root; an update goes where the document already
lives, which is the one deliberate departure and the reason "update, don't duplicate" works on a
project whose documentation predates Spectra. Your supplied originals stay outside the repository.

## It never commits

when the files are written it tells you they are uncommitted and hands the
review back to you.

## Examples

```
/speckit-spectra-kb-vault
/speckit-spectra-kb-vault these are our UX standards and the old architecture decisions
```

## The plan is the safety mechanism

This is the only Spectra document command that gates on approval rather than showing you the result,
and the reason is that it is aimed at repositories that **already** have documentation. An unwanted new
file is noticeable; an unwanted *update* to a document someone else wrote is not. So a comment on the
plan is not approval of it, any change re-presents the whole table, and an ambiguous answer writes
nothing. Declining costs you nothing — `git status` is unchanged.

You can move a row to a different category folder, rename it, drop it, split it, merge it, or convert a
create into an update. The one thing you cannot do is send a **new** file outside your artifact root;
ask for that and it offers the two routes that get you there properly — the `Artifact root:` declaration
line, or a `git mv` you run afterwards.

## It joins your existing sets instead of starting new ones

Where a supplied document is a kind Spectra already produces, it adopts that agent's folder, numbering
and template:

| If the source is | Folder | Template |
| --- | --- | --- |
| an architecture decision | `<artifact-root>/adr/` | `adr-template` |
| a business requirements document | `<artifact-root>/brd/` | `brd-template` |
| an impact analysis | `<artifact-root>/impact-analysis/` | `impact-analysis-template` |
| a defect root cause analysis | `<artifact-root>/defect-rca/` | `defect-rca-template` |
| a domain analysis, an engineering methodology, a test strategy, or a deployment strategy | `<artifact-root>/<kind>-source/` | `<kind>-source-template`, else `kb-document-template` |
| anything else | `<artifact-root>/<category>/` | `<category>-template`, else `kb-document-template` |

**It never writes the documents the constitution is built from.** `DOMAIN_ANALYSIS.md`,
`ENGINEERING_METHODOLOGY.md`, `TEST_STRATEGY.md`, and `DEPLOYMENT_STRATEGY.md` each belong to the agent
that produces them. A source of one of those kinds is kept as a **policy source** in its own
`<kind>-source/` folder — `domain-analysis-source/`, `engineering-methodology-source/`,
`test-strategy-source/`, `deployment-strategy-source/` — and the plan and report name the agent to run
next. That agent reads it as what the document *claims*, never as what your code does, and your original
stays in place after it runs.

## What it will not do

It never invents. Every substantive sentence traces to something you supplied; a template section with
no source says so instead of being filled; a file it cannot read is named and its content requested
rather than guessed at from the filename. It never mines your codebase for content — it reads your
project to decide *where* a document goes and *what shape* it takes, never what it says, so "document
the architecture" with nothing attached gets you a request for material. Your supplied originals stay
outside the repository; you get Markdown. And it never stages, commits, branches, pushes, tags or opens
a pull request — when the files are written it tells you they are uncommitted and hands the review back.

## Change the shape of your knowledge documents

The default structure is a shipped template. To change it for your whole team, permanently, copy it to
`.specify/templates/overrides/kb-document-template.md` and commit it — or shape a single category with
`.specify/templates/overrides/<category>-template.md`, which applies even to a category Spectra has
never heard of. Do **not** edit the installed copy under `.specify/extensions/`: the next extension
update replaces it. Every run reports which template it resolved, by full path, so an override that
failed to apply is visible rather than silent.

## How it works

1. Absorbs every supplied source in full, reporting per file whether it could read it.
2. Resolves your artifact root, then reads how your project already keeps documentation — folders,
   numbering, document shapes, templates, indexes.
3. Classifies each source into a category, from its content rather than its filename.
4. Looks for a document you already have about the same subject, and plans an **update** to it rather
   than a second file beside it.
5. Shows you a table — category, description, destination, create or update — and **stops**.
6. Writes only after you approve, and only what the approved table says.
