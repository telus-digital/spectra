---

description: "Task list for feature 040: one source of truth for every agent"
---

# Tasks: One Source of Truth for Every Agent

**Input**: Design documents from `specs/040-agent-single-source/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included. The plan names new test modules, the repository's own rule is that every behavior
lands with standard-library `unittest` coverage, and SC-004/SC-005 are verified by tests.

**Organization**: Tasks are grouped by user story. The three P1 stories are ordered US3 → US1 → US2
because the roster built in US3 is what every other output is rendered from.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: The user story the task belongs to (US1–US5)
- Paths are repository-relative. Run Python as `python3`, which must be 3.9 compatible: no `match`,
  no `tomllib`, and no 3.10+ APIs.

---

## Phase 1: Setup

**Purpose**: Create the source directory and seed every header from today's data.

- [X] T001 Create the `agents/` directory at the repository root and `specs/040-agent-single-source/seed/` for the one-off seeding scripts (research D8)
- [X] T002 Write `specs/040-agent-single-source/seed/seed_headers.py`.
  - **Inputs**: it reads `agents-list.json` and `spectra/extension.yml`.
  - **`agents/_phases.md`**: one `---`/`---` block per phase (`id`, `title`, `aidlc`), in today's order.
  - **One `agents/<id>.md` per agent**, 55 in all:
    - Each file gets a header block with keys in this order: `id, title, command, provider, type, phase, order, status, summary, manifest`.
    - `summary` is the roster `description`.
    - `order` is 10, 20, 30, … within each phase, in today's roster order.
    - `command` is omitted when the roster has none.
    - `manifest` is set only for shipped agents (`provider: spectra` and `status: available`), copied from that command's `description:` in `spectra/extension.yml`.
    - Values are written literally, after the first `": "`, with no quoting (contracts/agent-source-format.md, Header).
- [X] T003 Run `python3 specs/040-agent-single-source/seed/seed_headers.py`, then confirm that `agents/` holds 55 agent files plus `_phases.md`, and that every shipped file's `command` equals `speckit.spectra.<id>`

---

## Phase 2: Foundational (blocking)

**Purpose**: The parser, the Markdown renderer, and the generator core that every story depends on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T004 [P] Create `tools/agent_source.py` (standard library only).
  - **Header parsing** (research D1):
    - The first line is `---`, and the header ends at the next `---`.
    - Each line is `key: value`, split on the first `": "`.
    - A blank line, a comment, or a repeated key inside the header is an error.
  - **Loading**: `load(directory)` returns phases, in file order, and agents sorted by (phase position, `order`).
  - **Validation rules 1–6 and 11** from data-model.md:
    - A file that is neither `_phases.md` nor `<slug>.md` is an error.
    - Unknown, duplicate or missing keys are errors.
    - Enum rules: `provider` ∈ {`speckit`, `spectra`}, `type` ∈ {`core`, `add-on`}, `status` ∈ {`available`, `planned`}.
    - `order` is a positive integer, and the pair (`phase`, `order`) is unique.
    - `id` equals the file name, and `phase` must exist in `_phases.md`.
    - `manifest` is required on shipped agents and forbidden on all others.
    - A body is required on shipped agents and forbidden on all others.
  - **Errors**: raise `SourceError`, with every message starting `agents/<file>:<line>:`.
  - **Derived values**: `shipped` and `number` (01–14) on each agent.
- [X] T005 [P] Create `tools/markdown_subset.py` (standard library only, research D5, contracts/agent-source-format.md "Markdown subset").
  - **Block parser**:
    - Blocks: paragraph, `- ` and `1. ` lists with nesting by indentation, fenced code with an optional info string, pipe tables, and `##` headings.
    - The parser keeps each block's source line numbers and the author's line breaks.
  - **Inline parser**:
    - Code spans are extracted first.
    - All other text goes through `html.escape`, then `**…**` becomes `<b>`, `*…*` becomes `<i>`, and `[text](url)` becomes a link when the URL is http(s), a `#anchor`, or a relative path.
    - Backslash escapes are supported.
  - **Renderers**: `to_markdown(blocks, indent)` re-indents without ever rewrapping. `to_html(blocks)` and `inline_html(text)` return HTML.
  - **Rejections**, each raising `MarkdownError` with the line: any heading other than `##`, `>` blockquotes, images, reference links, `<` followed by a letter or `/` outside code, `&…;` entities, unclosed `**`, `*`, `` ` `` or fences, and non-http link schemes.
- [X] T006 Add a body splitter to `tools/agent_source.py` (rule 7, research D3, contracts/agent-source-format.md "Body").
  - It parses each shipped body with `markdown_subset` into: the lead (the first paragraph, inline only), further prose, items (every `##` section up to and including `Examples`), and guides (every `##` section after `Examples`).
  - It enforces the rules: `Arguments` is first and a single paragraph, `Use it when` is second, and `Examples` is the last item and exactly one fenced block with at least one non-empty line.
  - It records an item's joiner: a plain space when the label ends in `.`, `?` or `!`, and ` — ` otherwise.
