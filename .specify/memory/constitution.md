<!--
SYNC IMPACT REPORT
==================
Version: 1.11.1 → 1.12.0
Bump type: MINOR — materially expanded guidance. No principle added, removed, or renumbered.
  Not MAJOR: Principle I's intent — feature work goes through Spec Kit — is unchanged. The amendment
  says how the phases are run and draws the scope line explicitly; work that already complied with
  1.11.1 by running the workflow phase by phase still complies.
Rationale: agents were chaining specify → plan → tasks → implement in one turn, or building a feature
  straight from a chat ask. Principle I now defines feature work, makes each phase a user-held
  checkpoint, and requires out-of-band feature asks to be redirected to `/speckit.specify` with a
  suggested prompt. Small fixes and cosmetic changes are explicitly outside the workflow.

Modified principles:
  - I. Spec-Driven Development (We Dogfood Spec Kit) (title unchanged)
    - changed: "Non-trivial work" → "Feature work, as defined under Scope"
    - added: the user starts each phase and supporting command (`clarify`, `checklist`, `analyze`,
      `converge`, `taskstoissues`) by invoking it — a chat request to run one does not count; one
      command per invocation, then stop; out-of-band feature asks redirected with a ready-to-paste
      `/speckit.specify` prompt; a definition of feature work (new agent, material agent change, CLI
      behavior, packaging/distribution/release) and of what is exempt (small bug fixes, cosmetics,
      housekeeping); no implicit waiver; exempt work is still bound by Principles V–VI and ship.py
    - expanded rationale: chaining removes the review points; single maintainer means they are the
      only review; why small fixes are exempt

Modified sections:
  - Development Workflow — "adding or changing a command" narrowed to adding or materially changing
    one; small fixes may skip steps 1–4 but not 5–6 or Principle V; steps 1–4 and the supporting
    commands marked user-invoked, agent stops after each; long lines rewrapped

Added sections: none
Removed sections: none

Templates requiring updates:
  - .specify/templates/plan-template.md ✅ no change (Constitution Check reads principles at run time)
  - .specify/templates/spec-template.md ✅ no change
  - .specify/templates/tasks-template.md ✅ no change
  - .specify/templates/checklist-template.md ✅ no change
  - CLAUDE.md ✅ Principle I pointer added near the top
  - CONTRIBUTING.md ✅ "Add a new command" says each step is user-invoked and the agent stops

Follow-up TODOs: (none)
-->

# Spectra Constitution

