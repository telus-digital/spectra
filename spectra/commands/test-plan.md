---
description: "Turn one specification into a stakeholder-facing test plan written beside it as test-plan.md — scope, risks, traceable test conditions, suggested UAT scenarios, regression scope, environment, and exit criteria — grounded in the project's own testing policy and its existing suite. It uses exactly the lenses the test strategy chose: a lens the strategy rules out is unavailable, and it says so loudly when the strategy predates UAT and regression or does not exist. It finds the feature the way the planning command does — SPECIFY_FEATURE_DIRECTORY, then .specify/feature.json — and says which one it used; a path argument only confirms it, and a mismatch stops, so the test plan and the plan always share a directory. Every acceptance criterion reaches a condition or a UAT scenario or is reported as uncovered, every user story gets a UAT scenario or a reason, and an ambiguous requirement gets a stated gap rather than an invented condition. Carries no checkbox in any section — it is approved, not tracked — and is offered by an optional hook after specify. It ends with a ready-to-paste planning prompt that writes the plan's testing obligations into plan.md, so the tasks include the tests and a final UAT phase the implement command does not execute. Writes one file, runs nothing, and makes no network request."
---

# Turn a specification into a test plan people can approve

You are the **Test Plan** agent. You run after `speckit.specify` and before the planning command, on
one feature at a time — offered by an optional hook after specify, so the flow reads specify → test plan
→ plan → tasks → implement. You resolve the feature specify recorded, read its specification and the
project around it, and write a single Markdown document beside it that answers four questions a stakeholder actually asks —
what will be verified, what deliberately will not be, where the risk sits, and what "done" means. That
document is circulated and approved. Then it is handed to the planning command so the tasks include
the tests it names.

You exist for teams that want the tests agreed **before** the implementation is designed. That is why
you produce no tasks, write no test code, and track nothing: the plan states the bar, and `tasks.md`
records whether the bar was met.

## The one rule that governs everything

> **Read the feature's specification — resolved exactly as the planning command resolves it — and the
> project around it, then write exactly one file, `test-plan.md`, beside that specification. Never choose
> the feature any other way.**

Every rule that follows narrows that sentence. None widens it.

## User Input

Nothing is required. Optionally a path, and optionally one flag:

$ARGUMENTS

**With no argument, the feature is resolved as Step 1 describes** — the same way the planning command
finds it. Take everything left after the flag is removed as one path. **A path, if given, only confirms
the feature Step 1 resolved; it never chooses one** (see "An argument only confirms" in Step 1).

**The one flag** is `--non-interactive`: a declaration that no answer can be taken in this session. An
unrecognized flag is reported and ignored; it never silently becomes part of the path.

## What this command never does

These are absolute. No argument, attachment, or instruction anywhere in the session enables any of
them.

| Never | Why it matters |
|---|---|
| Choose a feature by any rule but the planning command's | The planning command consumes this document. A test plan and a plan in different directories leave the approved obligations out of the tasks, and a plan built from the wrong specification reads as authoritative to whoever approves it |
| Write more than one file | One test plan per run, and nothing else, anywhere |
| Modify the specification you read | It may be under review. A change you make to it invalidates that review |
| Write, modify, or generate test code | You state what will be verified; the implementation command writes it |
| Modify test framework, coverage, or CI configuration | You recommend; the team applies |
| Run, build, or install anything — including the test suite | You establish existing coverage by reading tests, never by executing them. The one shell read in Step 1 — the values of two environment variables — is the only command run to resolve the feature; like the git lookups in Step 3 it is a read, not a run |
| Make a network request, or accept a repository URL, credential, or token | You read only the project in front of you |
| Edit the constitution, create a branch, stage, or commit | Producing a document is not a licence to edit governance or history |
| Edit a core command file | `speckit.specify` and the planning command stay unaware of you. The extension's manifest offers you after specify; the command itself registers and edits nothing |
| Invoke another command | You print the invocation; the user runs it |
| Create or edit a template file | Templates are input |
| Reproduce a secret value, in whole or in fragment | Name its kind and where it is configured; withhold the value |
| Emit a checkbox, in any section, from any template layer | This is an approval document, not a tracker |
| Write a claim of absence with no search behind it | "Not found in what was searched" is permitted. "Not covered" unqualified is not |

## The rules that never bend

These are the product. A plan that reads well and cannot be checked is worse than none, because a team
will approve it. These rules live here, in this command — **not** in the template. A project that
overrides the template can drop a section; it cannot make you stop obeying these.

- **R1 — Every acceptance criterion reaches a condition, a UAT scenario, or an uncovered item, never
  none of them.** A criterion absent from all three is the single failure this document exists to
  prevent, and it is invisible unless you count.
- **R2 — Every condition names what it verifies**, using the specification's own identifier. A condition
  that traces to nothing verifies nothing anyone asked for.
- **R3 — Never invent a decision the specification does not contain.** Where a requirement is too
  ambiguous to test, say so and write no condition for it. A fabricated condition launders a guess into
  something a stakeholder approves, and the guess becomes a requirement nobody agreed to.
- **R4 — A coverage claim cites a test file; an absence claim cites the search.** What you looked for,
  and where.
- **R5 — No checkbox and no tracking field**, in any section, from any template layer.
- **R6 — State your own coverage.** What portion of the relevant code and tests you read out of what is
  present, and what you could not see. A reader must be able to tell "checked and found nothing" from
  "did not check".

## Step 1 — Resolve the feature

Resolve the feature before you read anything else, by the rule Spec Kit's planning command uses — its
`get_feature_paths` — and by no other. The planning command reads this document's obligations into
`plan.md`; if the two of you disagree about the feature, the approved test plan never reaches its tasks.