- [X] T007 [P] Write `tests/test_agent_source.py`.
  - It covers every validation rule in data-model.md items 1–7 against temporary directories, asserting each message names the file and line or field.
  - It also covers: a summary containing `: `, quotes and `—` round-tripping literally; ordering by (phase, order); two agents sharing `speckit.implement`; and a body on a planned agent being rejected.
- [X] T008 [P] Write `tests/test_markdown_subset.py`.
  - **Positive cases**: every allowed construct renders to the expected Markdown and HTML, including nested and ordered lists, a table, and a fence with `bash`.
  - **Escaping**: `<`, `>` and `&` are escaped in text and inside code.
  - **Rejections**: every rejected construct raises with its line number.
  - **Joiner rule**: covered for items.
- [X] T009 Rework the core of `tools/generate_agent_docs.py` (research D6, D7).
  - **Input**: replace the `agents-list.json` input with `agent_source.load(REPO_ROOT / "agents")`.
  - **Roster**: build the roster dict with keys in the order `id, title, description, status, phase, type, provider, command`, omitting `command` when absent. Pass it through `spectra_cli.roster.parse(data, strict=True)` and feed the existing four renderers from the result.
  - **Outputs**: introduce an output registry with three kinds: `whole`, `region`, and `line`. A line target must be found exactly once, or the run fails naming the file.
  - **Notice**: change it to `<!-- Generated from agents/ — do not edit by hand. Run: python3 tools/generate_agent_docs.py -->`.
  - **Guarantees**:
    - When the source is invalid, nothing is written.
    - Writes stay bytes with `\n` endings.
    - The CLI surface (`--check`) and `run(check)` are unchanged, so `tools/checks.py` keeps working.
  - **Docstring**: update the module docstring to describe `agents/` as the input.

**Checkpoint**: `python3 -m unittest tests.test_agent_source tests.test_markdown_subset` passes; the generator loads the seeded headers.

---

## Phase 3: User Story 3 — Installed tools and the live site keep working (P1)

**Goal**: `agents-list.json` becomes a generated output, byte-identical to today's file.

**Independent Test**: Generate from the seeded source and run `cmp` against `git show main:agents-list.json`, then run the roster tests unchanged.

- [X] T010 [US3] Register `agents-list.json` as a `whole` output in `tools/generate_agent_docs.py`, rendered as `json.dumps(data, indent=2, ensure_ascii=False) + "\n"` with `schema_version` taken from the current file's value (`"1.0"`) as a constant in the generator
- [X] T011 [US3] Run `python3 tools/generate_agent_docs.py`, then confirm three things. First, `cmp` against `git show main:agents-list.json` reports the two files identical. Second, the `readme-agents-table`, `agents-list-speckit-core`, `agents-list-roadmap` and `spectra-readme-commands` regions are byte-unchanged. Third, `git diff --stat` shows nothing outside `agents/`.
- [X] T012 [US3] Rework the sandbox in `tests/test_generator.py`.
  - Copy `agents/`, `agents-list.json`, `README.md`, `AGENTS_LIST.md`, `spectra/README.md`, `spectra/extension.yml`, `spectra/commands/`, and the whole of `docs/` except `docs/packages/` into the sandbox.
  - Patch the generator's `REPO_ROOT` and its source and output paths. Replace `edit_roster` with an `edit_agent(root, id, mutate)` helper that rewrites a source file.
  - Add tests: the generated roster is byte-identical to the committed file, and a hand edit to `agents-list.json` fails `--check` and names the file.
- [X] T013 [US3] Run `python3 -m unittest tests.test_roster_data tests.test_roster tests.test_agent_list tests.test_no_hardcoded_agents tests.test_net` and confirm they pass with no change to what they assert (SC-004)

