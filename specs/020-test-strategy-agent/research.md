# Phase 0 — Research: Test Strategy Agent

Nine decisions the command file cannot be written without. Each is a choice the spec left to design,
or a constraint discovered while reading the shipped roster. Format: decision, rationale, alternatives
rejected.

The recurring constraint behind most of them: **the deliverable is a prompt.** There is no code to hold
a threshold, no library to call, and no way to fail a build. Every rule below has to survive being
stated in prose to an agent that will improvise if the prose leaves room.

---

## 1. Classifying project maturity from signals, not a line count

**Decision.** Classification is a weighted read of five signals, reported with the evidence that
produced it and with any signal that pointed the other way (FR-006, FR-008):

| Signal | Greenfield reading | Brownfield reading |
|---|---|---|
| Source volume outside scaffolding | absent or generator output only | substantial hand-written source |
| Test files present | none, or generator's example test | real tests referencing real modules |
| Test/coverage tooling configured | absent, or a bare framework dependency | configured, with thresholds or reporters |
| CI definition | absent, or a build-only workflow | runs a suite |
| Specs, ADRs, and constitution | present, describing intent | present, describing what exists |

No numeric threshold is stated. A project matching mostly the left column is greenfield, mostly the
right is brownfield, and a genuine split — substantial source with zero tests is the common one — is
reported as **mixed**, naming which signals pointed each way.

**Rationale.** A line-count threshold ("under 2,000 lines is greenfield") is the obvious design and it
is wrong on both ends: a 400-line service with 90 tests and a CI gate is not greenfield, and a
40,000-line generated client with no hand-written logic is not brownfield. What actually changes the
strategy is whether there is testing *practice* to build on, and the five signals measure that
directly. Reporting the dissenting signals is what makes a mixed project legible rather than forced
into a box — and "substantial source, no tests" is the case where a wrong classification does the most
damage, because greenfield mode would propose a floor for code nobody has tested.

**Alternatives rejected.** *Ask the user* — the spec forbids it (FR-006), and it asks for something the
command is about to measure. *A line-count or file-count threshold* — wrong on both ends, as above, and
unstable across monorepos. *Commit count or repository age* — explicitly rejected by FR-007; a
freshly-initialised repository can be a decade-old codebase's new home, and a two-year-old repository
can still be scaffolding.

---

## 2. Reading a coverage baseline without running the suite by default

**Decision.** Three baseline provenances, and the command runs nothing unless asked:

| Provenance | How obtained | What may be claimed |
|---|---|---|
| `measured` | the command ran the project's coverage tool, **after an explicit confirmation** | the current figure |
| `reported` | read from a committed report or badge, **with its date** | the figure as of that date |
| `unavailable` | no tooling configured, no report present | no figure; the floor is conditional (FR-023) |

The confirmation is a single question naming the exact command it would run and warning that it
executes the project's test suite. Declined or unanswered, the run proceeds on `reported` or
`unavailable`. In a non-interactive session it is never asked and never run.

**Rationale.** FR-022 caps the brownfield floor at the baseline, and FR-026 reserves the word
*measured* for a figure the command produced — so the distinction has to exist. But running an
arbitrary project's test suite is the largest unbidden side effect a foundation agent could have: it
can take twenty minutes, hit the network, touch a database, or fail for reasons that have nothing to do
with the strategy. `flaky-test-detector` refused to run anything at all and that refusal is one of its
selling points. Gating the run behind a named, declinable confirmation keeps the honest claim available
without making it the default cost of asking for a strategy.

**Alternatives rejected.** *Never run anything* — most projects commit no coverage report, so nearly
every brownfield floor would rest on `unavailable` and FR-022's cap would have nothing to cap against.
*Always run* — unbidden, unbounded, and the opposite of the posture the roster already established.
*Infer coverage from the ratio of test files to source files* — a plausible-looking number with no
relationship to the metric a CI gate would enforce, which is exactly the kind of confident-and-wrong
output the honesty rules exist to prevent.

---

## 3. Stating lens boundaries without assuming a stack

**Decision.** Each lens is defined by **what it proves and what it is allowed to assume**, not by a
tool or a directory convention (FR-020):

- **Unit** — one unit of behaviour in isolation; may assume every collaborator is substitutable. Proves
  logic, not wiring.
- **Integration** — two or more real components together, including the real data store or the real
  framework where that is the thing under test. Proves wiring. May not assume the network is reachable.
- **API contract** — the shape and compatibility of an interface at a boundary someone else depends on,
  verified independently of either side's implementation. Proves that a change is or is not breaking.
- **End-to-end** — one user-visible journey through the assembled system by whatever means the project's
  surface admits. Proves the thing works, and proves nothing about why it stopped.

The document states, per project, which lens owns a given behaviour, so a team can settle
"where does this test go" from the document rather than from taste.

