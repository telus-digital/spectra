# Tasks: Defect Root Cause Analysis Agent

**Input**: Design documents from `/specs/022-defect-rca-agent/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md),
[data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md)

**Tests**: Included, and not optional here. FR-066 requires it, and this repository enforces Principles
V, VII and VIII with a Python suite whose checks derive from per-command registries —
`tests/test_doc_output_paths.py`, `tests/test_document_templates.py`, `tests/test_roster_data.py` — so a
new document agent absent from them is unguarded. Test tasks are in Phase 11.

**Organization**: by user story, in the priority order the spec assigns. One caveat particular to this
project: the runtime deliverable is a **single Markdown file**, so most tasks add a section to
`spectra/commands/defect-rca.md` and are therefore **strictly sequential within a phase**. Genuine
parallelism appears in Phase 10 (publishing, different files) and Phase 11 (tests, different files).

**The one item to carry through**: unlike spec 021, this command **joins `CANONICAL`** in
`tests/test_doc_output_paths.py` as `"defect-rca.md": "docs/defect-rca/"` (T070). That single dict entry
enrols the command in every Principle VII sweep the module runs, and those sweeps assert on **literal
strings in the command file**. Six of them are hard requirements on the prose, listed under Path
Conventions below. Write them exactly, or the entry fails the moment it is added.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel — different file, no dependency on an incomplete task
- **[Story]**: the user story the task serves (US1–US7)
- Every task names its file and cites the requirements it implements

## Path Conventions

This is a Spec Kit extension, not an application. There is no `src/`.

- Runtime deliverables: `spectra/commands/defect-rca.md`, `spectra/templates/defect-rca-template.md`
- Manifest and catalog: `spectra/extension.yml`, `catalog.json`
- Roster and docs: `agents-list.json`, `README.md`, `AGENTS_LIST.md`, `docs/index.html`, `spectra/README.md`
- Package: `docs/packages/spectra.zip` (built, never hand-edited)
- Tests: `tests/`

### The six literal strings `CANONICAL` membership demands

Every task that writes prose into `spectra/commands/defect-rca.md` is subject to these. They are exact
substring assertions in `tests/test_doc_output_paths.py`, not paraphrasable:

| Must appear literally | Asserted by | Landed in |
|---|---|---|
| `docs/defect-rca/` | `test_each_document_command_names_its_canonical_folder` | T009 |
| `Artifact root:` | `test_each_document_command_reads_the_declaration` | T009 |
| `never write it` | `test_each_document_command_refuses_to_write_the_declaration` | T009 |
| `mkdocs.yml`, `docusaurus.config`, `docs/_config.yml`, `docs/.nojekyll`, `docs/index.html`, `docs/conf.py` | `test_each_document_command_checks_for_a_published_docs_folder` | T009 |
| `documents/` | `test_each_document_command_prefers_the_non_publishing_fallback` | T009 |

And three prohibitions that sweep **all** command files, not just this one:

- **No absolute output path.** The literal tokens `` `/docs/ ``, ` /docs/`, `` `/brds ``, ` /brds/` fail
  the sweep. Write `docs/defect-rca/`, never `/docs/defect-rca/`, and never put a space or a backtick
  immediately before a leading slash on a path.
- **Every `docs/<slug>/` reference is lowercase kebab-case.** `docs/defect-rca/` passes;
  `docs/Defect-RCA/` does not.
- **A legacy folder (`docs/ADR`, `brds/`) may appear only in a legacy-handling clause** and never on a
  line that also carries a write instruction. This command has no legacy folder of its own, so the
  simplest compliance is to name none.

---

## Phase 1: Setup

**Purpose**: record what "before" looks like, then create the file with its interface and its one
governing rule.

- [X] T001 Record the pre-implementation baseline from the repository root: `python3 tools/generate_agent_docs.py --check` reads **49 agents / 9 prose blocks / roster and manifest agree**; `python3 tools/build_package.py` followed by `git diff --stat docs/packages/spectra.zip` shows no drift; `spectra/extension.yml` is at **1.14.0** with **9** commands and **7** templates, and `catalog.json` agrees at 1.14.0 / 9; `tests/test_roster_data.py` asserts **49 agents, 18 available, 31 planned**; `python3 -m unittest discover -s tests` is green at **965 tests**. Phase 11 asserts these became 50 agents / 10 prose blocks / 1.15.0 / 10 commands / 8 templates / 19 available / 31 planned.
- [X] T002 Create `spectra/commands/defect-rca.md` with YAML front matter carrying a single `description` key in the style of `spectra/commands/impact.md`, an H1 title, and a one-paragraph statement of the job: take a defect from a ticket, an issue, or a description, gather the evidence the repository already holds, test hypotheses against it until a root cause is validated, and write one advisory analysis into the project's artifact root (FR-001, FR-002).
- [X] T003 Add the **User Input** section to `spectra/commands/defect-rca.md` per [contracts/command-interface.md](./contracts/command-interface.md): the whole surface is the defect, passed through the generic arguments placeholder. State that with empty input the command asks what defect to analyze and stops — reading nothing, writing nothing, and inferring nothing from the branch name, recent commits, open issues, or failing tests (FR-009). Use no agent's invocation syntax anywhere in the file (FR-003).
- [X] T004 Add the **one rule that governs everything** section to `spectra/commands/defect-rca.md`, stated once and in full: *the repository answers first — never ask a human for what you can read — and never claim more than the evidence supports.* Name it as the sentence every later rule narrows, in the style of the equivalent section in `spectra/commands/impact.md`. State its two halves explicitly, because they fail in opposite directions: asking for what you could read wastes the one resource the human has, and asserting what you could not read is how an RCA becomes worse than no RCA.

**Checkpoint**: the file exists, declares its input surface, and states its limit.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: the machinery every story depends on — the prohibitions, the honesty rules, channel
detection, root resolution, the shipped template, and template resolution.

**⚠️ CRITICAL**: no user story work can begin until this phase is complete. Every task except T010 edits
the same file and they are strictly sequential.

- [X] T005 Add the **prohibition list** to `spectra/commands/defect-rca.md`, reproducing the write-scope table in [contracts/command-interface.md](./contracts/command-interface.md): never infer a defect from the branch name, commits, issues, or failing tests (FR-009); never prompt for, accept, transmit, or store a credential, API token, or password, and never attempt to authenticate (FR-013); no network request beyond the named ticket or issue retrieval, and no repository URL accepted for cloning (FR-014); exactly two files written per run, both under the defect-rca folder, and nothing else in the repository (FR-055); never generate, apply, or execute a code fix, patch, or configuration change, and never write or modify test code (FR-056); never write back to JIRA or GitHub, create an issue or comment, or transition a ticket (FR-057); never edit the constitution, create a branch, stage, or commit (FR-058); never create or edit a template file (FR-054); never overwrite an existing analysis (FR-043a); never reproduce a secret value (FR-039e). State explicitly that no argument, pasted material, or instruction in the session enables any of them.
- [X] T006 Add the **rules that never bend** section to `spectra/commands/defect-rca.md` — the rules that are the product, per [contracts/document-contract.md](./contracts/document-contract.md) and [research.md](./research.md) D4: (R1) every claim about the code cites the file, and the line where the claim is about a specific behaviour; a claim of absence states what was searched for and where (FR-019). (R2) a hypothesis is never marked validated on evidence that cannot settle it — an inability to disprove is `open`, not `supported` (FR-032). (R3) a runtime fact never observed is never inferred (FR-033). (R4) invalidated hypotheses are recorded, not only the surviving one; recording only confirmations produces justification, not analysis (FR-039a). (R5) the presenting symptom and the validated root cause are stated adjacently and explicitly distinguished (FR-039, FR-027 of the BRD). (R6) a preventive-action verdict of completed or not-completed requires a citation; otherwise the verdict is undeterminable (FR-022). (R7) a secret is located and described, never quoted (FR-039e). State that these stay with the command and are **not** part of the template, in the style of `review-pr`'s equivalent clause.
- [X] T007 Add **Step 1 — Resolve the channel** to `spectra/commands/defect-rca.md` per [contracts/command-interface.md](./contracts/command-interface.md) and [research.md](./research.md) D1: classify the argument by shape — a GitHub host URL containing an issues path, a JIRA key or JIRA URL, else plain prose — and **state the resolved channel before gathering any evidence** (FR-008). State that ambiguity resolves toward plain description, because that is the channel that cannot fail, and that announcing the classification is what makes a misread correctable in one word rather than invisible.
- [X] T008 Add **Step 2 — Retrieve, or degrade** to `spectra/commands/defect-rca.md`: for a GitHub issue, fetch the body **and its comments** with the `gh` CLI, verifying the binary is present and authenticated first and giving the distinct remedy for each failure — install versus `gh auth login` (FR-011). For JIRA, use whatever JIRA access the host agent already provides and nothing else (FR-012). On any failure, name it, ask the user to paste the content, and continue as a plain description (FR-013). State the posture explicitly and give the reason: this command **attempts and degrades** where `create-pr` and `review-pr` hard-gate, because a GitHub issue is one of three channels and a missing `gh` costs a copy-paste rather than the analysis. State that degrading into asking for a token is not degrading but escalating, and is forbidden.
- [X] T009 Add **Step 3 — Resolve where the analysis will live** to `spectra/commands/defect-rca.md`, adapting the equivalent step in `spectra/commands/impact.md` per [research.md](./research.md) D6 and [contracts/document-contract.md](./contracts/document-contract.md). **This task lands all six literal strings the `CANONICAL` entry asserts** — see Path Conventions: a declared `Artifact root:` line wins, matched case-insensitively, rejecting a leading slash or a `..` segment with a stated reason and falling back to the default (FR-040, FR-042); the default is `docs/` **only after** checking for `mkdocs.yml`, `docusaurus.config.*`, `docs/_config.yml`, `docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, or a Pages configuration pointing at `docs`; finding a signal with no declaration, surface it, recommend `documents/`, and take the non-publishing option where the choice cannot be obtained (FR-041); offer the declaration line and **never write it** (FR-058). State the folder as `docs/defect-rca/` under the default root, project-relative, created on demand. State why the publication check matters more here than for any other document agent: an RCA carries stack traces, production timings, and customer-impact figures, and a published `docs/` puts all of it on the web irretrievably.
- [X] T010 [P] Create `spectra/templates/defect-rca-template.md` declaring the sections from [contracts/document-contract.md](./contracts/document-contract.md) in BRD Appendix A's order — the identity block, 1. Root Cause, 2. Problem Statement & Timeline, 3. Supporting Evidence, 4. Impact, 5. Corrective Actions, 6. Preventive Actions — in the style of `spectra/templates/impact-analysis-template.md`. Carry the section structure and the column headings only. Carry **no** citation rule, no verdict rule, no recurrence rule, no secret rule, and no layer ladder: all of those stay with the command (Principle VIII, FR-053). Keep authoring guidance as HTML comments marked as guidance that never reaches the output (FR-039g).
- [X] T011 Add **Step 4 — Resolve the document's template** to `spectra/commands/defect-rca.md`: the five layers in priority order — `.specify/templates/overrides/defect-rca-template.md`, the preset layer, `.specify/extensions/spectra/templates/defect-rca-template.md`, `.specify/templates/defect-rca-template.md`, then the command's own inline skeleton — taking the first readable, non-empty layer, with no single path hard-coded (FR-050). Report the resolved path in the session (FR-052). Honour the resolved sections and their order; note rather than reinstate an omitted section (FR-051). Strip guidance comments and placeholder tokens whichever layer supplied them (FR-039g), and never write a template file (FR-054). State the override path once as the supported customization route, and that editing the installed copy under `.specify/extensions/` is not it, because a version bump discards the edit while the tracked path makes it look durable.
- [X] T012 Add the **rules that survive any template** section to `spectra/commands/defect-rca.md` per FR-053: answer-first ordering, the symptom/root-cause adjacency, the recording of invalidated hypotheses, evidence-source attribution, the advisory status line, the related-prior-RCA field filled either way, and the secret prohibition. State the reason inline so a future editor reads it before relaxing it: a template decides what sections exist, never whether a safety rule applies, and an override that could switch one off would make every project's guarantees different.
- [X] T013 Add the **Budgets** table to `spectra/commands/defect-rca.md` in the style of the equivalent section in `spectra/commands/impact.md`, per [research.md](./research.md) D8: at most **five** clarifying questions per round; at least **five** major hypothesis-tree branches; at least **four** major issue-tree branches. State that the root-resolution question of Step 3 does not count against the question budget because it is about where to write rather than about the defect, and that reaching a cap is a disclosure, never a silent stop.
- [X] T014 Add the **secret rule** to `spectra/commands/defect-rca.md` in the style of the equivalent clause in `spectra/commands/impact.md`: user-supplied logs, configuration and stack traces are the most likely carrier of a credential in any Spectra command, and this document gets **committed to the repository**. Name the shapes to watch for; require the finding to be rewritten as kind-and-location before it may be recorded; require the substitution to be stated in the session (FR-039e). State that over-withholding is the correct error to make.