**Checkpoint**: The roster file is generated and every consumer is unaffected.

---

## Phase 4: User Story 1 — Change an agent's description in one place (P1) 🎯 MVP

**Goal**: The two long-form outputs and every description line are rendered from the 14 shipped source files.

**Independent Test**: quickstart.md §2 and §3. Change one sentence in `agents/adr.md`, and every output showing it changes. Hand-edit an output, and `--check` names it.

### Seeding the long descriptions (FR-015, FR-016)

Rules for T014–T017, applied to each agent:
- **Base**: the agent's `AGENTS_LIST.md` block. The lead is the text after ``**`<command>`** — ``, without that prefix. Further paragraphs stay as written. Each `- **Label** — text` bullet becomes `## Label`, with `Example(s) (Claude)` becoming `## Examples` and its fence kept.
- **README-only material** from that agent's `spectra/README.md` section becomes guides (`## <Title>` after `## Examples`). This covers numbered walkthroughs, "Somewhere other than `docs/`?", upgrade notes, and the `###` template-override subsections. Keep its line breaks.
- **Restatements**: drop README sentences that only restate the base.
- **Constraints**: `## Arguments` must be one paragraph. Every raw `<word>` must be wrapped in backticks, and every entity replaced with its character.

- [X] T014 [P] [US1] Write the bodies of `agents/domain-analyzer.md`, `agents/methodology.md`, `agents/kb-vault.md` and `agents/test-strategy.md` per the rules above
- [X] T015 [P] [US1] Write the bodies of `agents/brd.md`, `agents/impact.md`, `agents/test-plan.md` and `agents/adr.md` per the rules above
- [X] T016 [P] [US1] Write the bodies of `agents/uat.md`, `agents/flaky-test-detector.md` and `agents/defect-rca.md` per the rules above. In `agents/uat.md` the first example line must be exactly `/speckit-spectra-uat`, and in `agents/test-plan.md` it must be exactly `/speckit-spectra-test-plan`.
- [X] T017 [P] [US1] Write the bodies of `agents/create-pr.md`, `agents/review-pr.md` and `agents/deployment-strategy.md` per the rules above

### Rendering

- [X] T018 [US1] Add the region `agents-list-shipped` to `AGENTS_LIST.md` (contracts/generated-outputs.md row 3, research D4).
  - **Markers**: the region spans from after the "Install them all at once…" paragraph under `## Shipped Spectra agents` to before `## Spec Kit core agents`. Keep the `---` separator outside the region.
  - **Renderer**: `render_agents_list_shipped` in `tools/generate_agent_docs.py`. Per shipped agent, in roster order, it emits:
    - `<!-- SPECTRA:AGENT id=<id> -->` and `### <title> ✅`
    - ``**`<command>`** — <lead>``, then the further prose
    - the item list, using the joiner rule; the Examples label is `Example (Claude)` for one line and `Examples (Claude)` otherwise, and the fence is indented two spaces
    - each guide as `#### <title>` followed by its blocks
- [X] T019 [US1] Add the region `spectra-readme-agents` to `spectra/README.md` (contracts/generated-outputs.md row 7).
  - **Markers**: the region spans from the first ``## `speckit.spectra.`` heading to before `## License, trademarks, and disclaimer`.
  - **Renderer**: `render_spectra_readme_agents`. Per shipped agent it emits ``## `<command>` — <title>``, the lead, further prose, the item list, `### <guide>` sections, and then `---`.
  - The text must be identical to the `AGENTS_LIST.md` text for each agent.
- [X] T020 [US1] Register the line outputs in `tools/generate_agent_docs.py` (rows 8 and 9). These are the named lines Principle V (2.1.0) permits.
  - **`spectra/extension.yml`**: the `      description: "…"` line that follows `- name: "speckit.spectra.<id>"` and its `file:` line.
  - **`spectra/commands/<id>.md`**: the `description: "…"` line inside the opening `---` block.
  - **Value**: both use the agent's `manifest`, with `\` escaped as `\\` and `"` as `\"`.
