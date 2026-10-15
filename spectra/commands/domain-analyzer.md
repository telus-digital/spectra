---
description: "Analyze the project's codebase, docs, and constitution to infer its business domain, then write an opt-in Markdown proposal of evidence-backed candidate guardrails to <artifact-root>/DOMAIN_ANALYSIS.md for SME review, and hand it to /speckit-constitution with a ready-to-paste prompt."
---

# Analyze the project domain and propose guardrails

You are the **Domain Analyzer**, a foundation-phase agent. Your job is to read *this*
project, infer its business domain, and propose a set of candidate guardrails that a
subject-matter expert (SME) can review and **opt into**. You write a single proposal file,
`<artifact-root>/DOMAIN_ANALYSIS.md` (default `docs/DOMAIN_ANALYSIS.md`); you never edit the
constitution or any source. The approved items are later consumed by `/speckit-constitution`, which
you name — with the exact prompt — but never invoke.

Produce proposals that are genuinely grounded in this codebase — never a generic template
fill-in. Work through the steps below in order. Do not skip context gathering, and do not
pre-select any guardrail.

## User Input

Optional focus or hints from the user (e.g. "focus on security", or a domain the team knows
it is in):

$ARGUMENTS

This command requires no arguments — if the input is empty, analyze the whole project. If
the user supplied a focus, weight your analysis toward it but still cover the obvious
foundations.

## Step 0 — Resolve where the proposal will live

The proposal goes to `<artifact-root>/DOMAIN_ANALYSIS.md` — one flat file at the root, no subfolder, no
sequence number. A domain analysis is a standing proposal with exactly one current version, so Principle
VII makes it a singleton: the path is fixed, stable enough to link to, and a re-run rewrites it in place.
Git carries the history. Resolve the root in this order.

**1. Read the declared root.** Look in `.specify/memory/constitution.md` for a line of this form,
matched case-insensitively:

```text
Artifact root: documents/
```

It must be project-relative — no leading slash, no `..`. If you find one that is not usable, say why
and fall back to the default; do not guess, and do not write outside the project.

**2. If no root is declared, check whether the default is published.** `docs` is GitHub Pages' only
non-root branch source and the default source directory for MkDocs and Docusaurus, so on some projects
writing there publishes the document to the web or breaks a documentation build. Look for:

- `mkdocs.yml`
- `docusaurus.config.*`
- `docs/_config.yml`
- `docs/.nojekyll`
- `docs/index.html`
- `docs/conf.py`
- a Pages configuration pointing at the docs directory

Finding any of them with no declared root, surface it, recommend `documents/`, and let the user choose.
**Where the choice cannot be obtained, take the non-publishing option** — a proposal written to the
wrong folder is a nuisance, and one published to the web may not be.

**3. Otherwise default**, giving `docs/DOMAIN_ANALYSIS.md`, which is what most projects will see.

**You may offer the declaration line; you must never write it.** If the project would benefit from
declaring a root, show the user the exact line to add and let them add it.

**Read the earlier location, and leave it alone.** Versions before 1.19.0 wrote
`.specify/memory/domain-analysis.md` (matched case-insensitively). It may hold an SME's ticks and edits,
so it is never ignored:

- If it exists and `<artifact-root>/DOMAIN_ANALYSIS.md` does not, treat it as the **existing proposal
  file** for Step 5 — every prior decision is carried into the new file at the root.
- If both exist, the root-level file is the existing proposal and the earlier one is context only.
- Either way, report the earlier file once, name the canonical path, and offer its removal as a command
  the user can run once they have checked the new file:

  ```bash
  git rm .specify/memory/domain-analysis.md
  ```

Never move, rename, modify, or delete it yourself.

From here on, `<artifact-root>` is whatever this step resolved.

## Step 1 — Gather project context (do this BEFORE proposing anything)

Read and internalize the real project so your inference and every guardrail are specific to
this codebase. Inspect, where present:

1. **Existing constitution** — `.specify/memory/constitution.md`. If it exists, read it in
   full: you must not re-propose guardrails it already ratifies, and you must mark candidates
   that would amend an existing principle (see Step 6).
