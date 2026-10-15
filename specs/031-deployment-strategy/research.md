# Research: Deployment Strategist Agent

Phase 0 for [plan.md](./plan.md). The spec carries no `NEEDS CLARIFICATION` markers; these are the
design decisions the command's text has to make concrete.

## R1 — How a deployable is classified

**Decision**: classify each deployable from the strongest signal present, in this order of authority:
an explicit release or deploy step in CI → a packaging manifest's publish configuration → a platform
manifest → the shape of the entry point. The classes and their deciding signals:

| Class | Deciding signals (any one is enough when unambiguous) |
|---|---|
| **running service** | a container build plus an orchestration or platform manifest (Kubernetes, Helm, Compose used for deploy, Cloud Run/App Engine/ECS/Fly/Heroku config, serverless function config); a long-running server entry point |
| **static site / SPA** | a static build output deployed to a host or bucket (Pages, Netlify, Vercel, S3/CloudFront config) with no server runtime |
| **library / package** | a registry publish configuration (`npm publish`, PyPI trusted publishing, Maven/Gradle publishing, crates, NuGet) and no deploy target |
| **CLI / desktop tool** | a binary or tool entry point plus a distribution mechanism (release assets, Homebrew tap, `uv tool`/`pipx`, installer build, app bundle) |
| **mobile app** | an iOS or Android project, store metadata, Fastlane, or EAS configuration |
| **infra-only** | IaC with no application source of its own (Terraform/OpenTofu, Pulumi, CloudFormation, Helm charts published as the product) |

Workspaces declared by the project are authoritative for *how many* deployables there are; otherwise a
deployable is the co-location of an independent build manifest with source, as `test-strategy` defines a
surface. A deployable that matches two classes (a service that also publishes a client library) is two
deployables.

**Rationale**: deployment behaviour is visible in what CI and manifests *do*, so classification can be
read rather than asked (FR-008, FR-031). The order of authority stops a stray `Dockerfile` used only for
local development from making a library a "service".

**Alternatives considered**: asking the user — rejected, a wrong answer re-shapes every lens; a single
project-wide class — rejected, monorepos are common and the classes need different lens meanings.

## R2 — Greenfield, brownfield, mixed for deployment

**Decision**: classify from deployment *practice*, not code volume. Signals: CI that deploys or
publishes; platform or orchestration manifests; release configuration or tags; migration tooling; any
operational config (health endpoints, monitoring definitions, scheduled-job manifests). Mostly absent →
greenfield; mostly present → brownfield; substantial application source with no deployment practice →
mixed (the common case for a project about to ship its first release). Dissenting signals are reported.

**Rationale**: mirrors `test-strategy` Step 2, which measures practice rather than size. What changes the
document is whether there is a deployment practice to report before proposing.

**Alternatives considered**: reusing `test-strategy`'s classification — rejected, a project can have a
mature test suite and no deployment practice at all.

## R3 — How each lens adapts to the classification

**Decision**: the command carries one adaptation table; each lens resolves its meaning against the
deployable's class before reporting.

| Lens | Running service | Static site | Library | CLI / desktop | Mobile | Infra-only |
|---|---|---|---|---|---|---|
| Environments & promotion | environments | preview → production hosting | release channels (pre-release tags, dist-tags) | release channels (beta/stable) | internal → beta (TestFlight/Play tracks) → store; store review is an uncontrolled gate | workspaces/stacks per environment |
| Pipeline, artifact & traceability | image build, immutable tags, promotion of one image | build once, deploy the same bundle | build once, publish the same artifact; provenance | release assets, checksums, signing | signed builds; one build promoted through tracks | plan artifact applied unchanged |
| Release & versioning | as specified | as specified | SemVer is a contract with consumers | as specified | store version + build number | module versioning |
| Data & schema change | migrations | usually not applicable | not applicable unless it ships migrations | usually not applicable; local data format migration if any | local data migration | state migration (`moved`, imports) |
| Rollback & recovery | rollback + DR | redeploy previous build | yank / deprecate / supersede; no unpublish assumption | supersede; update channel pinning | phased rollout halt; no store rollback | revert and re-apply; state recovery |
| Operability & configuration | health, alerting, jobs, secrets, IaC, drift | uptime, config at build time | not applicable beyond registry hygiene | update checks, telemetry if any | crash reporting, remote config | drift detection, state locking |