- [X] T021 [US1] In `tools/generate_agent_docs.py`, remove `check_prose_anchors` and `check_title_containment`, and their calls from `run()`. Make `--check` print one `<path>: generated output does not match agents/. Run: python3 tools/generate_agent_docs.py` line per stale output (FR-018), and update its success message.
- [X] T022 [US1] Run `python3 tools/generate_agent_docs.py` and review `git diff` on `AGENTS_LIST.md`, `spectra/README.md`, `spectra/extension.yml` and `spectra/commands/*.md`. Then run every flow and documentation test, with no edits to the tests (SC-004): `python3 -m unittest tests.test_adr_flow tests.test_uat_flow tests.test_test_plan_flow tests.test_onboarding_sequence tests.test_doc_output_paths tests.test_document_templates tests.test_extension` plus every other `tests/test_*_flow.py`. Fix any failure in `agents/<id>.md`, never in a test or a generated output.
- [X] T023 [US1] Write `specs/040-agent-single-source/seed/seed_report.py` and run it to produce `specs/040-agent-single-source/seeding-report.md` (FR-016, research D8).
  - **Sources**: for each shipped agent, it reads the old copies from `main` with `git show main:<path>`: the `AGENTS_LIST.md` block, the `spectra/README.md` section, the `docs/getting-started/agents.html` card text, and the old `spectra/commands/<id>.md` description.
  - **Comparison**: it splits each copy into sentences, normalizes whitespace and strips Markdown and HTML markup, then lists every sentence not found verbatim in the new `agents/<id>.md`.
  - **Classification**: for each missing sentence, find the closest sentence in the new source with `difflib.SequenceMatcher`. A ratio ≥ 0.6 is marked `reworded`, with that source sentence quoted as the pointer; anything lower is marked `dropped`. The implementer may change a `dropped` entry to `merged` only by adding a note naming where the content now lives.
  - **Output**: the listing is grouped per agent and per copy, each sentence carrying its mark.
- [X] T024 [US1] Add US1 tests to `tests/test_generator.py`:
  - Editing the lead in `agents/adr.md` changes `AGENTS_LIST.md`, `spectra/README.md` and the agents page, and nothing else.
  - Editing `summary` changes `agents-list.json` and the `spectra-readme-commands` table.
  - Editing `manifest` changes `spectra/extension.yml` and `spectra/commands/adr.md` identically.
  - A hand edit inside each new region fails `--check` and names the file.
  - Two consecutive runs are byte-identical.
  - A run writes no `\r`.
  - Hand-written text outside regions and line targets is byte-identical after a run.

**Checkpoint**: MVP. One source edit propagates to every long-form output, and drift is caught.

---

## Phase 5: User Story 2 — Add a new agent by adding one file (P1)

**Goal**: A new source file is all it takes; mismatches with the manifest are named.

**Independent Test**: quickstart.md §4.

- [X] T025 [US2] Rewrite `check_manifest_agreement` in `tools/generate_agent_docs.py` to compare the shipped sources against the `speckit.spectra.*` commands registered in `spectra/extension.yml` (FR-019). It names each side of a mismatch and also fails when `spectra/commands/<id>.md` is missing for a shipped agent. It runs in both write and check modes.
- [X] T026 [US2] Add US2 tests to `tests/test_generator.py`:
  - A new planned header-only file appears in `agents-list.json` and the roadmap region only.
  - A new shipped file not registered in the manifest fails and names the command, and a registered command with no source fails too.
  - Removing `## Examples` from a shipped file fails as `agents/<id>.md:<line>` with nothing written.
  - An `order` inserted between two existing agents lands in that position in every output.
  - A title change keeping the id propagates to every output.

**Checkpoint**: The roster can grow by one file.

---

## Phase 6: User Story 4 — The Agent reference page builds itself (P2)

**Goal**: The sidebar and cards of `docs/getting-started/agents.html` are generated static HTML with a collapsed Full reference.

**Independent Test**: quickstart.md §6 and §7. The page works with JavaScript disabled, and an unknown command on a narrative page fails `--check`.

- [X] T027 [US4] In `docs/getting-started/agents.html`, wrap the sidebar links inside `<nav class="scen-nav-track">` in the region `agents-page-nav`, and the cards inside `<ul class="cmds">` in the region `agents-page-cards`, using the same HTML comment markers. Leave the head, intro, `scen-head`, copy-button and scroll-spy scripts outside the regions.
- [X] T028 [US4] Implement `render_agents_page_nav` and `render_agents_page_cards` in `tools/generate_agent_docs.py`, exactly per contracts/agents-page-markup.md.
  - **Card content**:
    - `.cdesc` holds the lead via `inline_html`, and `.args` holds `<b>Arguments:</b>` plus the Arguments paragraph via `inline_html`.
    - The Examples label is `Example (Claude)` or `Examples (Claude)`, followed by one `<pre><code>` per example line.
    - The card ends with `<details class="fullref"><summary>Full reference</summary><div class="fullref-body">…</div></details>` holding the whole body via `to_html`, with items as `<ul class="items">` and guides as `<h4>`.
  - **Invariants**: no `<span>` inside `.cdesc` or `.args`; `<details>` comes after every `<pre>`; all text is escaped.