**Checkpoint**: the prohibitions, the never-bend rules, channel detection, retrieval and degradation,
root resolution, both the shipped template and its resolution, the budgets, and the secret rule are all
in place. User story work can begin.

---

## Phase 3: User Story 1 — Start the analysis with the evidence already gathered (Priority: P1) 🎯 MVP

**Goal**: a QE engineer hands over a defect and gets back what the repository already knows — implicated
code, recent commits, configuration, tests, the constitution's bearing, a MECE hypothesis tree, and a
short prioritized question list — instead of a questionnaire.

**Independent Test**: invoke against a repository with a seeded defect description, no prior RCA corpus,
no constitution, and no ticket system reachable; verify a hypothesis tree of at least five branches, a
statement of what was and was not examined, and at most five questions come back, and that no file is
created.

- [X] T015 [US1] Add **Step 5 — Read the project** to `spectra/commands/defect-rca.md`: read `.specify/memory/constitution.md` where it exists and **name by heading** which principles bear on this analysis (FR-015); then the source, configuration, tests and commit history relevant to the reported symptoms (FR-016). State that an absent constitution is stated once and the run continues on methodology alone.
- [X] T016 [US1] Add the **scan scoping** rules to `spectra/commands/defect-rca.md` per FR-017: scope the scan **outward from the symptom**, never exhaustively, and state both which areas of the codebase were examined and which were not. State the reason inline: on a large or unfamiliar repository an exhaustive scan is not available, so the only honest bound is a stated one — an unstated gap reads to the user as coverage.
- [X] T017 [US1] Add the **repository-state** rules to `spectra/commands/defect-rca.md` per FR-018: record the repository and the exact commit analyzed, and ask the user to confirm the deployed version **before** hypotheses are built on this code. State why it comes early rather than at synthesis: a wrong branch or an undeployed change makes every subsequent finding describe code that was never running, and discovering that at the end wastes the whole analysis.
- [X] T018 [US1] Add the **citation** rules to `spectra/commands/defect-rca.md` per FR-019 and R1: every claim about the code names the file, and the line where the claim is about a specific behaviour; a claim that something is absent states what was searched for and where. State that "there is no retry limit" without a stated search is not evidence, and that where repository-wide text search is unavailable the run says so and reports reduced coverage rather than narrowing silently.
- [X] T019 [US1] Add **Step 6 — Build the hypothesis tree** to `spectra/commands/defect-rca.md` per FR-025 and [data-model.md](./data-model.md): at least five major branches drawn from Code/Logic, Design/Architecture, Process/Practice, Environment/Configuration, Data, People/Knowledge, and Organizational/Systemic, or the domain-specific equivalents the project warrants. State the MECE discipline in both directions — a hypothesis belongs to exactly one branch, and a finding that fits no branch means a branch is added rather than the finding being filed under the nearest match.
- [X] T020 [US1] Add the **tree rendering** format to `spectra/commands/defect-rca.md` per [contracts/chat-output.md](./contracts/chat-output.md): branch, then each hypothesis with its **layer**, its **status**, and its evidence with source and locator. State that the tree is rendered in the session and **never written to disk** (FR-036), and state why — a written hypothesis tree would be a second artifact type needing its own folder under Principle VII, and the BRD excludes it from the output contract for the same reason.
- [X] T021 [US1] Add **Step 7 — Ask** to `spectra/commands/defect-rca.md` per FR-029 and [research.md](./research.md) D8: identify what cannot be obtained from the repository, and ask at most five questions ordered by which answer would most change the current hypothesis ranking, **each stating why it matters**. Give the question format from [contracts/chat-output.md](./contracts/chat-output.md). State that the stakes line is what lets a user answer three and skip two deliberately rather than abandoning the round, and that an unbounded list is never really prioritized because nothing is left out of it.
- [X] T022 [US1] Add the **intake report** to `spectra/commands/defect-rca.md` per [contracts/chat-output.md](./contracts/chat-output.md): the resolved channel and retrieval outcome; the constitution principles that bear, by heading; prior RCAs surfaced or the corpus searched and nothing matched; what was examined and what was not; the repository and commit with the deployed-version request; the hypothesis tree; the questions. State that intake writes nothing.

