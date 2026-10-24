# Research: Engineering Methodology Agent

No Technical Context item was left as NEEDS CLARIFICATION. The decisions below settle design questions the spec
left open, and the three boundary conflicts planning surfaced (R3–R5).

## R1 — Command, file, and template names

- **Decision**: command `speckit.spectra.methodology`, file `spectra/commands/methodology.md`; template
  `engineering-methodology-template`, file `spectra/templates/engineering-methodology-template.md`; output
  `<artifact-root>/ENGINEERING_METHODOLOGY.md`; roster id `methodology`, title "Methodology Analyst", phase
  `foundation`, type `add-on`, description "Find, choose, and record the team's engineering methodology —
  spec-driven by default, with test-first or behaviour-first as binding phase obligations — and hand it to the
  constitution."
- **Rationale**: the command name was agreed with the user. Principle VIII names a template
  `<artifact>-template.md`, and the artifact is the engineering methodology. The uppercase filename matches the
  other singletons and the name teams already use for a hand-written methodology, so such a team's existing
  file is already at the canonical path.
- **Alternatives**: `methodology-template` (rejected: it doesn't match the output name);
  `docs/methodology/001-…` (rejected: a standing policy is a singleton under Principle VII).

## R2 — The question round

- **Decision**: ten fixed questions, one per turn, numbered "Question N of 10", announced once with the ways out:

  | # | Asks | Shape |
  |---|---|---|
  | 1 | Methodology stack: which overlays to adopt on top of SDD | options: Recommended stack / Codify only what is practised / No overlays (SDD only) / Skip |
  | 2 | Strictness and scope of each adopted overlay | one table, a row per overlay; options per FR-021a; a confirmation when none is adopted |
  | 3–8, 10 | Lenses 2–7, 9 | domain-analyzer's four-option lens shape: Recommended set / Codify only what exists / Full set / Skip, with "Choose individually" replacing a duplicate |
  | 9 | Lens 8: AI collaboration | **Every phase a human checkpoint** (recommended) / **Human gates at spec approval and PR review** / **Autonomous to PR** / Skip. The lens's tools and secrets candidates are listed above the options and ride with the chosen level unless free text excludes them; Skip adopts nothing from the lens |

  Mode is stated, and corrected when mixed, before the round and outside the count. An unanswered or skipped
  question adopts nothing. "Use your defaults" takes every remaining recommendation as `default_taken`. In
  greenfield mode, "Codify only what exists" has nothing to take, so it is replaced by "Choose individually".
- **Rationale**: a fixed count is what lets the round be announced honestly (spec 034, R2). A single overlay
  table keeps the count fixed (Clarification 5). Question 9 gets its own shape because the autonomy levels
  exclude each other, so the generic "Full set" would adopt all three at once (analyze H3).
- **Alternatives**: per-overlay questions (rejected in Clarification 5); one question per lens with the stack
  folded into lens 1 (rejected: strictness and scope are a separate decision and would crowd lens 1's options).

## R3 — The boundary with `deployment-strategy` (spec reconciliation)

- **Finding**: `deployment-strategy`'s *Release & versioning* lens already decides "the branching model, how a
  release is cut, the versioning scheme, the hotfix path" (`deployment-strategy.md:125`). The spec gives the
  branching model to lens 5 and the versioning scheme to lens 7, so as written both agents would propose both.
- **Decision**: split by what the clause governs.
  - **Methodology** owns how work integrates: branching model, branch naming by change type, branch
    lifecycle, merge strategy (lens 5), and commit convention and changelog (lens 7). It also owns hotfix *as
    a change type* in the mode-choice table (lens 2): whether a spec is needed, its branch prefix.
  - **Deployment** keeps how work ships: how a release is cut, the **versioning scheme**, and the hotfix
    *promotion* path. Its *Release & versioning* lens stops proposing the branching model and cites
    `ENGINEERING_METHODOLOGY.md` for it (or names `speckit.spectra.methodology` when absent).
- **Rationale**: versioning is read by release tooling and promotion gates, which deployment already owns. The
  branching model is the first thing a new engineer needs from an onboarding methodology. Moving one clause, the branching
  model, is the smallest edit that leaves one source per clause.
- **Alternatives**: leaving branching with deployment (rejected: it contradicts the agreed lens 5 and leaves a
  methodology document without its branching section); methodology owning versioning too (rejected: a second
  shipped agent would have to give up a clause it already hands to the constitution).
- **Spec effect**: FR-018 gains "versioning scheme and release cut → deployment-strategy"; lens 7 narrows to
  commit convention and changelog; FR-019's edge change is joined by a deployment-strategy one. The user
  confirms this before `/speckit-tasks`.

## R4 — `kb-vault` routing (spec reconciliation)

- **Finding**: `kb-vault` classifies an absorbed methodology document as category `engineering-methodology`
  and writes a series file `<root>/engineering-methodology/NNN-….md`. Its reserved map has rows for the other
  singletons but none for this one.
- **Decision**: add a reserved-map row: "an engineering methodology" → `<artifact-root>/` →
  `ENGINEERING_METHODOLOGY.md` → `engineering-methodology-template`. Update the plan-table example in
  `kb-vault.md` so it no longer shows the series path. A file `kb-vault` writes there carries no
  `speckit.spectra.methodology` front matter, so the next methodology run reads it as evidence of current
  practice (R13), not as a prior analysis. Say so in one sentence under the reserved map.
- **Decision (fourth clarify session, FR-019)**: the converse is guarded. When the file at that path carries
  `command: speckit.spectra.methodology` front matter, a match against it does not produce an **update** row.
  The row becomes a referral: the file is left unchanged, `/speckit.spectra.methodology` is named as the way to
  fold the content in, and the source is listed under a new Step 12 report item, "Sources referred on". A file
  without that front matter keeps kb-vault's existing update rules.
- **Rationale (guard)**: kb-vault's update path edits in place and follows the document's shape, but it does not
  maintain command front matter or frozen `em-` IDs. One edit would turn the agent's file into one the next run
  reads as hand-written (R13), losing every prior decision.
- **Rationale**: the reserved map exists so that "a supplied PDF … would [not] land in a folder of its own beside
  the one [another agent] maintains" (`kb-vault.md:294`). The same failure applies here.
- **Alternatives**: none viable. Without the row, two methodology documents exist and neither knows of the other.

## R5 — `review-pr` as the first reader (spec reconciliation)

- **Decision**: add `ENGINEERING_METHODOLOGY.md` to `review-pr`'s T2 standards table (no legacy location), with
  the rule "only accepted guardrails are standards", worded like its domain-analysis paragraph.
- **Rationale**: branch naming, PR gates, and commit conventions are exactly what a PR review checks. FR-034
  needs a reader to bind. Without one, the methodology would be enforced only at plan time.
- **Alternatives**: deferring to a later feature (rejected: the document would be produced but never consulted
  at review, which is where most of its lenses apply).

## R6 — Mode detection

- **Decision**: the three signals and thresholds from Clarification 3.
  - *Source beyond scaffolding* means at least one source file with more than 20 non-blank lines that has been
    changed in more than one commit, or at least five such files when the history has at most one commit (including no history) (FR-002). A codebase imported as one squashed commit
    therefore still has this signal.
  - *Workflow configuration* means any of `.github/workflows/*`, `.gitlab-ci.yml`, a PR or MR template,
    `CODEOWNERS`, `CONTRIBUTING.md`.
  - *Commits* means `git rev-list --count HEAD > 10`.

  A repository that is not a git repository has signal (c) absent and says so.
- **Rationale**: no single signal is reliable (squashed imports, starter templates). The thresholds are simple
  enough to state in prose and to cite in the first output.
- **Alternatives**: a weighted score (rejected: it can't be explained in one line).

## R7 — Overlay obligations and their evidence

- **Decision**: the command carries a fixed obligations matrix, one row per offered overlay, and only the cells
  below may become clauses. "Evidence" is what a reviewer checks.

  | Overlay | specify | plan | tasks | implement / evidence |
  |---|---|---|---|---|
  | TDD | — | names the test approach per story | test task precedes and blocks each implementation task it covers | test task records a failing run before its implementation task is ticked; a fix starts with a failing regression test |
  | BDD/ATDD | acceptance criteria in Given/When/Then are binding | maps scenarios to executable specs | one task per scenario, before its step code | scenario recorded failing, then passing |
  | DDD | uses the domain's ubiquitous language; undefined terms flagged | names the bounded context touched | — | no cross-context dependency outside agreed seams (contexts defined by the domain analysis) |
  | Contract-first | — | contract written before handlers | contract task precedes implementation | implementation conforms to the committed contract |
  | ADR-driven | — | a significant decision cites or creates an ADR (`speckit.spectra.adr`) | — | — |

  Strictness (`MUST`/`SHOULD`) and scope (change types, optional modules) from question 2 are applied to every
  cell of an adopted row. An adopted overlay becomes **one** candidate guardrail in lens 1, `em-overlay-<name>`,
  whose statement lists its obligations phase by phase. Lens 1 therefore holds at most five candidates, one per
  overlay, within FR-008. A team may name another overlay in free text; it is accepted only if the team states
  at least one phase obligation for it.
- **Rationale**: Clarification 1 (`tasks.md` evidence). A closed set of cells keeps the agent from inventing
  slogans (FR-014).
- **Alternatives**: free-form obligations per run (rejected: they can't be tested, and they drift between runs).

## R8 — The domain-analyzer migration

- **Decision**: `domain-analyzer` loses lens 7 (6 lenses, 7 questions, "Question N of 7"). Its referral rule
  gains `speckit.spectra.methodology` beside test- and deployment-strategy. On re-run, prior Delivery & workflow
  records are kept in *Decisions and sources* under "Handed on to `speckit.spectra.methodology`", with their
  IDs and decisions unchanged, and leave the Constitution input section. `methodology` reads them from
  `DOMAIN_ANALYSIS.md`:
  - **accepted** becomes the prefilled proposal in the matching lens;
  - **declined** is never re-offered as new;
  - **adopted** stays adopted.

  Carried-over records keep their `da-` IDs (R11).
- **Rationale**: FR-020, and "never delete a prior candidate" (spec 034 FR-019).
- **Alternatives**: deleting prior lens-7 records (rejected: it loses an SME's decisions); leaving them active in
  the domain analysis (rejected: it leaves two sources).

## R9 — Section mapping

- **Decision**: where a constitution exists, its own section names are used. Otherwise:
  - lens 1 → Core Principles;
  - lenses 2–7 → Development Workflow;
  - lens 8 → Additional Constraints;
  - lens 9 → Governance.

  Lens 9 reports the existing Governance section as current practice and proposes nothing it already asserts.
- **Rationale**: Spec Kit's default constitution headings; matches the domain analyzer's mapping style.

## R10 — The constitution amendment

- **Decision**: MINOR 1.12.0 → 1.13.0. Add `<artifact-root>/ENGINEERING_METHODOLOGY.md`
  (`speckit.spectra.methodology`) to Principle VII's list of singletons, change "the three shipped singletons" to
  four, and add a Sync Impact Report. The user runs it with `/speckit-constitution`. Tasks provide the
  ready-to-paste prompt and order it before the singleton test is extended.
- **Rationale**: Principle VII: "A new singleton MUST be named in this paragraph by amendment; a command MUST
  NOT declare itself one." The agent's own FR-032 also forbids it from editing the constitution, which is
  consistent.

## R11 — Candidate IDs

- **Decision**: `em-<lens-slug>-<hash>`, where the hash covers the lens and the normalised statement, computed
  once and frozen. Overlay rows use `em-overlay-<name>`. Records carried over from the domain analyzer keep
  their `da-` IDs. Re-runs match by ID, then by same intent within the same lens.
- **Rationale**: mirrors the domain analyzer (spec 034 FR-018), so `review-pr` and future readers parse both
  the same way.

## R12 — The onboarding body

- **Decision**: the template's body sections, in order:
  1. Overview (mode, goal, stack in one paragraph)
  2. Methodology stack and obligations matrix
  3. Work modes (mode-choice table, spikes)
  4. Requirements intake
  5. Spec lifecycle & traceability
  6. Branching & integration (branch-naming reference)
  7. Review & merge gates
  8. Change records (commit-prefix reference)
  9. AI collaboration (autonomy level, tools, secrets)
  10. Governance & evolution
  11. Related strategies: one line each linking `DOMAIN_ANALYSIS.md`, `TEST_STRATEGY.md`, `DEPLOYMENT_STRATEGY.md`, or naming their commands
  12. Constitution input
  13. Decisions and sources

  Each lens section opens with *Current practice* (brownfield) or *Starting point* (greenfield), followed by
  its candidate records. Organisation-specific facts (internal URLs, BA tools) appear only when the team
  supplies them in free text.
- **Rationale**: this follows the order of a typical onboarding methodology: how work arrives, how it is
  classified, how it moves through branches and review, and how the rules change. Environments and coverage,
  which hand-written methodologies often keep inline, become one-line links, which is what FR-018 requires.

## R13 — A hand-written file already at the canonical path

- **Finding**: teams often already keep a hand-written `docs/ENGINEERING_METHODOLOGY.md`. It has no
  command-owned front matter, so a re-run cannot treat it as a prior analysis, and rewriting it in place would
  destroy hand-authored content.
- **Decision**: a file at the canonical path without `command: speckit.spectra.methodology` front matter is read
  as **evidence of current practice**, cited per lens like any other document. Before the round, outside the ten
  questions, the agent says it will replace the file (Git keeps the old version) and asks for consent. If the
  team declines, or the run is non-interactive, it writes nothing and shows the document in the session, with a
  note that the existing file was left unchanged. No second file is ever written.
- **Rationale**: Principle VII allows the command exactly one file and no writes anywhere else, and a singleton
  "MUST NOT create a second one". Showing the document in the session is the fallback the agent already uses
  when the file cannot be written, so nothing new is introduced.
- **Alternatives**: overwrite silently (rejected: it loses hand-written content); refuse to run (rejected: a team
  with its own methodology is exactly the team this agent is for); a `.proposed` staging file beside it (rejected by `/speckit-analyze` C1:
  it is a second file in the artifact root, which Principle VII forbids).