Spectra is a curated set of [Spec Kit](https://github.com/github/spec-kit) commands — delivered as a
single self-contained Spec Kit extension — that enable full agentic development across the entire
software development lifecycle (SDLC), built and maintained by TELUS Digital. This constitution
governs how Spectra itself is built and how every command in the extension is authored, published,
and maintained.

## Core Principles

### I. Spec-Driven Development (We Dogfood Spec Kit)

Spectra is built using the same spec-driven workflow it ships to others. Feature work, as defined
under **Scope** below, MUST flow through Spec Kit — `specify` → `plan` → `tasks` → `implement` —
rather than ad-hoc edits. Specs live under `specs/`, and the project constitution under
`.specify/memory/` is the source of truth that plans are checked against.

**The phases are checkpoints, and the user holds every one of them.** These rules are non-negotiable:

- **The user starts each phase; the agent never does.** `specify`, `plan`, `tasks`, and `implement` —
  and the supporting commands `clarify`, `checklist`, `analyze`, `converge`, and `taskstoissues` where
  they are used — MUST each be started by the user invoking that command (for example
  `/speckit.specify`). The invocation is what starts the phase: a chat message asking the agent to run
  one does not, and the agent answers it with the command for the user to run. An agent MUST NOT start
  a phase the user did not invoke: not by running its command, not by calling it as a skill or tool,
  and not by writing its artifacts (`spec.md`, `plan.md`, `tasks.md`, or code) by hand.
- **One command per invocation, then stop.** When a phase or supporting command finishes, the agent
  MUST stop, summarize what it produced, and name the next command for the user to run. It MUST NOT
  continue into the next one, however obvious it looks and even when the user's original wording
  described the whole feature. The stop between phases is where the user reviews the result.
- **An out-of-band feature ask is redirected, not fulfilled.** When a user asks in plain chat — outside
  a Spec Kit command — for feature work, the agent MUST NOT start building it and MUST NOT start the
  workflow on the user's behalf. It MUST instead (1) say that the work is feature work and goes through
  spec-driven development under Principle I; (2) give a ready-to-paste `/speckit.specify` prompt
  drafted from the ask, stating what is wanted and why, with known constraints and open questions, and
  staying out of implementation detail; and (3) stop and wait. Reading code to write a better prompt is
  allowed; editing files is not.
- **Scope — what is feature work.** Feature work is a new capability or an enhancement, or a material
  change to how something behaves: adding an agent; materially changing what an agent does, asks, or
  produces; changing how the `spectra` CLI works — its command surface, install or update flow, or
  prerequisites; and changing how Spectra is packaged, distributed, or released. It goes through specs
  however few lines it takes. Everything else is outside these rules and MAY be done directly in chat,
  with or without plan mode and with no spec: small bug fixes that restore intended behavior, cosmetic
  and wording changes, typos, broken links, formatting, and documentation or tooling housekeeping. So
  are answering questions, explaining code, and reviewing; running a Spectra command
  (`speckit.spectra.*`) the user invoked; and amending this constitution through `constitution`. Where
  it is unclear whether an ask is feature work, the agent MUST treat it as feature work, say why, and
  redirect; the user may reclassify it as a small fix.
- **No implicit waiver.** Urgency, a small diff, or "just do it" phrasing does not turn feature work
  into a small fix and does not waive a checkpoint. An agent MUST NOT read a broad request — "build X
  end to end" — as permission to run more than one phase.
- **Work outside specs is still governed.** A small fix skips the spec, not the other principles: a fix
  to a command still bumps the catalog version and resyncs the package (Principle V), a fix to the CLI
  still follows Principle VI, and every change still lands through `tools/ship.py`.

Rationale: Spectra's value proposition is agentic SDD across the SDLC. If we do not use it to build
ourselves, we cannot credibly recommend it, and we lose our best feedback loop on the extension we
publish. Using it means stopping at its checkpoints: an agent that chains `specify` → `plan` → `tasks` →
`implement` in one turn removes the review points that make spec-driven development worth doing, and the
user is handed a finished feature built on a spec and plan they never approved. With a single maintainer
(see Governance), those checkpoints are the only review the work gets. Small fixes are exempt because a
spec for a correction that changes nothing a user would call new costs more review than the change
carries; the line is drawn at capability and behavior, not at diff size.

### II. A Single Self-Contained Extension

Spectra ships as exactly **one** self-contained Spec Kit extension: a single folder `spectra/` at the
repository root whose name equals the extension `id` (`spectra`, lowercase). It MUST contain one
`extension.yml` (with `id: spectra`), a `commands/` directory, `README.md`, `CHANGELOG.md`, and
`LICENSE`. Every Spectra capability MUST be a command file under `spectra/commands/`, registered in
the single `spectra/extension.yml`; new top-level extension folders MUST NOT be created for new
capabilities. The extension MUST NOT depend on any other extension; it installs and runs on its own.
The authoritative structure is the [Spec Kit Extension Development Guide](https://github.com/github/spec-kit/blob/main/extensions/EXTENSION-DEVELOPMENT-GUIDE.md).

Rationale: Users install one extension — `specify extension add spectra` — and get every command.
Spec Kit's own command-name rule (Principle III) forces this: because a command's namespace segment
must equal the extension `id`, every `speckit.spectra.*` command can only live in a single extension
whose id is `spectra`. One extension keeps the package portable, versioned as a whole, and consistent
by construction.

### III. Agent-Agnostic Commands

Command files MUST be written in Spec Kit's generic format using `$ARGUMENTS` for user input, and
MUST NOT hard-code any single agent's invocation syntax. Each command MUST be namespaced
`speckit.spectra.<command>` — a fixed `spectra` segment followed by a clear, descriptive command
name (for example `speckit.spectra.adr`, `speckit.spectra.domain-analyzer`,
`speckit.spectra.create-pr`) — MUST begin with YAML front matter containing a `description`, and MUST
be registered in `provides.commands`.

The namespace is not a stylistic choice: Spec Kit validates command names against the pattern
`^speckit\.<extension-id>\.<command>$`, so the **middle segment MUST equal the extension `id`**.
Spectra's id is `spectra`, therefore every command is `speckit.spectra.<command>`. When constructing
or reviewing a command, consult the authoritative
[Spec Kit Extension Development Guide](https://github.com/github/spec-kit/blob/main/extensions/EXTENSION-DEVELOPMENT-GUIDE.md)
for the manifest schema, the command-name pattern, the command-file format, and validation rules.

Rationale: Spec Kit translates one source file into each agent's native format at install time. A
single agent-neutral source supports every agent (slash-command and skills mode alike); hard-coding
one agent's syntax breaks that promise. Grounding command construction in the upstream guide keeps
Spectra valid against the exact rules Spec Kit enforces at install time.

### IV. Context-Aware by Default

Commands MUST read real project context — the constitution under `.specify/memory/`, specs under
`specs/`, existing artifacts, and source code — before acting, rather than blindly filling a
template. A command that ignores the project it runs in is a defect.

Rationale: The differentiator for Spectra commands over generic boilerplate is that they ground
their output in the actual codebase and its constitution. Context-awareness is the feature.

### V. The Catalog and Package Are Maintained in Sync

The repository is **public** — anyone can access it with no authentication — and Spectra is
distributed straight from it over direct `raw.githubusercontent.com` links: the root `catalog.json`
is the install-facing catalog and the single downloadable package lives at `docs/packages/spectra.zip`.
GitHub Pages serves `main` `/docs` at <https://telus-digital.github.io/spectra/>, but it publishes the
landing page only — **no part of the install path depends on it.** **Anyone can add the catalog and
install the extension anonymously.** Two small maintainer scripts under `tools/` produce the generated
artifacts — `build_package.py` for the zip and `generate_agent_docs.py` for the agent listings — and
their output is committed rather than built on demand, so the repository always reads correctly for
someone who never runs either. Everything else is maintained by hand. Completing, changing, or releasing
the extension MUST include, in the same change:

- registering the agent in `agents-list.json` — the **single source of truth for the roster**;
- building the package into `docs/packages/spectra.zip` (a single top-level `spectra/` folder, the
  layout Spec Kit expects) with `tools/build_package.py`;
- updating `catalog.json` — the single source of truth for the catalog — so the `spectra` entry
  (name, description, version, tags, command count, and `download_url`) matches `spectra/extension.yml`
  and the new zip;
- updating `docs/index.html` so the landing page lists the extension and its commands;
- regenerating every structured agent listing with `tools/generate_agent_docs.py`, and hand-writing the
  per-agent prose block a newly shipped agent needs; and
- committing `agents-list.json`, `catalog.json`, `docs/`, `README.md`, `AGENTS_LIST.md`, and the
  `spectra/` folder, then pushing to `main`.

**The roster is authored once and published everywhere.** `agents-list.json` declares which agents
Spectra offers; every *structured* listing of agents is generated from it and MUST NOT be hand-edited.
The generated regions — the Agents table in `README.md`, the Spec Kit core and Roadmap sections of
`AGENTS_LIST.md`, and the Commands table in `spectra/README.md` — are delimited by
`<!-- SPECTRA:GENERATED START id=… -->` markers and carry a do-not-edit notice. Per-agent explanatory
prose stays hand-authored and MUST NOT be generated; automation guarantees only that it *exists*, never
what it says. The division is by kind of content, not by file: if it is a table or a list, it is
generated; if it is a paragraph, it is written.

`catalog.json`, `docs/index.html`, `README.md`, `AGENTS_LIST.md`, and the published
`docs/packages/spectra.zip` MUST never drift from the `spectra/` folder or from `agents-list.json`.

This sync obligation governs the **catalog channel only** (the extension, its package, and the pages
that link to them). The `spectra` CLI is a *separate* distribution channel with its own version and is
NOT expected to move in lockstep with the catalog — it is governed by Principle VI.

The landing page MUST NOT hard-code data that another artifact already defines — neither channel's
version number, nor the extension's description, nor the agent roster. `docs/index.html` reads the
extension version and description from `catalog.json`, the agent information from `agents-list.json`,
and the CLI version from the newest published GitHub Release, all at page load. A value typed into HTML
is drift waiting to happen; a value fetched from the artifact that defines it cannot drift.

Rationale: The repo is the catalog channel's only distribution point — users discover and install the
extension entirely from it, against the raw `catalog.json`. A stale catalog or a missing zip ships a
broken install. Keeping a single catalog entry and rebuilding the zip as part of finishing a command
keeps the landing page, catalog, and download link consistent by construction.

### VI. Two Independently-Versioned Release Channels

Spectra ships through **two** distribution channels, and each carries its **own** version number on its
**own** cadence. They are NOT 1:1 and MUST be versioned independently:

- **Catalog channel** — the `spectra` extension, distributed over the raw `catalog.json` and
  `docs/packages/spectra.zip` links. Its version is authoritative in `spectra/extension.yml` (mirrored
  into the `spectra` entry of `catalog.json`) and MUST bump — per SemVer — whenever a command (agent) is
  added, changed, or removed. This channel is **never tagged**: merging to `main` is its release.
- **CLI channel** — the `spectra_cli/` package, distributed as a `uv` tool installed from this repo's
  git URL (`uv tool install spectra-cli --from git+https://github.com/telus-digital/spectra`). Its version is
  authoritative in the root `VERSION` file (read by `pyproject.toml`, reported at runtime via
  `importlib.metadata`, and mirrored by the release tag) and MUST bump — per SemVer — only when the CLI
  itself changes in a way consumers should pick up.

**Git tags and GitHub Releases on this repository belong to the CLI channel, and only to it.** Tags MUST
be bare semver (`X.Y.Z`); Releases MUST be titled `Spectra CLI X.Y.Z`. The catalog channel MUST NOT be
tagged or released. Reserving tags for one channel is what makes `/releases/latest` an unambiguous
answer to "what is the newest `spectra` command" — which both `spectra update` and the landing page
depend on. If the catalog also cut releases, the CLI's update check could resolve to an extension
release and attempt to install it as a version of itself.

**The CLI's own version MUST remain readable outside a Spec Kit project.** `spectra version` reports the
whole stack, so it legitimately requires a project with Spectra installed and cannot answer "what version
is this command?" from an arbitrary directory. Bare `spectra` MUST therefore keep printing a `cli vX.Y.Z`
line, and MUST keep working anywhere while changing nothing. Three things depend on exactly that: the CI
assertion that the installed distribution matches the committed `VERSION`, the release smoke test, and the
clean-room check that removing a project's agents leaves the command intact. None of them can use
`spectra version` — the last one deliberately runs in the state where `spectra version` correctly
refuses. A change that drops the banner's version line would break all three without failing loudly.

The two version numbers MUST NOT be coupled: adding or changing a command (an agent/extension) bumps the
catalog/extension version **without necessarily** touching the CLI, and changing `spectra_cli/` bumps the
CLI version **without necessarily** touching the extension or catalog. A change to one channel MUST NOT
force a version bump of the other, and the two versions are not expected to match at any point in time.

To keep that independence real rather than aspirational, the CLI MUST NOT hard-code the set of
extensions it installs. It MUST read `catalog.json` at run time and install what the catalog
advertises, so adding an agent reaches every existing install with no CLI release at all.

Rationale: The catalog and the CLI serve different needs and change for different reasons — the catalog
evolves as we add SDLC agents, while the CLI changes only when the onboarding flow does. Forcing a
shared version number would either inflate the CLI on every agent addition or block agent releases on
unrelated CLI work. Independent SemVer per channel keeps each artifact's version honest about what
actually changed in it.

### VII. Document Artifacts Live Under One Declared Root

Every command that produces a durable Markdown **deliverable** for the user's project MUST write it into
`<artifact-root>/<artifact>/`, where `<artifact>` is the artifact type as a lowercase kebab-case slug and
`<artifact-root>` is the project's single artifact root. The subfolder MUST be created on demand, MUST hold
exactly **one** artifact type, and the command MUST NOT write anywhere else. Filenames MUST carry a
zero-padded three-digit sequence number scoped to that subfolder, starting at `001`. The two shipped
document agents define the pattern: `<artifact-root>/adr/ADR-NNN-<kebab-title>.md` and
`<artifact-root>/brd/NNN-<kebab-title>.md`. A new document-producing agent MUST take its own sibling
subfolder — `<artifact-root>/threat-model/`, `<artifact-root>/api-design/` — and MUST NOT introduce a
top-level folder of its own.

**A standing-policy artifact is one flat file at the root, not a series.** Where a document type has
exactly **one** current answer per project — a policy that a re-run replaces rather than adds to, as the
constitution is — the command MUST write it as a single file directly in the artifact root, named
`<artifact-root>/<UPPER_SNAKE_NAME>.md`: no subfolder, no sequence number. A re-run MUST rewrite that file
in place and MUST NOT create a second one; Git carries the history. The three shipped singletons are
`<artifact-root>/TEST_STRATEGY.md` (`speckit.spectra.test-strategy`), `<artifact-root>/DOMAIN_ANALYSIS.md`
(`speckit.spectra.domain-analyzer`), and `<artifact-root>/DEPLOYMENT_STRATEGY.md`
(`speckit.spectra.deployment-strategy`). A singleton that never had an earlier location has nothing to
read under the rule below and needs no migration. Everything else in this principle still binds a singleton — the
declared root, the publication check, the non-publishing fallback, the lowercase project-relative
directory path, and the read-report-leave-alone rule for earlier locations. Only the filename is
uppercase, which is what marks it as the one standing document rather than an entry in a series. A
series artifact — `adr`, `brd`, `impact-analysis`, `defect-rca`, and any agent whose re-run produces a
new document rather than a replacement — keeps the subfolder and the `NNN` sequence. A new singleton
MUST be named in this paragraph by amendment; a command MUST NOT declare itself one.

**The root defaults to `docs/` and is declarable per project.** A project overrides it with a single line
in its constitution, matched case-insensitively:

```text
Artifact root: documents/
```

A declared root MUST be honoured by **every** document-producing command, so a project decides this once
and every present and future agent inherits it. It MUST be project-relative — no leading slash, no `..` —
and a command that finds an unusable value MUST say so and fall back to the default rather than guess.

**A command MUST NOT write that declaration itself.** It offers the exact line and lets the user add it.
Producing a document is not a licence to edit governance; the one constitution change a Spectra command
may propose is one that is *about* the decision it just recorded, and even that requires explicit
approval.

**Defaulting into `docs/` requires a publication check first.** `docs/` is GitHub Pages' only non-root
branch source and the default source directory for MkDocs and Docusaurus, so on a minority of projects
writing there publishes the artifact to the web or breaks a documentation build. Before defaulting, a
command MUST look for that signal — `mkdocs.yml`, `docusaurus.config.*`, `docs/_config.yml`,
`docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, or a Pages configuration pointing at `docs` — and,
finding one with no declared root, MUST surface it, recommend `documents/`, and let the user choose. Where
the choice cannot be obtained it MUST take the non-publishing option: a document written to the wrong
private folder is moved with one command, while a business requirements document served on the public web
cannot be recalled from caches, clones, or forks.

**Spec Kit's own locations are outside this rule.** `.specify/` (constitution, memory, extension assets)
and `specs/` belong to Spec Kit, and a command writing there — as `speckit.spectra.flaky-test-detector`
does with its resumable task list in `.specify/memory/` — is writing **context** for another command to
consume, not a deliverable for a human to read. The rule governs deliverables. A document a human
reviews and edits before handing it on — a guardrail proposal an SME decides on — is a deliverable, even
when another command consumes it next.

**A per-feature deliverable lives beside the specification it concerns.** A document that is *about one
feature* — read by a human, and consumed next to that feature's `tasks.md` — is written into the
feature's own `specs/<feature>/` directory rather than under the artifact root, because moving it would
sever it from the specification a reader is holding, and the directory already supplies the sequence a
`NNN` prefix would repeat. The shipped per-feature deliverables are `specs/<feature>/test-plan.md`
(`speckit.spectra.test-plan`) and `specs/<feature>/uat-report.md` with its run-stamped `uat/` evidence
(`speckit.spectra.uat`). Such a command MUST write nowhere else, MUST take the feature as an explicit
input rather than infer it, and MUST stop before writing when the specification lies outside the project
it was invoked in — its destination comes from its input, so that is where the write scope is checked. A
new per-feature deliverable MUST be named in this paragraph by amendment. Everything else in Principle
VIII still binds it: it is shaped by a registered, overridable template.

**Paths MUST be lowercase and project-relative.** Not `Docs/`, not `/docs/`. This is correctness, not
style: mixed case is a distinct directory on Linux but silently aliases into an existing `docs/` on a
case-insensitive macOS filesystem, so one command produces two different layouts; and a leading slash
names the filesystem root rather than the project.

**A location an earlier version wrote to MUST be read, reported, and left alone.** That covers the
pre-1.6.0 folders (`Docs/ADR/`, `brds/`), the pre-singleton locations
(`docs/test-strategy/TEST_STRATEGY.md`, `.specify/memory/domain-analysis.md`), and the default root itself
once a project declares a different one. For a singleton the read is for its prior content — answers,
decisions, an SME's choices — rather than for sequence continuity, and where both the earlier and the
canonical file exist the canonical one wins. The command MUST read those locations — matching case-insensitively — for context and for sequence
continuity, so the next number is one greater than the highest found across the canonical folder *and*
every superseded one. It MUST report the superseded folder once, name the canonical one, and offer the
move as a command the user can run. It MUST NOT move, rename, modify, or delete anything there itself.

Rationale: A consumer installs **one** extension and gets many document-producing agents. If each picks
its own folder, the project root accumulates an unrelated top-level directory per agent and nobody can
predict where an agent's output went — the roster already lists a dozen more document producers under
development. One root, one subfolder per artifact type, decided once, means every future agent inherits
the answer instead of inventing one. The root is declarable rather than fixed because whether `docs/` is
safe is a fact about the project that cannot be known when the command is authored: `docs/adr/` is the
convention most teams expect, and the minority who publish `docs/` need an escape hatch that costs them
one line and then applies everywhere. Reading superseded locations rather than ignoring them is what keeps
a cut-over from producing a duplicate `ADR-001`; refusing to move them is what keeps a documentation agent
inside the write scope it promises. A singleton is the exception because a subfolder and a sequence number
both describe a series, and a standing policy is not one: a folder that can only ever hold one file is
noise, and a `001-` prefix on a document that is rewritten in place promises a `002-` that never comes.
Writing it flat at the root, under a fixed uppercase name, gives the one path a reader, a link, and the
next command can rely on.

### VIII. Documents Are Shaped by Overridable Templates

Where Principle VII settles **where** a produced document goes, this settles **how it is shaped**. Every
command that produces a durable Markdown deliverable MUST take its structure from a **template**, and that
template MUST be:
- **Shipped as an asset**, not embedded as a literal in the command file — one file per document type under
  `spectra/templates/`, named `<artifact>-template.md`;
- **Registered** in `spectra/extension.yml` under `provides.templates` with `name`, `file`, and
  `description`. An unregistered template file, or a registered entry whose file is missing, is a defect;
- **Resolved through Spec Kit's stack**, highest priority first: `.specify/templates/overrides/<name>.md` →
  `.specify/presets/<preset-id>/templates/<name>.md` → `.specify/extensions/<ext-id>/templates/<name>.md` →
  `.specify/templates/<name>.md` → the command's own inline skeleton as the last resort. A command MUST NOT
  hard-code a single template path, and MUST take the first readable, non-empty layer.

**"Deliverable" means the document, not the destination.** A file written into the artifact root is one; so is a
Markdown document a command **emits** without saving locally — a pull request body, a review comment, an issue
description. If a human reads it and a command composed it, it is shaped by a template. Only the *location*
rules of Principle VII are limited to files on disk.

**The project override is the supported customization point.** `.specify/templates/overrides/<name>.md` is
committed, applies to the whole team, and sits outside the extension tree — so it survives
`specify extension update`. Editing the *installed* copy under `.specify/extensions/` MUST NOT be documented
as the way to customize anything: extension-provided files resolve as `replace`, so a version bump discards
the edit, and because the path is tracked by Git the change looks durable until it silently reverts.

**A resolved template is honoured, not repaired.** A command MUST follow the sections the resolved template
declares, in its order, and MUST NOT add, rename, or reorder them. Where a template omits a section the
command would ordinarily fill, the command MUST note the omission rather than reinstating it — anything else
turns a team's override into a suggestion. Guidance comments and `[PLACEHOLDER]` tokens MUST be stripped from
the output whichever layer the template came from.

**The command MUST report which template it used**, naming the resolved path. Without that, an override that
failed to apply is indistinguishable from one that applied, and the user's first clue is a wrongly-shaped
document.

**Resolution MUST be expressed as prompt instructions.** Spec Kit's `resolve_template()` is a Bash function
in core's script tree: depending on it would break agent-agnosticism (Principle III) wherever Bash is not the
script flavour, and shipping a resolver of our own would break the Markdown-only guarantee the published
package makes — no scripts, no binaries, no post-install hooks. The commands therefore state the same
priority order in prose.

Rationale: A template is the difference between a consistent document set and a pile of differently-shaped
files, and an *overridable* template is the difference between Spectra's opinion and the team's. Both shipped
document agents had a template; only one was a file, and neither honoured the project's own override — so a
team's only lever was editing an installed file that the next update deletes. Shipping the structure as a
registered asset resolved through the stack means one file in a repository changes every document produced
from then on, for everyone, permanently. Requiring the same of future document agents keeps that promise from
being re-litigated per agent, which is exactly how the `adr`/`brd` divergence arose in the first place.

## Publishing & Distribution Standards
- **Semantic Versioning (per channel).** Both release channels follow [SemVer](https://semver.org/) on
  independent cadences (Principle VI). Each **extension (catalog) release** MUST bump `extension.version`
  in `spectra/extension.yml` and the matching `version` in the `catalog.json` entry, and add a matching
  `spectra/CHANGELOG.md` entry under that version heading; renaming or removing a command is a breaking
  (MAJOR) change. Each **CLI release** MUST bump the root `VERSION` file and be published under a
  matching bare-semver Git tag `X.Y.Z`; a breaking change to the install flow, the command surface, or
  the prerequisites is MAJOR. A bump to one channel MUST NOT be mirrored onto the other unless that
  channel actually changed.
- **The CLI version is single-sourced and CI-enforced.** `VERSION` is the sole source of truth for the
  CLI: `pyproject.toml` reads it and the tool reports it via `importlib.metadata`. The release workflow
  MUST refuse to publish when the pushed tag and `VERSION` disagree, so the committed version, the git
  tag, and the installed version cannot drift.
- **Compatibility pinning.** `spectra/extension.yml` MUST set `requires.speckit_version` to the Spec
  Kit version range actually tested against. Re-test when Spec Kit is upgraded.
- **Required manifest fields.** `extension.yml` MUST provide `schema_version`, `id`, `name`,
  `version`, `description`, `category`, `effect` (`read-only` or `read-write`), `author`,
  `repository`, `license`, `requires.speckit_version`, and `provides.commands[]` (with each command's
  `name`, `file`, and `description`).
- **Authorship & license.** Author is `TELUS Digital`; the extension is Apache-2.0 licensed unless
  explicitly stated otherwise, and carries its own `LICENSE`, `NOTICE`, **and** `TRADEMARK.md`. All
  three MUST ship inside the published package — Apache-2.0 §4(d) makes the `NOTICE` attribution
  binding on downstream redistributors, so dropping it silently weakens the attribution requirement,
  and §6 withholds trademark rights that only `TRADEMARK.md` actually spells out. A consumer who has
  only the installed package MUST be able to read what the licence does not grant.
- **No silent drift.** Before publishing, verify that `catalog.json`, `docs/packages/spectra.zip`, and
  `docs/index.html` all agree with the `spectra/` folder and use the raw
  `raw.githubusercontent.com/telus-digital/spectra/main/...` URLs; any mismatch MUST be resolved first. CI
  enforces this: `.github/workflows/ci.yml` fails when `extension.yml` and `catalog.json` disagree on
  the version or the command count, when the committed zip has drifted from the `spectra/` folder, or
  when `tools/generate_agent_docs.py --check` finds a generated region out of date with
  `agents-list.json`, a shipped agent with no prose block, a prose block for an agent the roster does
  not ship, a hand-written heading drifted from an agent's canonical title, or a disagreement between
  the roster and the manifest about the shipped set.

## Development Workflow

Adding a command, or materially changing one, is feature work and MUST flow through the Spec Kit
spec-driven commands (Principle I) — the `spectra/` folder MUST NOT be hand-created, feature work in it
MUST NOT be done ad hoc, and new capabilities are added as commands under it, never as new extensions.
A small fix to an existing command is outside Principle I's scope and may skip steps 1–4, but not
steps 5–6 or the sync obligations of Principle V. Steps 1–4 are the Principle I checkpoints: the user
invokes each one, and the agent stops when it finishes and names the next.

1. **Specify** (`specify`, user-invoked; the agent stops after it) — describe the command in plain
   language: its purpose and `read-only` vs `read-write` effect. This creates the spec branch (via the
   `before_specify` hook, per the Version Control & Branching Strategy) and
   `specs/<NNN>-<name>/spec.md`. The user may run `clarify` to resolve open questions before planning,
   and `checklist` to check the spec's quality; each is user-invoked and the agent stops after it.
2. **Plan** (`plan`, user-invoked; the agent stops after it) — generate the design artifacts. The
   Constitution Check gate enforces the single self-contained `spectra/` extension (Principle II), a
   new command file under `spectra/commands/` registered in `spectra/extension.yml`, agent-agnostic
   `$ARGUMENTS` commands under the `speckit.spectra.<command>` namespace (Principle III),
   context-awareness (Principle IV), the catalog/package sync obligations (Principle V), and — for any
   command that produces a document — the artifact-root output convention (Principle VII) and the
   registered, overridable template it is shaped by (Principle VIII).
3. **Tasks** (`tasks`, user-invoked; the agent stops after it) — produce the dependency-ordered task
   list. The user may then run `analyze` for a cross-artifact consistency check, or `taskstoissues`
   to open the tasks as GitHub issues; each is user-invoked and the agent stops after it.
4. **Implement** (`implement`, user-invoked; the agent stops after it) — execute the tasks: add the
   command file under `spectra/commands/`, register it in `spectra/extension.yml`, bump
   `extension.version` with a matching `spectra/CHANGELOG.md` entry, rebuild
   `docs/packages/spectra.zip` (a single top-level `spectra/` folder), update the `spectra` entry in
   `catalog.json` (the single source of truth) and `docs/index.html`, register the agent in
   `agents-list.json`, and regenerate the structured agent listings with
   `tools/generate_agent_docs.py` (Principle V). Where work is left unbuilt, the user may run
   `converge` to append it to `tasks.md` and then `implement` again; `converge` too is user-invoked
   and the agent stops after it.
5. **Test locally** by installing the working copy with `specify extension add --dev <path-to-spectra>`
   into a throwaway Spec Kit project and exercising every command end to end before publishing.
6. **Publish** by committing the `spectra/` folder, the `specs/` artifacts, the updated `catalog.json`,
   `docs/`, and `README.md`, then running `tools/ship.py` — a direct push to `main` is rejected, per
   the Version Control & Branching Strategy. The procedure is `SHIPPING.md`. Once the push lands the
   catalog and package are live immediately at their `raw.githubusercontent.com` links.

User-facing documentation (`README.md`) and contributor documentation (`CONTRIBUTING.md`) MUST be
kept consistent with these principles whenever behavior changes.

## Version Control & Branching Strategy

Every spec is developed in isolation on its own dedicated Git branch. Work for a spec MUST NOT be
committed directly to `main`; it flows through that spec's branch and is merged back only when the
spec is complete.

- **One branch per spec.** Each new spec MUST get its own branch. A single branch MUST NOT hold work
  for more than one spec, and a single spec MUST NOT be split across multiple branches.
- **Branch name equals spec name.** The branch name MUST exactly match the spec's directory name
  under `specs/` — identical sequential number and identical kebab-case title (for example, spec
  `001-domain-analyzer` is developed on branch `001-domain-analyzer`).
- **Create the branch before specifying.** The spec branch MUST exist before specification work
  begins. The `before_specify` Git hook (`speckit.git.feature`) automates this; if it is unavailable,
  the branch MUST be created manually with the matching name before `specify` runs.

**Nothing lands on `main` whose commit has not passed CI.** Every commit that reaches `main` MUST
carry a green run of every required status check **on its own SHA** before it gets there. This is
enforced rather than reviewed: a branch ruleset requires those checks and **no actor may bypass it**.
Because check runs attach to a commit rather than to a branch, the commit earns them on a staging
branch and is then pushed unchanged to `main` — `tools/ship.py` performs exactly that sequence and is
the only sanctioned way to write to `main`. The mechanism, the release paths, and the break-glass
procedure for an Actions outage are documented in `SHIPPING.md`.

This is a **separate obligation** from one-branch-per-spec above, and both hold. The branching rule
governs how *spec work* is organised; this one governs *every* change, including the documentation,
tooling, and housekeeping commits that never had a spec. A change can satisfy one and violate the
other, so neither excuses the other.

Rationale: Spectra dogfoods the same Git workflow its `git` extension ships. Pinning the branch
name to the spec name keeps the branch, the spec directory, and downstream automation (feature
hooks, change descriptions) trivially traceable to one another, and one-branch-per-spec keeps `main`
releasable and each spec's history reviewable in isolation.

## Governance

This constitution supersedes ad-hoc practice for the Spectra repository. All plans and changes MUST
verify compliance with the principles above; any deviation MUST be justified in the plan's Complexity
Tracking (or equivalent) and accepted before the change lands on `main`.

**Amendment procedure.** Amendments are made as a normal change on the repository's own workflow, MUST
document what changed and why, and MUST update this file together with any dependent templates and docs
in the same change.

**One maintainer, and the review is still binding.** This repository has a single owner and maintainer;
Issues and Discussions are disabled and it accepts no outside contributions, so every gate below is
self-applied. That makes the gates more load-bearing, not less — there is no second reader to catch a
principle quietly skipped. A deviation MUST be written down where a later reader will find it, not
settled in the maintainer's head.

**Versioning policy.** This constitution is versioned with Semantic Versioning:
- **MAJOR** — backward-incompatible governance changes or principle removals/redefinitions.
- **MINOR** — a new principle or section, or materially expanded guidance.
- **PATCH** — clarifications, wording, and non-semantic refinements.

**Compliance review.** The Constitution Check gate in the plan template is binding on whoever reviews
the change, including the maintainer reviewing their own. Complexity that violates a principle MUST be
justified or removed; unjustified violations block the change.

**Version**: 1.12.0 | **Ratified**: 2026-07-12 | **Last Amended**: 2026-10-24
