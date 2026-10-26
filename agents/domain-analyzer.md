---
id: domain-analyzer
title: Domain Analyzer
command: speckit.spectra.domain-analyzer
provider: spectra
type: add-on
phase: foundation
order: 20
status: available
summary: Infer the project's business domain from its code and docs, have an SME decide candidate guardrails lens by lens, and hand the result to the constitution.
manifest: Say whether the project has a constitution, infer its domain, work six lenses — handing workflow to speckit.spectra.methodology — and ask the SME seven questions to decide each lens's guardrails in the session — at least four options per question, one recommended, one Skip — then write the decisions and a Constitution input section to <artifact-root>/DOMAIN_ANALYSIS.md and hand it to /speckit-constitution to create or update the constitution. Reads documents imported by kb-vault as claimed, never as current practice, and replaces a DOMAIN_ANALYSIS.md it did not write only with consent.
---

Say whether the project has a constitution, so whether this run
creates or updates one, then scan the codebase, docs, and ADRs to infer the business domain and work
six lenses, handing workflow to the Methodology Analyst. It asks you to decide each lens's candidate guardrails in the session, with at least four
options per question, one recommended and one Skip. Only then does it write `docs/DOMAIN_ANALYSIS.md` —
or your declared artifact root — with a Constitution input section of what you accepted, and hand you a
ready-to-paste `/speckit-constitution` prompt. Documents imported by kb-vault are read as what they
*claim*, never as what the code does, and a guardrail you already accepted in an ADR is cited rather than
drafted twice. It never edits the constitution or source, and adopts nothing you did not choose.

## Arguments

none required. Optionally pass a focus or a domain hint to steer the analysis.

## Use it when

bootstrapping constitution guardrails for a brownfield project (no args — it infers
the domain from what's already there), or when you already know the domain and want to anchor the
analysis to it.

## Examples

```
/speckit-spectra-domain-analyzer
/speckit-spectra-domain-analyzer this is a banking system
```

## How it works

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

## Re-running and upgrading

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