**Rationale**: SC-004 requires zero infrastructure recommendations a project's evidence does not
support. A table the command resolves against is how that becomes mechanical instead of a judgement
made fresh each run.

**Alternatives considered**: separate commands per class — rejected, monorepos mix classes and the
handoff should be one document.

## R4 — The five questions: recommendations and confirmations

**Decision**: each question has a defined evidence source for its recommendation and a defined condition
under which it becomes a confirmation (it keeps its number either way, FR-029).

| # | Question | Recommendation drawn from | Becomes a confirmation when |
|---|---|---|---|
| 1 | Target platform / hosting | platform manifests, CI deploy steps, IaC providers, referenced documents | the evidence names the platform unambiguously |
| 2 | Who approves a production deploy, and how | CI environment protection, CODEOWNERS, manual-dispatch workflows, referenced documents; else convention: explicit approval by a named role through the CI system's environment protection | CI already encodes a required approval |
| 3 | Is there, or should there be, a stakeholder-review / pre-release environment | existing environment manifests or overlays; else convention by class (yes for a service with business stakeholders, release channel for a library) | an environment or overlay for it already exists |
| 4 | Availability and RPO/RTO targets | ADRs, SLO definitions, referenced documents; else the recommendation is "leave as an open question" — never an invented number | targets are documented, or the class has no running state (library, CLI, static site): confirm "not applicable" |
| 5 | Release cadence | tag history visible in the repository, release workflow triggers, changelog dates; else convention: release on demand from the default branch | a release workflow or changelog shows a clear pattern |

For question 4, the recommended option is never a number the agent supplies: the recommended answer when
nothing is documented is "record as an open question for the ops owner", and FR-024's open-questions
section carries it. Questions are asked once per project (clarification 2026-10-15); where deployables
differ, the question names the difference and accepts per-deployable free text.

**Rationale**: FR-028 requires evidence behind every recommendation; FR-024 forbids invented values. Q4
is where both pressures meet, so it is settled here rather than left to the run.

**Alternatives considered**: offering default RPO/RTO tiers as the recommendation — rejected, a plausible
number nobody chose is exactly the defect FR-024 exists to prevent.

## R5 — Four provenances

**Decision**: every claim carries one of `verified` (project-relative path, optionally line, to source,
CI, manifests, or IaC — what the repository does), `claimed` (a path to a document — README, ADR, a
referenced external file — asserting something the agent could not confirm in code), `stated` (a
clarification answer, naming its question number), or `convention`. Where a document's claim is confirmed
by code, the claim is `verified` and the document may be cited alongside.

**Rationale**: deployment documentation drifts from deployment reality more than most documentation,
because the pipeline is changed by whoever is on call. A reader has to tell what the workflow does from
what the wiki says it does.

**Alternatives considered**: `test-strategy`'s three provenances — rejected, it would file "the README
says blue-green" and "the workflow does blue-green" under the same label.

## R6 — A singleton with no earlier location

**Decision**: the command states that no earlier location exists for this document and that there is
nothing to migrate. In the test suite, `SINGLETON` entries become `(target, earlier-or-None)`, and the
earlier-location assertion skips a `None`. The constitution amendment adds
`<artifact-root>/DEPLOYMENT_STRATEGY.md` to Principle VII's named singletons without adding an earlier
location to the read-report-leave-alone list.

**Rationale**: the existing `SINGLETON` shape assumes every singleton has a pre-singleton past. Inventing
an earlier path to satisfy a test would make the command read a location that never existed.

**Alternatives considered**: a separate registry for new singletons — rejected, it would split one rule
across two dicts and let the next singleton choose the weaker one.

