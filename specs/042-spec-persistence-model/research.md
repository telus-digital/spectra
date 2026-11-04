# Research: Spec Persistence Model in the Methodology Agent

No `NEEDS CLARIFICATION` remained in the spec after the 2026-11-04 clarify session. The decisions below
settle the design questions the spec left to planning.

## R1. Where the decision sits: lens 4, question 5, the question 9 shape

- **Decision**: The persistence model is part of lens 4. Question 5 lists lens 4's other candidates
  first, then offers five options: Living Spec, Flow-Forward, Flow-Back, Hybrid (Living Spec by default),
  Skip. The chosen model is `accepted`, the other three `declined`, and the other lens 4 candidates take
  the model's decision unless free text excludes them. The Step 5 sentence "For questions 3–8 and 10, the
  four are" becomes "For questions 3, 4, 6–8 and 10".
- **Rationale**: This is the precedent question 9 already sets for mutually exclusive choices. Keeping the
  number fixed keeps "Question N of 10" honest and leaves every count in the agent, template, listings,
  and tests untouched.
- **Alternatives considered**: A tenth lens and eleventh question was rejected at specify time (spec,
  "Decisions recorded"). Keeping the Recommended set / Codify / Full set / Skip shape was rejected because
  "Full set" would accept four exclusive models.

## R2. Brownfield signals: how "after its feature merged" is detected

- **Decision**: Read the default branch's **first-parent** history (`git log --first-parent <default>`).
  A feature directory's **delivery point** is the first first-parent commit that contains
  `specs/<dir>/spec.md`. That is the merge commit with merge commits, and the squashed commit with
  squash-and-merge. After the delivery point:
  - **Living Spec signal**: a first-parent commit changes that directory's `spec.md`.
  - **Flow-Back signal**: a first-parent commit changes that directory's `plan.md` or `tasks.md` while its
    `spec.md` is unchanged in the same commit.
  - **Flow-Forward signal**: any `spec.md` names another spec directory it builds on: the exact
    cross-link wording, "supersedes"/"extends"/"builds on" next to a `specs/NNN-` path or a spec number,
    or an `**Input**:` line citing an earlier spec.

  Report each signal with a count and up to three citations (commit short SHA and path).
- **Rationale**: First-parent history makes "on the default branch" mechanical under every merge
  strategy, without needing PR metadata. Commits on feature branches before delivery are in-progress
  edits, which every model allows (spec, Edge Cases).
- **Alternatives considered**: Using `tasks.md` completion as the delivery point was rejected because
  status lines are often left unchecked, which is exactly what lens 4 already audits. Reading PR merge
  events was rejected because the agent cannot assume a forge or network access (the agent never makes
  network requests).

## R3. When a signal decides the recommendation

- **Decision**: A model is recommended when its signal is the only one found. Two or more signals, or
  none, means Hybrid. A Living Spec signal whose only commits are typo- or wording-only is still reported,
  but the report says so. The recommendation follows the rule regardless, and the team decides.
- **Rationale**: The spec fixes "mixed → Hybrid" (FR-008). Weighting signals by size would add a judgment
  the team cannot audit; a count plus citations lets them overrule with one word.
- **Alternatives considered**: A majority rule (most frequent signal wins) was rejected because it would
  recommend Living Spec to a Flow-Forward team that fixed a few typos in old specs. This repository is
  such a case.

## R4. Where Hybrid's mapping lives

- **Decision**: The accepted Hybrid guardrail **always** carries the per-type mapping in its statement.
  The document's mode-choice table gains a persistence column that mirrors it. When question 3 adopted no
  table, only the statement carries it, and the document says why (FR-013). On a re-run, the prior
  mapping is read from the accepted Hybrid candidate's statement. No extra front-matter key is added.
- **Rationale**: The constitution receives only the Constitution input section, not the mode-choice
  table. SC-003 requires the constitution entry alone to answer "edit or new directory?" for each change
  type, so the mapping must be in the guardrail. FR-013 was amended after analysis to state this
  directly, with the no-table case as the one where the mirror is absent.