**Checkpoint**: a defect description produces gathered evidence, a hypothesis tree, and a prioritized
question list, with nothing written. This is the MVP.

---

## Phase 4: User Story 2 — Catch the defect we have already fixed once (Priority: P1)

**Goal**: a defect matching a prior analysis is flagged **at intake**, with that analysis's root cause,
its preventive actions, and an assessment of whether those actions appear to have landed.

**Independent Test**: seed the RCA folder with a prior document, run intake on a defect with overlapping
symptoms, and verify the prior is surfaced with its matching axis, its root cause, and a cited verdict
per preventive action.

- [X] T023 [US2] Add **Step 8 — Search the corpus** to `spectra/commands/defect-rca.md` per [contracts/recurrence-contract.md](./contracts/recurrence-contract.md): read the index at `docs/defect-rca/README.md` under the resolved root if present, and **fall back to reading the documents themselves** when the index yields nothing (FR-021, FR-047). State the index's status inline — a cache of the corpus, never the corpus — and that nothing found in it means *read the documents*, never *no match exists*. State that an empty or absent folder proceeds without error and without prompting (FR-023).
- [X] T024 [US2] Add the **three match axes** to `spectra/commands/defect-rca.md` per [research.md](./research.md) D2: implicated-code overlap (strongest — a file or module named in the prior document's evidence table also appears in this defect's traced paths), symptom overlap (a normalized status, exception type, timeout or corruption shape), and root-cause overlap (the prior mechanism appears in this hypothesis tree). State that **title similarity is not an axis** and may only order results, and that the firing axis and the concrete overlap are always disclosed so a spurious match can be dismissed in one sentence.
- [X] T025 [US2] Add the **preventive-action verdict** rules to `spectra/commands/defect-rca.md` per FR-022 and [research.md](./research.md) D3: exactly three verdicts — `apparently completed` requiring a citation, `apparently not completed` requiring a citation of the absence, `undeterminable` requiring a reason. State that **undeterminable is the default** and that a bare "done" or "not done" is never emitted. State the reason inline: an uncited "completed" on an action that was never finished suppresses the exact recurrence signal this whole step exists to raise, so the command must under-claim and let the human check.
- [X] T026 [US2] Add the **surfaced-match format** to `spectra/commands/defect-rca.md` from [contracts/recurrence-contract.md](./contracts/recurrence-contract.md): the prior id, the axis, the concrete overlap, the root cause quoted, and each preventive action with its verdict and its citation or reason.
- [X] T027 [US2] Add the **what a match changes** clause to `spectra/commands/defect-rca.md`: the prior root cause enters the hypothesis tree as a named branch at whatever layer it sat; the new document's header carries the prior by id; the index row's related column is populated; the completion report names which priors were surfaced and on which axis (FR-024, FR-045, FR-060).
- [X] T028 [US2] Add the **no-match** clause to `spectra/commands/defect-rca.md` per FR-024: where nothing matched, the header records that the search **ran and found nothing** — never blank, never omitted. State the reason inline, from the BRD's template commentary: filling the field either way is what distinguishes "searched, nothing found" from "the search was skipped", and only one of those is a finding.