## R7 — The promotion-flow diagram

**Decision**: one Mermaid `flowchart LR` in the environments & promotion lens. Nodes are only the source
branch, the environments, and production (or the release channels) that the lens's table lists; edge
labels are only gates the table states. Recommended-but-not-yet-existing environments are drawn with a
dashed edge and labelled "recommended". No diagram when the lens is not applicable.

**Rationale**: clarification 2026-10-15 chose Mermaid. Binding the diagram to the table makes drift
between picture and text a detectable defect rather than a matter of taste.

**Alternatives considered**: one diagram per deployable — rejected for single-deployable projects;
permitted only where deployables genuinely promote differently, and then one per deployable, not more.

## R8 — What the amendment may contain

**Decision**: the draft carries only invariants the strategy establishes, drawn from this catalogue and
included only where the strategy supports them:

- production deploys only an artifact that has already passed every earlier gate, unchanged;
- a production deploy requires an explicit, recorded approval;
- no floating tag is a deployment identifier; every deployed artifact traces to a commit;
- schema changes are backward-compatible with the previous application version; rolling back the
  application does not roll back the database;
- every deployable has a documented rollback path;
- configuration and secrets enter environments through the declared mechanism, never by hand edit;
- the deployment strategy document is the reference for environment-specific detail.

The last item is how the constitution references `DEPLOYMENT_STRATEGY.md` without restating it.
Environment names, platform identifiers, cadences, and targets never appear as obligations.

**Rationale**: clarification 2026-10-15. A constitution that names a cluster needs amending on every
infrastructure change; one that states invariants does not.

**Alternatives considered**: the whole strategy as MUSTs; a single "follow the document" principle —
both rejected in clarification.

## R9 — kb-vault's reserved map

**Decision**: add a row to `kb-vault`'s reserved map: *a deployment strategy* → `<artifact-root>/` →
`DEPLOYMENT_STRATEGY.md` → `deployment-strategy-template`. The kb-vault test's `RESERVED` tuple gains the
row.

**Rationale**: kb-vault promises that a supplied document of a kind Spectra produces joins that agent's
set. Without the row, an ingested deployment strategy lands in a generic category folder beside the
singleton, and the next deployment-strategy run cannot find it.

**Alternatives considered**: leaving kb-vault unchanged — rejected, it silently breaks kb-vault's own
promise for the newest document type.

## R10 — "Going deeper" in session

**Decision**: when the user asks mid-session for detail beyond the high-level boundary (an alert
definition, a runbook step), the agent answers in the session. It adds that detail to the document only
on an explicit request, inside the relevant lens, and the run still writes exactly one file.

**Rationale**: clarification 2026-10-15 (operability stays high level; deeper by interaction). FR-034's
one-file rule forbids spilling the detail into a second document.

## R11 — Inputs outside the repository

**Decision**: local paths the user names in `$ARGUMENTS` or attaches are read with the host agent's own
file capabilities; formats the host cannot read are named in the could-not-read list. URLs are never
fetched; the agent says so and asks for local content where it matters. A referenced document's claims
are `claimed` (R5).

**Rationale**: FR-005, FR-049. Spectra ships no parser (Markdown-only package).

## R12 — Secrets

**Decision**: any value that looks like a credential, token, key, or connection string with an embedded
password is never reproduced in the session or the document; the agent cites the file and line and states
that a secret is present, and lists it as a finding under operability & configuration.

**Rationale**: FR-007; mirrors the secret rule in `impact`, `defect-rca`, and `kb-vault`.

## R13 — Versions and catalog fields

**Decision**: extension 1.19.0 → 1.20.0; `catalog.json` version and `provides.commands` 11 → 12; tags gain
`deployment`, `deployment-strategy`, `release`, and `operations`. Constitution 1.9.0 → 1.10.0. CLI
`VERSION` unchanged.

**Rationale**: Principle VI and Publishing Standards — a command added is MINOR on the catalog channel
only.