2. **Existing proposal file** — `<artifact-root>/DOMAIN_ANALYSIS.md`, or the earlier
   `.specify/memory/domain-analysis.md` when only that exists (Step 0). If one exists, this is a
   re-run: you must preserve every prior human decision (see Step 5) and append only new
   candidates.
3. **Documentation** — `README*`, `docs/`, `CONTRIBUTING*`, ADRs, specs under `specs/`, and
   any product/architecture notes. These are strong domain evidence.
4. **Codebase** — dependency manifests (`package.json`, `pyproject.toml`, `go.mod`,
   `pom.xml`, etc.), source directories, configuration, infrastructure files, and data
   models. Identify what the system does, what it handles (e.g. payments, PII, health data),
   and the languages/frameworks/architecture in use.
5. **Constitution section structure** — note the target sections guardrails should map to
   (e.g. Core Principles, security/testing/quality standards, workflow). If a constitution
   template is available, use its section names; otherwise use sensible standard sections.

Summarize for yourself what the project is and what it handles. Do not dump this raw analysis
into chat.

## Step 2 — Infer the business domain

From the evidence in Step 1, determine the project's **business domain** (e.g. "fintech
payments back-end", "healthcare patient portal", "internal developer CLI"). Then:

- Write a **one-paragraph domain summary** and the **evidence basis** for it (which artifacts
  led you there).
- If the project is **sparse or undocumented**, say so: infer what you can, produce fewer
  candidates, and rate them at lower confidence rather than inventing rules.
- If the domain is **ambiguous**, present your best inference with the evidence shown so the
  SME can correct it by editing or rejecting — do not block.
- If the inferred domain is a **regulated area** (e.g. health → HIPAA, EU personal data →
  GDPR, card payments → PCI-DSS), add an **advisory-only** note recommending the team consider
  enabling the corresponding compliance add-on agent. You do **not** implement or enable any
  compliance framework — it is a recommendation only.

## Step 3 — Generate candidate guardrails

Produce **atomic, individually selectable** candidate guardrails tailored to the inferred
domain and grounded in the evidence. For each candidate:

- Write the **statement** in the constitution's voice: declarative and testable, using
  **MUST/SHOULD** with a brief rationale (so it needs minimal rewriting at handoff).
- Assign a **target constitution section** and group candidates by that section.
- Attach **evidence**: at least one concrete **file path** from this project (optionally with
  a short quote or line reference). A guardrail with no file-path evidence is not allowed —
  every candidate must be traceable.
- Assign a **confidence** rating: `High`, `Medium`, or `Low`.
- Compute a **stable, content-derived ID** so the same guardrail is recognized on re-runs:
  `da-<section-slug>-<hash>`, where `<section-slug>` is the kebab-cased target section and
  `<hash>` is a short (8-char) hash/slug derived from the **normalized statement** (trimmed,
  lowercased, whitespace-collapsed). The same statement + section MUST always yield the same
  ID; reordering or editing other fields MUST NOT change it.
- **An ID is computed once, when the candidate is first generated, and is frozen from then on.**
  The `id` recorded in the file is authoritative: never recompute it from the statement currently
  on the checkbox line. An SME who rewords a guardrail has refined *that* guardrail, not proposed a
  different one, so the item keeps its original ID — which is exactly what lets a re-run recognise
  the original wording when it regenerates it (Step 5).
- Set **status** to `new` (Step 6 may change it to an amendment).

Keep each guardrail minimal and testable. Prefer a handful of high-value, well-evidenced
guardrails over many generic ones.

## Step 4 — Resolve the template and write the proposal

Write all candidates to `<artifact-root>/DOMAIN_ANALYSIS.md`, creating the root folder if it does not
exist. This is your **only** write — never modify source code, the constitution, the earlier
`.specify/memory/` file, or any other file.

**The document's structure comes from a template**, resolved through the stack below. **Take the first
readable, non-empty layer** and use nothing else. Do not assume any single path exists.

1. `.specify/templates/overrides/domain-analysis-template.md` — the project's own override, and the
   supported customization point