**Checkpoint**: a recurrence is visible at intake with an auditable basis and cited verdicts.

---

## Phase 5: User Story 3 — Test hypotheses against the code (Priority: P1)

**Goal**: the loop settles what the repository can settle, spends questions only on what it cannot, and
keeps peeling back past the first plausible code path.

**Independent Test**: pose a source-testable hypothesis and verify the command investigates and reports
rather than asking; then state a surface symptom and verify it proposes a deeper probe and names the
current layer.

- [X] T029 [US3] Add **Step 9 — The loop** to `spectra/commands/defect-rca.md` per [data-model.md](./data-model.md): form hypotheses with a **proposed test stated at formation, not after**; track each as open, supported, weakened, invalidated, or validated; refine the remaining branches as evidence lands (FR-027). Carry the legal state transitions, including that `validated` and `invalidated` are terminal for the evidence in hand, that reopening is legal but must be explicit, and that `invalidated → validated` never happens without new evidence.
- [X] T030 [US3] Add the **repository-answers-first** rule to `spectra/commands/defect-rca.md` per FR-028: test a hypothesis against the repository wherever the evidence is obtainable there, and never ask the user for anything readable. Give the concrete cases — which function handles the retry, whether a timeout is configurable, when a line last changed — and state that each is a question the command must answer for itself.
- [X] T031 [US3] Add the **five-layer ladder** to `spectra/commands/defect-rca.md` per FR-026 and [research.md](./research.md) D4: symptom, immediate technical cause, contributing factors, process and practice gaps, systemic and organizational root cause. Require **every probe to state its layer**, and state why that is not decoration: a session whose probes are all at layers one and two is visibly shallow while it is still cheap to fix.
- [X] T032 [US3] Add the **plausible-path** rule to `spectra/commands/defect-rca.md` per D4: a plausible code path is a layer-two **finding**, never a conclusion — name what was found *and* ask what allowed it to reach production, which is the missing test, the review that did not catch it, or the configuration never validated. State the failure mode inline, from the BRD risk register: code access produces false confidence precisely because the plausible path is genuinely there and genuinely related.
- [X] T033 [US3] Add the **running view** to `spectra/commands/defect-rca.md` per [contracts/chat-output.md](./contracts/chat-output.md): each round reports which hypotheses moved and on what evidence, the validated / supported / weakened / invalidated / open tallies, the open data gaps, the current deepest layer, and the next questions within budget.
- [X] T034 [US3] Add the **data gap** rules to `spectra/commands/defect-rca.md` per [data-model.md](./data-model.md): a gap carries the question, its priority, its status of open, closed or unobtainable, and — for any gap still open at synthesis — what its remaining open costs the conclusion's confidence (FR-031).
- [X] T035 [US3] Add the **two negative rules** to `spectra/commands/defect-rca.md`, stated as their own clause because they are the ones a helpful model breaks: never answer your own question (FR-032), and never infer a runtime fact — a log line, a metric, an environment state, a timestamp — that you did not observe or receive (FR-033). State that an inability to disprove a hypothesis makes it `open`, not `supported`.
- [X] T036 [US3] Add the **Non-interactive mode** section to `spectra/commands/defect-rca.md` in the style of the equivalent section in `spectra/commands/impact.md`, per FR-031: proceed on repository evidence alone, write the document, and record every unanswered question as an open data gap with its confidence cost stated. State that a document naming what it could not establish is useful and a refusal is not, and that the prohibitions of T035 apply unchanged — a session that cannot ask is not a licence to guess. Where a root would have been chosen after a publication signal, take the non-publishing option and say so.

**Checkpoint**: the loop settles what it can, asks for the rest, tracks status honestly, and refuses to
stop at layer two.

---

## Phase 6: User Story 4 — Leave a document the next person can act on (Priority: P1)

**Goal**: synthesis produces a template-shaped, answer-first analysis at the next free number, with the
index row beside it and nothing else in the repository touched.

**Independent Test**: run synthesis against a set of validated and invalidated hypotheses; verify all
nine elements are present, the root cause leads, the file lands at the next unused number, and
`git status` shows exactly two new files.

- [X] T037 [US4] Add **Step 10 — Synthesize** to `spectra/commands/defect-rca.md` per FR-038 and FR-039: restate the validated root cause **answer first**, with the presenting symptom adjacent and explicitly distinguished. State the nine required elements and where each lands in the resolved template.
- [X] T038 [US4] Add the **layer-two synthesis block** to `spectra/commands/defect-rca.md` per [research.md](./research.md) D4: where the deepest validated finding is an immediate technical cause, say so, name what would be needed to go deeper, and **do not promote it to root cause**. State that this is the single most likely way the document becomes a restated symptom with a heading over it.
- [X] T039 [US4] Add the **identity block** rules to `spectra/commands/defect-rca.md` per FR-038a: defect id, source reference — the JIRA key, the issue URL, or `direct prompt` — repository and commit analyzed, severity, related prior RCA, owner and date, and the advisory status line. State that a field that cannot be established **records that fact** rather than being omitted or invented.
- [X] T040 [US4] Add the **ownership** rules to `spectra/commands/defect-rca.md` per FR-039d: take the owner from the repository's configured Git author and offer it for correction; where no name is readable, record the owner as unassigned. Never invent a name. State that the advisory status line is never softened, reworded, or dropped, because it is what makes the document advisory rather than a directive.
- [X] T041 [US4] Add the **evidence table** rules to `spectra/commands/defect-rca.md` per FR-039a: one row per hypothesis with its status, what settled it, and its source attributed as code, commit, config, test, or user-supplied. Require invalidated and weakened rows where they exist. State that the source column is what makes the repository-answers-first claim checkable, and that a user-supplied finding is never relabelled as code because the command later confirmed it — that is a second row, not an edit.
- [X] T042 [US4] Add the **impact and actions** rules to `spectra/commands/defect-rca.md` per FR-039b, FR-039c and FR-034: quantify impact — severity, frequency, cost, risk, customer and business effect — where data exists or can be elicited, and where it cannot, **say so rather than omit the section**. Keep corrective and preventive actions in separate sections, each row naming an owner and a verification criterion, and flag a preventive action that merely restates a corrective one as a sign the analysis did not reach a root cause.
- [X] T043 [US4] Add the **nothing-validated** clause to `spectra/commands/defect-rca.md` per FR-039f: record that no root cause was validated, name what was ruled out, and state what evidence would settle it. State that a speculative cause must never be promoted to fill the section, and that an analysis which honestly eliminated five branches is worth more than one that guessed a sixth.
- [X] T044 [US4] Add the **out-of-reach** clause to `spectra/commands/defect-rca.md`: where the root cause lies outside the repository the command can read — another service, another repository, a vendor — name it as out of reach and report what was established locally, rather than forcing a local explanation. This is the monorepo and multi-repo limitation the spec records under Assumptions.
- [X] T045 [US4] Add **Step 11 — Number it and write it** to `spectra/commands/defect-rca.md` per [contracts/document-contract.md](./contracts/document-contract.md) and FR-043: `NNN-<slug>.md` under `docs/defect-rca/` at the resolved root, `NNN` zero-padded three digits scoped to that folder, **one greater than the highest already present — not a count of files** — starting at `001`, independent of the `specs/` sequence. The slug is lowercase, hyphen-separated, three to five words, naming the **observed problem and never the suspected cause**. Give the worked examples from the contract, including the wrong ones. State the reason for the symptom slug: the file is named before the analysis concludes, so a cause-named file is wrong exactly when the analysis is interesting.
- [X] T046 [US4] Add the **write-once** rules to `spectra/commands/defect-rca.md` per FR-043a and FR-043b: the document and the index row are written together as the run's **final act**, with the number resolved at that moment; a run that stops earlier leaves the folder exactly as it found it, with no partial document and no number consumed; an existing file is never overwritten, replaced, or amended; a file whose name does not match the convention is read for context, ignored for numbering, reported once, and left alone. State that a parallel-branch collision resolves at merge like any other file conflict.
- [X] T047 [US4] Add **Step 12 — The index** to `spectra/commands/defect-rca.md` per [contracts/index-contract.md](./contracts/index-contract.md): `README.md` in the same folder, one row per document carrying id, symptom, root cause, related prior RCA, and rolled-up preventive-action status — **rebuilt from the documents actually present** on every run that writes, so a hand-added or hand-deleted file self-corrects (FR-046). Include the table shape from the contract. State once more that it is a cache and never the corpus.