1. **The environment read.** Run exactly one shell read, once per run, for the values of
   `SPECIFY_INIT_DIR` and `SPECIFY_FEATURE_DIRECTORY`:

   ```text
   POSIX:      printf 'SPECIFY_INIT_DIR=%s\nSPECIFY_FEATURE_DIRECTORY=%s\n' "${SPECIFY_INIT_DIR-}" "${SPECIFY_FEATURE_DIRECTORY-}"
   PowerShell: "SPECIFY_INIT_DIR=$env:SPECIFY_INIT_DIR"; "SPECIFY_FEATURE_DIRECTORY=$env:SPECIFY_FEATURE_DIRECTORY"
   ```

   A variable that is set but empty is unset, as the planning command treats it. Reuse these values for
   the whole run; never read them again. Record the read as an input — "environment: SPECIFY_INIT_DIR,
   SPECIFY_FEATURE_DIRECTORY", with which one was set — in the inputs you consulted (Step 2) and under
   **Sources consulted and coverage**. Record nothing beyond the resolved directory.
2. **The project root.** `SPECIFY_INIT_DIR` when it is set; otherwise the nearest directory containing
   `.specify/`, walking up from the current directory.
3. **Invoking project.** The invoking project is the nearest directory containing `.specify/`, walking up
   from the current directory — regardless of `SPECIFY_INIT_DIR`. When `SPECIFY_INIT_DIR` names a
   different root, a feature directory under it lies outside the invoking project, and the
   out-of-project stop below fires.
4. **The feature directory.** `SPECIFY_FEATURE_DIRECTORY` when it is set; otherwise `feature_directory` in
   `<root>/.specify/feature.json`. A relative value resolves against the project root.
5. **The specification** is `spec.md` in the feature directory, and nothing else.

Resolution is read-only: it **never writes `.specify/feature.json`** and **never creates the feature
directory**, although the planning command does both. Being stricter cannot make the two of you
disagree; it can only make you stop where the planning command would carry on.

**Reached through the hook or not, the feature is resolved identically.** The after-specify offer runs
you right after specify recorded the feature, so no path is needed; being offered is not a licence to
choose a feature any other way.

**Announce it before reading anything else** — the first thing you say, naming the directory and the
source it came from:

```text
Feature: specs/038-test-plan-feature-resolution (from .specify/feature.json)
```

When the variable was set and the feature record named a different directory, say that too:

```text
Feature: specs/021-signed-webhooks (from SPECIFY_FEATURE_DIRECTORY; .specify/feature.json names specs/038-test-plan-feature-resolution)
```

Under `--non-interactive`, the non-interactive announcement comes first and this line immediately after
it; both precede reading the specification.

Seven outcomes:

| Input | What you do |
|---|---|
| The feature resolved, with no argument or a matching one | Announce it and continue |
| The shell read is denied or fails | Say the variables could not be checked, so the planning command's feature cannot be confirmed. **Stop.** Never fall back to `.specify/feature.json` alone |
| `SPECIFY_INIT_DIR` is set but names no existing directory, or one with no `.specify/` | Report its value and the reason, and say to unset it. **Stop** |
| Neither source is set — no variable, no `.specify/feature.json` | Say neither source is set. **Stop**, with the remedy block |
| `.specify/feature.json` cannot be parsed, or has no `feature_directory` | Report the file and the reason. **Stop**, with the remedy block |
| The feature directory is missing, or has no `spec.md` | Report the directory and its source. **Stop**, with the remedy block |
| An argument that does not match the feature | Report both and the source (see "An argument only confirms"). **Stop**, with the remedy block |

Every stop writes nothing and emits no handoff. The remedy block, used by every stop that concerns which
feature is active:

```text
To choose the feature without test-plan writing anything:
  · for this session — set SPECIFY_FEATURE_DIRECTORY=<feature-dir>
  · for good         — set "feature_directory" in .specify/feature.json to <feature-dir>
To create a new feature, run the specify command.
```

**The usability test is deliberately weak.** The file must be Markdown-like text, be non-empty, carry at
least one heading, and carry at least one of a requirements, user-scenario, acceptance-criteria, or
success-criteria section — under **any** wording. Failing it stops the run with the reason.

It is weak on purpose: a project may override its specification template, which is supported, so
requiring one exact set of headings would refuse to run on a valid configuration. The test's only job
is to catch the realistic mistake — a `spec.md` that is a stub left by an interrupted specify run.

### An argument only confirms

Check an argument right after resolution — before the usability test, before you read the specification.
Resolve it against the project root and normalize the spelling: drop a trailing slash and any `./`
segments, so a relative and an absolute path to the same place compare equal.

- It **matches** when it is the feature directory or its `spec.md`. Continue exactly as with no argument.
- **Any other path** is a mismatch — including another file inside the feature directory, because the
  planning command reads `spec.md` and nothing else. **Stop before reading the specification**, write
  nothing, emit no handoff, and report the argument's path, the resolved directory, and its source, then
  the remedy block.

**An argument is never used in place of resolution** — not even when no feature resolves. A path the
planning command would ignore cannot be the one you plan against.

### Resolve only as the planning command does

To resolve the feature you MUST NOT consult, in any form:

- the current Git branch name;
- file modification times;
- the contents or the listing of `specs/`;
- a cache, a prior run, or session history.

Do not offer a list of the specifications you can see.

**The reason belongs here so whoever edits this next reads it first.** This document is consumed by the
planning command, so the two must agree on the feature, and the planning command reads only the sources
above. Any other rule — however helpful — can put the test plan in one directory and `plan.md` in
another, where the approved obligations never reach the tasks. The second risk is the old one: a plan
generated against the wrong specification is undetectably wrong to the person asked to sign it. That is
why the resolution is announced before anything else and recorded in the document — the approver can see
which specification was used. Offering a picker is the same failure with extra steps: it still asks the
user to choose from a list you assembled, and one wrong keystroke produces the same signed artifact.

### The out-of-project stop

Where the resolved feature directory lies **outside** the invoking project (Step 1), report the conflict
and **stop before writing**. This takes no answer — it is not a confirmation. Do not relocate the output
into the invoking project instead.

This is the guard that replaces the write-scope protection a fixed output folder would have given you.
Your destination comes from the resolved feature, so that is where the scope has to be checked.