- [X] T029 [P] [US4] Add styles for `details.fullref`, `details.fullref > summary`, `.fullref-body` (including its `p`, `ul`, `ol`, `table`, `h4` and `pre`) and `ul.items` to `docs/getting-started/getting-started.css`, consistent with the existing card tokens. Change nothing else in the file.
- [X] T030 [US4] Add the narrative-page guard to `--check` in `tools/generate_agent_docs.py` (FR-024). It scans every `docs/**/*.html` and `docs/**/*.md`, plus the text outside generated regions in `README.md` and `spectra/README.md`, for `speckit\.spectra\.([a-z0-9-]+)` and `/speckit-spectra-([a-z0-9-]+)`, and reports `<path>: names <command>, which agents/ does not ship` for each name that is not a shipped id.
- [X] T031 [US4] Run `python3 tools/generate_agent_docs.py`, then run `python3 -m unittest tests.test_adr_flow tests.test_uat_flow tests.test_test_plan_flow` unchanged
- [X] T032 [US4] Add US4 tests to `tests/test_generator.py`:
  - The page has 14 sidebar links and 14 cards in roster order, numbered 01–14.
  - `.cdesc` and `.args` contain no `<span>`.
  - In each card, the first `<pre><code>` is the first example line and `<details class="fullref">` follows the last `<pre>`.
  - The Full reference text, with markup stripped, equals the agent's `AGENTS_LIST.md` text with markup stripped (SC-006).
  - Emphasis carries over (US4 acceptance scenario 3): every `**…**`, `*…*` and `` `…` `` span in an agent's lead appears in its `.cdesc` as `<b>…</b>`, `<i>…</i>` and `<code>…</code>` respectively.
  - The page contains no `fetch(` added by the generator.
  - An unknown `speckit.spectra.adrx` in a sandboxed narrative page fails `--check` and names the page.
- [X] T033 [US4] Start the `docs` preview from `.claude/launch.json` and open `/getting-started/agents.html`. Check that the page renders with JavaScript disabled, that each Full reference opens in place, that the sidebar scroll-spy still works with JavaScript on, and that there is no horizontal scroll at 375 px wide.

**Checkpoint**: The page is generated, and narrative pages are guarded.

---

## Phase 7: User Story 5 — The constitution names the source (P3)

**Goal**: Principle V matches what was built.

**Independent Test**: Read Principle V; it names `agents/`, the `order` field, and every generated output.

- [X] T034 [US5] Compare Principle V in `.specify/memory/constitution.md` (2.0.1) with the outputs actually registered in `tools/generate_agent_docs.py`, and with the header fields accepted by `tools/agent_source.py`. Report any mismatch for a `/speckit-constitution` run, and do not edit the constitution here. If the Sync Impact Report comment is still at the top of the file, remove it.

---

## Phase 8: Polish & Cross-Cutting

- [X] T035 [P] Update `CONTRIBUTING.md`, `SHIPPING.md` and `CLAUDE.md` (FR-008, FR-023).
  - Adding or changing an agent now means editing or creating `agents/<id>.md` and running `python3 tools/generate_agent_docs.py`.
  - `agents-list.json` and the generated outputs are described as generated, never as places to edit.
  - Add `agents/` to CONTRIBUTING's repository tree.
  - Update CLAUDE.md's "The roster is the source of truth" section and its generated-region table to the new regions.
- [X] T036 [P] Update the docstrings and user-facing messages in `tools/checks.py`, so `check_generated_listings` names `agents/`. Keep the check name `generated-listings`, its CI step, and the `Catalog and package stay in sync` job unchanged (FR-020). Check that `tests/test_ci_contract.py` still passes.
- [X] T037 Bump the extension in `spectra/extension.yml` for the changed shipped text (research D10).
  - Set `version: "1.29.0"` in `spectra/extension.yml`.
  - Add a `## [1.29.0] - <date>` entry to `spectra/CHANGELOG.md` covering the unified command descriptions and the regenerated README sections.
  - Update the `spectra` entry in `catalog.json`.
  - Run `python3 tools/build_package.py` to rebuild `docs/packages/spectra.zip`.
  - Leave `VERSION` untouched (Principle VI).