**Checkpoint**: synthesis produces a complete, correctly located, correctly numbered analysis and an
index row, and touches nothing else.

---

## Phase 7: User Story 5 — Explore a defect class before a defect exists (Priority: P1)

**Goal**: a practitioner can work through a whole failure class — intermittent failures, performance
degradation, data integrity — with a navigable issue tree and per-node discovery questions, writing
nothing.

**Independent Test**: request exploration of a named defect class; verify a MECE tree of at least four
major branches with sub-nodes and per-node questions comes back and that no file is created.

- [X] T048 [US5] Add **Exploration mode** to `spectra/commands/defect-rca.md` per FR-035: reached by naming or describing a defect **class** rather than a defect. Present the corresponding issue tree or fishbone with at least four major branches and sub-nodes, with tailored discovery questions at each node, and help rank branches by likelihood and impact. Record confirmed, refuted, and still-open nodes as the user navigates.
- [X] T049 [US5] Add the **exploration writes nothing** clause to `spectra/commands/defect-rca.md` per FR-035, and the **carry-over** clause: where an exploration turns into a real defect, the confirmed and refuted nodes carry into intake rather than the analysis starting over. State that exploration is the only mode useful with no defect in hand, which is why it exists separately from the tree Step 6 builds.
- [X] T050 [US5] Add the **McKinsey 7-Step** clause to `spectra/commands/defect-rca.md` per FR-035 and BR-13: map the process explicitly when the user asks for structured problem-solving support. Apply the methodology faithfully **without reproducing substantial portions of the copyrighted texts that describe it** (FR-059) — the same constraint the BRD sets, stated in the command so it survives a reader who has not read the BRD.

**Checkpoint**: a defect class can be explored end to end with nothing written.

---

## Phase 8: User Story 6 — Write where the project says, in the shape the project says (Priority: P1)

**Goal**: a project that declares an artifact root and ships a template override gets its document in
its folder with its sections in its order, and is told which layer resolved.

**Independent Test**: declare `Artifact root: documents/`, supply an override with a section removed, run
synthesis; verify the file lands under the declared root with the override's sections, the omission is
reported rather than repaired, and the resolved path is named.

> The machinery this story depends on lands in Phase 2 (T009, T011, T012), because User Story 4 cannot
> write without it. This phase adds the behaviours that are specifically about **honouring a project's
> own conventions** rather than resolving them.

- [X] T051 [US6] Add the **omission reporting** clause to `spectra/commands/defect-rca.md` per FR-051: where the resolved template omits a section the command would ordinarily fill, report the omission and do **not** reinstate the section. State the reason inline — reinstating turns a team's override into a suggestion — and pair it with the FR-053 exception already stated in T012, so a reader sees both halves together: sections are the template's, safety rules are the command's.
- [X] T052 [US6] Add the **superseded folder** clause to `spectra/commands/defect-rca.md` per FR-043c: a folder from an earlier convention — including the default root once a project declares a different one — is read for context and for numbering continuity, so the next number is one greater than the highest found across the canonical folder *and* every superseded one. Report it once, name the canonical folder, and offer the move as a command the user runs. Never move, rename, modify, or delete anything there. **Write this clause without naming any pre-1.6.0 folder**: `tests/test_doc_output_paths.py` sweeps every command file for `docs/ADR` and `brds/` outside a legacy-handling context, and this command has no legacy folder of its own to discuss.
- [X] T053 [US6] Add the **template layer reporting** clause to `spectra/commands/defect-rca.md` per FR-052: name the resolved path in the completion report. State the reason — an override that failed to apply is otherwise indistinguishable from one that applied, and the user's first clue would be a wrongly-shaped document in review.
- [X] T054 [US6] Add the **root determination reporting** clause to `spectra/commands/defect-rca.md` per FR-060: report the artifact root used and **how it was determined** — declared, default, or chosen after a publication signal. State that "declared" and "defaulted to the same value" look identical in the resulting path, and only one of them will survive a project adding a declaration later.
- [X] T055 [US6] Add **Step 13 — Report** to `spectra/commands/defect-rca.md` per [contracts/command-interface.md](./contracts/command-interface.md), pulling T053 and T054 into one section together with: the path written; the commit analyzed; which prior RCAs were surfaced and on which axis; and what could not be examined. State that the session gets the summary while the document gets the detail.

**Checkpoint**: a project's declared root and template override are both honoured and both reported.

---

## Phase 9: User Story 7 — Coach the practitioner (Priority: P2)

**Goal**: after synthesis, the practitioner can ask how the analysis went and get specific feedback with
at least one concrete improvement.

**Independent Test**: complete an analysis, request reflection, verify feedback covers all four
dimensions with a concrete improvement; request it with no analysis and verify it declines.