**Rationale.** Every project already disagrees about these words — "integration test" means a
database-backed test in one repository and a cross-service test in another. A strategy that uses the
terms without defining them produces four sections a team reads four different ways. Defining them by
proof obligation rather than by tooling makes the definitions portable across the stacks this command
will meet, which is Principle III's constraint applied to vocabulary.

**Alternatives rejected.** *Define by directory* (`tests/unit/`, `tests/integration/`) — encodes one
ecosystem's convention as the definition, and says nothing to a project that puts tests beside their
source. *Define by tool* — collapses the moment a project uses one runner for two lenses, which is the
common case. *Leave them undefined and rely on common usage* — the disagreement above is the reason
the boundary statement is a requirement rather than a nicety.

---

## 4. Detecting testable surfaces without a build graph

**Decision.** A **testable surface** is identified by the co-location of three things: an independent
dependency manifest, source under the same root, and either its own test configuration or no test
configuration at all. Workspace declarations (a workspaces array, a members list, a modules list) are
read where present and treated as the authoritative surface list. Where a repository yields exactly one
surface, the document says so once and never uses the word again — a single-stack project should not
read like a monorepo (FR-027, User Story 5).

**Rationale.** The command has no build system and cannot resolve a dependency graph, but the question
it actually needs to answer is narrower than "what are the modules": it is "which parts of this
repository would have *different* testing answers". A separate manifest is the strongest available
signal for that, because a separate manifest is what makes a separate toolchain possible. Reading the
workspace declaration first is what stops the heuristic from inventing surfaces in a repository that
has already declared them.

**Alternatives rejected.** *Top-level directory names* (`frontend/`, `backend/`, `services/`) — a naming
convention, not a fact, and absent in most repositories. *One surface always, with per-lens caveats* —
produces one coverage floor for a TypeScript UI and a Python service, which FR-027 exists to prevent.
*Ask the user to enumerate them* — the same objection as R1: it is measurable, and a wrong answer
silently mis-shapes the whole document.

---

## 5. Deriving the floor and its ratchet from the baseline

**Decision.** The floor is derived, not chosen from a table:

- **Brownfield with a baseline** — the floor is the baseline rounded *down* to a stated granularity, so
  ordinary fluctuation does not break the build on day one. The document states the rounding.
- **Brownfield without a baseline** — no number. The floor is stated as conditional on the tooling the
  document recommends as step one (FR-023).
- **Greenfield** — the floor is a convention, explicitly marked as unevidenced under FR-043, and framed
  as "hold from the first commit" rather than "reach eventually", because that is the one thing a
  greenfield project can do that a brownfield one cannot.

The **ratchet** is expressed as trigger-and-step pairs, never as dates: *when the floor has held for N
consecutive merges, raise it by M points; when a surface's baseline exceeds the floor by more than M,
raise the floor to the baseline.* The target is stated; the schedule is not.

**Rationale.** FR-022 caps the floor at the baseline and FR-024 requires a ratchet, so the only open
question is what generates the numbers. Rounding down is the difference between a floor that holds and
a floor that fails the next build on a two-line refactor — and a floor that fails immediately gets
deleted, which is worse than not proposing one. Dates are rejected because the command has no way to
know a team's cadence and a document dated in the past is self-evidently stale; a trigger stays true
indefinitely and is checkable from the repository.

**Alternatives rejected.** *A fixed industry number* (80%) — the single most common way a coverage
policy gets ignored, and flatly incompatible with FR-022 on any repository below it. *Per-file floors* —
enforceable in some tools and not others, and it turns one policy decision into hundreds. *A dated
schedule* — stale on arrival, unknowable cadence.

---

## 6. Detecting whether a strategy is "already embedded" in a constitution

**Decision.** A three-state answer, reached semantically and reported with a quotation (FR-029):

| State | Test | What the command does |
|---|---|---|
| **Embedded** | a principle or standards section states normative testing obligations covering the strategy's core claims | quote the governing clause, offer no amendment |
| **Partially embedded** | testing obligations exist but omit or contradict part of the strategy | quote what exists, draft an amendment scoped to the gap, and surface any contradiction as a finding (FR-033) |
| **Absent** | no normative testing obligation anywhere | draft a new principle |

The read is semantic — a section heading plus normative keywords (`MUST`, `SHOULD`, `required`) plus
subject matter — never a string match on the word "test", which fires on any constitution that mentions
testing in passing.

**Rationale.** The gate in User Story 3 turns entirely on this answer, and both wrong answers are
costly: a false *embedded* silently drops the amendment the user asked for, and a false *absent*
proposes a principle that duplicates one already in force. Quoting the clause is what makes the answer
auditable — the user can see the reasoning rather than trusting a verdict. The partial state exists
because it is the most likely real-world case: constitutions commonly say something about testing
without saying anything about a floor.

**Alternatives rejected.** *A keyword search for "test"* — fires on prose, misses a "Quality Standards"
section that never uses the word. *Binary embedded/absent* — forces the common partial case into
whichever answer is worse. *Ask the user* — they are asking the command precisely because they have not
read the constitution recently.

---

## 7. The shape of an amendment another command consumes

