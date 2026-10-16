# Research: What a Review Is Measured Against

Each item below records a decision, its rationale, and the alternatives considered. Line numbers refer to
`spectra/commands/review-pr.md` at 1.21.0.

## R1 — Where the standards chain is read and applied

- **Decision**: The chain is *read* in Step 4, next to the constitution, and *applied* in Step 5 Guardrails.
  Every T1 and T2 document is read at `baseRefOid`. T3 conventions are observed in the patch's context lines and in
  neighbouring files read at `baseRefOid`. A convention the PR itself introduces isn't yet the codebase's. The B1–B7 table lives in Step 5.
- **Rationale**: Step 4's revision table (`:236`) already encodes the rule "standards come from where the
  change is going". Supporting docs are standards, so they belong in the same table at the same revision. That
  also makes FR-007 (a PR editing a supporting doc is a governance change) the same mechanism as the ADR rule.
- **Alternatives**: a new standalone step. Rejected, because it would split "what revision" from "what document"
  and duplicate the absent/unreachable rule.

## R2 — Locating supporting documents

- **Decision**: Resolve the artifact root exactly as `test-plan` does (`test-plan.md:167–173`). Use an
  `Artifact root:` line in the constitution, matched case-insensitively. Otherwise use `docs/`, which is also
  the root when there is no constitution at all. Then read, at `baseRefOid`:
  - `<root>/TEST_STRATEGY.md`, falling back to `<root>/test-strategy/TEST_STRATEGY.md`
  - `<root>/DEPLOYMENT_STRATEGY.md`
  - `<root>/DOMAIN_ANALYSIS.md`, falling back to `.specify/memory/domain-analysis.md`
  - `CONTRIBUTING.md`, then `.github/CONTRIBUTING.md`

  Where both the canonical and the earlier file exist, the canonical one wins, as Principle VII says. No other
  path is tried (FR-002).

  The same root resolution locates **T1's ADRs**: `<root>/adr/*.md` (one directory listing), with `Docs/ADR/` as
  the earlier location. ADRs stay in T1 with the constitution. They are listed here only because they share the
  root lookup, and their clauses keep the rubric's existing ADR treatment.
- **Rationale**: These names are fixed by Constitution VII, so the reader and the writers can't disagree. A
  bounded, named list keeps the "never guess" stance Step 4 already takes for specs.
- **Alternatives**:
  - Scan `docs/` for anything that looks like a policy. Rejected as guessing, and unbounded.
  - Read only the constitution. Rejected: that is today's defect for projects that have a test strategy but no
    constitution.

## R3 — The bounded prior-spec lookup (FR-016)

- **Decision**: Only when no spec authorizes the PR. Take up to **three** keys from the diff, ranked by
  Step 3's risk order. A key is a public identifier the diff changes (command, flag, endpoint, config key) or,
  failing that, a touched file path. For each key, run:
  `gh search code "<key>" --repo "$REPO" --filename spec.md`
  A hit names a `specs/<dir>/spec.md`. Read that file at `baseRefOid` and look for the requirement that
  mentions the key. If a requirement is found and the diff contradicts it, raise one Question under FR-017.
- **Rationale**: Code search costs one call per key and searches only spec files, so the agent never browses
  `specs/`. That is the line between "was this behaviour specified?" and "reconstruct intent from history",
  the defect. Three keys plus R4's five searches stay under the 10-per-minute code-search limit (verified
  2026-10-16 against `gh api rate_limit`).
- **Caveat**: code search indexes the default branch only. When `baseRefName` isn't the default branch,
  coverage says so. A missing hit is reported as "not found by search", never as "not specified".
- **Rate limit**: code search allows 10 requests a minute. A rate-limited or otherwise failed search (HTTP 403 or
  429, or a `gh` error) is **unreachable, not absent**, under the existing absent-vs-unreachable rule. Coverage
  names the keys that weren't searched. The review never treats them as "not found", and never retries in a loop.
  The same rule applies to R4.
- **Alternatives**:
  - Read every `specs/*/spec.md` at base. Rejected: cost grows with the repository, and it recreates the
    behaviour being fixed.
  - Skip the lookup entirely. Rejected by the maintainer (spec Clarifications).

## R4 — How far blast radius reaches

- **Decision**: Use the patch first: changed defaults, removed branches, changed signatures and changed
  exports are all visible in hunks. For callers outside the diff, run up to **five**
  `gh search code "<symbol>" --repo "$REPO"` calls. Pick the changed symbols in Step 3 risk order, skipping
  test files. Read a hit at `headRefOid` only when it decides severity. Coverage states the searches run, the
  ones skipped, and the cap.