- [X] T056 [US7] Add **Reflection mode** to `spectra/commands/defect-rca.md` per FR-037: evaluate analysis depth, hypothesis-testing rigour, data-gap closure, and answer-first structure, with **at least one concrete improvement** rather than generic encouragement. State that reflection writes nothing.
- [X] T057 [US7] Add the **nothing to reflect on** clause to `spectra/commands/defect-rca.md` per FR-037: requested before any analysis has run, say so rather than inventing an assessment. Add the **coaching techniques** clause per FR-034 and BR-11 in the same section: peel-back questioning, hypothesis-validation phrasing, triangulation, and magic-wand framing, offered where they help rather than recited.

**Checkpoint**: all seven stories are independently exercisable.

---

## Phase 10: Publishing Surface (Principle V)

**Purpose**: make the command real to a consumer. These touch different files and are the only genuinely
parallel work in the plan — except where a task reads another's output.

- [X] T058 [P] Register both artifacts in `spectra/extension.yml`: add `speckit.spectra.defect-rca` → `commands/defect-rca.md` to `provides.commands` with the description from [contracts/command-interface.md](./contracts/command-interface.md); add `defect-rca-template` → `templates/defect-rca-template.md` to `provides.templates` with the override path and the command-owned rules in its description, in the style of the seven entries already there; bump `extension.version` 1.14.0 → **1.15.0**; add the tags `root-cause-analysis`, `defect-analysis`, and `rca` (FR-001, FR-061). The manifest is swept by `tests/test_doc_output_paths.py` for legacy folders — name none.
- [X] T059 [P] Add a `[1.15.0]` entry to `spectra/CHANGELOG.md` recording the new command and registered template, and the four decisions a reader would otherwise find surprising: it **attempts and degrades** on `gh` rather than gating, and never asks for a credential; it searches the **prior RCA corpus at intake**, not at synthesis, and reports a cited verdict on each earlier preventive action; it **refuses to call a layer-two finding a root cause**; and it writes **two** files — the analysis and a rebuilt index — and nothing else.
- [X] T060 [P] Add the roster entry to `agents-list.json`: `id: defect-rca`, `title: Defect Root Cause Analysis`, a one-line description, `status: available`, `phase: testing-quality`, `type: add-on`, `provider: spectra`, `command: speckit.spectra.defect-rca` — matching the shape of the `flaky-test-detector` entry. A `command` key is required exactly because the status is `available`. `tests/test_roster_data.py` asserts titles are unique; verify `Defect Root Cause Analysis` collides with none of the 49 existing titles before committing (FR-006).
- [X] T061 Regenerate every structured listing with `python3 tools/generate_agent_docs.py` (depends on T058, T060): the Agents table in `README.md`, the Spec Kit core and Roadmap sections of `AGENTS_LIST.md`, and the Commands table in `spectra/README.md`. Do not hand-edit anything between the `SPECTRA:GENERATED` markers (FR-065, Principle V).
- [X] T062 Hand-author the prose block in `AGENTS_LIST.md` anchored `<!-- SPECTRA:AGENT id=defect-rca -->` (depends on T060), in the style of the nine blocks already there: what it does, the three input channels and what happens when one is unreachable, that it reads the code before it asks you anything, that it checks whether you have analyzed this defect before, where it writes and that the file names the symptom rather than the cause, that conclusions stay yours, and what you do with it next. Automation guarantees the block exists, never what it says (FR-065).
- [X] T063 Hand-author the per-command prose section in `spectra/README.md` as `## speckit.spectra.defect-rca — Defect Root Cause Analysis` (depends on T061), matching the nine sections already there. **This is not optional**: `tools/generate_agent_docs.py --check` asserts a shipped agent's canonical title appears in `spectra/README.md` outside the generated region, and the check fails without it — the lesson recorded in `specs/021-test-plan-agent/tasks.md` Phase 10.
- [X] T064 [P] Add the command to `docs/index.html` in the commands list, with an example invocation naming a defect, matching the nine entries already there. Do not hard-code the version or the description — the page reads those from `catalog.json` and `agents-list.json` at load (FR-064, Principle V).
- [X] T065 Update the `spectra` entry in `catalog.json` (depends on T058): `version` → 1.15.0, `provides.commands` 9 → **10**, both `updated_at` fields, and the new tags — the values must match `spectra/extension.yml` exactly or the `catalog` job in `.github/workflows/ci.yml` fails (FR-062).
- [X] T066 Rebuild the package with `python3 tools/build_package.py` (depends on T010, T058, and the finished command file) and confirm `docs/packages/spectra.zip` contains `spectra/commands/defect-rca.md` and `spectra/templates/defect-rca-template.md` under a single top-level `spectra/` folder (FR-063).

**Checkpoint**: a consumer running `spectra install` would get the command, and every published surface
agrees with the extension folder.

---

## Phase 11: Validation

**Purpose**: prove the rules survived contact with the file, and that an agent actually follows them.

