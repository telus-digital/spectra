# Phase 0 Research: Test Plan Agent

**Feature**: `speckit.spectra.test-plan` | **Branch**: `021-test-plan-agent` | **Date**: 2026-09-11

Twelve decisions. Each one is a place where the specification states *what* must be true and the command
text has to decide *how* a language model reliably makes it true. Where an existing Spectra command has
already answered a question, the answer is reused and cited rather than re-derived — divergence between
two commands on the same mechanic is a defect in its own right.

---

## R1 — Resolving the required argument, and what counts as usable as a specification

**Decision.** Treat the whole of `$ARGUMENTS`, after any flags are removed, as one path. Resolve it in
this fixed order:

1. **Empty** → ask for a specification path and stop. Read nothing else (FR-007 to FR-009).
2. **A readable file** → candidate specification; apply the usability test below.
3. **A directory** → look for `spec.md` inside it. Exactly one → resolve to it and state the
   resolution. None → stop, naming the directory. More than one candidate specification and no
   `spec.md` → list what was found and ask; do not choose.
4. **Missing, unreadable, or of an unsupported type** → report the path and the reason, and stop.

The **usability test** is deliberately weak: the file must be Markdown-like text, non-empty, and carry at
least one heading plus at least one of a requirements, user-scenario, acceptance-criteria, or
success-criteria section under any wording. Failing it stops the run with the reason.

**Rationale.** The strong version of this test — requiring the Spec Kit spec template's exact headings —
would refuse to run on any project that overrode its spec template, which Spec Kit explicitly supports.
The weak version's only job is to catch the realistic mistake: a path to a `README.md`, a `plan.md`, or a
ticket export. Anything that passes has enough structure for traceability to mean something, and the
command states what it found so the user can see it resolved the file they meant.

Directory input is accepted because the feature directory is what a user actually has in hand after
`/speckit-specify`, and resolving `specs/021-x/` → `specs/021-x/spec.md` removes a guaranteed typo
without guessing *which feature* was meant — the distinction FR-008 protects.

**Alternatives rejected.** *Accepting a spec ID or feature number* (`021`, `test-plan-agent`) reintroduces
inference through the front door: the command would scan `specs/` to resolve it, which is exactly what
FR-008 forbids, and a mistyped number silently selects a real neighbouring feature. *Accepting multiple
paths* was rejected as scope the specification does not ask for; one plan is about one specification.

---

## R2 — Where the no-checkbox rule is enforced, given that runtime output cannot be tested

**Decision.** Enforce it at three layers, because no single one is sufficient:

| Layer | Mechanism | What it catches |
|---|---|---|
| The shipped template | It simply contains no checkbox; exit criteria are plain statements | The default path, for every run |
| The command text | An explicit instruction: emit no `- [ ]` or `- [x]` in any section, and render a checkbox found in any resolved template layer as a plain statement instead (FR-041) | An override that reintroduces one |
| This repository's suite | A regex over `spectra/templates/test-plan-template.md` and over the command's inline skeleton | A maintainer reintroducing one in a later edit |

**Rationale.** Prompt rules are not executable, so the enforceable surface for a Spectra command is the
text of the artifacts that ship — the posture `test_doc_output_paths.py` and `test_document_templates.py`
already take. A checkbox is unusually well suited to this: it is a fixed two-character construct, so the
assertion is exact rather than heuristic, and it is the one invariant in this feature that can be pinned
with no false positives. The command-text layer is what extends the rule to a project override, which no
test in this repository can ever see.

**Alternatives rejected.** *Template-only* leaves an override free to turn an approval document into a
competing tracker. *Command-text only* leaves the shipped default one careless edit away from violating
the rule it states. *Refusing to run on an override containing checkboxes* makes a formatting choice
fatal and would discard a team's whole section over two characters.

---

## R3 — Expressing traceability without renumbering the specification

**Decision.** The `Verifies` column carries the specification's **own** identifier, verbatim. Three forms,
in order of preference:

1. **An explicit identifier the spec defines** — `FR-014`, `SC-003`, `NFR-002`. Used as-is.
2. **A composed reference for an acceptance scenario**, which Spec Kit's template numbers within a story
   rather than globally: `US2-AC1` for the first acceptance scenario of User Story 2, with the story's
   title given once in the scope section so the reference is legible to someone who has the spec open.
3. **A short verbatim quotation** — six to twelve words in quotation marks — where the specification
   states a requirement in prose with no identifier at all.

The command never assigns a new identifier to a specification item, never renumbers, and never edits the
specification to add identifiers (FR-018).

**Rationale.** Traceability is only useful if a reviewer can check it in both directions without a
decoder ring. Reusing the spec's identifiers makes the check mechanical: search the spec for `FR-014`,
search the plan for `FR-014`. Composing `US2-AC1` is necessary because acceptance scenarios are numbered
per story in the template, so `AC1` alone is ambiguous across six stories; the composition is
deterministic, so two runs produce the same reference. The verbatim-quotation fallback keeps the column
honest on an unstructured spec instead of inventing an identifier scheme that exists nowhere else.

**Alternatives rejected.** *Minting `TP-REQ-nnn` identifiers for unnumbered requirements* creates a second
numbering authority for the spec, and the numbers change on every re-run as the prose moves. *Editing the
spec to add identifiers* is the cleanest fix and is forbidden: FR-018 makes the input read-only, and a
command that renumbers a spec under review is a command that invalidates a review in progress.

---

## R4 — Resolving the level vocabulary

**Decision.** A fixed precedence, with the resolved set and its provenance stated in the document:

1. **The test strategy document's lens names**, verbatim, where one exists (FR-035).
2. **Lens names the constitution declares**, where it carries a testing obligation naming them.
3. **The default set**: `unit`, `integration`, `api-contract`, `end-to-end`, `manual` (FR-036).

Where the constitution and the strategy name different sets, the constitution wins and the divergence is
reported (FR-013). `manual` is always available, appended to an inherited set that omits it.

**Rationale.** The four lenses `test-strategy` defines exist precisely so a team can settle "where does
this test go" from their own document. A test plan that renames them re-opens the question it was
supposed to close. Taking the names verbatim — not normalized, not title-cased, not mapped — is what
makes the two documents diffable against each other.

`manual` survives because a plan and a strategy have different jobs. A strategy decides what to automate;
a plan must be able to place a condition that no automated lens will ever cover — a visual check, a
third-party sandbox interaction, an accessibility walkthrough. Dropping it would force such conditions
into "explicitly not covered", which would be false: they *are* covered, by a person.

**Alternatives rejected.** *Always using the default set* reproduces exactly the two-documents-disagree
problem. *Mapping the project's names onto the default set* ("they said `component`, that means
`integration`") puts a silent translation between two artifacts a reviewer is reading side by side, and
the mapping is a guess about a word the team defined deliberately.

---

## R5 — Locating the strategy document without re-implementing logic that does not apply

**Decision.** Resolve the artifact root exactly as the shipped document commands do — a case-insensitive
`Artifact root:` line in the constitution, rejected if it carries a leading slash or a `..` segment,
defaulting to `docs/` — then look for `<artifact-root>/test-strategy/TEST_STRATEGY.md`. Read only.

Three obligations that attach to *writing* into the artifact root are deliberately **not** carried over:

- **No publication check.** The six signals (`mkdocs.yml`, `docusaurus.config.*`, `docs/_config.yml`,
  `docs/.nojekyll`, `docs/index.html`, `docs/conf.py`) exist to stop a command *publishing* a document to
  the web by accident. This command writes nothing into `docs/`, so the check has nothing to protect.
- **No `documents/` recommendation.** Same reason.
- **No offer of the declaration line.** There is nothing to declare: the output destination is fixed by
  the input path.

An unusable declared value is reported, the default is used, and the *output* destination is unaffected
either way. If the strategy is not found at the resolved location, say so once and continue on the
default lens set (FR-014).