- **Rationale**: FR-015a lets a blast-radius finding reach Major, so the evidence for "reaches callers" has to
  be real. A fixed cap keeps the cost bounded and visible. A truncated search lowers confidence, which the
  existing confidence cap already turns into a Question.
- **Alternatives**:
  - Patch-only. Rejected: it can't show reach, so every finding would be Minor or Question, and the most
    important vibe-coded failure would never reach the default proposal.
  - Unbounded search. Rejected on cost and rate limit.

## R5 — Fitting the always-on lenses into "do not run every lens"

- **Decision**: Keep `:345` for the conventional list. Add a sentence that the three always-on lenses are
  **always considered**: each is reported as run, or not run with a reason. For example, "test integrity: not
  run — the diff touches no test file and removes no test". The stated-intent check is considered only when
  no spec authorizes the PR; with a spec it is reported as "not run — traceability against the spec replaces
  it".
- **Rationale**: "Always run" can't mean "always produce findings". The existing honest-coverage rule
  ("A lens that did not run is never reported as passed") already handles inapplicability.
- **Alternatives**: fold the three into the conventional list. Rejected: they'd become optional, which Q1 of
  the clarification rejected.

## R6 — What counts as a weakened test (FR-015)

- **Decision**: A test file in the same diff as the code it exercises, where the diff does any of these:
  - removes an assertion, or replaces it with a weaker one (equality → truthiness, exact → `in`/contains, a
    narrowed exception type widened)
  - adds a skip or expected-failure marker
  - deletes a test function
  - changes an expected value in the same direction as the code change, with no requirement saying so

  The last one is Major only with high confidence. Otherwise it is a Question, under the existing confidence
  cap.
- **Rationale**: These are observable in the patch, so the floor is applied mechanically, not by feel. The
  last case is the one an author legitimately does when behaviour is meant to change, so it alone depends on
  confidence.
- **Alternatives**: any test-file edit counts. Rejected: that would punish ordinary test maintenance.

## R7 — Lint, format and CI configuration as T2

- **Decision**: Read enforced tool configuration only to **suppress** findings. When CI runs a linter or
  formatter (`.github/workflows/*.yml` naming it, or its config at the repo root), the review raises no
  finding of the kind that tool enforces. Coverage says it deferred those to the tool.
- **Rationale**: A reviewer that restates the linter adds noise. A tool the project actually runs is a
  stronger standard than any convention the agent infers.
- **Alternatives**:
  - Parse lint rules into citable clauses. Rejected: unbounded, and duplicates the tool.
  - Ignore config. Rejected: style nits would come back exactly where the project has automated them away.

## R8 — Where the new severity rules sit

- **Decision**: Step 6 gains one floor and four ceilings, in the same "Two floors override the table" block,
  which becomes "Floors and ceilings":
  - Floor: weakened or deleted test ≥ Major (R6).
  - Ceilings: B6/T3 ≤ Minor; PR-text-only ≤ Minor; prior-spec contradiction = Question; non-authorizing-spec
    divergence ≤ Minor and only the FR-010 staleness note.
  - Unchanged rules: the constitution floor (T1 only) and the issue ceiling.
  - Two non-ceilings: blast radius is classified by the rubric (FR-015a), and a dependency is Question unless
    unpinned or duplicate, then Major (FR-014).
- **Rationale**: One place for every override, next to the existing ones. Repeated reviews keep agreeing,
  because none of the rules is left to feel.
- **Alternatives**: put each rule next to its lens. Rejected: the rubric would become scattered, and the
  "assign from this rubric, not by feel" promise depends on one table plus one override block.

## R9 — Which published copies move

- **Decision**: Update three hand-written copies:
  - the review-pr prose block in `AGENTS_LIST.md`
  - the `## speckit.spectra.review-pr` section in `spectra/README.md`
  - the review-pr card in `docs/index.html:655`

  Each gains one or two sentences: what the review is measured against without a constitution (supporting docs,
  codebase conventions, a cited baseline), and that a shipped spec overrides older ones. The front-matter
  description, the `spectra/README.md:25` table row (generated), and `agents-list.json` stay unchanged.
- **Rationale**: Users read those three to decide whether the command fits a project with no constitution, the
  very case this change addresses.
- **Alternatives**: changelog only. Rejected: the landing page would undersell the change to its main audience.