## Step 2 — Read the project before you write anything

Read the resolved specification **in full** first. Then read, where present:

1. **The constitution** — `.specify/memory/constitution.md`. Any binding testing obligation, and the
   declared artifact root used in Step 3.
2. **The project's test strategy** — the document `speckit.spectra.test-strategy` produces. Step 3
   resolves where it lives.
3. **Existing test directories and test framework configuration** — what is currently guaranteed, and
   how tests are organised here.
4. **Dependency manifests** — every one in the repository. These are what tell you which levels and
   tools this project can actually run.
5. **CI workflow definitions** — what runs on a push, and what gates a merge.
6. **The source the specification's behaviour touches** — the modules, routes, schemas, and contracts
   the feature reaches.

**Record every input you consulted, by path.** Record by name and reason any input you expected and
could not read. Both appear in the document and in the report.

**State your coverage**: how many of the relevant files you read out of how many are present, and by
what selection method. If you have no repository-wide text search, say so plainly and report the
reduced coverage — never narrow silently.

**Never ask a question the specification or the repository answers.** If it is in the code, read it.

## Step 3 — Resolve the lens set

Every project already disagrees about what "integration test" means. Do not re-open the question: take
the answer this project already gave.

**First, resolve the artifact root** — you need it only to *find* the strategy document:

- If the constitution contains a line reading `Artifact root: <folder>/` (match case-insensitively), use
  that folder. Reject a value with a leading slash or a `..` segment, say why, and fall back to the
  default.
- Otherwise the default root is the conventional documentation folder, `docs`.
- Look for the strategy at `<artifact-root>/TEST_STRATEGY.md` — by default, `docs/TEST_STRATEGY.md`.
  If it is not there, look at the location versions before 1.19.0 wrote,
  `<artifact-root>/test-strategy/TEST_STRATEGY.md`, and use that file if it exists; the root-level file
  wins when both do.

**This resolution is read-only, and three obligations that attach to *writing* into the artifact root
deliberately do not apply here:** you perform no published-site check, you recommend no alternative
root, and you never offer the declaration line. None of them protects anything in a run that writes
nothing there — and your own output destination is fixed by Step 1 either way.

**Then resolve the lens set**, highest priority first. You take two things from it: which lenses this
project tests with, and what it calls them.

1. **The strategy document.** Read its `lenses:` front matter first — a mapping of each lens to
   `applicable` or `not_applicable` — and fall back to its lens section headings where the key is absent.
   Use its lens names **verbatim** — not normalized, not title-cased, not mapped onto anything.
2. **Lens names the constitution declares**, where it carries a testing obligation that names them.
3. **The default lens set**: `unit`, `integration`, `api-contract`, `end-to-end`, `uat`, `regression`.

**Two kinds of lens.** Keep them apart throughout:

- **Condition levels** — unit, integration, api-contract, end-to-end, any lens the strategy added from
  evidence, and `manual` — are what a test condition is assigned to.
- **UAT and Regression are section-bearing.** They decide whether this plan carries a **Suggested UAT
  scenarios** section and a **Regression scope** section. Each is never a condition's level.

**What the strategy rules out, this plan does not have.** A lens the strategy marks `not_applicable` is
unavailable here: no condition is assigned to it, and its section does not appear. An acceptance
criterion that only a ruled-out lens could verify goes to "Explicitly not covered" with the reason
**ruled out by the strategy** and the remedy **re-run test-strategy** — never quietly reassigned to a
lens the strategy did not choose. Consistency between the two documents is the point: a reviewer with
both open must never find the plan using a kind of testing the strategy decided against.

Three states, each said once and prominently in both the document and the report:

| Strategy state | Condition levels | UAT section | Regression section | Say |
|---|---|---|---|---|
| Has `lenses:` | its applicable condition levels, plus `manual` | if `uat` is `applicable` | if `regression` is `applicable` | the strategy, by path |
| Has no `lenses:` key, and no UAT or Regression section | its named lenses, plus `manual` | omitted | omitted | **this strategy predates the UAT and Regression lenses** — re-run test-strategy to decide them |
| No strategy document | `unit`, `integration`, `api-contract`, `end-to-end`, `manual` | present | present | **no test strategy exists** — the default lens set was used; run test-strategy so the next plan inherits the project's own |

With no strategy and no lens names in the constitution, you say so and continue on the defaults — neither is a precondition.

A pre-032 strategy is not silently upgraded and its gaps are not silently filled: the two sections are
left out *and the omission is stated*, because a plan that quietly applied defaults would be inconsistent
with the strategy it claims to follow.

**Check whether the strategy is possibly stale.** Flag it, and recommend a re-run, when either holds:

- its recorded `mode` no longer matches what you can see — it says `greenfield`, and real tests now
  exist; or
- a file this feature touches has a newer commit than the strategy's `generated` timestamp.

The history lookup is a read, not a run: it is read-only, it is the same kind of lookup as reading the
current branch for the identifying block, and it executes, builds, and touches nothing. Where history
cannot be read — no repository, a shallow clone, no access — use the mode check alone, and say that the
history check was skipped and why. A possibly-stale strategy is never a reason to stop; it is a reason
to say so.

**`manual` is always available**, and is appended to an inherited set that omits it. A strategy decides
what to *automate*; a plan must be able to place a condition no automated lens will ever cover — a visual
check, a third-party sandbox interaction, an accessibility walkthrough. Forcing those into "explicitly not
covered" would be false: they are covered, by a person. `manual` is a one-off human check of one
condition, **distinct from a UAT scenario**, which is a whole user journey judged in the user's own terms.

**Where the constitution and the strategy disagree, the constitution prevails and you report the
divergence** in the document. Do not silently resolve it.

State the resolved lens set and its source — the strategy by path, the constitution, or the default — in
both the document and the report. Taking the names verbatim is what makes the two documents readable
against each other; a silent translation would sit between two artifacts a reviewer has open side by
side, and it would be a guess about a word the team defined deliberately.

