# Spectra (`spectra`)

The Spectra extension for [Spec Kit](https://github.com/github/spec-kit) — a single self-contained
extension that bundles Spectra's agentic SDLC commands. Every command lives under the unified
`speckit.spectra.*` namespace and installs together in one step.

## Commands

<!-- SPECTRA:GENERATED START id=spectra-readme-commands -->
<!-- Generated from agents/ — do not edit by hand. Run: python3 tools/generate_agent_docs.py -->

| Command | What it does |
| ------- | ------------ |
| `speckit.spectra.domain-analyzer` | Infer the project's business domain from its code and docs, have an SME decide candidate guardrails lens by lens, and hand the result to the constitution. |
| `speckit.spectra.methodology` | Find, choose, and record the team's engineering methodology — spec-driven by default, with test-first or behaviour-first as binding phase obligations — and hand it to the constitution. |
| `speckit.spectra.kb-vault` | Absorb documents you supply — ADRs, engineering methodology, UX/UI standards — and land them in the repository as Markdown, planned and approved before anything is written. |
| `speckit.spectra.test-strategy` | Decide how this project tests itself — and what coverage floor it can actually hold — before the first feature is planned. |
| `speckit.spectra.brd` | Turn a raw business requirement, typed or in a document, into a structured, specify-ready BRD. |
| `speckit.spectra.impact` | Find out what a proposed feature would actually touch, with cited evidence, before anyone commits to building it. |
| `speckit.spectra.test-plan` | Turn a specification into a test plan stakeholders can approve — traceable conditions, stated exclusions, and a real exit bar — before the implementation is designed. |
| `speckit.spectra.adr` | Capture a context-aware Architecture Decision Record grounded in the codebase, prior ADRs, and the constitution. |
| `speckit.spectra.uat` | Run the user-acceptance scenarios from your test plan on explicit request — perform what the agent can drive, save the evidence, and tick only what it saw pass. |
| `speckit.spectra.flaky-test-detector` | Find the tests that pass and fail on the same code, then fix the ones you approve, one at a time. |
| `speckit.spectra.defect-rca` | Take a defect from a ticket, an issue, or a description down to its root cause — with evidence read from the code, not asked for. |
| `speckit.spectra.create-pr` | Open a correctly-targeted GitHub PR for the current spec branch and return its URL. |
| `speckit.spectra.review-pr` | Review a GitHub pull request against the spec, plan, tasks, ADRs, and constitution it carries, then publish a single human-curated review containing only the findings the reviewer selected. |
| `speckit.spectra.deployment-strategy` | Decide how this project gets from a merged change to something running or published — environments, gates, releases, rollback, and who owns what — grounded in what it already does. |
<!-- SPECTRA:GENERATED END id=spectra-readme-commands -->

## Install

You need a project already initialized with `specify init`; the commands register for whatever AI
agent that project uses. After installing, **restart your agent** so it picks up the new commands.

From the catalog (see the [repo root README](../README.md) for catalog setup):

```bash
specify extension add spectra
```

Or install a working copy directly:

```bash
specify extension add --dev ./spectra
```

To update later, add `--force` to overwrite your existing copy — e.g.
`specify extension add --dev ./spectra --force`.

## A note for mixed-agent teams

Commands are named `speckit.spectra.<command>` in the manifest, and Spec Kit rewrites each into your
agent's native format at install time — so the **trigger you type differs by agent**:

- **Claude** registers them as *skills*, invoked with a leading slash and dashes: `/speckit-spectra-adr`.
- **Other agents** (e.g. kiro-cli) keep the dots: `/speckit.spectra.adr`.

It's the same extension and the same source files across all of them. After install,
`specify extension info spectra` (or your agent's command/skill list) shows the exact triggers. If a
command doesn't show up, restart your agent so it re-scans its command/skill directory.

---

## Starting on an existing codebase

On a brownfield project, five SPECTRA agents lay the foundation the constitution is built from. Run them
in this order, and run the constitution after each one:

1. `/speckit-spectra-kb-vault` *(optional)* — import knowledge kept outside the repository: wiki pages,
   exported documents, design notes. Policy sources land in their own `<kind>-source/` folder for the
   owning agent to read, never in that agent's document.
2. `/speckit-spectra-domain-analyzer`, then `/speckit-constitution` — **create** the constitution.
3. `/speckit-spectra-methodology`, then `/speckit-constitution` — **amend** it.
4. `/speckit-spectra-test-strategy`, then `/speckit-constitution` — **amend** it.
5. `/speckit-spectra-deployment-strategy`, then `/speckit-constitution` — **amend** it.

**Why the constitution runs after each agent.** Each agent ends by handing you its own ready-to-paste
`/speckit-constitution` line, built from the guardrails you accepted in its round. Running it before the
next agent means that agent finds a ratified constitution: each later agent detects the constitution,
switches its goal to update, and proposes only what it does not already say — so no rule gets two
sources, and nothing you already ratified is offered to you again. An imported document is read as what
someone *claimed*, never as current practice: only the code and history decide that, and only your
answers adopt a guardrail.

**Declare the artifact root in the first constitution run.** Add a line such as `Artifact root: docs/` to
the constitution when you create it — or `Artifact root: documents/` where `docs/` is published by GitHub
Pages, MkDocs, or Docusaurus. Every later agent reads it, and stops asking where its document should go.

On a greenfield project, skip the import and start with the domain analyzer; the order is otherwise the
same. With an agent other than Claude, type the dotted form of each command, such as
`/speckit.spectra.domain-analyzer`.

<!-- SPECTRA:GENERATED START id=spectra-readme-agents -->
<!-- Generated from agents/ — do not edit by hand. Run: python3 tools/generate_agent_docs.py -->

## `speckit.spectra.domain-analyzer` — Domain Analyzer

Say whether the project has a constitution, so whether this run
creates or updates one, then scan the codebase, docs, and ADRs to infer the business domain and work
six lenses, handing workflow to the Methodology Analyst. It asks you to decide each lens's candidate guardrails in the session, with at least four
options per question, one recommended and one Skip. Only then does it write `docs/DOMAIN_ANALYSIS.md` —
or your declared artifact root — with a Constitution input section of what you accepted, and hand you a
ready-to-paste `/speckit-constitution` prompt. Documents imported by kb-vault are read as what they
*claim*, never as what the code does, and a guardrail you already accepted in an ADR is cited rather than
drafted twice. It never edits the constitution or source, and adopts nothing you did not choose.

- **Arguments** — none required. Optionally pass a focus or a domain hint to steer the analysis.
- **Use it when** — bootstrapping constitution guardrails for a brownfield project (no args — it infers
  the domain from what's already there), or when you already know the domain and want to anchor the
  analysis to it.
- **Examples (Claude)** —
  ```
  /speckit-spectra-domain-analyzer
  /speckit-spectra-domain-analyzer this is a banking system
  ```

### How it works

It is built for an existing codebase that has never had a constitution, and it works with one that has.

1. Says first whether it found `.specify/memory/constitution.md`, and so whether this run's goal is to
   **create** the constitution or **update** it.
2. Reads your project — constitution, docs and specs, source code and dependency manifests, and any
   prior analysis — and infers your business domain from the evidence.
3. Works six lenses: domain and business rules, data sensitivity and regulation, security and trust
   boundaries, architecture and boundaries, technology and dependency policy, and reliability and
   operability. Each candidate guardrail cites a file and says whether the code already follows it
   (`observed`) or not (`aspirational`). Testing, deployment, and workflow policy are left to
   `test-strategy`, `deployment-strategy`, and `methodology`.
4. Asks you seven questions, one at a time: the domain, then one per lens. Each has at least four
   options, one recommended and one **Skip**, and free text always works.
5. Only after the last answer, writes `docs/DOMAIN_ANALYSIS.md` — or `DOMAIN_ANALYSIS.md` at your
   declared artifact root — recording every candidate and decision, plus the **Constitution input**
   section holding exactly what you accepted. It is shaped by `domain-analysis-template` (override at
   `.specify/templates/overrides/domain-analysis-template.md`).
6. Ends with a link to the file and a ready-to-paste `/speckit-constitution` prompt that creates or
   amends the constitution from that section.

Skip, an unanswered question, and `--non-interactive` all adopt nothing.

### Re-running and upgrading

Re-running offers your previous answers as each question's proposed answer, so it confirms rather than
asks again. A guardrail you reworded keeps its ID, and one you declined is not offered back to you as
new. An accepted guardrail the constitution now carries is marked `status: adopted` and leaves the
Constitution input section, so a second `/speckit-constitution` run does not adopt it twice.

From an earlier version:

- An analysis left at `.specify/memory/domain-analysis.md` is read on the next run, so your decisions
  carry over; the command reports it and leaves it for you to remove.
- A checkbox file is read as your prior decisions: ticked means accepted, and unticked items are asked
  about again, since an unticked box cannot say whether anyone looked at it.
- Delivery and workflow decisions are kept as a record, handed on to `methodology`, and leave the
  Constitution input section.

---

## `speckit.spectra.methodology` — Methodology Analyst

Say whether the project is brownfield or greenfield and whether this
run creates or updates the constitution, then read the history, workflow configuration, and sibling
documents and work nine lenses: methodology stack, work modes, requirements intake, spec lifecycle,
branching, review gates, change records, AI collaboration, and governance. Spec-driven development is
the base; test-first, behaviour-first, domain-first, contract-first, and ADR-driven overlays are offered
with their evidence and enter the constitution only as obligations bound to a spec-kit phase. It asks
you ten questions one at a time, then writes an onboarding-grade `docs/ENGINEERING_METHODOLOGY.md` — or
your declared artifact root — with a Constitution input section, and hands you a ready-to-paste
`/speckit-constitution` prompt. Documents imported by kb-vault are read as what they *claim*, never as
what the history shows. It never edits the constitution and adopts nothing you did not choose.

- **Arguments** — none required. Optionally pass a focus hint, or `--non-interactive` to write the
  document without asking anything (and adopt nothing).
- **Use it when** — bringing an existing codebase onto Spectra and writing down how the team really works,
  or agreeing a methodology for a new project — including whether test-first is binding.
- **Examples (Claude)** —
  ```
  /speckit-spectra-methodology
  /speckit-spectra-methodology we are weighing TDD for new code
  ```

### How it works

1. Says first whether the project is **brownfield** or **greenfield** — from three signals: source
   beyond scaffolding, workflow configuration, and more than 10 commits — and whether this run's goal
   is to **create** the constitution or **update** it. With exactly one signal it asks you to settle
   the reading.
2. Reads `git log` and `git branch -a`, PR and issue templates, `CODEOWNERS`, CI workflows, commit and
   changelog configuration, `CONTRIBUTING.md`, `specs/`, the constitution, and the sibling documents —
   accepted entries only.
3. Works nine lenses: methodology stack, work modes and classification, requirements intake, spec
   lifecycle and traceability, branching and integration, review and merge gates, change records, AI
   collaboration rules, and governance and evolution. In brownfield mode each reports current practice
   with citations before proposing; in greenfield mode each offers defaults.
4. Treats spec-driven development as the base, and offers TDD, BDD/ATDD, DDD, contract-first, and
   ADR-driven as overlays, each with its evidence. An adopted overlay becomes obligations bound to
   specify, plan, tasks, or implement — TDD's implement obligation is checked in `tasks.md` — with a
   strictness (MUST or SHOULD) and a scope you choose.
5. Asks you ten questions, one at a time. Each has at least four options, one recommended and one
   **Skip**, and free text always works.
6. Only after the last answer, writes `docs/ENGINEERING_METHODOLOGY.md` — or `ENGINEERING_METHODOLOGY.md`
   at your declared artifact root — with a mode-choice table, branch-naming and commit-prefix references,
   the obligations matrix, and a **Constitution input** section holding exactly what you accepted. It is
   shaped by `engineering-methodology-template` (override at
   `.specify/templates/overrides/engineering-methodology-template.md`).
7. Ends with a ready-to-paste `/speckit-constitution` prompt, then lists the other constitution-feeding
   agents you have not run yet.

It never edits the constitution, never runs another spec-kit phase, and never proposes in a sibling's
ground: test levels and coverage stay with `test-strategy`, environments and versioning with
`deployment-strategy`, product technology and domain content with `domain-analyzer`. A hand-written
methodology already at the path is read as evidence and replaced only with your consent.

### Re-running and upgrading

Re-running offers your previous answers as each question's proposed answer, keeps every guardrail's ID,
and does not offer a declined one back to you as new. Delivery and workflow decisions made in an earlier
domain analysis are read as prior answers.

---

## `speckit.spectra.kb-vault` — KB Vault

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

- **Arguments** — optional. Steering for the attached documents, or the knowledge itself when you have
  nothing to attach. With neither an argument nor a document it asks for material and stops.
- **Use it when** — onboarding a repository that has knowledge living in PDFs, decks and people's
  heads; folding an acquired or inherited project's documentation into the tree; or writing down a
  process you have never written down.
- **Your guardrails bind it** — it reads your constitution before planning, honours your declared
  artifact root, and where a supplied document conflicts with a stated principle it surfaces the
  conflict and asks rather than writing the contradiction. It never amends the constitution to fit.
- **Where it writes** — `<artifact-root>/<category>/` per document, plus a rebuilt index in each
  category folder it owns. New files never leave that root; an update goes where the document already
  lives, which is the one deliberate departure and the reason "update, don't duplicate" works on a
  project whose documentation predates Spectra. Your supplied originals stay outside the repository.
- **It never commits** — when the files are written it tells you they are uncommitted and hands the
  review back to you.
- **Examples (Claude)** —
  ```
  /speckit-spectra-kb-vault
  /speckit-spectra-kb-vault these are our UX standards and the old architecture decisions
  ```

### The plan is the safety mechanism

This is the only Spectra document command that gates on approval rather than showing you the result,
and the reason is that it is aimed at repositories that **already** have documentation. An unwanted new
file is noticeable; an unwanted *update* to a document someone else wrote is not. So a comment on the
plan is not approval of it, any change re-presents the whole table, and an ambiguous answer writes
nothing. Declining costs you nothing — `git status` is unchanged.

You can move a row to a different category folder, rename it, drop it, split it, merge it, or convert a
create into an update. The one thing you cannot do is send a **new** file outside your artifact root;
ask for that and it offers the two routes that get you there properly — the `Artifact root:` declaration
line, or a `git mv` you run afterwards.

### It joins your existing sets instead of starting new ones

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

### What it will not do

It never invents. Every substantive sentence traces to something you supplied; a template section with
no source says so instead of being filled; a file it cannot read is named and its content requested
rather than guessed at from the filename. It never mines your codebase for content — it reads your
project to decide *where* a document goes and *what shape* it takes, never what it says, so "document
the architecture" with nothing attached gets you a request for material. Your supplied originals stay
outside the repository; you get Markdown. And it never stages, commits, branches, pushes, tags or opens
a pull request — when the files are written it tells you they are uncommitted and hands the review back.

### Change the shape of your knowledge documents

The default structure is a shipped template. To change it for your whole team, permanently, copy it to
`.specify/templates/overrides/kb-document-template.md` and commit it — or shape a single category with
`.specify/templates/overrides/<category>-template.md`, which applies even to a category Spectra has
never heard of. Do **not** edit the installed copy under `.specify/extensions/`: the next extension
update replaces it. Every run reports which template it resolved, by full path, so an override that
failed to apply is visible rather than silent.

### How it works

1. Absorbs every supplied source in full, reporting per file whether it could read it.
2. Resolves your artifact root, then reads how your project already keeps documentation — folders,
   numbering, document shapes, templates, indexes.
3. Classifies each source into a category, from its content rather than its filename.
4. Looks for a document you already have about the same subject, and plans an **update** to it rather
   than a second file beside it.
5. Shows you a table — category, description, destination, create or update — and **stops**.
6. Writes only after you approve, and only what the approved table says.

---

## `speckit.spectra.test-strategy` — Test Strategy

Decide how this project tests itself, once, at the start. It reads
the repository, works out for itself whether this is greenfield or brownfield, and writes one strategy to
`docs/TEST_STRATEGY.md` — or your declared artifact root — covering unit, integration, API
contract, end-to-end, UAT, and regression testing plus a coverage floor. Then it drafts the guardrails that
would hold every future work session to it, records your decision on each, and hands a Constitution input
section to `/speckit-constitution` — to create the constitution when there is none, or to update it.

Before it writes, it asks you five things — one at a time, each arriving with the answer it would have
chosen and the evidence behind it. Where the testing weight should sit, whether anything outside the
repository depends on an interface here, which journeys justify an end-to-end test, what has broken that
your tests did not catch, and what constraints the repository does not show: no container runtime in CI,
a freeze on new dependencies, a compliance rule. That last one is the gap worth closing — it already
refused to name a tool your stack cannot run, but had nothing to say about one your stack can run and
your team may not adopt. **It will not ask you anything it can measure.** Not the mode, not the stack,
not the surfaces, not your coverage figure; those it reads, because a wrong answer would outrank a right
one. And declining is free: say "use your defaults" and you get the document it would have written on its
own, for the cost of one reply. `--non-interactive` skips the round entirely.

It is deliberately hard for it to say something plausible and wrong. Every recommendation either cites a
path in your project, is marked as a convention with no project evidence, or is marked `stated` and names
the question you answered — never neither, and never an answer dressed up as evidence. **An answer never
moves a number**: ask for a 90% floor in a repository measuring 31% and the floor stays at 31%, with the
disagreement recorded in the document rather than argued at you. It will not name a tool your stack
cannot run, so the end-to-end lens resolves to browser, HTTP, CLI, or **none** rather than reaching for a
browser driver; for a published library, `none` is the correct answer and it says so. When it claims
something is missing, it tells you what it searched for and where.

Brownfield is where most of the care went. It reads your source rather than your README, reports what each
lens covers today before proposing anything, and **never proposes a floor above your current baseline** —
a floor that fails the next build gets deleted, and a deleted floor is worth less than none. Coverage
figures carry their provenance: `measured` only if it ran your tool this session after asking permission,
`reported` with the report's date if it read a committed file, `unavailable` if there is nothing to read.
Where the floor sits below the target, the ratchet is written as triggers you can check from the
repository, not as dates it has no way to know.

The last two lenses are policy rather than levels. **UAT** states whether acceptance testing applies,
who may perform it — a human, or an AI agent only on explicit request — and what counts as evidence on
each surface this project actually has: a screenshot for a browser, a transcript for a CLI or an HTTP
call. **Regression** names the suite that must stay green, cites where it runs or says it runs nowhere
automatically, and records whether a fixed defect earns a regression test. Both are marked applicable or
not, with the reason, and both are recorded in the document's front matter — the lens set and which level
owns what — so `test-plan` can read them rather than guess. The drafted guardrails gain one that keeps
UAT out of the implement command's hands.

Two things it will not do. **It never writes your constitution** — not on approval, not on a re-run, not
if you insist. It drafts each guardrail under a frozen `ts-` ID, records whether you accepted, declined,
or skipped it, and tells you the command that applies the accepted ones, because one command should own
constitution edits and the sync impact report that goes with them. A document imported by kb-vault is
read as what it *claims*, never as current practice. And **it never applies configuration**: the exact CI or coverage change
is written out for you to make.

Unlike the other document agents, it produces a **singleton** — one file at a fixed path, rewritten in
place on a re-run, with Git carrying the history. A standing policy has exactly one current answer, and
anything that links to it should not break every time you refresh it.

- **Arguments** — none required. Optionally pass a focus to weight the analysis; it never narrows the six
  mandatory lenses.
- **Use it when** — setting up a new project before the first feature, or landing Spectra on an
  established codebase and wanting a testing baseline that starts from what is already there.
- **Examples (Claude)** —
  ```
  /speckit-spectra-test-strategy
  /speckit-spectra-test-strategy focus on the API contract boundary with the payments service
  ```

### How it works

1. Reads your project — constitution, specs, docs, dependency manifests, test and coverage
   configuration, CI definitions, and, in a brownfield repository, the source itself.
2. **Classifies the project greenfield, brownfield, or mixed from evidence**, never by asking you, and
   reports the signals that decided it — including any that pointed the other way.
3. Identifies the **testable surfaces**, so a monorepo does not get one answer for three stacks.
4. Asks you its five questions, one at a time.
5. Works six lenses — unit, integration, API contract, end-to-end, UAT, regression — each either
   applicable with a named approach or not applicable with a stated reason.
6. Derives a **coverage floor** from the baseline it could establish, with a ratchet toward the target.
7. Writes one document to `docs/TEST_STRATEGY.md`, or `TEST_STRATEGY.md` at your declared artifact root.
8. Checks whether the strategy is already in your constitution — or whether there is one at all —
   drafts the guardrails it would make binding, records your decision on each, and hands a
   Constitution input section to `/speckit-constitution`.

It runs nothing without your explicit confirmation — not even your coverage tool.

### Re-running and upgrading

On a re-run it marks what the constitution has since adopted, never offers a declined guardrail again
as new, and reads a strategy from before 1.25.0 without losing a ticked decision.

### Change the shape of the strategy

The document's twelve sections are overridable at
`.specify/templates/overrides/test-strategy-template.md`.

---

## `speckit.spectra.brd` — BRD Generator

Turn a raw business requirement into a structured, **specify-ready** BRD. It
accepts the requirement as inline text or a document (`.docx`, `.pdf`, `.md`, `.txt`), reads project
context (the shipped template, constitution, existing BRDs under `docs/brd/`, prior specs) to ground it,
asks up to five clarifying questions only when the requirement has material gaps, and writes one
`NNN-<title>.md` under `docs/brd/` — never inventing requirements (genuine unknowns become Open
Questions). It then tells you to run the specify command with the BRD; its only write is the BRD file.

- **Arguments** — the business requirement as text, or a path to a requirement document. When both are
  given, the document is primary and the text is guidance. With no input, it asks for a requirement or
  a path.
- **Use it when** — you have a rough business need (in your head or in a `.docx`/`.pdf`) and want a
  structured, reviewable BRD to feed into `specify`, instead of pasting a loose paragraph straight in.
- **Where it writes** — `docs/brd/` by default. Declare `Artifact root: documents/` in the constitution to
  move it, and every Spectra document agent follows. Because `docs/` is GitHub Pages' only non-root branch
  source and the default source directory for MkDocs and Docusaurus, the command checks for that setup and
  asks before writing a BRD somewhere it would be published.
- **Template** — `brd-template.md`, the 14-section structure. Override it at
  `.specify/templates/overrides/brd-template.md` to add or drop sections; the override is committed, team-wide,
  and survives extension updates. Each run reports which template it used.
- **Examples (Claude)** —
  ```
  /speckit-spectra-brd Support agents need to merge duplicate customer tickets while preserving history
  /speckit-spectra-brd reqs/ticket-merge-brief.docx
  ```

### How it works

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

### Publishing and upgrading

`Artifact root: documents/` in `.specify/memory/constitution.md` sends BRDs to `documents/brd/` instead
of `docs/brd/`. The command checks whether `docs/` is a published site source before defaulting there
and asks first if it is; a BRD carries stakeholders, revenue targets, and competitive rationale, so
publishing one by accident is the mistake worth one question. Unanswered, it picks the non-publishing
folder.

Upgrading from an older version? A `brds/` folder from before 1.6.0 is read for context and numbering,
so the next BRD continues the sequence; the command says once where BRDs live now and offers a
`git mv`. Nothing in the old folder is moved or modified.

### Change the shape of your BRDs

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

---

## `speckit.spectra.impact` — Impact Analyzer

Find out what a proposed feature would actually touch, **before** anyone
commits to building it. A Business Analyst gives it one paragraph — what should be true after this ships
that is not true today — and it reads the project, works out the blast radius, asks at most five questions
about the things code cannot answer, and writes one numbered document to take to stakeholders for a go /
no-go decision. It runs before `specify`, because the point is to inform the decision that authorizes the
spend.

The reason to use it instead of an hour of interviews is **evidence**. A BA cannot read an entire
repository, so conventional impact analysis is a memory exercise that systematically misses coupling —
the config file naming a column, the handler registered by string key, the service that reads a table
nobody remembers. Every finding it reports carries a `path/to/file.ts:142` citation and one of three
confidence levels, and every run states how much of the repository it actually read.

What it refuses to do is as important as what it does:

- **It never says there is no impact.** "No consumers found in what was scanned" is allowed; "no downstream
  impact" is not. The limit of a search is never reported as a property of the system.
- **The impact rating is a lookup, not an opinion** — derived from a defined trigger set (irreversible data
  change, external contract change, no rollback path, and so on) and reported with the trigger that fired,
  so two runs on the same change agree.
- **It never reproduces a secret.** Where a line it would cite holds a token or a credential, it gives the
  location and the kind and says the value was withheld.
- **It routes rather than judges.** Touching auth or personal data flags the finding and names the security
  or compliance agent that owns the question; it renders no compliance verdict of its own. Things a
  repository simply cannot know — stakeholders, training, support model, vendor cost — come back as
  explicit follow-up items rather than plausible filler.

- **Arguments** — the feature intent as one paragraph (required), plus optional document paths
  (`.md`, `.txt`, `.pdf`, `.docx`) for a brief, an epic, or a prior analysis. `--non-interactive` for CI.
  Five cap overrides — `--seed-cap`, `--hops`, `--max-files`, `--identifier-cap`, `--per-system-cap` —
  when the defaults are too tight for a large repository.
- **Use it when** — a feature has been proposed and someone has to decide whether to fund it, and the
  honest answer to "what else does this touch?" is currently a guess.
- **More than one repository?** It asks. Other systems are declared as a sentence, as a document, or as a
  **path to a local copy** it reads in place. It accepts no repository URL and makes **no network request
  at all** — not even for a public repo with `gh` authenticated. A system with no local checkout is
  recorded as described, and still produces a handoff item naming the owning team and the exact contract to
  confirm with them.
- **Where it writes** — `docs/impact-analysis/` by default, as `NNN-<name>.md` plus an auto-maintained
  index. Declare `Artifact root: documents/` in the constitution to move it, and every Spectra document
  agent follows. Since `docs/` is GitHub Pages' only non-root branch source and the default for MkDocs and
  Docusaurus, it checks for that setup first and asks before writing an analysis somewhere it would be
  published — this document names internal systems, owning teams, and unmitigated risks.
- **Approval is yours, and manual.** Every run writes `status: draft`. You take it to your stakeholders and
  record their answer in the front matter yourself; the command never sets any other status. The index is
  rebuilt from the documents on each run, so an approval you record by hand shows up there without the
  command editing anything.
- **Re-runs never overwrite.** Every run takes the next number and writes a new document — including a
  re-run with identical input. Each report carries its own timestamp and a verbatim record of what it was
  asked, and the one it supersedes is linked rather than replaced.
- **Template** — `impact-analysis-template.md`, a ten-section structure. Override it at
  `.specify/templates/overrides/impact-analysis-template.md` to reshape or drop sections; the override is
  committed, team-wide, and survives extension updates. Each run reports which template it used. The
  citation rule, the confidence levels, the rating triggers, and the coverage statement stay with the
  command — a template shapes the document, not the standards.
- **What it does not do** — It does not design the solution, estimate in story points, write requirements, create or link a
  spec, or touch `specs/`. An impact analysis and a specification are independent; feed one into the other
  by hand if you want to.
- **Examples (Claude)** —
  ```
  /speckit-spectra-impact We want to email customers who leave items in their cart for more than 24 hours
  /speckit-spectra-impact Add a nickname field to accounts reqs/nickname-brief.docx
  /speckit-spectra-impact --non-interactive Retire the v1 pricing endpoint
  ```

### Change the shape of your impact analyses

Same mechanism as the ADR and BRD agents, with `impact-analysis-template.md`:

```bash
mkdir -p .specify/templates/overrides
cp .specify/extensions/spectra/templates/impact-analysis-template.md \
   .specify/templates/overrides/impact-analysis-template.md
```

Commit it, and every analysis follows your structure — the ten shipped sections are a default, not a fixed
contract. Delete a section, including a whole lens, and the command notes the omission rather than putting it
back. Resolution order, the reported template path, and the survives-updates guarantee are identical to the
ADR agent's, described [above](#change-the-shape-of-your-adrs).

What an override **cannot** change is the part that makes the document usable at a gate: citations, confidence
levels, the rating and its trigger, the coverage statement, the no-absence-of-impact phrasing, and the refusal
to reproduce a secret. Those live in the command. Drop *Sources consulted* and the section goes — the command
still tells you what it read and what it could not reach.

### How it works

1. Reads the project — the constitution, existing specs, source, ADRs, API contracts, migrations, tests,
   CI. Where specs and a constitution exist it orients on them and reads code to confirm and extend them;
   where they do not, it reconstructs the same understanding from source and says so. Which mode it ran
   is in the output.
2. Asks, before scanning, whether this repository is the whole system.
3. Scans in five bounded phases — structural map, term expansion across naming conventions, a
   role-weighted seed search, two-hop graph expansion, and two sweeps for what static reading misses:
   dynamic dispatch and string-keyed registries, then every contract identifier (tables, columns,
   endpoints, events, topics, config keys, flags, env vars) swept as a raw string across the whole
   project.
4. Asks at most 5 clarifying questions, generated from what the scan found ambiguous, each with options
   and a recommendation grounded in a cited finding. Pressing enter accepts the recommendation and
   records the answer as unconfirmed.
5. Analyzes through five core lenses — blast radius, data, behavioural change, risk and reversibility,
   effort and sequencing — plus security/privacy and compliance lenses that fire on trigger and route to
   the agent that owns the question rather than answering it.
6. Writes one analysis plus the index, and reports coverage.

### Numbering, interruptions, and the publishing check

The next number is one greater than the highest present, not a count of the files. An interrupted run
leaves the folder untouched and consumes no number.

An impact analysis also says where secrets live, which is one more reason the `docs/` publishing check
asks first. Unanswered, it picks the non-publishing folder.

Nothing under `specs/` is written or depended on, and there is no `spec_refs` field.

---

## `speckit.spectra.test-plan` — Test Plan

Get the tests **agreed before anyone writes them**. Run it after
`specify` and it picks up the feature `specify` recorded — the same one `plan` will plan — then reads its
specification, your constitution, your test strategy, your existing suite,
and the source the feature touches, then writes one `test-plan.md` **beside the spec**: scope with real
exclusions, a risk table that is a decision rather than an inventory, traceable test conditions,
suggested UAT scenarios, a regression scope, environment and data, and an exit bar someone can make a
go/no-go call from. It runs between `specify` and `plan`, and it is built for teams who want the test set
settled before the implementation is designed.

The document has two audiences and that shapes everything. A stakeholder reads it and approves it; the
planning command reads it and designs around it. So it states intent, not progress — and it produces no
tasks, writes no test code, and tracks nothing.

What makes it worth more than an hour with a whiteboard is **traceability that runs both ways**. Every
acceptance criterion in your spec reaches a test condition, a UAT scenario, or the uncovered list with a
reason — never none of them. Every condition names what it verifies using your spec's own identifiers
(`FR-014`, `SC-003`, or the composed `US2-AC1` for an acceptance scenario), so a reviewer can check
coverage in either direction without opening the code. The run tells you the count.

What it refuses to do is as important as what it does:

- **It finds the feature exactly as `plan` does, and no other way.** `SPECIFY_FEATURE_DIRECTORY` if set,
  otherwise `.specify/feature.json` — the record `specify` writes — so the test plan and `plan.md` always
  land in the same directory. No branch-name inference, no most-recently-modified heuristic, no picker.
  It says which feature it resolved and from where before doing anything else, and records it in the
  document, because a plan built against the wrong spec reads as authoritative to whoever approves it.
  If nothing resolves, it stops and tells you how to choose a feature. It runs one read-only shell
  command to see those two environment variables, and stops if that is refused rather than guess.
- **It never invents the missing decision.** Where a requirement is too ambiguous to test, it says so and
  writes no condition for it. A plausible-looking condition would be worse than the gap, because it
  launders a guess into something a stakeholder approves — and the guess becomes a requirement nobody
  agreed to.
- **It carries no checkboxes — exit criteria included.** It is approved, not tracked. A circulated document
  with live checkboxes creates a second apparent source of truth about progress, and it will disagree with
  `tasks.md`. If a template override puts checkboxes back, they are rendered as plain statements: your
  section is kept, only the construct goes.
- **It runs nothing.** Existing coverage is established by reading test source, never by executing the
  suite or a coverage tool. A coverage claim cites the test file; an absence claim cites the search — "no
  test referencing `SignatureVerifier` found under `tests/`" is allowed, "there is no coverage for
  signature verification" is not.
- **It inherits rather than invents.** Level names come from your `TEST_STRATEGY.md` **verbatim** where you
  have one — not normalized, not mapped — so the two documents read against each other. A declared coverage
  floor is carried into the exit criteria and attributed, never adjusted. And no level or tool is assigned
  that your dependency manifests cannot support, so a command-line tool never gets handed a browser driver.
- **It honours the whole strategy, not just its lens names.** A lens the strategy ruled out is unavailable
  here: a criterion that needs it goes to the uncovered list with the remedy "re-run test-strategy". It
  follows the strategy's ownership map when choosing a level, never names a tool the strategy ruled out,
  raises the likelihood of a risk in an area the strategy says has broken before, picks the floor of the
  surface the feature actually touches, and carries each inherited rule's provenance — cited, convention,
  or stated. A strategy that predates the UAT and Regression lenses, or looks stale against the repository,
  is flagged loudly. With no strategy at all it uses the full default set and says so, recommending
  `test-strategy`. `manual` stays available for a one-off human check, distinct from a UAT scenario.
- **UAT scenarios and regression scope.** Every user story gets at least one UAT scenario, traced to its
  acceptance criteria and given an executor — `agent`, `human`, or `either`, with `agent` only where the
  surface can actually be driven. The regression scope lists the existing tests that touch the feature's
  modules and must stay green, plus the additions its risks call for.

- **Arguments** — none needed. A path to the feature directory or its `spec.md` is accepted only as a
  confirmation: if it names a different feature than the active one, the run stops and writes nothing.
  `--non-interactive` for CI.
- **Use it when** — a spec is finished, your team works test-first, and you want the test set reviewed and
  agreed before the implementation is planned. Skip it when nobody outside the implementing team needs to
  see the test set; it is an add-on. After `specify` or `clarify`, an optional hook offers it — the hook
  only asks, and the run picks up the feature `specify` recorded.
- **Where it writes** — `test-plan.md` in the active feature's directory, beside its `spec.md`. No sequence number, no
  artifact subfolder, no `Artifact root:` resolution for the output. A test plan is *about one feature*, so
  its identity is that feature's directory, exactly as `spec.md` and `plan.md` beside it carry no number.
  It reads your declared artifact root for one purpose only — finding `TEST_STRATEGY.md`.
- **Feeding it to the planner is one copy-paste.** The run ends with a ready-to-copy planning prompt that
  links the written path and asks `plan` to record a *Testing obligations* section in `plan.md` — because
  that is what `tasks` reads. P1 conditions become test tasks written before their implementation, the
  regression scope stays green, and the UAT scenarios become a final phase titled "User Acceptance (UAT) —
  not executed by the implement command". No core command is modified, so `plan` behaves exactly as it does
  today for anyone who never installs this agent.
- **Re-runs ask first.** The usual trigger is a `clarify` session changing the spec. It reads the existing
  plan, tells you what would change before you answer, and carries forward every *explicitly not covered*
  decision — or says it removed one. Declining leaves the file byte-identical. One file, rewritten in
  place; Git carries the history.
- **Priorities come from your spec.** A condition inherits the priority of the story it verifies, and only
  P1 conditions gate the exit criteria. The one override: a prohibition, safety, or data-integrity property
  is promoted to P1 whatever the story says, because a "MUST NOT" requirement rarely has a user story and
  is exactly the one whose violation is unrecoverable.
- **Template** — `test-plan-template.md`, a seven-section structure. Override it at
  `.specify/templates/overrides/test-plan-template.md` to reshape or drop sections; the override is
  committed, team-wide, and survives extension updates. Each run reports which template it used. The
  traceability invariant, the no-checkbox rule, the cited-absence rule, the priority derivation, and the
  coverage statement stay with the command — a template shapes the document, not the standards.
- **What it does not do** — It does not write tests, generate tasks, modify your spec, touch test or CI configuration, edit the
  constitution, commit, or make a network request. It writes exactly one file.
- **Examples (Claude)** —
  ```
  /speckit-spectra-test-plan
  /speckit-spectra-test-plan specs/021-signed-webhooks
  /speckit-spectra-test-plan --non-interactive
  ```

### How it works

1. Resolves the feature exactly as `plan` does and says which one it picked and from where.
2. Reads your project — the spec in full, the constitution, your test strategy, existing tests and runner
   configuration, dependency manifests, CI definitions, and the source the feature touches.
3. Resolves the lens set from your own `TEST_STRATEGY.md` where you have one.
4. Turns every acceptance criterion into a test condition or a UAT scenario — or reports it as uncovered,
   with a reason. A requirement too ambiguous to test is reported as a gap naming what is missing.
5. Derives the risk table from stated triggers and the strategy's known risk areas, and condition
   priority from your spec's own story priorities.
6. Suggests UAT scenarios and a regression scope.
7. Writes one `test-plan.md` beside the spec, reports the count — criteria covered out of criteria
   found — then prints the planning prompt that consumes it.

The final UAT phase in `tasks.md` is one a human ticks, or that `speckit.spectra.uat` performs on
request.

### Unattended runs

Pass `--non-interactive` in CI: it will create a plan that does not exist, but never rewrite one that
does.

---

## `speckit.spectra.adr` — Architecture Decision Records (ADR)

Create a context-aware Architecture Decision Record grounded in your codebase,
prior ADRs, and the project constitution. It gathers project context, asks up to five clarifying
questions, and writes the ADR under `docs/adr/` — or the artifact root your constitution declares. When the
decision is significant, it drafts the constitution guardrails it implies, on its own ground —
architecture-level choices — and refers testing, deployment, languages and frameworks, and workflow to
the agent that owns them. You decide each guardrail; the ADR records the outcome in a Constitution input
section and hands you a ready-to-paste `/speckit-constitution` line that cites it. It never edits the
constitution.

- **Arguments** — a one-or-two-sentence description of the decision. If omitted, the command asks you
  for one before drafting.
- **Use it when** — you're making a significant architecture or technology choice and want it captured
  and checked against the constitution as you decide.
- **Where it writes** — `docs/adr/` by default, or the `Artifact root:` your constitution declares. It
  checks whether `docs/` is a published site source (Pages, MkDocs, Docusaurus) and asks first if it is.
- **Template** — `adr-template.md`. Override it at `.specify/templates/overrides/adr-template.md` to change the
  sections; the override is committed, team-wide, and survives extension updates. Each run reports which
  template it used.
- **Example (Claude)** —
  ```
  /speckit-spectra-adr We should standardize on PostgreSQL for all primary data stores
  ```

### Change the shape of your ADRs

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

### How it works

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

### Somewhere other than docs/?

One line in `.specify/memory/constitution.md` moves every Spectra document agent at once:

```text
Artifact root: documents/
```

The command reads that line and writes to `documents/adr/` instead. It offers the line but never adds it
for you.

The published-site check looks for `mkdocs.yml`, `docusaurus.config.*`, `docs/_config.yml`,
`docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, or a Pages configuration pointing at `docs` — and
asks before defaulting there, since that would publish the ADR or add it to a generated docs build.

### Upgrading from an older version?

If the project still has a `Docs/ADR/` folder from before 1.6.0, the command reads it for context and
continues its numbering, tells you once where ADRs live now, and offers a `git mv` you can run. It never
moves or edits anything in the old folder.

---

## `speckit.spectra.uat` — UAT Runner

Perform a feature's user-acceptance scenarios on the real build, after
implementation, **only when you ask**. The test plan suggests the scenarios, `tasks` turns them into a
final UAT phase, and the implement command leaves that phase open. From there you choose: perform UAT
yourself and tick the tasks, or hand the feature to this command and let the agent perform the scenarios
it can drive — with screenshots, transcripts, and comparisons as evidence.

**It ticks only what it saw pass.** A tick in `tasks.md` is a claim that acceptance happened, so a
scenario is marked done only when the agent observed its outcome, and the tick carries a link to the
evidence. A `human` scenario, a failed one, and one the agent could not reach stay open with a reason. A
task a human already ticked is never touched, and a pass is never reverted.

**It starts nothing before you confirm.** It shows the exact command it would run to start the build and
waits. Decline and every scenario is reported blocked, not failed. It acts on a locally started build
unless you name an environment with `--env`, and it makes no network request beyond what the build under
test makes. `--non-interactive` starts nothing and attempts nothing.

**It changes nothing it is accepting** — not source, not tests, not configuration, not the spec, not the
test plan, not the constitution. It never edits code to make a scenario pass. Its writes are the `[UAT]`
lines in `tasks.md` it observed passing, `uat-report.md` beside the spec, and the evidence under
`specs/<feature>/uat/<run-stamp>/`, which a re-run adds to and never overwrites. A capture that might
show a secret is masked or skipped, and the report records what was withheld.

- **Arguments** — none needed: it finds the feature the way the implement command does
  (`SPECIFY_FEATURE_DIRECTORY`, then `.specify/feature.json`) and names it before anything starts — no
  branch name, no picker. A path to the feature directory or its `spec.md` only confirms it, and a
  mismatch stops. `--env <name>` to act on a named environment. `--non-interactive` for CI.
- **Use it when** — implementation is done and you want acceptance evidence before opening a pull
  request. After implement, an optional hook offers it ahead of `create-pr`, and another offers it after
  converge; the hooks only ask.
- **Drivability is judged in its own session.** It states which tools it relied on; a scenario marked
  `agent` that this session cannot reach becomes *awaiting human* rather than a guess.
- **Template** — `uat-report-template.md`. Override it at
  `.specify/templates/overrides/uat-report-template.md`. The report carries no checkboxes — `tasks.md` is
  the tracker — and keeps a cumulative run log.
- **Examples (Claude)** —
  ```
  /speckit-spectra-uat
  /speckit-spectra-uat --env staging
  /speckit-spectra-uat specs/021-signed-webhooks
  ```

### How it works

1. Finds the feature the way the implement command does, and names it before anything starts and again
   in the run confirmation. Where no feature resolves, it stops and says how to set one.
2. Reads the UAT phase in `tasks.md`, the scenarios in `test-plan.md`, the strategy's evidence rule, and
   the constitution.
3. Reports incomplete implementation and asks before going on, then shows the exact command it would run
   to start the build and waits for your confirmation.
4. Performs only the `agent` and `either` scenarios it can drive with the tools available in its own
   session.
5. Captures evidence — screenshots, transcripts, comparisons — under
   `specs/<feature>/uat/<YYYYMMDD-HHMMSS>/`, never overwriting an earlier run.
6. Ticks only the UAT tasks it observed pass, appending a link to the evidence, and writes
   `uat-report.md` beside the spec.

### Other environments

`--env` takes a name or a URL: pass `--env <name-or-url>` to act on an environment other than a local
build.

---

## `speckit.spectra.flaky-test-detector` — Flaky Test Detector

Find the tests that pass and fail on the same code, then fix
the ones you approve. The usual way to catch a flaky test is to instrument CI, collect hundreds of runs,
and compute a score — pipeline work, a results store, and weeks of waiting before the first answer. This
agent needs none of that, because the causes are sitting in the source: an unconditional sleep before an
assertion, an un-awaited async call, state one test leaves behind for another, a live network call, an
unseeded random value, an assertion against the real clock. It reads your test suite and names them, on
the day you install it.

**It never runs anything** — not the suite, not a build, not an install, and not to check that a fix
worked. That last exclusion is the deliberate one: an agent that can run the tests it just edited is an
agent that can iterate until green, and iterating until green is how tests get quietly weakened.
Verification stays with you and your CI.

**A fix removes the cause.** Deleting an assertion, loosening one until it always passes, skipping the
test, marking it expected-to-fail, adding a retry, or lengthening a sleep are all forbidden as remedies —
they make the symptom disappear and leave you worse off, because now the suite lies quietly. Edits stay
inside test and test-support files; where the genuine remedy belongs in application code, the item is
left open with a note saying what would need to change and where.

**Two gates, with your review in between.** The run reports a ranked table — test, file, confidence, and
a specific fix — and stops. On your go-ahead it writes `.specify/memory/flaky-test-analysis.md`: a run
summary, one `[ ]` row per candidate, the evidence behind each, and an honest account of what it could
not examine. You delete the rows you disagree with. On a second go-ahead it works what is left, one item
at a time, ticking each `[x]` on disk as it lands — so an interrupted session leaves a file that is
exactly true rather than one that claims nothing happened. Nothing is ever committed; the working-tree
diff is your review surface.

**The list outlives the session**, which is the point of writing it down. Every run reads that file first
and branches on what it finds: unfinished work resumes without re-analysing and without discarding your
pruning, a completed list asks before it is replaced, and a file it cannot parse is never overwritten
silently. There is exactly one analysis file at any time.

- **Arguments** — optional. With none, it analyses the whole working tree; give it a path or a suite name
  to narrow the run. Before a narrowed run replaces a broader plan, it names the pending items that would
  be dropped and waits for an answer.
- **Use it when** — your suite has become something people re-run rather than trust, and you want a short
  reviewable list of what to fix rather than a dashboard telling you it is bad.
- **Confidence** — High, Medium, or Low, rating the strength of the evidence rather than a failure rate.
  With no run history there is no denominator, so it emits no percentage, score, or flakiness index.
- **Your guardrails bind it** — it reads your project's own constitution, and where a rule forbids the
  only available remedy, the item is left open naming that rule instead of producing a fix your review
  would reject.
- **Where it writes** — `.specify/memory/flaky-test-analysis.md`, and test code you approved row by row.
  Never production source, never governance, never a commit.
- **Examples (Claude)** —
  ```
  /speckit-spectra-flaky-test-detector
  /speckit-spectra-flaky-test-detector api/
  ```

### The list is meant to outlive the session

There is exactly **one** analysis file, at `.specify/memory/flaky-test-analysis.md`, at any time. Close
your terminal mid-run and the file is still exactly true — progress is written after every single fix, not
batched at the end — so the next run picks up the remaining items without re-analysing and without
discarding the pruning you did. A completed list is never replaced without asking. A file it cannot parse
is never overwritten silently; it says what it could not read and waits. And before a run scoped to one
suite replaces a plan covering more, it names the pending items that would be dropped.

The file is yours to edit. Delete rows to exclude those tests, reword a suggested fix and it acts on your
wording, tick an item yourself and it skips it. Only structural damage — a missing `## Tasks` heading,
rows it cannot resolve — counts as unreadable.

### Confidence, and what it is not

High, Medium, or Low, rating **the strength of the evidence in your source**, not a measured failure rate.
High requires the triggering construct in the test's own body or its direct fixtures, citable by line.
With no run history there is no denominator, so the command emits no percentage, score, or flakiness
index — inventing one would be the easiest way to sound authoritative and be wrong.

Your project's constitution binds the fix it chooses. If a guardrail rules out the only available remedy —
no mocking libraries, no new test dependencies — the item is left open with that rule named, rather than
producing a change your own review would reject.

### How it works

It is the only Spectra agent that edits code you wrote.

1. Reads `.specify/memory/flaky-test-analysis.md` first, before anything else, and branches on what it
   finds.
2. Identifies your test suites from the working tree — runner configuration, test scripts in the project
   manifest, directory conventions, filename patterns — and reports each with its framework and file
   count before naming a single candidate. Several suites in several languages are fine.
3. Reads the tests for the eight signal categories: timing and async, isolation and shared state,
   unmocked external dependencies, non-determinism, brittle assertions, parallel-execution conflicts,
   environment coupling, and existing retry or known-flaky annotations.
4. Reports the ranked table and stops, asking before it writes anything.
5. On your go-ahead writes the plan, then stops again and tells you to delete the rows you disagree with.
6. On a second go-ahead works the surviving rows in file order, ticking each `[x]` on disk as it lands,
   and closes with what it fixed, what it left open and why, and every file it touched.

A fix may create a helper or a mock where it needs one, and it will say so — but it never touches
production source and never adds a new dependency.

---

## `speckit.spectra.defect-rca` — Defect Root Cause Analysis

Take a defect down to its root cause, with evidence read from the code
rather than asked for. Conventional root cause analysis is an interview: the analyst asks an engineer
what the code does, and the answer is a memory. This agent reads the implicated code, the commits that
touched it, the configuration and the tests, reports what it found with file-and-line citations, and
spends your attention only on the runtime facts nobody can grep for — the logs, the metrics, the
environment state, what the team knew at the time.

**It takes the defect however you have it.** A GitHub issue URL, a JIRA ticket reference, or a sentence
describing what went wrong. It says which channel it resolved to before doing anything else, so a misread
costs you one word. Where the GitHub CLI is missing or JIRA is unreachable it names the failure and its
specific remedy, asks you to paste the content, and carries on — and it never asks you for a token, a
password, or a key.

**It checks whether you have analyzed this defect before, at intake.** A recurrence surfaced after the
document is written is one surfaced too late to change anything. Matches are made on implicated code, on
symptom, or on root cause — never on title similarity — and the axis that fired is disclosed with the
concrete overlap, so a spurious match costs a sentence to dismiss. Each preventive action from the
earlier analysis gets a verdict of apparently completed, apparently not completed, or undeterminable, and
the first two require a citation. Undeterminable is the default, because an uncited "completed" against
an action nobody finished is precisely what makes a recurrence read as a fresh defect.

**It will not call the first plausible code path a root cause.** Every probe names its layer — symptom,
immediate technical cause, contributing factors, process gap, systemic cause — and where the deepest
validated finding is still an immediate technical cause, the run says so and names what would be needed
to go deeper. Reading the code creates a failure mode an interviewer does not have: the path it finds is
genuinely there and genuinely related, which makes stopping feel like finishing.

**The document records what was ruled out, not only what survived.** Invalidated and weakened hypotheses
appear in the evidence table with what settled them, because a table of nothing but confirmations is a
justification rather than an analysis. Where nothing could be validated, it says so and names the
evidence that would settle it rather than promoting a guess into the heading.

- **Arguments** — required. With none it asks what defect to analyze and stops, inferring nothing from
  your branch name, your recent commits, your open issues, or your failing tests.
- **Use it when** — a defect is worth understanding rather than just patching: a recurrence, a
  multi-cause failure, an incident that needs a written answer, or an unfamiliar codebase where tracing
  the defect by hand would take an afternoon.
- **Your guardrails bind it** — it reads your project's constitution and names which of its principles
  bear on the analysis, by heading. Those principles are often where a systemic root cause actually
  lives.
- **Where it writes** — `docs/defect-rca/NNN-<slug>.md` and a rebuilt folder index, under your declared
  artifact root if you have one. Two files, both written as the run's final act, and nothing else
  anywhere. It fixes nothing, writes no test, and never touches your ticket. The filename names the
  symptom rather than the cause, because the file is named before the analysis concludes.
- **Examples (Claude)** —
  ```
  /speckit-spectra-defect-rca https://github.com/acme/orders/issues/412
  /speckit-spectra-defect-rca orders intermittently return 500 under concurrent load
  ```

### How it works

Run it when a defect has been found — by a failing test, by QE, or in production. Hand it the defect and
it:

1. Resolves the **channel** from what you gave it — a GitHub issue URL, a JIRA ticket reference, or a
   plain description — and says which one it picked before doing anything else.
2. Reads your project: the constitution, the implicated code, the commits that touched it, the
   configuration, the tests. It says what it examined *and what it did not*.
3. Searches your **existing analyses** for this defect, and surfaces any match while the investigation
   is still open.
4. Builds a MECE hypothesis tree, tests what the repository can settle, and asks at most five questions
   per round about the things it cannot.
5. Writes one analysis to `docs/defect-rca/NNN-<slug>.md` — or wherever your declared artifact root puts
   it — plus a rebuilt folder index.

**It reads the code before it asks you anything.** Which function handles the retry, whether the timeout
is configurable, when the offending line last changed, whether a test covers that path — those are its
questions to answer, not yours. Every claim it makes about the code cites the file and line; every claim
that something is *absent* states what it searched for and where.

An evidence table of nothing but confirmations leaves a reader unable to tell what was ruled out, so they
cannot tell how much to trust what was not — which is why invalidated hypotheses stay in the document.

### The document

**The filename names the symptom, never the cause.** `order-submission-500s`, not `missing-pool-limit`.
A cause-named file is wrong exactly when the analysis turns out to be interesting — and the flat
directory stays scannable, which is what keeps the recurrence search cheap.

**Conclusions stay yours.** Beyond fixing nothing and writing no test, it changes no configuration. The
document carries an advisory status line naming a human owner, and that line is never softened or
dropped.

The document's six sections are overridable at `.specify/templates/overrides/defect-rca-template.md`.

---

## `speckit.spectra.create-pr` — Create PR

Open a correctly-targeted GitHub PR for the branch you are on, optionally
linked to an issue, with the body built from an overridable PR template. It asks once with everything on the
table before creating anything, and returns the PR URL. Also offered automatically by an `after_implement`
hook once `implement` finishes, so you don't have to invoke it by hand.

`gh` is required at run time, and the command **gates on it before doing anything else**: if `gh` is
missing or unauthenticated it stops immediately — before reading the constitution, before deriving a base
branch, before touching the remote — and names which of the two failed, because the remedies differ
(install the CLI, or `gh auth login`). Nothing is mutated on that path, and a missing `gh` never produces
a `gh` command you cannot run. A remote that isn't on GitHub stops the same way, with a scope statement.
Failures *after* the gate degrade instead: you get the manual `git push` + `gh pr create` commands with
the derived base branch filled in, plus an explicit statement of whether the branch already reached the
remote.

**Works from any branch** — a `fix/…` or chore branch is fine; only a detached HEAD and a branch that is
already the base are refused. A spec branch simply contributes more to the body (`spec.md`, `plan.md`,
`tasks.md`), while the **Changes** section always comes from the real diff against the base.

**Uncommitted work is offered a commit, not a warning.** A dirty tree gets the file list and the question
*"should I proceed with committing and pushing first?"* — yes behaves like an ordinary commit-and-push, no
opens the PR from committed work and says what was excluded. Credential-shaped filenames are called out
before anything is staged, and `--no-verify` is never used.

- **Arguments** — all optional:
  - *(none)* — open a **ready-for-review** PR (the default).
  - `--issue <url-or-number>` — the issue this PR addresses. Omit it and you are asked once; skipping the
    question writes no issue section at all.
  - `--draft` — open the PR as a **draft** instead.
  - `--base <branch>` — use this base branch (still shown in the final summary).
- **Use it when** — a piece of work is ready for review and you want the PR opened against the right base,
  shaped like your team's template, without running `git`/`gh` by hand.
- **Template** — `pr-template.md`: Summary, Related Issues, Type of Change, Changes, How to Test, Evidence,
  Breaking Changes, Notes for Reviewers — and deliberately **no self-certification checklist**. Override it
  at `.specify/templates/overrides/pr-template.md`; the override is committed, team-wide, and survives
  extension updates. Trimming **Related Issues** does not unlink the PR: an issue you passed is appended with
  a note rather than dropped.
- **Linked issues** — GitHub honours closing keywords **only** on PRs targeting the default branch, so the
  command writes `Closes #42` there and a plain `#42` reference anywhere else, telling you that merging will
  not auto-close it. Cross-repository issues are referenced by full URL.
- **Base branch** — a promotion flow documented in the constitution or the `git` extension config is used
  and cited. With nothing documented the command *proposes* a base and asks at the final gate, so you can
  answer "no, use dev" without restarting.
- **Examples (Claude)** —
  ```
  /speckit-spectra-create-pr
  /speckit-spectra-create-pr --draft
  /speckit-spectra-create-pr --base develop
  ```

### One thing to know about linked issues

GitHub interprets closing keywords **only when a PR targets the repository's default branch**. On any other
base they are ignored: no link is created and merging closes nothing. So the command writes `Closes #42`
only when the base *is* the default branch. Targeting a `dev` in a promotion flow, it writes a plain `#42`
reference instead — which still records a cross-reference on the issue — and tells you auto-close will not
happen on this merge. An issue in another repository is referenced by full URL, never with a keyword.

### Change the shape of your PRs

The body's structure comes from `pr-template.md`. Override it exactly like the ADR and BRD templates:

```bash
mkdir -p .specify/templates/overrides
cp .specify/extensions/spectra/templates/pr-template.md .specify/templates/overrides/pr-template.md
```

Commit it, and every PR the command opens follows your structure — resolution order, the reported template
path, and the survives-updates guarantee are identical to the ADR agent's, described
[above](#change-the-shape-of-your-adrs). Sections you delete stay deleted.

The shipped template has **no self-certification checklist** on purpose: an agent cannot honestly tick "I
have self-reviewed the full diff". If your override adds one, the command leaves those boxes unchecked and
tells you it left them for you.

One thing the template does *not* control: whether the PR is linked to the issue you passed. Trim the
**Related Issues** section and the command appends a short one rather than dropping the link — saying that it
did. Keep the section if you would rather choose where it sits.

**GitHub only** in this version (via the `gh` CLI), and `gh` is required at run time rather than
optional: without it the command stops with the remedy instead of half-running. Failures *after* that
gate — a protected base branch, a token without push permission, a fork restriction — degrade to the
manual `git push` + `gh pr create` commands (including the base branch it derived) plus an explicit
statement of whether the branch already reached the remote.

### How it works

When you accept the hook's offer (or run it directly) it:

1. **Gates on `gh` first**, stopping before anything else if it is missing or unauthenticated.
2. Confirms the remote is on GitHub. A missing remote, or one on another host, stops with a scope
   statement rather than a `gh` fallback that could not work.
3. Checks the branch, refusing only a detached HEAD and a branch that is already the base.
4. Detects an **existing open PR** and returns its link instead of opening a duplicate.
5. Determines the **base branch**. A promotion flow documented in the constitution's *Version Control &
   Branching Strategy* section or `.specify/extensions/git/git-config.yml` is used and cited. With nothing
   documented it proposes one — the branch yours appears to be cut from, else the repository default.
6. **Offers to commit and push** when the working tree is dirty. Clean tree, unpushed commits — it asks
   to push.
7. **Asks for a linked issue** if you did not pass `--issue`, and accepts a skip.
8. **Resolves the PR template**, fills it from the real diff, and reports which template it used.
9. **Asks once, with everything on the table**: source → base and where the base came from, the issue or
   nothing, draft or ready, the template path, and anything it has already done. Nothing is created
   before you say yes.
10. Opens the PR with `gh` and returns the URL.

Its mutations are the Git and remote actions needed to open the PR — including a commit **when you ask for
one** — and nothing else: never your source, spec, plan, tasks, or constitution.

---

## `speckit.spectra.review-pr` — Review PR

Review a GitHub pull request against **the intent and standards it
carries**, not just the diff. It reads the PR's spec, plan, tasks, and ADRs *at the PR's own head
revision*, plus the constitution and ADRs in force on the **base** branch, then reports findings that a
diff-only reviewer cannot produce: a task marked complete but absent from the change, scope no
requirement authorized, a pattern an ADR forbids. Every finding cites a file, a line, and the clause,
requirement, or principle it rests on — anything that cannot be anchored and sourced is not reported at
all.

Then the reviewer takes over, starting from a deliberately narrow default. **Only blockers and majors are
proposed** — minors, nits and questions are shown to you, enumerated by number, but are not in the
proposal. Answering `yes` publishes exactly those and submits the verdict that follows from them; `all`
takes everything, and any selection of your own still works. You see the exact text before anything is
posted. One review event goes to the pull request under your own `gh` credentials, containing only what
you accepted — and the published body declares that it was AI-assisted and human-curated.

The default is a proposal, never an assumption: an empty or absent answer posts nothing, which is a
normal outcome rather than a failure. That is the whole point of the narrow default — a short, correct,
human-endorsed review beats thirty findings that bury the two that matter, and a blank prompt in front of
sixteen findings is answered `all` far more often than it is answered carefully.

Like `create-pr`, this command **hard-stops** when `gh` is missing or unauthenticated, naming which of
the two failed — neither command can deliver its product without reading GitHub through `gh`. What
differs is what each hands over after that gate: `create-pr` gives you the `git`/`gh` commands to finish
by hand, this one gives you the rendered review body to post yourself. It is deliberately **on demand
only** — there is no hook — since a reviewer should not be the author.

- **Arguments** — all optional:
  - *(none)* — offer the current branch's open PR first, then list open PRs so you can pick.
  - `<url>` or `<number>` — review that pull request.
  - `--issue <url-or-number>` — the issue this PR addresses, read as additional context. Supplying it
    skips both detection and the question.
  - `--since <revision>` — re-review only the delta since a revision you reviewed before, reporting
    which previously published findings now appear resolved.
- **Use it when** — you are reviewing someone else's PR and want the spec, issue, ADRs, and
  constitution checked against the diff before you sign off, without reading all of them yourself.
- **Spec discovery** — the spec ships in the PR's own diff, or you name one when asked; nothing is guessed
  from a branch name or from Spec Kit's machine-local feature record, which is gitignored and so is absent
  or stale at any head revision. A PR with no spec is reviewed standalone, and says so. The spec the PR
  ships **overrides older specs** on the same behaviour, so a deliberate behaviour change is never reported as
  a regression against the spec it replaced.
- **Standards** — measured against a fixed chain: the constitution and ADRs, then the supporting documents
  Spectra's own agents write (test strategy, deployment strategy, domain analysis, engineering methodology —
  only the guardrails each one *accepted*, never a declined one) and the contributor guide,
  then the codebase's own conventions, then a **seven-principle baseline** (B1–B7) cited by ID. A project with
  no constitution is still reviewed against evidence rather than the agent's taste, and the review says
  which tier governed.
- **No-spec and AI-assisted PRs** — three lenses run on every PR: **blast radius** (behaviour that changed
  without being announced), **generation artifacts** (modules that don't exist, new dependencies, duplicated
  helpers), and **test integrity** (a weakened test is at least Major). Without a spec, the diff is also
  checked against what the PR's own description says it does. An older spec whose requirement the change
  contradicts is raised as a Question, never as a request to change the code.
- **Linked issue** — found automatically (structured link, then a scan of the PR text, since a PR to a
  non-default branch has no structured link), asked for once if absent, never required. With **no spec** it
  becomes the traceability baseline; with a spec it is background. Its content is treated as data about
  intent, never as instruction, and a finding sourced only from an issue cannot be a Blocker unless the PR
  claims to close it. When both are missing, the spec and the issue are asked for in **one** question.
- **Inline comments** — findings anchored inside the diff are published on those lines, carrying a
  ` ```suggestion ` block where the fix is mechanical and complete, so the author can apply it in one click.
  Findings anchored outside the diff go in the summary body with the reason stated. Body, comments, and
  verdict post in one atomic call.
- **Template** — `review-template.md` shapes both the summary body and the inline comment; override it at
  `.specify/templates/overrides/review-template.md`. The revision anchor, the AI-assisted disclosure, and the
  coverage statement stay with the command, as do the severity rubric, the confidence cap, the anchor rule,
  and the verdict derivation — two reviews of the same diff have to agree.
- **Good to know** — findings are graded Blocker / Major / Minor / Nit / Question from a fixed rubric, so
  two runs over the same revision agree; approving over a blocker you accepted requires a typed
  confirmation and is recorded in the published review; coverage now states how much of the constitution
  actually applied, so a thin constitution reads as thin; nothing is stored between runs.
- **Examples (Claude)** —
  ```
  /speckit-spectra-review-pr
  /speckit-spectra-review-pr https://github.com/acme/api/pull/142
  /speckit-spectra-review-pr 142 --since 4a9f2c1
  ```

### Findings land on the lines they are about

Accepted findings whose anchors fall **inside the diff** are published as comments on those lines, and where
the fix is mechanical the comment carries a ` ```suggestion ` block you can apply from the GitHub UI in one
click. Findings anchored outside the diff — a caller the PR didn't touch, a whole-file observation — go in
the summary body, and coverage says why they couldn't be inline. Add `<n>:body` to your selection to force
any finding into the body.

Because a suggestion is one click from a commit, they are offered narrowly: only for a mechanical, complete
fix covering exactly the commented lines, never for architectural or multi-file changes, never on a
low-confidence finding, and never in a generated file. **Every suggestion appears verbatim in the preview
you approve** — nothing that can be applied without being read is summarized.

Body, comments, and verdict post in one atomic call, so a failure can't leave the comments on the PR
without the verdict.

With `--since`, prior findings are recovered by reading the earlier review off the pull request itself,
since nothing is stored locally.

### Change the shape of your reviews

The findings presentation comes from `review-template.md` — the summary body *and* the inline comment shape.
Override it exactly like the other templates:

```bash
mkdir -p .specify/templates/overrides
cp .specify/extensions/spectra/templates/review-template.md .specify/templates/overrides/review-template.md
```

Three things are **not** the template's to change, and survive any override: the
`<!-- spectra:review-pr revision=… -->` anchor that `--since` and self-review detection depend on, the
AI-assisted disclosure line, and the **Coverage and limits** section — the one that stops a review implying
assurance it didn't earn.

Judgment isn't overridable either. The severity rubric and its floors, the confidence cap, the anchor rule,
the selection grammar, and how the verdict is derived stay in the command, because two reviews of the same
diff have to agree. The template governs how findings *read*, not what counts as a Blocker.

Deliberately **on demand only** — there is no hook, because a reviewer should not be the author.
**GitHub only** in this version (via the `gh` CLI), and single-body reviews only; line-anchored inline
comments are a follow-on. Failures *after* the `gh` gate — a fork restriction, insufficient permission —
degrade to handing you the rendered review body for manual posting.

### How it works

It covers the last fully manual gate in the lifecycle: where `create-pr` opens a pull request, this
reviews one. It:

1. **Gates on `gh` first**, stopping before any analysis.
2. Resolves the target — a URL, a number, or a pick from the repository's open PRs — and **pins the
   review to one head revision**, reported everywhere and re-checked before publishing.
3. Reads the PR's spec, plan, tasks, and ADRs at that revision, and the constitution and ADRs in force on
   the base branch. The revision split is deliberate: it is what lets the agent notice a PR that changes
   the rules it is being measured against.
4. Locates the governing spec as described under Spec discovery. Spec Kit's machine-local feature record
   is `.specify/feature.json`, which is why it is never used to guess.
5. Reads the **linked issue as optional extra context**. Where the issue and the spec disagree, that is a
   Question naming both.
6. Runs **traceability in both directions** (work claimed complete but absent; changes no task
   authorized), **guardrails** with the violated clause quoted, and **craft** lenses chosen from what the
   diff actually touches — reporting which lenses did not run, and why. Among the generation artifacts, a
   new dependency is always raised.
7. Grades every finding from the fixed rubric, with a separate confidence axis that caps severity: a
   low-confidence finding becomes a Question rather than a Blocker.
8. Presents the findings numbered and ranked, with a severity tally, its own reading of the change, a
   recommended verdict, and a mandatory **coverage-and-limits** statement.
9. Hands control back from the narrow default, shows you the exact review — body *and* every inline
   comment — and only then posts a single review event.

Its only mutation is publishing that one review, after an explicit go-ahead. It never edits source, the
spec, the plan, the tasks, or the constitution, never touches your working tree, and holds no credentials
of its own.

---

## `speckit.spectra.deployment-strategy` — Deployment Strategist

Decide how this project gets from a merged change to
something running or published. It reads the repository — CI workflows, container and orchestration
files, infrastructure code, migrations, specs, ADRs, and any test strategy or domain analysis already
written — plus any local document you point it at, such as a client's hosting standard or an ops runbook.
Then it writes one strategy to `docs/DEPLOYMENT_STRATEGY.md`, or your declared artifact root, drafts the
strategy's lasting rules as guardrails, records your decision on each, and hands a Constitution input
section to `/speckit-constitution` — to create the constitution or update it.

It starts by working out **what ships**, from evidence rather than by asking: a running service, a static
site, a library, a CLI or desktop tool, a mobile app, or infrastructure on its own. That classification
changes what every lens means. For a library, "deploy" means publish, environments are release channels,
and rollback is yank-or-supersede; for a mobile app, store review is a gate your team does not control. It
will not recommend a cluster rollback to a package that has no cluster.

Six lenses, every one addressed or marked not applicable with a reason: **environments and promotion**
(with a Mermaid promotion diagram drawn only from the environments it lists), **pipeline, artifact and
traceability**, **release and versioning**, **data and schema change**, **rollback and recovery**, and
**operability and configuration**. On an established project each lens reports what happens today before
proposing anything. Every claim carries one of four provenances — `verified` from what the repository
does, `claimed` from what a document says, `stated` from an answer you gave, or `convention` — because
deployment docs drift from deployment reality faster than almost anything else, and you should be able to
tell the workflow from the wiki.

Before it writes, it asks five things the repository cannot settle, once for the whole project and one at
a time, each with a recommendation and the evidence behind it: where it is hosted, who approves a
production deploy, whether a pre-release environment exists or is wanted, availability and recovery
targets, and release cadence. Say "use your defaults" and it takes every recommendation. It **never
invents a value only the client or ops owner can supply** — account IDs, cluster names, domains, who gets
paged, recovery targets nobody set. Those go in an open-questions section with the role that can answer
them. Operability stays at the level of what should be monitored and who owns it; ask in the session if
you want to go deeper.

It **never writes your constitution**. It checks whether the constitution already carries a deployment
policy, drafts only durable invariants — same artifact promoted unchanged, explicit production approval,
no floating tags, compatible migrations, a documented rollback path — and ends with a link to the file
and a ready-to-paste `/speckit-constitution` line. It never edits source, CI, manifests, or infrastructure
code, runs nothing, and makes no network request. Like the test strategy, it is a singleton, rewritten in
place on a re-run, with your previous answers offered back for confirmation.

- **Arguments** — none required. Optionally a focus, paths to local documents, and `--non-interactive`.
- **Use it when** — a project is about to ship its first release, or an established project's deployment
  practice has grown by accretion and needs writing down as one policy.
- **Examples (Claude)** —
  ```
  /speckit-spectra-deployment-strategy
  /speckit-spectra-deployment-strategy ./client/hosting-standard.md focus on the pre-release gate
  ```

### What it reads and records

Besides the CI, container, orchestration, infrastructure and migration files, it reads your constitution,
specs, ADRs, docs, and release configuration, and any `TEST_STRATEGY.md` or `DOMAIN_ANALYSIS.md` already
written.

A `convention` claim is a default with nothing behind it. Each guardrail it drafts is recorded under a
frozen `ds-` ID along with your decision on it.

The document's twelve sections are overridable at
`.specify/templates/overrides/deployment-strategy-template.md`.
<!-- SPECTRA:GENERATED END id=spectra-readme-agents -->

## License, trademarks, and disclaimer

Apache License 2.0 — see the [`LICENSE`](./LICENSE) and [`NOTICE`](./NOTICE) files shipped with this
extension. Attribution is a licence condition: keep the copyright notice, the `LICENSE`, and the
`NOTICE` file with any derivative work, and state which files you changed.

Trademarks are not licensed. "TELUS", "TELUS Digital", "Spectra", and the TELUS Digital logo are
excluded from the grant; forks must rebrand. See [`TRADEMARK.md`](./TRADEMARK.md).

Spectra agents produce drafts for human review. Output is not legal, regulatory, medical,
financial, or compliance advice and does not constitute certification or audit. Compliance agents
are readiness-support tooling only — running them does not make a system compliant, and Spectra is
not certified by or affiliated with any standards body or regulator.