**Decision.** The drafted amendment reuses `domain-analyzer`'s handoff shape rather than inventing one:
a checkbox-selected statement written in the constitution's voice, carrying a `section:` naming where it
goes and a `status:` of `add` or `amends: <principle name>` (FR-032b). It lives in the strategy
document's proposed-amendment section, and the handoff is a sentence telling the user to run
`/speckit-constitution` against that document.

The command never invokes `/speckit-constitution` itself.

**Rationale.** `domain-analyzer` already established a format that `/speckit-constitution` consumes, and
a second format would be a second thing to keep compatible. Naming the command as something the *user*
runs — rather than something this command calls — is what keeps Principle III intact: an agent-agnostic
prompt cannot portably invoke another command, and a chained invocation would also bypass the user's
own review of what is about to change in their governance.

Putting the draft in the strategy document rather than in a separate handoff file is the one departure
from the precedent, and it follows from Q2: the document already exists, already ships, and is already
the thing the user was asked to approve. A second file would need its own location decision under
Principle VII and its own template under Principle VIII, for content that has one reader and one
consumer.

**Alternatives rejected.** *A separate handoff file* under `.specify/memory/` — mirrors
`domain-analyzer` exactly, at the cost of a second artifact whose only purpose is to hold three
sentences. *Invoking `/speckit-constitution` directly* — breaks Principle III and removes the user from
their own governance change. *Emitting the amendment only in the session* — it is lost the moment the
session ends, which defeats the purpose of taking the approval.

---

## 8. Artifact-root and template resolution: reuse, do not re-derive

**Decision.** Both resolutions are copied in substance from the three shipped document agents, not
reinvented:

- **Root** — read `Artifact root:` from the constitution case-insensitively; reject an absolute path or
  one containing `..` and say why; otherwise check the publication signals (`mkdocs.yml`,
  `docusaurus.config.*`, `docs/_config.yml`, `docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, a Pages
  configuration pointing at `docs`) before defaulting to `docs/`; where a signal fires and no root is
  declared, recommend `documents/` and let the user choose; where the choice cannot be obtained, take
  the non-publishing option. State the declaration line but **never write it**.
- **Template** — `.specify/templates/overrides/test-strategy-template.md` → preset → extension → core →
  the command's inline skeleton, first readable non-empty layer wins, resolved path reported.

**Rationale.** These are solved problems with an enforcement suite already pointed at them.
`test_doc_output_paths.py` asserts the literal publication signals, the `Artifact root:` string, the
`never write it` clause, and the `documents/` recommendation in every command listed in its `CANONICAL`
dict; `test_document_templates.py` asserts four-layer resolution and heading parity between the shipped
template and the inline skeleton. Adding this command to both dicts is what converts those from prose
into assertions — divergence would mean writing new prose that the existing tests would then reject.

**One project-specific note worth recording**: Spectra's own repository trips the publication check.
`docs/index.html` is present and `main` `/docs` is served by Pages, so a self-hosted run must surface
the choice rather than default silently. That makes the check testable by running the command here.

**Alternatives rejected.** *A single hard-coded `docs/` path* — the 1.6.0 bug the principle and the test
module both exist to prevent. *A single hard-coded template path* — the 1.7.0 bug `test_document_
templates.py` exists to prevent. *Re-deriving the wording* — gratuitous divergence from four commands
that already say it correctly, and the tests match on literal strings.

---

## 9. Recommending tools from behind a knowledge cutoff, with no network

**Decision.** Tool recommendations are ranked by how much the project already tells the command
(FR-016, FR-043):

1. **Already present** — named in a manifest, lockfile, or config. Recommended freely; the evidence is
   the manifest entry.
2. **Ecosystem-standard for a stack the project demonstrably uses** — recommended, cited to the stack
   evidence, and marked as a convention rather than a finding.
3. **Anything else** — recommended only with an explicit note that the command cannot verify the tool's
   current state, is offering it from frozen knowledge, and that the team should confirm it is
   maintained before adopting.

The document carries one standing note that no tool recommendation was verified against a registry,
because no network request was made (FR-050).

**Rationale.** The command's picture of the tooling landscape is whatever the host agent's training
left it with, and testing tooling moves. Recommending a deprecated or renamed package is the failure
mode most likely to make a whole document look untrustworthy, and it is undetectable from inside a
prompt with no network. Ranking by project evidence turns the limitation into a preference that is
correct anyway: the tool a project already has is nearly always the right answer, and it needs no
verification because its presence *is* the verification.

This is also the rule that makes FR-017's Playwright treatment fall out rather than being special-cased
— a project with no browser dependency in any manifest gives no evidence for a browser driver at any of
the three tiers.

**Alternatives rejected.** *Recommend freely from knowledge* — the deprecated-package failure, with no
signal to the reader. *Recommend only what is already present* — useless to greenfield, which is
Story 1. *Fetch a registry to verify* — a network request the command has promised not to make, and the
one promise `impact` set as precedent for the whole roster.