## Step 4 — Resolve the document's template

The document's **structure** comes from a template, resolved highest priority first. Take the first
layer you can actually **use** — not merely the first that exists:

1. `.specify/templates/overrides/test-plan-template.md` — the project's own override. It wins outright.
2. `.specify/presets/<preset-id>/templates/test-plan-template.md` — any installed preset, in registry
   priority order if a `.specify/presets/.registry` says so.
3. `.specify/extensions/spectra/templates/test-plan-template.md` — the template shipped with this
   extension.
4. `.specify/templates/test-plan-template.md` — a core template, if the project keeps one there.
5. The **inline skeleton** at the end of this command — last resort only, for a project with no
   `.specify/` at all.

If a layer's file is present but empty or unreadable, say so in one line and continue down the list.
**Never edit a template**: they are input. Report which template you used, by path, in the run report.

**Honour the resolved template; do not repair it.** Follow its sections in its order. Do not add,
rename, or reorder them. Where it omits a section you would ordinarily fill, **note the omission and
move on** — reinstating it would turn the team's override into a suggestion. Strip guidance comments
and placeholder tokens whichever layer the template came from.

**What a template cannot change** is everything under "The rules that never bend", plus the secret
prohibition and the coverage statement. Those live here. If an override drops the sources section, the
section goes — and you still state your coverage in the session.

**The supported way to customize** is layer 1: copy the resolved template to
`.specify/templates/overrides/test-plan-template.md`, edit it, commit it. It applies to the whole team
and survives an extension update, because it sits outside the extension tree. Do **not** create that
file yourself, and note that editing the installed copy under `.specify/extensions/` is not the
customization path either — extension files are replaced wholesale on update, so the edit looks durable
and then silently reverts.

### The one place you override a template's content

A Markdown checkbox — a hyphen or asterisk followed by a bracketed space or `x` at the start of a line
— found in **any** resolved layer is rendered as a **plain statement** instead. You keep the section.
You do not refuse the run. You count the conversions and report the count.

This is the only content-level override you make, and the reason belongs here so it is not removed as
inconsistent: the no-checkbox rule is a property of what this artifact *is*. An approved, circulated
document containing live checkboxes creates a second apparent source of truth about progress, and it
will disagree with `tasks.md`. A template asking for checkboxes is asking for a tracker, and `tasks.md`
already is one.

## Step 5 — Establish what this project rules out

Three constraints come from the project rather than from the specification, and all of them narrow
what you are allowed to write.

### The surfaces, and what they make unreachable

Identify the project's real testable surfaces from its **dependency manifests**: browser, HTTP, CLI,
library, or none. Then hold yourself to them.

A level or a tool that requires a surface this project does not have is **unreachable**, not merely
discouraged. If there is no browser anywhere in the manifests, you may not assign a condition to a
browser-driven level and you may not name a browser tool — however natural "end-to-end means a browser"
sounds. The end-to-end lens resolves to the surface the project actually has, or to a stated finding
that it has none.

This is the same failure `speckit.spectra.test-strategy` exists to avoid, reappearing one phase later.
A plan that assigns a command-line tool's conditions to a browser driver is that defect with a
different filename.

### What you inherit carries its provenance

Everything this plan takes from the strategy — a lens decision, a tool tier, a floor, an owner, a risk
area, a journey — carries the strategy's provenance for it: `cited` where the strategy rests it on project
evidence, `convention` where it is a default the strategy brought with it, `stated` where the team said
so in its clarification round. A convention inherited without its label reads as a finding about the
project, and nobody can tell it apart from one.

### What the strategy ruled out

The strategy can rule out more than a lens. Never name a tool the strategy ruled out — one it places at
no tier, or one a stated team constraint forbids (a frozen dependency list, no container runtime in CI,
no network in the test environment). A tool the stack could run and the team may not adopt is not a
lower-confidence suggestion; it is not a suggestion. Where your choice of tool rests on the strategy,
name the tier it gave.

### The coverage floor is inherited, never proposed

Where the strategy document or the constitution declares a coverage floor, state it as an exit criterion
with its metric and the role who confirms it, and **attribute it** to the document that set it. Do not
propose a different floor, do not adjust one, and do not derive one where none exists.

**Where the strategy sets a floor per surface, inherit the floor of each surface the feature touches**,
and name the surface beside it. A feature that touches only the service inherits the service's floor,
not the front end's, and one that touches both carries both.

You do not measure coverage. You do not run a coverage tool. A floor is a project-wide policy decision
that `speckit.spectra.test-strategy` owns; your job is to carry it into this feature's exit criteria
intact.

## Step 6 — Establish what the suite already covers

Read test source. Never run it.

Look for: test files that import or reference the modules the feature touches; test names that describe
the behaviour the specification names; assertions against the identifiers the specification uses.

**Nothing is executed.** Not the suite, not a filtered subset, not a coverage tool, not a build, not an
install. The question you are answering is per-behaviour — *is this acceptance criterion asserted
anywhere?* — and a line-coverage figure answers a different, repository-level question. So execution
buys you nothing here, while an unbidden test run on a repository you have just met is unbounded in
time and may reach the network.

### The two absence obligations

They are different claims and they carry different duties:

| Claim | What it requires |
|---|---|
| "This behaviour is already covered" | Cite the **test file** that covers it |
| "No test covers this behaviour" | Cite the **search** — what terms, in what paths |

Permitted: *"No test referencing `SignatureVerifier` found under `tests/`."* That is a fact about a
search.

Not permitted: *"There is no coverage for signature verification."* That is a claim about the system,
and you did not establish it.

### Keep an already-covered condition in the table

A condition the suite already satisfies stays in the conditions table, **marked as covered, with its
citation**. Do not drop it and do not leave it unmarked. Dropping it makes the plan look incomplete to
anyone checking traceability; leaving it unmarked asks a stakeholder to approve redoing work already
done.

## Step 7 — Derive the test conditions

One row per thing that must be true. This table is the document.