- [X] T067 [P] Create `tests/test_defect_rca_flow.py` in the style of `tests/test_impact_flow.py`, asserting on the text of `spectra/commands/defect-rca.md`: the manifest registration (`file: "commands/defect-rca.md"`); the three channels and the state-the-channel-first rule (**SC-011**); the empty-input gate and the inference prohibition naming the branch, commits, issues, and failing tests; the two write targets and no third; the citation rule in both directions (**SC-006**); the layer ladder with the layer-two synthesis block; the never-answer-your-own-question and never-infer-a-runtime-fact rules; the three recurrence axes **with title excluded** (**SC-007**); the three-valued verdict with citations mandatory and `undeterminable` as default; the nothing-validated clause; the write-once-at-the-end ordering and the never-overwrite rule (**SC-010**); the index-is-a-cache fallback; and the no-session-file rule. Assertions read **whitespace-normalized** text, per the lesson in `specs/021-test-plan-agent/tasks.md` T060 — the command file is hard-wrapped, so a rule that straddles a line break must still match.
- [X] T068 [P] Add the **credential prohibition** assertion to `tests/test_defect_rca_flow.py`: sweep the command file for any instruction that would request, accept, or store a token, password, API key, or credential, and assert the file instead contains the explicit refusal (FR-013). This is the highest-consequence rule in the feature — a shipped prompt that asks a user for a JIRA token is a phishing surface distributed in a zip — and it is cheap to assert, so it gets its own test rather than a clause in T067.
- [X] T069 [P] Add the **degrade-don't-gate** assertion to `tests/test_defect_rca_flow.py`: assert the command names both `gh` failure modes with their distinct remedies (install versus `gh auth login`) and that each leads to continuing in plain-description mode rather than stopping — the posture that distinguishes this command from `create-pr` and `review-pr`, which hard-gate. Pin it in both directions so neither a silent hard-gate nor a silent removal of the check passes.
- [X] T070 [P] Add `"defect-rca.md": "docs/defect-rca/"` to `CANONICAL` in `tests/test_doc_output_paths.py`. This single line enrols the command in every Principle VII sweep the module already runs — the canonical folder, the `Artifact root:` declaration, the literal `never write it`, all six publication signals, and the `documents/` recommendation. Add no new assertion logic: the point of the entry is that the existing assertions apply. Run the module immediately and fix the command file rather than the test if any of the six literals is missing.
- [X] T071 [P] Add `"defect-rca.md": "defect-rca-template"` to `DOCUMENT_COMMANDS` in `tests/test_document_templates.py`, which asserts registration both ways, heading parity between the shipped template and the command's inline skeleton, all four resolution layers present in the command, the override layer named first, the command reporting the template it used, an inline last resort, no hard-coded template path, and no executable asset.
- [X] T072 [P] Add the **numbering** assertion to `tests/test_defect_rca_flow.py`: the command states the sequence is **one greater than the highest present** and explicitly not a count of files, and that the slug names the observed problem rather than the suspected cause. Both are rules a future edit would plausibly "simplify" away, and both fail silently in production — a count-based sequence collides after a deletion, and a cause-named slug is wrong exactly when the analysis is interesting.
- [X] T073 [P] Update the census in `tests/test_roster_data.py`, verified against the module during planning: 49 → **50** agents; 18 → **19** available, renaming the split method to `..._nineteen_available_...`; **31** planned unchanged; `test_nine_available_agents_come_from_spec_kit` unchanged at 9; and add `"defect-rca"` to the sorted id list in `test_spectra_ships_exactly_nine_agents_today`, renaming it to `test_spectra_ships_exactly_ten_agents_today`. The list is sorted, so `"defect-rca"` goes between `"create-pr"` and `"domain-analyzer"`.
- [X] T074 Run the full gate from the repository root (depends on T058–T073): `python3 -m unittest discover -s tests` green, `python3 tools/generate_agent_docs.py --check` reporting **50 agents and 10 prose blocks** with roster and manifest agreeing, and `python3 tools/build_package.py && git diff --stat docs/packages/spectra.zip` showing no drift.
- [X] T075 Install the working copy into a throwaway Spec Kit project with `specify extension add --dev` per [quickstart.md](./quickstart.md), and run Passes 1 through 6, recording the observed result for each. These passes are where the observable success criteria are actually measured: **SC-005** (all nine elements, root cause leading), **SC-006** (hypotheses settled from source rather than by asking), **SC-007** (recurrence surfaced at intake), **SC-010** (nothing written outside the folder, nothing overwritten), **SC-011** (every run reports path, template layer, root and determination, commit), **SC-012** (declared root and override both honoured), **SC-013** (no secret in the written document), **SC-014** (defect to document in one session without external documentation). Record which passes were executed and which were not — a deferred pass recorded as done is the one failure mode this row exists to prevent.
  > **Partially executed 2026-09-11.** A throwaway Spec Kit project was created with
  > `specify init --here --force --non-interactive --integration claude` and the working copy installed
  > with `specify extension add --dev`. Registration verified: **10 commands and 8 templates** at the
  > extension layer, `defect-rca-template.md` present under `.specify/extensions/spectra/templates/`,
  > and `speckit-spectra-defect-rca` registered as a skill.
  >
  > A probe was then built — an orders module with an unbounded `while True` retry loop and no backoff,
  > a pool sized 5 and commented "sized for the sequential batch importer, 2023", a single happy-path
  > test, a constitution carrying a bounded-retry principle and a concurrency-testing principle, and a
  > **seeded prior RCA (`001-invoice-email-duplicates`) whose two preventive actions were never
  > completed**. The prior RCA was deliberately given a *different* implicated file from the new defect,
  > so a match could only come from the root-cause axis rather than the strongest one.
  >
  > The command's steps were followed against it and the document produced. **25 of 25 assertions on the
  > output passed**, covering Passes 1 through 4 and 6: all six template sections in order with the root
  > cause leading and the symptom adjacent; **two invalidated hypotheses recorded**, including the
  > "recent regression" hypothesis killed by `git log`; every evidence row attributed to Code / Commit /
  > Config / Test; three `path:line` citations and three cited absences; severity recorded as *not
  > established* rather than guessed; impact stated as not quantifiable rather than omitted; the owner
  > taken from the real Git author; the analyzed commit recorded; the related-prior-RCA row naming
  > `001`; no placeholder or guidance comment surviving; numbering at `002` with `001` byte-identical;
  > and `git status --porcelain` showing **exactly two** paths — the analysis and the index.
  >
  > **Two assertions of mine were wrong and the document was right.** The evidence-row check matched the
  > Markdown separator row (`|---|---|`) because its pipe count passes a naive row filter, and the
  > citation check counted only `src/` locators while one real citation is `config/db.yaml:2`. Both were
  > corrected and both then passed. Worth recording because it is the same lesson spec 021 hit: a naive
  > assertion over a document the command wrote correctly fails in the direction that looks like a
  > command defect.
  >
  > **The recurrence check is the one that earned its keep.** Searching `docs/` for an audit document —
  > the evidence that RCA 001's first preventive action had landed — returned RCA 001 itself, because
  > the action's own *text* contains the word. Treating that as evidence of completion would have
  > produced an uncited "apparently completed" on an action nobody did, which is exactly the failure
  > FR-022 exists to prevent. The verdict recorded is *apparently not completed*, citing what was
  > searched and that the only match is the action text.
  >
  > **Pass 4 was executed mechanically only.** A declared `Artifact root: documents/` and an override
  > removing section 4 and renaming section 2 were both placed, and the resolution inputs verified: the
  > declaration is found, the override resolves ahead of the installed copy, the two diverging sections
  > are identifiable, and the superseded folder holds two numbered documents so continuity demands
  > `003`. Whether an agent *honours* the override and reports the omission rather than reinstating it
  > needs a fresh agent session.
  >
  > **Not executed as live agent runs: Pass 5's behavioural probes** — the empty-argument gate, the `gh`
  > degradation and credential refusal, and the layer-2 synthesis block. Each needs an interactive
  > session with the command registered and the agent restarted, which cannot be driven from inside the
  > session that authored the command. The credential refusal is the significant gap:
  > `tests/test_defect_rca_flow.py` proves the refusal is written down, not that a model obeys it.