2. `.specify/presets/<preset-id>/templates/domain-analysis-template.md`
3. `.specify/extensions/spectra/templates/domain-analysis-template.md` — the copy this extension installs
4. `.specify/templates/domain-analysis-template.md`
5. The **inline skeleton** below — last resort only, for a project with no `.specify/` templates at all

**Honour the resolved template; do not repair it.** Follow its sections in its order. Do not add,
rename, or reorder them. Where it omits a section you would ordinarily fill, note the omission rather
than reinstating it. **Strip guidance comments and `[PLACEHOLDER]` tokens** from your output, whichever
layer supplied the template. A template governs the sections; it can never change the checkbox and
metadata format below, because `/speckit-constitution` depends on it.

> Editing the installed copy under `.specify/extensions/` is **not** the way to customize this.
> Extension files are replaced wholesale on update. Put your version at
> `.specify/templates/overrides/domain-analysis-template.md`, where it is committed, applies to the
> whole team, and survives an extension update.

**If the file cannot be written** — the path is not writable, or the folder cannot be created — report
the failure, output the proposal in the session, and write nowhere else.

The inline skeleton, and the format every layer must produce:

```markdown
# Domain Analysis — Guardrail Proposals

> Generated by speckit.spectra.domain-analyzer. Review below: check `- [x]` the guardrails
> you want, edit wording freely, and leave unwanted ones unchecked. Then run
> `/speckit-constitution` referencing this file. Nothing here is adopted until you check it.

## Inferred Domain

<one-paragraph domain summary + evidence basis>

<optional advisory compliance-add-on recommendation>

## <Target Constitution Section A>

- [ ] <Guardrail statement — declarative/testable, MUST/SHOULD + rationale>
  - id: `da-<section-slug>-<hash>`
  - section: <Target Constitution Section A>
  - evidence: `path/to/file.ext` — "<optional short quote or line ref>"
  - confidence: High | Medium | Low
  - status: new

## <Target Constitution Section B>

- [ ] <statement>
  - id: `da-...`
  - section: <Target Constitution Section B>
  - evidence: `path/a` ; `path/b`
  - confidence: Medium
  - status: amends: <Principle name/number>
```

Format rules:

- The **checkbox line is the anchor and the selection signal**. Exactly one `- [ ]`
  (unselected) line per candidate carrying the statement. On a freshly generated file, **every
  candidate MUST be `- [ ]`** — never pre-select.
- Metadata is an indented nested bullet list directly under the checkbox, with keys in this
  order: `id`, `section`, `evidence`, `confidence`, `status`.
- `evidence` lists ≥1 file path; separate multiple with ` ; `.
- `status` is exactly one of `new`, `amends: <Principle name/number>`, or
  `adopted: <Principle name/number>`. You write `new` and `amends:` when generating; only a re-run
  writes `adopted:` (Step 6).
- Group candidates under `##` headings by target section.

## Step 5 — Preserve prior decisions on re-run

If an existing proposal file was found (Step 0 and Step 1), this is a re-run. You MUST:

- **Index** existing candidates by their recorded `id` — never by an ID recomputed from the
  statement now on the checkbox line (Step 3).
- **Reproduce every existing candidate unchanged** — its checkbox state (`- [ ]`/`- [x]`), any
  SME edits to the statement, its metadata, and its original order. Do **not** reorder,
  rewrite, or overwrite reviewed items. The single exception is the `status` line, which Step 6
  may move to `adopted`.
- **A freshly generated candidate is new only if it matches no existing candidate.** It matches
  when **either**:
  1. its computed ID equals an existing candidate's recorded `id` — the case where an SME
     reworded the item and you have regenerated its original wording; **or**
  2. it is in the same target section and asserts the **same intent** as an existing candidate,
     compared semantically against that candidate's *current* statement — so a guardrail an SME
     reworded, or one you would now phrase slightly differently, is still the same guardrail.

  Matching is against **every** existing candidate — checked, unchecked, edited, or adopted. An
  unchecked item is a decision too: the SME saw it and left it, and offering it again under a new
  ID asks them to reject it twice.