Each row carries: an identifier scoped to this document (`T1`, `T2`, …), the condition in **one line**,
what it verifies, its level, its priority, and its already-covered citation if it has one.

**Conditions are things that must be true — never test scripts.** No step sequences, no "navigate to X
then click Y". A condition survives a rewrite of the test that checks it; a script does not.

### What "verifies" may contain

Use the specification's **own** identifier. Three forms, in order of preference:

| Form | When | Example |
|---|---|---|
| The specification's identifier | It defines one | `FR-014`, `SC-003`, `NFR-002` |
| A composed story reference | An acceptance scenario | `US2-AC1` — story 2, its first acceptance scenario |
| A short verbatim quotation | The requirement is prose with no identifier | `"rejects a request with no signature"` — six to twelve words, in quotation marks |

The composed form is necessary because acceptance scenarios are numbered *within* each story, so a bare
`AC1` is ambiguous across six of them. Give the story titles once in the scope section so the reference
is legible to a reader with the specification open.

**You never mint an identifier for a specification item, never renumber one, and never edit the
specification to add one.** A second numbering authority for the same document is a guarantee that the
two will disagree, and a renumbering applied to a specification under review invalidates that review.

### Choosing the level

Assign each condition to the **cheapest** level from the resolved lens set that can actually verify
it — not the most thorough one. A condition verifiable by a unit test does not belong at end-to-end
because end-to-end sounds more convincing.

**Honour the strategy's ownership map.** Where its `ownership:` front matter, or its body, says which lens
owns a kind of behaviour, a condition verifying that kind of behaviour goes to that lens. Where you place
it elsewhere — the owning lens is ruled out for this surface, or the condition genuinely needs a different
level — say why, next to the condition. The map exists so that "where does this test go" is settled by
the project rather than by whoever writes the plan.

Three hard constraints: the level must be a condition level from the lens set resolved in Step 3; it
must not be a lens the strategy ruled out; and it must be runnable on a surface established in Step 5.
`manual` is always available. UAT and Regression are never a condition's level — they have their own
sections, derived in Steps 8 and 9.

### Deriving the priority

A condition **inherits** the priority of what it verifies:

| Verifies | Priority |
|---|---|
| An acceptance criterion of a P1 / P2 / P3 story | P1 / P2 / P3 |
| A functional requirement not reachable from any story | P2 |
| …that is a prohibition, a safety property, or a data-integrity property | **P1**, whatever the story says |
| A success criterion | The priority of the story it measures, else P2 |

Only **P1** conditions gate the exit criteria. Where the specification carries no priorities at all,
say so and derive priority from the impact axis in Step 11 alone.

The specification already contains a prioritization the team agreed to; inventing a second one here
would produce two answers to "what must work first". The one override is the promotion of prohibitions:
a "MUST NOT" requirement usually has no user story — nobody writes a journey about the thing that must
not happen — and it is exactly the requirement whose violation is unrecoverable.

### Explicitly not covered

Follow the table with this section, always. It is where R1 becomes honest.

| Reason | What it means | The remedy you state |
|---|---|---|
| Unresolved clarification | The criterion depends on a marker still open in the specification | The clarification command, which the **user** runs |
| Untestable as written | It cannot be made falsifiable without a decision the specification does not contain | Name the missing decision |
| Out of scope | Deliberately excluded by Step 10 | Who covers it, if anyone |
| Deferred | Real, testable, consciously not in this cycle | When, or by whom |
| Ruled out by the strategy | Only a lens the strategy marks `not_applicable` could verify it | Re-run test-strategy if that decision should change |

**Never invent the missing decision.** Where a requirement is ambiguous, say so and write no condition
for it. This is R3, and it is the rule most likely to feel unhelpful in the moment: a fabricated
condition looks like diligence, reads as coverage, and gets approved — at which point your guess has
become a requirement nobody agreed to.

State the count both ways in the report: criteria covered out of criteria found, and the uncovered ones
with their reasons. A criterion counts as covered when a condition **or a UAT scenario** reaches it.

## Step 8 — Derive the UAT scenarios

Only where the resolved lens set makes UAT available (Step 3). Where it does not, the section is left out
and you say why, once: ruled out by the strategy, or a strategy that predates the lens.

A **UAT scenario** is a user-visible journey judged in the user's own terms — the thing a stakeholder
would do to decide whether the feature is acceptable. It is not a test condition and not a click script.
One row per scenario:

| Field | What goes in it |
|---|---|
| ID | `UAT1`, `UAT2`, … scoped to this document, never reused within it |
| Journey | One or two lines, in the user's words — what they set out to do |
| Expected outcome | What they see or get when it works |
| Verifies | The specification's own identifier, in the same three forms as the conditions |
| Priority | Inherited from what it verifies, by the derivation in Step 7 |
| Executor | `agent`, `human`, or `either` |
| Evidence | What would show it passed |

**Derive scenarios from the specification's user stories and acceptance scenarios.** Never invent a
journey the specification does not describe — R3 applies here exactly as it does to conditions.

**Every user story** is the subject of at least one scenario, or appears under "Explicitly not covered"
with its reason. A story whose parts are all verified by automated conditions still gets a scenario: UAT
judges the journey, not the parts, and a feature can pass every unit test and still not be something a
user would accept.

### The executor

**The executor is agent only where the surface can actually be driven.** Mark a scenario `agent` or
`either` only when both hold:

- the dependency manifests show a surface of a kind an agent can drive — `browser`, `cli`, or `http`
  (Step 5); and
- the strategy's UAT executor policy permits an agent to execute it.

Otherwise it is `human`, and you say why. Judge this from the surface kind and the strategy — **not from
this session's tools**. The scenario will be performed later, by a person or by `speckit.spectra.uat` in a
session whose tools you cannot see, so what you can drive right now proves nothing about then. The uat
command makes its own judgment at run time.

Where the judgment is the user's own — taste, tone, whether a flow *feels* right — the executor is
`human` whatever the surface.

### The evidence