- [ ] T076 Run Passes 1, 3, and 5 on a **second agent** — the intake gate, recurrence detection, and the negative invariants — because those are where a prompt-expressed rule is most likely to be quietly ignored by a different model, and none is catchable by `tests/test_defect_rca_flow.py`, which can only assert that the *instruction* is present. The credential refusal (T068) and the layer-two synthesis block are the two to watch hardest: both are rules a helpful model has a strong prior to break. Record the results in `test/README.md`.
  > **Not executed.** It needs a different model in an interactive session with the extension
  > installed, which the authoring session cannot provide. Recorded as outstanding rather than waived:
  > the three behaviours it targets — the empty-argument gate, the credential refusal, and the layer-2
  > synthesis block — are all prompt-expressed, and `tests/test_defect_rca_flow.py` asserts only that
  > each rule is written down, never that a model follows it. If any regresses on another agent, this
  > row is where to look first, and the `test/README.md` rows added by T077 are where a result would go.

- [X] T077 [P] Add the manual pass rows to `test/README.md` covering the five things only a human can confirm: an empty invocation reads nothing and writes nothing; a missing `gh` degrades without ever asking for a token; a pasted API key is described rather than quoted; a layer-two finding is refused as a root cause; and a prior RCA with an unfinished preventive action is surfaced at intake with a cited verdict.

**Checkpoint**: the rules are asserted in the suite, and an agent has been observed following them.

---

## Phase 12: Publish (Constitution Development Workflow step 6)

- [X] T078 Verify the two facts CI will check before pushing: `spectra/extension.yml` and `catalog.json` agree on **1.15.0** and **10** commands, and the committed zip matches the `spectra/` folder. Nothing in `tests/` catches either — the `catalog` job in `.github/workflows/ci.yml` is the only guard.
- [X] T079 Commit the whole set on branch `022-defect-rca-agent`: `spectra/`, `specs/022-defect-rca-agent/`, `agents-list.json`, `catalog.json`, `docs/`, `README.md`, `AGENTS_LIST.md`, `test/README.md`, and `tests/`.
  > **Done 2026-09-11** — 28 files, 4123 insertions, 10 deletions, on branch
  > `022-defect-rca-agent`. Not pushed.

- [ ] T080 Open the pull request for branch `022-defect-rca-agent` with `speckit.spectra.create-pr` — the extension's own `after_implement` hook — and confirm the body states the 1.15.0 bump, the new `spectra/commands/defect-rca.md` and `spectra/templates/defect-rca-template.md`, the four decisions from T059, and the three departures from `BRD-DEFECTRCA-001 v2.0.0` with a pointer to the plan section that argues them.

---

## Dependencies & Execution Order

### Phase dependencies

- **Phase 1 (Setup)**: no dependencies.
- **Phase 2 (Foundational)**: depends on Phase 1. **Blocks every user story.** T009 in particular blocks
  US4 entirely — nothing can be written until the root resolves.
- **Phases 3–9 (US1–US7)**: all depend on Phase 2. They edit the same file, so they are sequential in
  practice even though they are logically independent.
- **Phase 10 (Publishing)**: depends on the command file and template being complete (Phases 1–9).
- **Phase 11 (Validation)**: depends on Phase 10. T070 and T071 will fail until the command file carries
  the literals they assert, which is by design — they are the gate, not a formality.
- **Phase 12 (Publish)**: depends on Phase 11 passing.

### Story dependencies

| Story | Depends on | Why |
|---|---|---|
| US1 (intake) | Phase 2 | Needs channel detection and retrieval |
| US2 (recurrence) | Phase 2, and US1 for the traced code paths the strongest match axis uses | The implicated-code axis has nothing to compare against before the scan runs |
| US3 (loop) | US1 | The loop refines a tree US1 builds |
| US4 (synthesis) | US1, US3, and **T009** | Writes the result of the loop, to the resolved root |
| US5 (exploration) | Phase 2 only | Genuinely independent — it is the one mode that needs no defect |
| US6 (conventions) | **T009, T011, T012** in Phase 2 | Adds honouring and reporting on top of resolution |
| US7 (reflection) | US4 | Reflects on a completed analysis |

US5 is the only story that could be built and demonstrated entirely on its own.

### Within each phase

Tasks editing `spectra/commands/defect-rca.md` are **strictly sequential** — they append sections to one
file. Only T010 (the template) is parallel within Phase 2.

### Parallel opportunities

- **Phase 10**: T058, T059, T060, T064, T077 are genuinely parallel — different files. T061 depends on
  T058 and T060; T062 on T060; T063 on T061; T065 on T058; T066 on T010, T058 and the command file.
- **Phase 11**: T067–T073 are all parallel — different test modules, or different assertions added to
  different files. T074 depends on all of them.

---

## Parallel Example: Phase 10

```bash
# Four different files, no ordering between them:
Task: "Register both artifacts in spectra/extension.yml and bump to 1.15.0"
Task: "Add the [1.15.0] entry to spectra/CHANGELOG.md"
Task: "Add the roster entry to agents-list.json"
Task: "Add the command to the commands list in docs/index.html"
```

```bash
# Phase 11, all parallel — different modules:
Task: "Create tests/test_defect_rca_flow.py"
Task: "Add defect-rca.md to CANONICAL in tests/test_doc_output_paths.py"
Task: "Add defect-rca.md to DOCUMENT_COMMANDS in tests/test_document_templates.py"
Task: "Update the census in tests/test_roster_data.py"
```

---

## Implementation Strategy

### MVP (User Story 1 only)

1. Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1).
2. **Stop and validate**: Pass 1 in [quickstart.md](./quickstart.md). A defect description produces
   gathered evidence, a hypothesis tree, and a question list, with nothing written.
3. That alone is shippable value: it is the hour of manual code archaeology the BRD's problem statement
   opens with.

### Incremental delivery

1. Setup + Foundational → the file exists and knows its limits.
2. + US1 → **MVP**: evidence gathering and a hypothesis tree.
3. + US2 → recurrence visible at intake.
4. + US3 → the loop narrows honestly.
5. + US4 → the durable document. **This is the first phase that writes anything.**
6. + US5, US6, US7 → exploration, project conventions, coaching.
7. Phase 10 → publishable. Phase 11 → guarded. Phase 12 → published.

### The order that is not negotiable

T009 before anything in US4. T010 before T066. T070 and T071 after the command file is complete, never
before — they assert literals that Phase 2 and Phase 8 land.

---

## Notes

- `[P]` = different file, no dependency on an incomplete task.
- Every task naming `spectra/commands/defect-rca.md` is subject to the six literal strings and three
  prohibitions under **Path Conventions**. Re-read that table before writing any prose into the file.
- Write every path **project-relative**: `docs/defect-rca/`, never `/docs/defect-rca/`, and never a
  space or backtick immediately before a leading slash.
- This command has no legacy output folder. The simplest way to pass the legacy sweep is to name none.
- Commit after each task or logical group. Stop at any checkpoint to validate a story independently.
- Two rules are worth more scrutiny than the rest in review, because a helpful model has a strong prior
  to break both: the credential refusal (T005, T008, T068) and the layer-two synthesis block (T038).
