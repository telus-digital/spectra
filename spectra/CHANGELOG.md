# Changelog

All notable changes to the `spectra` extension are documented here. This project follows
[Semantic Versioning](https://semver.org/).

## [1.16.0] - 2026-09-11

### Added
- **`speckit.spectra.kb-vault` — the knowledge your team has, in the repository where agents can read it.**
  Attach the documents — a PDF of architecture decisions inherited from a previous team, a Word file
  describing the engineering workflow, a deck of UX/UI standards, a diagram exported as an image — or
  just describe what you know. It absorbs all of it, works out what kind of document each source is,
  learns how your project already keeps documentation, and shows you a table of exactly what it intends
  to write and where. Then it stops and waits. Only after you approve does anything land, as Markdown,
  under your artifact root.

  Three decisions a reader would otherwise find surprising:

  **It shows a plan and stops, which no other document agent does.** Every other Spectra command writes
  as its final act and you see the result. This one is aimed at repositories that already have
  documentation, where an unwanted *update* is not trivially undone by someone who did not notice it
  happened — so the plan table is the safety mechanism, and a comment on it is not approval of it. Any
  change re-presents the whole table. An ambiguous answer writes nothing.

  **It updates rather than duplicates, even outside the artifact root.** Supply a revised standards
  document and it finds the one you already have — matching on subject and category, never on title
  similarity — and edits it in place, at its existing path, keeping its name and the hand-written
  sections your source never mentions. That is a deliberate departure from the usual "one root, one
  folder" rule: on any project whose documentation predates Spectra, writing the update into the root
  instead would leave you with two documents disagreeing with each other and no rule for which is
  current. New files stay bounded to the root; only updates go where the document already lives.

  **It never invents, and it never mines your codebase.** Every substantive sentence traces to
  something you supplied. A template section with no source says so instead of being filled. A file it
  cannot read is named and its content requested — never guessed at from the filename. A diagram is
  transcribed only as far as it is legible, and where the structure will not carry, it says that rather
  than implying a picture is present. And "document the architecture" with nothing attached gets you a
  request for material, not documentation reverse-engineered from source code.

  Where a supplied document is a kind Spectra already produces — an ADR, a BRD, an impact analysis, a
  test strategy, a defect RCA — it adopts that agent's folder, numbering and template, so it joins the
  existing set rather than starting a second one beside it. Everything else takes its own category
  folder, with an index maintained beside it. Six sections, overridable at
  `.specify/templates/overrides/kb-document-template.md`, or per category at
  `.specify/templates/overrides/<category>-template.md`.

  It commits nothing. When the files are written it tells you they are uncommitted and hands the review
  back to you.

- `kb-document-template` — the default shape for an ingested knowledge document: purpose and scope with
  real exclusions, context, the substance in whatever structure the source actually has, the rules and
  decisions pulled out so they can be cited, the open questions and gaps, and provenance naming the
  sources it came from.

## [1.15.0] - 2026-09-11

### Added
- **`speckit.spectra.defect-rca` — the root cause, not the first plausible code path.**
  Hand it a defect — a JIRA ticket reference, a GitHub issue URL, or just a description of what went
  wrong — and it reads the project before it asks you anything: the constitution, the implicated code,
  the commits that touched it, the configuration, the tests. It builds a MECE hypothesis tree, tests
  what the repository can settle, asks at most five questions per round about the runtime facts nobody
  can grep for, and writes one advisory analysis to `docs/defect-rca/NNN-<slug>.md` — or wherever the
  project's declared artifact root puts it — with the root cause stated first, the evidence that
  settled it, the impact, and corrective and preventive actions carrying owners and verification
  criteria.

  It fixes nothing, writes no test, and updates no ticket. The conclusions are yours; it is a coach and
  a structuring aid.

  Four decisions a reader would otherwise find surprising:

  **It attempts and degrades on `gh` rather than gating on it.** `create-pr` and `review-pr` refuse to
  run without the GitHub CLI, because their whole purpose is unreachable without it. A GitHub issue is
  one of three channels here, so a missing or unauthenticated `gh` is named with its specific remedy —
  install, versus `gh auth login` — and the run continues from a pasted description. What it never does
  is degrade into asking for a credential: a prompt that requests an API token is a phishing surface,
  and this one ships in a package.

  **It searches your prior analyses at intake, not at synthesis.** A recurrence surfaced after the
  document is written is a recurrence surfaced too late to change the analysis. Matches are made on
  implicated code, symptom, or root cause — never on title similarity — and the firing axis and the
  concrete overlap are always disclosed, so a spurious match costs one sentence to dismiss. Each of the
  earlier analysis's preventive actions gets a verdict of apparently completed, apparently not
  completed, or undeterminable, and **the first two require a citation**. `undeterminable` is the
  default, because an uncited "completed" against an action nobody finished makes a recurrence read as
  a fresh defect.

  **It refuses to call a layer-two finding a root cause.** Reading the code produces a specific failure
  mode a human interviewer does not have: the plausible path you find is genuinely there and genuinely
  related, which makes stopping feel like finishing. So every probe names its layer on the symptom →
  immediate cause → contributing factors → process gap → systemic cause ladder, and where the deepest
  validated finding is still an immediate technical cause, the run says so and names what would go
  deeper rather than promoting it under a "Root Cause" heading.

  **It writes two files and reads everything else.** The analysis and a rebuilt folder index, both under
  one directory, both as the run's final act — so an interrupted run consumes no sequence number and
  leaves nothing behind. The hypothesis tree, the issue trees, and the session notes are rendered in
  the conversation and never written to disk.

  Registered template: `defect-rca-template`. Override it for your whole team at
  `.specify/templates/overrides/defect-rca-template.md`.

## [1.14.0] - 2026-09-11

### Added
- **`speckit.spectra.test-plan` — the tests, agreed before anyone writes them.**
  Run it after `speckit.specify` and before the planning command, on one feature at a time. Hand it the
  path to a `spec.md` and it reads that specification, the constitution, the project's test strategy, the
  existing suite, and the source the feature touches, then writes one `test-plan.md` **beside the
  specification**: scope, risks, traceable test conditions, environment and data, and exit criteria. The
  document is circulated and approved; the planning command then designs around it.

  It is for teams that want the test set settled before the implementation is designed. It produces no
  tasks, writes no test code, and tracks nothing.

  What separates it from a template fill-in is the traceability, enforced in both directions. **Every
  acceptance criterion in the specification reaches at least one test condition, or is reported as
  uncovered with a reason** — never absent from both. **Every condition names what it verifies**, using
  the specification's own identifier (`FR-014`, `SC-003`, or the composed `US2-AC1` for an acceptance
  scenario), so a reviewer can check coverage in either direction without reading the code. The run states
  the count: criteria covered out of criteria found.

  Four decisions a reader would otherwise find surprising:

  **The specification path is required, and it is never inferred.** Not from the current branch, not from
  `.specify/feature.json`, not from modification times, not by scanning `specs/` — and it does not offer a
  picker either. With no argument it asks and stops, having read nothing. This is deliberately less
  helpful than the rest of the workflow, because the output is a document that gets circulated and signed:
  a plan generated against the wrong specification reads as authoritative and is undetectably wrong to
  whoever approves it. A picker is the same failure with extra steps.

  **The plan is written beside the specification, not under the artifact root.** No sequence number, no
  artifact subfolder. A test plan is *about one feature* and is consumed by the planning command, so its
  identity is the feature's directory — exactly as the specification and plan next to it carry no number,
  because the directory already supplies one. This is a documented reading of the convention's carve-out
  for Spec Kit's own locations, argued in `specs/021-test-plan-agent/plan.md`.

  **It carries no checkbox, in any section — exit criteria included.** It is approved, not tracked. An
  approved, circulated document with live checkboxes creates a second apparent source of truth about
  progress, and it will disagree with `tasks.md`. A checkbox reintroduced by a template override is
  rendered as a plain statement instead: the team's section is kept, only the construct goes.

  **The planning handoff is printed text, not a hook.** The run ends with a ready-to-copy invocation
  naming the written path. No `before_plan` hook is registered and no core command is edited, so the
  planning command works exactly as it does today for anyone who never installs this agent — which is
  what makes it genuinely optional.

  It inherits rather than invents. Level names come from `docs/test-strategy/TEST_STRATEGY.md` **verbatim**
  where one exists, so the two documents read against each other; otherwise from the constitution, else
  from convention — with `manual` always available, because a plan must be able to place a condition no
  automated lens will ever cover. A declared coverage floor is carried into the exit criteria and
  attributed, never adjusted. No level or tool is assigned that the project's manifests cannot support, so
  a command-line tool never gets a browser driver. Existing coverage is established by **reading test
  source, never running it**: a coverage claim cites the test file, and an absence claim cites the search.
  Where a requirement is too ambiguous to test, it says so and writes no condition — a fabricated
  condition would launder a guess into something a stakeholder approves.

  Risk ratings are derived from stated triggers rather than judged, capped at two to five rows, with
  `accept` a first-class response. Condition priority is inherited from the specification's own story
  priorities, with prohibitions and data-integrity properties promoted to P1 regardless. Re-running asks
  before rewriting, states what would change, and carries forward every explicitly-not-covered decision.
  One file per run. Nothing executed. No network request.

  Shaped by the new registered `test-plan-template`, overridable at
  `.specify/templates/overrides/test-plan-template.md`.