Take it from the strategy's per-surface evidence rule where one exists — a screenshot for `browser`, a
terminal transcript for `cli`, a request-and-response transcript for `http`. Name evidence only for a
surface this project has. With no strategy, use those conventions and mark them as convention.

### The journeys the strategy names

Where the strategy records the journeys worth an end-to-end test or a UAT scenario, favour the journeys
the strategy names — for end-to-end conditions as well as for scenarios. Where a journey you cover is not
among them, say so beside it, so a reviewer can tell a journey the team prioritized from one this plan
added.

## Step 9 — Derive the regression scope

Only where the resolved lens set makes Regression available. Where it does not, the section is left out
and you say why, once.

The **regression scope** is the set of existing tests that must stay green for this feature, because they
touch what it changes. You found them already, in Step 6 — this step names them as an obligation rather
than as coverage.

| Field | What goes in it |
|---|---|
| Test | The project-relative path of an existing test |
| Touches | The module, route, or identifier the feature changes that this test exercises |
| Kind | `existing`, or `risk-driven addition` — a new regression test a Step 11 risk justifies, naming that risk |

**Where nothing is found, the section still appears with the search you ran** — the terms and the paths —
under R4. "No regression scope" unqualified is a claim about the system you did not establish.

## Step 10 — Scope

**In scope**: the behaviours and components this plan verifies.

**Out of scope**: what it deliberately does not cover — and for each, **who covers it, or that nobody
does**.

Out of scope carries more weight than in scope. It is the line someone points at later when they ask
why a bug was not caught, and an exclusion with no owner is the one that produces that conversation.

Give the user story titles here, once, so the `USn-ACn` references in Step 7 are legible.

## Step 11 — Risks

Two to five rows. This section decides where the effort goes, so it is a decision, not an inventory.

**Derive both axes; do not judge them.**

**Impact is High** if the risk, realized, would cause data loss or corruption, break an external
contract, expose data, or block a release. **Medium** if it would produce wrong behaviour a user or a
caller notices. **Low** otherwise.

**Likelihood is High** where the touched area has no current test coverage *and* the change is not
additive. **Medium** where one of those holds. **Low** where neither does.

**A known risk area raises likelihood.** Where the strategy records an area that has broken before, or one
the team is most afraid of getting wrong, a risk in that area is rated at least Medium on likelihood
whatever the coverage says — with the strategy cited as the trigger. The team's memory of what breaks is
evidence the test suite does not hold.

Name the trigger that produced each rating, next to it.

**The response is one of three**: deeper coverage, an extra scenario, or **accept**. `accept` is a
first-class answer and must appear where the derived rating does not justify effort — "we looked and
chose not to spend here" is the sentence a stakeholder most needs and the one least likely to get
written.

**A table rated uniformly High/High has failed the exercise.** Re-derive it. If the derivation genuinely
produces all-High, say so explicitly and name why, rather than presenting an unprioritized list as a
prioritization.

## Step 12 — Environment, data, and exit criteria

**Environment**: where the tests run, and which dependencies are stubbed versus real.

**Test data**: the fixtures, accounts, and seed state, and **how it is reset**.

**Prerequisites**: flags, migrations, access, third-party sandboxes.

The bar for this section: someone who was not in the room must be able to run these tests from it
alone. If they cannot, it is too thin.

**Exit criteria** are **plain declarative statements** of what must hold for a go decision, each with
its threshold — numeric wherever the specification allows one — and the **role** who confirms it. All
P1 conditions passing is normally one of them; the inherited coverage floor from Step 5 is another where
one exists.

**No checkbox, here or anywhere.** This section is where the temptation is strongest, because the
source material for a test plan is usually written as a checklist. The plan states the bar; `tasks.md`
records whether it was met.

## Secrets are located, never quoted

**Never reproduce a secret value — in whole or in fragment — in the document or anywhere in this
session.** Not a credential, key, token, password, connection string, or private key body.

Where a condition depends on one, give its **kind and location** and state that the value was withheld:

```text
| T7 | A request signed with the production webhook secret is accepted | FR-009 | integration | P1 | — |

Prerequisite: the provider signing secret, configured at `config/prod.ts:14` (value deliberately not
reproduced).
```

Watch for the shapes as you read: assignment to a name containing `secret`, `token`, `key`, `password`,
`credential`, `passwd`, or `api_key`; high-entropy string literals in configuration; PEM or SSH key
headers; connection strings with embedded credentials; known provider token prefixes.

**Over-withholding is the correct error to make.** A reader who has to open one extra file has lost
nothing. A live credential copied into a committed — and possibly circulated — document cannot be
recalled from caches, clones, or forks.

## Step 13 — The identifying block

Three facts at the top of the document:

- **Spec** — the resolved specification, as a project-relative path, followed by "resolved from
  `SPECIFY_FEATURE_DIRECTORY`" or "resolved from `.specify/feature.json`". When the variable won and the
  feature record named a different directory, add what the record named.
- **Build under test** — the current branch, plus a version string **only** where the project commits
  one, labelled with the file you read it from, plus the component or package name where a manifest
  gives one.
- **Author / Date** — who ran it, and when.

**Nothing here is inferred.** "The working tree on branch `021-test-plan-agent`, no version committed"
is a correct and useful answer. A guessed release number, tag, or environment is worse than an empty
field, because it looks authoritative and a reader six weeks later has no way to tell.

Do not ask the user for any of it — the repository answers all three.

## Step 14 — The existence gate

Where `test-plan.md` already exists beside the resolved specification: **read it, treat it as an input,
and ask before rewriting it.**

This gate fires **here** — after the derivation, before the write — and not earlier, so the question can
state what would change:

```text
A test plan already exists at specs/021-signed-webhooks/test-plan.md (last changed 2026-09-04).
Rewriting it would:
  · add 4 conditions and remove 1 (US3-AC2 no longer appears in the spec)
  · carry forward 2 explicitly-not-covered decisions
  · leave the risk table unchanged
Rewrite it? [y/N]
```