- **Alternatives considered**: A `persistence_mapping` front-matter key was rejected because it would be a
  second copy that could disagree with the statement the team reworded. Mapping only in the table was
  rejected because it fails SC-003.

## R5. The guardrail's identity and strictness

- **Decision**: Each model is one candidate in lens 4's namespace, `em-spec-lifecycle-traceability-<hash>`,
  generated and frozen like any other (Step 4). Strictness is **MUST**. Basis is `observed` when its
  brownfield signal was found, otherwise `aspirational`. Section is lens 4's default, Development
  Workflow, or the project's equivalent. Against an existing constitution, the usual suppress and
  `amends:` rules apply.
- **Rationale**: Reusing the existing record keeps `/speckit-constitution`, `kb-vault`, and re-runs working
  unchanged. MUST, because a SHOULD convention for which file to edit is the case-by-case drift the
  feature removes.
- **Alternatives considered**: A dedicated `em-persistence-<model>` slug, like `em-overlay-<name>`, was
  rejected because the record's lens key would then disagree with its slug, and overlays have a slug of
  their own only because lens 1 owns them by name.

## R6. Agent-agnostic wording inside the guardrail

- **Decision**: Guardrail statements name **phases** ("the specify phase", "the converge phase") and
  artifacts (`spec.md`, `plan.md`, `tasks.md`), not any agent's invocation syntax. The canonical text is
  in [contracts/persistence-guardrail.md](contracts/persistence-guardrail.md).
- **Rationale**: Principle III. The constitution is read by whichever agent the team uses, so a slash
  form would be wrong for skills-mode and dotted-command agents.
- **Alternatives considered**: Writing `/speckit-specify`, as some existing hand-off lines in the command
  do, was rejected. Spec 041's plan already notes those lines are not a precedent for new text.

## R7. Flow-Back's divergence rule and reconciliation check

- **Decision**: Under Flow-Back, the artifact nearest the work takes the change first: `tasks.md` for a
  task-level change, `plan.md` for a design change, `spec.md` for a requirement change. All three must
  agree before the pull request carrying the change merges (FR-019), and the guardrail names the analyze
  phase as the check: it reports no inconsistency between spec, plan, and tasks before merge.
- **Rationale**: "Agree" has to be checkable to mitigate silent drift. The analyze phase is the core,
  read-only Spec Kit check that already exists for exactly this.
- **Alternatives considered**: Leaving "agree" undefined was rejected as untestable. A Spectra-owned
  reconcile command is out of scope (spec).

## R8. The persistence reference in the written document

- **Decision**: A fifth always-written reference, alongside the existing four in Step 7, goes in the Spec
  lifecycle & traceability section. It names the accepted model and gives a five-row table: phase →
  obligation. For Hybrid it adds the mapping (or points to the mode-choice column). With no model
  accepted, it is one sentence. The template's Spec lifecycle comment describes it. No new heading is
  added, so the template and inline skeleton section lists are unchanged.
- **Rationale**: FR-022, and the template test that pins the section order.
- **Alternatives considered**: A new `## Spec persistence` section was rejected because it changes the
  section list a team's override is matched against, and it would split lens 4 across two sections.

## R9. Versioning and listings

- **Decision**: Extension minor bump, 1.30.0 → 1.31.0, with a `CHANGELOG.md` entry. `agents/methodology.md`
  manifest gains the phrase "spec lifecycle and persistence model" in its lens list, and the body's "How
  it works" step 3 and step 5 gain one sentence each. The generator re-renders the description lines and
  listings. The template's `provides.templates` description in `extension.yml` (hand-maintained) adds
  "the persistence reference" to what stays with the command.
- **Rationale**: Principle V and VI: a materially changed agent is a minor change; nothing is renamed or
  removed.
- **Alternatives considered**: Patch bump was rejected because the agent asks and produces something new.