**Rationale.** This is the first read-only use of the declaration, and the distinction is load-bearing for
the enforcement suite. `tests/test_doc_output_paths.py` keys its declared-root assertions to
`DOCUMENT_COMMANDS = tuple(CANONICAL)` and every one of them asserts a *write* posture — the literal
string `never write it`, all six publication signals, a `documents/` fallback. Adding this command to
`CANONICAL` would require three clauses that are false here and would assert an artifact-root write
target it does not have. So the entry is not added, and a negative assertion pins the omission with its
reason, because "absent" and "someone forgot" look identical in a dict.

**Alternatives rejected.** *Adding the command to `CANONICAL` and writing the three clauses anyway* would
put false statements in a shipped command to satisfy a test. *Searching the repository for
`TEST_STRATEGY.md` wherever it may be* was rejected because the declaration is the project's stated answer
to where its artifacts live; searching around it would find a copy in a vendored dependency or an
archive folder and treat it as policy.

---

## R6 — The shape of the `/speckit-plan` handoff

**Decision.** The command prints a ready-to-copy invocation naming the written path and stating what the
planner should do with it, and does nothing else:

```text
/speckit-plan Plan this feature against the approved test plan at
specs/021-test-plan-agent/test-plan.md. Every P1 test condition in it must map to a task that
writes the test before the implementation it covers.
```

The command does not invoke it (FR-048), registers no hook, writes no marker into `spec.md`, and edits no
core command file (FR-005). The invocation is presented as something the **user** runs; each agent renders
its own slash-command syntax, so the command names the Spec Kit command rather than any agent's spelling
of it.

**Rationale.** `/speckit-plan` takes free-form `$ARGUMENTS` and reads the feature directory, so a path
plus one sentence of intent is genuinely sufficient — no mechanism is needed, and the only reliable way to
make a *core* command aware of an optional add-on's output is to have the user tell it. This is the same
handoff `test-strategy` uses for `/speckit-constitution`: name the command, hand over the text, stop.

**Alternatives rejected.** *Registering a `before_plan` hook in `spectra/extension.yml`* would make every
project that installs Spectra prompt for a test plan on every feature — the opposite of the opt-in
add-on the description asks for, and it would couple `/plan` to an agent the user may never install.
*Writing a pointer into `spec.md`* would modify the input, which FR-018 forbids and which would put a
Spectra-specific line into an artifact under stakeholder review. *Relying on `/plan` noticing the file
on its own* is not a mechanism at all — it is a hope about another command's reading order.

---

## R7 — Keeping the risk table a decision rather than an inventory

**Decision.** Cap the section at **two to five rows**, and derive likelihood and impact from stated
triggers rather than judgement, in the manner of `impact`'s rating lookup:

**Impact is High** if the risk, realized, would cause data loss or corruption, break an external
contract, expose data, or block a release. **Medium** if it would produce wrong behaviour a user or
caller notices. **Low** otherwise.

**Likelihood is High** where the touched area has no current test coverage *and* the change is not
additive; **Medium** where one of those holds; **Low** where neither does.

The `Testing response` column takes one of three values — deeper coverage, an extra scenario, or
**accept** — and `accept` must appear where the derived rating does not justify effort. A table where
every row is High/High is treated as a failure of the exercise: the command re-derives, and if the
derivation genuinely produces all-High it says so explicitly and names why, rather than presenting an
unprioritized list as a prioritization (FR-033).

**Rationale.** The attached template's own guidance says it: *"If everything is High/High, you haven't
prioritized."* A model asked to list risks will rate them all severe, because severity feels like
diligence. Deriving the two axes from conditions the command can actually check — is this area tested, is
this change additive — converts the section from a mood into a lookup, and makes two runs on the same
spec agree. Making `accept` a first-class answer is what lets the table say "we looked and chose not to
spend here", which is the sentence a stakeholder most needs and a generator is least likely to write.

**Alternatives rejected.** *An uncapped table* produces an inventory nobody reads and buries the two rows
that matter. *A numeric score* implies a precision the inputs do not support and invites arguing about
arithmetic instead of about risk.

---

## R8 — Deriving condition priority from the specification's own priorities

**Decision.** A condition inherits the priority of the specification item it verifies. Spec Kit's template
already prioritizes user stories `P1`/`P2`/`P3`, so:

- verifies an acceptance criterion of a **P1** story → **P1**
- verifies a **P2** story → **P2**; a **P3** story → **P3**
- verifies a functional requirement not reachable from any story → **P2** by default, **P1** where the
  requirement is a prohibition, a safety property, or a data-integrity property
- verifies a success criterion → the priority of the story it measures, else **P2**

`P1` has one further meaning fixed by the document: only `P1` conditions gate the exit criteria (FR-040).
Where the specification carries no priorities at all, the command says so and assigns priority from the
impact axis of R7 alone.

**Rationale.** The spec already contains a prioritization the team agreed to; inventing a second one in
the test plan creates two answers to "what must work first". Inheriting it makes the plan's priorities
reviewable against the spec's, and makes the exit criteria mean something specific rather than
aspirational. Promoting prohibitions and data-integrity properties to `P1` regardless of story is the one
override, because a requirement of the form "MUST NOT" usually has no story — nobody writes a user
journey about the thing that must not happen — and it is exactly the requirement whose violation is
unrecoverable.

**Alternatives rejected.** *Rating each condition independently* discards agreed information and produces
a plan whose priorities quietly disagree with the spec's. *Making everything P1* makes the exit criteria
unmeetable and the priority column noise.

---

## R9 — Detecting existing coverage by reading tests, never by running them

**Decision.** Establish what the current suite already guarantees by reading test source: test files that
import or reference the module the feature touches, test names that describe the behaviour, and assertions
against the identifiers the specification names. A claim that something **is** covered cites the test file
(FR-029). A claim that something **is not** covered cites the search — what terms, in what paths (FR-028).
The suite is never executed, and no coverage tool is run.

**Rationale.** This command has no baseline figure to label, which is precisely what made `test-strategy`
willing to run a coverage tool behind a confirmation: it needed to distinguish `measured` from `reported`.
Here the question is per-behaviour, not per-repository, and a coverage report answers the wrong one — a
line-covered module tells you nothing about whether *this acceptance criterion* is asserted anywhere. So
there is nothing to gain from execution and a great deal to lose: an unbidden test run on a stranger's
repository is unbounded in time and may touch the network. This lands on `flaky-test-detector`'s
never-runs-anything posture rather than `test-strategy`'s confirmed-run exception.

**Alternatives rejected.** *Running the suite with a filter* to see what passes conflates "a test exists"
with "a test passes", and a red suite would make the plan claim there is no coverage. *Reading a committed
coverage report* answers the repository-level question this command does not ask. *Skipping
existing-coverage detection entirely* was rejected because it produces a plan that asks stakeholders to
approve re-testing ground the suite already holds, which is the fastest way to get the document ignored.

---

## R10 — Re-run and non-interactive semantics

**Decision.** Two gates, and one preservation rule.

- **Gate 1 (existence).** Where `test-plan.md` already exists beside the specification, read it, then ask
  before rewriting. Declined → nothing is written and nothing else happens (FR-050, FR-051).
- **Gate 2 (out-of-project).** Where the resolved specification lies outside the project the command was
  invoked in, stop before writing (FR-022). This gate takes no answer; it is not a confirmation.
- **Preservation.** Any condition the previous plan recorded as *explicitly not covered* is carried
  forward, or its removal is stated in the run report. Same for an accepted risk.
- **Non-interactive.** A session that cannot take an answer may **create** a plan that does not exist,
  because Gate 1 does not fire. It may not **rewrite** one: it reports that a plan exists and what it
  would have changed (FR-052). An empty argument still stops (FR-009) — that is a missing input, not a
  gate.

**Rationale.** The asymmetry between creating and rewriting is the whole of this decision. Creating is
additive and recoverable; rewriting destroys a document that may already have been circulated and
approved, and the not-covered list is the part most likely to hold a decision a human made deliberately
and no re-read of the spec will recover. `test-strategy` rewrites its singleton in place because a
standing policy has one current answer; a test plan under stakeholder review does not have that property.

**Alternatives rejected.** *Always overwriting* silently destroys approved content. *Never overwriting*
makes the command useless after `/speckit-clarify`, which is when it is most needed. *Writing
`test-plan-2.md`* produces two documents with no statement of which is current — the failure numbering
was rejected for in the first place.

