---
id: deployment-strategy
title: Deployment Strategist
command: speckit.spectra.deployment-strategy
provider: spectra
type: add-on
phase: deployment-operations
order: 30
status: available
summary: Decide how this project gets from a merged change to something running or published — environments, gates, releases, rollback, and who owns what — grounded in what it already does.
manifest: Read the project and any local documents the user references, classify what it ships — service, static site, library, CLI or desktop tool, mobile app, or infrastructure — and write one deployment strategy to docs/DEPLOYMENT_STRATEGY.md (or DEPLOYMENT_STRATEGY.md at the project's declared artifact root) covering six lenses: environments and promotion, pipeline and artifact traceability, release and versioning, data and schema change, rollback and recovery, and operability and configuration. Each lens reports today's state before recommending, and every claim is marked verified, claimed, stated, or convention. Asks five judgment calls the repository cannot settle — hosting, production approval, a pre-release environment, recovery targets, release cadence — once per project and one at a time, each with a recommendation and the evidence behind it; never invents a value only the client or ops owner can supply, listing it as an open question instead. Operability stays at the level of policy and ownership. Then drafts only durable invariants as guardrails, records the team's decision on each under a frozen ds- ID, and hands a Constitution input section to speckit.constitution with a ready-to-paste line, to create the constitution or update it: it never edits the constitution, in any run, approved or not. Never edits source, CI, manifests, or infrastructure code, runs nothing, and makes no network request.
---

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

## Arguments

none required. Optionally a focus, paths to local documents, and `--non-interactive`.

## Use it when

a project is about to ship its first release, or an established project's deployment
practice has grown by accretion and needs writing down as one policy.

## Examples

```
/speckit-spectra-deployment-strategy
/speckit-spectra-deployment-strategy ./client/hosting-standard.md focus on the pre-release gate
```

## What it reads and records

Besides the CI, container, orchestration, infrastructure and migration files, it reads your constitution,
specs, ADRs, docs, and release configuration, and any `TEST_STRATEGY.md` or `DOMAIN_ANALYSIS.md` already
written.

A `convention` claim is a default with nothing behind it. Each guardrail it drafts is recorded under a
frozen `ds-` ID along with your decision on it.

The document's twelve sections are overridable at
`.specify/templates/overrides/deployment-strategy-template.md`.
