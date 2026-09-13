# Spectra Agents — full reference

What every agent does, its status, and how to run it where available. For the at-a-glance roster
(SDLC phase, AI-DLC phase, type, status), see the [Agents table in the README](README.md#agents).

**Status:** ✅ available today · 🚧 under development.

Every Spectra command lives under the unified `speckit.spectra.*` namespace. Triggers below use
**Claude's form** (`/speckit-spectra-<command>`). Other agents register the same command under a
slightly different trigger — kiro-cli, for instance, keeps the dots (`/speckit.spectra.adr`). The
manifest name (`speckit.spectra.<command>`) is the same everywhere.

## Contents

- [Shipped Spectra agents](#shipped-spectra-agents) — installable from the catalog today
- [Spec Kit core agents](#spec-kit-core-agents) — available, shipped by Spec Kit itself
- [Roadmap](#roadmap) — under development, grouped by SDLC phase

---

## Shipped Spectra agents

These ship in the `spectra` extension today. Install them all at once with
`specify extension add spectra`, then restart your AI agent so it picks up the commands.

<!-- SPECTRA:AGENT id=adr -->
### Architecture Decision Records (ADR) ✅

**`speckit.spectra.adr`** — Create a context-aware Architecture Decision Record grounded in your codebase,
prior ADRs, and the project constitution. It gathers project context, asks up to five clarifying
questions, writes the ADR under `docs/adr/` — or the artifact root your constitution declares — and flags
any constitution update the decision implies.

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

<!-- SPECTRA:AGENT id=domain-analyzer -->
### Domain Analyzer ✅

**`speckit.spectra.domain-analyzer`** — Scan the existing codebase, docs, and ADRs to infer the
project's business domain, then write an opt-in proposal of candidate guardrails to
`.specify/memory/domain-analysis.md` for SME review and handoff to `/speckit-constitution`. It never
edits the constitution or source — you choose which guardrails to adopt.

- **Arguments** — none required. Optionally pass a focus or a domain hint to steer the analysis.
- **Use it when** — bootstrapping constitution guardrails for a brownfield project (no args — it infers
  the domain from what's already there), or when you already know the domain and want to anchor the
  analysis to it.
- **Examples (Claude)** —
  ```
  /speckit-spectra-domain-analyzer
  /speckit-spectra-domain-analyzer this is a banking system
  ```

<!-- SPECTRA:AGENT id=kb-vault -->
### KB Vault ✅

**`speckit.spectra.kb-vault`** — Get the knowledge your team already has into the repository, where
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
Spectra already produces — an ADR, a BRD, an impact analysis, a test strategy, a defect RCA — it adopts
that agent's folder, numbering and template. Without that rule, a PDF of past architecture decisions
would land in a folder of its own beside the one the ADR agent maintains: two decision records, two
numbering schemes, and no rule for which is authoritative.

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

<!-- SPECTRA:AGENT id=test-strategy -->
### Test Strategy ✅

**`speckit.spectra.test-strategy`** — Decide how this project tests itself, once, at the start. It reads
the repository, works out for itself whether this is greenfield or brownfield, and writes one strategy to
`docs/test-strategy/TEST_STRATEGY.md` — or your declared artifact root — covering unit, integration, API
contract, and end-to-end testing plus a coverage floor. Then it drafts the constitution amendment that
would hold every future work session to it, and hands that to `/speckit-constitution`.

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

Two things it will not do. **It never writes your constitution** — not on approval, not on a re-run, not
if you insist. It drafts the amendment, shows it, records your approval in the strategy document, and
tells you the command that applies it, because one command should own constitution edits and the sync
impact report that goes with them. And **it never applies configuration**: the exact CI or coverage change
is written out for you to make.

Unlike the other document agents, it produces a **singleton** — one file at a fixed path, rewritten in
place on a re-run, with Git carrying the history. A standing policy has exactly one current answer, and
anything that links to it should not break every time you refresh it.

- **Arguments** — none required. Optionally pass a focus to weight the analysis; it never narrows the four
  mandatory lenses.
- **Use it when** — setting up a new project before the first feature, or landing Spectra on an
  established codebase and wanting a testing baseline that starts from what is already there.
- **Examples (Claude)** —
  ```
  /speckit-spectra-test-strategy
  /speckit-spectra-test-strategy focus on the API contract boundary with the payments service
  ```

<!-- SPECTRA:AGENT id=create-pr -->
### Create PR ✅

**`speckit.spectra.create-pr`** — Open a correctly-targeted GitHub PR for the branch you are on, optionally
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
- **Use it when** — a piece of work is ready for review and you want the PR opened against the right base,
  shaped like your team's template, without running `git`/`gh` by hand.
- **Examples (Claude)** —
  ```
  /speckit-spectra-create-pr
  /speckit-spectra-create-pr --draft
  /speckit-spectra-create-pr --base develop
  ```

<!-- SPECTRA:AGENT id=review-pr -->
### Review PR ✅

**`speckit.spectra.review-pr`** — Review a GitHub pull request against **the intent and standards it
carries**, not just the diff. It reads the PR's spec, plan, tasks, and ADRs *at the PR's own head
revision*, plus the constitution and ADRs in force on the **base** branch, then reports findings that a
diff-only reviewer cannot produce: a task marked complete but absent from the change, scope no
requirement authorized, a pattern an ADR forbids. Every finding cites a file, a line, and the clause,
requirement, or principle it rests on — anything that cannot be anchored and sourced is not reported at
all.

Then the reviewer takes over. **Nothing is pre-selected.** You choose which findings get published, you
choose the verdict, and you see the exact text before anything is posted. One review event goes to the
pull request under your own `gh` credentials, containing only what you selected — and the published body
declares that it was AI-assisted and human-curated. An empty selection posts nothing, which is a normal
outcome rather than a failure: a short, correct, human-endorsed review beats thirty findings that bury
the two that matter.

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
- **Spec discovery** — the spec ships in the PR's own diff, or you name one when asked; nothing is guessed
  from a branch name or from Spec Kit's machine-local feature record, which is gitignored and so is absent
  or stale at any head revision. A PR with no spec is reviewed standalone, and says so.
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
- **Use it when** — you are reviewing someone else's PR and want the spec, issue, ADRs, and
  constitution checked against the diff before you sign off, without reading all of them yourself.
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

<!-- SPECTRA:AGENT id=brd -->
### BRD Generator ✅

**`speckit.spectra.brd`** — Turn a raw business requirement into a structured, **specify-ready** BRD. It
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

<!-- SPECTRA:AGENT id=impact -->
### Impact Analyzer ✅

**`speckit.spectra.impact`** — Find out what a proposed feature would actually touch, **before** anyone
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
- **It does not** design the solution, estimate in story points, write requirements, create or link a
  spec, or touch `specs/`. An impact analysis and a specification are independent; feed one into the other
  by hand if you want to.
- **Examples (Claude)** —
  ```
  /speckit-spectra-impact We want to email customers who leave items in their cart for more than 24 hours
  /speckit-spectra-impact Add a nickname field to accounts reqs/nickname-brief.docx
  /speckit-spectra-impact --non-interactive Retire the v1 pricing endpoint
  ```

<!-- SPECTRA:AGENT id=test-plan -->
### Test Plan ✅

**`speckit.spectra.test-plan`** — Get the tests **agreed before anyone writes them**. Hand it the path to
a `spec.md` and it reads that specification, your constitution, your test strategy, your existing suite,
and the source the feature touches, then writes one `test-plan.md` **beside the spec**: scope with real
exclusions, a risk table that is a decision rather than an inventory, traceable test conditions,
environment and data, and an exit bar someone can make a go/no-go call from. It runs between `specify`
and `plan`, and it is built for teams who want the test set settled before the implementation is designed.

The document has two audiences and that shapes everything. A stakeholder reads it and approves it; the
planning command reads it and designs around it. So it states intent, not progress — and it produces no
tasks, writes no test code, and tracks nothing.

What makes it worth more than an hour with a whiteboard is **traceability that runs both ways**. Every
acceptance criterion in your spec reaches at least one test condition, or is reported as uncovered with a
reason — never absent from both. Every condition names what it verifies using your spec's own identifiers
(`FR-014`, `SC-003`, or the composed `US2-AC1` for an acceptance scenario), so a reviewer can check
coverage in either direction without opening the code. The run tells you the count.

What it refuses to do is as important as what it does:

- **It will not guess which spec you meant.** No branch-name inference, no `.specify/feature.json`, no
  most-recently-modified heuristic — and no picker either. With no argument it asks and stops, having read
  nothing. This is deliberately less helpful than the rest of the workflow: the output is a document that
  gets circulated and signed, and a plan built against the wrong spec reads as authoritative and is
  undetectably wrong to whoever approves it. A picker is the same failure with extra steps.
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

- **Arguments** — the path to a `spec.md`, or to the feature directory containing it (**required**, and
  never inferred). `--non-interactive` for CI.
- **Use it when** — a spec is finished, your team works test-first, and you want the test set reviewed and
  agreed before the implementation is planned. Skip it when nobody outside the implementing team needs to
  see the test set; it is an add-on, and nothing in the workflow prompts for it.
- **Where it writes** — `test-plan.md` in the directory of the spec you gave it. No sequence number, no
  artifact subfolder, no `Artifact root:` resolution for the output. A test plan is *about one feature*, so
  its identity is that feature's directory, exactly as `spec.md` and `plan.md` beside it carry no number.
  It reads your declared artifact root for one purpose only — finding `TEST_STRATEGY.md`.
- **Feeding it to the planner is one copy-paste.** The run ends with a ready-to-copy planning invocation
  naming the written path. No hook is registered and no core command is modified, so `plan` behaves exactly
  as it does today for anyone who never installs this agent. That is what keeps it genuinely optional.
- **Re-runs ask first.** The usual trigger is a `clarify` session changing the spec. It reads the existing
  plan, tells you what would change before you answer, and carries forward every *explicitly not covered*
  decision — or says it removed one. Declining leaves the file byte-identical. One file, rewritten in
  place; Git carries the history.
- **Priorities come from your spec.** A condition inherits the priority of the story it verifies, and only
  P1 conditions gate the exit criteria. The one override: a prohibition, safety, or data-integrity property
  is promoted to P1 whatever the story says, because a "MUST NOT" requirement rarely has a user story and
  is exactly the one whose violation is unrecoverable.
- **Template** — `test-plan-template.md`, a six-section structure. Override it at
  `.specify/templates/overrides/test-plan-template.md` to reshape or drop sections; the override is
  committed, team-wide, and survives extension updates. Each run reports which template it used. The
  traceability invariant, the no-checkbox rule, the cited-absence rule, the priority derivation, and the
  coverage statement stay with the command — a template shapes the document, not the standards.
- **It does not** write tests, generate tasks, modify your spec, touch test or CI configuration, edit the
  constitution, commit, or make a network request. It writes exactly one file.
- **Examples (Claude)** —
  ```
  /speckit-spectra-test-plan specs/021-signed-webhooks/spec.md
  /speckit-spectra-test-plan specs/021-signed-webhooks
  /speckit-spectra-test-plan --non-interactive specs/021-signed-webhooks/spec.md
  ```

<!-- SPECTRA:AGENT id=flaky-test-detector -->
### Flaky Test Detector ✅

**`speckit.spectra.flaky-test-detector`** — Find the tests that pass and fail on the same code, then fix
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

<!-- SPECTRA:AGENT id=defect-rca -->
### Defect Root Cause Analysis ✅

**`speckit.spectra.defect-rca`** — Take a defect down to its root cause, with evidence read from the code
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

---

## Spec Kit core agents

Available today, but shipped by **Spec Kit** itself — Spectra layers on top of them. No installation
beyond Spec Kit is needed; run them with their built-in commands.

<!-- SPECTRA:GENERATED START id=agents-list-speckit-core -->
<!-- Generated from agents-list.json — do not edit by hand. Run: python tools/generate_agent_docs.py -->

### Guardrails — `speckit.constitution` ✅

Encode your coding, security, and architecture standards once, so every downstream agent inherits
them.

- **Run it (Claude)** — `/speckit-constitution`

### Requirements Analyst — `speckit.specify` ✅

Turn a BRD or product brief into structured user stories with clear, testable acceptance criteria.

- **Run it (Claude)** — `/speckit-specify`

### Clarifier — `speckit.clarify` ✅

Interrogate vague or missing requirements up front, before they turn into expensive rework.

- **Run it (Claude)** — `/speckit-clarify`

### Requirements Quality — `speckit.checklist` ✅

Score the spec for completeness, clarity, and consistency — effectively unit tests for your
requirements.

- **Run it (Claude)** — `/speckit-checklist`

### Architecture Planner — `speckit.plan` ✅

Produce the technical plan and tech-stack decisions, choosing the design patterns that fit the
problem.

- **Run it (Claude)** — `/speckit-plan`

### Task Planner — `speckit.tasks` ✅

Break the plan into an ordered, dependency-aware task list, ready to sync straight to an issue
tracker.

- **Run it (Claude)** — `/speckit-tasks`

### Consistency — `speckit.analyze` ✅

Cross-check spec, plan, and tasks for drift, gaps, and contradictions before the build kicks off.

- **Run it (Claude)** — `/speckit-analyze`

### Implementation — `speckit.implement` ✅

Execute the task list in dependency order, building to spec with tests written alongside the code.

- **Run it (Claude)** — `/speckit-implement`

### Testing — `speckit.implement` ✅

Generate unit, integration, smoke, and end-to-end tests mapped to acceptance criteria — run inside
the Implementation agent, not as a separate command.

- **Run it (Claude)** — `/speckit-implement`
<!-- SPECTRA:GENERATED END id=agents-list-speckit-core -->

---

## Roadmap

Planned agents, grouped by SDLC phase. Descriptions reflect intended scope; the command lands when
each one ships. All are **🚧 under development**.

<!-- SPECTRA:GENERATED START id=agents-list-roadmap -->
<!-- Generated from agents-list.json — do not edit by hand. Run: python tools/generate_agent_docs.py -->

### Foundation

- **FDA 21 CFR Part 11 & IEC 62304** (Add-on) — Check electronic-records and e-signature integrity
  plus medical-device lifecycle rigor, mapped to software safety class.
- **ISO 27001 / 27701** (Add-on) — Audit ISMS and privacy-management controls against Annex A,
  reusing shared evidence across SOC 2, ISO, and HIPAA.

### Requirements & Discovery

- **GDPR Compliance** (Add-on) — Verify data-subject rights, lawful basis, minimization, retention,
  and transfers, and scaffold Article 30 records.
- **Canadian Privacy — PIPEDA / PHIPA / Law 25** (Add-on) — Evaluate PIPEDA's fair-information
  principles and Quebec Law 25's mandatory PIAs and privacy-by-default duties.
- **EU AI Act & Responsible-AI Governance** (Add-on) — Classify AI components by risk tier and
  assemble the transparency and Annex IV documentation the EU AI Act requires.
- **Legal-Obligation Extraction** (Add-on) — Turn regulatory and contractual text into testable
  acceptance criteria the compliance agents can consume.

### Architecture & Design

- **Architecture Reviewer** (Add-on) — Audit the design against best practices, design principles,
  and your own standards before a line is written.
- **HIPAA Compliance** (Add-on) — Audit PHI handling against the Security Rule technical safeguards
  and map gaps to §164.312.
- **PCI-DSS** (Add-on) — Scope the cardholder-data environment and check development, storage,
  crypto, and testing controls against v4.0.1.
- **Threat Modeling** (Add-on) — Generate design-time STRIDE and attack-surface analysis from
  data-flow and architecture.
- **Performance & Scalability** (Add-on) — Static hot-path, complexity, and N+1 analysis with
  load-model sanity checks, surfacing risk before the build.
- **Data Governance & Privacy Engineering** (Add-on) — Discover PII and PHI across code and schemas,
  map data flows and lineage, and classify data.
- **API Design & Contract** (Add-on) — Lint OpenAPI specs, detect breaking changes, and enforce
  versioning and backward compatibility.

### Implementation

- **Dependency & Supply-Chain** (Add-on) — Generate an SBOM and run reachability-aware
  vulnerability, license, and transitive supply-chain analysis.
- **Database & Data-Layer** (Add-on) — Review schema design, migration safety, and indexing,
  flagging lock risk and backward-incompatible changes.
- **Documentation Quality** (Add-on) — Assess API doc coverage, README and runbook completeness, and
  drift where the code changed but the docs did not.
- **Technical-Debt & Maintainability** (Add-on) — Quantify complexity, duplication, dead code, and
  smells into a maintainability rating and remediation estimate.

### Testing & Quality

- **Test Coverage Analyst** (Add-on) — Find the gaps against the test pyramid, so coverage is real
  protection rather than just a percentage.
- **Test Automation Analyst** (Add-on) — Recommend what is worth automating and where each test
  should run across the pipeline.
- **Security Analyst** (Add-on) — Surface threat exposure and OWASP-class issues through static and
  dynamic analysis of the change.
- **Accessibility & WCAG Compliance** (Add-on) — Audit the UI against WCAG 2.2 AA, map conformance
  to ADA, Section 508, and EN 301 549, then scaffold a VPAT.
- **Carbon & Green-Software** (Add-on) — Estimate software carbon intensity with the ISO-standard
  SCI methodology and surface the efficiency hotspots.
- **Internationalization Readiness** (Add-on) — Flag hardcoded strings, locale and RTL handling, and
  un-externalized resources before localization begins.
- **Responsible-AI & Bias** (Add-on) — Audit ML components for bias, fairness, and explainability,
  and scaffold the model card.

### Deployment & Operations

- **Operations Monitor** (Add-on) — Analyze logs, latency, and error signals post-deployment,
  surfacing anomalies and predicting SLA breaches.
- **Incident Responder** (Add-on) — Correlate incident signals with recent deployments, recommend a
  targeted rollback or fix, and validate the resolution.
- **SOC 2** (Add-on) — Map controls to the AICPA Trust Services Criteria and assemble continuous,
  change-managed evidence.
- **SOX Change-Management** (Add-on) — Validate segregation of duties and change-approval evidence,
  producing an immutable release-approval trail.
- **Infrastructure-as-Code Analysis** (Add-on) — Detect Terraform, CloudFormation, and Kubernetes
  misconfigurations and drift, mapped to CIS, PCI, and SOC 2.
- **Cost & FinOps** (Add-on) — Estimate cloud cost from IaC, flag right-sizing and waste, and show
  the cost delta of each change.
- **Observability Readiness** (Add-on) — Check whether logs, metrics, and traces are instrumented,
  SLOs defined, and alert coverage adequate.
<!-- SPECTRA:GENERATED END id=agents-list-roadmap -->