- [X] T038 Run the full validation: `python3 -m unittest discover -s tests`, then `python3 tools/checks.py --all`, then `python3 tools/ship.py --dry-run`, then quickstart.md §1–§9. Record any failure rather than skipping it.

---

## Dependencies & Execution Order

- **Constitution commits**: the Sync Impact Report comment at the top of `.specify/memory/constitution.md` is temporary. Strip it in whichever commit first includes the amended constitution, including a commit made by an optional `git.commit` hook, rather than waiting for T034.

- **Setup (T001–T003)** → **Foundational (T004–T009)** → all stories.
- **US3 (T010–T013)** comes first among the stories: it proves the source reproduces the roster, which every other renderer reads.
- **US1 (T014–T024)** depends on US3. T014–T017 (seeding) come before T018–T022, and T023 runs after T022.
- **US2 (T025–T026)** depends on US1's registry (T020, T021).
- **US4 (T027–T033)** depends on the seeded bodies (T014–T017) and the renderer (T005). It is independent of US2.
- **US5 (T034)** comes after US1, US2 and US4.
- **Polish (T035–T038)**: T035 and T036 can start after T021. T037 comes after every shipped-file change, and T038 is last.

### Within the foundation

- T004 and T005 are parallel. T006 needs both. T007 needs T004 and T006. T008 needs T005. T009 needs T004–T006.

## Parallel Opportunities

- T004 ∥ T005, then T007 ∥ T008.
- T014 ∥ T015 ∥ T016 ∥ T017: four groups of different files.
- T029 (CSS) runs alongside T027 and T028.
- T035 ∥ T036.

```text
# Seeding, in parallel:
T014 agents/{domain-analyzer,methodology,kb-vault,test-strategy}.md
T015 agents/{brd,impact,test-plan,adr}.md
T016 agents/{uat,flaky-test-detector,defect-rca}.md
T017 agents/{create-pr,review-pr,deployment-strategy}.md
```

## Implementation Strategy

1. **MVP** is Setup + Foundational + US3 + US1 (through T024).
   - At that point the roster is generated byte-identically, every long-form output and description line is rendered from `agents/`, and drift fails `--check`.
   - Stop and validate with quickstart.md §1–§3 and §8.
2. **US2**: the manifest agreement and one-file additions.
3. **US4**: the Agent reference page and the narrative guard.
4. **US5 + Polish**: the constitution cross-check, docs, version bump, package rebuild, and the full pre-flight.
   - Land everything through `python3 tools/ship.py`, never `git push origin main`.

---

## Phase 9: Convergence

- [X] T039 Restore the README-only material that seeding dropped, per FR-015 and FR-016 (partial). `specs/040-agent-single-source/seeding-report.md` marks 28 sentences from the old `spectra/README.md` sections as **dropped**, including upgrade notes ("An analysis an earlier version left at …"), re-run behaviour ("Re-running offers your previous answers …") and template-override paths. FR-015 requires them to move into the source. For each shipped agent, review the dropped `spectra/README.md` sentences. Move every upgrade note, re-run rule and override path into `agents/<id>.md` as a titled guide section after Examples, or into an existing guide section. A sentence that only restates the lead or the existing items stays out, but it must be changed to `merged` in the report's NOTES with a pointer to where its content lives. Then run `python3 tools/generate_agent_docs.py` and regenerate the report with `python3 specs/040-agent-single-source/seed/seed_report.py`. Done when no dropped `spectra/README.md` sentence remains that carries a fact absent from `agents/`.
- [X] T040 Name the agent file when the built roster is rejected, per FR-021 (partial). Today `tools/generate_agent_docs.py` `build_roster` reports `agents/: the roster it builds is invalid (agent 'uat' is planned but records a command.)`, which names only the directory. Validate in `tools/agent_source.py` that a planned agent records no `command`, reported as `agents/<id>.md:<line>: a planned agent records no command`. Add a test in `tests/test_agent_source.py`. Make the `build_roster` fallback name `agents/<id>.md` when the roster error names an agent.