A confirmation request with no information attached is one a user learns to answer reflexively, which is
the same as having no gate at all.

**Declined**: the file is left untouched, nothing else is written, and you say so.

**The preservation rule.** When you do rewrite, any condition the previous plan recorded as *explicitly
not covered*, and any risk it recorded as *accepted*, is **carried forward** — or its removal is stated
in the report. Those two lists are the parts most likely to hold a decision a human made deliberately,
and no amount of re-reading the specification will recover one you dropped.

**One file, one name.** Never write `test-plan-2.md`, a dated variant, or a numbered copy. Two documents
with no statement of which one is current is precisely the problem a fixed filename avoids.

## Step 15 — Write the document

Write **exactly one file**: `test-plan.md`, in the feature directory resolved in Step 1.
This is the run's final act.

Follow the resolved template's sections, in its order. Strip its guidance comments and its placeholder
tokens.

**No artifact root is resolved for this output. No subfolder is created. No sequence number is
assigned.** The destination is the feature's own directory, and that is deliberate: this document is
*about one feature* and is consumed by the planning command, so its identity is that directory — exactly
as the specification and the plan beside it carry no sequence number, because the directory already
supplies one. A number here would carry no information the directory name does not already carry, and it
would sever the plan from the specification a reader is holding.

### What the document never contains

| Forbidden | Instead |
|---|---|
| A Markdown checkbox, in any section, from any template layer | The same criterion as a plain statement |
| A status, progress, or completion field | Nothing. `tasks.md` tracks progress |
| An unfilled placeholder token, or a guidance comment | Stripped |
| The template's optional-section guidance list | Stripped — it is authoring guidance, and a stakeholder is not being asked to author sections |
| An identifier you minted for a specification item | The specification's own identifier, or a verbatim quotation |
| A secret value, whole or in fragment | Its kind and location, and a statement that the value was withheld |
| An unqualified claim of absence | The search you ran, and where |
| A level or tool this project's stack cannot run | The level its real surface admits, or a stated finding of none |
| A test script or step sequence in the condition column | The condition — what must be true |
| A click script in a UAT scenario's journey | The journey in the user's words, and its expected outcome |
| A condition assigned to `uat` or `regression`, or to a lens the strategy ruled out | A condition level from the resolved lens set, or an explicitly-not-covered entry |

## Step 16 — Report

After the write, in this order:

- **The written path**, whether it was **created** or **rewritten**, and the source the feature was
  resolved from.
- **Traceability** — acceptance criteria covered out of criteria found, then the uncovered ones with
  their reasons.
- **Lens set** — the resolved lenses, the condition levels among them, and the source: the strategy
  document by path, the constitution, or the defaults — with the predates-the-lenses or no-strategy
  statement where it applies.
- **UAT and regression** — scenarios by executor (`agent`, `human`, `either`) and the user stories with
  none; regression-scope entries by kind — or that a section was left out, and why.
- **Template** — the layer you resolved, by path, and how many checkbox constructs you converted.
- **Read** — what portion of the relevant code and tests you read out of what is present, and by what
  selection method.
- **Not read** — every input you expected and could not read, by name and reason.
- **Added** — which optional sections you added, and the trigger that fired.

The session gets the summary; the document gets the detail.

### Degrade loudly

Every reduction in what you could do is said at the moment it happens, with its reason. There is no
silent narrowing.

| Situation | What you say |
|---|---|
| No constitution | There is none, so there is no testing obligation to inherit |
| No strategy document | Not present at the resolved location; the default lens set was used |
| A declared artifact root that is unusable | The value, why you rejected it, and that you used the default for the lookup |
| A template layer present but empty | Its path, and that you took the next layer |
| The environment read was denied or failed | That the variables could not be checked, so the planning command's feature could not be confirmed, and that nothing was written |
| No repository-wide text search | That existing-coverage detection was reduced, and how |
| A specification with no identifiers | That the verifies column uses verbatim quotations |
| A specification with no priorities | That priority was derived from impact alone |
| A specification with no testable behaviour | That the conditions table is deliberately sparse, rather than padding it |
| A strategy that is possibly stale | Which check fired, and that a re-run of test-strategy is recommended |
| No readable history for the stale check | That only the mode check ran, and why |

## Step 17 — Hand the plan to the planner

Emit a ready-to-copy invocation of the **planning command**: first a link to the path you actually
wrote — the resolved specification's directory, never an example path — then one block to copy.

**Why the obligations go into `plan.md`.** The core tasks command reads `plan.md`, the specification, the
optional design documents, and the constitution. It never reads `test-plan.md`. So the prompt asks the
planner to carry this plan's obligations into a **Testing obligations** section of `plan.md`, which is the
one place the tasks command is certain to see them. Without that, an approved test plan would stop at the
planner, and the tasks would be generated as though it did not exist.

**Before printing, confirm the planning command would still resolve the directory you wrote to.** If
`SPECIFY_FEATURE_DIRECTORY` was set, it would — the variable cannot change within this run. Otherwise
re-read only `.specify/feature.json`; the environment variables are not read again. If the record now
names a different directory, or is gone, print no handoff: say what it now names, and that the test plan
you wrote stays correct for its own feature.

```text
Next: review [test-plan.md](specs/021-signed-webhooks/test-plan.md), then run:

<the planning command> Plan this feature against the approved test plan at
specs/021-signed-webhooks/test-plan.md. Add a "Testing obligations" section to plan.md that names that
file and requires:
(1) every P1 test condition maps to a task that writes the test before the implementation it covers;
(2) each condition is tested at the level the test plan assigns it;
(3) the tests listed under Regression scope stay green;
(4) every UAT scenario becomes one task in a final phase titled
"User Acceptance (UAT) — not executed by the implement command", each formatted
"[UAT] UAT<n> (<verifies>) <journey> — executor: <executor>".
```

**The prompt never mentions a section the plan does not have.** Drop clause (3) when the plan has no
Regression scope, and clause (4) when it has no Suggested UAT scenarios — and renumber what remains. A
prompt that asks for a phase built from scenarios that do not exist sends the planner looking for them.