## [1.13.0] - 2026-09-10

### Added
- **`speckit.spectra.test-strategy` — the testing strategy a project inherits, decided once at the start.**
  Run it in the foundation phase, alongside the constitution, before there are features to plan. It reads
  the project, decides for itself whether this is a greenfield or a brownfield codebase, and writes one
  strategy covering unit, integration, API contract, and end-to-end testing plus a coverage floor — to
  `docs/test-strategy/TEST_STRATEGY.md`, or the project's declared artifact root.

  What separates it from a template fill-in is what it refuses to say. **Every recommendation either cites
  a path in the project or is explicitly marked as a convention with no project evidence** — never neither.
  **No tool is named that the stack cannot run**, ranked across three tiers: already in a manifest,
  ecosystem-standard for a stack the project demonstrably uses, or unverified and flagged as offered from
  frozen knowledge. That is why the end-to-end lens resolves to browser, HTTP, CLI, or *none* rather than
  defaulting to a browser driver — a published library gets `none`, which is the honest answer.
  **A claim that something is missing cites what was searched and where**, and the run always states how
  much of the repository it actually read.

  Three decisions a reader would otherwise find surprising:

  **The strategy is a singleton, rewritten in place.** Every other Spectra document agent numbers its
  output because it produces a series; this one produces a standing policy with exactly one current
  answer, like the constitution. The path is fixed so anything can link to it, and Git carries the
  history. This is a deliberate, documented departure from the artifact-numbering convention, argued in
  `specs/020-test-strategy-agent/plan.md`.

  **It never writes the constitution.** Not on approval, not on a re-run, not when the user insists. It
  detects whether the strategy is already embedded — quoting the governing clause where it is — drafts the
  exact amendment in the constitution's voice, takes the approval, records the text in the strategy
  document, and hands off to `speckit.constitution`, which owns the sync impact report, the bump-type
  judgement, and dependent-artifact propagation. One owner for every constitution edit.

  **It runs nothing unless you say so.** Coverage figures carry their provenance — `measured` only if it
  ran the tool this session after asking, `reported` (with the report's date) if it read a committed file,
  `unavailable` if there is nothing to read. That distinction is load-bearing, because in a brownfield
  project **the proposed floor is never above the baseline**: a floor that fails the next build gets
  deleted, and a deleted floor is worse than none. Where the floor is below the target, the ratchet is
  expressed as triggers rather than dates.

  It recommends configuration and never applies it: the exact CI or coverage change is stated for the team
  to make. Ten sections, overridable at `.specify/templates/overrides/test-strategy-template.md`.

## [1.12.1] - 2026-09-09

### Changed
- **The extension now points at `github.com/telus-digital/spectra`.** The repository moved from the
  `xavient` organisation to `telus-digital`, and the manifest's `repository` and `homepage` URLs moved
  with it — as did the links in the packaged `NOTICE` and `TRADEMARK.md`, the two files a consumer reads
  to find out who owns the work and where to raise an issue. No command changed: the roster, the
  templates, and the behaviour of every agent are identical to 1.12.0.

  The version moves because the packaged bytes did. GitHub keeps the old paths reachable with a rename
  redirect, so nothing breaks today — but that redirect holds only while the `xavient` organisation name
  stays unclaimed, and an install path resolving through a name anyone can register is not something to
  leave sitting in a shipped package.

## [1.12.0] - 2026-09-03

### Added
- **`speckit.spectra.impact` — a feature impact analysis a BA can take to a stakeholder gate.** Give it one
  paragraph describing what should be true after a feature ships, and it scans the project, works out what
  the change would touch, asks at most five clarifying questions about the things code cannot answer, and
  writes a numbered Markdown document under `docs/impact-analysis/` — or the project's declared artifact
  root. It runs *before* `specify`, because the point is to inform the go / no-go decision that authorizes
  development spend.

  What makes the output usable at a gate is what it refuses to do. **Every finding carries a
  `path/to/file.ext:142` citation and one of three confidence levels**, with the level fixed by the *kind* of
  evidence rather than by how convincing it felt — a document with no code citation never reaches
  `confirmed`. **The impact rating is a lookup, not a judgement**, derived from a defined trigger set and
  reported with the trigger that fired. **Absence of evidence is never reported as absence of impact**: "no
  consumers found in what was scanned" is permitted, "no downstream impact" is not. **Coverage is stated per
  system** — files read of files present, and by what method — alongside the terms that were searched for and
  produced nothing, so a reviewer can tell "I checked and found nothing" from "I did not check".

  Five bounded phases do the work — a structural map, term expansion across naming conventions, a
  role-weighted seed search, two-hop graph expansion, and two sweeps for the coupling static reading misses:
  dynamic dispatch, string-keyed registries, config-driven behaviour, and a raw-string sweep of every
  contract identifier (table and column names, endpoints, events, topics, config keys, flags, env vars)
  across the whole project. Each phase has a disclosed cap, overridable per run, and reaching one is
  reported rather than absorbed.

- **`impact-analysis-template`, the fifth registered template.** The document's ten sections resolve through
  Spec Kit's four-layer stack, so a team reshapes every future analysis by committing
  `.specify/templates/overrides/impact-analysis-template.md` — including deleting a section, which the
  command notes rather than reinstating. The trustworthiness rules stay with the command: an override can
  drop *Sources consulted*, and coverage is still reported in the session.

### Notes
Three decisions in this command are deliberate and worth stating, because each one is a capability someone
will look for and not find.

- **No network access, and no external repository fetching at all.** The command accepts no repository URL,
  credential, or token, and never clones or downloads anything — not even a public repo with `gh` already
  authenticated. Where a system spans more than one repository, the other systems are declared as free text,
  as a document, or as a **path to a local copy that is read in place** and never modified or copied. A
  system with no local checkout is *described* rather than searched, and still produces a targeted handoff
  item naming the owning team and the contract to confirm. Spectra opens no channel your agent does not
  already use, and this command holds that line rather than becoming the first exception.

- **No link to specifications, in either direction.** An impact analysis and a spec are independent
  processes. The document carries no `spec_refs` field, nothing under `specs/` is written or depended on, and
  `speckit.specify` is unchanged and unaware. Existing specs *are* read — as evidence, and they make the scan
  cheaper and better-oriented — but reading one creates no relationship to it, and a spec that disagrees with
  the code becomes a finding rather than a resolution.

- **The approval gate is manual.** Every run writes `status: draft`. The BA takes the draft to stakeholders
  and records the outcome in the front matter themselves; the command never sets, prompts for, or infers any
  other status. Because a human owns that field, the folder index is **rebuilt from the documents on every
  run** rather than appended to, so an approval recorded by hand reaches the index without the command
  touching a document to get it there.

Re-runs never overwrite. Every run allocates the next number — one greater than the highest present, not a
count of the files — and identical input twice produces two reports, each carrying its own timestamp and its
own verbatim record of what it was asked. An interrupted run leaves the folder untouched and consumes no
number, because the document and the index are written once, as the run's final act.

## [1.11.1] - 2026-08-31

### Added
- **`TRADEMARK.md` now ships inside the extension.** Apache-2.0 §6 withholds trademark rights, but
  until now the extension said nothing about which marks that covers. A consumer with only the
  installed package in front of them could see a permissive licence and a TELUS Digital logo in the
  same tree and reasonably conclude the logo came with the grant. `TRADEMARK.md` states what is
  excluded — the TELUS marks, "Spectra" as a project identifier, and the logo — and that a fork must
  rebrand. It sits beside `LICENSE` and `NOTICE` rather than only at the repository root, so the
  carve-out travels into every consumer's `.specify/` directory instead of dangling as a reference to
  a file they do not have.

### Changed
- **`NOTICE` carries the trademark carve-out, third-party attributions, and a regulatory
  disclaimer.** The attribution mechanics under §4(b) and §4(d) are unchanged; three sections are
  added on top. The third-party section names GitHub Spec Kit and reproduces the MIT permission
  notice verbatim, which the repository owed for the copies of Spec Kit's own `git` and
  `agent-context` extensions it carries; it also disclaims affiliation with AWS over the AI-DLC
  references, and with every standards body, regulator, and certification authority the agents name.
  The disclaimer says plainly what the compliance agents are: readiness-support tooling that produces
  drafts for human review, never certification or audit. `NOTICE` is the one file a downstream
  redistributor is required to carry forward, which makes it the right place for all of this.
- **The extension README's licence section states obligations rather than permissions**, and points
  at the shipped `TRADEMARK.md` and the disclaimer.

## [1.11.0] - 2026-08-26

### Added
- **`speckit.spectra.flaky-test-detector` — find the tests that pass and fail on the same code, then fix
  the ones you approve.** The conventional way to find a flaky test is to instrument CI, collect hundreds
  of runs, and compute a score: pipeline changes, a results store, and weeks of waiting before the first
  answer. This agent needs none of it. The causes are visible in the source — an unconditional sleep
  before an assertion, an un-awaited async call, state one test leaves for another, a live network call,
  an unseeded random value, an assertion against the real clock — so it reads the test suite and names
  them, on the day you install it.

  **It never runs anything.** Not the suite, not a build, not an install, and not to verify a fix it just
  applied. That last exclusion is deliberate: an agent that can run the tests it edited is an agent that
  can iterate until green, and iterating until green is how tests get weakened. Verification stays with
  you and your CI.

  **A fix removes the cause.** Deleting an assertion, loosening one until it always passes, skipping the
  test, marking it expected-to-fail, adding a retry wrapper, or lengthening a sleep are all forbidden as
  remedies. Edits are confined to test and test-support files; where the real fix belongs in application
  code, the item is left open with a note saying what would need to change and where.

  **Two gates, and pruning in between.** The run reports a ranked table — test, file, confidence, and a
  concrete fix — and stops. On your go-ahead it writes `.specify/memory/flaky-test-analysis.md`: a run
  summary, one `[ ]` row per candidate, the evidence behind each, and what it could not examine. You
  delete the rows you disagree with. On a second go-ahead it works what is left, one item at a time,
  ticking each `[x]` on disk as it lands — so an interrupted session leaves a file that is exactly true.
  Nothing is ever committed.

  **The list outlives the session.** Every run reads that file first and branches on its state: unfinished
  work resumes without re-analysing and without discarding your pruning; a completed list asks before it
  is replaced; a file it cannot parse is never overwritten silently. There is exactly one analysis file at
  any time. Before a run scoped to one suite replaces a broader plan, it names the pending items that
  would be dropped and waits.

  Confidence is High, Medium, or Low, and it rates the strength of the evidence rather than a failure
  rate — with no run history there is no denominator, so the agent emits no percentage or score. Your
  project's own constitution binds the choice of fix: where a guardrail rules out the only remedy, the
  item is left open with that rule named.

## [1.10.0] - 2026-08-22

### Changed
- **`speckit.spectra.review-pr` no longer looks for a spec in `.specify/feature.json`.** Spec Kit now gitignores
  that file — its own CLI writes the rule, describing it as "per-checkout state rather than something to share" —
  so the second tier of the spec-discovery chain read a path that, at a pull request's head revision, is either
  missing or stale. Missing was the common case and cost nothing but a wasted call. Stale was the dangerous one: a
  project that committed the file before Spec Kit began ignoring it still carries whatever feature its last
  committer happened to be on, so the review would check the diff against **someone else's spec** and report full
  traceability while doing it. That is the exact failure the chain's ban on branch-name guessing exists to prevent.

  The tier is now **a spec you name**. When the diff carries no spec, the command asks for one and reads the path
  at the pinned head revision, falling through to the standalone review if it does not resolve there. The addendum
  case — the spec merged in an earlier pull request — stays covered, on evidence a human vouched for rather than on
  a machine-local pointer. Both forbidden guesses are now named in the command, with the reason recorded, so
  neither comes back by accident.

  **The run still asks at most one question.** When neither a spec nor an issue was found, the existing single
  context question asks for both together; `--issue` answers only its own half, so a run with no spec in the diff
  still asks for the spec. Tier 1 is untouched: a PR that ships its spec behaves exactly as in 1.9.1, and a PR with
  no spec anywhere is still reviewed standalone — traceability reported as not run, guardrails at full strength,
  intent findings capped at Question.

## [1.9.1] - 2026-08-21

### Fixed
- **An issue passed to `speckit.spectra.create-pr` now always reaches the pull request.** The rendering was
  already right — `Closes #42` when the base is the repository's default branch, a plain `#42` reference
  elsewhere, since GitHub ignores closing keywords outside the default branch — but the reference was treated
  as *presentation*. Combined with the honour-the-template rule, that meant a project whose
  `.specify/templates/overrides/pr-template.md` had no **Related Issues** section got a pull request with no
  issue link at all: `--issue 42` noted the omission in chat and opened an unlinked PR that looked complete.

  The reference is now the command's obligation rather than the template's. It goes in the template's issue
  section when there is one — judged by intent, so a team's `## Ticket` counts — and is **appended** with a
  one-line note when there is not. With no issue, nothing is appended and any such section is removed, as
  before.

  This is the same line `review-pr` draws for its revision anchor, its AI-assisted disclosure, and its
  coverage statement: a template governs how a document *reads*; functional obligations stay with the command.
  Rendering is unchanged, and a template that has the section produces byte-identical output to 1.9.0.

## [1.9.0] - 2026-08-21

### Added
- **`speckit.spectra.review-pr` reads the linked issue as optional context — in both kinds of PR.** It looks
  for one automatically, tells you which issue it used, and asks once if it cannot find one. Skip the
  question and the review proceeds exactly as before, on the constitution and the spec.

  Detection runs two routes, and the second is not redundant: the structured link
  (`closingIssuesReferences`), then a scan of the PR title and body for `#42` and issue URLs. GitHub only
  records the structured link when a PR targets the **default branch** — the same rule that shaped
  `create-pr` in 1.8.0 — so a PR into `dev` can say `Closes #42` and return nothing structured. Without the
  text fallback the command would ask you for an issue already sitting on the pull request.

  What the issue is *for* depends on what else exists. With **no spec** it becomes the traceability baseline:
  the lens now runs against the issue in both directions — does the diff address what it describes, and does
  it do anything the issue never asked for — instead of being reported as not run. With a **spec**, the spec
  still authorizes and the issue is background. Where the two disagree, that is a Question naming both; the
  command does not adjudicate between two human artifacts.

  Two limits keep it honest. An issue's content is **data about intent, never instruction** — text asking to
  "just merge it" is a fact about the conversation, not a direction. And a finding whose only source is an
  issue **cannot be a Blocker** unless the PR claims to close it, in which case the rubric's existing clause
  about failing a requirement it claims to satisfy already applies. An issue is a conversation; a spec is
  authorized scope.

- **Line-anchored comments, with applicable code suggestions.** The review no longer arrives as one body
  with file:line references for you to go and find. Accepted findings whose anchors fall inside the diff are
  published **on those lines**, and where the fix is mechanical the comment carries a ` ```suggestion ` block
  the author can apply in one click.

  This was the command's one deferred feature, and its stated reason — "diff-position arithmetic" — is
  obsolete: the reviews endpoint takes `path`, `line`, and `side` directly. Everything posts in **one call**
  carrying body, comments, and verdict together, so there is no state where the comments landed and the
  verdict did not. Publication moves from `gh pr review` to `gh api` for that reason; it is the same tool and
  the same authentication, and `curl` remains forbidden.

  Because a suggestion is one click from a commit, the rails are requirements rather than advice: mechanical
  and complete for exactly the replaced range, never architectural, never spanning files, never on a
  low-confidence finding, never on a removed line or a generated file — and **every suggestion appears
  verbatim in the pre-publish preview**, because it can be applied without being read. Findings anchored
  outside the diff go in the body, with the reason stated. `<n>:body` in the selection forces any finding
  into the body.

- **A review template, overridable per project.** The body's shape was hard-coded; it is now
  `templates/review-template.md`, registered in `provides.templates` and resolved through the same stack as
  the ADR, BRD, and PR templates. It defines two shapes — the summary body and the inline comment — and the
  command reports which template path it used.

  Its remit is deliberately **narrower** than the other templates. Three things stay with the command and
  survive any override: the `<!-- spectra:review-pr revision=… -->` anchor (how `--since` and self-review
  detection find previous reviews), the AI-assisted disclosure line, and the **Coverage and limits** section
  that stops a review implying assurance it did not earn. Judgment is not overridable either — the severity
  rubric and its floors, the confidence cap, the anchor rule, the selection grammar, and the verdict
  derivation stay in the command, because two reviews of the same diff have to agree.

  The shipped default keeps today's sections and adds a **Summary**, with `- [ ]` task items on Blockers and
  Majors only. Ticking a Question means nothing, so Minor, Nits, and Questions stay plain bullets.

### Changed
- **Coverage now says how much of the constitution applied**, not merely that the guardrail lens ran. A
  review reporting "guardrails: run" against three vague principles looks thorough and is not. It states how
  many principles were read and how many bore on this diff, says so plainly when none did, and names the
  domain-analyzer and constitution commands as the way to close that gap. An absent constitution is stated
  rather than implied.
- Coverage also records **which context authorized the review** — spec and discovery tier, issue with number,
  title and state, constitution, or the absence of each — and **what could not be placed inline**.
- The summary gained an **Issue status** line: the issue, its state, and how it was obtained.

## [1.8.0] - 2026-08-21

### Added
- **`speckit.spectra.create-pr` takes an optional `--issue`.** Pass a number or a URL (`--issue 42`,
  `--issue https://github.com/owner/repo/issues/42`) and the PR links to it. Omit it and the command asks once;
  skip the question and the PR is opened with no issue section at all. A reference that `gh issue view` cannot
  resolve is reported and dropped rather than written into the body broken.

  **The link is written differently depending on the base branch, and that is not cosmetic.** GitHub interprets
  closing keywords *only* when a PR targets the repository's default branch — on any other base the keywords are
  ignored, no link is created, and merging closes nothing. So a `Closes #42` on a PR into `dev` would look
  correct and do nothing. The command writes a closing keyword only when the base is the default branch;
  otherwise it writes a plain `#42` reference, which still records a cross-reference on the issue, and tells you
  auto-close will not happen on this merge. An issue in another repository is referenced by full URL, never with
  a keyword.

- **The PR body now comes from an overridable template.** `templates/pr-template.md` ships with the extension,
  is registered in `provides.templates`, and resolves through the same stack as the ADR and BRD templates:
  project override → presets → extension → core → an inline skeleton. Drop
  `.specify/templates/overrides/pr-template.md` into your project and every PR follows your structure —
  committed, team-wide, and surviving extension updates.

  Sections: Summary, Related Issues, Type of Change, Changes, How to Test, Screenshots / Evidence, Breaking
  Changes, Notes for Reviewers. **Deliberately no self-certification checklist** — an agent cannot honestly tick
  "I have self-reviewed the full diff". If your override reintroduces one, the command leaves those boxes
  unchecked and says it left them for you.

- **One final confirmation before anything is created.** The command summarizes source → base and where the base
  came from, the linked issue or nothing, draft or ready, the resolved template path, and anything it has
  already done — then asks once. Confirmations that used to be scattered now happen in one place.

### Changed
- **Uncommitted work is offered a commit instead of a warning.** Previously the command surfaced a dirty tree,
  warned that the PR would exclude it, and explicitly would not commit. It now lists the files and asks *"there
  are uncommitted changes, should I proceed with committing and pushing first?"* — and on a yes behaves like any
  ordinary commit-and-push request. Rails: the file list is shown before staging, credential-shaped names
  (`.env`, `*.pem`, `id_rsa`, `credentials*`) are called out for a specific go-ahead, nothing is blind-`git
  add -A`'d beyond what you saw, and `--no-verify` is never used — a hook that rejects the commit stops the run
  with the hook's own message. Answer no and the PR is opened from committed work with the exclusion stated
  plainly.

  This widens the command's write scope, which is worth saying out loud: it may now create a commit on your
  behalf, with your explicit consent, in addition to pushing and opening the PR. It still never edits source,
  the spec, the plan, the tasks, or the constitution.

- **The base branch: documented intent wins, and a guess is confirmed rather than assumed.** A promotion flow in
  the constitution or `.specify/extensions/git/git-config.yml` is used and cited, as before. With nothing
  documented, the command proposes a base — the branch this one appears to have been cut from, else the default
  branch — and asks at the final gate: *"This PR will be created to merge into `main`. Is that correct?"* You can
  redirect it in the same breath, and the corrected base is re-checked on the remote before use.

  The reason it asks rather than decides: **Git records no parent branch.** `@{upstream}` is the tracking branch,
  and `git merge-base --fork-point` reads the reflog, so it yields nothing in a fresh clone or CI checkout and
  nothing useful when two candidates share a commit.

- **It works from any branch now.** The one-branch-per-spec refusal is gone: a `fix/…` or chore branch can open a
  PR. Only two refusals remain — detached HEAD, and a branch that is already the resolved base. A spec branch is
  still better served: it contributes `spec.md`, `plan.md`, and `tasks.md` to the body, where other branches
  contribute their commits. Either way the **Changes** section comes from the real diff
  (`git diff --name-status <base>...HEAD`), not from a restatement of the plan.

- Constitution **1.7.1** clarifies Principle VIII: a deliverable is the document, not the destination, so a PR
  body a command emits is shaped by a template exactly as a file written to disk is. Only Principle VII's
  *location* rules are limited to files.

Every earlier guarantee is intact: the hard `gh` gate before anything else, GitHub-only scope, the duplicate-PR
check, `--head` always explicit, `--body-file -` for the body, and post-gate degradation that states exactly what
was mutated.

## [1.7.0] - 2026-08-21

### Added
- **Both document agents are now driven by an overridable template.** `speckit.spectra.adr` used to carry its
  structure as a literal block inside the command file — there was no file to change. It now ships as
  `templates/adr-template.md`, alongside the BRD template, and both are declared in `extension.yml` under
  `provides.templates`.

- **`.specify/templates/overrides/<name>.md` is the supported way to customize them.** Drop
  `.specify/templates/overrides/adr-template.md` (or `brd-template.md`) into your project, edit it, commit it —
  every document produced from then on follows your structure, on every teammate's machine. Add the sections
  your governance needs, or delete ones you don't want.

  Both commands now resolve their template through Spec Kit's stack, first usable layer wins: project override
  → installed presets → this extension → core `.specify/templates/` → the command's inline skeleton as a last
  resort. A layer that exists but is empty or unreadable is reported and skipped rather than being fatal.

  **This is the part that was broken before.** `brd` read the extension's copy at a hard-coded path, so an
  override was silently ignored, which left editing the installed copy as the only lever — and that edit does
  not survive: extension files are replaced wholesale when the extension updates. Because the path is tracked
  by Git, the edit looks durable and then reverts later inside an unrelated diff. An override lives outside the
  extension tree and survives.

- **Each command reports which template it used**, by path. An override that silently failed to apply
  otherwise looks exactly like one that worked, and the first clue would be a wrongly-shaped document.

### Changed
- **A resolved template is honoured, not repaired.** If your override renames, renumbers, drops, or adds
  sections, the command follows *your* structure and mentions once what it left out, instead of quietly
  reinstating it. Where your template adds sections, they are filled from the same gathered context; where
  there is genuinely nothing to say, the command says so rather than inventing content.

- **The ADR's section list is unchanged**: Context, Decision, Consequences, with the same `Date` and `Status`
  header. With no override in place, output is structurally identical to 1.6.0. Enriching the default was
  deliberately left out of this release — now that every project can add sections itself, changing the shipped
  default would have altered everyone's output while claiming to be additive.

- Constitution **Principle VIII — Documents Are Shaped by Overridable Templates** (constitution 1.7.0) records
  the rule so future document agents inherit it: the structure comes from a registered template resolved
  through the stack, with an inline fallback and never a hard-coded path; the resolved template is honoured as
  authored; the command names the template it used. Resolution stays prompt-expressed, because calling Spec
  Kit's Bash `resolve_template()` would break agent-agnosticism and shipping a resolver of our own would break
  the Markdown-only guarantee — the package still contains no scripts, no binaries, and no hooks.

## [1.6.0] - 2026-08-21

### Changed
- **ADRs and BRDs now go to one place: `docs/adr/` and `docs/brd/`.** `speckit.spectra.adr` used to write
  `Docs/ADR/ADR-NNN-*.md` and `speckit.spectra.brd` used to write `/brds/NNN-*.md` — two different parent
  folders, two different capitalizations, and one path that named the filesystem root rather than the
  project. Both now write under a single root, project-relative and lowercase, one subfolder per artifact
  type. Filenames are unchanged: `docs/adr/ADR-NNN-<title>.md` and `docs/brd/NNN-<title>.md`. The root
  itself is a project setting — see **Added** below.

  The lowercasing is a fix, not a preference. `Docs/ADR/` is a distinct directory on Linux but silently
  aliases into an existing `docs/` folder on a case-insensitive macOS filesystem, so the same command
  produced different layouts on different machines.

- **Existing projects keep their numbering, and their old folder.** Both commands still read the earlier
  locations — `Docs/ADR/` (matched case-insensitively), `brds/`, and `docs/<artifact>/` when a project
  declares a different root — for context and for the next number, so the sequence after this update
  continues from the highest artifact found across old and new instead of restarting at `001`. Those folders
  are read-only to the agent: it reports them once, offers a `git mv` you can run, and moves nothing itself.
  If a new ADR supersedes one that still lives in an earlier folder, the supersession is recorded in the new
  ADR and reported to you rather than written into the old file.

- **Every write scope is unchanged in size.** `brd` still writes exactly one file; `adr` still writes one
  ADR plus, only with your agreement, the superseded-status line and a constitution edit.

### Added
- **A project can move the artifact root with one line.** `docs/` is the default, not a hard-coded path.
  Put this in `.specify/memory/constitution.md` and every Spectra document agent — these two and every one
  we ship later — writes there instead:

  ```text
  Artifact root: documents/
  ```

  The commands offer that line but never write it themselves: producing a document is not a licence to edit
  governance.

- **A publication check before defaulting into `docs/`.** `docs/` is GitHub Pages' only non-root branch
  source and the default source directory for MkDocs and Docusaurus, so on some projects writing there
  publishes the document or breaks a docs build. Both commands now look for that signal — `mkdocs.yml`,
  `docusaurus.config.*`, `docs/_config.yml`, `docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, or a Pages
  configuration pointing at `docs` — and when they find one with no declared root, they say so before
  writing, recommend `documents/`, and ask. Unanswered, they take the non-publishing option: a misplaced
  private file is one `git mv` away, while a BRD served on the public web cannot be recalled from caches or
  forks. The question does not count against either command's five-question limit, because it is about
  where to write rather than what to record.

- **Constitution Principle VII — Document Artifacts Live Under One Declared Root** (constitution 1.6.0).
  Every command producing a durable Markdown deliverable writes it to `<artifact-root>/<artifact>/` with a
  lowercase kebab-case slug, one artifact type per folder, three-digit numbering. Spec Kit's own
  `.specify/` and `specs/` are carved out, so `speckit.spectra.domain-analyzer` writing
  `.specify/memory/domain-analysis.md` stays compliant — that is context for another command, not a
  deliverable. The point is forward-looking: the roster has a dozen more document producers under
  development, and each one now inherits its output location instead of choosing a new top-level folder.

## [1.5.0] - 2026-08-19

### Changed
- **`speckit.spectra.create-pr` now hard-stops when `gh` is missing or unauthenticated**, instead of
  degrading to a printed manual fallback. The check runs as the first thing after you accept the offer —
  before the constitution is read, before a target branch is derived, before any `git` command — and it
  names which of the two failed, because the remedies differ: install the GitHub CLI, or run
  `gh auth login`. Nothing is mutated on that path, and when `gh` is absent the message no longer prints
  a `gh` command line; the only alternative it names is the GitHub web interface.

  This **reverses the difference recorded in 1.4.0**, where `create-pr` degrading was described as a
  deliberate contrast with `review-pr`. That justification does not survive contact with the two
  failures it was meant to serve. The printed fallback told the user to run `gh pr create` — the command
  they demonstrably did not have — and the duplicate-PR check is itself a `gh` call, so a run without
  `gh` could walk them into a second pull request for a branch that already had one. Both GitHub
  commands now gate identically. What differs is only what each hands over *after* the gate.

- **A refusal after the gate now degrades properly, and says what it changed.** A protected base branch,
  a token without push permission, or a fork restriction is reported with the underlying `git`/`gh`
  message, the manual commands including the derived base branch — runnable, because `gh` is present
  here — and, critically, the mutation state: *nothing reached the remote*, or *the branch is on the
  remote and no pull request exists*. The command previously had no instructions for this case at all,
  even though by then it may already have pushed.

- **A remote that is absent or not on `github.com` is now a stop with a scope statement**, not a
  degradation, and prints no `gh` fallback — there is nothing `gh` can do with a GitLab remote. GitHub
  Enterprise is named as out of scope rather than half-attempted.

- **The pull request body is passed on standard input** (`--body-file -`) rather than as a
  command-line argument, so spec prose carrying backticks, code fences, quotes, and blank lines reaches
  the pull request unaltered. `review-pr` already published review bodies this way.

- **Fork detection is read from the repository, not guessed from the URL.** One
  `gh repo view --json nameWithOwner,isFork,parent,defaultBranchRef,viewerPermission` call replaces the
  previous "if `origin` looks like a fork" heuristic *and* the separate default-branch lookup. Forks and
  multi-remote setups are still resolved by asking, and now for a stated reason: `gh pr list --head`
  rejects `<owner>:<branch>` while `gh pr create --head` accepts it, so an inferred fork flow would
  check for duplicates against one head and open against another.

- **`gh` is declared as the only route to GitHub** in the command's governing rule — no `curl`, no
  direct REST calls — matching `review-pr`.

`gh` remains **optional at the extension level**: `adr`, `brd`, and `domain-analyzer` never touch
GitHub, so requiring it would block installation for users who only want those.

A command changed behaviour, no argument or output contract did, which is why this is a MINOR.

## [1.4.0] - 2026-08-17

### Added
- **`speckit.spectra.review-pr` — a reviewing agent for the last manual gate in the lifecycle.** It
  reviews a GitHub pull request against **the intent and standards the PR carries**: the spec, plan,
  tasks, and ADRs read at the PR's own head revision, plus the constitution and ADRs in force on the
  **base** branch. That is what lets it report a task marked complete but absent from the diff, scope
  no requirement authorized, or a pattern an ADR forbids — none of which a diff-only reviewer can see.

  Two properties define it:

  - **Every finding is anchored and sourced.** A file, a line, and the clause, requirement id, or named
    principle it rests on. A finding that cannot be anchored and sourced is not reported at all.
  - **The human is the filter.** Nothing is pre-selected. The reviewer chooses which findings are
    published and which verdict to submit, sees the exact body first, and gives a final go-ahead before
    anything is posted. An empty selection posts nothing and is a normal outcome. Approving over a
    blocker the reviewer accepted requires a typed confirmation and is recorded in the published review.

  Findings are graded Blocker / Major / Minor / Nit / Question from a fixed rubric so repeated reviews of
  one revision agree, with floors that keep an explicit constitution violation at Major or above and an
  explicit compliance violation at Blocker. Low confidence cannot be a Blocker — it becomes a Question.

  Publication is a single review event through the reviewer's own `gh` authentication. The agent holds no
  credentials, adds no data path, and stores nothing between runs.

  Two behaviours differ from `create-pr` on purpose:

  - **It hard-stops when `gh` is missing or unauthenticated** rather than degrading, because a review's
    value is the analysis and the analysis needs the PR. Failures *after* that gate — a fork
    restriction, insufficient permission — still degrade gracefully to a rendered body for manual
    posting.
  - **It registers no hook.** Review is on demand only, since the reviewer should not be the author.

  GitHub only in this release, and single-body reviews only — line-anchored inline comments are a
  follow-on.

A command was added, which is why this is a MINOR.

## [1.3.1] - 2026-08-09

### Changed
- **The extension description is now the positioning line used everywhere else:** "TELUS Digital -
  Agentic software engineering across the entire SDLC." It previously enumerated the four shipped
  commands, which meant it needed editing every time an agent was added and disagreed with the
  wording on the landing page and in the README. One line, one place, no drift.
- **The Commands table in `README.md` is generated** from the new root `agents-list.json` roster
  rather than maintained by hand. The region is marked with
  `<!-- SPECTRA:GENERATED START id=spectra-readme-commands -->`; everything around it, including the
  four per-agent sections, stays hand-written. Its Effect column is dropped — `effect: read-write` is
  declared once for the extension in `extension.yml`.
- **The PR agent is titled "GitHub (PR)" everywhere.** It previously appeared as `github`, GitHub,
  GitHub (PR), and "GitHub PR delivery" across four documents. Its command is unchanged:
  `speckit.spectra.create-pr`.

No command was added, changed, or removed, which is why this is a PATCH.

## [1.3.0] - 2026-08-08

### Changed
- **Relicensed from MIT to the Apache License 2.0.** Spectra stays free to use, modify, and
  redistribute for any purpose, including commercially. Apache-2.0 adds an explicit patent grant and
  makes attribution enforceable: redistributions and derivative works must retain the copyright
  notice, ship the `LICENSE` and `NOTICE` files, and state which files were changed
  (§4(b)–4(d)).

### Added
- `NOTICE` — the attribution notice that downstream redistributors are required to carry forward
  under Apache-2.0 §4(d). It now ships inside the extension package.

## [1.2.0] - 2026-07-14

### Added
- **`speckit.spectra.brd`** — a Requirements & Discovery-phase command that transforms a raw business
  requirement (inline text or a `.docx`/`.pdf`/`.md`/`.txt` document) into a structured,
  specify-ready BRD written under `/brds`. It reads project context to ground the document, asks up to
  five clarifying questions only when the requirement has material gaps, never invents requirements
  (genuine unknowns become Open Questions), and hands off to the Spec Kit **specify** command. Its only
  write is the BRD file.
- Bundled the canonical BRD template as `templates/brd-template.md` so the command produces the same
  structure in any installed project.

## [1.1.0] - 2026-07-09

### Changed
- Consolidated the previously separate `adr`, `domain-analyzer`, and `github` extensions into a
  single `spectra` extension. Every capability is now a command under the unified `speckit.spectra.*`
  namespace, matching Spec Kit's `speckit.<extension-id>.<command>` rule (the extension `id` is
  `spectra`):
  - `speckit.adr.new` → `speckit.spectra.adr`
  - `speckit.domain-analyzer.analyze` → `speckit.spectra.domain-analyzer`
  - `speckit.github.create-pr` → `speckit.spectra.create-pr`
- Install once with `specify extension add spectra` to get all three commands. The `after_implement`
  hook now invokes `speckit.spectra.create-pr`.

### Commands
- **`speckit.spectra.adr`** — Create a context-aware Architecture Decision Record grounded in the
  codebase, prior ADRs, and the project constitution; asks up to five clarifying questions and writes
  the ADR under `Docs/ADR/`.
- **`speckit.spectra.domain-analyzer`** — Infer the project's business domain and write an opt-in
  proposal of evidence-backed candidate guardrails to `.specify/memory/domain-analysis.md` for SME
  review and handoff to `/speckit-constitution`. Never edits the constitution or source.
- **`speckit.spectra.create-pr`** — Offer to open a correctly-targeted GitHub PR for the current spec
  branch after `implement`, deriving the base branch from the promotion strategy, confirming before
  any push, and returning the PR URL — with a graceful manual fallback when `gh`, the remote, or the
  network is unavailable.