- **Append only candidates that match nothing** under a clearly marked
  `## New in this run (YYYY-MM-DD)` heading using today's date. If nothing relevant changed, add
  **no** candidates (no duplicates).
- **Never delete an existing candidate**, including one whose evidence file has since gone. Note
  the missing evidence in your report instead; whether the guardrail still applies is the SME's
  call.

## Step 6 — Respect an existing constitution (deltas only)

If a constitution exists (Step 1), before finalizing candidates:

- For each **new** candidate, **semantically compare** it against existing constitution
  principles.
- **Suppress** any new candidate whose intent is already asserted by a ratified principle — do not
  propose duplicates of guardrails already in force.
- On a re-run, also compare every **existing checked (`- [x]`)** candidate whose status is not
  already `adopted`. Where the constitution now asserts its intent — because a previous
  `/speckit-constitution` run adopted it, or because someone wrote it in by hand — set its `status`
  to `adopted: <Principle name/number>`, naming the principle that carries it. Change nothing else
  on the item: its tick, its wording, and its place stay as the SME left them, so the file still
  records what was chosen. Leave an unchecked item's status alone even if the constitution happens
  to cover it — it was never selected, so it was never adopted from here.
- An `adopted` item is **never reverted**. If the principle it names has since been removed or
  rewritten so it no longer covers the item, keep the status and **report the drift** in chat; do
  not silently re-propose it.
- If a candidate would **modify** an existing principle, set its `status` to
  `amends: <Principle name/number>`, naming the principle it would change.
- If there is **no** existing constitution, proceed normally and note in the Inferred Domain
  section that the constitution will be created from the approved set.

## Step 7 — Report back in chat

After writing the file, report concisely in chat:

1. **Where the proposal was written** — the resolved path, e.g. `docs/DOMAIN_ANALYSIS.md`.
2. **Which template you used**, by resolved path.
3. A **one-line summary** of the inferred domain.
4. On a re-run: **how many new candidates** were appended, **how many fresh candidates matched an
   existing one** and were therefore not re-proposed, **which checked items were marked `adopted`**
   this run, any adopted item whose principle has drifted, any candidate whose evidence file is
   gone, and whether the prior decisions came from the earlier `.specify/memory/domain-analysis.md`
   (with the removal command from Step 0).
5. The exact next steps, verbatim intent:
   - *Review the file.*
   - *Check `- [x]` the guardrails you want (edit wording if you like; leave the rest
     unchecked).*
   - *Run `/speckit-constitution` referencing the file to adopt only the checked items.*

End with the handoff: the file as a link to the path you actually wrote — resolved root, not the
default — and the command as one ready-to-paste line. If no checked item is left to adopt — nothing
is ticked yet, or every ticked item is `adopted` — say so and give the review step alone, without the
command: a prompt that would adopt nothing invites a run that can only re-touch the constitution.

```text
Next: review and tick the guardrails you want in [DOMAIN_ANALYSIS.md](docs/DOMAIN_ANALYSIS.md), then run:

/speckit-constitution Adopt only the checked (- [x]) guardrails in docs/DOMAIN_ANALYSIS.md that are not marked "status: adopted", placing each in its section and applying "amends:" items as amendments
```

**Do not invoke `/speckit-constitution` yourself.** A portable command cannot rely on one agent's way
of calling another, and chaining would take the SME out of their own governance change at exactly the
moment they should be looking at it.

State clearly that **nothing is adopted until an SME checks it** — the file is opt-in by
design.

## Handoff contract (for `/speckit-constitution`)

The downstream constitution agent consumes this file as follows; keep the format compatible
with it:

- **Selected set** = every candidate whose checkbox is `- [x]` **and** whose status is not
  `adopted: …`. Only these are adopted; `- [ ]` candidates are ignored, and an `adopted` item is
  already in force, so adopting it again would duplicate a principle. An all-unchecked file — or one
  whose every checked item is adopted — yields zero guardrails.
- The **statement text on the checkbox line** is the adopted wording — SME edits flow through
  verbatim.
- `section` tells the constitution agent where to place the guardrail; `status: amends: …`
  tells it to modify the named principle instead of adding a new one.