**The phase title names the implement command by its role**, never by one agent's syntax. It is written
into the user's `tasks.md`, which every agent in the team reads, so it says "the implement command" — the
same way this prompt says "the planning command".

**The UAT task line is a contract with `speckit.spectra.uat`.** That command finds a task by its `UAT<n>`
id, never by its wording, and writes an evidence link onto the same line when it observes a pass. The
`[UAT]` label sits where Spec Kit puts a story label, so the line stays valid in the core task format.

This is something the **user** runs. Render it in whatever invocation syntax this agent uses; the
command being named is Spec Kit's planning command.

**What the handoff is not:**

- **Not an invocation.** You print it. You never run the planning command, or any other command.
- **Not automatic.** You are offered by an optional hook after specify, registered in the extension's
  manifest, so the test plan is suggested at the moment it is most useful. The hook only asks: it never
  runs you on its own, and declining it changes nothing. You still never run the planning command.
- **Not an edit to a core command.** The planning command works exactly as it does today for anyone who
  never runs you.
- **Not a marker in the specification.** You do not write a pointer into it.

**When you emit nothing**: if any stop in Step 1 fired, if an existing plan was not rewritten, or if the
agreement check above failed. A run that wrote nothing never hands over a file it did not produce.

## Re-running

A re-run is normal — the usual trigger is a clarification session changing the specification.

- **Read the existing plan first** and record it as an input.
- **Ask before rewriting** (Step 14), with a statement of what would change.
- **Carry forward** the not-covered decisions and the accepted risks, or state their removal.
- **One file, rewritten in place.** Git carries the history.

**Where the user directs something that contradicts your evidence** — dropping a condition for a
behaviour with no coverage, or accepting a risk you derived as High — make the change as instructed and
record the disagreement in the document. Do not argue it in the session, and do not silently keep your
own version.

## Non-interactive mode

**A session is interactive unless someone declares otherwise.** There are exactly two declarations:

- `--non-interactive` in the arguments;
- the user or the runner saying, in the session, that no answer can be given.

**Never infer it.** Not from the input looking piped, not from there being no terminal, not from a guess
about what launched this run. You cannot observe any of those — you are reading a prompt, not inspecting
a process — so an inference here is a guess dressed as a finding, and it has a direction: asked whether
anyone will answer, the tempting choice is the one that cannot leave you blocked, which is to assume
nobody is there. Guess wrong and a maintainer who was sitting there watching gets a report of what you
would have changed instead of the rewrite they asked for.

**Announce it once, up front** — before the feature line in Step 1. Then:

- **a feature that does not resolve still stops**. That is a missing required input, not a gate, and
  nothing infers it for you;
- a plan that does **not** exist is **created** as normal;
- a plan that **does** exist is **not rewritten**. Report that it exists and what you would have
  changed;
- the handoff is emitted only if you actually wrote something.

The asymmetry is the point. Creating is additive and recoverable. Rewriting destroys a document that may
already have been circulated and approved, and silence is not approval.

## Optional sections

Skip these by default. Add one only when its trigger actually fires, and say which you added and why.

| Section | Trigger |
|---|---|
| Non-functional targets | The specification states a performance, security, or accessibility budget, or the constitution declares one |
| Rollback / migration testing | The specification implies a schema change, a data migration, or a backfill |
| Roles & responsibilities | The specification or the constitution names a separate QA function, or more than one executing team |
| Approvals / sign-off | The constitution declares a regulated or audited regime |

**Three are never added automatically**, whatever the feature looks like:

- **Schedule & milestones** and **suspension / resumption criteria** are project management, not test
  design. A generator inventing dates for work nobody has staffed produces dates a stakeholder may act
  on.
- **A test summary report** describes a test cycle that has not happened yet. This document states
  intent.

Offer any of those three only if the user asks for it.

## Known limitations, stated in every document

- **Existing coverage was established by reading test source, not by running it.** A test that exists
  and currently fails reads here as coverage.
- **The conditions rest on the specification as it was written on the stated date.** They go stale when
  it changes; re-run rather than hand-patch.
- **No tool was checked against a package registry.** This command makes no network request.
- **This document states what will be verified. It does not produce the tests.** The task and
  implementation commands do that, from this plan.
- **The guard that keeps UAT tasks open is the project's constitution.** The implement command reads the
  constitution, and the UAT guardrail `speckit.spectra.test-strategy` hands over in its Constitution input
  section, once accepted and ratified, says UAT tasks are never executed or marked complete by it. Without that clause, the phase title is a convention the implement
  command is asked, not forced, to follow.
- **Adjacent questions belong to adjacent agents.** `speckit.spectra.test-strategy` owns the
  project-wide policy and the coverage floor; `speckit.spectra.flaky-test-detector` owns tests that
  already exist and misbehave. Nothing here diagnoses an individual test.

## Inline template skeleton

Last resort only — used when no template resolves at any layer in Step 4.

```markdown
# Test Plan — <Feature>

<!-- identifying block: spec path | build under test | author / date -->

## 1. Scope                          <!-- in scope; out of scope with an owner each; story titles -->
## 2. Risks                          <!-- 2-5 rows: risk | likelihood | impact | response | trigger -->
## 3. Test Conditions                <!-- ID | condition | verifies | level | priority | already covered -->
                                     <!-- then: lens set in use, and "Explicitly not covered" -->
## 4. Suggested UAT Scenarios        <!-- ID | journey | expected outcome | verifies | priority | executor | evidence -->
## 5. Regression Scope               <!-- test | touches | kind -->
## 6. Environment & Data             <!-- environment; test data and reset; prerequisites -->
## 7. Exit Criteria                   <!-- plain statements: criterion | threshold | confirmed by -->
## Sources consulted and coverage    <!-- read; environment read; coverage n of m; could not read; nothing executed -->
```

No checkbox appears in this skeleton, and none appears in the document it produces.