---

## R11 — Filling "build under test" without inventing a version

**Decision.** Populate it from evidence, labelled, in this order: the current Git branch name; plus a
version string if the project commits one in a conventional location (a `VERSION` file, or a version field
in a dependency manifest); plus the service or package name where the manifest gives one. Where nothing is
readable, write that the build under test is the working tree on the named branch. Never infer a release
number, a tag, or an environment.

**Rationale.** The field's purpose is to let a reader tell *what was planned against* six weeks later. A
branch name is always available and always true. A version number read from a committed file is true and
attributable. A version number the command guesses is worse than an empty field, because it looks
authoritative — the same reason `test-strategy` labels a coverage baseline `measured`, `reported`, or
`unavailable` rather than printing a bare figure.

**Alternatives rejected.** *Asking the user* spends a question on something the repository answers, which
FR-017 forbids. *Leaving the field as a placeholder* is the one outcome FR-043 explicitly bans.

---

## R12 — Which optional sections may be added, and on what trigger

**Decision.** The template ships the attached description's guidance list as authoring guidance that never
reaches the output (FR-044). The command adds a section only on its stated trigger, and names which it
added and why (FR-045):

| Optional section | Trigger the command checks |
|---|---|
| Non-functional targets | The specification states a performance, security, or accessibility budget, or the constitution declares one |
| Rollback / migration testing | The specification implies a schema change, a data migration, or a backfill |
| Roles & responsibilities | The specification or constitution names a separate QA function or more than one executing team |
| Approvals / sign-off | The constitution declares a regulated or audited regime |
| Schedule & milestones | **Never added automatically.** Offered only if the user asks |
| Suspension / resumption criteria | **Never added automatically.** Offered only if the user asks |
| Test summary report | **Never added automatically** — it reports an outcome, and this document states intent |

**Rationale.** Every one of these sections is a real need for some projects and noise for most, which is
why the description says "skip these by default". A trigger the command can actually check keeps the
decision out of the model's taste: a performance budget in the spec is a fact, and "this feels like it
needs a schedule" is not. The three refused outright are refused because they are *project management*
rather than test design — a generator inventing a schedule for work nobody has staffed produces dates a
stakeholder may act on, and a test summary report describes a test cycle that has not happened yet.

**Alternatives rejected.** *Emitting the guidance list into the document* instructs a stakeholder to
author sections nobody asked them for, in a document they were handed to approve. *Including every
optional section* buries the five that matter. *Never adding any* would fail the spec whose only
requirements are non-functional, which is a realistic case the edge cases already name.

---

## Summary of decisions

| # | Decision | Primary requirements |
|---|---|---|
| R1 | Path-only argument; directory resolves to `spec.md`; weak usability test; never infer | FR-007 to FR-010 |
| R2 | No-checkbox enforced in template, command text, and this repository's suite | FR-041 |
| R3 | Reuse the spec's own identifiers; compose `USn-ACn`; quote as a last resort; never renumber | FR-023, FR-024 |
| R4 | Level vocabulary: strategy, then constitution, then default five; `manual` always available | FR-013, FR-035, FR-036 |
| R5 | Read the declared root to *find* the strategy; no publication check; `CANONICAL` deliberately not extended | FR-012, FR-014 |
| R6 | Handoff is printed text naming `/speckit-plan`; no hook, no invocation, no marker in the spec | FR-005, FR-047, FR-048 |
| R7 | Risk table capped at 2–5 rows; both axes derived from triggers; `accept` is a first-class response | FR-032, FR-033 |
| R8 | Condition priority inherited from the spec's story priorities; prohibitions promoted to P1 | FR-034, FR-040 |
| R9 | Existing coverage read from test source; nothing is ever executed | FR-020, FR-028, FR-029 |
| R10 | Confirm before rewriting; create but never rewrite non-interactively; preserve not-covered decisions | FR-050 to FR-052 |
| R11 | "Build under test" from branch plus committed version, labelled; never inferred | FR-030, FR-043 |
| R12 | Optional sections added only on a checkable trigger; three never added automatically | FR-044, FR-045 |
