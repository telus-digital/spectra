---
id: impact
title: Impact Analyzer
command: speckit.spectra.impact
provider: spectra
type: add-on
phase: requirements-discovery
order: 30
status: available
summary: Find out what a proposed feature would actually touch, with cited evidence, before anyone commits to building it.
manifest: Produce a codebase-grounded feature impact analysis for a stakeholder go / no-go decision before any specification work begins — cited findings, a defined impact rating, at most five clarifying questions, and a stated coverage boundary — written under docs/impact-analysis/ (or the project's declared artifact root). Makes no network request and accepts no repository URL: other systems are declared as text, a document, or a local directory read in place.
---

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

## Arguments

the feature intent as one paragraph (required), plus optional document paths
(`.md`, `.txt`, `.pdf`, `.docx`) for a brief, an epic, or a prior analysis. `--non-interactive` for CI.
Five cap overrides — `--seed-cap`, `--hops`, `--max-files`, `--identifier-cap`, `--per-system-cap` —
when the defaults are too tight for a large repository.

## Use it when

a feature has been proposed and someone has to decide whether to fund it, and the
honest answer to "what else does this touch?" is currently a guess.

## More than one repository?

It asks. Other systems are declared as a sentence, as a document, or as a
**path to a local copy** it reads in place. It accepts no repository URL and makes **no network request
at all** — not even for a public repo with `gh` authenticated. A system with no local checkout is
recorded as described, and still produces a handoff item naming the owning team and the exact contract to
confirm with them.

## Where it writes

`docs/impact-analysis/` by default, as `NNN-<name>.md` plus an auto-maintained
index. Declare `Artifact root: documents/` in the constitution to move it, and every Spectra document
agent follows. Since `docs/` is GitHub Pages' only non-root branch source and the default for MkDocs and
Docusaurus, it checks for that setup first and asks before writing an analysis somewhere it would be
published — this document names internal systems, owning teams, and unmitigated risks.

## Approval is yours, and manual.

Every run writes `status: draft`. You take it to your stakeholders and
record their answer in the front matter yourself; the command never sets any other status. The index is
rebuilt from the documents on each run, so an approval you record by hand shows up there without the
command editing anything.

## Re-runs never overwrite.

Every run takes the next number and writes a new document — including a
re-run with identical input. Each report carries its own timestamp and a verbatim record of what it was
asked, and the one it supersedes is linked rather than replaced.

## Template

`impact-analysis-template.md`, a ten-section structure. Override it at
`.specify/templates/overrides/impact-analysis-template.md` to reshape or drop sections; the override is
committed, team-wide, and survives extension updates. Each run reports which template it used. The
citation rule, the confidence levels, the rating triggers, and the coverage statement stay with the
command — a template shapes the document, not the standards.

## What it does not do

It does not design the solution, estimate in story points, write requirements, create or link a
spec, or touch `specs/`. An impact analysis and a specification are independent; feed one into the other
by hand if you want to.

## Examples

```
/speckit-spectra-impact We want to email customers who leave items in their cart for more than 24 hours
/speckit-spectra-impact Add a nickname field to accounts reqs/nickname-brief.docx
/speckit-spectra-impact --non-interactive Retire the v1 pricing endpoint
```

## Change the shape of your impact analyses

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

## How it works

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

## Numbering, interruptions, and the publishing check

The next number is one greater than the highest present, not a count of the files. An interrupted run
leaves the folder untouched and consumes no number.

An impact analysis also says where secrets live, which is one more reason the `docs/` publishing check
asks first. Unanswered, it picks the non-publishing folder.

Nothing under `specs/` is written or depended on, and there is no `spec_refs` field.
